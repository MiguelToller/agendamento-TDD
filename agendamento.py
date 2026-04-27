from datetime import time, datetime, timedelta
from exceptions import HorarioIndisponivelError, ConflitoHorarioError, TurnoInvalidoError, ConsultaNaoEncontradaError
import uuid

class Medico:

    def __init__(self, nome: str, inicio: time, fim: time) -> None:
        if inicio > fim:
            raise TurnoInvalidoError("O termino do turno nao pode ser anterior ao inicio.")
        if inicio == fim:
            raise TurnoInvalidoError("O turno nao pode ter duracao de zero minutos.")
        
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self.__agenda = []

    @property
    def agenda(self) -> tuple['Consulta']:
        return tuple(self.__agenda)

    def __contains__(self, consulta_nova: 'Consulta') -> bool:
        for consulta_agendada in self.__agenda:
            if consulta_nova.inicio < consulta_agendada.fim and \
               consulta_agendada.inicio < consulta_nova.fim:
                return True
        return False

    def agendar(self, consulta: 'Consulta') -> bool:
        hora_inicio_consulta = consulta.inicio.time()
        hora_fim_consulta = consulta.fim.time()

        if hora_inicio_consulta < self.inicio or hora_fim_consulta > self.fim:
            raise HorarioIndisponivelError("O medico nao atende neste horario.")
        if consulta in self:
            raise ConflitoHorarioError("O medico ja possui um paciente neste horario.")

        self.__agenda.append(consulta)
        return True
    
    def cancelar(self, consulta: 'Consulta') -> bool:
        
        for consulta in self.__agenda:
            if consulta.id == consulta.id:
                self.__agenda.remove(consulta)
                return True
        raise ConsultaNaoEncontradaError("Esta consulta nao foi encontrada na agenda do medico.")
    
class Consulta:

    DURACAO_CONSULTA_MIN = 30

    def __init__(self, data_hora: datetime, medico: Medico, paciente: str) -> None:
        self.id = str(uuid.uuid4())
        
        self.medico = medico
        self.paciente = paciente
        self.inicio = data_hora
        self.fim = data_hora + timedelta(minutes=self.DURACAO_CONSULTA_MIN)

    def __str__(self) -> str:
        data_formatada = self.inicio.strftime("%d/%m/%Y")
        hora_formatada = self.inicio.strftime("%H:%M")  
        return f"Consulta de {self.paciente} no dia {data_formatada} as {hora_formatada}"

    @classmethod
    def criar(cls, horario_str: str, medico: Medico, paciente: str) -> 'Consulta':
        hoje = datetime.today()
        data_hora = datetime.strptime(horario_str, "%H:%M").replace(
            year=hoje.year, month=hoje.month, day=hoje.day
        )
        return cls(data_hora, medico, paciente)