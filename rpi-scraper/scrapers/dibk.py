"""
Scraper for DiBK – bruker Scrapling StealthyFetcher.
Kilde: https://www.dibk.no
"""

import logging
from pathlib import Path

from .base import BaseScraper

logger = logging.getLogger(__name__)

DIBK_SIDER = [
    ("tek17/krav-til-byggverk", "https://dibk.no/regelverk/byggteknisk-forskrift-tek17/"),
    ("tek17/brannsikkerhet",
     "https://dibk.no/regelverk/byggteknisk-forskrift-tek17/11-brannsikkerhet/"),
    ("tek17/energi",
     "https://dibk.no/regelverk/byggteknisk-forskrift-tek17/14-energi/"),
    ("tek17/universell-utforming",
     "https://dibk.no/regelverk/byggteknisk-forskrift-tek17/12-planlosning-og-bygningsdeler/"),
    ("tek17/sikkerhet-i-bruk",
     "https://dibk.no/regelverk/byggteknisk-forskrift-tek17/13-sikkerhet-ved-bruk/"),
    ("sak10/soknadspliktige-tiltak",
     "https://dibk.no/regelverk/byggesaksforskriften-sak10/"),
    ("sak10/unntak-fra-soknadsplikt",
     "https://dibk.no/regelverk/byggesaksforskriften-sak10/2-unntak-fra-soknadsplikt/"),
    ("gof/produktdokumentasjon",
     "https://dibk.no/regelverk/forskrift-om-omsetning-og-dokumentasjon-av-produkter-til-byggverk-dof/"),
    ("veiledere/tilbygg", "https://dibk.no/byggeregler/tilbygg/"),
    ("veiledere/garasje", "https://dibk.no/byggeregler/garasje-og-uthus/"),
    ("veiledere/terrasse", "https://dibk.no/byggeregler/terrasse/"),
    ("veiledere/gjerde", "https://dibk.no/byggeregler/gjerde-og-levegg/"),
    ("veiledere/bod", "https://dibk.no/byggeregler/bod-og-sykkeloppbevaring/"),
    ("veiledere/soknadsguide", "https://dibk.no/soknadspliktig-eller-ikke/"),
    ("soknader/nabovarsling", "https://dibk.no/byggesok/nabo-og-gjenboer/nabovarsel/"),
    ("soknader/rammetillatelse", "https://dibk.no/byggesok/saksgangen/rammetillatelse/"),
    ("soknader/igangsettingstillatelse",
     "https://dibk.no/byggesok/saksgangen/igangsettingstillatelse/"),
    ("soknader/ferdigattest",
     "https://dibk.no/byggesok/saksgangen/ferdigattest-og-midlertidig-brukstillatelse/"),
]

_INNHOLD_SELEKTORER = ["main", "article", ".article-body", "#main", "[role='main']"]


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
        logger.info("DiBK: %d filer endret/nye", len(created))
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

        oppdatert = ""
        dato_el = self.css_first(page, "time[datetime], .date, .published")
        if dato_el:
            oppdatert = dato_el.attrib.get("datetime", "") or str(dato_el.text or "")

        parts = slug.split("/")
        target_dir = output_dir
        for part in parts[:-1]:
            target_dir = target_dir / part
        target_dir.mkdir(parents=True, exist_ok=True)
        filepath = target_dir / f"{parts[-1]}.md"

        formatert = self._formater(tittel, raa_innhold, url, oppdatert.strip())
        return filepath if self.skriv_hvis_endret(filepath, raa_innhold, formatert) else None

    def _formater(self, tittel: str, innhold: str, url: str, oppdatert: str) -> str:
        return "\n".join([
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** Direktoratet for byggkvalitet (DiBK) – {url}",
            f"- **Kategori:** Byggteknisk regelverk",
            f"- **Sist oppdatert (kilde):** {oppdatert or 'ukjent'}",
            f"- **Sist hentet:** {self.now_iso()}",
            "",
            "## Innhold",
            "",
            innhold,
            "",
            "---",
            f"*Automatisk hentet fra [DiBK]({url}) av norges-lover-bot.*",
        ])
