from enum import Enum


class DiaSemana(Enum):
    SEGUNDA = 0
    TERCA = 1
    QUARTA = 2
    QUINTA = 3
    SEXTA = 4
    SABADO = 5
    DOMINGO = 6


map_dia_semana = {
    DiaSemana.SEGUNDA: "Segunda",
    DiaSemana.TERCA: "Terça",
    DiaSemana.QUARTA: "Quarta",
    DiaSemana.QUINTA: "Quinta",
    DiaSemana.SEXTA: "Sexta",
    DiaSemana.SABADO: "Sábado",
    DiaSemana.DOMINGO: "Domingo",
}
