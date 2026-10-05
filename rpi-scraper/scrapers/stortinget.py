"""
Scraper for Stortingets åpne data-API.
Henter saker per sesjon via det offisielle REST-API-et.
API-dokumentasjon: https://data.stortinget.no
Ingen autentisering nødvendig – dette er et åpent offentlig API.

Merk: dette er saksmetadata (tittel, status, komité, henvisning), ikke
konsolidert lovtekst.
"""

import hashlib
import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path

from .base import BaseScraper
from config import STATE_DIR

logger = logging.getLogger(__name__)

API_BASE = "https://data.stortinget.no/eksport"
_JSON = {"format": "json"}
ANTALL_SESJONER = 4

# Felt som beskriver saken. Nestede objekter (komité, emner, personer) tas
# bare med som ID-er: de har egne cache-tidsstempler («respons_dato_tid»)
# som endret seg mellom kall, og fikk tidligere de samme ~100 sakene til å
# se «endret» ut hver runde – så resten av sakene ble aldri nådd.
_STABILE_FELTER = (
    "id", "tittel", "korttittel", "type", "status", "henvisning",
    "sist_oppdatert_dato", "behandlet_sesjon_id", "innstilling_id", "dokumentgruppe",
)
_FLYKTIGE_NØKLER = {"respons_dato_tid", "versjon"}
_SESJON = re.compile(r"^(\d{4})-(\d{4})$")


def _ids(liste) -> list[str]:
    return sorted(str(x.get("id")) for x in (liste or []) if isinstance(x, dict))


def stabilt_innhold(sak: dict) -> str:
    s = {k: sak.get(k) for k in _STABILE_FELTER}
    s["komite"] = (sak.get("komite") or {}).get("id")
    s["emner"] = _ids(sak.get("emne_liste"))
    s["forslagstillere"] = _ids(sak.get("forslagstiller_liste"))
    s["saksordforere"] = _ids(sak.get("saksordfoerer_liste"))
    return json.dumps(s, ensure_ascii=False, sort_keys=True)


def uten_flyktige(o):
    if isinstance(o, dict):
        return {k: uten_flyktige(v) for k, v in o.items() if k not in _FLYKTIGE_NØKLER}
    if isinstance(o, list):
        return [uten_flyktige(x) for x in o]
    return o


def stortingsperiode(sesjon_id: str) -> str:
    """'2024-2025' → '2021-2025'. Periodene starter 2017, 2021, 2025, …"""
    år = int(sesjon_id[:4])
    start = år - (år - 2017) % 4
    return f"{start}-{start + 4}"


def sesjoner_fra_dato(i_dag: datetime, antall: int) -> list[str]:
    """Reserve hvis /sesjoner ikke svarer. Sesjonen starter 1. oktober."""
    år = i_dag.year if i_dag.month >= 10 else i_dag.year - 1
    return [f"{y}-{y + 1}" for y in range(år, år - antall, -1)]


