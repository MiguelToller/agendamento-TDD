from datetime import time, datetime, timedelta
from src.exceptions import (
    HorarioIndisponivelError,
    ConflitoHorarioError,
    TurnoInvalidoError,
    ConsultaNaoEncontradaError,
    DiaIndisponivelError,
)
import uuid
from src.enums import DiaSemana


class Paciente:

    def __init__(self, nome: str, cpf: str, telefone: str) -> None:
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone


class Agenda:

    def __init__(self, inicio: time, fim: time, dias_atendimento: list[DiaSemana] | None = None) -> None:

        self.inicio = inicio
        self.fim = fim

        if dias_atendimento is None:
            self.dias_atendimento = [
                DiaSemana.SEGUNDA,
                DiaSemana.TERCA,
                DiaSemana.QUARTA,
                DiaSemana.QUINTA,
                DiaSemana.SEXTA,
            ]
        else:
            self.dias_atendimento = dias_atendimento

        self.__consultas = []

    def __contains__(self, consulta_nova: "Consulta") -> bool:
        for consulta_agendada in self.__consultas:
            if consulta_nova.inicio < consulta_agendada.fim and consulta_agendada.inicio < consulta_nova.fim:
                return True
        return False

    @property
    def consultas(self) -> tuple["Consulta"]:
        return tuple(self.__consultas)

    def agendar(self, consulta: "Consulta") -> bool:
        data_da_consulta = consulta.inicio.date()
        
        limite_inicio_turno = datetime.combine(data_da_consulta, self.inicio)
        limite_fim_turno = datetime.combine(data_da_consulta, self.fim)

        if consulta.inicio < limite_inicio_turno or consulta.fim > limite_fim_turno:
            raise HorarioIndisponivelError("O medico nao atende neste horario.")
        if consulta in self:
            raise ConflitoHorarioError("O medico ja possui um paciente neste horario.")
        dia_da_semana = DiaSemana(consulta.inicio.weekday())
        if dia_da_semana not in self.dias_atendimento:
            raise DiaIndisponivelError("O medico nao atende neste dia da semana.")

        self.__consultas.append(consulta)
        return True

    def cancelar(self, consulta_id: str) -> bool:

        for consulta in self.__consultas:
            if consulta.id == consulta_id:
                self.__consultas.remove(consulta)
                return True
        raise ConsultaNaoEncontradaError("Esta consulta nao foi encontrada na agenda do medico.")

    def buscar_consulta(self, consulta_id: str) -> "Consulta":

        for consulta in self.__consultas:
            if consulta.id == consulta_id:
                return consulta
        raise ConsultaNaoEncontradaError("Consulta nao encontrada no sistema.")


class Medico:

    def __init__(self, nome: str, inicio: time, fim: time, dias_atendimento: list[DiaSemana] | None = None) -> None:

        if inicio > fim:
            raise TurnoInvalidoError("O termino do turno nao pode ser anterior ao inicio.")
        if inicio == fim:
            raise TurnoInvalidoError("O turno nao pode ter duracao de zero minutos.")

        self.nome = nome
        self.agenda = Agenda(inicio, fim, dias_atendimento)


class Consulta:

    DURACAO_CONSULTA_MIN = 30

    def __init__(self, data_hora: datetime, medico: Medico, paciente: Paciente) -> None:
        self.id = str(uuid.uuid4())
        self.medico = medico
        self.paciente = paciente
        self.inicio = data_hora
        self.fim = data_hora + timedelta(minutes=self.DURACAO_CONSULTA_MIN)

    def __str__(self) -> str:
        data_formatada = self.inicio.strftime("%d/%m/%Y")
        hora_formatada = self.inicio.strftime("%H:%M")
        return f"Consulta de {self.paciente.nome} no dia {data_formatada} as {hora_formatada}"

    @classmethod
    def criar(cls, horario_str: str, medico: Medico, paciente: Paciente) -> "Consulta":
        hoje = datetime.today()
        data_hora = datetime.strptime(horario_str, "%H:%M").replace(year=hoje.year, month=hoje.month, day=hoje.day)
        return cls(data_hora, medico, paciente)
