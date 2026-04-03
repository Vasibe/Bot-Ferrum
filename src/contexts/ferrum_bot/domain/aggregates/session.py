from dataclasses import dataclass
from typing import Optional


@dataclass
class Session:
    """
    Entidad de dominio que representa la sesión activa del bot.
    Se actualiza durante la navegación para reflejar el estado actual.
    """
    is_authenticated: bool = False
    current_url: Optional[str] = None
    cookies_path: str = "auth.json"

    def mark_authenticated(self, url: str) -> None:
        self.is_authenticated = True
        self.current_url = url

    def mark_unauthenticated(self) -> None:
        self.is_authenticated = False
        self.current_url = None
