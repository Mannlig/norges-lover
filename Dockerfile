# =============================================================================
# Norges Lover – scraper
# Fungerer på: amd64, arm64 (Raspberry Pi 4/5)
# =============================================================================

FROM python:3.11-slim

# System-avhengigheter for Scrapling + Playwright + git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    # Chromium og Playwright-avhengigheter
    chromium \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libgbm1 \
    libasound2 \
    libxrandr2 \
    libxdamage1 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Pek Playwright mot systemets Chromium (ARM-kompatibelt)
ENV PLAYWRIGHT_BROWSERS_PATH=/usr/bin
ENV SCRAPLING_CHROMIUM_PATH=/usr/bin/chromium

WORKDIR /app

# Installer Python-avhengigheter
COPY rpi-scraper/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer Scrapling-nettlesere – bruker system-Chromium på ARM
RUN scrapling install || true

# Kopier scraper-koden
COPY rpi-scraper/ .

# Repo klones i entrypoint til /repo (volum)
ENV REPO_ROOT=/repo
ENV GIT_USER_NAME="norges-lover-bot"
ENV GIT_USER_EMAIL="bot@norges-lover"

COPY rpi-scraper/setup/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["--daemon", "--intervall", "6"]
