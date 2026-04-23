from datetime import time

class Medico:

    def __init__(self, nome: str, inicio: time, fim: time):
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self._agenda = []

    def agendar(self, consulta: 'Consulta'):
        self._agenda.append(consulta)
        return True
    
class Consulta:

    def __init__(self, horario: time, medico: Medico, paciente: str):
        self.horario = horario
        self.medico = medico
        self.paciente = paciente
    

