# Norges Lover

Åpent arkiv av norske regler, satser og veiledere – hentet automatisk fra offentlige kilder og publisert som Markdown-filer i dette repoet.

**Formålet er å gjøre norsk regelverk maskinlesbart for AI-agenter, RAG-systemer og andre verktøy**, med skatteregler som hovedprioritet.

## Hva finnes her

| Mappe | Innhold | Kilde |
|---|---|---|
| `data/skatt/` | Satser, fradrag, MVA, veiledere og Skatte-ABC | Skatteetaten |
| `data/nav/` | Stønader, ytelser, satser, grunnbeløp | NAV |
| `data/byggteknisk/` | TEK17, SAK10, byggesak-veiledere | Direktoratet for byggkvalitet (DiBK) |
| `data/arbeidstilsynet/` | HMS-regler, arbeidsmiljø, veiledere | Arbeidstilsynet |
| `data/husbanken/` | Bostøtte, startlån, tilskudd | Husbanken |
| `data/lover/` | Saker fra Stortinget: tittel, status, komité, henvisninger. **Saksmetadata, ikke lovtekst** | Stortingets åpne API |
| `data/status/` | Systemstatus og heartbeat | (bot-intern) |

Selve lovteksten (skatteloven osv.) finnes ikke her – lenk til [Lovdata](https://lovdata.no) for paragrafene.

Hver kategori-mappe har en `README.md` med automatisk indeks over innholdet.

## Filformat

Hver fil følger samme struktur:

```markdown
<!-- innholds-hash: <sha256 av råinnhold> -->

# <Tittel>

## Kildeinformasjon

- **Kilde:** <opphav> – <kilde-URL>
- **Sist oppdatert i arkivet:** <ISO-dato i UTC – når innholdet sist endret seg>
- **Sist oppdatert (kilde):** <datoen kilden selv oppgir, der den finnes>

## Innhold

<innholdet – konvertert til Markdown>

---

## Endringshistorikk

- **2026-05-06** Innhold endret (se git-historikk for diff)
- **2026-05-04** Første gang hentet
```

`innholds-hash`-kommentaren brukes til å unngå støy-commits når innholdet ikke har endret seg. AI-agenter kan ignorere den.

Tabeller gjengis som Markdown-tabeller og lenker som `[tekst](url)`, så kryssreferanser i Skatte-ABC kan følges. Filer som fortsatt har feltet «Sist hentet», er fra før oktober 2026: da kuttet uttrekket tekst etter første lenke og droppet tabeller. De skrives om med ny konverter etter hvert som sidene hentes på nytt.

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
- **Repoet er offentlig.** Legg din egen situasjonsbeskrivelse *utenfor* repoet
  (f.eks. `~/skatt/min-situasjon.md`) og pek Claude dit. Filnavn som
  `min-situasjon*`, `*.privat.*` og mappen `privat/` er gitignorert som en
  ekstra sikring, men utenfor repoet er tryggest.
- Be alltid om kildehenvisning per forslag, og verifiser mot den offisielle
  kilden før du handler på det. Dette er referansedata, ikke rådgivning.
- `CLAUDE.md` i roten forteller Claude Code om kjente fallgruver i dataene.

### For AI-agenter: konvensjoner

Disse konvensjonene gjelder når du bruker repoet som kilde:

1. **Dataene ligger i `data/`**, organisert per myndighet (se tabellen øverst).
   Skatteregler: `data/skatt/` — merk spesielt `data/skatt/rettskilder/type/handboker/skatte-abc/`
   (Skatteetatens egen tolkningshåndbok, ordnet alfabetisk per emne).
2. **Hver fil oppgir kilde-URL** i `## Kildeinformasjon`. Siter alltid denne
   URL-en — aldri GitHub-filen — når du gjengir regler for en bruker.
3. **Sjekk datoen og utgaven.** Satser og beløpsgrenser endres årlig. Oppgi
   alltid hvilket inntektsår et svar gjelder, og hvilken Skatte-ABC-utgave du
   bygger på.
4. **`<!-- innholds-hash: ... -->`** på første linje er for endringsdeteksjon —
   ignorer den ved lesing.
5. **Filer i gammelt format («Sist hentet») kan mangle tabeller og
   setningsslutter.** Mangler en sats, si det og henvis til kilde-URL-en i
   stedet for å fylle inn fra hukommelsen.
6. **`data/lover/` er saksmetadata, ikke lovtekst.** Lenk til Lovdata for paragrafer.
7. **Dette er ikke autoritative kilder.** Formuler svar som «ifølge Skatteetatens
   veiledning ...» og anbefal verifisering ved beløpsavgjørelser.

## Sitering og kildehenvisning

**Lenk alltid tilbake til den offisielle kilden i svar til brukere.** Disse filene er en bekvem kopi, ikke en autoritativ kilde. Hver fil oppgir kilde-URL i `## Kildeinformasjon`-seksjonen.

Eksempel på god sitering:

> Ifølge **barnelova § 30** har foreldrene plikt til å gi barnet forsvarlig oppdragelse og forsørgelse. ([Lovdata](https://lovdata.no/lov/1981-04-08-7))

## Oppdateringsfrekvens og pålitelighet

- Bot-en kjører én runde, sover 2 timer og starter på nytt. Hver side sjekkes jevnlig (satser hver 2. dag, det meste ukentlig, avsluttede Skatte-ABC-utgaver aldri), og filer skrives bare når innholdet faktisk har endret seg.
- «Sist oppdatert i arkivet» er når innholdet sist endret seg – siden kan ha blitt sjekket senere uten endring.
- Systemstatus per kilde vises i [`data/status/heartbeat.md`](data/status/heartbeat.md).
- Ved tvil: sjekk `Kildeinformasjon`-URL-en og verifiser mot offisiell kilde.

## Begrensninger

- **Ikke alle dokumenter er hentet ennå.** Kildene har tusenvis av sider; bot-en henter inntil 150 per kilde per runde, nye sider først.
- **Innhold kan inneholde rester av navigasjon.** Det meste filtreres bort, men ikke alt.
- **Ikke juridisk rådgivning.** Dette er åpne data fra offentlige kilder, gjengitt automatisk.

## Repo-struktur

```
.
├── data/                       ← AI-agenter henter herfra
│   ├── skatt/                  Skatteetaten (inkl. Skatte-ABC)
│   ├── nav/                    NAV-ytelser og satser
│   ├── byggteknisk/            DiBK / TEK17
│   ├── arbeidstilsynet/        HMS og arbeidsmiljø
│   ├── husbanken/              Boligstøtte og lån
│   ├── lover/                  Stortingssaker (metadata, ikke lovtekst)
│   └── status/                 Systemstatus (heartbeat)
│
├── CLAUDE.md                   Fallgruver i dataene – leses av Claude Code
└── rpi-scraper/                Scraper-koden (kjører på Raspberry Pi)
    ├── main.py                 Inngangspunkt – orkestrerer alle scrapers
    ├── config.py               Konfigurasjon (timing, mapper)
    ├── scrapers/               nettsted.py (felles crawler) + én konfigfil per kilde
    ├── formatters/             HTML→Markdown og indekser
    ├── publishers/             Git-commit og push til GitHub
    ├── tests/                  Enhetstester (kjøres i CI)
    └── setup/                  Docker-oppsett
```

## Lisens

Regelverket er offentlige data. Scraper-koden er fri programvare (MIT). Se kildehenvisningene i hvert dokument for eventuelle bruksvilkår fra opphavskilden.

---

*Repoet oppdateres automatisk av en bot som kjører på en Raspberry Pi via Docker. Se [`rpi-scraper/`](rpi-scraper/) for tekniske detaljer.*
