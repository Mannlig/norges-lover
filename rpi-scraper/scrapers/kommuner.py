"""
Scraper for kommunale forskrifter – bruker Scrapling DynamicFetcher (Playwright).
Kilde: https://lovdata.no/register/lokaleforskrifter
"""

import logging
import time
from pathlib import Path

from .base import BaseScraper
from config import KOMMUNER

logger = logging.getLogger(__name__)


class KommunerScraper(BaseScraper):
    name = "kommuner"
    source_url = "https://lovdata.no/register/lokaleforskrifter"

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        created = []
        total = 0

        for kommunenr, kommunenavn in KOMMUNER.items():
            if total >= max_pages:
                break

            kommune_dir = output_dir / f"{kommunenr}-{kommunenavn}"
            kommune_dir.mkdir(parents=True, exist_ok=True)

            url = f"{self.source_url}/{kommunenr}"
            for tittel, forskrift_url, raa_innhold in self._hent_kommuneforskrifter(url, kommunenavn):
                if total >= max_pages:
                    break

                slug = self.slugify(tittel)
                filepath = kommune_dir / f"{slug}.md"
                formatert = self._formater(tittel, raa_innhold, forskrift_url, kommunenavn, kommunenr)
                endret = self.skriv_hvis_endret(filepath, raa_innhold, formatert)
                if endret:
                    created.append(filepath)
                logger.info("%s/%s: %s", kommunenavn, slug, "endret" if endret else "uendret")
                total += 1
                time.sleep(4)

        logger.info("Kommuner: %d filer endret/nye", len(created))
        return created

    def _hent_kommuneforskrifter(
        self, url: str, kommunenavn: str
    ) -> list[tuple[str, str, str]]:
        page = self._dynamic_fetch(url)
        if not page:
            return []

        forskrifter = []
        for el in page.css("a[href*='/forskrift/']")[:10]:
            href = el.attrib.get("href", "")
            tittel = (el.text or "").strip()
            if not href or len(tittel) < 5:
                continue
            if href.startswith("/"):
                href = f"https://lovdata.no{href}"

            innhold_page = self._dynamic_fetch(href)
            if not innhold_page:
                continue

            raa_innhold = self.side_til_markdown(
                innhold_page, ["div.law-content", "article", "main"]
            )
            if raa_innhold:
                forskrifter.append((tittel, href, raa_innhold))
            time.sleep(4)

        return forskrifter[:5]

    def _dynamic_fetch(self, url: str, retries: int = 3):
        from scrapling.fetchers import DynamicFetcher

        for attempt in range(retries):
            self._polite_delay()
            try:
                page = DynamicFetcher.fetch(url, headless=True, network_idle=True, disable_resources=True)
                self._last_request_time = time.time()
                return page
            except Exception as e:
                logger.warning("DynamicFetcher feil (forsøk %d/%d) %s: %s", attempt + 1, retries, url, e)
                time.sleep(8 * (attempt + 1))
        return None

    def _formater(self, tittel: str, innhold: str, url: str, kommunenavn: str, kommunenr: str) -> str:
        return "\n".join([
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** Lovdata – {url}",
            f"- **Kommune:** {kommunenavn.capitalize()} (kommunenr. {kommunenr})",
            f"- **Kategori:** Kommunal/lokal forskrift",
            f"- **Sist hentet:** {self.now_iso()}",
            "",
            "## Innhold",
            "",
            innhold,
            "",
            "---",
            f"*Automatisk hentet fra [Lovdata – lokale forskrifter]({url}) av norges-lover-bot.*",
        ])
