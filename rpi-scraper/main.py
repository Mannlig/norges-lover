"""
Norges Lover – Raspberry Pi scraper
====================================
Henter norsk regelverk, skatteregler, byggtekniske krav og stønader fra
offentlige kilder og publiserer til GitHub.

Kjøring (entrypoint.sh kaller denne én gang per runde):
    python main.py                     # Én full runde
    python main.py --kilde stortinget  # Kun én kilde

Exit-koder:
    0  runden er fullført og publisert
    2  push til GitHub avvist eller feilet – se loggen etter «PUSH»

Miljøvariabler:
    GITHUB_TOKEN   – token med skrivetilgang til repoet (påkrevd)
    GIT_USER_NAME  – valgfri, standard: norges-lover-bot
    GIT_USER_EMAIL – valgfri, standard: bot@norges-lover
"""

import argparse
import logging
import logging.handlers
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from config import DATA_DIR, DATA_PATHS, DELAY_BETWEEN_SOURCES, LOGS_DIR, REPO_ROOT
from formatters.markdown import KATEGORI_INFO, lag_indeks, lag_oversikt
from publishers.github_publisher import GitHubPublisher
from scrapers import (
    ArbeidstilsynetScraper,
    DibkScraper,
    HusbankScraper,
    NavScraper,
    SkatteetatenScraper,
    StortingetScraper,
)

# --- Logging ---
LOGS_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        # Roteres, så loggen ikke vokser til SD-kortet er fullt
        logging.handlers.RotatingFileHandler(
            LOGS_DIR / "scraper.log", maxBytes=5_000_000, backupCount=3, encoding="utf-8"),
    ],
)
logger = logging.getLogger("main")

# --- Oversikt over alle kjøringer ---
# Format: (kilde-nøkkel, scraper-klasse, data-mappe-nøkkel, maks-sider)
KJØRINGER = [
    # Stortinget henter hele sesjoner i ett API-kall; taket gjelder bare
    # hvor mange filer som skrives per runde.
    ("stortinget",      StortingetScraper,      "stortinget",      300),
    ("skatteetaten",    SkatteetatenScraper,    "skatt",           150),
    ("dibk",            DibkScraper,            "byggteknisk",     150),
    ("nav",             NavScraper,             "nav",             150),
    ("arbeidstilsynet", ArbeidstilsynetScraper, "arbeidstilsynet", 150),
    ("husbanken",       HusbankScraper,         "husbanken",       150),
]


def kjor_kilde(kilde_navn: str, scraper_klasse, data_mappe: Path, max_sider: int) -> tuple[list[Path], dict]:
    """Kjør én scraper. Returnerer (endrede filer, statistikk)."""
    logger.info("▶ Starter: %s → %s", kilde_navn, data_mappe)
    start = time.monotonic()
    scraper = None
    try:
        scraper = scraper_klasse()
        filer = scraper.scrape(data_mappe, max_pages=max_sider)
        statistikk = dict(scraper.teller)
        logger.info("✓ Ferdig: %s – %d filer", kilde_navn, len(filer))
    except Exception as e:
        logger.error("✗ KRASJ i %s: %s", kilde_navn, e, exc_info=True)
        filer = []
        statistikk = dict(scraper.teller) if scraper else {}
        statistikk["krasj"] = type(e).__name__
    statistikk["sekunder"] = int(time.monotonic() - start)
    return filer, statistikk


def vurder_helse(s: dict) -> tuple[str, str]:
    """
    (status, grunn) for én kilde. Heartbeaten teller ikke bare endrede filer
    lenger – da så en død kilde ut akkurat som en frisk («0 filer»).
    """
    ok = s.get("hentet_ok", 0)
    feilet = s.get("feil_midlertidig", 0)
    tolket = s.get("ny", 0) + s.get("endret", 0) + s.get("uendret", 0)
    if "krasj" in s:
        return "FEIL", f"krasj: {s['krasj']}"
    if s.get("avbrutt"):
        return "FEIL", "avbrutt etter mange feil på rad – nede eller blokkerer oss?"
    if ok == 0 and feilet > 0:
        return "FEIL", "ingen sider kunne hentes"
    if ok >= 10 and tolket == 0 and s.get("for_lite_innhold", 0) >= ok // 2:
        return "FEIL", "sidene hentes, men innholdet kan ikke tolkes – ny HTML?"
    if feilet and feilet > ok * 0.3:
        return "ADVARSEL", f"{feilet} feil mot {ok} vellykkede"
    return "OK", ""


