"""
Basis-klasse for alle scrapere.
Håndterer rate limiting, retry-logikk og felles logging.
"""

import logging
import random
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests

from config import DELAY_MIN, DELAY_MAX, REQUEST_TIMEOUT, USER_AGENT

logger = logging.getLogger(__name__)


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

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def today() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def slugify(self, text: str) -> str:
        """Gjør tekst til filnavn-vennlig slug."""
        import re
        text = text.lower().strip()
        text = text.replace("æ", "ae").replace("ø", "o").replace("å", "a")
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s_-]+", "-", text)
        return text[:100]

    @abstractmethod
    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        """
        Hent data og skriv til output_dir.
        Returnerer liste over filer som ble opprettet/oppdatert.
        """
        ...
