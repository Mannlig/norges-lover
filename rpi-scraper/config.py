"""
Konfigurasjon for norges-lover scraper.
Alle hemmeligheter leses fra miljøvariabler - ALDRI hardkodet her.
"""

import os
from pathlib import Path

# --- Repo og git ---
# I Docker settes REPO_ROOT=/repo via miljøvariabel.
REPO_ROOT = Path(os.environ.get("REPO_ROOT", str(Path(__file__).parent.parent)))
DATA_DIR = REPO_ROOT / "data"
LOGS_DIR = REPO_ROOT / "logs"

# Køtilstand lagres utenfor git-repoet så git-operasjoner aldri sletter den.
# NB: i Docker havner standardverdien i containerens eget filsystem og slettes
# ved `docker compose up --force-recreate`. Det er ufarlig (alt crawles på
# nytt), men første runde etterpå blir lang.
STATE_DIR = Path(os.environ.get("STATE_DIR", str(Path.home() / ".norges-lover-state")))

GITHUB_REPO = "mannlig/norges-lover"
GIT_USER_NAME = os.environ.get("GIT_USER_NAME", "norges-lover-bot")
GIT_USER_EMAIL = os.environ.get("GIT_USER_EMAIL", "bot@norges-lover")

# --- Rate limiting (sekunder) ---
DELAY_MIN = 3.0               # Minimum ventetid mellom requests
DELAY_MAX = 8.0               # Maksimum ventetid (tilfeldig i intervallet)
DELAY_BETWEEN_SOURCES = 15.0  # Pause mellom ulike kilder

# --- Brukeragent - identifiser oss høflig ---
USER_AGENT = (
    "NorgesLoverBot/1.0 (https://github.com/mannlig/norges-lover; "
    "åpent arkiv av norsk regelverk; kontakt via GitHub issues)"
)

# --- Data-undermapper per kilde ---
DATA_PATHS = {
    "stortinget": DATA_DIR / "lover",
    "skatt": DATA_DIR / "skatt",
    "byggteknisk": DATA_DIR / "byggteknisk",
    "nav": DATA_DIR / "nav",
    "arbeidstilsynet": DATA_DIR / "arbeidstilsynet",
    "husbanken": DATA_DIR / "husbanken",
}
