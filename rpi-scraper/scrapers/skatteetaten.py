"""
Scraper for Skatteetaten – rekursiv crawler som følger alle lenker.
Kilde: https://www.skatteetaten.no
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

SKATT_STARTPUNKTER = [
    "https://www.skatteetaten.no/satser/",
    "https://www.skatteetaten.no/person/skatt/",
    "https://www.skatteetaten.no/person/aksjer-og-verdipapirer/",
    "https://www.skatteetaten.no/person/bolig-og-eiendom/",
    "https://www.skatteetaten.no/person/arv-og-gaver/",
    "https://www.skatteetaten.no/person/skattekort/",
    "https://www.skatteetaten.no/person/skattemelding/",
    "https://www.skatteetaten.no/person/utland/",
    "https://www.skatteetaten.no/person/fradrag/",
    "https://www.skatteetaten.no/person/selvstendig-naringsdrivende/",
    "https://www.skatteetaten.no/bedrift-og-organisasjon/skatt/",
    "https://www.skatteetaten.no/bedrift-og-organisasjon/mva/",
    "https://www.skatteetaten.no/bedrift-og-organisasjon/arbeidsgiver/",
    "https://www.skatteetaten.no/bedrift-og-organisasjon/starte-bedrift/",
    "https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/",
    "https://www.skatteetaten.no/naringsdrivende/",
    # Rettskilder – Skatte-ABC (Skatteetatens tolkningshåndbok) og andre
    "https://www.skatteetaten.no/rettskilder/",
    "https://www.skatteetaten.no/rettskilder/type/handboker/",
    "https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/",
]

_SKATTE_ABC_BASE = "https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/"


def skatte_abc_kandidater(i_dag: datetime | None = None) -> list[str]:
    """
    Inngangs-URL-er for Skatte-ABC-årsutgaver.

    Oversiktssiden lister utgavene i en JS-generert meny, så lenkene finnes
    ikke i HTML-en scraperen ser – uten disse blir arkivet stående på den
    utgaven som tilfeldigvis ble crawlet først (2023). Utgavene bruker to
    navnemønstre («2023» og «2022-2023»), begge gjettes ut fra årstall så
    listen fornyer seg selv. Utgaver som ikke finnes gir 404 og hoppes over.
    """
    år = (i_dag or datetime.now(timezone.utc)).year
    kandidater = []
    for y in range(år - 2, år + 1):
        kandidater.append(f"{_SKATTE_ABC_BASE}{y}/")
        kandidater.append(f"{_SKATTE_ABC_BASE}{y}-{y + 1}/")
    return kandidater


_EKSKLUDER = re.compile(
    r"/(nn|en|se|kontakt|sok|login|logg-inn|om-skatteetaten|"
    r"presse|kurs|arrangementer|sitemap|404|500|"
    r"skjema|ettersendelse|klage)(/|$)",
    re.IGNORECASE,
)

_INKLUDER_PREFIKS = (
    "https://www.skatteetaten.no/person/",
    "https://www.skatteetaten.no/bedrift-og-organisasjon/",
    "https://www.skatteetaten.no/naringsdrivende/",
    "https://www.skatteetaten.no/satser/",
    "https://www.skatteetaten.no/rettskilder/",
    "https://www.skatteetaten.no/tema/",
)

_INNHOLD_SELEKTORER = [
    "main article", "main", "article", "[role='main']",
    ".article-content", "#main-content", ".page-content",
]


class SkatteetatenScraper(BaseScraper):
    name = "skatteetaten"
    source_url = "https://www.skatteetaten.no"

    def __init__(self):
        super().__init__()
        self._state: dict = {}
        self._state_path: Path | None = None

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        self._state_path = STATE_DIR / "skatt-state.json"
        self._state = self._les_state()

        if self._bor_crawle_huber():
            self._crawl_huber()

        created = self._hent_fra_ko(output_dir, max_pages)
        gjenstaar = sum(1 for v in self._state.get("kø", {}).values() if not v["hentet"])
        logger.info("Skatteetaten: %d filer | %d gjenstår i kø", len(created), gjenstaar)
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
        logger.info("Starter Skatteetaten hub-crawl...")
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
        for hub_url in SKATT_STARTPUNKTER + skatte_abc_kandidater():
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
                href = f"https://www.skatteetaten.no{href}"
            href = href.split("#")[0].split("?")[0].rstrip("/") + "/"
            if self._er_relevant_side(href):
                lenker.add(href)
        return sorted(lenker)

    def _er_relevant_side(self, url: str) -> bool:
        if not any(url.startswith(p) for p in _INKLUDER_PREFIKS):
            return False
        if _EKSKLUDER.search(url):
            return False
        if re.search(r"\.(pdf|docx?|xlsx?|zip|png|jpg)$", url, re.I):
            return False
        return True

    @staticmethod
    def _url_til_nokkel(url: str) -> str:
        return url.replace("https://www.skatteetaten.no/", "").strip("/")

    def _hent_fra_ko(self, output_dir: Path, max_pages: int) -> list[Path]:
        kø = self._state.get("kø", {})
        venter = [(k, v) for k, v in kø.items() if not v["hentet"]]

        if not venter:
            logger.info("Skatteetaten: alle sider à jour")
            return []

        logger.info("Skatteetaten: %d sider gjenstår, henter %d nå",
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
        if not tittel:
            tittel = nøkkel.replace("/", " – ").replace("-", " ").title()

        raa_innhold = self.side_til_markdown(page, _INNHOLD_SELEKTORER)
        if len(raa_innhold.strip()) < 100:
            logger.warning("For lite innhold (%d tegn) for %s", len(raa_innhold.strip()), url)
            return None

        oppdatert = ""
        dato_el = self.css_first(page, "time[datetime], .last-updated, [class*='updated']")
        if dato_el:
            oppdatert = dato_el.attrib.get("datetime", "") or str(dato_el.text or "")

        deler = [d for d in nøkkel.split("/") if d]
        target_dir = output_dir
        for del_ in deler[:-1]:
            target_dir = target_dir / del_
        target_dir.mkdir(parents=True, exist_ok=True)
        filnavn = deler[-1] if deler else "index"
        filepath = target_dir / f"{filnavn}.md"

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
