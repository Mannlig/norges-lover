# Norges Lover

Åpent arkiv av norsk lovverk, forskrifter, satser og veiledere – hentet automatisk fra offentlige kilder og publisert som Markdown-filer i dette repoet.

**Formålet er å gjøre norsk regelverk maskinlesbart for AI-agenter, RAG-systemer og andre verktøy som trenger lokal tilgang til lovteksten uten å treffe rate-limit på Lovdata.**

## Hva finnes her

| Mappe | Innhold | Kilde |
|---|---|---|
| `data/lover/` | Nasjonale lover, proposisjoner og Stortinget-saker | Stortingets åpne API |
| `data/skatt/` | Skattesatser, fradrag, MVA, veiledere | Skatteetaten |
| `data/byggteknisk/` | TEK17, SAK10, byggesak-veiledere | Direktoratet for byggkvalitet (DiBK) |
| `data/nav/` | Stønader, ytelser, satser, grunnbeløp | NAV |
| `data/arbeidstilsynet/` | HMS-regler, arbeidsmiljø, veiledere | Arbeidstilsynet |
| `data/husbanken/` | Bostøtte, startlån, tilskudd | Husbanken |
| `data/kommuner/` | Lokale og kommunale forskrifter | Lovdata |
| `data/status/` | Systemstatus og heartbeat | (bot-intern) |

Hver kategori-mappe har en `README.md` med automatisk indeks over innholdet.

## Filformat

Hver fil følger samme struktur:

```markdown
<!-- innholds-hash: <sha256 av råinnhold> -->

# <Tittel>

## Kildeinformasjon

- **Kilde:** <opphav> – <kilde-URL>
- **Sist hentet:** <ISO-dato i UTC>

## Innhold

<innholdet – konvertert til Markdown>

---

## Endringshistorikk

- **2026-05-06** Innhold endret (se git-historikk for diff)
- **2026-05-04** Første gang hentet
```

`innholds-hash`-kommentaren brukes til å unngå støy-commits når innholdet ikke har endret seg. AI-agenter kan ignorere den.

## Bruk som AI-agent

### 1. Klon hele repoet

```bash
git clone --depth 1 https://github.com/mannlig/norges-lover.git
grep -rl "barnehage" norges-lover/data/
```

### 2. Hent enkeltfiler via raw URL

```python
import urllib.request
url = "https://raw.githubusercontent.com/mannlig/norges-lover/main/data/nav/dagpenger.md"
text = urllib.request.urlopen(url).read().decode("utf-8")
```

### 3. Sparse checkout (bare én kategori)

```bash
git clone --no-checkout --filter=blob:none https://github.com/mannlig/norges-lover.git
cd norges-lover
git sparse-checkout init --cone
git sparse-checkout set data/skatt
git checkout main
```

### 4. RAG / vektor-indeksering

Hver fil er semantisk avgrenset til ett lovverk eller ett tema. Anbefalt chunking:
- **Per fil** for korte dokumenter (< 10 KB)
- **Per `## ` / `### `-overskrift** for lengre dokumenter
- Behold `## Kildeinformasjon`-blokken i hvert chunk slik at modellen kan sitere kilde

### 5. Sjekke om en fil er endret

`innholds-hash` gjør det billig å detektere endringer uten å re-indeksere:

```python
import re
text = open("data/nav/dagpenger.md").read()
match = re.search(r"<!-- innholds-hash: ([a-f0-9]{64}) -->", text)
hash_i_fil = match.group(1) if match else None
# Sammenlign med din lagrede hash
```

## Bruk med Claude Code (og andre AI-verktøy)

### For mennesker: skatteanalyse med Claude Code

Repoet egner seg som kunnskapsgrunnlag når du vil ha veldokumenterte svar om
norske regler — for eksempel lovlige måter å redusere skatt på:

```bash
# 1. Klon repoet (eller bare skatt-delen, se sparse checkout over)
git clone --depth 1 https://github.com/mannlig/norges-lover.git

# 2. Start Claude Code i mappen
cd norges-lover && claude
```

Eksempel på spørsmål du kan stille:

> Jeg har lønnsinntekt på X kr, bolig med utleiedel, pendler 40 km til jobb
> og sparer i aksjefond. Gå gjennom data/skatt/ og finn alle fradrag og
> tilpasninger som er relevante for meg. Siter kilden for hvert forslag.

