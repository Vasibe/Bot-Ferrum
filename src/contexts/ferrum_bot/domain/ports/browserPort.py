from abc import ABC, abstractmethod


class BrowserPort(ABC):
    """
    Puerto (interfaz) que define el contrato que debe cumplir
    cualquier implementación del navegador.
    """

    @abstractmethod
    async def start(self) -> None:
        """Inicia el navegador."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Cierra el navegador."""
        pass

    @abstractmethod
    async def goto(self, url: str) -> None:
        """Navega a una URL."""
        pass

    @abstractmethod
    async def current_url(self) -> str:
        """Retorna la URL actual."""
        pass

    @abstractmethod
    async def save_session(self, path: str) -> None:
        """Guarda cookies/storage para persistir la sesión."""
        pass

    @abstractmethod
    async def load_session(self, path: str) -> None:
        """Carga cookies/storage de una sesión guardada."""
        pass
