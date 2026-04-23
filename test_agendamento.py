from unittest import TestCase
from datetime import time
from agendamento import Medico, Consulta

class TestAgendamento(TestCase):
    
    def test_deve_realizar_agendamento(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(8, 0))
        consulta = Consulta(horario=time(9, 0), medico=medico, paciente="Julia")

        medico.agendar(consulta)
        self.assertTrue(consulta, medico._agenda)