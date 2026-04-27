from unittest import TestCase
from datetime import time
from agendamento import Medico, Consulta
from exceptions import HorarioIndisponivelError, ConflitoHorarioError, TurnoInvalidoError

class TestAgendamento(TestCase):
    
    def test_deve_realizar_agendamento(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta = Consulta.criar("08:00", medico, "Julia")

        medico.agendar(consulta)
        self.assertIn(consulta, medico.agenda)

    def test_deve_permitir_consultas_em_sequencia(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta_1 = Consulta.criar("08:00", medico, "Julia")
        consulta_2 = Consulta.criar("08:30", medico, "Pedro")

        medico.agendar(consulta_1)
        medico.agendar(consulta_2)

        self.assertIn(consulta_2, medico.agenda)

    def test_deve_cancelar_consulta_agendada(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta = Consulta.criar("08:00", medico, "Julia")

        medico.agendar(consulta)
        medico.cancelar(consulta)

        self.assertNotIn(consulta, medico.agenda)

    def test_nao_deve_agendar_fora_do_horario(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta = Consulta.criar("14:00", medico, "Julia")

        with self.assertRaises(HorarioIndisponivelError):
            medico.agendar(consulta)

    def test_nao_deve_agendar_passando_do_horario_fim(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta = Consulta.criar("11:45", medico, "Julia")

        with self.assertRaises(HorarioIndisponivelError):
            medico.agendar(consulta)

    def test_nao_deve_permitir_conflito_de_horario(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta_1 = Consulta.criar("08:00", medico, "Julia")
        consulta_2 = Consulta.criar("08:00", medico, "Pedro")

        medico.agendar(consulta_1)

        with self.assertRaises(ConflitoHorarioError):
            medico.agendar(consulta_2)

    def test_nao_deve_permitir_conflito_de_horario_parcial(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))

        consulta_1 = Consulta.criar("08:00", medico, "Julia")
        consulta_2 = Consulta.criar("08:15", medico, "Pedro")

        medico.agendar(consulta_1)

        with self.assertRaises(ConflitoHorarioError):
            medico.agendar(consulta_2)    

    def test_nao_deve_criar_medico_com_turno_invertido(self):
        with self.assertRaises(TurnoInvalidoError):
            Medico(nome="Gabriel", inicio=time(12, 0), fim=time(8, 0))

    def test_nao_deve_criar_medico_com_turno_zerado(self):
        with self.assertRaises(TurnoInvalidoError):
            Medico(nome="Gabriel", inicio=time(8, 0), fim=time(8, 0))
