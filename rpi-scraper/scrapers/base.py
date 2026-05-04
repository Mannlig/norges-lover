"""
Basis-klasse for alle scrapere.
Bruker Scrapling (StealthyFetcher) i stedet for requests+BeautifulSoup.
Scrapling omgår bot-deteksjon og sporer elementer adaptivt selv om
nettsiden endrer HTML-struktur.
"""

import hashlib
import json
import logging
import random
import re
import time
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from config import DELAY_MIN, DELAY_MAX, USER_AGENT

logger = logging.getLogger(__name__)

_HASH_PATTERN = re.compile(r"^<!-- innholds-hash: ([a-f0-9]{64}) -->", re.MULTILINE)
_LOGG_SEPARATOR = "\n\n## Endringshistorikk\n\n"


class BaseScraper(ABC):
    name: str = "base"
    source_url: str = ""

    def __init__(self):
        self._last_request_time: float = 0.0

    # ------------------------------------------------------------------
    # Henting via Scrapling
    # ------------------------------------------------------------------

    def _polite_delay(self):
        elapsed = time.time() - self._last_request_time
        wait = random.uniform(DELAY_MIN, DELAY_MAX)
        if elapsed < wait:
            time.sleep(wait - elapsed)

    def fetch(self, url: str, retries: int = 3):
        """
        Hent en statisk/bot-beskyttet side med StealthyFetcher.
        Returnerer et Scrapling Adaptor-objekt, eller None ved feil.
        """
        from scrapling.fetchers import StealthyFetcher

        for attempt in range(retries):
            self._polite_delay()
            try:
                page = StealthyFetcher.fetch(
                    url,
                    headless=True,
                    network_idle=True,
                    disable_resources=True,  # Ikke last bilder/fonter – raskere
                    extra_headers={"Accept-Language": "nb-NO,nb;q=0.9"},
                )
                self._last_request_time = time.time()
                logger.debug("Hentet: %s", url)
                return page
            except Exception as e:
                msg = str(e).lower()
                if "429" in msg or "rate" in msg:
                    wait = 60 * (attempt + 1)
                    logger.warning("Rate limit fra %s, venter %ds", url, wait)
                    time.sleep(wait)
                elif "403" in msg or "404" in msg:
                    logger.warning("Tilgang nektet/ikke funnet: %s – hopper over", url)
                    return None
                else:
                    logger.warning("Feil (forsøk %d/%d) for %s: %s", attempt + 1, retries, url, e)
                    time.sleep(5 * (attempt + 1))

        logger.error("Alle %d forsøk feilet: %s", retries, url)
        return None

    @staticmethod
    def css_first(page, selector: str):
        """Returner første element som matcher selector, eller None."""
        if page is None:
            return None
        try:
            matches = page.css(selector)
            return matches[0] if matches else None
        except Exception:
            return None

    def get_json(self, url: str, params: dict | None = None, retries: int = 3) -> dict | None:
        """Hent JSON fra et åpent API (f.eks. data.stortinget.no)."""
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"
        for attempt in range(retries):
            self._polite_delay()
            try:
                req = urllib.request.Request(url, headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json",
                    "Accept-Language": "nb-NO,nb;q=0.9",
                })
                with urllib.request.urlopen(req, timeout=30) as resp:
                    self._last_request_time = time.time()
                    return json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                logger.warning("JSON-feil (forsøk %d/%d) %s: %s", attempt + 1, retries, url, e)
                time.sleep(5 * (attempt + 1))
        return None

    def side_til_markdown(self, page, selektorer: list[str]) -> str:
        """
        Konverter Scrapling-side til Markdown.
        Prøver selektorer i rekkefølge til én gir innhold.
        """
        if page is None:
            return ""

        for selector in selektorer:
            element = self.css_first(page, selector)
            if element:
                return self._element_til_markdown(element)
        return ""

    def _element_til_markdown(self, element) -> str:
        linjer = []
        for tag in element.css("h1, h2, h3, h4, p, li, dt, dd"):
            tekst = str(tag.text).strip() if tag.text else ""
            if not tekst:
                continue
            navn = tag.tag
            if navn == "h1":
                linjer.append(f"\n## {tekst}\n")
            elif navn == "h2":
                linjer.append(f"\n### {tekst}\n")
            elif navn in ("h3", "h4"):
                linjer.append(f"\n#### {tekst}\n")
            elif navn == "p":
                linjer.append(f"{tekst}\n")
            elif navn == "li":
                linjer.append(f"- {tekst}")
            elif navn == "dt":
                linjer.append(f"\n**{tekst}**")
            elif navn == "dd":
                linjer.append(f"  {tekst}")
        return "\n".join(linjer)

    def hent_tittel(self, page) -> str:
        if page is None:
            return "Ukjent tittel"
        for selector in ["h1", "title"]:
            el = self.css_first(page, selector)
            if el and el.text:
                return str(el.text).strip()
        return "Ukjent tittel"

    # ------------------------------------------------------------------
    # Endringsdeteksjon og filskriving (uendret fra forrige versjon)
    # ------------------------------------------------------------------

    def skriv_hvis_endret(self, filepath: Path, raa_innhold: str, formatert_md: str) -> bool:
        ny_hash = self._hash(raa_innhold)

        if filepath.exists():
            if self._les_hash(filepath) == ny_hash:
                logger.debug("Ingen endring: %s", filepath.name)
                return False
            gammel_logg = self._les_endringslogg(filepath)
            ny_logg = gammel_logg + f"- **{self.today()}** Innhold endret (se git-historikk for diff)\n"
            logger.info("Endring oppdaget: %s", filepath.name)
        else:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            ny_logg = f"- **{self.today()}** Første gang hentet\n"
            logger.info("Ny fil: %s", filepath.name)

        filepath.write_text(self._bygg_fil(ny_hash, formatert_md, ny_logg), encoding="utf-8")
        return True

    @staticmethod
    def _hash(tekst: str) -> str:
        return hashlib.sha256(tekst.strip().encode("utf-8")).hexdigest()

    @staticmethod
    def _les_hash(filepath: Path) -> str:
        try:
            m = _HASH_PATTERN.search(filepath.read_text(encoding="utf-8")[:200])
            return m.group(1) if m else ""
        except Exception:
            return ""

    @staticmethod
    def _les_endringslogg(filepath: Path) -> str:
        try:
            innhold = filepath.read_text(encoding="utf-8")
            if _LOGG_SEPARATOR in innhold:
                del_etter = innhold.split(_LOGG_SEPARATOR, 1)[1]
                return del_etter.split("\n---\n")[0].rstrip() + "\n"
        except Exception:
            pass
        return ""

    @staticmethod
    def _bygg_fil(hash_verdi: str, formatert_md: str, endringslogg: str) -> str:
        if _LOGG_SEPARATOR in formatert_md:
            formatert_md = formatert_md.split(_LOGG_SEPARATOR)[0]
        return (
            f"<!-- innholds-hash: {hash_verdi} -->\n\n"
            + formatert_md.rstrip()
            + _LOGG_SEPARATOR
            + endringslogg.rstrip()
            + "\n"
        )

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def today() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def slugify(self, text: str) -> str:
        text = text.lower().strip()
        text = text.replace("æ", "ae").replace("ø", "o").replace("å", "a")
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s_-]+", "-", text)
        return text[:100]

    @abstractmethod
    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        ...
