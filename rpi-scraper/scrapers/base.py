"""
Basis-klasse for alle scrapere.
Håndterer rate limiting, retry-logikk, hash-basert endringsdeteksjon og logging.
"""

import hashlib
import logging
import random
import re
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests

from config import DELAY_MIN, DELAY_MAX, REQUEST_TIMEOUT, USER_AGENT

logger = logging.getLogger(__name__)

# HTML-kommentar øverst i hver fil som lagrer hash av råinnhold.
# Usynlig på GitHub, men maskinlesbar for endringsdeteksjon.
_HASH_PATTERN = re.compile(r"^<!-- innholds-hash: ([a-f0-9]{64}) -->", re.MULTILINE)
_LOGG_SEPARATOR = "\n\n## Endringshistorikk\n\n"


class BaseScraper(ABC):
    """
    Alle scrapere arver fra denne klassen.
    Respekterer robots.txt-prinsippet: lav hastighet, identifiserer seg, kun offentlige sider.
    """

    name: str = "base"
    source_url: str = ""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept-Language": "nb-NO,nb;q=0.9,no;q=0.8",
        })
        self._last_request_time: float = 0.0

    # ------------------------------------------------------------------
    # HTTP
    # ------------------------------------------------------------------

    def _polite_delay(self):
        """Vent tilfeldig tid mellom DELAY_MIN og DELAY_MAX sekunder."""
        elapsed = time.time() - self._last_request_time
        wait = random.uniform(DELAY_MIN, DELAY_MAX)
        if elapsed < wait:
            time.sleep(wait - elapsed)

    def get(self, url: str, params: Optional[dict] = None, retries: int = 3) -> Optional[requests.Response]:
        """HTTP GET med rate limiting og retry."""
        for attempt in range(retries):
            self._polite_delay()
            try:
                resp = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
                self._last_request_time = time.time()
                resp.raise_for_status()
                logger.debug("GET %s → %d", url, resp.status_code)
                return resp
            except requests.exceptions.HTTPError as e:
                if e.response is not None and e.response.status_code == 429:
                    wait = 60 * (attempt + 1)
                    logger.warning("Rate limit (429) fra %s, venter %ds", url, wait)
                    time.sleep(wait)
                elif e.response is not None and e.response.status_code in (403, 404):
                    logger.warning("HTTP %d for %s – hopper over", e.response.status_code, url)
                    return None
                else:
                    logger.warning("HTTP-feil for %s: %s (forsøk %d/%d)", url, e, attempt + 1, retries)
            except requests.exceptions.RequestException as e:
                logger.warning("Nettverksfeil for %s: %s (forsøk %d/%d)", url, e, attempt + 1, retries)
                time.sleep(5 * (attempt + 1))
        logger.error("Alle %d forsøk feilet for %s", retries, url)
        return None

    # ------------------------------------------------------------------
    # Endringsdeteksjon og filskriving
    # ------------------------------------------------------------------

    def skriv_hvis_endret(
        self,
        filepath: Path,
        raa_innhold: str,
        formatert_md: str,
    ) -> bool:
        """
        Skriv fil KUN hvis rå-innholdet har endret seg siden sist.

        Args:
            filepath:     Hvor filen skal lagres.
            raa_innhold:  Kun selve lovteksten/innholdet (brukes til hashing).
                          Skal IKKE inneholde tidsstempler eller metadata som
                          endres hver kjøring.
            formatert_md: Komplett markdown-dokument som skal skrives (uten
                          endringslogg – den legges til automatisk).

        Returnerer True hvis filen ble skrevet (dvs. endring ble funnet).
        """
        ny_hash = self._hash(raa_innhold)

        if filepath.exists():
            gammel_hash = self._les_hash(filepath)
            if gammel_hash == ny_hash:
                logger.debug("Ingen endring: %s", filepath.name)
                return False
            gammel_logg = self._les_endringslogg(filepath)
            ny_logg = gammel_logg + f"- **{self.today()}** Innhold endret (se git-historikk for diff)\n"
            logger.info("Endring oppdaget: %s", filepath.name)
        else:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            ny_logg = f"- **{self.today()}** Første gang hentet\n"
            logger.info("Ny fil: %s", filepath.name)

        endelig = self._bygg_fil(ny_hash, formatert_md, ny_logg)
        filepath.write_text(endelig, encoding="utf-8")
        return True

    # ------------------------------------------------------------------
    # Interne hjelpemetoder for filformat
    # ------------------------------------------------------------------

    @staticmethod
    def _hash(tekst: str) -> str:
        return hashlib.sha256(tekst.strip().encode("utf-8")).hexdigest()

    @staticmethod
    def _les_hash(filepath: Path) -> str:
        """Hent lagret innholds-hash fra toppen av filen."""
        try:
            topp = filepath.read_text(encoding="utf-8")[:200]
            m = _HASH_PATTERN.search(topp)
            return m.group(1) if m else ""
        except Exception:
            return ""

    @staticmethod
    def _les_endringslogg(filepath: Path) -> str:
        """Hent eksisterende endringslogg fra bunnen av filen."""
        try:
            innhold = filepath.read_text(encoding="utf-8")
            if _LOGG_SEPARATOR in innhold:
                logg_del = innhold.split(_LOGG_SEPARATOR, 1)[1]
                # Fjern eventuell avsluttende fotnote
                logg_del = logg_del.split("\n---\n")[0]
                return logg_del.rstrip() + "\n"
        except Exception:
            pass
        return ""

    @staticmethod
    def _bygg_fil(hash_verdi: str, formatert_md: str, endringslogg: str) -> str:
        """Sett sammen endelig filinnhold med hash-kommentar og endringslogg."""
        # Fjern eventuell gammel endringslogg fra formatert_md
        if _LOGG_SEPARATOR in formatert_md:
            formatert_md = formatert_md.split(_LOGG_SEPARATOR)[0]

        return (
            f"<!-- innholds-hash: {hash_verdi} -->\n\n"
            + formatert_md.rstrip()
            + _LOGG_SEPARATOR
            + endringslogg.rstrip()
            + "\n"
        )

    # ------------------------------------------------------------------
    # Hjelpemetoder
    # ------------------------------------------------------------------

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def today() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def slugify(self, text: str) -> str:
        """Gjør tekst til filnavn-vennlig slug."""
        import re as _re
        text = text.lower().strip()
        text = text.replace("æ", "ae").replace("ø", "o").replace("å", "a")
        text = _re.sub(r"[^\w\s-]", "", text)
        text = _re.sub(r"[\s_-]+", "-", text)
        return text[:100]

    @abstractmethod
    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        """
        Hent data og skriv til output_dir.
        Returnerer liste over filer som faktisk ble endret/opprettet.
        """
        ...
