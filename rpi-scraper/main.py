"""
Norges Lover – Raspberry Pi scraper
====================================
Henter norsk lovverk, forskrifter, skatteregler, byggtekniske krav
og stønader fra offentlige kilder og publiserer til GitHub.

Kjøring:
    python main.py                     # Én full kjøring
    python main.py --kilde stortinget  # Kun én kilde
    python main.py --daemon            # Kjør kontinuerlig (cron-modus)

Miljøvariabler som MÅ settes:
    GITHUB_TOKEN   – Personal Access Token med repo-write tilgang
    GIT_USER_NAME  – Valgfri, default: norges-lover-bot
    GIT_USER_EMAIL – Valgfri, default: bot@norges-lover
"""

import argparse
import logging
import sys
import time
from pathlib import Path

from config import DATA_PATHS, DELAY_BETWEEN_SOURCES, LOGS_DIR, MAX_PAGES_PER_RUN
from formatters.markdown import lag_indeks, KATEGORI_INFO
from publishers.github_publisher import GitHubPublisher
from scrapers import (
    StortingetScraper,
    LovdataScraper,
    SkatteetatenScraper,
    DibkScraper,
    NavScraper,
    KommunerScraper,
)

# --- Logging ---
LOGS_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOGS_DIR / "scraper.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("main")

# --- Oversikt over alle kjøringer ---
# Format: (kilde-nøkkel, scraper-klasse, data-mappe-nøkkel, maks-sider)
KJØRINGER = [
    ("stortinget", StortingetScraper, "lover", 100),
    ("lovdata", LovdataScraper, "lover", 30),      # Chromium, ta det rolig
    ("skatteetaten", SkatteetatenScraper, "skatt", 50),
    ("dibk", DibkScraper, "byggteknisk", 50),
    ("nav", NavScraper, "nav", 50),
    ("kommuner", KommunerScraper, "kommuner", 30),  # Chromium, ta det rolig
]


def kjor_kilde(kilde_navn: str, scraper_klasse, data_mappe: Path, max_sider: int) -> list[Path]:
    """Kjør én scraper og returner liste over endrede filer."""
    logger.info("▶ Starter: %s → %s", kilde_navn, data_mappe)
    try:
        scraper = scraper_klasse()
        filer = scraper.scrape(data_mappe, max_pages=max_sider)
        logger.info("✓ Ferdig: %s – %d filer", kilde_navn, len(filer))
        return filer
    except Exception as e:
        logger.error("✗ Feil i %s: %s", kilde_navn, e, exc_info=True)
        return []


def oppdater_indekser(alle_filer: list[Path]) -> list[Path]:
    """Lag/oppdater README.md i hver datamappe."""
    indeks_filer = []
    for kat, data_path in DATA_PATHS.items():
        if not data_path.exists():
            continue
        info = KATEGORI_INFO.get(kat, (kat.capitalize(), ""))
        tittel = f"Data – {kat.capitalize()}"
        beskrivelse = info[0] if info else ""
        try:
            readme = lag_indeks(data_path, tittel, beskrivelse)
            indeks_filer.append(readme)
        except Exception as e:
            logger.warning("Kunne ikke lage indeks for %s: %s", kat, e)
    return indeks_filer


def en_kjoring(kun_kilde: str | None = None, publisher: GitHubPublisher | None = None):
    """Én full runde: scrape → indekser → publish."""
    if publisher is None:
        publisher = GitHubPublisher()

    # Hent siste endringer fra GitHub først
    publisher.pull_latest()

    alle_nye_filer: list[Path] = []

    for kilde_navn, scraper_klasse, data_nøkkel, max_sider in KJØRINGER:
        if kun_kilde and kilde_navn != kun_kilde:
            continue

        data_path = DATA_PATHS[data_nøkkel]
        filer = kjor_kilde(kilde_navn, scraper_klasse, data_path, max_sider)
        alle_nye_filer.extend(filer)

        if filer:
            # Publiser etter hver kilde for å unngå å miste data ved feil
            indekser = oppdater_indekser(alle_nye_filer)
            alle_nye_filer.extend(indekser)
            publisher.publish(alle_nye_filer)
            alle_nye_filer = []  # Reset – allerede pushet

        if not kun_kilde:
            logger.info("Venter %.0fs før neste kilde...", DELAY_BETWEEN_SOURCES)
            time.sleep(DELAY_BETWEEN_SOURCES)

    # Siste publisering om noe gjenstår
    if alle_nye_filer:
        indekser = oppdater_indekser(alle_nye_filer)
        publisher.publish(alle_nye_filer + indekser)

    logger.info("=== Kjøring fullført ===")


def daemon_modus(intervall_timer: int = 6):
    """Kjør kontinuerlig med angitt intervall (timer)."""
    publisher = GitHubPublisher()
    logger.info("Daemon-modus: kjører hvert %d time(r)", intervall_timer)

    while True:
        try:
            en_kjoring(publisher=publisher)
        except Exception as e:
            logger.error("Uventet feil i daemon-løkke: %s", e, exc_info=True)

        neste = intervall_timer * 3600
        logger.info("Sover %d timer til neste kjøring...", intervall_timer)
        time.sleep(neste)


def main():
    parser = argparse.ArgumentParser(
        description="Norges Lover – scraper for Raspberry Pi"
    )
    parser.add_argument(
        "--kilde",
        choices=[k[0] for k in KJØRINGER],
        help="Kjør kun én spesifikk kilde",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Kjør kontinuerlig i bakgrunnen",
    )
    parser.add_argument(
        "--intervall",
        type=int,
        default=6,
        help="Timer mellom kjøringer i daemon-modus (default: 6)",
    )
    args = parser.parse_args()

    if args.daemon:
        daemon_modus(args.intervall)
    else:
        en_kjoring(kun_kilde=args.kilde)


if __name__ == "__main__":
    main()
