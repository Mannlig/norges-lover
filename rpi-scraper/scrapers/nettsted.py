"""
Felles crawler for nettkildene (Skatteetaten, DiBK, NAV, Arbeidstilsynet,
Husbanken).

De fem scraperne var tidligere nesten identiske kopier på ~250 linjer hver,
så rettelser ble gjort i én av dem og glemt i resten. Nå er hver kilde bare
konfigurasjon, og kølogikken finnes ett sted:

- Sider som aldri er hentet går foran gjenbesøk av gamle sider, så nye sider
  ikke sultes ut av ukentlig gjenhenting.
- Gjenbesøksintervall per prefiks: frosne arkiver (Skatte-ABC for tidligere
  år, TEK10) hentes ikke på nytt hver uke.
- Feil merkes ikke som «hentet»: midlertidige feil prøves igjen neste runde
  (opptil tre ganger), og 404 merkes som borte i stedet for å hentes ukentlig.
- Køen ryddes for oppføringer som ikke lenger passerer filteret.
- Lenker normaliseres (relative, med/uten www, «..»-segmenter), og
  omdirigeringer bort fra kilden (innlogging, andre domener) lagres ikke.
- robots.txt respekteres.
"""

import json
import logging
import posixpath
import re
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib import robotparser
from urllib.parse import urljoin, urlsplit

from config import STATE_DIR, USER_AGENT

from .base import BORTE, MIDLERTIDIG, OK, BaseScraper

logger = logging.getLogger(__name__)

HUB_CRAWL_INTERVALL_TIMER = 24
MAKS_FORSØK = 3                # midlertidige feil før en side gis opp til neste gjenbesøk
BORTE_SJEKK_DAGER = 90         # hvor ofte 404-sider sjekkes på nytt
AVBRYT_ETTER_FEIL_PÅ_RAD = 10  # kilden er trolig nede eller blokkerer oss
ANDEL_NYE = 0.75               # andel av kvoten som går til nye sider når begge finnes
LAGRE_HVER = 25                # lagre køen underveis, så et krasj ikke mister alt

# Gjelder alle kilder: språkvarianter, søk, innlogging og feilsider.
FELLES_EKSKLUDER = re.compile(
    r"/(nn|en|se|english|sok|search|sitemap|404|500|login|logg-inn|innlogging)(/|$)",
    re.IGNORECASE,
)
_INNLOGGING = ("Bruk BankID-app eller kodebrikke",)
_FILENDELSER = re.compile(r"\.(pdf|docx?|xlsx?|pptx?|zip|png|jpe?g|gif|svg|csv|xml|json)$", re.I)


