"""
Scraper for Direktoratet for byggkvalitet (DiBK).
Henter tekniske forskrifter, veiledere og regelverk for bygg og anlegg.

Kilde: https://www.dibk.no og https://byggeregler.dibk.no
Innholdet er offentlig tilgjengelig.
"""

import logging
from pathlib import Path

from bs4 import BeautifulSoup

from .base import BaseScraper

logger = logging.getLogger(__name__)

DIBK_SIDER = [
    # TEK17 – Teknisk forskrift
    ("tek17/krav-til-byggverk", "https://dibk.no/regelverk/byggteknisk-forskrift-tek17/"),
    ("tek17/brannsikkerhet", "https://dibk.no/regelverk/byggteknisk-forskrift-tek17/11-brannsikkerhet/"),
    ("tek17/energi", "https://dibk.no/regelverk/byggteknisk-forskrift-tek17/14-energi/"),
    ("tek17/universell-utforming",
     "https://dibk.no/regelverk/byggteknisk-forskrift-tek17/12-planlosning-og-bygningsdeler/"),
    ("tek17/sikkerhet-i-bruk",
     "https://dibk.no/regelverk/byggteknisk-forskrift-tek17/13-sikkerhet-ved-bruk/"),
    ("tek17/inneklima",
     "https://dibk.no/regelverk/byggteknisk-forskrift-tek17/13-sikkerhet-ved-bruk/"),
    # SAK10 – Byggesaksforskriften
    ("sak10/soknadspliktige-tiltak",
     "https://dibk.no/regelverk/byggesaksforskriften-sak10/"),
    ("sak10/unntak-fra-soknadsplikt",
     "https://dibk.no/regelverk/byggesaksforskriften-sak10/2-unntak-fra-soknadsplikt/"),
    # GOF – Forskrift om omsetning og dokumentasjon
    ("gof/produktdokumentasjon",
     "https://dibk.no/regelverk/forskrift-om-omsetning-og-dokumentasjon-av-produkter-til-byggverk-dof/"),
    # Veiledere
    ("veiledere/tilbygg", "https://dibk.no/byggeregler/tilbygg/"),
    ("veiledere/garasje", "https://dibk.no/byggeregler/garasje-og-uthus/"),
    ("veiledere/terrasse", "https://dibk.no/byggeregler/terrasse/"),
    ("veiledere/gjerde", "https://dibk.no/byggeregler/gjerde-og-levegg/"),
    ("veiledere/bod", "https://dibk.no/byggeregler/bod-og-sykkeloppbevaring/"),
    ("veiledere/soknadsguide",
     "https://dibk.no/soknadspliktig-eller-ikke/"),
    # Energi og miljø
    ("energi/energimerking",
     "https://www.enova.no/privatperson/bolig/energimerking/"),
    # Søknadsprosess
    ("soknader/nabovarsling",
     "https://dibk.no/byggesok/nabo-og-gjenboer/nabovarsel/"),
    ("soknader/rammetillatelse",
     "https://dibk.no/byggesok/saksgangen/rammetillatelse/"),
    ("soknader/igangsettingstillatelse",
     "https://dibk.no/byggesok/saksgangen/igangsettingstillatelse/"),
    ("soknader/ferdigattest",
     "https://dibk.no/byggesok/saksgangen/ferdigattest-og-midlertidig-brukstillatelse/"),
]


class DibkScraper(BaseScraper):
    name = "dibk"
    source_url = "https://www.dibk.no"

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        created = []

        for slug, url in DIBK_SIDER[:max_pages]:
            path = self._hent_side(output_dir, slug, url)
            if path:
                created.append(path)

        logger.info("DiBK: lagret %d sider", len(created))
        return created

    def _hent_side(self, output_dir: Path, slug: str, url: str) -> Path | None:
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
        oppdatert = self._hent_dato(soup)

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
            self._formater(tittel, innhold, url, oppdatert),
            encoding="utf-8",
        )
        logger.info("Lagret: %s", filepath.name)
        return filepath

    def _hent_tittel(self, soup: BeautifulSoup) -> str:
        tag = soup.find("h1")
        return tag.get_text(strip=True) if tag else soup.title.string if soup.title else "Ukjent"

    def _hent_innhold(self, soup: BeautifulSoup) -> str:
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        for selector in ["main", "article", ".article-body", "#main", "[role='main']"]:
            el = soup.select_one(selector)
            if el:
                return self._til_markdown(el)
        return ""

    def _til_markdown(self, element) -> str:
        linjer = []
        for tag in element.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
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
        return "\n".join(linjer)

    def _hent_dato(self, soup: BeautifulSoup) -> str:
        for selector in ["time[datetime]", ".date", ".published"]:
            tag = soup.select_one(selector)
            if tag:
                return tag.get("datetime", "") or tag.get_text(strip=True)
        return ""

    def _formater(self, tittel: str, innhold: str, url: str, oppdatert: str) -> str:
        return "\n".join([
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** Direktoratet for byggkvalitet (DiBK) – {url}",
            f"- **Kategori:** Byggteknisk regelverk",
            f"- **Sist oppdatert (kilde):** {oppdatert or 'ukjent'}",
            f"- **Hentet:** {self.now_iso()}",
            "",
            "## Innhold",
            "",
            innhold,
            "",
            "---",
            "",
            f"*Automatisk hentet fra [DiBK]({url}) av norges-lover-bot. "
            "Se [mannlig/norges-lover](https://github.com/mannlig/norges-lover) for kildekode.*",
        ])
