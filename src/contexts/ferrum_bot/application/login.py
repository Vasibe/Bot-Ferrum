from src.contexts.ferrum_bot.domain.aggregates.user import User
from src.contexts.ferrum_bot.domain.aggregates.session import Session
from src.contexts.ferrum_bot.domain.ports.authPort import AuthPort


class Login:
    """
    servicio de aplicación para autenticar al usuario en Ferrum.
    Orquesta el proceso de login usando el puerto de autenticación.
    """

    def __init__(self, auth_port: AuthPort) -> None:
        self._auth = auth_port

    async def execute(self, username: str, password: str) -> Session:
        print("[USE CASE] Login")
        user = User(username=username, password=password)
        session = Session()
        return await self._auth.login(user, session)
