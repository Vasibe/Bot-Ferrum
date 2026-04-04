from playwright.async_api import TimeoutError as PlaywrightTimeout

from src.contexts.ferrum_bot.domain.exceptions import ElementNotFoundException, NavigationException
from src.contexts.ferrum_bot.domain.ports.navigationPort import NavigationPort
from src.contexts.ferrum_bot.infrastructure.adapters.playwrightBrowser import PlaywrightBrowser
from src.app.config.settings import settings


COURSE_NAME = "ELECTIVA III"
SECTION_NAME = "Evaluaci\u00f3n Formativa"
ACTIVITY_NAME = "Taller Pr\u00e1ctico individual"

# Scripts JS que se ejecutan en el navegador via page.evaluate()
# Buscan hrefs en el DOM independientemente de la visibilidad CSS del elemento
JS_FIND_SECTION = """(name) => {
    const links = document.querySelectorAll('a[href*="section="]');
    for (const link of links) {
        if (link.textContent.trim().includes(name)) return link.href;
    }
    return null;
}"""

JS_FIND_ACTIVITY = """(name) => {
    const links = document.querySelectorAll('a[href*="mod/assign"]');
    for (const link of links) {
        if (link.textContent.includes(name)) return link.href;
    }
    return null;
}"""


class CourseNavigator(NavigationPort):

    def __init__(self, browser: PlaywrightBrowser) -> None:
        self._browser = browser

    async def go_to_course(self) -> None:
        page = self._browser.page
 
        print("[NAV] Navegando a My courses...")
        await self._browser.goto(f"{settings.FERRUM_URL}/my/")
        await page.wait_for_load_state("networkidle", timeout=20_000)
        await page.wait_for_timeout(2000)

        print(f"[NAV] Buscando curso: '{COURSE_NAME}'...")
        try:
            course_link = page.locator(f"a:has-text('{COURSE_NAME}')")
            await course_link.first.wait_for(state="visible", timeout=15_000)
            await course_link.first.scroll_into_view_if_needed()
            await course_link.first.click()
            await page.wait_for_load_state("domcontentloaded")
        except PlaywrightTimeout:
            raise ElementNotFoundException(
                f"No se encontro el curso '{COURSE_NAME}' en My courses."
            )

        current = await self._browser.current_url()
        if "course/view.php" not in current:
            raise NavigationException(f"Se esperaba llegar al curso pero la URL es: {current}")

        print(f"[OK] Dentro del curso. URL: {current}")

    async def scroll_to_section(self) -> None:
        page = self._browser.page
        print("[NAV] Buscando seccion: Evaluacion Formativa...")

        section_url: str | None = await page.evaluate(JS_FIND_SECTION, SECTION_NAME)

        if not section_url:
            raise ElementNotFoundException("No se encontro la seccion Evaluacion Formativa.")

        print(f"[OK] Seccion encontrada: {section_url}")

        try:
            await page.get_by_text(SECTION_NAME, exact=False).first.scroll_into_view_if_needed()
            await page.wait_for_timeout(800)
        except Exception:
            pass

        await self._browser.goto(section_url)
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(1000)
        print("[OK] Seccion Evaluacion Formativa cargada.")

    async def open_activity(self) -> None:
        page = self._browser.page
        print("[NAV] Buscando actividad: Taller Practico individual...")

        activity_href: str | None = await page.evaluate(JS_FIND_ACTIVITY, ACTIVITY_NAME)

        if not activity_href:
            raise ElementNotFoundException("No se encontro la actividad Taller Practico individual.")

        print(f"[OK] Enlace encontrado: {activity_href}")

        try:
            await page.get_by_text(ACTIVITY_NAME, exact=False).first.scroll_into_view_if_needed()
            await page.wait_for_timeout(800)
        except Exception:
            pass

        await self._browser.goto(activity_href)
        await page.wait_for_load_state("domcontentloaded")

        current = await self._browser.current_url()
        if "assign/view.php" not in current and "mod/" not in current:
            raise NavigationException(f"Se esperaba llegar a la actividad pero la URL es: {current}")

        print("[OK] Llegaste a la actividad correctamente.")
        print(f"[OK] URL final: {current}")
