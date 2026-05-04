"""
Scraper for Lovdata – bruker Scrapling DynamicFetcher (Playwright).
Henter nasjonale lover og forskrifter.

Kilde: https://lovdata.no
"""

import logging
from pathlib import Path

from .base import BaseScraper

logger = logging.getLogger(__name__)

PRIORITERTE_LOVER = [
    ("arbeidsmiljoeloven", "https://lovdata.no/lov/2005-06-17-62"),
    ("skatteloven", "https://lovdata.no/lov/1999-03-26-14"),
    ("merverdiavgiftsloven", "https://lovdata.no/lov/2009-06-19-58"),
    ("plan-og-bygningsloven", "https://lovdata.no/lov/2008-06-27-71"),
    ("forvaltningsloven", "https://lovdata.no/lov/1967-02-10"),
    ("folketrygdloven", "https://lovdata.no/lov/1997-02-28-19"),
    ("barnelova", "https://lovdata.no/lov/1981-04-08-7"),
    ("husleieloven", "https://lovdata.no/lov/1999-03-26-17"),
    ("avtaleloven", "https://lovdata.no/lov/1918-05-31-4"),
    ("straffeloven", "https://lovdata.no/lov/2005-05-20-28"),
    ("likestillingsloven", "https://lovdata.no/lov/2017-06-16-51"),
    ("personopplysningsloven", "https://lovdata.no/lov/2018-06-15-38"),
    ("aksjeloven", "https://lovdata.no/lov/1997-06-13-44"),
    ("regnskapsloven", "https://lovdata.no/lov/1998-07-17-56"),
    ("konkursloven", "https://lovdata.no/lov/1984-06-08-58"),
]

LOV_KATEGORIER = [
    ("arbeidsliv", "https://lovdata.no/register/lover?topic=arbeidsliv"),
    ("skatt", "https://lovdata.no/register/lover?topic=skatt"),
    ("trygd", "https://lovdata.no/register/lover?topic=trygd"),
    ("bygg", "https://lovdata.no/register/lover?topic=bygg"),
    ("familie", "https://lovdata.no/register/lover?topic=familie"),
    ("helse", "https://lovdata.no/register/lover?topic=helse"),
    ("miljoe", "https://lovdata.no/register/lover?topic=miljo"),
    ("naering", "https://lovdata.no/register/lover?topic=naering"),
    ("forvaltning", "https://lovdata.no/register/lover?topic=forvaltning"),
]

_INNHOLD_SELEKTORER = ["div.law-content", "article.law", "main", "#lovtekst", ".lovtekst"]


class LovdataScraper(BaseScraper):
    name = "lovdata"
    source_url = "https://lovdata.no"

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        created = []

        for navn, url in PRIORITERTE_LOVER[:max_pages]:
            path = self._hent_lov(output_dir / "lover", url, navn)
            if path:
                created.append(path)

        remaining = max_pages - len(created)
        if remaining > 0:
            for kategori, kat_url in LOV_KATEGORIER:
                for lenke_url, tittel in self._hent_lenker(kat_url)[:5]:
                    if len(created) >= max_pages:
                        break
                    slug = self.slugify(tittel)
                    path = self._hent_lov(output_dir / "kategorier" / kategori, lenke_url, slug)
                    if path:
                        created.append(path)

        logger.info("Lovdata: %d filer endret/nye", len(created))
        return created

    def _hent_lov(self, output_dir: Path, url: str, navn: str) -> Path | None:
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / f"{navn}.md"

        page = self._dynamic_fetch(url)
        if not page:
            return None

        tittel = self.hent_tittel(page)
        raa_innhold = self.side_til_markdown(page, _INNHOLD_SELEKTORER)
        if not raa_innhold.strip():
            logger.warning("Ingen innhold for %s", url)
            return None

        oppdatert = ""
        dato_el = self.css_first(page, ".last-updated, .date-modified, time")
        if dato_el and dato_el.text:
            oppdatert = str(dato_el.text)

        formatert = self._formater(tittel, raa_innhold, url, oppdatert.strip())
        return filepath if self.skriv_hvis_endret(filepath, raa_innhold, formatert) else None

    def _hent_lenker(self, url: str) -> list[tuple[str, str]]:
        page = self._dynamic_fetch(url)
        if not page:
            return []
        lenker = []
        for el in page.css("a[href*='/lov/']")[:20]:
            href = el.attrib.get("href", "")
            tekst = str(el.text or "").strip()
            if href and len(tekst) > 5:
                if href.startswith("/"):
                    href = f"https://lovdata.no{href}"
                lenker.append((href, tekst))
        return lenker

    def _dynamic_fetch(self, url: str, retries: int = 3):
        """Hent JS-rendret side med Scrapling DynamicFetcher (Playwright)."""
        from scrapling.fetchers import DynamicFetcher
        import time, random

        for attempt in range(retries):
            self._polite_delay()
            try:
                page = DynamicFetcher.fetch(
                    url,
                    headless=True,
                    network_idle=True,
                    disable_resources=True,
                )
                self._last_request_time = time.time()
                return page
            except Exception as e:
                logger.warning("DynamicFetcher feil (forsøk %d/%d) %s: %s", attempt + 1, retries, url, e)
                time.sleep(8 * (attempt + 1))
        return None

    def _formater(self, tittel: str, innhold: str, url: str, oppdatert: str) -> str:
        return "\n".join([
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** Lovdata – {url}",
            f"- **Sist oppdatert (kilde):** {oppdatert or 'ukjent'}",
            f"- **Sist hentet:** {self.now_iso()}",
            "",
            "## Lovtekst",
            "",
            innhold,
            "",
            "---",
            f"*Automatisk hentet fra [Lovdata]({url}) av norges-lover-bot.*",
        ])
