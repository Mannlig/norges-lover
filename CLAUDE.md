# CLAUDE.md

Åpent arkiv av norsk regelverk (Skatteetaten, NAV, DiBK, Arbeidstilsynet,
Husbanken, Stortinget) som Markdown, skrapet av en Raspberry Pi. Hovedbruken er
å la Claude svare på skattespørsmål med kildehenvisning.

## Når du bruker dataene

- **Skatt:** `data/skatt/`. Skatteetatens tolkningshåndbok ligger under
  `data/skatt/rettskilder/type/handboker/skatte-abc/<utgave>/`. Sjekk hvilken
  utgave filen tilhører, og si alltid hvilket inntektsår et svar gjelder.
- **`data/lover/` er IKKE lovtekst.** Det er saksmetadata fra Stortinget
  (tittel, status, komité). For selve paragrafene: lenk til Lovdata.
- **Verifiser beløp og satser mot kilde-URL-en** i `## Kildeinformasjon`
  før du foreslår noe som påvirker penger. Siter kilde-URL-en, ikke GitHub-filen.
- **Eldre filer kan ha hull.** Før oktober 2026 kuttet uttrekket tekst etter
  første lenke/utheving og droppet tabeller. Filer med feltet «Sist hentet»
  er i gammelt format og kan mangle tall og setningsslutter; filer med
  «Sist oppdatert i arkivet» er hentet med ny konverter. Mangler en sats
  eller setning, si det og henvis til kilden – ikke fyll inn fra hukommelsen.
- Ved søk: utelat indeksene, f.eks. `grep -r --exclude=README.md`.
- Første linje (`<!-- innholds-hash: … -->`) er for endringsdeteksjon – ignorer.

## Personopplysninger

Repoet er offentlig. Skriv aldri brukerens inntekt, formue eller andre
personlige opplysninger inn i repoet. Hold dem utenfor repoet, eller i filer
som er gitignorert (`min-situasjon*`, `*.privat.*`, `privat/`).

## Når du endrer koden

- **Alt som havner på `main` kjører på Pi-en innen ett par timer** (entrypoint
  gjør `git reset --hard origin/main` før hver runde). Ingen staging.
- Kjør testene før push: `cd rpi-scraper && python -m unittest discover -s tests`
  (krever bare `pip install scrapling==0.4.7`, ingen nettleser).
- **Ingen nye pip-pakker** uten å avtale det: `requirements.txt` er bakt inn i
  Docker-imaget, og en ny import stopper alle scraperne til eieren bygger
  imaget på nytt for hånd. Det samme gjelder endringer i `Dockerfile` og
  `rpi-scraper/setup/entrypoint.sh` – de krever `docker compose up -d --build`.
- Nettkildene deler logikk i `scrapers/nettsted.py`; hver kilde er bare
  konfigurasjon. HTML→Markdown ligger i `formatters/html.py`.
- Heartbeat (`data/status/heartbeat.md`) har en maskinlesbar helselinje som
  `.github/workflows/overvak-pi.yml` leser. Endrer du formatet, endre begge.
