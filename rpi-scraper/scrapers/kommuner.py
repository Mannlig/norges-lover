"""
Scraper for kommunale og fylkeskommunale forskrifter.
Henter lokale forskrifter fra Lovdata sitt kommuneregister.

Kilde: https://lovdata.no/register/lokaleforskrifter
SSB kommunenummer: https://www.ssb.no/klass/klassifikasjoner/131
"""

import asyncio
import json
import logging
from pathlib import Path

from .base import BaseScraper
from config import KOMMUNER

logger = logging.getLogger(__name__)


class KommunerScraper(BaseScraper):
    name = "kommuner"
    source_url = "https://lovdata.no/register/lokaleforskrifter"

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        return asyncio.run(self._scrape_async(output_dir, max_pages))

    async def _scrape_async(self, output_dir: Path, max_pages: int) -> list[Path]:
        try:
            import nodriver as uc
        except ImportError:
            logger.error("nodriver ikke installert. Kjør: pip install nodriver")
            return []

        created = []
        browser = None
        total = 0

        try:
            browser = await uc.start(
                headless=True,
                browser_executable_path="/usr/bin/chromium-browser",
                browser_args=["--no-sandbox", "--disable-dev-shm-usage"],
            )

            for kommunenr, kommunenavn in KOMMUNER.items():
                if total >= max_pages:
                    break

                kommune_dir = output_dir / f"{kommunenr}-{kommunenavn}"
                kommune_dir.mkdir(parents=True, exist_ok=True)

                url = f"{self.source_url}/{kommunenr}"
                forskrifter = await self._hent_kommuneforskrifter(browser, url, kommunenavn, kommunenr)

                for tittel, forskrift_url, innhold in forskrifter:
                    if total >= max_pages:
                        break
                    slug = self.slugify(tittel)
                    filepath = kommune_dir / f"{slug}.md"
                    md = self._formater(tittel, innhold, forskrift_url, kommunenavn, kommunenr)
                    filepath.write_text(md, encoding="utf-8")
                    created.append(filepath)
                    total += 1
                    logger.info("Lagret: %s/%s", kommunenavn, slug)
                    await asyncio.sleep(4)

        finally:
            if browser:
                try:
                    await browser.stop()
                except Exception:
                    pass

        logger.info("Kommuner: lagret %d forskrifter", len(created))
        return created

    async def _hent_kommuneforskrifter(
        self, browser, url: str, kommunenavn: str, kommunenr: str
    ) -> list[tuple[str, str, str]]:
        """Henter liste over forskrifter for en kommune og innholdet."""
        page = None
        forskrifter = []

        try:
            page = await browser.get(url)
            await asyncio.sleep(3)

            # Hent alle lenker til lokale forskrifter
            lenker_json = await page.evaluate("""
                JSON.stringify(
                    Array.from(document.querySelectorAll('a[href*="/forskrift/"]'))
                    .map(a => ({href: a.href, text: a.innerText.trim()}))
                    .filter(a => a.text.length > 5)
                    .slice(0, 10)
                )
            """)
            lenker = json.loads(lenker_json or "[]")

            for lenke in lenker[:5]:
                forskrift_url = lenke["href"]
                tittel = lenke["text"]
                innhold = await self._hent_forskrift_innhold(browser, forskrift_url)
                if innhold:
                    forskrifter.append((tittel, forskrift_url, innhold))
                await asyncio.sleep(4)

        except Exception as e:
            logger.warning("Feil ved henting av %s (%s): %s", kommunenavn, kommunenr, e)
        finally:
            if page:
                try:
                    await page.close()
                except Exception:
                    pass

        return forskrifter

    async def _hent_forskrift_innhold(self, browser, url: str) -> str:
        page = None
        try:
            page = await browser.get(url)
            await asyncio.sleep(3)

            innhold = ""
            for selector in ["div.law-content", "article", "main"]:
                innhold = await page.evaluate(
                    f"document.querySelector('{selector}')?.innerText || ''"
                )
                if innhold.strip():
                    break
            return innhold.strip()
        except Exception as e:
            logger.warning("Feil ved henting av forskrift %s: %s", url, e)
            return ""
        finally:
            if page:
                try:
                    await page.close()
                except Exception:
                    pass

    def _formater(
        self, tittel: str, innhold: str, url: str, kommunenavn: str, kommunenr: str
    ) -> str:
        return "\n".join([
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** Lovdata – {url}",
            f"- **Kommune:** {kommunenavn.capitalize()} (kommunenr. {kommunenr})",
            f"- **Kategori:** Kommunal/lokal forskrift",
            f"- **Hentet:** {self.now_iso()}",
            "",
            "## Innhold",
            "",
            innhold,
            "",
            "---",
            "",
            f"*Automatisk hentet fra [Lovdata – lokale forskrifter]({url}) av norges-lover-bot. "
            "Se [mannlig/norges-lover](https://github.com/mannlig/norges-lover) for kildekode.*",
        ])
