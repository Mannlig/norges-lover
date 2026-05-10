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

# Viktige lover som alltid skal være i køen – supplement til register-crawl
# som bare finner nyeste endringer. Format: (url, slug, tittel)
SEED_LOVER = [
    ("https://lovdata.no/dokument/NL/lov/1814-05-17",     "grunnloven",                    "Kongeriket Norges Grunnlov"),
    ("https://lovdata.no/dokument/NL/lov/1902-05-22-10",  "straffeloven-1902",             "Straffeloven 1902"),
    ("https://lovdata.no/dokument/NL/lov/2005-05-20-28",  "straffeloven",                  "Straffeloven"),
    ("https://lovdata.no/dokument/NL/lov/1981-05-22-25",  "straffeprosessloven",           "Straffeprosessloven"),
    ("https://lovdata.no/dokument/NL/lov/2005-06-17-90",  "tvisteloven",                   "Tvisteloven"),
    ("https://lovdata.no/dokument/NL/lov/1967-02-10",     "forvaltningsloven",             "Forvaltningsloven"),
    ("https://lovdata.no/dokument/NL/lov/2006-05-19-16",  "offentleglova",                 "Offentleglova"),
    ("https://lovdata.no/dokument/NL/lov/1999-05-21-30",  "menneskerettsloven",            "Menneskerettsloven"),
    ("https://lovdata.no/dokument/NL/lov/1918-05-31-4",   "avtaleloven",                   "Avtaleloven"),
    ("https://lovdata.no/dokument/NL/lov/1988-05-13-27",  "kjopsloven",                    "Kjøpsloven"),
    ("https://lovdata.no/dokument/NL/lov/2002-06-21-34",  "forbrukerkjopsloven",           "Forbrukerkjøpsloven"),
    ("https://lovdata.no/dokument/NL/lov/2014-06-20-27",  "angrerettloven",                "Angrerettloven"),
    ("https://lovdata.no/dokument/NL/lov/1969-06-13-26",  "skadeserstatningsloven",        "Skadeserstatningsloven"),
    ("https://lovdata.no/dokument/NL/lov/1988-12-23-104", "produktansvarsloven",           "Produktansvarsloven"),
    ("https://lovdata.no/dokument/NL/lov/1999-03-26-14",  "skatteloven",                   "Skatteloven"),
    ("https://lovdata.no/dokument/NL/lov/2016-05-27-14",  "skatteforvaltningsloven",       "Skatteforvaltningsloven"),
    ("https://lovdata.no/dokument/NL/lov/2005-06-17-67",  "skattebetalingsloven",          "Skattebetalingsloven"),
    ("https://lovdata.no/dokument/NL/lov/2009-06-19-58",  "merverdiavgiftsloven",          "Merverdiavgiftsloven"),
    ("https://lovdata.no/dokument/NL/lov/2007-12-21-119", "tolloven",                      "Tolloven"),
    ("https://lovdata.no/dokument/NL/lov/1980-02-29-4",   "ligningsloven",                 "Ligningsloven"),
    ("https://lovdata.no/dokument/NL/lov/1997-06-13-44",  "aksjeloven",                    "Aksjeloven"),
    ("https://lovdata.no/dokument/NL/lov/1997-06-13-45",  "allmennaksjeloven",             "Allmennaksjeloven"),
    ("https://lovdata.no/dokument/NL/lov/1985-06-21-83",  "selskapsloven",                 "Selskapsloven"),
    ("https://lovdata.no/dokument/NL/lov/2007-06-29-81",  "samvirkelova",                  "Samvirkelova"),
    ("https://lovdata.no/dokument/NL/lov/1998-07-17-56",  "regnskapsloven",                "Regnskapsloven"),
    ("https://lovdata.no/dokument/NL/lov/1984-06-08-58",  "konkursloven",                  "Konkursloven"),
    ("https://lovdata.no/dokument/NL/lov/1984-06-08-59",  "dekningsloven",                 "Dekningsloven"),
    ("https://lovdata.no/dokument/NL/lov/1992-06-26-86",  "tvangsfullbyrdelsesloven",      "Tvangsfullbyrdelsesloven"),
    ("https://lovdata.no/dokument/NL/lov/2005-06-17-62",  "arbeidsmiljoloven",             "Arbeidsmiljøloven"),
    ("https://lovdata.no/dokument/NL/lov/1988-04-29-21",  "ferieloven",                    "Ferieloven"),
    ("https://lovdata.no/dokument/NL/lov/2012-01-27-9",   "arbeidstvistloven",             "Arbeidstvistloven"),
    ("https://lovdata.no/dokument/NL/lov/1993-06-04-58",  "allmenngjoringsloven",          "Allmenngjøringsloven"),
    ("https://lovdata.no/dokument/NL/lov/1989-06-16-65",  "yrkesskadeforsikringsloven",    "Yrkesskadeforsikringsloven"),
    ("https://lovdata.no/dokument/NL/lov/1973-03-14-4",   "lonnsgarantiloven",             "Lønnsgarantiloven"),
    ("https://lovdata.no/dokument/NL/lov/1997-02-28-19",  "folketrygdloven",               "Folketrygdloven"),
    ("https://lovdata.no/dokument/NL/lov/2000-03-24-16",  "foretakspensjonsloven",         "Foretakspensjonsloven"),
    ("https://lovdata.no/dokument/NL/lov/2000-11-24-81",  "innskuddspensjonsloven",        "Innskuddspensjonsloven"),
    ("https://lovdata.no/dokument/NL/lov/1981-04-08-7",   "barnelova",                     "Barnelova"),
    ("https://lovdata.no/dokument/NL/lov/1991-07-04-47",  "ekteskapsloven",                "Ekteskapsloven"),
    ("https://lovdata.no/dokument/NL/lov/2019-06-14-21",  "arveloven",                     "Arveloven"),
    ("https://lovdata.no/dokument/NL/lov/2021-06-18-97",  "barnevernsloven",               "Barnevernsloven"),
    ("https://lovdata.no/dokument/NL/lov/1999-03-26-17",  "husleieloven",                  "Husleieloven"),
    ("https://lovdata.no/dokument/NL/lov/1997-06-13-43",  "bustadoppforingslova",          "Bustadoppføringslova"),
    ("https://lovdata.no/dokument/NL/lov/2017-06-16-65",  "eierseksjonsloven",             "Eierseksjonsloven"),
    ("https://lovdata.no/dokument/NL/lov/2003-06-06-39",  "borettslagslova",               "Borettslagslova"),
    ("https://lovdata.no/dokument/NL/lov/1980-02-08-2",   "panteloven",                    "Panteloven"),
    ("https://lovdata.no/dokument/NL/lov/1935-06-07-2",   "tinglysingsloven",              "Tinglysingsloven"),
    ("https://lovdata.no/dokument/NL/lov/1996-12-20-106", "tomtefesteloven",               "Tomtefesteloven"),
    ("https://lovdata.no/dokument/NL/lov/2003-11-28-98",  "konsesjonsloven",               "Konsesjonsloven"),
    ("https://lovdata.no/dokument/NL/lov/1995-05-12-23",  "jordlova",                      "Jordlova"),
    ("https://lovdata.no/dokument/NL/lov/2008-06-27-71",  "plan-og-bygningsloven",         "Plan- og bygningsloven"),
    ("https://lovdata.no/dokument/NL/lov/2009-06-19-100", "naturmangfoldloven",            "Naturmangfoldloven"),
    ("https://lovdata.no/dokument/NL/lov/1981-03-13-6",   "forurensningsloven",            "Forurensningsloven"),
    ("https://lovdata.no/dokument/NL/lov/1957-06-28-16",  "friluftsloven",                 "Friluftsloven"),
    ("https://lovdata.no/dokument/NL/lov/1990-06-29-50",  "energiloven",                   "Energiloven"),
    ("https://lovdata.no/dokument/NL/lov/1996-11-29-72",  "petroleumsloven",               "Petroleumsloven"),
    ("https://lovdata.no/dokument/NL/lov/1998-07-17-61",  "opplaringslova",                "Opplæringslova"),
    ("https://lovdata.no/dokument/NL/lov/2005-04-01-15",  "universitets-og-hoyskolelov",   "Universitets- og høyskoleloven"),
    ("https://lovdata.no/dokument/NL/lov/2008-05-15-35",  "utlendingsloven",               "Utlendingsloven"),
    ("https://lovdata.no/dokument/NL/lov/2005-06-10-51",  "statsborgerskapsloven",         "Statsborgerskapsloven"),
    ("https://lovdata.no/dokument/NL/lov/2018-06-22-83",  "kommuneloven",                  "Kommuneloven"),
    ("https://lovdata.no/dokument/NL/lov/2002-06-28-57",  "valgloven",                     "Valgloven"),
    ("https://lovdata.no/dokument/NL/lov/1999-07-02-63",  "pasient-og-brukerrettighetsloven", "Pasient- og brukerrettighetsloven"),
    ("https://lovdata.no/dokument/NL/lov/1999-07-02-64",  "helsepersonelloven",            "Helsepersonelloven"),
    ("https://lovdata.no/dokument/NL/lov/1999-07-02-61",  "spesialisthelsetjenesteloven",  "Spesialisthelsetjenesteloven"),
    ("https://lovdata.no/dokument/NL/lov/1999-07-02-62",  "psykisk-helsevernloven",        "Psykisk helsevernloven"),
    ("https://lovdata.no/dokument/NL/lov/1994-08-05-55",  "smittevernloven",               "Smittevernloven"),
    ("https://lovdata.no/dokument/NL/lov/1992-12-04-132", "legemiddelloven",               "Legemiddelloven"),
    ("https://lovdata.no/dokument/NL/lov/1992-12-04-126", "arkivloven",                    "Arkivloven"),
    ("https://lovdata.no/dokument/NL/lov/2018-06-15-38",  "personopplysningsloven",        "Personopplysningsloven"),
    ("https://lovdata.no/dokument/NL/lov/2016-06-17-73",  "anskaffelsesloven",             "Anskaffelsesloven"),
    ("https://lovdata.no/dokument/NL/lov/2017-06-16-51",  "likestillings-og-diskrimineringsloven", "Likestillings- og diskrimineringsloven"),
    ("https://lovdata.no/dokument/NL/lov/2017-06-16-67",  "statsansatteloven",             "Statsansatteloven"),
    ("https://lovdata.no/dokument/NL/lov/2009-01-09-2",   "markedsforingsloven",           "Markedsføringsloven"),
    ("https://lovdata.no/dokument/NL/lov/2020-11-18-146", "finansavtaleloven",             "Finansavtaleloven"),
    ("https://lovdata.no/dokument/NL/lov/1989-06-16-69",  "forsikringsavtaleloven",        "Forsikringsavtaleloven"),
    ("https://lovdata.no/dokument/NL/lov/2007-06-29-75",  "verdipapirhandelloven",         "Verdipapirhandelloven"),
    ("https://lovdata.no/dokument/NL/lov/2015-04-10-17",  "finansforetaksloven",           "Finansforetaksloven"),
    ("https://lovdata.no/dokument/NL/lov/1965-06-18-4",   "vegtrafikkloven",               "Vegtrafikkloven"),
    ("https://lovdata.no/dokument/NL/lov/1993-06-11-101", "luftfartsloven",                "Luftfartsloven"),
    ("https://lovdata.no/dokument/NL/lov/1994-06-24-39",  "sjoloven",                      "Sjøloven"),
    ("https://lovdata.no/dokument/NL/lov/2003-12-19-124", "matloven",                      "Matloven"),
    ("https://lovdata.no/dokument/NL/lov/1989-06-02-27",  "alkoholloven",                  "Alkoholloven"),
    ("https://lovdata.no/dokument/NL/lov/2009-06-19-97",  "dyrevelferdsloven",             "Dyrevelferdsloven"),
    ("https://lovdata.no/dokument/NL/lov/2009-12-18-131", "sosialtjenesteloven",           "Sosialtjenesteloven"),
    ("https://lovdata.no/dokument/NL/lov/2016-12-09-88",  "folkeregisterloven",            "Folkeregisterloven"),
    ("https://lovdata.no/dokument/NL/lov/2003-12-05-100", "bioteknologiloven",             "Bioteknologiloven"),
    ("https://lovdata.no/dokument/NL/lov/2016-06-10-23",  "politiloven",                   "Politiloven"),
    ("https://lovdata.no/dokument/NL/lov/1995-08-04-53",  "politiloven-1995",              "Politiloven"),
    ("https://lovdata.no/dokument/NL/lov/1992-07-17-99",  "gjeldsordningsloven",           "Gjeldsordningsloven"),
    ("https://lovdata.no/dokument/NL/lov/1961-02-03",     "bilansvarslova",                "Bilansvarslova"),
    ("https://lovdata.no/dokument/NL/lov/2020-11-06-127", "integreringsloven",             "Integreringsloven"),
]

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

        # Fase 0: Legg til viktige lover som mangler i køen (kjøres alltid, rask)
        self._seed_koen()
        self._reparer_feil_titler(output_dir)

        # Fase 1: Oppdater URL-kø fra registersider om det er lenge siden
        if self._bor_crawle_register():
            self._crawl_alle_registre(output_dir)

        # Fase 2: Hent dokumenter fra køen
        created = self._hent_fra_ko(output_dir, max_pages)

        gjenstaar = sum(1 for v in self._state.get("kø", {}).values() if not v["hentet"])
        logger.info("Lovdata: %d filer endret/nye | %d gjenstår i kø", len(created), gjenstaar)
        return created

    def _reparer_feil_titler(self, output_dir: Path):
        """Fiks filer der tittelen er en generisk navigasjonstitel (f.eks. 'Hoved­meny')."""
        _GENERISKE = {"hoved­meny", "hoved-meny", "hovedmeny", "meny", "menu", "navigation"}
        kø = self._state.get("kø", {})
        fikset = 0
        for meta in kø.values():
            kjent_tittel = meta.get("tittel", "")
            if not kjent_tittel:
                continue
            filepath = output_dir / meta["type"] / f"{meta['slug']}.md"
            if not filepath.exists():
                continue
            innhold = filepath.read_text(encoding="utf-8")
            for line in innhold.splitlines():
                if line.startswith("# "):
                    current_title = line[2:].strip()
                    if current_title.lower() in _GENERISKE:
                        ny_innhold = innhold.replace(f"# {current_title}\n", f"# {kjent_tittel}\n", 1)
                        filepath.write_text(ny_innhold, encoding="utf-8")
                        fikset += 1
                    break
        if fikset:
            logger.info("Reparerte %d filer med feil navigasjonstitel", fikset)

    def _seed_koen(self):
        """Legg til lovene fra SEED_LOVER i køen om de mangler (rask, ingen nettverkskall)."""
        kø = self._state.setdefault("kø", {})
        nye = 0
        for url, slug, tittel in SEED_LOVER:
            nøkkel = f"lover/{slug}"
            if nøkkel not in kø:
                kø[nøkkel] = {
                    "url": url,
                    "slug": slug,
                    "tittel": tittel,
                    "type": "lover",
                    "hentet": False,
                }
                nye += 1
        if nye:
            self._lagre_state()
            logger.info("Seed: %d nye lover lagt til køen", nye)

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
        neste_url: str | None = base_url

        for side in range(1, 600):  # Lovdata har maks ~475 sider for lokale forskrifter
            url = neste_url or f"{base_url}?start={(side - 1) * 25}"
            page = self._fetch_register(url)
            if not page:
                logger.warning("Register %s side %d: fetch feilet for %s", type_slug, side, url)
                break

            # Diagnostisk logging – hjelper oss forstå hva Lovdata returnerer
            alle_href = [str(el.attrib.get("href", "")) for el in page.css("a[href]")]
            ikke_match = [h for h in alle_href
                          if h and not any(h.startswith(p) for p in _LOV_PREFIXES)]
            logger.info(
                "Register %s side %d (%s): %d totale a[href], %d matcher prefiks",
                type_slug, side, url, len(alle_href),
                len(alle_href) - len(ikke_match),
            )
            if ikke_match and side <= 3:
                logger.info("Ikke-matchende hrefs (utvalg): %s", ikke_match[:8])

            lenker = self._trekk_ut_register_lenker(page)
            if not lenker:
                # Fallback 1: next-link i HTML
                neste_el = self.css_first(
                    page,
                    "a[rel='next'], a.neste, a[aria-label='Neste'], "
                    ".pagination a:last-child, [class*='next'] a",
                )
                if neste_el:
                    href = str(neste_el.attrib.get("href", "")).strip()
                    if href and href != url:
                        neste_url = f"https://lovdata.no{href}" if href.startswith("/") else href
                        logger.info("Ingen lenker side %d, fant next-link: %s", side, neste_url)
                        continue

                # Fallback 2: URL-offset – prøv neste side manuelt om vi er på side 1
                # (Lovdata kan ignorere ?start= men verdt å prøve én gang)
                if side == 1 and "?" not in base_url:
                    neste_url = f"{base_url}?start=25"
                    logger.info("Ingen lenker side 1, prøver URL-offset: %s", neste_url)
                    continue

                logger.info("Ingen lovlenker og ingen neste-side på side %d av %s – stopper",
                            side, base_url)
                break

            nye_på_side = 0
            for dok_url, slug, tittel in lenker:
                if dok_url not in sett_url:
                    sett_url.add(dok_url)
                    resultater.append((dok_url, slug, tittel))
                    nye_på_side += 1

            logger.info("Register %s side %d: %d lovlenker (totalt %d)",
                        type_slug, side, nye_på_side, len(resultater))
            self._lagre_state()

            # Finn neste side via next-link; faller tilbake til URL-offset
            neste_el = self.css_first(
                page,
                "a[rel='next'], a.neste, a[aria-label='Neste'], "
                ".pagination a:last-child, [class*='next'] a",
            )
            if neste_el:
                href = str(neste_el.attrib.get("href", "")).strip()
                neste_url = f"https://lovdata.no{href}" if href.startswith("/") else href
            else:
                # Ingen next-link – prøv URL-offset som fallback
                offset = side * 25
                kandidat = f"{base_url}?start={offset}"
                if kandidat != url:
                    neste_url = kandidat
                    logger.info("Ingen next-link etter side %d, prøver offset: %s", side, neste_url)
                else:
                    neste_url = None

        return resultater

    def _trekk_ut_register_lenker(self, page) -> list[tuple[str, str, str]]:
        """Hent alle lenker til lovdokumenter fra en side."""
        lenker = []
        for el in page.css("a[href]"):
            href = str(el.attrib.get("href", "")).strip()
            if not href or not any(href.startswith(p) for p in _LOV_PREFIXES):
                continue

            if href.startswith("/"):
                href = f"https://lovdata.no{href}"

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

        nye = [(k, v) for k, v in kø.items() if not v["hentet"]]
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

            kø[nøkkel]["hentet"] = True
            kø[nøkkel]["sist_hentet"] = self.now_iso()

        self._lagre_state()
        return created

    def _hent_dokument(
        self, output_dir: Path, url: str, slug: str, kjent_tittel: str = ""
    ) -> Path | None:
        filepath = output_dir / f"{slug}.md"

        page, strategi = self._fetch_dokument(url)
        if not page:
            return None

        raa_tittel = self.hent_tittel(page)
        _GENERISKE = {"hoved­meny", "hoved-meny", "hovedmeny", "meny", "menu", "navigation", ""}
        if raa_tittel.lower().strip() in _GENERISKE:
            tittel = kjent_tittel or slug
        else:
            tittel = raa_tittel
        logger.debug("Tittel for %s: %r (strategi: %s)", slug, tittel, strategi)
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
        for sel in _INNHOLD_SELEKTORER:
            el = self.css_first(page, sel)
            if el:
                tekst = self._element_til_markdown_filtrert(el)
                if len(tekst.strip()) >= _MIN_INNHOLD_LENGDE:
                    return tekst

        el = self.css_first(page, _FALLBACK_SELEKTOR)
        if el:
            return self._element_til_markdown_filtrert(el)

        return ""

    def _element_til_markdown_filtrert(self, element) -> str:
        linjer = []
        for tag in element.css("h1, h2, h3, h4, h5, p, li, dt, dd"):
            tekst = str(tag.text or "").strip()
            if not tekst or len(tekst) < 2:
                continue

            if _UI_MØNSTRE.match(tekst):
                continue

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
    # Fetch med fallback-strategier
    # -------------------------------------------------------------------------

    def _fetch_dokument(self, url: str) -> tuple[object | None, str]:
        """
        Henter en Lovdata-dokumentside med progressivt lettere strategier.
        Returnerer (page, strategi_navn) eller (None, "").
        Lovdata krever JS for å rendre lovtekst, så DynamicFetcher er primær.
        """
        # Strategi 1: DynamicFetcher – full Playwright med JS
        page = self._dynamic_fetch(url, fetcher="dynamic")
        if page and self._har_nok_innhold(page):
            return page, "dynamic"

        # Strategi 2: StealthyFetcher – lettere Playwright (raskere, men noen JS-sider feiler)
        logger.info("Fallback til StealthyFetcher for %s", url)
        page = self._dynamic_fetch(url, fetcher="stealth")
        if page and self._har_nok_innhold(page):
            return page, "stealth"

        # Strategi 3: Plain urllib – fungerer kun om siden rendres server-side
        logger.info("Fallback til urllib for %s", url)
        page = self._plain_fetch(url)
        if page and self._har_nok_innhold(page):
            return page, "urllib"

        # Returner det vi har (selv om lite innhold) slik at logger kan rapportere
        return page, "urllib" if page else ""

    def _fetch_register(self, url: str) -> object | None:
        """
        Henter en registerside. Prøver StealthyFetcher først (raskere),
        faller tilbake til DynamicFetcher om siden krever tung JS.
        """
        page = self._dynamic_fetch(url, fetcher="stealth")
        if page:
            return page
        logger.info("Fallback til DynamicFetcher for registerside %s", url)
        return self._dynamic_fetch(url, fetcher="dynamic")

    def _har_nok_innhold(self, page) -> bool:
        """Sjekk at siden har tilstrekkelig tekstinnhold (ikke bare nav/header)."""
        if page is None:
            return False
        el = self.css_first(page, "main, article, body")
        if not el:
            return False
        tekst = str(el.text or "")
        return len(tekst.strip()) >= _MIN_INNHOLD_LENGDE * 2

    def _dynamic_fetch(self, url: str, retries: int = 3, fetcher: str = "dynamic"):
        from scrapling.fetchers import DynamicFetcher, StealthyFetcher

        klass = DynamicFetcher if fetcher == "dynamic" else StealthyFetcher
        for attempt in range(retries):
            self._polite_delay()
            try:
                page = klass.fetch(
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
                logger.warning("%s feil (forsøk %d/%d) %s: %s",
                               klass.__name__, attempt + 1, retries, url, e)
                time.sleep(10 * (attempt + 1))
        return None

    def _plain_fetch(self, url: str):
        """Hent side med ren urllib – rask, men uten JS-rendering."""
        import urllib.request
        from scrapling import Selector
        from config import USER_AGENT

        self._polite_delay()
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "nb-NO,nb;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                self._last_request_time = time.time()
                if resp.status >= 400:
                    logger.warning("urllib HTTP %d: %s", resp.status, url)
                    return None
                html = resp.read().decode("utf-8", errors="replace")
                return Selector(content=html, url=url)
        except Exception as e:
            logger.warning("urllib feil for %s: %s", url, e)
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
