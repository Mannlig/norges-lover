#!/bin/bash
# =============================================================================
# Norges Lover – Docker – ÉN KOMMANDO som fikser alt
#
# Kjør:
#   curl -sSL https://raw.githubusercontent.com/mannlig/norges-lover/main/docker-setup.sh | bash
#
# Eller lokalt:
#   bash docker-setup.sh
# =============================================================================

set -euo pipefail

GROEN="\033[0;32m"; GUL="\033[1;33m"; ROD="\033[0;31m"; RESET="\033[0m"
ok()   { echo -e "${GROEN}  ✓ $*${RESET}"; }
info() { echo -e "  → $*"; }
feil() { echo -e "${ROD}  ✗ $*${RESET}"; exit 1; }

echo ""
echo "================================================"
echo "  Norges Lover – Docker-installasjon"
echo "================================================"
echo ""

# =============================================================================
# 1. Installer Docker hvis ikke tilgjengelig (RPi-støtte)
# =============================================================================
if ! command -v docker &>/dev/null; then
    echo "[1/4] Installerer Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker "$USER"
    ok "Docker installert"
    echo ""
    echo -e "${GUL}  Docker ble installert. Du må logge ut og inn igjen"
    echo -e "  for at gruppemedlemskapet skal tre i kraft.${RESET}"
    echo "  Kjør deretter: bash docker-setup.sh"
    exit 0
else
    ok "Docker er tilgjengelig ($(docker --version | cut -d' ' -f3 | tr -d ','))"
fi

# =============================================================================
# 2. Klon eller oppdater repo
# =============================================================================
REPO_DIR="$HOME/norges-lover"

if [ -d "$REPO_DIR/.git" ]; then
    info "Repo finnes allerede – oppdaterer..."
    git -C "$REPO_DIR" pull --ff-only origin main -q 2>/dev/null || true
    ok "Repo oppdatert: $REPO_DIR"
else
    echo "[2/4] Kloner repo..."
    git clone https://github.com/mannlig/norges-lover.git "$REPO_DIR"
    ok "Repo klonet"
fi
cd "$REPO_DIR"

# =============================================================================
# 3. GitHub-token
# =============================================================================
echo ""
if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo -e "${GUL}Du trenger et GitHub Personal Access Token.${RESET}"
    echo ""
    echo "  Slik oppretter du det:"
    echo "  1. Gå til: https://github.com/settings/tokens"
    echo "  2. 'Generate new token (classic)'"
    echo "  3. Navn: norges-lover-docker"
    echo "  4. Scope: huk av 'repo'"
    echo "  5. Klikk 'Generate token' og kopier"
    echo ""
    # Les fra /dev/tty slik at det fungerer selv ved curl | bash
    read -rsp "  Lim inn token (vises ikke): " GITHUB_TOKEN </dev/tty
    echo ""
    [ -z "$GITHUB_TOKEN" ] && feil "Ingen token oppgitt."
fi

# Skriv .env (gitignorert)
cat > "$REPO_DIR/.env" << ENVEOF
GITHUB_TOKEN=${GITHUB_TOKEN}
GIT_USER_NAME=${GIT_USER_NAME:-norges-lover-bot}
GIT_USER_EMAIL=${GIT_USER_EMAIL:-bot@norges-lover}
ENVEOF
chmod 600 "$REPO_DIR/.env"
ok "Token lagret i .env (kun lesbar av deg)"

# =============================================================================
# 4. Bygg og start container
# =============================================================================
echo ""
echo "[4/4] Bygger og starter Docker-container..."
info "Dette kan ta 3–5 minutter første gang (laster ned Chromium m.m.)"
echo ""

docker compose up -d --build

echo ""
ok "Container kjører!"
echo ""
echo "================================================"
echo "  Alt er i gang!"
echo "================================================"
echo ""
echo "  Scraperen kjører hvert 6. time og pusher til GitHub."
echo ""
echo "  Nyttige kommandoer:"
echo ""
echo "    Følg logger live:    docker compose logs -f"
echo "    Sjekk status:        docker compose ps"
echo "    Stopp:               docker compose down"
echo "    Start igjen:         docker compose up -d"
echo "    Kjør én kilde nå:    docker compose run --rm norges-lover --kilde stortinget"
echo ""
echo "  Data lagres i Docker-volum 'repo-data'."
echo "  Publisert til: https://github.com/mannlig/norges-lover"
echo ""
