from playwright.async_api import TimeoutError as PlaywrightTimeout

from src.contexts.ferrum_bot.domain.aggregates.user import User
from src.contexts.ferrum_bot.domain.aggregates.session import Session
from src.contexts.ferrum_bot.domain.exceptions import LoginFailedException
from src.contexts.ferrum_bot.domain.ports.authPort import AuthPort
from src.contexts.ferrum_bot.infrastructure.adapters.playwrightBrowser import PlaywrightBrowser
from src.app.config.settings import settings


class LoginNavigator(AuthPort):

    def __init__(self, browser: PlaywrightBrowser) -> None:
        self._browser = browser

    async def login(self, user: User, session: Session) -> Session:
        page = self._browser.page

        print(f"[LOGIN] Navegando al login: {settings.login_url}")
        await self._browser.goto(settings.login_url)

        try:
            await page.wait_for_selector("#username", timeout=10_000)
            await page.fill("#username", user.username)
            await page.fill("#password", user.password)
            await page.click("#loginbtn")

            await page.wait_for_load_state("domcontentloaded", timeout=20_000)
            await page.wait_for_timeout(2000)

            current = page.url
            if "login" in current:
                error_visible = await page.is_visible(".loginerrors, #loginerrormessage, .alert")
                raise LoginFailedException(
                    "Credenciales incorrectas. Verifica FERRUM_USERNAME y FERRUM_PASSWORD en el .env"
                    if error_visible else
                    "Login no completado. Seguimos en la pagina de login."
                )

        except PlaywrightTimeout:
            raise LoginFailedException(
                "Timeout durante el login. Verifica tu conexion o las credenciales."
            )

        current = await self._browser.current_url()
        session.mark_authenticated(current)
        print(f"[OK] Login exitoso. URL actual: {current}")
        return session

    async def is_authenticated(self) -> bool:
        await self._browser.goto(settings.dashboard_url)
        current = await self._browser.current_url()
        return "login" not in current
