"""
Scraper for NAV – bruker Scrapling StealthyFetcher.
Kilde: https://www.nav.no
"""

import logging
from pathlib import Path

from .base import BaseScraper

logger = logging.getLogger(__name__)

NAV_SIDER = [
    ("dagpenger/om-dagpenger", "https://www.nav.no/dagpenger"),
    ("dagpenger/satser", "https://www.nav.no/dagpenger"),
    ("sykepenger/om-sykepenger", "https://www.nav.no/sykepenger"),
    ("sykepenger/arbeidsgivere", "https://www.nav.no/sykepenger"),
    ("foreldrepenger/om", "https://www.nav.no/foreldrepenger"),
    ("foreldrepenger/satser", "https://www.nav.no/foreldrepenger"),
    ("barnetrygd/om", "https://www.nav.no/barnetrygd"),
    ("barnetrygd/satser", "https://www.nav.no/barnetrygd"),
    ("kontantstotte/om", "https://www.nav.no/kontantstotte"),
    ("uforetrygd/om", "https://www.nav.no/uforetrygd"),
    ("uforetrygd/satser", "https://www.nav.no/uforetrygd"),
    ("alderspensjon/om", "https://www.nav.no/alderspensjon"),
    ("aap/om", "https://www.nav.no/arbeidsavklaringspenger"),
    ("sosialhjelp/om", "https://www.nav.no/sosialhjelp"),
    ("hjelpemidler/om", "https://www.nav.no/hjelpemidler"),
    ("bostotte/om", "https://www.husbanken.no/bostotte/"),
    ("overgangsstonad/om", "https://www.nav.no/overgangsstonad-enslig"),
    ("omsorgspenger/om", "https://www.nav.no/omsorgspenger"),
    ("pleiepenger/om", "https://www.nav.no/pleiepenger-sykt-barn"),
    ("gravid/svangerskapspenger", "https://www.nav.no/svangerskapspenger"),
    ("grunnbelop", "https://www.nav.no/grunnbelopet"),
]

_INNHOLD_SELEKTORER = ["main", "article", "[role='main']", ".article-body", "#maincontent"]


class NavScraper(BaseScraper):
    name = "nav"
    source_url = "https://www.nav.no"

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        created = []
        for slug, url in NAV_SIDER[:max_pages]:
            path = self._hent_side(output_dir, slug, url)
            if path:
                created.append(path)
        logger.info("NAV: %d filer endret/nye", len(created))
        return created

    def _hent_side(self, output_dir: Path, slug: str, url: str) -> Path | None:
        page = self.fetch(url)
        if not page:
            return None

        tittel = self.hent_tittel(page)
        raa_innhold = self.side_til_markdown(page, _INNHOLD_SELEKTORER)
        if not raa_innhold.strip():
            logger.warning("Ingen innhold for %s", url)
            return None

        parts = slug.split("/")
        target_dir = output_dir
        for part in parts[:-1]:
            target_dir = target_dir / part
        target_dir.mkdir(parents=True, exist_ok=True)
        filepath = target_dir / f"{parts[-1]}.md"

        formatert = self._formater(tittel, raa_innhold, url)
        return filepath if self.skriv_hvis_endret(filepath, raa_innhold, formatert) else None

    def _formater(self, tittel: str, innhold: str, url: str) -> str:
        return "\n".join([
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** NAV (Arbeids- og velferdsdirektoratet) – {url}",
            f"- **Kategori:** Stønader og ytelser",
            f"- **Sist hentet:** {self.now_iso()}",
            "",
            "> **Merk:** Satser endres normalt 1. mai ved G-regulering.",
            f"> Sjekk alltid [nav.no]({url}) for oppdaterte tall.",
            "",
            "## Innhold",
            "",
            innhold,
            "",
            "---",
            f"*Automatisk hentet fra [NAV]({url}) av norges-lover-bot.*",
        ])
