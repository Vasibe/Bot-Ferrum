import sys
sys.dont_write_bytecode = True

import asyncio

from src.app.config.settings import settings
from src.contexts.ferrum_bot.domain.ferrumBotException import FerrumBotException

from src.contexts.ferrum_bot.infrastructure.adapters.playwrightBrowser import PlaywrightBrowser
from src.contexts.ferrum_bot.infrastructure.adapters.sessionManager import try_load_session, save_session
from src.contexts.ferrum_bot.infrastructure.adapters.loginNavigator import LoginNavigator
from src.contexts.ferrum_bot.infrastructure.adapters.courseNavigator import CourseNavigator

from src.contexts.ferrum_bot.application.login import Login
from src.contexts.ferrum_bot.application.navigateTo import NavigateToActivity


async def run() -> None:
    settings.validate()

    browser = PlaywrightBrowser()
    await browser.start()

    try:
        session_loaded = await try_load_session(browser)

        if session_loaded:
            login_navigator = LoginNavigator(browser)
            still_valid = await login_navigator.is_authenticated()
            if not still_valid:
                print("[INFO] Sesion expirada. Haciendo login nuevamente...")
                session_loaded = False

        if not session_loaded:
            login = Login(LoginNavigator(browser))
            await login.execute(settings.FERRUM_USERNAME, settings.FERRUM_PASSWORD)
            await save_session(browser)

        navigate = NavigateToActivity(CourseNavigator(browser))
        await navigate.execute()

        await browser.page.wait_for_timeout(3000)

    except FerrumBotException as e:
        print(f"[ERROR] {e}")
        raise
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
        raise
    finally:
        await browser.stop()


if __name__ == "__main__":
    asyncio.run(run())
