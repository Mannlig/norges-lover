"""
Scraper for NAV (Arbeids- og velferdsdirektoratet).
Henter informasjon om stønader, ytelser og rettigheter fra nav.no.

Kilde: https://www.nav.no
Innholdet er offentlig og gratis tilgjengelig.
"""

import logging
from pathlib import Path

from bs4 import BeautifulSoup

from .base import BaseScraper

logger = logging.getLogger(__name__)

NAV_SIDER = [
    # Dagpenger
    ("dagpenger/om-dagpenger", "https://www.nav.no/dagpenger"),
    ("dagpenger/satser", "https://www.nav.no/dagpenger#satser"),
    ("dagpenger/soek", "https://www.nav.no/dagpenger#soek"),
    # Sykepenger
    ("sykepenger/om-sykepenger", "https://www.nav.no/sykepenger"),
    ("sykepenger/satser", "https://www.nav.no/sykepenger#satser"),
    ("sykepenger/arbeidsgivere", "https://www.nav.no/sykepenger#for-arbeidsgivere"),
    # Foreldrepenger
    ("foreldrepenger/om", "https://www.nav.no/foreldrepenger"),
    ("foreldrepenger/fedrekvote", "https://www.nav.no/foreldrepenger#fedrekvote"),
    ("foreldrepenger/satser", "https://www.nav.no/foreldrepenger#satser"),
    # Barnetrygd
    ("barnetrygd/om", "https://www.nav.no/barnetrygd"),
    ("barnetrygd/satser", "https://www.nav.no/barnetrygd#satser"),
    # Kontantstøtte
    ("kontantstotte/om", "https://www.nav.no/kontantstotte"),
    # Uføretrygd
    ("uforetrygd/om", "https://www.nav.no/uforetrygd"),
    ("uforetrygd/satser", "https://www.nav.no/uforetrygd#satser"),
    # Alderspensjon
    ("alderspensjon/om", "https://www.nav.no/alderspensjon"),
    ("alderspensjon/satser", "https://www.nav.no/alderspensjon#satser"),
    # AAP (Arbeidsavklaringspenger)
    ("aap/om", "https://www.nav.no/arbeidsavklaringspenger"),
    ("aap/satser", "https://www.nav.no/arbeidsavklaringspenger#satser"),
    # Sosialhjelp
    ("sosialhjelp/om", "https://www.nav.no/sosialhjelp"),
    ("sosialhjelp/veiledende-satser", "https://www.nav.no/sosialhjelp#veiledende-satser"),
    # Hjelpemidler
    ("hjelpemidler/om", "https://www.nav.no/hjelpemidler"),
    # Bostøtte
    ("bostotte/om", "https://www.husbanken.no/bostotte/"),
    # Overgangsstønad
    ("overgangsstonad/om", "https://www.nav.no/overgangsstonad-enslig"),
    # Pleie- og omsorgspenger
    ("omsorgspenger/om", "https://www.nav.no/omsorgspenger"),
    ("pleiepenger/om", "https://www.nav.no/pleiepenger-sykt-barn"),
    # Gravid
    ("gravid/svangerskapspenger", "https://www.nav.no/svangerskapspenger"),
    # Grunnbeløp
    ("grunnbelop", "https://www.nav.no/grunnbelopet"),
]


class NavScraper(BaseScraper):
    name = "nav"
    source_url = "https://www.nav.no"

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        created = []

        for slug, url in NAV_SIDER[:max_pages]:
            # Fjern anker fra URL for HTTP-request
            request_url = url.split("#")[0]
            path = self._hent_side(output_dir, slug, request_url, url)
            if path:
                created.append(path)

        logger.info("NAV: lagret %d sider", len(created))
        return created

    def _hent_side(self, output_dir: Path, slug: str, url: str, original_url: str) -> Path | None:
        resp = self.get(url)
        if not resp:
            return None

        try:
            soup = BeautifulSoup(resp.text, "html.parser")
        except Exception as e:
            logger.warning("HTML-parsing feilet for %s: %s", url, e)
            return None

        tittel = self._hent_tittel(soup)
        innhold = self._hent_innhold(soup)

        if not innhold.strip():
            logger.warning("Ingen innhold for %s", url)
            return None

        parts = slug.split("/")
        target_dir = output_dir
        for part in parts[:-1]:
            target_dir = target_dir / part
        target_dir.mkdir(parents=True, exist_ok=True)

        filepath = target_dir / f"{parts[-1]}.md"
        filepath.write_text(
            self._formater(tittel, innhold, original_url),
            encoding="utf-8",
        )
        logger.info("Lagret: %s", filepath.name)
        return filepath

    def _hent_tittel(self, soup: BeautifulSoup) -> str:
        tag = soup.find("h1")
        return tag.get_text(strip=True) if tag else "Ukjent tittel"

    def _hent_innhold(self, soup: BeautifulSoup) -> str:
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        for selector in ["main", "article", "[role='main']", ".article-body", "#maincontent"]:
            el = soup.select_one(selector)
            if el:
                return self._til_markdown(el)
        return ""

    def _til_markdown(self, element) -> str:
        linjer = []
        for tag in element.find_all(["h1", "h2", "h3", "h4", "p", "li", "dt", "dd"]):
            tekst = tag.get_text(separator=" ", strip=True)
            if not tekst:
                continue
            if tag.name == "h1":
                linjer.append(f"\n## {tekst}\n")
            elif tag.name == "h2":
                linjer.append(f"\n### {tekst}\n")
            elif tag.name in ("h3", "h4"):
                linjer.append(f"\n#### {tekst}\n")
            elif tag.name == "p":
                linjer.append(f"{tekst}\n")
            elif tag.name == "li":
                linjer.append(f"- {tekst}")
            elif tag.name == "dt":
                linjer.append(f"\n**{tekst}**")
            elif tag.name == "dd":
                linjer.append(f"  {tekst}")
        return "\n".join(linjer)

    def _formater(self, tittel: str, innhold: str, url: str) -> str:
        return "\n".join([
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** NAV (Arbeids- og velferdsdirektoratet) – {url}",
            f"- **Kategori:** Stønader og ytelser",
            f"- **Hentet:** {self.now_iso()}",
            "",
            "> **Merk:** Satser og beløp endres normalt hvert år (1. mai ved G-regulering).",
            "> Sjekk alltid [nav.no]({url}) for oppdaterte tall.",
            "",
            "## Innhold",
            "",
            innhold,
            "",
            "---",
            "",
            f"*Automatisk hentet fra [NAV]({url}) av norges-lover-bot. "
            "Se [mannlig/norges-lover](https://github.com/mannlig/norges-lover) for kildekode.*",
        ])
