# Norges Lover – Raspberry Pi Scraper

Automatisk innsamling av norsk lovverk, forskrifter og offentlige regler.
Kjører på en Raspberry Pi og publiserer alt til dette GitHub-repoet.

## Hva samles inn

| Kilde | Innhold | Scraper |
|-------|---------|---------|
| [Stortingets API](https://data.stortinget.no) | Lover, proposisjoner, lovsaker | REST API (åpent) |
| [Lovdata](https://lovdata.no) | Lovtekster, nasjonale forskrifter, kommunale forskrifter | nodriver (Chromium) |
| [Skatteetaten](https://www.skatteetaten.no) | Skattesatser, MVA, fradrag, veiledere | requests + BS4 |
| [DiBK](https://www.dibk.no) | TEK17, SAK10, byggeregler, søknadsveiledere | requests + BS4 |
| [NAV](https://www.nav.no) | Dagpenger, sykepenger, stønader, grunnbeløp | requests + BS4 |
| [Lovdata kommuner](https://lovdata.no/register/lokaleforskrifter) | Lokale/kommunale forskrifter | nodriver (Chromium) |

## Mappestruktur i repoet

```
data/
├── lover/          – Nasjonale lover (Stortinget + Lovdata)
├── forskrifter/    – Nasjonale forskrifter
├── skatt/          – Skatteregler og satser
├── byggteknisk/    – TEK17, SAK10, DiBK-veiledere
├── nav/            – Stønader og ytelser
└── kommuner/       – Kommunale forskrifter (kommunenr-navn/)
```

Hvert dokument inneholder:
- Tittel og fullt innhold
- `Kilde:` med URL til originalkilden
- `Hentet:` tidsstempel (ISO 8601)
- Kategori og eventuelt kommunenummer

## Oppsett på Raspberry Pi

### Krav

- Raspberry Pi 4 eller 5 (anbefalt: 4 GB RAM eller mer)
- Raspberry Pi OS (Bookworm/64-bit anbefalt)
- Python 3.11+
- Internettilgang

### Rask installasjon

```bash
# Klon repoet
git clone https://github.com/mannlig/norges-lover.git
cd norges-lover

# Kjør installasjonsskriptet
bash rpi-scraper/setup/install.sh
```

Skriptet installerer alle avhengigheter, setter opp Python-miljø og konfigurerer systemd-tjeneste.

### Manuell installasjon

```bash
# Systempakker
sudo apt update
sudo apt install python3 python3-pip python3-venv chromium-browser git

# Python-avhengigheter
cd rpi-scraper
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Konfigurasjon (ingen hemmeligheter i repoet!)

Lag filen `~/.norges-lover-env` (denne filen skal **aldri** commites):

```bash
export GITHUB_TOKEN="ghp_ditt_token_her"
export GIT_USER_NAME="norges-lover-rpi"
export GIT_USER_EMAIL="rpi@norges-lover"
```

### Generer GitHub Personal Access Token

1. Gå til [github.com/settings/tokens](https://github.com/settings/tokens)
2. Klikk «Generate new token (classic)»
3. Gi den et navn, f.eks. «norges-lover-rpi»
4. Velg scope: **repo** → Contents: read/write
5. Kopier tokenen og lim inn i `~/.norges-lover-env`

> Tokenen lagres kun lokalt på Pi-en. Den commites **aldri** til repoet.

## Kjøring

```bash
cd rpi-scraper
source .venv/bin/activate
source ~/.norges-lover-env

# Test én kilde
python main.py --kilde stortinget
python main.py --kilde skatteetaten
python main.py --kilde nav

# Full kjøring (alle kilder)
python main.py

# Daemon-modus (kjør automatisk hvert 6. time)
python main.py --daemon --intervall 6
```

### Automatisk oppstart med systemd

```bash
sudo systemctl enable norges-lover
sudo systemctl start norges-lover

# Status og logger
sudo systemctl status norges-lover
journalctl -u norges-lover -f
```

## Rate limiting og høflighet

Scraperen er designet for å ikke overbelaste kildene:

- **3–8 sekunder** mellom hvert HTTP-request (tilfeldig)
- **30 sekunder** pause mellom hver kilde
- **Max 50–100 sider** per kilde per kjøring
- Identifiserer seg med en tydelig User-Agent
- Respekterer HTTP 429 (Too Many Requests) med eksponentiell backoff
- Kjøringen spres over flere dager via 6-timers intervaller

> Merk: Lovdata.no bruker bot-beskyttelse. Vi bruker nodriver (headless Chromium)
> som kjører en ekte nettleser. Dette er tregere men mer pålitelig.

## Legge til nye kilder

1. Lag en ny fil i `scrapers/`, f.eks. `scrapers/husbanken.py`
2. Arv fra `BaseScraper` og implementer `scrape(output_dir, max_pages) -> list[Path]`
3. Sett alltid `source_url` og inkluder kilde-URL i hvert dokument
4. Legg til i `scrapers/__init__.py` og i `KJØRINGER`-listen i `main.py`

## Dataformat

Alle dokumenter lagres som Markdown (`.md`) med følgende struktur:

```markdown
# Tittel på loven/regelverket

## Kildeinformasjon

- **Kilde:** Lovdata – https://lovdata.no/lov/...
- **Hentet:** 2025-01-15T08:30:00Z

## Innhold

[Fullt innhold her]

---
*Automatisk hentet av norges-lover-bot.*
```

## Lisens

Kildekode: MIT-lisens (se LICENSE i rotkatalogen).

Innholdet i `data/`-mappen er hentet fra offentlige norske myndigheter og er
underlagt deres respektive lisenser. Alt innhold er offentlig tilgjengelig
og refererer til originalkilden.
