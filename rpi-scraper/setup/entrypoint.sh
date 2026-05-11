#!/bin/bash
# Entrypoint for Docker-container.
#
# Kjører en evig løkke som:
#   1. Henter siste kode fra origin/main
#   2. Kjører én full scraping-runde
#   3. Sover INTERVALL_TIMER timer
#   4. Gjentar
#
# På denne måten plukkes nye kode-endringer opp automatisk
# uten at noen trenger å røre Pi-en.
set -euo pipefail

REPO_DIR="${REPO_ROOT:-/repo}"
INTERVALL_TIMER="${SCRAPER_INTERVALL:-6}"
INTERVALL_SEK=$(( INTERVALL_TIMER * 3600 ))

if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo "FEIL: GITHUB_TOKEN er ikke satt. Sett den i .env-filen."
    exit 1
fi

REMOTE="https://${GITHUB_TOKEN}@github.com/mannlig/norges-lover.git"

# --- Init repo om det ikke finnes ---
if [ ! -d "$REPO_DIR/.git" ]; then
    echo "Initierer repo i $REPO_DIR..."
    cd "$REPO_DIR"
    git init -q
    git remote add origin "$REMOTE"
fi

cd "$REPO_DIR"
git remote set-url origin "$REMOTE"

echo "Starter scraper-løkke (intervall: ${INTERVALL_TIMER}t)"

while true; do
    echo ""
    echo "=== $(date -u '+%Y-%m-%d %H:%M UTC') – henter ny kode fra origin/main ==="

    # Tving full sync til origin/main – plukker opp alle kode-endringer
    git fetch origin main -q
    git reset --hard -q
    git clean -fd -q
    git checkout -B main origin/main -q

    echo "Kode: $(git rev-parse --short HEAD) – $(git log -1 --format='%s')"

    # Kjør én full scraping-runde
    cd "$REPO_DIR/rpi-scraper"
    python main.py || echo "ADVARSEL: scraper returnerte feil, fortsetter løkken"

    echo "Sover ${INTERVALL_TIMER} timer til neste kjøring..."
    sleep "$INTERVALL_SEK"

    cd "$REPO_DIR"
done
