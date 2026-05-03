#!/bin/bash
# =============================================================================
# Norges Lover – Raspberry Pi – ETT STEG-installasjon
#
# Kjør:
#   curl -sSL https://raw.githubusercontent.com/mannlig/norges-lover/main/rpi-scraper/setup/install.sh | bash
#
# Eller hvis du allerede har klonet repoet:
#   bash rpi-scraper/setup/install.sh
#
# Skriptet vil spørre om GitHub-token interaktivt,
# installere alt og starte tjenesten automatisk.
# =============================================================================

set -euo pipefail

REPO_URL="https://github.com/mannlig/norges-lover.git"
REPO_DIR="$HOME/norges-lover"
SCRAPER_DIR="$REPO_DIR/rpi-scraper"
SERVICE_NAME="norges-lover"
ENV_FILE="$HOME/.norges-lover-env"

# --- Farger ---
GROEN="\033[0;32m"
GUL="\033[1;33m"
ROD="\033[0;31m"
RESET="\033[0m"

ok()   { echo -e "${GROEN}  ✓ $*${RESET}"; }
info() { echo -e "  → $*"; }
adv()  { echo -e "${GUL}  ⚠ $*${RESET}"; }
feil() { echo -e "${ROD}  ✗ $*${RESET}"; exit 1; }

echo ""
echo "=============================================="
echo "  Norges Lover – automatisk installasjon"
echo "=============================================="
echo ""

# =============================================================================
# 0. Spør om GitHub-token FØRST (slik at resten kan kjøre uovervåket)
# =============================================================================

# Token kan også settes på forhånd: GITHUB_TOKEN=ghp_xxx bash install.sh
if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo -e "${GUL}Du trenger et GitHub Personal Access Token for at Pi-en kan pushe data.${RESET}"
    echo ""
    echo "  Slik oppretter du det:"
    echo "  1. Gå til: https://github.com/settings/tokens"
    echo "  2. Klikk 'Generate new token (classic)'"
    echo "  3. Navn: norges-lover-rpi"
    echo "  4. Scope: huk av 'repo' (gir lese- og skrivetilgang)"
    echo "  5. Klikk 'Generate token' og kopier verdien"
    echo ""
    read -rsp "  Lim inn token her (vises ikke): " GITHUB_TOKEN
    echo ""
    if [ -z "$GITHUB_TOKEN" ]; then
        feil "Ingen token oppgitt. Avbryter."
    fi
fi
ok "Token mottatt"

# Valgfri: git-brukerinfo
GIT_USER_NAME="${GIT_USER_NAME:-norges-lover-rpi}"
GIT_USER_EMAIL="${GIT_USER_EMAIL:-rpi@norges-lover}"

# =============================================================================
# 1. Systempakker
# =============================================================================
echo ""
echo "[1/5] Installerer systempakker..."
sudo apt-get update -qq
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    chromium-browser \
    git \
    curl \
    --no-install-recommends -qq
ok "Systempakker installert"

# =============================================================================
# 2. Klon / oppdater repo
# =============================================================================
echo ""
echo "[2/5] Setter opp repo..."
if [ ! -d "$REPO_DIR/.git" ]; then
    info "Kloner $REPO_URL ..."
    git clone "$REPO_URL" "$REPO_DIR" -q
    ok "Repo klonet til $REPO_DIR"
else
    info "Repo finnes allerede, henter siste endringer..."
    git -C "$REPO_DIR" fetch origin -q
    ok "Repo oppdatert"
fi

cd "$REPO_DIR"
# Prøv feature-branch, fall tilbake til main
git checkout claude/raspberry-pi-code-wGVyg -q 2>/dev/null \
    || git checkout main -q 2>/dev/null \
    || true

# =============================================================================
# 3. Python virtuelt miljø og avhengigheter
# =============================================================================
echo ""
echo "[3/5] Setter opp Python-miljø..."
python3 -m venv "$SCRAPER_DIR/.venv" -q
# shellcheck source=/dev/null
source "$SCRAPER_DIR/.venv/bin/activate"
pip install --upgrade pip -q
pip install -r "$SCRAPER_DIR/requirements.txt" -q
ok "Python-avhengigheter installert"

# =============================================================================
# 4. Skriv miljøfil (med token – kun lesbar av denne brukeren)
# =============================================================================
echo ""
echo "[4/5] Lagrer konfigurasjon..."
cat > "$ENV_FILE" << ENVEOF
# Norges Lover – miljøvariabler
# Generert automatisk av install.sh
# VIKTIG: Ikke del denne filen – den inneholder GitHub-token

export GITHUB_TOKEN="${GITHUB_TOKEN}"
export GIT_USER_NAME="${GIT_USER_NAME}"
export GIT_USER_EMAIL="${GIT_USER_EMAIL}"
ENVEOF
chmod 600 "$ENV_FILE"
ok "Konfigurasjon lagret i $ENV_FILE (kun lesbar av deg)"

# =============================================================================
# 5. Systemd-tjeneste – installer, enable og start
# =============================================================================
echo ""
echo "[5/5] Installerer og starter systemd-tjeneste..."

sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null << SERVICEEOF
[Unit]
Description=Norges Lover – automatisk scraping og publisering til GitHub
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${USER}
WorkingDirectory=${SCRAPER_DIR}
EnvironmentFile=${ENV_FILE}
ExecStart=${SCRAPER_DIR}/.venv/bin/python main.py --daemon --intervall 6
Restart=on-failure
RestartSec=300
StandardOutput=journal
StandardError=journal
SyslogIdentifier=norges-lover

[Install]
WantedBy=multi-user.target
SERVICEEOF

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME" -q
sudo systemctl restart "$SERVICE_NAME"
ok "Tjeneste startet: $SERVICE_NAME"

# =============================================================================
# Ferdig
# =============================================================================
echo ""
echo -e "${GROEN}=============================================="
echo -e "  Installasjon fullført!"
echo -e "==============================================${RESET}"
echo ""
echo "  Scraperen kjører nå i bakgrunnen og publiserer"
echo "  automatisk til GitHub hvert 6. time."
echo ""
echo "  Nyttige kommandoer:"
echo ""
echo "    Sjekk status:   sudo systemctl status $SERVICE_NAME"
echo "    Følg logger:    journalctl -u $SERVICE_NAME -f"
echo "    Stopp:          sudo systemctl stop $SERVICE_NAME"
echo "    Kjør én gang:   cd $SCRAPER_DIR && source .venv/bin/activate && source $ENV_FILE && python main.py"
echo ""
echo "  Data lagres i:  $REPO_DIR/data/"
echo "  Loggfil:        $REPO_DIR/logs/scraper.log"
echo ""
