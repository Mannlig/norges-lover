<!-- innholds-hash: 998c3ecdbf4006f38446f369fa99a7d20dbc6a60296b924c08b73d1739a130e7 -->

# Testinnsending av SAF-T Regnskap (Financial) og SAF-T Kassasystem (CashRegister)

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/starte-og-drive/rutiner-regnskap-og-kassasystem/saf-t-regnskap/testinnsending/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-27T19:50:29Z

## Innhold

## Testinnsending av SAF-T Regnskap (Financial) og SAF-T Kassasystem (CashRegister)

Skatteetaten tilbyr testinnsending for systemleverandører og andre som utvikler løsninger for å støtte SAF-T formatene.

### Kort om testinnsending

Vi anbefaler alle som utvikler løsninger som støtter SAF-T formatene å delta på test. Ved å delta kan du teste validering av filformatet og få tilbakemelding om innholdet.

For å bidra til at en SAF-T fil skal ha så god kvalitet som mulig gjør vi en gjennomgang av innsendte SAF-T testfiler. Vi kontrollerer at opplysningene i testfilene er konsistente.

For SAF-T Regnskap sjekker vi for eksempel at alle MVA koder (<TaxCode>) som er brukt i transaksjoner (GeneralLedgerEntries) er definerte i oversikten over MVA koder (MasterFiles\TaxTable).

For SAF-T Kassasystem sjekker vi for eksempel at alle hendelsestyper (<eventType>) som er brukt i «hendelser» (<event>) er definert i oversikten over hendelser som ikke er salg (Event codes) i basics.

#### Test filformatet selv

Før dere sender inn SAF-T testinnsending bør dere teste filformatet selv. Det finnes ulike valideringsverktøy som kan brukes. Skatteetaten har utviklet en [validator for testing av filformatet (Github)](https://github.com/Skatteetaten/saf-t).

### Slik kan du teste

Du kan sende testfiler i SAF-T format på e-post til:

saft.testinnsending@skatteetaten.no

Dersom en testinnsending består av flere filer kan disse sendes samlet. Hver testfil kan være inntil 15 mb og en testinnsending kan bestå av inntil 10 filer.

Vi aksepterer bare xml-filer som vedlegg i eposten.

Vi aksepterer ikke .zip-filer.

#### SAF-T filene skal inneholde syntetiske data

Filene som sendes inn til Skatteetatens testmiljø skal av hensyn til personvern inneholde syntetiske data.

Syntetiske data vil si kunstige data, ikke basert på ekte data. Syntetisk data skal ikke inneholde identifiserbar informasjon om personer eller virksomheter. Identifiserbar informasjon kan for eksempel være organisasjonsnummer, personnummer, adresse, telefonnummer og lignende.

Filer som har annet innhold enn syntetiske data blir ikke behandlet.

### Tilbakemelding

Etter at testfilen er gjennomgått, sender vi en tilbakemelding via e-post.

Ønsker du tilbakemeldingen på engelsk kan du informere oss når du sender inn SAF-T testfilen.

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/starte-og-drive/rutiner-regnskap-og-kassasystem/saf-t-regnskap/testinnsending/) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-27** Første gang hentet
