import os
from src.contexts.ferrum_bot.infrastructure.adapters.playwrightBrowser import PlaywrightBrowser


SESSION_FILE = "auth.json"


async def try_load_session(browser: PlaywrightBrowser) -> bool:
    if os.path.exists(SESSION_FILE):
        await browser.load_session(SESSION_FILE)
        return True
    return False


async def save_session(browser: PlaywrightBrowser) -> None:
    await browser.save_session(SESSION_FILE)


def clear_session() -> None:
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print("[OK] Sesion eliminada.")
