"""
Scraper for Lovdata – henter alle nasjonale lover, stortingsvedtak og lokale forskrifter.

Kjører i to faser:
  1. Register-crawl (én gang per 24t): Henter alle dokument-URL-er fra registersidene
     og lagrer dem i DATA_DIR/.lovdata-state.json
  2. Dokument-henting: Prosesserer køen inntil max_pages per kjøring

Kilde: https://lovdata.no
"""

import json
import logging
import re
import time
from pathlib import Path

from .base import BaseScraper

logger = logging.getLogger(__name__)

# Register-sider å crawle (url, type-slug, output-submappe)
REGISTRE = [
    ("https://lovdata.no/register/lover",               "lover",               "lover"),
    ("https://lovdata.no/register/stortingsvedtak",     "stortingsvedtak",     "stortingsvedtak"),
    ("https://lovdata.no/register/lokaleForskrifter",   "lokale-forskrifter",  "lokale-forskrifter"),
]

# Maks timer mellom register-crawl
REGISTER_CRAWL_INTERVALL_TIMER = 24

# Linker vi er interessert i (path-prefix)
_LOV_PREFIXES = ("/lov/", "/stv/", "/lf/", "/dokument/NL/", "/dokument/LT/", "/dokument/SF/")

# Tekst-mønstre som indikerer UI-elementer, ikke lovtekst
_UI_MØNSTRE = re.compile(
    r"^(Verktøylinje|Del dokument|Trykk Escape|Innholdsfortegnelse|"
    r"Søk i loven|Skriv ut|Meld feil|Følg loven|Lukk|Åpne|"
    r"Gå til|Hopp til|Tilbake|Forrige|Neste|Hjem|Meny|"
    r"Last ned|PDF|EPUB|Print)$",
    re.IGNORECASE,
)

# Prøv disse selektorene for å finne selve lovteksten – fra mest til minst spesifikk
_INNHOLD_SELEKTORER = [
    ".document-content",
    ".law-document",
    "[class*='document-body']",
    "[class*='law-content']",
    "[class*='lovtekst']",
    "#lovtekst",
    "article.document",
    "section.document",
    "article",
]

# Fallback – filtrer innholdet fra main
_FALLBACK_SELEKTOR = "main"

# Minimumslengde for at innhold regnes som gyldig
_MIN_INNHOLD_LENGDE = 200


