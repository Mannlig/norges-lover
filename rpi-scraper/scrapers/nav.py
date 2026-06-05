"""
Scraper for NAV – rekursiv crawler som følger alle lenker fra startpunkter.
Kilde: https://www.nav.no
"""

import json
import logging
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from .base import BaseScraper
from config import STATE_DIR

logger = logging.getLogger(__name__)

HUB_CRAWL_INTERVALL_TIMER = 24
RECRAWL_DAGER = 7

NAV_STARTPUNKTER = [
    "https://www.nav.no/dagpenger",
    "https://www.nav.no/sykepenger",
    "https://www.nav.no/foreldrepenger",
    "https://www.nav.no/barnetrygd",
    "https://www.nav.no/kontantstotte",
    "https://www.nav.no/uforetrygd",
    "https://www.nav.no/alderspensjon",
    "https://www.nav.no/arbeidsavklaringspenger",
    "https://www.nav.no/sosialhjelp",
    "https://www.nav.no/hjelpemidler",
    "https://www.nav.no/overgangsstonad-enslig",
    "https://www.nav.no/omsorgspenger",
    "https://www.nav.no/pleiepenger-sykt-barn",
    "https://www.nav.no/svangerskapspenger",
    "https://www.nav.no/grunnbelopet",
    "https://www.nav.no/pensjonsgivende-inntekt",
    "https://www.nav.no/arbeid",
    "https://www.nav.no/permittering",
    "https://www.nav.no/gjenlevendepensjon",
    "https://www.nav.no/barnepensjon",
    # Arbeidsgiver-sider
    "https://www.nav.no/arbeidsgiver",
    "https://www.nav.no/arbeidsgiver/sykepenger",
    "https://www.nav.no/arbeidsgiver/foreldrepenger",
    "https://www.nav.no/arbeidsgiver/rekruttering",
    # Satser og regelverk
    "https://www.nav.no/satser",
    "https://www.nav.no/saksbehandlingstider",
    "https://www.nav.no/klagerettigheter",
    # Spesifikke ytelser som mangler
    "https://www.nav.no/omstillingsstonad",
    "https://www.nav.no/yrkesskade",
    "https://www.nav.no/lonnsgaranti",
    "https://www.nav.no/tiltakspenger",
    "https://www.nav.no/supplerende-stonad",
]

_EKSKLUDER = re.compile(
    r"/(innlogging|logg-inn|sok|kontakt|om-nav|presse|"
    r"nyheter|arrangementer|sitemap|404|500|kontakt-oss|"
    r"minside|samarbeidspartner|[a-z]{2}/person|nav/lov|nav-loven)(/|$)",
    re.IGNORECASE,
)

_EKSKLUDER_DOMENER = re.compile(
    r"https://(arbeidsplassen|tjenester|aktivitetsplan|minside|"
    r"familie|foreldrepengerplanlegger)\.nav\.no",
    re.IGNORECASE,
)

_INNHOLD_SELEKTORER = ["main", "article", "[role='main']", ".article-body", "#maincontent"]


