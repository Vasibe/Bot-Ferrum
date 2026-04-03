from abc import ABC, abstractmethod
from src.contexts.ferrum_bot.domain.aggregates.user import User
from src.contexts.ferrum_bot.domain.aggregates.session import Session


class AuthPort(ABC):
    """
    Puerto (interfaz) que define el contrato de autenticación.
    """

    @abstractmethod
    async def login(self, user: User, session: Session) -> Session:
        """
        Realiza el proceso de login.
        """
        pass

    @abstractmethod
    async def is_authenticated(self) -> bool:
        """Verifica si la sesión actual está autenticada."""
        pass