class NettstedScraper(BaseScraper):
    # ── Konfigurasjon – overstyres per kilde ─────────────────────────────
    kildenavn: str = ""                 # kort navn i logger og lenketekst
    kilde_beskrivelse: str = ""         # i «Kilde:»-linjen; standard = kildenavn
    base_url: str = ""                  # f.eks. "https://www.skatteetaten.no"
    state_fil: str = ""                 # filnavn i STATE_DIR
    startpunkter: list[str] = []
    inkluder_prefiks: tuple[str, ...] = ()   # tom = hele domenet
    ekskluder: re.Pattern | None = None
    innhold_selektorer: list[str] = ["main", "article", "[role='main']"]
    dato_selektor: str = ""             # CSS for «sist oppdatert» hos kilden
    skråstrek_slutt: bool = True        # skal URL-er slutte på «/»?
    ekstra_metadata: list[str] = []     # ekstra linjer i Kildeinformasjon
    # (nøkkelprefiks, dager) – dager=None betyr «hent aldri på nytt»
    gjenbesøk: list[tuple[str, int | None]] = []
    standard_gjenbesøk_dager: int = 7

    def __init__(self):
        super().__init__()
        self._state: dict = {}
        self._state_path: Path | None = None
        self._robots: robotparser.RobotFileParser | bool | None = None
        self._netloc = urlsplit(self.base_url).netloc
        self._domene = self._netloc.removeprefix("www.")

    # ── Hovedflyt ────────────────────────────────────────────────────────

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        self._state_path = STATE_DIR / self.state_fil
        self._state = self._les_state()
        self._rydd_ko()

        if self._bor_crawle_huber():
            self._crawl_huber()

        created = self._hent_fra_ko(output_dir, max_pages)
        kø = self._state.get("kø", {})
        self.teller["i_kø"] = sum(1 for v in kø.values() if not v.get("hentet"))
        self.teller["aldri_hentet"] = sum(1 for v in kø.values() if not v.get("sist_hentet"))
        logger.info("%s: %d filer | %d gjenstår i kø (%d aldri hentet)",
                    self.kildenavn, len(created), self.teller["i_kø"], self.teller["aldri_hentet"])
        return created

    def hub_urler(self) -> list[str]:
        """Startpunktene for hub-crawl. Overstyres hvis listen må beregnes."""
        return list(self.startpunkter)

    # ── URL-håndtering ───────────────────────────────────────────────────

    def normaliser(self, href: str, side_url: str = "") -> str | None:
        """Gjør en lenke absolutt og kanonisk, eller None hvis den ikke er vår."""
        href = (href or "").strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            return None
        deler = urlsplit(urljoin(side_url or self.base_url + "/", href))
        if deler.scheme not in ("http", "https"):
            return None
        if deler.netloc.lower().removeprefix("www.") != self._domene:
            return None
        sti = deler.path or "/"
        if "/." in sti:
            sti = posixpath.normpath(sti)
            if ".." in sti.split("/"):
                return None
        sti = "/" + sti.strip("/")
        if sti == "/":
            return None
        if self.skråstrek_slutt:
            sti += "/"
        return f"https://{self._netloc}{sti}"

    def er_relevant(self, url: str) -> bool:
        if not url or not url.startswith(f"https://{self._netloc}/"):
            return False
        if self.inkluder_prefiks and not url.startswith(self.inkluder_prefiks):
            return False
        if FELLES_EKSKLUDER.search(url):
            return False
        if self.ekskluder is not None and self.ekskluder.search(url):
            return False
        if _FILENDELSER.search(url.rstrip("/")):
            return False
        return True

    def nøkkel(self, url: str) -> str:
        return urlsplit(url).path.strip("/")

    def _lenker(self, page) -> list[str]:
        side_url = str(getattr(page, "url", "") or "")
        lenker = set()
        for el in page.css("a[href]"):
            url = self.normaliser(str(el.attrib.get("href", "")), side_url)
            if url and self.er_relevant(url):
                lenker.add(url)
        return sorted(lenker)

    def _robots_tillater(self, url: str) -> bool:
        if self._robots is None:
            self._robots = self._les_robots()
        if self._robots is False:
            return True
        return self._robots.can_fetch("NorgesLoverBot", url)

    def _les_robots(self):
        try:
            req = urllib.request.Request(f"{self.base_url}/robots.txt",
                                         headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=20) as resp:
                tekst = resp.read().decode("utf-8", "replace")
            rp = robotparser.RobotFileParser()
            rp.parse(tekst.splitlines())
            return rp
        except Exception as e:
            # Utilgjengelig robots.txt (ofte bot-vern mot urllib) = ingen regler
            logger.info("%s: robots.txt ikke tilgjengelig (%s) – ingen begrensninger", self.kildenavn, e)
            return False

    # ── Kø ───────────────────────────────────────────────────────────────

    def _rydd_ko(self) -> int:
        """
        Fjern køoppføringer som ikke lenger passerer filteret. Filteret brukes
        ellers bare når lenker oppdages, så en utvidelse av ekskluderingen ville
        latt gamle oppføringer bli liggende og hentes på nytt for alltid.
        """
        kø = self._state.setdefault("kø", {})
        fjern = [k for k, v in kø.items() if not self.er_relevant(v.get("url", ""))]
        for k in fjern:
            del kø[k]
        if fjern:
            logger.info("%s: ryddet %d irrelevante URL-er fra køen", self.kildenavn, len(fjern))
            self.teller["ryddet"] = len(fjern)
            self._lagre_state()
        return len(fjern)

    def gjenbesøk_dager(self, nøkkel: str) -> int | None:
        for prefiks, dager in self.gjenbesøk:
            p = prefiks.strip("/")
            if nøkkel == p or nøkkel.startswith(p + "/"):
                return dager
        return self.standard_gjenbesøk_dager

    def _bor_crawle_huber(self) -> bool:
        sist = self._state.get("sist_hub_crawl", "")
        if not sist:
            return True
        try:
            sist_tid = datetime.fromisoformat(sist.replace("Z", "+00:00"))
            return datetime.now(timezone.utc) - sist_tid >= timedelta(hours=HUB_CRAWL_INTERVALL_TIMER)
        except Exception:
            return True

    def _crawl_huber(self):
        logger.info("Starter %s hub-crawl...", self.kildenavn)
        kø = self._state.setdefault("kø", {})
        nå = datetime.now(timezone.utc)

        # Slipp sider hvis gjenbesøksintervall har gått ut tilbake i køen
        for nøkkel, meta in kø.items():
            if not meta.get("hentet") or not meta.get("sist_hentet"):
                continue
            dager = BORTE_SJEKK_DAGER if meta.get("borte") else self.gjenbesøk_dager(nøkkel)
            if dager is None:
                continue
            try:
                sist = datetime.fromisoformat(meta["sist_hentet"].replace("Z", "+00:00"))
            except Exception:
                sist = None
            if sist is None or nå - sist >= timedelta(days=dager):
                meta["hentet"] = False
                meta["feil"] = 0

        nye = 0
        for hub_url in self.hub_urler():
            hub_url = self.normaliser(hub_url) or hub_url
            if not self._robots_tillater(hub_url):
                continue
            page = self.fetch(hub_url)
            if page is None:
                if self.siste_status == BORTE:
                    logger.info("Hub finnes ikke: %s", hub_url)
                continue
            lenker = self._lenker(page)
            logger.info("Hub %s: %d relevante lenker", hub_url, len(lenker))
            for url in lenker + [hub_url]:
                k = self.nøkkel(url)
                if k and k not in kø and self.er_relevant(url):
                    kø[k] = {"url": url, "hentet": False}
                    nye += 1

        self._state["sist_hub_crawl"] = self.now_iso()
        self._lagre_state()
        logger.info("Hub-crawl ferdig: %d nye URL-er i kø (totalt %d)", nye, len(kø))

    def _velg_fra_ko(self, max_pages: int) -> list[tuple[str, dict]]:
        """Aldri hentede sider først, deretter de som er sjekket for lengst siden."""
        kø = self._state.get("kø", {})
        venter = [(k, v) for k, v in kø.items() if not v.get("hentet")]
        nye = [kv for kv in venter if not kv[1].get("sist_hentet")]
        gamle = sorted((kv for kv in venter if kv[1].get("sist_hentet")),
                       key=lambda kv: kv[1]["sist_hentet"])
        antall_nye = min(len(nye), max(int(max_pages * ANDEL_NYE), max_pages - len(gamle)))
        return nye[:antall_nye] + gamle[:max_pages - antall_nye]

    def _hent_fra_ko(self, output_dir: Path, max_pages: int) -> list[Path]:
        kø = self._state.get("kø", {})
        valgt = self._velg_fra_ko(max_pages)
        if not valgt:
            logger.info("%s: alle sider à jour", self.kildenavn)
            return []
        logger.info("%s: henter %d sider", self.kildenavn, len(valgt))

        created = []
        feil_på_rad = 0
        for i, (nøkkel, meta) in enumerate(valgt, 1):
            if not self._robots_tillater(meta["url"]):
                self.teller["robots_blokkert"] += 1
                meta.update(hentet=True, sist_hentet=self.now_iso(), borte=True)
                continue

            path = self._hent_side(output_dir, nøkkel, meta["url"])
            if path:
                created.append(path)

            if self.siste_status == MIDLERTIDIG:
                feil_på_rad += 1
                meta["feil"] = meta.get("feil", 0) + 1
                if meta["feil"] >= MAKS_FORSØK:
                    meta.update(hentet=True, sist_hentet=self.now_iso())
            else:
                feil_på_rad = 0
                meta.update(hentet=True, sist_hentet=self.now_iso(), feil=0,
                            borte=self.siste_status == BORTE)

            if i % LAGRE_HVER == 0:
                self._lagre_state()
            if feil_på_rad >= AVBRYT_ETTER_FEIL_PÅ_RAD:
                logger.error("%s: %d feil på rad – avbryter kilden denne runden",
                             self.kildenavn, feil_på_rad)
                self.teller["avbrutt"] = 1
                break

        self._lagre_state()
        return created

    # ── Én side ──────────────────────────────────────────────────────────

    def _hent_side(self, output_dir: Path, nøkkel: str, url: str) -> Path | None:
        page = self.fetch(url)
        if page is None:
            return None

        # Omdirigert? Til innlogging/annet domene = ikke innhold. Til en annen
        # side hos kilden = hent den under sin egen adresse, ikke som kopi.
        endelig = self.normaliser(str(getattr(page, "url", "") or url), url)
        if endelig != self.normaliser(url):
            if not endelig or not self.er_relevant(endelig):
                self.teller["omdirigert_bort"] += 1
                self.siste_status = BORTE
                return None
            kø = self._state.setdefault("kø", {})
            k = self.nøkkel(endelig)
            if k not in kø:
                kø[k] = {"url": endelig, "hentet": False}
            self.teller["omdirigert"] += 1
            self.siste_status = BORTE
            return None

        kø = self._state.setdefault("kø", {})
        for lenke in self._lenker(page):
            k = self.nøkkel(lenke)
            if k and k not in kø:
                kø[k] = {"url": lenke, "hentet": False}

        raa_innhold = self.side_til_markdown(page, self.innhold_selektorer)
        if any(tegn in raa_innhold for tegn in _INNLOGGING):
            # Innloggingsskjerm (ID-porten) som ikke ble fanget av omdirigeringssjekken
            self.teller["omdirigert_bort"] += 1
            self.siste_status = BORTE
            return None
        if len(raa_innhold.strip()) < 100:
            logger.warning("For lite innhold (%d tegn) for %s", len(raa_innhold.strip()), url)
            self.teller["for_lite_innhold"] += 1
            return None

        deler = [d for d in nøkkel.split("/") if d and d not in (".", "..")]
        if not deler:
            deler = ["index"]
        filepath = output_dir.joinpath(*deler[:-1], f"{deler[-1]}.md")
        if output_dir.resolve() not in filepath.resolve().parents:
            logger.warning("Ugyldig filsti for %s – hopper over", url)
            return None
        filepath.parent.mkdir(parents=True, exist_ok=True)

        tittel = self.hent_tittel(page) or deler[-1].replace("-", " ").capitalize()
        oppdatert = ""
        if self.dato_selektor:
            dato_el = self.css_first(page, self.dato_selektor)
            if dato_el is not None:
                oppdatert = (dato_el.attrib.get("datetime", "") or str(dato_el.text or "")).strip()

        formatert = self._formater(tittel, raa_innhold, url, oppdatert)
        return filepath if self.skriv_hvis_endret(filepath, raa_innhold, formatert) else None

    def _formater(self, tittel: str, innhold: str, url: str, oppdatert: str) -> str:
        linjer = [
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** {self.kilde_beskrivelse or self.kildenavn} – {url}",
            *self.ekstra_metadata,
        ]
        if self.dato_selektor:
            linjer.append(f"- **Sist oppdatert (kilde):** {oppdatert or 'ukjent'}")
        linjer += [
            f"- **Sist oppdatert i arkivet:** {self.now_iso()}",
            "",
            "## Innhold",
            "",
            innhold,
            "",
            "---",
            f"*Automatisk hentet fra [{self.kildenavn}]({url}) av norges-lover-bot.*",
        ]
        return "\n".join(linjer)

    # ── Tilstand ─────────────────────────────────────────────────────────

    def _les_state(self) -> dict:
        if self._state_path and self._state_path.exists():
            try:
                return json.loads(self._state_path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.warning("%s: kunne ikke lese tilstand (%s) – starter på nytt", self.kildenavn, e)
        return {"sist_hub_crawl": "", "kø": {}}

    def _lagre_state(self):
        if not self._state_path:
            return
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self._state, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self._state_path)
