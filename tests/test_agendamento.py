from unittest import TestCase
from datetime import time, datetime
from src.agendamento import Medico, Consulta, Paciente
from src.exceptions import (
    HorarioIndisponivelError,
    ConflitoHorarioError,
    TurnoInvalidoError,
    ConsultaNaoEncontradaError,
    DiaIndisponivelError,
)
from src.enums import DiaSemana

TODOS_OS_DIAS = [
    DiaSemana.SEGUNDA,
    DiaSemana.TERCA,
    DiaSemana.QUARTA,
    DiaSemana.QUINTA,
    DiaSemana.SEXTA,
    DiaSemana.SABADO,
    DiaSemana.DOMINGO,
]


class TestAgendamento(TestCase):

    def setUp(self):
        self.julia = Paciente(nome="Julia", cpf="111.111.111-11", telefone="7777-7777")
        self.pedro = Paciente(nome="Pedro", cpf="222.222.222-22", telefone="8888-8888")

        self.medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0), dias_atendimento=TODOS_OS_DIAS)

    def test_deve_realizar_agendamento(self):
        consulta = Consulta.criar("08:00", self.medico, self.julia)

        self.medico.agendar(consulta)
        self.assertIn(consulta, self.medico.agenda)

    def test_deve_cancelar_consulta_agendada(self):
        consulta = Consulta.criar("08:00", self.medico, self.julia)

        self.medico.agendar(consulta)
        self.medico.cancelar(consulta.id)

        self.assertNotIn(consulta, self.medico.agenda)

    def test_deve_permitir_consultas_em_sequencia(self):
        consulta_1 = Consulta.criar("08:00", self.medico, self.julia)
        consulta_2 = Consulta.criar("08:30", self.medico, self.pedro)

        self.medico.agendar(consulta_1)
        self.medico.agendar(consulta_2)

        self.assertIn(consulta_2, self.medico.agenda)

    def test_deve_permitir_agendar_apos_cancelamento(self):
        consulta_julia = Consulta.criar("08:00", self.medico, self.julia)
        consulta_pedro = Consulta.criar("08:00", self.medico, self.pedro)

        self.medico.agendar(consulta_julia)
        self.medico.cancelar(consulta_julia.id)
        self.medico.agendar(consulta_pedro)

        self.assertNotIn(consulta_julia, self.medico.agenda)
        self.assertIn(consulta_pedro, self.medico.agenda)

    def test_deve_retornar_texto_formatado_da_consulta(self):
        consulta = Consulta.criar("08:00", self.medico, self.julia)

        texto = str(consulta)

        self.assertIn("Consulta de Julia", texto)
        self.assertIn("as 08:00", texto)

    def test_deve_encontrar_consulta_pelo_id(self):
        consulta = Consulta.criar("08:00", self.medico, self.julia)

        self.medico.agendar(consulta)

        consulta_encontrada = self.medico.buscar_consulta(consulta.id)
        self.assertEqual(consulta_encontrada.paciente.nome, "Julia")

    def test_deve_permitir_consultas_no_mesmo_horario_em_dias_diferentes(self):
        data_terca = datetime(2026, 4, 28, 8, 0)
        data_quarta = datetime(2026, 4, 29, 8, 0)

        consulta_terca = Consulta(data_terca, self.medico, self.julia)
        consulta_quarta = Consulta(data_quarta, self.medico, self.pedro)

        self.medico.agendar(consulta_terca)
        self.medico.agendar(consulta_quarta)

        self.assertIn(consulta_terca, self.medico.agenda)
        self.assertIn(consulta_quarta, self.medico.agenda)

    def test_deve_criar_medico_com_dias_padrao_quando_nao_informado_agenda(self):
        medico = Medico(nome="Gabriel", inicio=time(8, 0), fim=time(12, 0))

        dias_padrao = [
            DiaSemana.SEGUNDA,
            DiaSemana.TERCA,
            DiaSemana.QUARTA,
            DiaSemana.QUINTA,
            DiaSemana.SEXTA,
        ]
        self.assertEqual(medico.dias_atendimento, dias_padrao)

    def test_nao_deve_encontrar_consulta_inexistente(self):

        with self.assertRaises(ConsultaNaoEncontradaError):
            self.medico.buscar_consulta("1234")

    def test_nao_deve_cancelar_consulta_inexistente(self):

        with self.assertRaises(ConsultaNaoEncontradaError):
            self.medico.cancelar("1234")

    def test_nao_deve_agendar_fora_do_horario(self):
        consulta = Consulta.criar("14:00", self.medico, self.julia)

        with self.assertRaises(HorarioIndisponivelError):
            self.medico.agendar(consulta)

    def test_nao_deve_agendar_passando_do_horario_fim(self):
        consulta = Consulta.criar("11:45", self.medico, self.julia)

        with self.assertRaises(HorarioIndisponivelError):
            self.medico.agendar(consulta)

    def test_nao_deve_permitir_conflito_de_horario(self):
        consulta_1 = Consulta.criar("08:00", self.medico, self.julia)
        consulta_2 = Consulta.criar("08:00", self.medico, self.pedro)

        self.medico.agendar(consulta_1)

        with self.assertRaises(ConflitoHorarioError):
            self.medico.agendar(consulta_2)

    def test_nao_deve_permitir_conflito_de_horario_parcial(self):
        consulta_1 = Consulta.criar("08:00", self.medico, self.julia)
        consulta_2 = Consulta.criar("08:15", self.medico, self.pedro)

        self.medico.agendar(consulta_1)

        with self.assertRaises(ConflitoHorarioError):
            self.medico.agendar(consulta_2)

    def test_nao_deve_criar_medico_com_turno_invertido(self):
        with self.assertRaises(TurnoInvalidoError):
            Medico(
                nome="Gabriel",
                inicio=time(12, 0),
                fim=time(8, 0),
                dias_atendimento=TODOS_OS_DIAS,
            )

    def test_nao_deve_criar_medico_com_turno_zerado(self):
        with self.assertRaises(TurnoInvalidoError):
            Medico(
                nome="Gabriel",
                inicio=time(8, 0),
                fim=time(8, 0),
                dias_atendimento=TODOS_OS_DIAS,
            )

    def test_nao_deve_agendar_em_dia_de_folga(self):
        medico = Medico(
            nome="Gabriel",
            inicio=time(8, 0),
            fim=time(12, 0),
            dias_atendimento=[DiaSemana.SEGUNDA, DiaSemana.QUARTA, DiaSemana.SEXTA],
        )

        data_sabado = datetime(2026, 5, 2, 10, 0)
        consulta_sabado = Consulta(data_sabado, medico, self.julia)

        with self.assertRaises(DiaIndisponivelError):
            medico.agendar(consulta_sabado)