class NavScraper(BaseScraper):
    name = "nav"
    source_url = "https://www.nav.no"

    def __init__(self):
        super().__init__()
        self._state: dict = {}
        self._state_path: Path | None = None

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        self._state_path = STATE_DIR / "nav-state.json"
        self._state = self._les_state()

        if self._bor_crawle_huber():
            self._crawl_huber()

        created = self._hent_fra_ko(output_dir, max_pages)
        gjenstaar = sum(1 for v in self._state.get("kø", {}).values() if not v["hentet"])
        logger.info("NAV: %d filer | %d gjenstår i kø", len(created), gjenstaar)
        return created

    def _bor_crawle_huber(self) -> bool:
        sist = self._state.get("sist_hub_crawl", "")
        if not sist:
            return True
        try:
            sist_tid = datetime.fromisoformat(sist.replace("Z", "+00:00"))
            timer = (datetime.now(timezone.utc) - sist_tid).total_seconds() / 3600
            return timer >= HUB_CRAWL_INTERVALL_TIMER
        except Exception:
            return True

    def _crawl_huber(self):
        logger.info("Starter NAV hub-crawl...")
        kø = self._state.setdefault("kø", {})

        # Reset gamle oppføringer så rekursiv crawling finner nye lenker
        grense = datetime.now(timezone.utc) - timedelta(days=RECRAWL_DAGER)
        for meta in kø.values():
            if meta.get("hentet") and meta.get("sist_hentet"):
                try:
                    sist = datetime.fromisoformat(meta["sist_hentet"].replace("Z", "+00:00"))
                    if sist < grense:
                        meta["hentet"] = False
                except Exception:
                    pass

        nye = 0
        for hub_url in NAV_STARTPUNKTER:
            lenker = self._hent_lenker_fra_side(hub_url)
            logger.info("Hub %s: %d relevante lenker", hub_url, len(lenker))
            for url in lenker:
                nøkkel = self._url_til_nokkel(url)
                if nøkkel not in kø:
                    kø[nøkkel] = {"url": url, "hentet": False}
                    nye += 1
            nøkkel = self._url_til_nokkel(hub_url)
            if nøkkel not in kø:
                kø[nøkkel] = {"url": hub_url, "hentet": False}
                nye += 1

        self._state["sist_hub_crawl"] = self.now_iso()
        self._lagre_state()
        logger.info("Hub-crawl ferdig: %d nye URL-er i kø (totalt %d)", nye, len(kø))

    def _hent_lenker_fra_side(self, url: str, page=None) -> list[str]:
        if page is None:
            page = self.fetch(url)
        if not page:
            return []

        lenker = set()
        for el in page.css("a[href]"):
            href = str(el.attrib.get("href", "")).strip()
            if not href:
                continue
            if href.startswith("/"):
                href = f"https://www.nav.no{href}"
            href = href.split("#")[0].split("?")[0].rstrip("/")
            if self._er_relevant_side(href):
                lenker.add(href)
        return sorted(lenker)

    def _er_relevant_side(self, url: str) -> bool:
        if not url.startswith("https://www.nav.no/"):
            return False
        if _EKSKLUDER_DOMENER.match(url):
            return False
        if _EKSKLUDER.search(url):
            return False
        if re.search(r"\.(pdf|docx?|xlsx?|zip|png|jpg)$", url, re.I):
            return False
        if url in ("https://www.nav.no", "https://www.nav.no/"):
            return False
        return True

    @staticmethod
    def _url_til_nokkel(url: str) -> str:
        return url.replace("https://www.nav.no/", "").strip("/")

    def _hent_fra_ko(self, output_dir: Path, max_pages: int) -> list[Path]:
        kø = self._state.get("kø", {})
        venter = [(k, v) for k, v in kø.items() if not v["hentet"]]

        if not venter:
            logger.info("NAV: alle sider à jour")
            return []

        logger.info("NAV: %d sider gjenstår, henter %d nå",
                    len(venter), min(len(venter), max_pages))

        created = []
        for nøkkel, meta in venter[:max_pages]:
            path = self._hent_side(output_dir, nøkkel, meta["url"])
            if path:
                created.append(path)
            kø[nøkkel]["hentet"] = True
            kø[nøkkel]["sist_hentet"] = self.now_iso()

        self._lagre_state()
        return created

    def _hent_side(self, output_dir: Path, nøkkel: str, url: str) -> Path | None:
        page = self.fetch(url)
        if not page:
            return None

        kø = self._state.get("kø", {})
        for lenke_url in self._hent_lenker_fra_side(url, page=page):
            lenke_nøkkel = self._url_til_nokkel(lenke_url)
            if lenke_nøkkel not in kø:
                kø[lenke_nøkkel] = {"url": lenke_url, "hentet": False}

        tittel = self.hent_tittel(page)
        raa_innhold = self.side_til_markdown(page, _INNHOLD_SELEKTORER)
        if len(raa_innhold.strip()) < 100:
            logger.warning("For lite innhold (%d tegn) for %s", len(raa_innhold.strip()), url)
            return None

        deler = [d for d in nøkkel.split("/") if d]
        target_dir = output_dir
        for del_ in deler[:-1]:
            target_dir = target_dir / del_
        target_dir.mkdir(parents=True, exist_ok=True)
        filnavn = deler[-1] if deler else "index"
        filepath = target_dir / f"{filnavn}.md"

        formatert = self._formater(tittel, raa_innhold, url)
        return filepath if self.skriv_hvis_endret(filepath, raa_innhold, formatert) else None

    def _formater(self, tittel: str, innhold: str, url: str) -> str:
        return "\n".join([
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** NAV (Arbeids- og velferdsdirektoratet) – {url}",
            f"- **Sist hentet:** {self.now_iso()}",
            "",
            "## Innhold",
            "",
            innhold,
            "",
            "---",
            f"*Automatisk hentet fra [NAV]({url}) av norges-lover-bot.*",
        ])

    def _les_state(self) -> dict:
        if self._state_path and self._state_path.exists():
            try:
                return json.loads(self._state_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"sist_hub_crawl": "", "kø": {}}

    def _lagre_state(self):
        if not self._state_path:
            return
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path.write_text(
            json.dumps(self._state, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