def skriv_heartbeat(output_dir: Path, statistikk: dict[str, dict], rundetid_s: int) -> Path:
    """Skriv heartbeat med helse per kilde – alltid, uansett endringer."""
    status_dir = output_dir / "status"
    status_dir.mkdir(parents=True, exist_ok=True)
    filepath = status_dir / "heartbeat.md"

    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT,
                             capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        sha = "ukjent"

    helse = {k: vurder_helse(s) for k, s in statistikk.items()}
    linjer = [
        "# Systemstatus – norges-lover-bot",
        "",
        f"**Sist kjørt:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Kode:** `{sha or 'ukjent'}`",
        f"**Rundetid:** {rundetid_s // 3600} t {rundetid_s % 3600 // 60} min",
        "",
        # Maskinlesbar linje – leses av .github/workflows/overvak-pi.yml
        "<!-- helse: " + " ".join(f"{k}={h[0]}" for k, h in helse.items()) + " -->",
        "",
        "| Kilde | Status | Nye | Endret | Uendret | Hentet OK | Feilet | Borte | I kø |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for kilde, s in statistikk.items():
        status, _ = helse[kilde]
        linjer.append(
            f"| {kilde} | {status} | {s.get('ny', 0)} | {s.get('endret', 0)} | "
            f"{s.get('uendret', 0)} | {s.get('hentet_ok', 0)} | {s.get('feil_midlertidig', 0)} | "
            f"{s.get('feil_borte', 0)} | {s.get('i_kø', 0)} |")
    problemer = [(k, h[0], h[1]) for k, h in helse.items() if h[0] != "OK"]
    if problemer:
        linjer += ["", "## Problemer", ""]
        for k, st, grunn in problemer:
            årsaker = sorted(((n, a.removeprefix("årsak:")) for a, n in statistikk[k].items()
                              if a.startswith("årsak:")), reverse=True)
            detalj = ", ".join(f"{a} ×{n}" for n, a in årsaker[:3])
            linjer.append(f"- **{k}** ({st}): {grunn}" + (f" – feiltyper: {detalj}" if detalj else ""))
    linjer += ["", "*«Uendret» betyr at siden ble hentet og sjekket uten at innholdet hadde endret seg.*", ""]
    filepath.write_text("\n".join(linjer), encoding="utf-8")
    return filepath


def oppdater_indekser() -> list[Path]:
    """Lag/oppdater README.md i hver datamappe og oversikten i data/."""
    indeks_filer = []
    for kat, (tittel, beskrivelse) in KATEGORI_INFO.items():
        data_path = DATA_PATHS.get(kat)
        if not data_path or not data_path.exists():
            continue
        try:
            indeks_filer.append(lag_indeks(data_path, tittel, beskrivelse))
        except Exception as e:
            logger.warning("Kunne ikke lage indeks for %s: %s", kat, e)
    try:
        indeks_filer.append(lag_oversikt(DATA_DIR, DATA_PATHS))
    except Exception as e:
        logger.warning("Kunne ikke lage oversikt: %s", e)
    return indeks_filer


def en_kjoring(kun_kilde: str | None = None) -> int:
    """Én full runde: sjekk push → scrape → indekser → publish. Returnerer exit-kode."""
    start = time.monotonic()
    publisher = GitHubPublisher()
    publisher.pull_latest()

    ok, feil = publisher.sjekk_push_tilgang()
    if not ok:
        # Scraping uten push kaster arbeidet (entrypoint nullstiller til
        # origin/main) mens køen tror sidene er hentet. Bedre å vente.
        logger.error("=" * 70)
        logger.error("PUSH-TILGANG AVVIST – scraper ikke denne runden.")
        logger.error("Sannsynlig årsak: GITHUB_TOKEN er utløpt eller trukket tilbake.")
        logger.error("Fiks: nytt token i .env, deretter `docker compose up -d --force-recreate`.")
        logger.error("Svar fra GitHub: %s", feil)
        logger.error("=" * 70)
        return 2

    alle_nye_filer: list[Path] = []
    statistikk: dict[str, dict] = {}

    for kilde_navn, scraper_klasse, data_nøkkel, max_sider in KJØRINGER:
        if kun_kilde and kilde_navn != kun_kilde:
            continue
        filer, statistikk[kilde_navn] = kjor_kilde(
            kilde_navn, scraper_klasse, DATA_PATHS[data_nøkkel], max_sider)
        alle_nye_filer.extend(filer)
        if not kun_kilde:
            logger.info("Venter %.0fs før neste kilde...", DELAY_BETWEEN_SOURCES)
            time.sleep(DELAY_BETWEEN_SOURCES)

    alle_nye_filer.append(skriv_heartbeat(DATA_DIR, statistikk, int(time.monotonic() - start)))
    alle_nye_filer += oppdater_indekser()

    if not publisher.publish(alle_nye_filer):
        logger.error("PUSH FEILET – rundens data ligger bare lokalt og forkastes ved neste runde.")
        return 2

    logger.info("=== Kjøring fullført ===")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Norges Lover – scraper for Raspberry Pi")
    parser.add_argument("--kilde", choices=[k[0] for k in KJØRINGER],
                        help="Kjør kun én spesifikk kilde")
    args = parser.parse_args()
    sys.exit(en_kjoring(kun_kilde=args.kilde))


if __name__ == "__main__":
    main()
