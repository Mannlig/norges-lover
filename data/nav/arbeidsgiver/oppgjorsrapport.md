<!-- innholds-hash: f557a6c0808a609ff9689838a84a197540b0a87db930353fb35dac5e46092012 -->

# Oppgjørsrapport arbeidsgiver – refusjoner fra Nav  - nav.no

## Kildeinformasjon

- **Kilde:** NAV (Arbeids- og velferdsdirektoratet) – https://www.nav.no/arbeidsgiver/oppgjorsrapport
- **Sist oppdatert i arkivet:** 2026-10-06T04:30:47Z

## Innhold

For arbeidsgivere

## Oppgjørsrapport arbeidsgiver – refusjoner fra Nav

Oppgjørsrapporten (tidligere kalt K27) gir oversikt over utbetalte refusjoner fra Nav. Du kan sjekke om utbetalingen stemmer med det virksomheten forventer.

Nytt: Nav sender oppgjørsrapport via Altinn 3

15. juni 2026 avvikles Altinn 2, og vi sender kun rapporter via Altinn 3.

Leverandører av lønns- og personalsystem må ta i bruk nytt API før 15. juni 2026. Her er [teknisk info om API for oppgjørsrapport](https://github.com/navikt/sokos-oppgjorsrapporter/wiki/Forel%C3%B8pig-fremdriftsplan).

### Om oppgjørsrapporten

Oppgjørsrapporten viser informasjon om refusjon av sykepenger, foreldrepenger, feriepenger, svangerskapspenger, pleie/opplæring- og omsorgspenger.

Rapporten blir tilgjengelig i innboksen i Altinn 1-2 virkedager etter utbetaling. Hvis du ikke får varsel om ny rapport i Altinn 3 innboks, må du få delegert riktig tilgang.

Hvis rapporten viser et minusbeløp knyttet til organisasjonsnummeret ditt, bør du undersøke om virksomheten har fått et brev fra Nav som forklarer trekket.

Hvis du mangler refusjon for en ansatt, [sjekk saksbehandlingstidene til Nav her](https://www.nav.no/arbeidsgiver/saksbehandlingstider). Ved avvik bør du kontakte Nav.

Nav utbetaler refusjoner slik at de er på konto første virkedag i en ny måned. Hvis du får refusjon utenom dette, vil du få en egen oppgjørsrapport i etterkant.

Pengene utbetales til det kontonummeret virksomheten har registrert hos Nav.

Her kan du lese om hvem som kan registrere kontonummer og hvordan det gjøres: [Registrere kontonummer for utbetalinger fra Nav](https://www.nav.no/arbeidsgiver/endre-kontonummer)

### Oppgjørsrapport med feriepenger

Rapporten i juni inneholder både feriepenger fra i fjor og ordinære refusjoner for mai. Feriepengene står alltid med perioden 01.05-31.05, uavhengig av når de egentlig er opptjent.

Hvis en stønadsperiode fra i fjor beregnes på nytt etter juni, blir også feriepengene regnet om, og endringen vises på neste måneds oppgjørsrapport.

Her kan du lese mer om [ferie og feriepenger](https://www.nav.no/feriepenger#stotter) for ulike pengestøtter og [refusjon av feriepenger til arbeidsgiver](https://www.nav.no/arbeidsgiver/feriepenger#refusjon-feriepenger)

### Tilgang til rapporten

#### Hvem kan lese rapporten?

For å lese rapporten trenger du en av disse tilgangspakkene i Altinn:

- Lønn med personopplysninger av særlig kategori
- Ansvarlig revisor
- Regnskapsfører lønn
- Regnskapsfører med eller uten signeringsrettighet
- Revisormedarbeider

Du kan også gi tilgang til bare denne rapporten ved å tildele enkelttjenesten: Oppgjørsrapport arbeidsgiver - refusjoner fra Nav (tidligere K27). Dette gir bedre mulighet til å begrense innsyn internt i din virksomhet.

Du finner mer om [enkelttjenester og tilgangspakker på altinn.no](https://info.altinn.no/hjelp/ny-tilgangsstyring/). Hvis du lurer på noe om tilganger, må du kontakte Altinn. Se [Altinns hjelpesider om tilgangsstyring](https://info.altinn.no/hjelp/).

Tjenesten inneholder noe sensitiv informasjon og krever derfor minimum innlogging med sikkerhetsnivå 3. Sikkerhetsnivået vises med ikon ved siden av innloggingsvalget.

#### Hvordan lese eller laste ned rapporten?

Du finner rapporten ved å klikke på lenken i meldingen i innboksen på Altinn. Rapporten er tilgjengelig i tre format:

1. PDF-format som kan åpnes for lesing eller utskrift
2. CSV-fil som kan lastes ned og overføres til virksomhetens lønns- og økonomisystem. Du må åpne/laste ned filene for videre bruk i egen virksomhet. Når meldingen med vedlegget er åpnet, vil det bli registrert som om rapporten er lest eller lastet ned.

| Kolonne | Forklaring |
| --- | --- |
| A | Navenhet |
| B | Overordnet enhet |
| C | Underenhet |
| D | Ytelse |
| E | Fødselsnummer |
| F | Dato fra og med |
| G | Kontonummer |
| H | Navn |
| I | Dato til og med |
| J | Beløp |
| K | Ikke i bruk |
| L | Maksdato |
| Ytelseskode | Ytelse |
| 1 | Foreldrepenger adopsjon |
| 2 | Foreldrepenger fødsel |
| 3 | Svangerskapspenger |
| 4 | Sykepenger |
| 5 | Forsikret i arbeidsgiverperioden |
| 6 | Stort sykefravær |
| 7 | Gravide |
| 8 | Reisetilskudd |
| 9 | Pleiepenger |
| A | Trekk/Tilbakebetaling |
| Z | Omsorgspenger |
| Y | Opplæringspenger |
| Ytelseskode | Ytelse |
| E | Foreldrepenger adopsjon feriepenger |
| F | Foreldrepenger fødsel feriepenger |
| G | Svangerskapspenger feriepenger |
| H | Sykepenger feriepenger |
| I | Forsikret i arbeidsgiverperioden feriepenger |
| J | Stort sykefravær feriepenger |
| K | Gravide feriepenger |
| M | Opplæringspenger, Omsorgs- og pleiepenger feriepenger |

1. Gjennom API der din lønns – og personalleverandør må koble seg opp slik at rapporten leses direkte inn i ditt system.

#### Finner du ikke oppgjørsrapporten i innboksen i Altinn?

- Sjekk at riktig hovedenhet eller underenhet er valgt i «Rapporterer for»-feltet øverst på siden i Altinn.
- Sjekk at du har riktige tilganger i Altinn.
  - Den vanligste tilgangspakken for Oppgjørsrapport Arbeidsgiver - refusjoner fra Nav heter: Lønn med personopplysninger av særlig kategori.
  - [Mer informasjon om tilgangsstyring i Altinn](https://info.altinn.no/nyheter/enklere-tilgangsstyring-i-nye-altinn/).
- Hvis andre i virksomheten har sett på rapporten, kan den ligge som arkivert. Da finner du rapporten i arkivmappen i Altinn.
- Hvis andre i virksomheten har slettet rapporten, ligger den i Slettede elementer i Altinn.
- Hvis du har avsluttet en virksomhet og har fått refusjon, men ikke har fått oppgjørsrapport, så avvent og følg med i Altinn. Ta kontakt med Nav hvis rapporten ikke har dukket opp i Altinn innen midten av måneden.
  - Eksempel: Hvis du skulle fått rapporten 1. april, kan du vente til 15. april før du eventuelt kontakter Nav.
  - [Sjekk her hva du må gjøre hvis du omorganiserer](https://www.nav.no/arbeidsgiver/refusjon-underenhet).

Oppdatert 27.07.2026

---
*Automatisk hentet fra [NAV](https://www.nav.no/arbeidsgiver/oppgjorsrapport) av norges-lover-bot.*

## Endringshistorikk

- **2026-05-21** Første gang hentet
- **2026-06-03** Innhold endret (se git-historikk for diff)
- **2026-06-18** Innhold endret (se git-historikk for diff)
- **2026-07-28** Innhold endret (se git-historikk for diff)
- **2026-10-06** Innhold endret (se git-historikk for diff)
