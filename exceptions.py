class AgendamentoError(Exception):
    """Classe base para os erros de agendamento."""
    pass

class HorarioIndisponivelError(AgendamentoError):
    """Lancada quando a consulta e fora do expediente do medico."""
    pass

class ConflitoHorarioError(AgendamentoError):
    """Lancada quando existe uma consulta no horario solicitado."""
    pass