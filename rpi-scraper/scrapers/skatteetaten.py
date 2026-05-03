"""
Scraper for Skatteetaten – bruker Scrapling StealthyFetcher.
Kilde: https://www.skatteetaten.no
"""

import logging
from pathlib import Path

from .base import BaseScraper

logger = logging.getLogger(__name__)

SKATTEETATEN_SIDER = [
    ("satser/skattesatser", "https://www.skatteetaten.no/satser/skattesatser/"),
    ("satser/frikort", "https://www.skatteetaten.no/satser/frikortgrense/"),
    ("satser/minstefradrag", "https://www.skatteetaten.no/satser/minstefradrag/"),
    ("satser/personfradrag", "https://www.skatteetaten.no/satser/personfradrag/"),
    ("satser/foreldrefradrag", "https://www.skatteetaten.no/satser/foreldrefradrag/"),
    ("satser/pendlerfradrag", "https://www.skatteetaten.no/satser/pendlere/"),
    ("satser/reisefradrag", "https://www.skatteetaten.no/satser/reisefradrag/"),
    ("satser/bsu", "https://www.skatteetaten.no/satser/bsu/"),
    ("satser/ips", "https://www.skatteetaten.no/satser/individuell-pensjonssparing-ips/"),
    ("satser/firmabil", "https://www.skatteetaten.no/satser/fordel-firmabil/"),
    ("satser/kilometergodtgjorelse", "https://www.skatteetaten.no/satser/kilometergodtgjorelse/"),
    ("satser/diett", "https://www.skatteetaten.no/satser/kostgodtgjorelse/"),
    ("satser/arbeidsgiveravgift", "https://www.skatteetaten.no/satser/arbeidsgiveravgift/"),
    ("satser/formuesskatt", "https://www.skatteetaten.no/satser/formueskatt/"),
    ("veiledere/aksjer", "https://www.skatteetaten.no/person/aksjer-og-verdipapirer/"),
    ("veiledere/bolig", "https://www.skatteetaten.no/person/skatt/hjelp-til-riktig-skatt/bolig/"),
    ("veiledere/gaver", "https://www.skatteetaten.no/person/skatt/hjelp-til-riktig-skatt/gaver/"),
    ("veiledere/arv", "https://www.skatteetaten.no/person/skatt/hjelp-til-riktig-skatt/arv-og-gave/"),
    ("veiledere/selvstendig-naringsdrivende",
     "https://www.skatteetaten.no/bedrift-og-organisasjon/starte-og-drive/skatt-for-naringsdrivende/"),
    ("mva/veileder", "https://www.skatteetaten.no/bedrift-og-organisasjon/mva/"),
    ("mva/satser", "https://www.skatteetaten.no/satser/merverdiavgift/"),
    ("mva/frister", "https://www.skatteetaten.no/bedrift-og-organisasjon/mva/frister/"),
    ("arbeidsgiver/trekkplikt", "https://www.skatteetaten.no/bedrift-og-organisasjon/arbeidsgiver/"),
    ("naering/skattekort", "https://www.skatteetaten.no/person/skattekort/"),
]

_INNHOLD_SELEKTORER = ["main", "article", "[role='main']", ".article-content", "#main-content"]


class SkatteetatenScraper(BaseScraper):
    name = "skatteetaten"
    source_url = "https://www.skatteetaten.no"

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        created = []
        for slug, url in SKATTEETATEN_SIDER[:max_pages]:
            path = self._hent_side(output_dir, slug, url)
            if path:
                created.append(path)
        logger.info("Skatteetaten: %d filer endret/nye", len(created))
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
        dato_el = page.css_first("time, .last-updated, [datetime]")
        if dato_el:
            oppdatert = dato_el.attrib.get("datetime", "") or (dato_el.text or "")

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
            f"- **Kilde:** Skatteetaten – {url}",
            f"- **Sist oppdatert (kilde):** {oppdatert or 'ukjent'}",
            f"- **Sist hentet:** {self.now_iso()}",
            "",
            "## Innhold",
            "",
            innhold,
            "",
            "---",
            f"*Automatisk hentet fra [Skatteetaten]({url}) av norges-lover-bot.*",
        ])
