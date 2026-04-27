class HorarioIndisponivelError(Exception):
    """Lancada quando a consulta e fora do expediente do medico."""
    pass

class ConflitoHorarioError(Exception):
    """Lancada quando existe uma consulta no horario solicitado."""
    pass

class TurnoInvalidoError(Exception):
    """Lancada quando o horario de fim de turno e menor ou igual que o de inicio."""
    pass

class ConsultaNaoEncontradaError(Exception):
    """Lancada quando uma consulta nao existe ou nao conseguiu ser acessada."""
    pass