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
    # Docker volume-mount oppretter /repo som tom mappe – git clone krever at den ikke finnes.
    # Tøm innholdet men behold selve mount-punktet.
    find "$REPO_DIR" -mindepth 1 -delete 2>/dev/null || true
    git clone "$REMOTE" "$REPO_DIR"
fi

cd "$REPO_DIR"
git remote set-url origin "$REMOTE"

# Bruk main-branch
git fetch origin -q
git checkout main -q 2>/dev/null || true
git pull --ff-only origin main -q 2>/dev/null || true

echo "Repo klar: $(git rev-parse --abbrev-ref HEAD) @ $(git rev-parse --short HEAD)"
echo "Starter scraper: python /app/main.py $*"

exec python /app/main.py "$@"