class LovdataScraper(BaseScraper):
    name = "lovdata"
    source_url = "https://lovdata.no"

    def __init__(self):
        super().__init__()
        self._state: dict = {}
        self._state_path: Path | None = None

    # -------------------------------------------------------------------------
    # Hoved-inngang
    # -------------------------------------------------------------------------

    def scrape(self, output_dir: Path, max_pages: int = 100) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        self._state_path = output_dir / ".lovdata-state.json"
        self._state = self._les_state()

        # Fase 1: Oppdater URL-kø fra registersider om det er lenge siden
        if self._bor_crawle_register():
            self._crawl_alle_registre(output_dir)

        # Fase 2: Hent dokumenter fra køen
        created = self._hent_fra_ko(output_dir, max_pages)

        gjenstaar = sum(1 for v in self._state.get("kø", {}).values() if not v["hentet"])
        logger.info("Lovdata: %d filer endret/nye | %d gjenstår i kø", len(created), gjenstaar)
        return created

    # -------------------------------------------------------------------------
    # Fase 1 – Register-crawl
    # -------------------------------------------------------------------------

    @staticmethod
    def _er_utdatert(iso_tid: str, maks_dager: int) -> bool:
        if not iso_tid:
            return True
        try:
            from datetime import datetime, timezone
            sist = datetime.fromisoformat(iso_tid.replace("Z", "+00:00"))
            alder_dager = (datetime.now(timezone.utc) - sist).days
            return alder_dager >= maks_dager
        except Exception:
            return True

    def _bor_crawle_register(self) -> bool:
        sist = self._state.get("sist_register_crawl", "")
        if not sist:
            return True
        try:
            from datetime import datetime, timezone
            sist_tid = datetime.fromisoformat(sist.replace("Z", "+00:00"))
            fra_sist = (datetime.now(timezone.utc) - sist_tid).total_seconds() / 3600
            return fra_sist >= REGISTER_CRAWL_INTERVALL_TIMER
        except Exception:
            return True

    def _crawl_alle_registre(self, output_dir: Path):
        logger.info("Starter register-crawl fra Lovdata (én gang per 24t)...")
        kø = self._state.setdefault("kø", {})
        totalt_nye = 0

        for reg_url, type_slug, _ in REGISTRE:
            urls = self._crawl_register(reg_url, type_slug)
            for dok_url, slug, tittel in urls:
                nøkkel = f"{type_slug}/{slug}"
                if nøkkel not in kø:
                    kø[nøkkel] = {
                        "url": dok_url,
                        "slug": slug,
                        "tittel": tittel,
                        "type": type_slug,
                        "hentet": False,
                    }
                    totalt_nye += 1

        self._state["sist_register_crawl"] = self.now_iso()
        self._lagre_state()
        logger.info("Register-crawl ferdig: %d nye URL-er lagt til køen", totalt_nye)

    def _crawl_register(self, base_url: str, type_slug: str) -> list[tuple[str, str, str]]:
        """Paginer gjennom en registreside og returner (url, slug, tittel)-tupler."""
        resultater = []
        sett_url = set()

        for side in range(1, 600):  # Lovdata har maks ~475 sider for lokale forskrifter
            url = f"{base_url}?start={(side - 1) * 25}" if side > 1 else base_url
            page = self._dynamic_fetch(url)
            if not page:
                break

            lenker = self._trekk_ut_register_lenker(page)
            if not lenker:
                logger.info("Ingen lenker på side %d av %s – stopper", side, base_url)
                break

            nye_på_side = 0
            for dok_url, slug, tittel in lenker:
                if dok_url not in sett_url:
                    sett_url.add(dok_url)
                    resultater.append((dok_url, slug, tittel))
                    nye_på_side += 1

            logger.info("Register %s side %d: %d lenker (totalt %d)",
                        type_slug, side, nye_på_side, len(resultater))
            self._lagre_state()  # Lagre etter hver side – crash-sikker

        return resultater

    def _trekk_ut_register_lenker(self, page) -> list[tuple[str, str, str]]:
        """Hent alle lenker til lovdokumenter fra en side."""
        lenker = []
        for el in page.css("a[href]"):
            href = str(el.attrib.get("href", "")).strip()
            if not href or not any(href.startswith(p) for p in _LOV_PREFIXES):
                continue

            # Normaliser til absolutt URL
            if href.startswith("/"):
                href = f"https://lovdata.no{href}"

            # Bruk kanonisk dokument-URL om mulig
            href = self._normaliser_url(href)

            tekst = str(el.text or "").strip()
            slug = self.slugify(tekst) if len(tekst) > 3 else href.rstrip("/").split("/")[-1]
            lenker.append((href, slug, tekst))

        return lenker

    @staticmethod
    def _normaliser_url(url: str) -> str:
        """Gjør /lov/ID om til /dokument/NL/lov/ID for direkte henting."""
        if re.match(r"https://lovdata\.no/lov/", url):
            return url.replace("https://lovdata.no/lov/", "https://lovdata.no/dokument/NL/lov/")
        if re.match(r"https://lovdata\.no/stv/", url):
            return url.replace("https://lovdata.no/stv/", "https://lovdata.no/dokument/LT/stv/")
        if re.match(r"https://lovdata\.no/lf/", url):
            return url.replace("https://lovdata.no/lf/", "https://lovdata.no/dokument/LF/lf/")
        return url

    # -------------------------------------------------------------------------
    # Fase 2 – Hent dokumenter fra kø
    # -------------------------------------------------------------------------

    def _hent_fra_ko(self, output_dir: Path, max_pages: int) -> list[Path]:
        from config import LOVDATA_RESJEKK_DAGER
        kø = self._state.get("kø", {})

        # Nye URL-er (aldri hentet) har prioritet
        nye = [(k, v) for k, v in kø.items() if not v["hentet"]]

        # Dokumenter som ikke er sjekket på LOVDATA_RESJEKK_DAGER
        gamle = [
            (k, v) for k, v in kø.items()
            if v["hentet"] and self._er_utdatert(v.get("sist_hentet", ""), LOVDATA_RESJEKK_DAGER)
        ]

        venter = nye + gamle
        if not venter:
            logger.info("Lovdata: alle dokumenter er à jour (re-sjekkes om %d dager)",
                        LOVDATA_RESJEKK_DAGER)
            return []

        if nye:
            logger.info("Lovdata: %d nye + %d klare for re-sjekk (henter %d nå)",
                        len(nye), len(gamle), min(len(venter), max_pages))
        else:
            logger.info("Lovdata: %d dokumenter klare for re-sjekk (henter %d nå)",
                        len(gamle), min(len(venter), max_pages))

        created = []
        for nøkkel, meta in venter[:max_pages]:
            type_slug = meta["type"]
            target_dir = output_dir / type_slug
            target_dir.mkdir(parents=True, exist_ok=True)

            path = self._hent_dokument(target_dir, meta["url"], meta["slug"], meta["tittel"])
            if path:
                created.append(path)

            # Marker som hentet og oppdater tidsstempel
            kø[nøkkel]["hentet"] = True
            kø[nøkkel]["sist_hentet"] = self.now_iso()

        self._lagre_state()
        return created

    def _hent_dokument(
        self, output_dir: Path, url: str, slug: str, kjent_tittel: str = ""
    ) -> Path | None:
        filepath = output_dir / f"{slug}.md"

        page = self._dynamic_fetch(url)
        if not page:
            return None

        tittel = self.hent_tittel(page) or kjent_tittel or slug
        innhold = self._hent_lovtekst(page)

        if len(innhold.strip()) < _MIN_INNHOLD_LENGDE:
            logger.warning("For lite innhold (%d tegn) for %s", len(innhold.strip()), url)
            return None

        oppdatert = ""
        for sel in ["time[datetime]", ".last-updated", ".date-modified", "time"]:
            el = self.css_first(page, sel)
            if el:
                oppdatert = el.attrib.get("datetime", "") or str(el.text or "")
                if oppdatert:
                    break

        formatert = self._formater(tittel, innhold, url, oppdatert.strip())
        return filepath if self.skriv_hvis_endret(filepath, innhold, formatert) else None

    # -------------------------------------------------------------------------
    # Innholdsuthenting
    # -------------------------------------------------------------------------

    def _hent_lovtekst(self, page) -> str:
        """
        Prøver spesifikke selektorer først, faller tilbake til filtrert main-innhold.
        """
        # Prøv spesifikke selektorer
        for sel in _INNHOLD_SELEKTORER:
            el = self.css_first(page, sel)
            if el:
                tekst = self._element_til_markdown_filtrert(el)
                if len(tekst.strip()) >= _MIN_INNHOLD_LENGDE:
                    return tekst

        # Fallback: main med filtrering av UI-støy
        el = self.css_first(page, _FALLBACK_SELEKTOR)
        if el:
            return self._element_til_markdown_filtrert(el)

        return ""

    def _element_til_markdown_filtrert(self, element) -> str:
        """
        Konverterer HTML til Markdown og filtrerer ut navigasjonselementer.
        Prioriterer §-paragrafer og kapitteltitler.
        """
        linjer = []
        for tag in element.css("h1, h2, h3, h4, h5, p, li, dt, dd"):
            tekst = str(tag.text or "").strip()
            if not tekst or len(tekst) < 2:
                continue

            # Filtrer kjente UI-elementer
            if _UI_MØNSTRE.match(tekst):
                continue

            # Filtrer veldig korte linjer som sannsynligvis er knapper/ikoner
            if len(tekst) < 4 and not tekst.startswith("§"):
                continue

            navn = tag.tag
            if navn == "h1":
                linjer.append(f"\n## {tekst}\n")
            elif navn == "h2":
                linjer.append(f"\n### {tekst}\n")
            elif navn in ("h3", "h4", "h5"):
                linjer.append(f"\n#### {tekst}\n")
            elif navn == "p":
                # Fremhev paragraf-markører (§ 1, § 2 osv.)
                if re.match(r"^§\s*\d+", tekst):
                    linjer.append(f"\n**{tekst}**\n")
                else:
                    linjer.append(f"{tekst}\n")
            elif navn == "li":
                linjer.append(f"- {tekst}")
            elif navn == "dt":
                linjer.append(f"\n**{tekst}**")
            elif navn == "dd":
                linjer.append(f"  {tekst}")

        return "\n".join(linjer)

    # -------------------------------------------------------------------------
    # DynamicFetcher (Playwright)
    # -------------------------------------------------------------------------

    def _dynamic_fetch(self, url: str, retries: int = 3):
        from scrapling.fetchers import DynamicFetcher

        for attempt in range(retries):
            self._polite_delay()
            try:
                page = DynamicFetcher.fetch(
                    url,
                    headless=True,
                    network_idle=True,
                    disable_resources=True,
                )
                self._last_request_time = time.time()
                status = getattr(page, "status", 200)
                if status >= 400:
                    logger.warning("HTTP %d: %s", status, url)
                    return None
                return page
            except Exception as e:
                logger.warning("DynamicFetcher feil (forsøk %d/%d) %s: %s",
                               attempt + 1, retries, url, e)
                time.sleep(10 * (attempt + 1))
        return None

    # -------------------------------------------------------------------------
    # State-fil
    # -------------------------------------------------------------------------

    def _les_state(self) -> dict:
        if self._state_path and self._state_path.exists():
            try:
                return json.loads(self._state_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"sist_register_crawl": "", "kø": {}}

    def _lagre_state(self):
        if not self._state_path:
            return
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path.write_text(
            json.dumps(self._state, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # -------------------------------------------------------------------------
    # Formatering
    # -------------------------------------------------------------------------

    def _formater(self, tittel: str, innhold: str, url: str, oppdatert: str) -> str:
        return "\n".join([
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** Lovdata – {url}",
            f"- **Sist oppdatert (kilde):** {oppdatert or 'ukjent'}",
            f"- **Sist hentet:** {self.now_iso()}",
            "",
            "## Innhold",
            "",
            innhold,
            "",
            "---",
            f"*Automatisk hentet fra [Lovdata]({url}) av norges-lover-bot.*",
        ])
