# Norges Lover – Raspberry Pi Scraper

Automatisk innsamling av norske regler og veiledere fra offentlige kilder.
Kjører på en Raspberry Pi i Docker og publiserer alt til dette GitHub-repoet.

## Hva samles inn

| Kilde | Innhold | Metode |
|-------|---------|--------|
| [Stortingets API](https://data.stortinget.no) | Saker per sesjon (metadata, ikke lovtekst) | REST API (åpent) |
| [Skatteetaten](https://www.skatteetaten.no) | Satser, MVA, fradrag, veiledere, Skatte-ABC | Headless browser |
| [DiBK](https://www.dibk.no) | TEK17, SAK10, byggeregler | Headless browser |
| [NAV](https://www.nav.no) | Dagpenger, sykepenger, stønader, grunnbeløp | Headless browser |
| [Arbeidstilsynet](https://www.arbeidstilsynet.no) | HMS, arbeidsmiljø, veiledere | Headless browser |
| [Husbanken](https://www.husbanken.no) | Bostøtte, startlån, tilskudd | Headless browser |

## Arkitektur

```
entrypoint.sh (Docker, bakt inn i imaget)
    └── git reset --hard origin/main   ← henter alltid siste kode
    └── python main.py                 ← én full runde (exit 2 = push feilet)
    └── sleep $SCRAPER_INTERVALL       ← vent (default: 2 timer)
    └── (gjenta)

main.py
    └── GitHubPublisher.pull_latest()
    └── GitHubPublisher.sjekk_push_tilgang()   ← avbryter runden hvis tokenet avvises
    └── for hver kilde: scraper.scrape(...)    ← feil i én kilde stopper ikke de andre
    └── skriv_heartbeat()                      ← alltid, med helse per kilde
    └── GitHubPublisher.publish()              ← commit + push
```

| Fil | Ansvar |
|---|---|
| `scrapers/nettsted.py` | Felles crawler for nettkildene: hub-crawl, kø, gjenbesøk, robots.txt, omdirigeringer |
| `scrapers/<kilde>.py` | Bare konfigurasjon: startpunkter, prefikser, ekskluderinger |
| `scrapers/stortinget.py` | Stortingets API, én forespørsel per sesjon |
| `scrapers/base.py` | Henting (StealthyFetcher), endringsdeteksjon med innholds-hash |
| `formatters/html.py` | HTML → Markdown (lenker, tabeller, lister) |
| `publishers/github_publisher.py` | Git: commit, push, token via credential helper |

Køtilstand (hvilke URL-er som er hentet, og når) lagres i `STATE_DIR`
(standard `~/.norges-lover-state/`) utenfor git-repoet. Innholds-hashen ligger
i selve markdown-filene, så tapt tilstand gir aldri duplikater eller korrupte
data – bare en lengre første runde.

### Køen

- Sider som aldri er hentet går først (inntil 75 % av kvoten), deretter de som er sjekket for lengst siden.
- Gjenbesøk: satser hver 2. dag, standard 7 dager, avsluttede Skatte-ABC-utgaver og TEK10 aldri.
- Midlertidige feil (nett, 429, 5xx) prøves igjen neste runde, inntil tre ganger. 404 merkes som borte og sjekkes hver 90. dag.
- Ti feil på rad avbryter kilden for denne runden (nettstedet er nede eller blokkerer).

## Oppsett på Raspberry Pi

### Krav

- Raspberry Pi 4 eller 5 (4 GB RAM anbefalt)
- Docker og Docker Compose installert
- GitHub-token med skrivetilgang til repoet

### Installasjon

Enklest: `curl -sSL https://raw.githubusercontent.com/mannlig/norges-lover/main/docker-setup.sh | bash`

Eller for hånd:

```bash
git clone https://github.com/mannlig/norges-lover.git
cd norges-lover
cat > .env << EOF
GITHUB_TOKEN=github_pat_ditt_token_her
SCRAPER_INTERVALL=2
EOF
chmod 600 .env
docker compose build
docker compose up -d
```

### GitHub-token

Anbefalt: et **fine-grained token** som bare gjelder dette repoet.

1. [github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new)
2. Repository access → *Only select repositories* → `norges-lover`
3. Repository permissions → **Contents: Read and write** (ingenting annet)
4. Sett utløpsdato, og skriv den inn i `TOKEN_UTLOP` i `.github/workflows/varsle-token-utlop.yml`
5. Lim tokenet inn i `.env`, og kjør `docker compose up -d --force-recreate`

Test at tokenet virker uten å vente på en hel runde:

```bash
docker compose exec norges-lover git push --dry-run origin HEAD:refs/heads/main 2>&1 | sed -E 's/(ghp_|github_pat_)[A-Za-z0-9_]+/\1***/g'
```

> Tokenet lagres kun lokalt i `.env` og commites **aldri** til repoet.

## Nyttige kommandoer

```bash
docker compose ps                                        # status
docker compose logs -f                                   # følg loggen
docker compose logs --tail=300 | grep -E 'PUSH|KRASJ'    # finn problemer
docker compose exec norges-lover python main.py --kilde stortinget   # én kilde
docker compose restart
```

## Høflighet

- 3–8 sekunder mellom hver forespørsel, 15 sekunder mellom kilder
- Maks 150 sider per kilde per runde
- Respekterer `robots.txt`
- Venter og prøver igjen senere ved HTTP 429 og 5xx

## Overvåking

- `data/status/heartbeat.md` skrives hver runde med helse per kilde (OK/ADVARSEL/FEIL) og en maskinlesbar `<!-- helse: … -->`-linje
- `overvak-pi.yml` sjekker daglig: issue og e-post hvis Pi-en er stille i over 20 timer, og eget issue hvis en kilde har FEIL
- `varsle-token-utlop.yml` varsler 14 dager før tokenet utløper
- `valider-kode.yml` kjører syntakssjekk, importsjekk og enhetstester ved hver push

## Utvikling

```bash
pip install scrapling==0.4.7            # nok for testene, ingen nettleser
python -m unittest discover -s tests    # fra rpi-scraper/
python smoke_test.py --kilde stortinget # ekte kjøring mot kilden, i temp-mapper
```

Alt som pushes til `main` kjører på Pi-en innen et par timer. **Ikke legg til
nye pip-pakker** uten å bygge imaget på nytt på Pi-en – avhengighetene er bakt
inn i imaget, og en manglende import stopper alle scraperne.

### Ny nettkilde

1. Lag `scrapers/ny_kilde.py` med en klasse som arver `NettstedScraper` og setter `kildenavn`, `base_url`, `state_fil`, `startpunkter` og eventuelt `inkluder_prefiks`/`ekskluder`
2. Legg den til i `scrapers/__init__.py`, i `KJØRINGER` i `main.py`, i `DATA_PATHS` i `config.py` og i `KATEGORI_INFO` i `formatters/markdown.py`

## Lisens

Kildekode: MIT-lisens (se `LICENSE` i rotkatalogen).

Innholdet i `data/` er hentet fra offentlige norske myndigheter og er underlagt deres respektive lisenser. Alt innhold refererer til originalkilden.
