import asyncio

from playwright.async_api import TimeoutError as PlaywrightTimeout

from src.contexts.ferrum_bot.domain.exceptions import ElementNotFoundException, NavigationException
from src.contexts.ferrum_bot.domain.ports.navigationPort import NavigationPort
from src.contexts.ferrum_bot.infrastructure.adapters.playwrightBrowser import PlaywrightBrowser
from src.app.config.settings import settings


COURSE_NAME = "ELECTIVA III"
SECTION_NAME = "Evaluaci\u00f3n Formativa"
ACTIVITY_NAME = "¿Eres un robot?"

class CourseNavigator(NavigationPort):

    def __init__(self, browser: PlaywrightBrowser) -> None:
        self._browser = browser

    async def go_to_course(self) -> None:
        page = self._browser.page

        print("[NAV] Navegando a My courses...")
        await self._browser.goto(f"{settings.FERRUM_URL}/my/courses.php")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1500) 

        print(f"[NAV] Buscando curso: '{COURSE_NAME}'...")

        # Buscar el contenedor del curso por texto
        course = page.locator('[data-region="course-content"]').filter(
            has_text=COURSE_NAME
        )

        count = await course.count()
        if count == 0:
            raise ElementNotFoundException(f"No se encontró el curso '{COURSE_NAME}'")

        # Obtener el href directamente
        link = course.locator("a[href*='course/view.php']").first
        await link.wait_for(state="attached")
        href = await link.get_attribute("href")

        if not href:
            raise ElementNotFoundException("No se pudo obtener el enlace del curso")

        print(f"[OK] URL encontrada: {href}")
        await asyncio.sleep(1)

        await self._browser.goto(href)
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(1500)

        print("[OK] Dentro del curso")

    async def scroll_to_section(self) -> None:
        page = self._browser.page
        print(f"[NAV] Buscando sección: {SECTION_NAME}...")
        await page.wait_for_timeout(1000)

        # Buscar enlaces de secciones
        section = page.locator("a[href*='section=']").filter(
            has_text=SECTION_NAME
        )


        # Obtener URL
        await section.first.wait_for(state="attached",timeout=5000)
        href = await section.first.get_attribute("href")

        if not href:
            raise ElementNotFoundException(
                f"No se pudo obtener el enlace de la sección '{SECTION_NAME}'"
            )

        print(f"[OK] Sección encontrada: {href}")
        await page.wait_for_timeout(1000)

        try:
            await section.first.scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
        except Exception:
            pass

        await self._browser.goto(href)
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(1500)

        print(f"[OK] Sección '{SECTION_NAME}' cargada.")

    async def reply_forum(self) -> None:
        page = self._browser.page

        print("[NAV] Entrando al tema del foro...")
        await page.wait_for_timeout(1000)

        topic = page.locator("a").filter(has_text=ACTIVITY_NAME)

        await topic.first.wait_for(state="attached", timeout=5000)

        await topic.first.click()
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(1500)

        print("[OK] Dentro del tema")

        # Botón responder
        reply_button = page.locator('a[href*="post.php?reply="]').first
        await reply_button.wait_for(state="attached")
        await asyncio.sleep(1)
        

        await reply_button.click()
        
        textarea = page.locator('textarea[name="post"]')
        await textarea.wait_for(state="visible")

        print("[OK] Editor abierto")

        # escribir
        message = "No soy un robot"
        await textarea.fill(message)
        await page.wait_for_timeout(1500)

        # botón enviar
        submit = page.locator('button[data-action="forum-inpage-submit"]')
        await submit.wait_for(state="visible")
        await submit.click()
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)

        print("[OK] Respuesta enviada")