Tips:
- Legg din egen situasjonsbeskrivelse i en lokal fil (f.eks. `min-situasjon.md`)
  som **ikke** commites — repoet er offentlig.
- Be alltid om kildehenvisning per forslag, og verifiser mot den offisielle
  kilden før du handler på det. Dette er referansedata, ikke rådgivning.

### For AI-agenter: konvensjoner

Disse konvensjonene gjelder når du bruker repoet som kilde:

1. **Dataene ligger i `data/`**, organisert per myndighet (se tabellen øverst).
   Skatteregler: `data/skatt/` — merk spesielt `data/skatt/rettskilder/type/handboker/skatte-abc/`
   (Skatteetatens egen tolkningshåndbok, ordnet alfabetisk per emne).
2. **Hver fil oppgir kilde-URL** i `## Kildeinformasjon`. Siter alltid denne
   URL-en — aldri GitHub-filen — når du gjengir regler for en bruker.
3. **Sjekk `Sist hentet`-datoen.** Satser og beløpsgrenser endres årlig; er
   dataen gammel, si det eksplisitt og henvis til kilde-URL-en for gjeldende verdi.
4. **`<!-- innholds-hash: ... -->`** på første linje er for endringsdeteksjon —
   ignorer den ved lesing.
5. **Innholdet kan ha rest-UI** («Skriv ut», menytekst). Filtrer bort ved sitering.
6. **Dette er ikke autoritative kilder.** Formuler svar som «ifølge Skatteetatens
   veiledning (hentet DATO) ...» og anbefal verifisering ved beløpsavgjørelser.

## Sitering og kildehenvisning

**Lenk alltid tilbake til den offisielle kilden i svar til brukere.** Disse filene er en bekvem kopi, ikke en autoritativ kilde. Hver fil oppgir kilde-URL i `## Kildeinformasjon`-seksjonen.

Eksempel på god sitering:

> Ifølge **barnelova § 30** har foreldrene plikt til å gi barnet forsvarlig oppdragelse og forsørgelse. ([Lovdata](https://lovdata.no/lov/1981-04-08-7))

## Oppdateringsfrekvens og pålitelighet

- Bot-en kjører omtrent **hvert 2. time** og committer kun ved faktisk endring i innholdet.
- `Sist hentet`-feltet i hver fil viser hvor fersk dataen er.
- Systemstatus vises i [`data/status/heartbeat.md`](data/status/heartbeat.md).
- Ved tvil: sjekk `Kildeinformasjon`-URL-en og verifiser mot offisiell kilde.

## Begrensninger

- **Ikke alle dokumenter er hentet ennå.** Kildene har tusenvis av sider; bot-en arbeider seg gjennom køen ~150 dokumenter per kilde per kjøring.
- **Innhold kan inneholde navigasjonstekst.** Noen sider har «Verktøylinje», «Skriv ut» og lignende UI-elementer som ikke er filtrert helt vekk.
- **Ikke juridisk rådgivning.** Dette er åpne data fra offentlige kilder, gjengitt automatisk.

## Repo-struktur

```
.
├── data/                       ← AI-agenter henter herfra
│   ├── lover/                  Stortingssaker og nasjonale lover
│   ├── skatt/                  Skatteetaten
│   ├── byggteknisk/            DiBK / TEK17
│   ├── nav/                    NAV-ytelser og satser
│   ├── arbeidstilsynet/        HMS og arbeidsmiljø
│   ├── husbanken/              Boligstøtte og lån
│   ├── kommuner/               Lokale forskrifter
│   └── status/                 Systemstatus (heartbeat)
│
└── rpi-scraper/                Scraper-koden (kjører på Raspberry Pi)
    ├── main.py                 Inngangspunkt – orkestrerer alle scrapers
    ├── config.py               Konfigurasjon (URL-er, timing, mapper)
    ├── scrapers/               Én fil per kilde
    ├── formatters/             Markdown-konvertering
    ├── publishers/             Git-commit og push til GitHub
    └── setup/                  Docker-oppsett
```

## Lisens

Lovteksten er offentlige data. Scraper-koden er fri programvare (MIT). Se kildehenvisningene i hvert dokument for eventuelle bruksvilkår fra opphavskilden.

---

*Repoet oppdateres automatisk av en bot som kjører på en Raspberry Pi via Docker. Se [`rpi-scraper/`](rpi-scraper/) for tekniske detaljer.*
