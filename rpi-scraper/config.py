"""
Konfigurasjon for norges-lover scraper.
Alle hemmeligheter leses fra miljøvariabler - ALDRI hardkodet her.
"""

import os
from pathlib import Path

# --- Repo og git ---
# I Docker settes REPO_ROOT=/repo via miljøvariabel.
# På Pi uten Docker brukes standard relativ sti.
REPO_ROOT = Path(os.environ.get("REPO_ROOT", str(Path(__file__).parent.parent)))
DATA_DIR = REPO_ROOT / "data"
LOGS_DIR = REPO_ROOT / "logs"

GITHUB_REPO = "mannlig/norges-lover"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")  # Sett på Pi: export GITHUB_TOKEN=...
GIT_USER_NAME = os.environ.get("GIT_USER_NAME", "norges-lover-bot")
GIT_USER_EMAIL = os.environ.get("GIT_USER_EMAIL", "bot@norges-lover")

# --- Rate limiting (sekunder mellom requests) ---
DELAY_MIN = 3.0   # Minimum ventetid mellom requests
DELAY_MAX = 8.0   # Maksimum ventetid (tilfeldig i intervallet)
DELAY_BETWEEN_SOURCES = 30.0  # Pause mellom ulike kilder

# --- Scraping-grenser ---
MAX_PAGES_PER_RUN = 50    # Maks sider per kilde per kjøring
REQUEST_TIMEOUT = 30      # Sekunder før timeout

# --- Brukeragent - identifiser oss høflig ---
USER_AGENT = (
    "NorgesLoverBot/1.0 (https://github.com/mannlig/norges-lover; "
    "åpent arkiv av norsk lovverk; kontakt via GitHub issues)"
)

# --- Kilde-URL-er ---
SOURCES = {
    "stortinget_api": "https://data.stortinget.no/eksporter/json",
    "lovdata_base": "https://lovdata.no",
    "skatteetaten_base": "https://www.skatteetaten.no",
    "dibk_base": "https://www.dibk.no",
    "nav_base": "https://www.nav.no",
    "kommuner_base": "https://lovdata.no/register/lokaleforskrifter",
}

# --- Data-undermapper ---
DATA_PATHS = {
    "lover": DATA_DIR / "lover",
    "forskrifter": DATA_DIR / "forskrifter",
    "skatt": DATA_DIR / "skatt",
    "byggteknisk": DATA_DIR / "byggteknisk",
    "nav": DATA_DIR / "nav",
    "kommuner": DATA_DIR / "kommuner",
}

# SSB kommunenummer for alle norske kommuner (utvalg av store)
KOMMUNER = {
    "0301": "oslo",
    "1103": "stavanger",
    "4601": "bergen",
    "5001": "trondheim",
    "3201": "kongsberg",
    "3203": "drammen",
    "3205": "ringerike",
    "1507": "alesund",
    "5401": "tromso",
    "1804": "bodo",
    "1001": "kristiansand",
    "0602": "drammen",
    "3811": "skien",
    "4204": "grimstad",
    "1502": "molde",
}
