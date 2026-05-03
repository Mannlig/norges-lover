#!/bin/bash
# =============================================================================
# Installasjonsskript for Norges Lover scraper på Raspberry Pi
# Testet på: Raspberry Pi OS (Debian Bookworm), RPi 4/5
# =============================================================================

set -euo pipefail

REPO_DIR="$HOME/norges-lover"
SCRAPER_DIR="$REPO_DIR/rpi-scraper"
SERVICE_NAME="norges-lover"

echo "=============================================="
echo " Norges Lover – RPi installasjon"
echo "=============================================="
echo ""

# --- 1. Systemoppdatering og avhengigheter ---
echo "[1/6] Installerer systempakker..."
sudo apt-get update -qq
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    chromium-browser \
    git \
    curl

# --- 2. Klon repo (hvis ikke allerede klonet) ---
echo "[2/6] Setter opp repo..."
if [ ! -d "$REPO_DIR/.git" ]; then
    echo "  Kloner mannlig/norges-lover..."
    git clone https://github.com/mannlig/norges-lover.git "$REPO_DIR"
else
    echo "  Repo finnes allerede: $REPO_DIR"
fi

cd "$REPO_DIR"
git fetch origin
git checkout claude/raspberry-pi-code-wGVyg 2>/dev/null || git checkout main

# --- 3. Python virtuelt miljø ---
echo "[3/6] Setter opp Python virtuelt miljø..."
python3 -m venv "$SCRAPER_DIR/.venv"
source "$SCRAPER_DIR/.venv/bin/activate"
pip install --upgrade pip -q
pip install -r "$SCRAPER_DIR/requirements.txt" -q
echo "  Python-pakker installert"

# --- 4. Miljøvariabler ---
echo "[4/6] Konfigurerer miljøvariabler..."
ENV_FILE="$HOME/.norges-lover-env"

if [ ! -f "$ENV_FILE" ]; then
    cat > "$ENV_FILE" << 'ENVEOF'
# Norges Lover – miljøvariabler
# VIKTIG: Denne filen inneholder hemmeligheter – del ALDRI innholdet

# GitHub Personal Access Token (repo: write-tilgang)
# Opprett token på: https://github.com/settings/tokens
export GITHUB_TOKEN=""

# Git-brukerinfo for commits
export GIT_USER_NAME="norges-lover-rpi"
export GIT_USER_EMAIL="rpi@norges-lover"
ENVEOF
    chmod 600 "$ENV_FILE"
    echo ""
    echo "  ⚠️  VIKTIG: Rediger $ENV_FILE og legg inn din GITHUB_TOKEN"
    echo "  ⚠️  Generer token på: https://github.com/settings/tokens"
    echo "       Velg: repo → Contents: read/write"
    echo ""
else
    echo "  Env-fil finnes allerede: $ENV_FILE"
fi

# --- 5. Systemd-tjeneste ---
echo "[5/6] Installerer systemd-tjeneste..."

sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null << SERVICEEOF
[Unit]
Description=Norges Lover – automatisk scraping og publisering
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$SCRAPER_DIR
EnvironmentFile=$ENV_FILE
ExecStart=$SCRAPER_DIR/.venv/bin/python main.py --daemon --intervall 6
Restart=on-failure
RestartSec=300
StandardOutput=journal
StandardError=journal
SyslogIdentifier=norges-lover

[Install]
WantedBy=multi-user.target
SERVICEEOF

sudo systemctl daemon-reload
echo "  Tjeneste installert: $SERVICE_NAME"

# --- 6. Ferdig ---
echo "[6/6] Installasjon fullført!"
echo ""
echo "=============================================="
echo " Neste steg:"
echo "=============================================="
echo ""
echo "1. Åpne og fyll ut GITHUB_TOKEN:"
echo "   nano $ENV_FILE"
echo ""
echo "2. Test at scraper fungerer:"
echo "   cd $SCRAPER_DIR"
echo "   source .venv/bin/activate"
echo "   source $ENV_FILE"
echo "   python main.py --kilde stortinget"
echo ""
echo "3. Start tjenesten:"
echo "   sudo systemctl enable $SERVICE_NAME"
echo "   sudo systemctl start $SERVICE_NAME"
echo ""
echo "4. Sjekk logger:"
echo "   journalctl -u $SERVICE_NAME -f"
echo "   tail -f $REPO_DIR/logs/scraper.log"
echo ""
echo "Scraperen kjører hvert 6. time og pusher til GitHub."
echo "Se README for mer info: $REPO_DIR/rpi-scraper/README.md"
