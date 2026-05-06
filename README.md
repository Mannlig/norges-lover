# Norges Lover

Åpent arkiv av norsk lovverk, forskrifter, satser og veiledere – henta automatisk fra offentlige kilder og publisert som Markdown-filer i dette repoet.

**Formålet er å gjøre norsk regelverk maskinlesbart for AI-agenter, RAG-systemer og andre verktøy som trenger lokal tilgang til lovteksten uten å rate-limit-e Lovdata.**

## Hva som finnes her

| Mappe | Innhold | Kilde |
|---|---|---|
| `data/lover/` | Nasjonale lover (folketrygdloven, skatteloven, …) og Stortinget-saker | Lovdata + Stortingets åpne API |
| `data/lover/lokale-forskrifter/` | Kommunale og lokale forskrifter | Lovdata |
| `data/lover/stortingsvedtak/` | Stortingsvedtak | Lovdata |
| `data/skatt/` | Skattesatser, fradrag, MVA, veiledere | Skatteetaten |
| `data/byggteknisk/` | TEK17, SAK10, byggesak-veiledere | Direktoratet for byggkvalitet |
| `data/nav/` | Stønader, ytelser, satser, grunnbeløp | NAV |

Hver kategori-mappe har en `README.md` med automatisk indeks over innholdet.

## Filformat

Hver fil følger samme struktur:

```markdown
<!-- innholds-hash: <sha256 av råinnhold> -->

# <Lovnavn>

## Kildeinformasjon

- **Kilde:** <opphav> – <kilde-URL>
- **Sist oppdatert (kilde):** <ISO-dato eller "ukjent">
- **Sist hentet:** <ISO-dato i UTC>

## Innhold

<lovteksten – konvertert til Markdown med h2/h3 for kapitler/§§>

---

## Endringshistorikk

- **2026-05-06** Innhold endret (se git-historikk for diff)
- **2026-05-04** Første gang hentet
```

`innholds-hash`-kommentaren brukes til å unngå støy-commits når innholdet ikke har endra seg. AI-agenter kan ignorere den.

## Bruk som AI-agent

### 1. Klon hele repoet (mindre enn 100 MB)

```bash
git clone --depth 1 https://github.com/mannlig/norges-lover.git
grep -l "barnehage" norges-lover/data/lover/*.md
```

### 2. Hent enkeltfiler via raw URL

```python
import urllib.request
url = "https://raw.githubusercontent.com/mannlig/norges-lover/main/data/lover/barnelova.md"
text = urllib.request.urlopen(url).read().decode("utf-8")
```

### 3. Sparse checkout (bare en kategori)

```bash
git clone --no-checkout --filter=blob:none https://github.com/mannlig/norges-lover.git
cd norges-lover
git sparse-checkout init --cone
git sparse-checkout set data/skatt
git checkout main
```

### 4. RAG / vektor-indeksering

Hver fil er semantisk avgrensa til ett lovverk eller ett tema. Anbefalt chunking:
- **Per fil** for små lover (< 10 KB)
- **Per `## ` / `### `-overskrift** for større lover (kapitler/paragrafer)
- Behold `## Kildeinformasjon`-blokken i hvert chunk slik at modellen kan sitere kilde

### 5. Sjekke om en fil er endra

`innholds-hash` gjør det billig å detektere endringer uten å re-indeksere:

```python
import re, hashlib
text = open("data/lover/barnelova.md").read()
match = re.search(r"<!-- innholds-hash: ([a-f0-9]{64}) -->", text)
hash_in_file = match.group(1) if match else None
# Sammenlign med din lokale lagra hash
```

## Sitering og kildehenvisning

**Du må alltid lenke tilbake til den offisielle kilden i svar til brukere.** Disse Markdown-filene er en bekvem kopi, ikke en autoritativ kilde. Hver fil oppgir kilde-URL i `## Kildeinformasjon`-seksjonen.

Eksempel på god sitering fra en AI-agent:

> Ifølge **barnelova § 30** har foreldrene plikt til å gi barnet forsvarlig oppdragelse og forsørgelse. ([Lovdata](https://lovdata.no/lov/1981-04-08-7))

## Friskhet og pålitelighet

- Bot-en oppdaterer hvert **6. time** og pusher commit kun ved faktisk endring.
- `Sist hentet`-feltet i hver fil viser hvor frisk dataen er.
- Lovdata re-sjekkes hvert **90. dag** for innholdsendringer (selv om vi vet om dokumentet fra før).
- Ved tvil: sjekk `Kildeinformasjon`-URL-en og verifiser mot offisiell kilde.

## Begrensninger

- **Ikke alle lover er hentet ennå.** Lovdata har 700+ nasjonale lover og 11 800+ lokale forskrifter; bot-en arbeider seg gjennom køen ~100 dokumenter per kjøring.
- **Innhold kan inneholde navigasjon.** Noen sider har `Verktøylinje`, `Skriv ut` og lignende UI-elementer som ikke er filtrert helt vekk. Filtrere på h2/h3 eller `§`-prefiks for ren lovtekst.
- **Ikke juridisk rådgivning.** Dette er åpne data fra offentlige kilder, gjengitt automatisk. Bruk det som referanse, ikke autoritativ tolking.

## Repo-struktur

```
.
├── data/                    # ← AI-agenter henter herfra
│   ├── lover/
│   ├── skatt/
│   ├── byggteknisk/
│   └── nav/
└── rpi-scraper/             # Scraper-koden (ikke nødvendig for å bruke dataen)
    ├── main.py
    ├── scrapers/
    ├── publishers/
    └── smoke_test.py        # Smoke-test for utviklere
```

## Lisens

Lovteksten selv er offentlige data. Strukturering, formatering og scraper-koden er fri programvare – se kildene som blir oppgitt i hvert dokument for evt. bruksvilkår fra opphavskilden.

---

*Denne repo-en oppdateres automatisk av en bot som kjører på en Raspberry Pi. Se [`rpi-scraper/`](rpi-scraper/) for tekniske detaljer.*
