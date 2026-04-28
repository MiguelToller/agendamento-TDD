from unittest import TestCase
from datetime import time, datetime
from src.agendamento import Medico, Consulta
from src.exceptions import (
    HorarioIndisponivelError,
    ConflitoHorarioError,
    TurnoInvalidoError,
    ConsultaNaoEncontradaError,
    DiaIndisponivelError,
)
from src.enums import DiaSemana


class TestAgendamento(TestCase):

    def test_deve_realizar_agendamento(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta = Consulta.criar("08:00", medico, "Julia")

        medico.agendar(consulta)
        self.assertIn(consulta, medico.agenda)

    def test_deve_cancelar_consulta_agendada(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta = Consulta.criar("08:00", medico, "Julia")

        medico.agendar(consulta)
        medico.cancelar(consulta.id)

        self.assertNotIn(consulta, medico.agenda)

    def test_deve_permitir_consultas_em_sequencia(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta_1 = Consulta.criar("08:00", medico, "Julia")
        consulta_2 = Consulta.criar("08:30", medico, "Pedro")

        medico.agendar(consulta_1)
        medico.agendar(consulta_2)

        self.assertIn(consulta_2, medico.agenda)

    def test_deve_permitir_agendar_apos_cancelamento(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta_julia = Consulta.criar("08:00", medico, "Julia")
        consulta_pedro = Consulta.criar("08:00", medico, "Pedro")

        medico.agendar(consulta_julia)
        medico.cancelar(consulta_julia.id)
        medico.agendar(consulta_pedro)

        self.assertNotIn(consulta_julia, medico.agenda)
        self.assertIn(consulta_pedro, medico.agenda)

    def test_deve_retornar_texto_formatado_da_consulta(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta = Consulta.criar("08:00", medico, "Julia")

        texto = str(consulta)

        self.assertIn("Consulta de Julia", texto)
        self.assertIn("as 08:00", texto)

    def test_deve_encontrar_consulta_pelo_id(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))
        consulta = Consulta.criar("08:00", medico, "Julia")
        medico.agendar(consulta)

        consulta_encontrada = medico.buscar_consulta(consulta.id)
        self.assertEqual(consulta_encontrada.paciente, "Julia")

    def test_nao_deve_encontrar_consulta_inexistente(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))

        with self.assertRaises(ConsultaNaoEncontradaError):
            medico.buscar_consulta("1234")

    def test_nao_deve_cancelar_consulta_inexistente(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))

        with self.assertRaises(ConsultaNaoEncontradaError):
            medico.cancelar("id-falso-12345")

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

    def test_nao_deve_agendar_em_dia_de_folga(self):
        medico = Medico(
            nome="Gabriel",
            inicio=time(8, 0),
            fim=time(12, 0),
            dias_atendimento=[DiaSemana.SEGUNDA, DiaSemana.QUARTA, DiaSemana.SEXTA],
        )

        data_sabado = datetime(2026, 5, 2, 10, 0)
        consulta_sabado = Consulta(data_sabado, medico, "Julia")

        with self.assertRaises(DiaIndisponivelError):
            medico.agendar(consulta_sabado)
