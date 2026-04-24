from datetime import time, datetime, timedelta
from exceptions import HorarioIndisponivelError, ConflitoHorarioError, TurnoInvalidoError

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
        if consulta.inicio < self.inicio or consulta.fim > self.fim:
            raise HorarioIndisponivelError("O medico nao atende neste horario.")
        if consulta in self:
            raise ConflitoHorarioError("O medico ja possui um paciente neste horario.")

        self.__agenda.append(consulta)
        return True
    
class Consulta:

    def __init__(self, data_hora: datetime, medico: Medico, paciente: str) -> None:
        self.medico = medico
        self.paciente = paciente

        self.inicio = data_hora.time()
        self.fim = (data_hora + timedelta(minutes=30)).time()

    def __str__(self) -> str:
        hora_formatada = self.inicio.strftime("%H:%M")
        return f"Consulta de {self.paciente} com Dr(a). {self.medico.nome} as {hora_formatada}"

    @classmethod
    def criar(cls, horario_str: str, medico: Medico, paciente: str) -> 'Consulta':
        hoje = datetime.today()
        data_hora = datetime.strptime(horario_str, "%H:%M").replace(
            year=hoje.year, month=hoje.month, day=hoje.day
        )
        return cls(data_hora, medico, paciente)