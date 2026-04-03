class DomainException(Exception):
    """
    Base abstracta para todas las excepciones de dominio.
    Cualquier contexto bounded extiende de esta clase.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
