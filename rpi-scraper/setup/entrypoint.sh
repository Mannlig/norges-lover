#!/bin/bash
# Entrypoint for Docker-container.
#
# /repo behandles som en DEPLOY-mappe, ikke en utviklingsmappe:
# vi tvinger den til å matche origin/main eksakt ved hver oppstart.
# Dette unngår at uncommitted scraper-output (mid-run) eller divergerende
# lokale commits stopper kode-oppdatering. Bot-en pusher data fortløpende
# under run, så reset --hard mister ikke noe som har verdi.
set -euo pipefail

REPO_DIR="${REPO_ROOT:-/repo}"

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

# --- Tving full sync til origin/main ---
echo "Henter origin/main..."
git fetch origin main -q

# Rydd uncommitted endringer (mid-run scraper-output som vil regenereres)
git reset --hard -q
git clean -fd -q

# Hopp til origin/main eksakt – overstyrer divergerende lokale commits
git checkout -B main origin/main -q

echo "Repo klar: $(git rev-parse --abbrev-ref HEAD) @ $(git rev-parse --short HEAD)"

# Kjør koden direkte fra repo – sikrer alltid fersk versjon uten rebuild
cd "$REPO_DIR/rpi-scraper"
echo "Starter scraper: python main.py $*"
exec python main.py "$@"
