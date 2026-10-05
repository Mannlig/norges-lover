"""
Basis-klasse for alle scrapere.
Bruker Scrapling (StealthyFetcher) i stedet for requests+BeautifulSoup.
"""

import collections
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

from config import DELAY_MIN, DELAY_MAX, USER_AGENT
from formatters.html import html_til_markdown

logger = logging.getLogger(__name__)

_HASH_PATTERN = re.compile(r"^<!-- innholds-hash: ([a-f0-9]{64}) -->", re.MULTILINE)
_LOGG_SEPARATOR = "\n\n## Endringshistorikk\n\n"

# Utfall av siste fetch(), slik at køen kan skille feil fra suksess.
OK = "ok"
BORTE = "borte"          # 404/410 – siden finnes ikke
MIDLERTIDIG = "midlertidig"  # nettfeil, timeout, 429, 5xx, 403 – prøv igjen senere


class BaseScraper(ABC):
    name: str = "base"
    source_url: str = ""

    def __init__(self):
        self._last_request_time: float = 0.0
        self.siste_status: str = OK
        # Tellere per kjøring – leses av heartbeat for å skille en frisk
        # kilde («0 endret, 150 uendret») fra en død («0 ok, 150 feilet»).
        self.teller: collections.Counter = collections.Counter()

    # ------------------------------------------------------------------
    # Henting via Scrapling
    # ------------------------------------------------------------------

    def _polite_delay(self):
        elapsed = time.time() - self._last_request_time
        wait = random.uniform(DELAY_MIN, DELAY_MAX)
        if elapsed < wait:
            time.sleep(wait - elapsed)

    def fetch(self, url: str, retries: int = 2):
        """
        Hent en side med StealthyFetcher.
        Returnerer en Scrapling-side, eller None ved feil. Utfallet står i
        self.siste_status (OK, BORTE eller MIDLERTIDIG).
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
                    google_search=False,     # Ikke utgi oss for å komme fra Google
                    retries=1,               # Vi styrer nye forsøk selv (var 3×3)
                )
                self._last_request_time = time.time()
                status = getattr(page, "status", 200) or 200
                if status in (404, 410):
                    logger.warning("HTTP %d: %s – finnes ikke", status, url)
                    return self._utfall(BORTE)
                if status == 429 or status >= 500:
                    wait = 60 * (attempt + 1)
                    logger.warning("HTTP %d fra %s, venter %ds", status, url, wait)
                    time.sleep(wait)
                    continue
                if status >= 400:
                    logger.warning("HTTP %d: %s – hopper over", status, url)
                    return self._utfall(MIDLERTIDIG)
                logger.debug("Hentet: %s", url)
                self._utfall(OK)
                return page
            except Exception as e:
                logger.warning("Feil (forsøk %d/%d) for %s: %s", attempt + 1, retries, url, e)
                time.sleep(5 * (attempt + 1))

        logger.error("Alle %d forsøk feilet: %s", retries, url)
        return self._utfall(MIDLERTIDIG)

    def _utfall(self, status: str):
        self.siste_status = status
        self.teller["hentet_ok" if status == OK else f"feil_{status}"] += 1
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
                    data = json.loads(resp.read().decode("utf-8"))
                    self._utfall(OK)
                    return data
            except Exception as e:
                logger.warning("JSON-feil (forsøk %d/%d) %s: %s", attempt + 1, retries, url, e)
                time.sleep(5 * (attempt + 1))
        return self._utfall(MIDLERTIDIG)

    def side_til_markdown(self, page, selektorer: list[str]) -> str:
        """
        Konverter Scrapling-side til Markdown.
        Bruker første selektor som gir et element med innhold.
        """
        if page is None:
            return ""
        base_url = str(getattr(page, "url", "") or "")
        for selector in selektorer:
            element = self.css_first(page, selector)
            if element is not None:
                tekst = html_til_markdown(str(element.html_content), base_url)
                if tekst:
                    return tekst
        return ""

    def hent_tittel(self, page) -> str:
        """Hent sidetittel med flere fallback-strategier."""
        if page is None:
            return ""

        # 1. og:title meta-tag (mest spesifikk for dokument-titler)
        for el in page.css("meta[property='og:title'], meta[name='title']"):
            verdi = str(el.attrib.get("content", "")).strip()
            if verdi:
                return verdi

        # 2. Dedikert tittel-element
        for sel in [
            ".document-title", "[class*='document-title']",
            "h1.title", "[aria-label='Dokumenttittel']",
        ]:
            el = self.css_first(page, sel)
            if el and el.text:
                return str(el.text).strip()

        # 3. Første h1
        el = self.css_first(page, "h1")
        if el and el.text:
            return str(el.text).strip()

        # 4. <title>-tag, renset for nettstedssuffikser
        el = self.css_first(page, "title")
        if el and el.text:
            tittel = str(el.text).strip()
            # Fjern "– Lovdata", "| nav.no" o.l.
            for sep in [" – ", " | ", " - ", " :: "]:
                if sep in tittel:
                    tittel = tittel.split(sep)[0].strip()
            if tittel:
                return tittel

        return ""

    # ------------------------------------------------------------------
    # Endringsdeteksjon og filskriving (uendret fra forrige versjon)
    # ------------------------------------------------------------------

    def skriv_hvis_endret(self, filepath: Path, raa_innhold: str, formatert_md: str) -> bool:
        ny_hash = self._hash(raa_innhold)

        if filepath.exists():
            if self._les_hash(filepath) == ny_hash:
                logger.debug("Ingen endring: %s", filepath.name)
                self.teller["uendret"] += 1
                return False
            self.teller["endret"] += 1
            gammel_logg = self._les_endringslogg(filepath)
            ny_logg = gammel_logg + f"- **{self.today()}** Innhold endret (se git-historikk for diff)\n"
            logger.info("Endring oppdaget: %s", filepath.name)
        else:
            self.teller["ny"] += 1
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
