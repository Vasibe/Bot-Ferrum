from src.shared.domain.domainException import DomainException


class FerrumBotException(DomainException):
    """
    Excepcion base del contexto ferrum_bot.
    Todas las excepciones especificas de este contexto extienden de esta.
    """
    def __init__(self, message: str) -> None:
        super().__init__(f"FerrumBot: {message}")
