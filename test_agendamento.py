from unittest import TestCase
from datetime import time
from agendamento import Medico, Consulta

class TestAgendamento(TestCase):
    
    def test_deve_realizar_agendamento(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta = Consulta(horario=time(9, 0), medico=medico, paciente="Julia")

        medico.agendar(consulta)
        self.assertIn(consulta, medico._agenda)

    def test_nao_deve_agendar_fora_do_horario(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta = Consulta(horario=time(14, 0), medico=medico, paciente="Julia")

        with self.assertRaises(ValueError):
            medico.agendar(consulta)