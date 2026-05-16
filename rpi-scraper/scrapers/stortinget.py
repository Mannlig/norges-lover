"""
Scraper for Stortingets åpne data-API.
Henter saker (alle typer) via det offisielle REST-APIet.
API-dokumentasjon: https://data.stortinget.no
Ingen autentisering nødvendig – dette er et åpent offentlig API.
"""

import hashlib
import json
import logging
from pathlib import Path

from .base import BaseScraper

logger = logging.getLogger(__name__)

API_BASE = "https://data.stortinget.no/eksport"
_JSON = {"format": "json"}

ANTALL_PERIODER = 3
SAKER_PER_SIDE = 200


class StortingetScraper(BaseScraper):
    name = "stortinget"
    source_url = "https://data.stortinget.no"

    def __init__(self):
        super().__init__()
        self._state: dict = {}
        self._state_path: Path | None = None

    def scrape(self, output_dir: Path, max_pages: int = 100) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        self._state_path = output_dir / ".stortinget-state.json"
        self._state = self._les_state()
        created = self._hent_saker(output_dir, max_pages)
        self._lagre_state()
        return created

    def _hent_saker(self, output_dir: Path, max_pages: int) -> list[Path]:
        created = []

        perioder = self._hent_perioder()
        if not perioder:
            logger.error("Stortinget: ingen perioder hentet fra API")
            return created

        logger.info("Stortinget: henter saker fra %d periode(r): %s",
                    len(perioder), [p.get("id") for p in perioder])

        for periode in perioder:
            if len(created) >= max_pages:
                break
            periode_id = periode.get("id", "")
            filer = self._hent_saker_for_periode(output_dir, periode_id, max_pages - len(created))
            created.extend(filer)

        logger.info("Stortinget: %d nye/endrede filer totalt", len(created))
        return created

    def _hent_perioder(self) -> list[dict]:
        data = self.get_json(f"{API_BASE}/stortingsperioder", _JSON)
        if not data:
            return []
        liste = data.get("stortingsperioder_liste", [])
        perioder = liste if isinstance(liste, list) else liste.get("stortingsperiode", [])
        return perioder[:ANTALL_PERIODER]

    def _hent_saker_for_periode(self, output_dir: Path, periode_id: str, max_pages: int) -> list[Path]:
        created = []
        start = 0

        while len(created) < max_pages:
            data = self.get_json(f"{API_BASE}/saker", {
                **_JSON,
                "stortingsperiodeid": periode_id,
                "antall": SAKER_PER_SIDE,
                "start": start,
            })
            if not data:
                break

            saker_data = data.get("saker_liste", [])
            saker = saker_data if isinstance(saker_data, list) else saker_data.get("sak", [])

            if not saker:
                break

            if start == 0:
                typer = {s.get("type", "ukjent") for s in saker}
                logger.info("Stortinget periode %s: sakstyper funnet i API: %s", periode_id, typer)

            for sak in saker:
                if len(created) >= max_pages:
                    break
                sak_id = sak.get("id", "")
                if not sak_id:
                    continue

                nøkkel = f"{periode_id}/{sak_id}"
                sak_hash = self._sak_hash(sak)
                if self._state.get(nøkkel) == sak_hash:
                    continue

                tittel = sak.get("tittel", "ukjent")
                path = self._lagre_sak(output_dir, sak_id, tittel, sak, periode_id)
                if path:
                    created.append(path)
                self._state[nøkkel] = sak_hash

            if len(saker) < SAKER_PER_SIDE:
                break
            start += SAKER_PER_SIDE

        return created

    @staticmethod
    def _sak_hash(sak: dict) -> str:
        return hashlib.sha256(
            json.dumps(sak, ensure_ascii=False, sort_keys=True).encode()
        ).hexdigest()[:16]

    def _lagre_sak(
        self, output_dir: Path, sak_id: str, tittel: str, data: dict, periode: str
    ) -> Path | None:
        slug = self.slugify(tittel)
        periode_dir = output_dir / periode
        periode_dir.mkdir(parents=True, exist_ok=True)
        filepath = periode_dir / f"{sak_id}-{slug}.md"

        raa_innhold = json.dumps(data, ensure_ascii=False, sort_keys=True)
        formatert = self._formater_sak(sak_id, tittel, data, periode)

        endret = self.skriv_hvis_endret(filepath, raa_innhold, formatert)
        return filepath if endret else None

    def _formater_sak(self, sak_id: str, tittel: str, data: dict, periode: str) -> str:
        sakstype = data.get("type", "")
        korttittel = data.get("korttittel", "")
        status = data.get("status", "")
        behandlet = data.get("behandlet_dato", "")
        sak_url = f"https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p={sak_id}"

        return "\n".join([
            f"# {tittel}",
            "",
            "## Metadata",
            "",
            f"- **Kilde:** Stortingets åpne API – {self.source_url}",
            f"- **Sak-ID:** {sak_id}",
            f"- **Type:** {sakstype}",
            f"- **Korttittel:** {korttittel}",
            f"- **Status:** {status}",
            f"- **Stortingsperiode:** {periode}",
            f"- **Behandlet:** {behandlet}",
            f"- **Sist hentet:** {self.now_iso()}",
            f"- **Sak-URL:** {sak_url}",
            "",
            "## Rådata (JSON fra API)",
            "",
            "```json",
            json.dumps(data, ensure_ascii=False, indent=2),
            "```",
            "",
            f"*Automatisk hentet fra {self.source_url} av norges-lover-bot. "
            "Se [mannlig/norges-lover](https://github.com/mannlig/norges-lover) for kildekode.*",
        ])

    def _les_state(self) -> dict:
        if self._state_path and self._state_path.exists():
            try:
                return json.loads(self._state_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {}

    def _lagre_state(self):
        if not self._state_path:
            return
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path.write_text(
            json.dumps(self._state, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
