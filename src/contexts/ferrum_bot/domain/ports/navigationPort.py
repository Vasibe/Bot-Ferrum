from abc import ABC, abstractmethod


class NavigationPort(ABC):
    """
    Interfaz para el navegador de curso que sepa moverse por Ferrum.
    """

    @abstractmethod
    async def go_to_course(self) -> None:
        pass

    @abstractmethod
    async def scroll_to_section(self) -> None:
        pass

    @abstractmethod
    async def reply_forum(self) -> None:
        pass
