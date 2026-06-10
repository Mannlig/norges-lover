# Norges Lover – Raspberry Pi Scraper

Automatisk innsamling av norsk lovverk, forskrifter og offentlige regler.
Kjører på en Raspberry Pi i Docker og publiserer alt til dette GitHub-repoet.

## Hva samles inn

| Kilde | Innhold | Metode |
|-------|---------|--------|
| [Stortingets API](https://data.stortinget.no) | Lover, proposisjoner, lovsaker | REST API (åpent) |
| [Skatteetaten](https://www.skatteetaten.no) | Skattesatser, MVA, fradrag, veiledere | Headless browser |
| [DiBK](https://www.dibk.no) | TEK17, SAK10, byggeregler | Headless browser |
| [NAV](https://www.nav.no) | Dagpenger, sykepenger, stønader, grunnbeløp | Headless browser |
| [Arbeidstilsynet](https://www.arbeidstilsynet.no) | HMS, arbeidsmiljø, veiledere | Headless browser |
| [Husbanken](https://www.husbanken.no) | Bostøtte, startlån, tilskudd | Headless browser |
| [Lovdata kommuner](https://lovdata.no/register/lokaleforskrifter) | Kommunale forskrifter | Headless browser |

## Arkitektur

```
entrypoint.sh (Docker)
    └── git reset --hard origin/main   ← henter alltid siste kode
    └── python main.py                 ← kjør én full runde
    └── sleep $SCRAPER_INTERVALL       ← vent (default: 2 timer)
    └── (gjenta)

main.py
    └── GitHubPublisher.pull_latest()
    └── for hver kilde:
    │       scraper.scrape(output_dir, max_pages=150)
    └── skriv_heartbeat()              ← alltid, uansett endringer
    └── GitHubPublisher.publish()      ← commit + push
```

State (hvilke URL-er som er hentet) lagres i `~/.norges-lover-state/` utenfor git-repoet.

## Oppsett på Raspberry Pi

### Krav

- Raspberry Pi 4 eller 5 (4 GB RAM anbefalt)
- Docker og Docker Compose installert
- GitHub Personal Access Token med `repo`-tilgang

### 1. Klon repoet

```bash
git clone https://github.com/mannlig/norges-lover.git
cd norges-lover
```

### 2. Lag `.env`-fil

```bash
cat > .env << EOF
GITHUB_TOKEN=ghp_ditt_token_her
GIT_USER_NAME=norges-lover-bot
GIT_USER_EMAIL=bot@norges-lover
SCRAPER_INTERVALL=2
EOF
chmod 600 .env
```

### 3. Bygg og start

```bash
docker compose build
docker compose up -d
```

### GitHub Personal Access Token

1. Gå til [github.com/settings/tokens](https://github.com/settings/tokens)
2. «Generate new token (classic)»
3. Scope: **repo**
4. Kopier tokenet inn i `.env`

> Token lagres kun lokalt i `.env` og commites **aldri** til repoet.

## Nyttige kommandoer

```bash
# Sjekk status
docker compose ps

# Følg logger live
docker compose logs -f

# Kjør én kilde manuelt (for testing)
docker compose exec norges-lover python main.py --kilde stortinget

# Restart
docker compose restart

# Stopp
docker compose down
```

## Rate limiting og høflighet

- **3–8 sekunder** mellom hvert HTTP-request (tilfeldig)
- **15 sekunder** pause mellom hver kilde
- **Maks 150 sider** per kilde per kjøring
- Tydelig User-Agent med kontaktinfo
- Respekterer HTTP 429 med eksponentiell backoff

## Overvåking

- `data/status/heartbeat.md` oppdateres hver kjøring med tidsstempel og antall filer hentet
- GitHub Actions (`overvak-pi.yml`) sjekker heartbeat daglig kl. 08:00 UTC og åpner issue hvis Pi er stille i mer enn 12 timer
- GitHub Actions (`valider-kode.yml`) sjekker Python- og YAML-syntaks ved hver push til main

## Legge til nye kilder

1. Lag `scrapers/ny_kilde.py` med en klasse som arver `BaseScraper` og implementerer `scrape(output_dir, max_pages) -> list[Path]`
2. Legg til i `scrapers/__init__.py`
3. Legg til i `KJØRINGER`-listen i `main.py`
4. Legg til `DATA_PATHS`-oppføring i `config.py`

## Lisens

Kildekode: MIT-lisens (se `LICENSE` i rotkatalogen).

Innholdet i `data/` er hentet fra offentlige norske myndigheter og er underlagt deres respektive lisenser. Alt innhold er offentlig tilgjengelig og refererer til originalkilden.
