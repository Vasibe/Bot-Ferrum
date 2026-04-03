from src.contexts.ferrum_bot.domain.ports.navigationPort import NavigationPort


class NavigateToActivity:
    """Caso de uso que representa navegar hasta la actividad del taller"""
    def __init__(self, navigation: NavigationPort) -> None:
        self._navigation = navigation

    async def execute(self) -> None:
        print("[USE CASE] Navegar hasta la actividad")
        await self._navigation.go_to_course()
        await self._navigation.scroll_to_section()
        await self._navigation.open_activity()
        print("[FIN] Flujo completado exitosamente.")
