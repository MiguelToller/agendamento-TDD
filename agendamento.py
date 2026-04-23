from datetime import time, datetime, timedelta
from exceptions import HorarioIndisponivelError, ConflitoHorarioError

class Medico:

    def __init__(self, nome: str, inicio: time, fim: time):
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self._agenda = []

    def __contains__(self, consulta_nova: 'Consulta'):
        for consulta_agendada in self._agenda:
            if consulta_nova.inicio < consulta_agendada.fim and \
               consulta_agendada.inicio < consulta_nova.fim:
                return True
        return False

    def agendar(self, consulta: 'Consulta'):
        if consulta.inicio < self.inicio or consulta.fim > self.fim:
            raise HorarioIndisponivelError("O medico nao atende neste horario.")
        if consulta in self:
            raise ConflitoHorarioError("O medico ja possui um paciente neste horario.")

        self._agenda.append(consulta)
        return True
    
class Consulta:

    def __init__(self, data_hora: datetime, medico: Medico, paciente: str):
        self.medico = medico
        self.paciente = paciente

        self.inicio = data_hora.time()
        self.fim = (data_hora + timedelta(minutes=30)).time()

    @classmethod
    def criar(cls, horario_str: str, medico: Medico, paciente: str):
        hoje = datetime.today()
        data_hora = datetime.strptime(horario_str, "%H:%M").replace(
            year=hoje.year, month=hoje.month, day=hoje.day
        )
        return cls(data_hora, medico, paciente)