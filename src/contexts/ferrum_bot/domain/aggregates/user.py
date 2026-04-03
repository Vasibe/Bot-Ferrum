from dataclasses import dataclass
from src.contexts.ferrum_bot.domain.exceptions import InvalidUserException


@dataclass(frozen=True)
class User:
    """
    Entidad de dominio que representa las credenciales del usuario.
    """
    username: str
    password: str

    def __post_init__(self) -> None:
        if not self.username or not self.username.strip():
            raise InvalidUserException("El nombre de usuario no puede estar vacio.")
        if not self.password:
            raise InvalidUserException("La contrasena no puede estar vacia.")
