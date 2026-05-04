"""
Scraper for Stortingets åpne data-API.
Henter lover og proposisjoner via det offisielle REST-APIet.
API-dokumentasjon: https://data.stortinget.no
Ingen autentisering nødvendig – dette er et åpent offentlig API.
"""

import json
import logging
from pathlib import Path

from .base import BaseScraper

logger = logging.getLogger(__name__)

API_BASE = "https://data.stortinget.no/eksporter/json"


class StortingetScraper(BaseScraper):
    name = "stortinget"
    source_url = "https://data.stortinget.no"

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        created = []
        created += self._hent_saker(output_dir, max_pages)
        created += self._hent_lover(output_dir, max_pages)
        return created

    def _hent_saker(self, output_dir: Path, max_pages: int) -> list[Path]:
        created = []
        data = self.get_json(f"{API_BASE}/stortingsperioder")
        if not data:
            return created

        perioder = data.get("stortingsperioder_liste", {}).get("stortingsperiode", [])
        if not perioder:
            return created

        siste_periode = perioder[-1].get("id", "")
        logger.info("Henter saker fra periode: %s", siste_periode)

        data = self.get_json(f"{API_BASE}/saker", params={
            "stortingsperiodeid": siste_periode,
            "antall": 100,
            "start": 0,
        })
        if not data:
            return created

        saker = data.get("saker_liste", {}).get("sak", [])
        count = 0
        for sak in saker:
            if count >= max_pages:
                break
            sak_id = sak.get("id", "")
            tittel = sak.get("tittel", "ukjent")
            saktype = sak.get("type", "").lower()
            if saktype not in ("lovsak", "proposisjon", "melding"):
                continue

            path = self._lagre_sak(output_dir, sak_id, tittel, sak, siste_periode)
            if path:
                created.append(path)
                count += 1

        logger.info("Stortinget: %d saker behandlet", count)
        return created

    def _hent_lover(self, output_dir: Path, max_pages: int) -> list[Path]:
        created = []
        data = self.get_json(f"{API_BASE}/lovsaker", params={"antall": min(max_pages, 100), "start": 0})
        if not data:
            return created

        lovsaker = data.get("lovsaker_liste", {}).get("lovsak", [])
        for lov in lovsaker[:max_pages]:
            sak_id = lov.get("id", "")
            tittel = lov.get("tittel", "ukjent")
            path = self._lagre_sak(output_dir / "lovsaker", sak_id, tittel, lov, periode="")
            if path:
                created.append(path)

        return created

    def _lagre_sak(
        self, output_dir: Path, sak_id: str, tittel: str, data: dict, periode: str
    ) -> Path | None:
        if not sak_id:
            return None

        output_dir.mkdir(parents=True, exist_ok=True)
        slug = self.slugify(tittel)
        filepath = output_dir / f"{sak_id}-{slug}.md"

        # Råinnhold for hashing: kun selve sak-dataene fra API (ikke tidsstempler)
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
