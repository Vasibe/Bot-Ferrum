import os
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from src.contexts.ferrum_bot.domain.ports.browserPort import BrowserPort
from src.app.config.settings import settings


class PlaywrightBrowser(BrowserPort):

    def __init__(self) -> None:
        self._playwright = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    @property
    def page(self) -> Page:
        if self._page is None:
            raise RuntimeError("El navegador no esta iniciado. Llama a start() primero.")
        return self._page

    async def start(self) -> None:
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=settings.HEADLESS,
            slow_mo=settings.SLOW_MO,
        )
        self._context = await self._browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        pages = self._context.pages
        self._page = pages[0] if pages else await self._context.new_page()
        print("[OK] Navegador iniciado.")

    async def stop(self) -> None:
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        print("[FIN] Navegador cerrado.")

    async def goto(self, url: str) -> None:
        await self.page.goto(url, wait_until="domcontentloaded", timeout=60_000)

    async def current_url(self) -> str:
        return self.page.url

    async def save_session(self, path: str) -> None:
        if self._context:
            await self._context.storage_state(path=path)
            print(f"[OK] Sesion guardada en: {path}")

    async def load_session(self, path: str) -> None:
        if not os.path.exists(path):
            print(f"[INFO] No se encontro sesion guardada en: {path}")
            return
        if self._browser:
            if self._context:
                await self._context.close()
            self._context = await self._browser.new_context(
                storage_state=path,
                viewport={"width": 1280, "height": 720},
            )
            self._page = await self._context.new_page()
            print(f"[OK] Sesion cargada desde: {path}")
