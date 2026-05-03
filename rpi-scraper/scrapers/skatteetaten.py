"""
Scraper for Skatteetaten.
Henter skatteregler, veiledere og satser fra skatteetaten.no.

Kilde: https://www.skatteetaten.no
Innholdet er offentlig og tilgjengelig uten innlogging.
"""

import logging
import re
from pathlib import Path
from html.parser import HTMLParser

from bs4 import BeautifulSoup

from .base import BaseScraper

logger = logging.getLogger(__name__)

# Sider vi vil hente fra Skatteetaten
SKATTEETATEN_SIDER = [
    # Satser og beløp
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
    # Veiledere
    ("veiledere/aksjer", "https://www.skatteetaten.no/person/aksjer-og-verdipapirer/"),
    ("veiledere/bolig", "https://www.skatteetaten.no/person/skatt/hjelp-til-riktig-skatt/bolig/"),
    ("veiledere/gaver", "https://www.skatteetaten.no/person/skatt/hjelp-til-riktig-skatt/gaver/"),
    ("veiledere/arv", "https://www.skatteetaten.no/person/skatt/hjelp-til-riktig-skatt/arv-og-gave/"),
    ("veiledere/selvstendig-naringsdrivende",
     "https://www.skatteetaten.no/bedrift-og-organisasjon/starte-og-drive/skatt-for-naringsdrivende/"),
    # MVA
    ("mva/veileder", "https://www.skatteetaten.no/bedrift-og-organisasjon/mva/"),
    ("mva/satser", "https://www.skatteetaten.no/satser/merverdiavgift/"),
    ("mva/frister", "https://www.skatteetaten.no/bedrift-og-organisasjon/mva/frister/"),
    # Arbeidsgiver
    ("arbeidsgiver/trekkplikt", "https://www.skatteetaten.no/bedrift-og-organisasjon/arbeidsgiver/"),
    # Næringsdrivende
    ("naering/skattekort", "https://www.skatteetaten.no/person/skattekort/"),
]


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

        logger.info("Skatteetaten: lagret %d sider", len(created))
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

        if not innhold:
            logger.warning("Ingen innhold funnet for %s", url)
            return None

        # Lag undermapper basert på slug
        parts = slug.split("/")
        target_dir = output_dir
        for part in parts[:-1]:
            target_dir = target_dir / part
        target_dir.mkdir(parents=True, exist_ok=True)

        filepath = target_dir / f"{parts[-1]}.md"
        md = self._formater(tittel, innhold, url, oppdatert)
        filepath.write_text(md, encoding="utf-8")
        logger.info("Lagret: %s", filepath.relative_to(output_dir.parent.parent))
        return filepath

    def _hent_tittel(self, soup: BeautifulSoup) -> str:
        for selector in ["h1", "title"]:
            tag = soup.select_one(selector)
            if tag:
                return tag.get_text(strip=True)
        return "Ukjent tittel"

    def _hent_innhold(self, soup: BeautifulSoup) -> str:
        # Fjern navigasjon, footer og script
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        for selector in [
            "main",
            "article",
            "[role='main']",
            ".article-content",
            ".main-content",
            "#main-content",
        ]:
            element = soup.select_one(selector)
            if element:
                return self._html_til_markdown(element)

        return ""

    def _html_til_markdown(self, element) -> str:
        """Enkel HTML → Markdown konvertering."""
        lines = []
        for tag in element.find_all(["h1", "h2", "h3", "h4", "p", "li", "table", "tr", "td", "th"]):
            name = tag.name
            text = tag.get_text(separator=" ", strip=True)
            if not text:
                continue
            if name == "h1":
                lines.append(f"\n## {text}\n")
            elif name == "h2":
                lines.append(f"\n### {text}\n")
            elif name in ("h3", "h4"):
                lines.append(f"\n#### {text}\n")
            elif name == "p":
                lines.append(f"{text}\n")
            elif name == "li":
                lines.append(f"- {text}")
            elif name in ("th", "td"):
                lines.append(f"| {text} ")
        return "\n".join(lines)

    def _hent_dato(self, soup: BeautifulSoup) -> str:
        for selector in ["time", ".last-updated", ".date", "[datetime]"]:
            tag = soup.select_one(selector)
            if tag:
                return tag.get("datetime", "") or tag.get_text(strip=True)
        return ""

    def _formater(self, tittel: str, innhold: str, url: str, oppdatert: str) -> str:
        linjer = [
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** Skatteetaten – {url}",
            f"- **Sist oppdatert (kilde):** {oppdatert or 'ukjent'}",
            f"- **Hentet:** {self.now_iso()}",
            "",
            "## Innhold",
            "",
            innhold,
            "",
            "---",
            "",
            f"*Automatisk hentet fra [Skatteetaten]({url}) av norges-lover-bot. "
            "Se [mannlig/norges-lover](https://github.com/mannlig/norges-lover) for kildekode.*",
        ]
        return "\n".join(linjer)
