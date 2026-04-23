from datetime import time

class Medico:

    def __init__(self, nome: str, inicio: time, fim: time):
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self._agenda = []

    def __contains__(self, nova_consulta: 'Consulta'):
        for consulta_agendada in self._agenda:
            if consulta_agendada.horario == nova_consulta.horario:
                return True
        return False

    def agendar(self, consulta: 'Consulta'):
        if consulta.horario < self.inicio or consulta.horario >= self.fim:
            raise ValueError("O medico nao esta disponivel neste horario.")
        if consulta in self:
            raise ValueError("O medico ja possui um paciente neste horario.")

        self._agenda.append(consulta)
        return True
    
class Consulta:

    def __init__(self, horario: time, medico: Medico, paciente: str):
        self.horario = horario
        self.medico = medico
        self.paciente = paciente