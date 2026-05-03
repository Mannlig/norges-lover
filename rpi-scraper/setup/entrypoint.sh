#!/bin/bash
# Entrypoint for Docker-container.
# Kloner/oppdaterer repo og starter scraperen.
set -euo pipefail

REPO_DIR="${REPO_ROOT:-/repo}"
REPO_URL="https://github.com/mannlig/norges-lover.git"

if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo "FEIL: GITHUB_TOKEN er ikke satt. Sett den i .env-filen."
    exit 1
fi

# --- Klon eller oppdater repo ---
if [ ! -d "$REPO_DIR/.git" ]; then
    echo "Kloner repo til $REPO_DIR ..."
    git clone "https://${GITHUB_TOKEN}@github.com/mannlig/norges-lover.git" "$REPO_DIR"
fi

cd "$REPO_DIR"

# Oppdater remote med token (for push)
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/mannlig/norges-lover.git"

# Gå til riktig branch
git fetch origin -q
git checkout claude/raspberry-pi-code-wGVyg -q 2>/dev/null \
    || git checkout main -q 2>/dev/null \
    || true

git pull --ff-only origin "$(git rev-parse --abbrev-ref HEAD)" -q 2>/dev/null || true

echo "Repo klar: $(git rev-parse --abbrev-ref HEAD) @ $(git rev-parse --short HEAD)"
echo "Starter scraper: python /app/main.py $*"

exec python /app/main.py "$@"