class StortingetScraper(BaseScraper):
    name = "stortinget"
    source_url = "https://data.stortinget.no"

    def __init__(self):
        super().__init__()
        self._state: dict = {}
        self._state_path: Path | None = None

    def scrape(self, output_dir: Path, max_pages: int = 300) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        self._state_path = STATE_DIR / "stortinget-state.json"
        self._state = self._les_state()
        hasher = self._state.setdefault("saker", {})

        created: list[Path] = []
        sett: set[str] = set()
        for sesjon in self._hent_sesjoner():
            saker = self._hent_saker(sesjon)
            logger.info("Stortinget %s: %d saker", sesjon, len(saker))
            for sak in saker:
                sak_id = str(sak.get("id", ""))
                if not sak_id or sak_id in sett:
                    continue
                sett.add(sak_id)
                h = hashlib.sha256(stabilt_innhold(sak).encode()).hexdigest()[:16]
                if hasher.get(sak_id) == h:
                    continue
                if len(created) >= max_pages:
                    continue  # tas neste runde – hashen er ikke lagret
                path = self._lagre_sak(output_dir, sak, sesjon)
                if path:
                    created.append(path)
                hasher[sak_id] = h

        self.teller["i_kø"] = sum(1 for _ in sett) - len(hasher.keys() & sett)
        self._lagre_state()
        logger.info("Stortinget: %d nye/endrede filer", len(created))
        return created

    def _hent_sesjoner(self) -> list[str]:
        data = self.get_json(f"{API_BASE}/sesjoner", _JSON) or {}
        liste = data.get("sesjoner_liste", [])
        if isinstance(liste, dict):
            liste = liste.get("sesjon", [])
        ids = {str(s.get("id", "")) for s in liste if isinstance(s, dict)}
        ids = sorted((i for i in ids if _SESJON.match(i)), reverse=True)
        nåværende = str((data.get("innevaerende_sesjon") or {}).get("id", ""))
        if _SESJON.match(nåværende):
            ids = [i for i in ids if i <= nåværende]
        if not ids:
            logger.warning("Stortinget: fikk ingen sesjoner fra API – beregner fra dato")
            return sesjoner_fra_dato(datetime.now(timezone.utc), ANTALL_SESJONER)
        return ids[:ANTALL_SESJONER]

    def _hent_saker(self, sesjon: str) -> list[dict]:
        data = self.get_json(f"{API_BASE}/saker", {**_JSON, "sesjonid": sesjon})
        if not data:
            return []
        svar_sesjon = data.get("sesjon_id")
        if svar_sesjon and svar_sesjon != sesjon:
            logger.warning("Stortinget: ba om sesjon %s, fikk %s", sesjon, svar_sesjon)
            return []
        liste = data.get("saker_liste", [])
        return liste if isinstance(liste, list) else liste.get("sak", [])

    def _lagre_sak(self, output_dir: Path, sak: dict, sesjon: str) -> Path | None:
        sak_id = str(sak["id"])
        mappe = output_dir / stortingsperiode(sesjon)
        mappe.mkdir(parents=True, exist_ok=True)
        # Behold eksisterende filnavn selv om tittelen endres, så en sak ikke
        # ender opp som to filer med motstridende status.
        eksisterende = sorted(output_dir.glob(f"*/{sak_id}-*.md"))
        filepath = eksisterende[0] if eksisterende else \
            mappe / f"{sak_id}-{self.slugify(sak.get('tittel', 'ukjent'))}.md"
        formatert = self._formater_sak(sak, sesjon)
        return filepath if self.skriv_hvis_endret(filepath, stabilt_innhold(sak), formatert) else None

    def _formater_sak(self, sak: dict, sesjon: str) -> str:
        sak_id = sak.get("id", "")
        emner = ", ".join(e.get("navn", "") for e in sak.get("emne_liste") or [] if isinstance(e, dict))
        komite = (sak.get("komite") or {}).get("navn", "")
        return "\n".join([
            f"# {sak.get('tittel', 'ukjent')}",
            "",
            "## Metadata",
            "",
            f"- **Kilde:** Stortingets åpne API – {self.source_url}",
            f"- **Sak-ID:** {sak_id}",
            f"- **Type:** {sak.get('type', '')}",
            f"- **Korttittel:** {sak.get('korttittel', '')}",
            f"- **Status:** {sak.get('status', '')}",
            f"- **Henvisning:** {sak.get('henvisning', '')}",
            f"- **Komité:** {komite}",
            f"- **Emner:** {emner}",
            f"- **Behandlet i sesjon:** {sak.get('behandlet_sesjon_id') or ''}",
            f"- **Hentet fra sesjon:** {sesjon} (stortingsperiode {stortingsperiode(sesjon)})",
            f"- **Sist oppdatert i arkivet:** {self.now_iso()}",
            f"- **Sak-URL:** https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p={sak_id}",
            "",
            "> Dette er saksmetadata fra Stortinget, ikke lovtekst.",
            "",
            "## Rådata (JSON fra API)",
            "",
            "```json",
            json.dumps(uten_flyktige(sak), ensure_ascii=False, indent=2),
            "```",
            "",
            f"*Automatisk hentet fra {self.source_url} av norges-lover-bot.*",
        ])

    def _les_state(self) -> dict:
        if self._state_path and self._state_path.exists():
            try:
                data = json.loads(self._state_path.read_text(encoding="utf-8"))
                if "saker" in data:   # gammelt format («periode/sak_id»: hash) forkastes
                    return data
            except Exception:
                pass
        return {"saker": {}}

    def _lagre_state(self):
        if not self._state_path:
            return
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path.write_text(json.dumps(self._state, ensure_ascii=False, indent=2),
                                    encoding="utf-8")
