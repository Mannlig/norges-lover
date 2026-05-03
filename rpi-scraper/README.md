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

### Installasjon – én kommando

Kjør dette på Pi-en din:

```bash
curl -sSL https://raw.githubusercontent.com/mannlig/norges-lover/main/rpi-scraper/setup/install.sh | bash
```

Skriptet vil:
1. Spørre om GitHub-token (se under)
2. Installere alle avhengigheter automatisk
3. Klone repoet
4. Sette opp Python-miljø
5. Starte scraperen som en systemd-tjeneste

Etter det kjører den autonomt i bakgrunnen og pusher til GitHub hvert 6. time.

### GitHub Personal Access Token

Skriptet spør om dette under installasjon. Slik oppretter du det:

1. Gå til [github.com/settings/tokens](https://github.com/settings/tokens)
2. Klikk «Generate new token (classic)»
3. Gi den et navn, f.eks. «norges-lover-rpi»
4. Velg scope: **repo** (gir lese- og skrivetilgang)
5. Klikk «Generate token» og kopier verdien

> Token lagres kun lokalt på Pi-en i `~/.norges-lover-env` (chmod 600).
> Den commites **aldri** til repoet.

## Nyttige kommandoer etter installasjon

```bash
# Sjekk at tjenesten kjører
sudo systemctl status norges-lover

# Følg logger live
journalctl -u norges-lover -f

# Kjør én kilde manuelt (for testing)
cd ~/norges-lover/rpi-scraper
source .venv/bin/activate && source ~/.norges-lover-env
python main.py --kilde stortinget

# Stopp / start
sudo systemctl stop norges-lover
sudo systemctl start norges-lover
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
