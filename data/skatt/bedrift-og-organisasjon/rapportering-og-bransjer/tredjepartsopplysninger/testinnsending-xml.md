<!-- innholds-hash: 3e28ace4b86a5e8f7bba836e84dfb7be66d3608900f7f64dc49983c4ab0e460d -->

# Testinnsending av tredjepartsopplysninger som skal rapporteres som filvedlegg

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/testinnsending-xml/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-10T11:36:19Z

## Innhold

## Testinnsending av tredjepartsopplysninger som skal rapporteres som filvedlegg

Skatteetaten tilbyr testinnsending for opplysningspliktige og innsendere som skal levere tredjepartsopplysninger som filvedlegg via nytt skjema på Skatteetaten for inntektsåret 2025.

Viktig informasjon

For de som bruker filopplastingstjenesten til rapportering av tredjepartsopplysninger vil det være flere endringer:

- For tredjepartsopplysninger vil opplasting av vedlegg kun være tilgjengelig gjennom manuell løsning for rapportering av tredjepartsopplysninger med vedlegg på Skatteetaten.no (RF-1301) og ikke API.
- Av sikkerhetsmessige årsaker godtas ikke zip-filer, kun XML-filer.
- En fil kan være på opptil 2 GB.
- En fil kan kun inneholde data for én oppgavegiver *, én ordning, og for ett inntektsår av gangen. Skal du sende inn for flere oppgavegivere, ordninger eller korrigeringer for tidligere inntektsår, må dataene legges i separate filer.
- Du kan sende inn opptil 20 filer samtidig. Hver fil behandles som én leveranse med en tilhørende tilbakemelding (20 filer = 20 leveranser).
- Mulighet for maskinell filopplasting via RF-1301 (på Altinn 2) videreføres midlertidig frem til Altinn 2 skrus av i juni.
- Det vil kun være mulig å gjøre komplette innsendinger. Muligheten for "ikke komplette" innsendinger ble fjernet 2. januar 2026.
- Vi bruker en skytjeneste for å kontrollere filen du laster opp. For å unngå problemer med brannmur, sørg for at det er åpning basert på FQDN til stincomingplattformskarp.blob.core.windows.net

* Kravet om kun én opplysningspliktig i en leveranse pr innsending er ikke definert i xsd, men validering i tjenesten vil gi feil i tilbakemeldingen dersom man sender flere.

### Kort om testinnsending

Vi anbefaler alle som rapporterer tredjepartsopplysninger som vedlegg å delta på test. Ved å delta får dere mulighet til å teste hele verdikjeden, både validering av filformatet, selve innsendingsprosessen og sjekk av tilbakemelding på innsendte data.

Vi tar imot testfiler hele året.

Før dere sender inn tredjepartsopplysninger på XML-format bør dere teste filformatet selv.

[Formatene for inntektsåret 2025](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/formatbeskrivelser/)

For 2025 er format i internasjonal adresse for disponent og oppgaveeier endret for Verdipapirfondhistorikk.

Via reetablert løsning for rapportering av tredjepartsopplysninger som vedlegg (RF-1301), kan du sende inn filer til Skatteetaten for følgende ordninger:

| Ordning |
| --- |
| Aksjesparekonto |
| Aksjonærregisteroppgaven |
| Betalinger til selvstendig næringsdrivende |
| Boligsameie |
| Boligselskap |
| Boligsparing for ungdom |
| Drosjesentraler |
| Fagforeningskontingent |
| Finansprodukter |
| Fondskonto |
| Gaver til frivillige organisasjoner, tros- og livssynssamfunn |
| Godtgjøring til opphaver til åndsverk |
| Individuelle pensjonsordninger |
| Innskudd, utlån og renter |
| Internasjonal rapportering (CRS FATCA) |
| Kjøp fra primærnæring – egg |
| Kjøp fra primærnæring - frukt, bær, poteter og grønnsaker (jord- og hagebruk) |
| Kjøp fra primærnæring – korn |
| Kjøp fra primærnæring – melk |
| Kjøp fra primærnæring – slakt |
| Livsforsikring |
| Melding om flernasjonale konserns fordeling av inntekt, skatt m.v. (Land-for-land-rapport for skatteformål) |
| Melding om utleie av fast eiendom fra formidlingsselskaper |
| Opsjoner i oppstartsselskap |
| Overskuddstrøm (NY) |
| Pass og stell av barn |
| Primær - Fisk |
| Primær - Tømmer |
| Skadeforsikring |
| Skattefrie utbetalinger fra offentlige myndigheter |
| Skattepliktig kundeutbytte |
| Tilskudd erstatning mv innen primærnæringene |
| Tilskudd til vitenskapelig forskning eller yrkesopplæring |
| Underholdsbidrag |
| Verdipapirfond historikk |
| Verdipapirfond |

### Slik kan du teste

Nytt skjema for rapportering av tredjepartsopplysninger som vedlegg på skatteetaten.no er tilgjengelig. Lenken leder deg til skjema i et testmiljø med syntestiske testdata.

[Tredjepartsopplysninger som vedlegg (TEST)](https://skatt-test.sits.no/web/tpo-filopplasting/)

Når du sender inn tredjepartsopplysninger vil du motta svar fra Skatteetatens nye [innboks (lenke til innboks i testmiljø)](https://skatt-test.sits.no/web/minside/innboks/). Ønsker du å se tilbakemeldinger i [innboks i Altinn, gå hit](https://info.tt02.altinn.no/).

#### Du må ha en testperson

Du må ha en testperson for å kunne sende inn testfiler til Skatteetaten. Du finner informasjon om dette på [Tenor testdatasøk](https://www.skatteetaten.no/testdata/). Når du søker frem testperson er det viktig å sørge for at denne har riktig rolle i firma. Vi anbefaler deg å velge testbruker som er daglig leder.

Vi gjør oppmerksom på at testpersonene ikke er personlige. Samme testperson kan dermed benyttes av flere testinnsendere.

#### Filvedlegg skal kun inneholde syntetiske data

Filen som sendes inn til Skatteetatens testmiljø skal av personvernhensyn inneholde syntetiske data. Syntetiske data vil si kunstige data, ikke basert på ekte data. Syntetiske data skal ikke inneholde identifiserbar informasjon om personer eller virksomheter. Identifiserbar informasjon kan for eksempel være organisasjonsnummer, personnummer, adresse, telefonnummer og lignende.

Hvis dere sender inn filer som inneholder noe annet enn syntetiske data, vil disse ikke bli behandlet.

#### Tilbakemeldinger

Tilbakemelding på innrapportering av grunnlagsdata kan hentes ut via API, eller lastes ned via innboks på Skatteetaten. De er tilgjengelig i PDF-, XML- og CSV-format.

[Teknisk spesifikasjon av XML tilbakemelding (Github)](https://skatteetaten.github.io/api-dokumentasjon/anvendelsesomraader/innrapportering-tredjepartsopplysninger#teknisk-spesifikasjon-av-xml-tilbakemelding)

### Trenger du hjelp?

Dersom du har spørsmål om test av tredjepartsopplysninger, eller vil gi oss tilbakemeldinger på skjema, ta kontakt med oss på slack, i kanalen [#innrapportering-av-tredjepartsopplysninger](https://skatteetaten.slack.com/archives/C070DRSNVLP).

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/testinnsending-xml/) av norges-lover-bot.*

## Endringshistorikk

- **2026-05-21** Første gang hentet
- **2026-10-10** Innhold endret (se git-historikk for diff)
