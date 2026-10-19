<!-- innholds-hash: 2485bc25da8e327ae33051f7aa41c016c580080c6bb7b02b1558c93d0467e600 -->

# Nytt for inntektsåret 2026

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/nytt-for-inntektsaret/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-19T18:35:02Z

## Innhold

## Nytt for inntektsåret 2026

Her gjør vi oppmerksom på årlige endringer som påvirker rapportering av tredjepartsopplysninger.

For inntektsåret 2026 blir det vesentlige endringer som påvirker rapportering av tredjepartsopplysninger:

Tilgangsstyring

Altinn-roller slik du kjenner dem er erstattet av nye [tilgangspakker eller fullmakter.](https://info.altinn.no/hjelp/ny-tilgangsstyring/) Disse inneholder fullmakt til skjema og tjenester innenfor samme kategori

Du kan gi tilgang/fullmakt til en enkelttjeneste, mens en tilgangspakke gir tilgang til alle tjenestene som inngår i pakken.

For tredjepartsrapportering kan virksomheten velge enten:

- én eller flere relevante enkelttjenester, eller
- Tilgangspakken Skattegrunnlag

Tilgangspakken Skattegrunnlag gir tilgang til alle tjenestene i pakken, totalt om lag 55 tjenester. Ved å tildele enkelttjenester får medarbeideren kun tilgang til de tjenestene som er nødvendige for å utføre arbeidsoppgavene sine.

Det er virksomheten selv som må vurdere om det er mest hensiktsmessig å gi tilgang gjennom en tilgangspakke eller ved å tildele enkelttjenester, basert på hvilke arbeidsoppgaver medarbeideren skal utføre.

De mest brukte Altinn 2 rollene som blir borte og som må erstattes av en enkelttjeneste eller tilgangspakken Skattegrunnlag er:

- Regnskapsmedarbeider
- Utfyller/Innsender
- Begrenset signeringsrettighet
- Post/Arkiv

Rapportering

For inntektsåret 2026 tilbyr Skatteetaten flere løsninger for innrapportering av tredjepartsopplysninger. Opplysninger kan sendes direkte fra sluttbrukersystemer gjennom våre API-løsninger, noe som gir effektiv rapportering, bedre datakvalitet og mindre behov for manuelle operasjoner.

Nye API-er er tilgjengelig for testing, se [Innrapportering av tredjepartsopplysninger | API-dokumentasjon](https://skatteetaten.github.io/api-dokumentasjon/anvendelsesomraader/innrapportering-tredjepartsopplysninger#nye-api-er-for-re-etablering-av-altinn-tjenester)

Nye muligheter for maskinell innrapportering av tredjepartsopplysninger

For enkelte finans- og verdipapirordninger tilbyr Skatteetaten nå også innsending av XML-filer via maskin-til-maskin-integrasjon (M2M). Løsningen gjør det mulig å sende inn større datamengder direkte fra egne systemer ved bruk av samme XML-format som benyttes ved ordinær filrapportering.

XML-basert M2M er et supplement til eksisterende rapporteringsløsninger. Opplysningspliktige kan fortsatt rapportere ved filopplasting gjennom vedleggsskjemaet, og kan velge den innsendingsløsningen som passer best for egne systemer og rapporteringsbehov.

Merk at XML-basert M2M kun er tilgjengelig for utvalgte finans- og verdipapirordninger. For øvrige tredjepartsordninger gjelder de rapporteringsløsningene som er etablert for den enkelte ordning.

Både [API-baserte løsninger (JSON](https://skatteetaten.github.io/api-dokumentasjon/anvendelsesomraader/innrapportering-tredjepartsopplysninger)), [XML-basert M2M](https://skatteetaten.github.io/api-dokumentasjon/api/innrapportering-tpo-filmottak) og filopplasting gjennom vedleggsskjemaet legger til rette for sikker og effektiv rapportering til Skatteetaten.

Les mer om informasjonsmodeller, eksempelfiler, testing og annen nyttig informasjon på [GitHub](https://skatteetaten.github.io/api-dokumentasjon/anvendelsesomraader/innrapportering-tredjepartsopplysninger), eller [overordnet informasjon om reetableringen av våre tjenester](https://www.skatteetaten.no/samarbeidspartnere/reetablering-altinn/)

### Tidligere års endringer

For inntektsåret 2025 blir det vesentlige endringer som påvirker rapportering av tredjepartsopplysninger:

Reetablering av skjemaer på skatteetaten.no

Altinn skal fornyes. I den forbindelse reetablerer vi våre tjenester på skatteetaten.no, samtidig som vi tar i bruk fellesløsninger fra Altinn. Alle som benytter Skatteetatens tjenester, bør sette seg inn i endringene i god tid før årsskiftet 2025/2026 og gjennomføre nødvendige tilpasninger.

Les mer om informasjonsmodeller, eksempelfiler, testing og annen nyttig informasjon på [GitHub](https://skatteetaten.github.io/api-dokumentasjon/anvendelsesomraader/innrapportering-tredjepartsopplysninger), eller [overordnet informasjon om reetableringen av våre tjenester](https://www.skatteetaten.no/samarbeidspartnere/reetablering-altinn/)

For verdipapirfondshistorikk:

For 2025 er format i internasjonal adresse for disponent og oppgaveeier endret.

For inntektsåret 2024 er det ingen endringer som påvirker rapportering av tredjepartsopplysninger.

For ordningen Innskudd, utlån og renter:

Rapportering av medlånetaker pliktig fra skatteåret 2023.

Aksjesparekonto, Fondskonto, Innskudd, utlån og renter, Livsforsikring, Finansprodukter og Verdipapirfond:

Avvikling av mulighet for merking av konti til utveksling

- Oppgaver som med verdien «true» i feltet «inneholderInternasjonalRapportering» vil avvises i mottaket. Oppgaver som skal rapporteres til utveksling i tillegg til ordinær rapportering må i tillegg rapporteres til tredjepartsordningen Internasjonal rapportering CRS/FATCA.

Endring i formatbeskrivelser:

Aksjesparekonto, Finansprodukter og Fondskonto:

- Nytt frivillig felt «andelFraOgMed20221006» må benyttes for skattepliktig beløp akkumulert fra 6. oktober til og med 31. desember.

Endring i formatbeskrivelser:

Aksjesparekonto:

- Nytt frivillig felt "kontoOverfoertNyTilbyder". Merkes "True" hvis beholdning på konto er overført en annen tilbyder.

Finansprodukter

- Nytt frivillig felt "ukjentGevinstEllerTap". Merkes "True" hvis det mangler data for å kunne gjøre en korrekt gevinst/tapsberegning.

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/nytt-for-inntektsaret/) av norges-lover-bot.*

## Endringshistorikk

- **2026-05-21** Første gang hentet
- **2026-10-10** Innhold endret (se git-historikk for diff)
- **2026-10-19** Innhold endret (se git-historikk for diff)
