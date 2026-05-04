#!/bin/bash
# Entrypoint for Docker-container.
# Kloner/oppdaterer repo og starter scraperen.
set -euo pipefail

REPO_DIR="${REPO_ROOT:-/repo}"

if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo "FEIL: GITHUB_TOKEN er ikke satt. Sett den i .env-filen."
    exit 1
fi

REMOTE="https://${GITHUB_TOKEN}@github.com/mannlig/norges-lover.git"

# --- Klon eller oppdater repo ---
if [ -d "$REPO_DIR/.git" ]; then
    echo "Repo finnes – oppdaterer..."
    git -C "$REPO_DIR" remote set-url origin "$REMOTE"
    git -C "$REPO_DIR" pull --ff-only origin main -q 2>/dev/null || true
else
    echo "Kloner repo..."
    # Docker volume-mount oppretter /repo som eksisterende mappe – git clone feiler da.
    # Bruk git init + fetch + checkout i stedet, som fungerer uansett.
    cd "$REPO_DIR"
    git init -q
    git remote add origin "$REMOTE"
    git fetch origin main -q
    git checkout -b main --track origin/main -q
fi

cd "$REPO_DIR"
git remote set-url origin "$REMOTE"

# Bruk main-branch
git fetch origin -q
git checkout main -q 2>/dev/null || true
git pull --ff-only origin main -q 2>/dev/null || true

echo "Repo klar: $(git rev-parse --abbrev-ref HEAD) @ $(git rev-parse --short HEAD)"

# Kjør koden direkte fra repo – sikrer alltid fersk versjon uten rebuild
cd "$REPO_DIR/rpi-scraper"
echo "Starter scraper: python main.py $*"
exec python main.py "$@"
