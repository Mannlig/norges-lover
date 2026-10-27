<!-- innholds-hash: e985e0bb3c52ae116293d73df36f680af8d2805d7f967245b40188e1876d1f3b -->

# Rettledning for utfylling og innlevering av tredjepartsopplysninger om livsforsikring

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/bank-finans-og-forsikring/livsforsikring/rettledning/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-27T14:11:27Z

## Innhold

## Rettledning for utfylling og innlevering av tredjepartsopplysninger om livsforsikring

### Kort om ordningen

Denne rettledningen gjelder kapitalforsikringer som ikke omfattes av fondskontoordningen: kapitalforsikringer med sparing, livrenter og livsforsikringsprodukter med garantert avkastning.

Kapitalforsikringer der forsikringselementet utgjør mindre enn 50 prosent, skal rapporteres i ordningen Fondskonto. Se [rettledningen for Fondskonto](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/bank-finans-og-forsikring/fondskonto/).

### Opplysningsplikten

#### Hvem er opplysningspliktig

Opplysningsplikten etter denne tredjepartsordningen omfatter virksomheter som nevnt i [skatteforvaltningsloven § 7-3 første ledd](https://lovdata.no/lov/2016-05-27-14/%C2%A77-3) med tilhørende [forskrift](https://lovdata.no/forskrift/2016-11-23-1360/%C2%A77-3-1).

#### Reelle rettighetshavere

Opplysningsplikten omfatter reelle rettighetshavere som er skattemessig bosatt i Norge eller i utlandet, og/eller som er amerikanske statsborgere. En reell rettighetshaver kan være skattemessig bosatt i flere land. Da gjelder opplysningsplikten for hvert av disse landene. Opplysningsplikten omfatter også reelle rettighetshavere i selskap mv. Reelle rettighetshavere som er skattemessig bosatt i Norge, skal inkluderes i ordningen Livsforsikring når foretak er polisehaver og vilkårene i skatteforvaltningsforskriften § 7-3-22 tredje ledd er oppfylt. Reelle rettighetshavere som er skattemessig bosatt utenfor Norge, skal rapporteres via tredjepartsordningen Internasjonal rapportering CRS/FATCA.

#### Registrering i oppgavegiverregisteret

For å rapportere til grunnlagsdataordningen må opplysningspliktige registrere seg i Skatteetatens oppgavegiverregister via skjema [Tredjepartsopplysninger – nye opplysninger til oppgavegiverregisteret](https://www.altinn.no/skjemaoversikt/skatteetaten/tredjepartsopplysninger---nye-opplysninger-til-oppgavegiverregisteret-/). Kontaktopplysningene må til enhver tid være oppdaterte. Skatteetaten bruker dem blant annet til å sende viktig informasjon og invitere til dialogmøter.

#### Internasjonal rapportering

Finansielle konti og forsikringsforhold som skal rapporteres til utveksling etter CRS og FATCA, skal rapporteres i ordningen [Internasjonal rapportering CRS/FATCA](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/bank-finans-og-forsikring/internasjonal-rapportering/rettledning/). Se rettledningen for tredjepartsordningen Internasjonal rapportering CRS/FATCA for nærmere veiledning.

### Levere tredjepartsopplysninger

#### Maskin-til-maskin-rapportering (M2M)

Tredjepartsopplysninger kan sendes direkte fra sluttbrukersystemet til Skatteetaten med maskin-til-maskin-integrasjon (M2M). Opplysningene kan leveres i JSON-format eller som XML-fil, avhengig av hvilken løsning og ordning som benyttes. Dette krever at systemet er koblet til Skatteetatens mottaks-API med en systembruker.

XML-baserte leveranser er særlig aktuelle for virksomheter som rapporterer større datamengder, og som ønsker å sende inn opplysninger direkte fra egne fagsystemer. XML-filen må være bygget opp i samsvar med gjeldende informasjonsmodell, formatbeskrivelse (XSD) og tekniske krav for den aktuelle ordningen.

Les mer om Skatteetatens API-er i [API-dokumentasjonen](https://skatteetaten.github.io/api-dokumentasjon/) og [TPO filmottak API (XML)](https://skatteetaten.github.io/api-dokumentasjon/api/innrapportering-tpo-filmottak).

#### Vedleggskjema

Tredjepartsopplysninger kan leveres som XML-filvedlegg via skjemaet [Tredjepartsopplysninger som vedlegg](https://www.skatteetaten.no/skjema/tredjepartsopplysninger-som-vedlegg/). Filen som lastes opp, skal være i XML-format og følge Skatteetatens spesifikasjoner.

#### Beskrivelse av filformatet

Formatbeskrivelsen viser hvordan maskin-til-maskin-leveranser (JSON) og XML-fil for rapportering av tredjepartsopplysninger for livsforsikring skal bygges opp. Dokumentene finner du ved å følge denne lenken:

[Formater og tekniske spesifikasjoner – Livsforsikring](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/bank-finans-og-forsikring/livsforsikring/formater-og-tekniske-spesifikasjoner/)

Formatbeskrivelsen skal brukes av opplysningspliktige og innsendere som rapporterer tredjepartsopplysninger via maskin-til-maskin (JSON) eller vedleggsskjema (XML).

#### Identifisere oppgaver

En leveranse består av én eller flere oppgaver. Oppgavene skilles fra hverandre ved hjelp av feltene «inntektsår», «opplysningspliktig», «oppgaveeier» og «forsikringsnummer». Disse feltene utgjør til sammen oppgavens unike identifikator.

#### Opplysningspliktig

- Opplysningspliktige identifiseres ved organisasjonsnummer.

#### Oppgaveeier (den som står som eier av forsikringen)

- Oppgaveeier identifiseres ved fødselsnummer, D-nummer eller organisasjonsnummer. Dersom oppgaveeier ikke har fødselsnummer eller organisasjonsnummer, må den opplysningspliktige vurdere om forholdet også skal rapporteres til tredjepartsordningen [Internasjonal rapportering CRS/FATCA](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/bank-finans-og-forsikring/internasjonal-rapportering/rettledning/)for utveksling.

#### Forsikringsnummer

- Nummer som identifiserer forsikringen.

#### Korrigere oppgaver

Du korrigerer en tidligere innsendt oppgave ved å rapportere en ny oppgave med samme verdier i identifikatorfeltene. Den nye oppgaven erstatter den tidligere oppgaven.

#### Korrigere oppgave med feil identifikator

Hvis ett eller flere identifikatorfelt er feil i en tidligere innsendt oppgave, må oppgaven slettes. Da må du sende inn en ny oppgave med riktige verdier og en sletteoppgave for å slette oppgaven med feil identifikator. Sletteoppgaven må ha de samme identifikatorene som oppgaven med feil identifikator.

### Forsikringstyper

#### Hvilken type forsikring oppgaven gjelder

Ordningen omfatter kapitalforsikring med sparing (forsikringstype «Kapitalforsikring med sparing»), individuelle livrenter (forsikringstype «Individuelle livrenter») og kontobasert kapitalforsikring (forsikringstype «Kontobasert kapitalforsikring»). Se også «Gjeldende forsikringstyper».

#### Kapitalforsikring med sparing

Kapitalforsikring med sparing rapporteres med forsikringstype «Kapitalforsikring med sparing».

Investering i aksjer og andre verdipapirer gjennom kapitalforsikring, der forsikringselementet er lite, skal skattlegges som investering i verdipapirfond og rapporteres i ordningen [Fondskonto](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/bank-finans-og-forsikring/fondskonto/).

#### Gjenkjøpsverdi

Gjenkjøpsverdien per 1. januar året etter inntektsåret er skattepliktig formue og skal rapporteres. Ved en eventuell utbetaling skal forskuddstrekket betales direkte til Skatteetaten og inngår ikke i beregningen av gjenstående gjenkjøpsverdi. Hvis gjenkjøpsverdien er negativ, skal beløpet rapporteres som 0. Eventuell andel av tilleggsavsetninger og kursreserve skal ikke tas med.

Gjenkjøpsverdien skal deles likt på eierne når det er to eller flere eiere.

#### Avkastning

Den beregnede årlige avkastningen på sparedelen av en kapitalforsikring med garantert avkastning skal rapporteres. Hvis samlet årlig avkastning i selskapet er under kr 300, har selskapet ikke plikt til å rapportere beløpet, jf. forskrift til skatteloven (FSFIN) § 5-20-12 andre ledd bokstav b. Avkastningen skal deles likt mellom eierne når det er to eller flere eiere.

Se også «Kontobasert kapitalforsikring».

#### Individuell livrente

#### Gjenkjøpsverdi

Individuelle livrenter skal rapporteres med forsikringstype «Individuelle livrenter». Gjenkjøpsverdien per 1. januar året etter inntektsåret er skattepliktig formue og skal rapporteres. Hvis det ikke finnes opplysninger om livrentens gjenkjøpsverdi, må verdien fastsettes ved skjønn.

#### Avkastning

Avkastning på individuelle livrenter skal rapporteres ved utbetaling.

#### Kontobasert kapitalforsikring

Kontobasert kapitalforsikring skal rapporteres med forsikringstype «Kontobasert kapitalforsikring».

#### Gjenkjøpsverdi

Gjenkjøpsverdi per 1. januar året etter inntektsåret er skattepliktig som formue og skal rapporteres.

#### Avkastning

Den beregnede årlige avkastningen på sparedelen av en kapitalforsikring med garantert avkastning skal rapporteres. Hvis samlet årlig avkastning i selskapet er under kr 300, har selskapet ikke plikt til å rapportere beløpet, jf. forskrift til skatteloven (FSFIN) § 5-20-12 andre ledd bokstav b. Avkastningen skal deles likt mellom eierne når det er to eller flere eiere.

Hvis en konto avsluttes i løpet av året, skal opptjente renter fram til avslutningsdatoen rapporteres som skattepliktig avkastning. Det samlede beløpet som blir utbetalt, rapporteres i utbetalingsformatet. Se også «Utbetalt beløp».

#### Skattetrekk

Eventuelt skattetrekk i den årlige avkastningen skal ikke rapporteres i denne oppgaven, men i a-meldingen.

### Utbetalinger på livsforsikring (utbetalingsformatet)

Bestemmelsene i FSFIN § 5-41 om beregning av skattepliktig inntekt av livrente gjelder så langt de passer for livrente som er tegnet etter lov om individuell pensjonsordning av 27. juni 2008 nr. 62 § 5-3. Ved rapporteringen må det derfor skilles mellom utbetalinger fra individuell pensjonsforsikringsavtale etter skatteloven (IPA) og utbetalinger fra ny individuell livrenteavtale. Utbetalinger fra IPA-avtalen skattlegges fullt ut som pensjonsinntekt, med unntak av uføreytelser som skattlegges som lønnsinntekt. Utbetalinger fra IPA-avtaler skal rapporteres i a-meldingen.

Med utbetalinger i denne forbindelse menes utbetalinger fra livsforsikringsselskaper, unntatt pensjoner og kollektive livrenter (livrenter i arbeidsforhold).

#### Hvem beløpet er utbetalt til

Den som mottar beløpet, skal identifiseres med fødselsnummer, D-nummer eller organisasjonsnummer. Ett av disse numrene må alltid oppgis for at fastsettingen skal bli korrekt.

Hvis beløpet utbetales til en annen enn forsikringstaker, skal du også oppgi navn og identifikasjonsnummer (fødselsnummer, D-nummer eller organisasjonsnummer) til forsikringstaker i feltet «forsikringstaker». Ved utbetaling til dødsbo skal forsikringstakers navn og fødselsnummer oppgis.

Ved utbetaling av gruppelivsforsikring tegnet av arbeidsgiver, når beløpet utbetales til gjenlevende ektefelle eller barn, skal beløpet rapporteres på mottakeren. I tillegg skal arbeidsgiver oppgis som forsikringstaker med organisasjonsnummer. Det samme gjelder ved utbetaling av livsforsikring som arbeidsgiver har tegnet og betalt til fordel for arbeidstaker, medeier, aksjonær eller deres nærmeste familie.

NB! Unntak fra hovedregelen Hvis gjeldsforsikring utbetales direkte til en bank, skal forsikredes (avdødes) navn og fødselsnummer oppgis som den beløpet er utbetalt til. I tillegg skal bankens navn og organisasjonsnummer oppgis som forsikringstaker.

### Gjeldende forsikringstyper

Oppgaven gjelder for følgende typer forsikringer:

| Verdifelt: <forsikringstype></forsikringstype> | Beskrivelse |
| --- | --- |
| kapitalforsikringMedSparing | Kapitalforsikring med sparing |
| gjeldsforsikring | Gjeldsforsikring |
| gruppelivsforsikring | Gruppelivsforsikring (individuell og kollektiv) |
| individuellRisikoforsikring | Individuell risikoforsikring |
| individuelleLivrenter | Individuelle livrenter |
| ufoererenter | Uførerenter |
| kontobasertKapitalforsikring | Kontobasert kapitalforsikring |

Kontobasert livrente likestilles med vanlig livrente (forsikringstype «Individuelle livrenter»).

Om kombinasjoner av forsikringstyper og utbetalingstyper, og hvilke som er skattepliktige eller skattefrie, se oversikten «Kombinasjoner av forsikrings- og utbetalingstyper».

#### Utbetalingstyper

Oppgaven gjelder for følgende utbetalingstyper:

| Verdifelt: <utbetalingstype></utbetalingstype> | Beskrivelse |
| --- | --- |
| engangsutbetalingDoed | Engangsutbetaling, død |
| engangsutbetalingUfoerhet | Engangsutbetaling, uførhet |
| engangsutbetalingAlder | Engangsutbetaling, alder |
| engangsutbetalingGjenkjoep | Engangsutbetaling, gjenkjøp |
| renterAvLivsforsikring | Renter av livsforsikring |
| terminutbetalingLivrente | Terminutbetaling, livrente |
| terminutbetalingUfoererente | Terminutbetaling, uførerente |

Når det i løpet av året bare er foretatt én à konto-utbetaling, skal beløpet rapporteres med den utbetalingstype som utbetalingen hører hjemme under.

Om kombinasjoner av utbetalingstyper og forsikringstyper, og hvilke som er skattepliktige eller skattefrie, se oversikten «Kombinasjoner av forsikrings- og utbetalingstyper».

#### Kombinasjoner av forsikrings- og utbetalingstyper

Se følgende dokument for gyldige kombinasjoner av forsikrings- og utbetalingstyper.

[Oversikt over kombinasjoner av forsikrings- og utbetalingstyper](https://www.skatteetaten.no/contentassets/d01374b0abbc423a9789dde6ffaa94fe/kombinasjon-av-forsikring-og-utbetalingstype.pdf)

#### Utbetalt beløp

Alle utbetalinger skal rapporteres, også den skattefrie delen av livrenter og uførerenter. Skattepliktige beløp skal oppgis før eventuelt skattetrekk. Beløpet oppgis i hele kroner.

Hvis en utbetaling består av både skattepliktig og skattefritt beløp, kan dette rapporteres i samme oppgave. Det trenger ikke være samme utbetalingstype. Hvis det for eksempel utbetales «Engangsutbetaling, uførhet» og i tillegg renter, kan dette rapporteres i samme oppgave.

Individuelle livrenter skal rapporteres ved skattepliktig utbetaling eller når det foreligger fradragsberettiget tap. Ved gjenkjøp (innløsning) av livrenter før vilkåret om minste forsikringstid er oppfylt, skal «tilleggsskatten» på en åttendedel av gjenkjøpsverdien, jf. FSFIN § 5-41-8 andre ledd, føres i elementet med utbetalingstype «Engangsutbetaling, gjenkjøp».

Ved rapportering av fradragsberettiget tap på individuelle livrenter skal det ikke rapporteres negative beløp i feltet «skattepliktig beløp», slik som i tidligere format. Gevinst eller tap skal oppgis som positivt beløp i egne utbetalingstyper.

Utbetaling skal bare rapporteres når en kontobasert kapitalforsikring opphører. Da skal hele beløpet rapporteres, både det som står på kontoen og det som gjelder forsikringsdekningen. Vanlige uttak i løpet av året skal ikke rapporteres. Opptjente renter skal rapporteres som skattepliktig avkastning med forsikringstype «Kontobasert kapitalforsikring».

### Fortsettelsesforsikring i kollektiv pensjonsforsikring etter opphør av arbeidsforhold

Etter forsikringsavtaleloven § 19-7 kan en skattepliktig fortsette forsikringsforholdet med individuell premieberegning når vedkommende avslutter et arbeidsforhold og trer ut av gruppen som forsikringen omfatter. Forsikringen kalles fortsettelsesforsikring.

Løpende utbetalinger fra fortsettelsesforsikring skal rapporteres i a-meldingen. Bestemmelsene i FSFIN § 5-41 om beregning av skattepliktig inntekt gjelder så langt de passer for livrente som er tegnet som fortsettelsesforsikring etter lov om foretakspensjon § 4-9, og for livrente som er tegnet etter overgangsbestemmelsen i FSFIN § 6-47-41.

Det vises til [veiledningen til a-meldingen](https://www.skatteetaten.no/a-meldingen/).

Overgangsreglene står i FSFIN § 6-47-40. De gjelder for avtaler om fortsettelsesforsikring som er inngått før 1. januar 2007.

FSFIN § 6-47-40 gir rettighetshaver rett til å få utbetalt samlede innestående midler dersom vilkårene i bestemmelsen er oppfylt. Rettighetshaver som har brukt denne adgangen, må ha sendt skriftlig melding til selskapet innen 31. desember 2010.

#### Innestående beløp på premiefond

Innestående beløp på premiefond i fortsettelsesforsikring ved utgangen av inntektsåret skal rapporteres i feltet «innestående på premiefond». Beløpet skal inkludere renter for siste år. Beløpet skal rapporteres selv om det ikke har vært innbetalinger i løpet av inntektsåret.

### Temahenvisninger til skattemeldingen

Tredjepartsopplysningene brukes til forhåndsutfylling av skattemeldingen.

Skattemeldingen er temabasert. Opplysningene fra denne tredjepartsordningen vises under tema og undertema i skattemeldingen. Tabellen nedenfor viser hvor opplysningene normalt vises. Les mer om skattemeldingen på Skatteetatens nettsider.

| Opplysning | Tema | Undertema |
| --- | --- | --- |
| Livrenter utenfor arbeidsforhold (engangsutbetaling) | Bank, lån og forsikring | Livsforsikring |
| Uførerenter 20 % av terminbeløpet | Bank, lån og forsikring | Livsforsikring |
| Utbetalt skattepliktig beløp (individuell livrente) | Bank, lån og forsikring | Livsforsikring |
| Renteinntekter av livsforsikring | Bank, lån og forsikring | Livsforsikring |
| Avkastning/gevinst på kapitalforsikring | Bank, lån og forsikring | Skattepliktig formuesverdi av kapitalforsikringsavtale |
| Tap på kapitalforsikring | Bank, lån og forsikring | Livsforsikring |
| Innestående på premiefond (fortsettelsesforsikring) | Bank, lån og forsikring | Livsforsikring |
| Gjenkjøpsverdi av individuell livrenteforsikring | Bank, lån og forsikring | Livsforsikring |
| Formue kapitalforsikring | Bank, lån og forsikring | Skattepliktig formuesverdi av kapitalforsikringsavtale |

### Aktuelt regelverk

- Skatteforvaltningsloven § 7-3 første ledd
- Skatteforvaltningsforskriften § 7-3
- Skatteloven § 5-20 andre ledd
- Finansdepartementets forskrift til skatteloven av 26. mars 1999 nr. 14 (FSFIN) § 5-20-12 andre ledd bokstav b
- Skatteloven § 5-41, jf. FSFIN § 5-41
- Lov om individuell pensjonsordning av 27. juni 2008 nr. 62 § 5-3
- Forsikringsavtaleloven § 19-7
- Lov om foretakspensjon § 4-9

#### Ingen dispensasjonsadgang ved opplysningsplikt

Skatteetaten kan ikke gi den enkelte opplysningspliktige dispensasjon fra opplysningsplikten. Tredjepartsopplysninger som ikke er levert innen fristen kan som hovedregel ilegges tvangsmulkt.

#### Tvangsmulkt ved for sent eller ikke leverte oppgaver

Opplysningspliktige som ikke har levert oppgaver innen fristen, kan ilegges tvangsmulkt, jf. skatteforvaltningsloven § 14-1

Opplysninger anses ikke levert når de:

- er helt uteblitt
- Ikke er sendt elektronisk, men er sendt eller levert til lokalt skattekontor
- mangler 11-sifret fødselsnummer eller D-nummer for personlige skattepliktige
- mangler 9-sifret organisasjonsnummer
- mangler fullt navn, adresse og landkode til personer som ikke er tildelt fødsels- eller organisasjonsnummer
- er levert på en måte som ikke følger Skatteetatens bestemmelser

Vedtak om tvangsmulkt sendes ut noen dager etter ordinær frist med orientering om at mulkt vil løpe fra en bestemt fremtidig dato hvis opplysningene ikke blir levert. Tvangsmulkten utgjør ett halvt [rettsgebyr](https://www.skatteetaten.no/satser/rettsgebyr/) per dag opplysningene uteblir og opp til 50 rettsgebyr.

Du unngår tvangsmulkt ved å levere opplysningene innen den nye fristen som er gitt i vedtaket. Da starter ikke den varslede tvangsmulkten å løpe.

#### Oppdatering av kontaktopplysninger

Skatteetatens oppgavegiverregister henter opplysningspliktiges organisasjonsnavn og adresse automatisk fra Enhetsregisteret i Brønnøysund. Det er derfor viktig at disse opplysningene til enhver tid er oppdatert. Dette gjøres ved å fylle ut [samordnet registermelding](https://www.altinn.no/skjemaoversikt/bronnoysundregistrene/samordnet-registermelding---registrering-av-nye-og-endring-av-eksisterende-foretak-og-enheter/).

Skatteetaten sender ut informasjonsbrev og vedtak til opplysningspliktige elektronisk i innboks på altinn.no eller innboks hos Skatteetaten.no. De som skal motta varsel om nye meldinger i innboksene på vegne av virksomheten, må registrere e-postadresse og mobilnummer for SMS i Altinn. Fyll ut «Din kontaktinformasjon for virksomheten» og «Varslingsadresser for virksomheten» under virksomhetens «Profil» i Altinn.

Endringer i Skatteetatens oppgavegiverregister om kontaktinformasjon, dvs. navn og telefon-/mobilnummer og e-postadresse til kontaktperson i forbindelse med innsending av tredjepartsopplysninger, kvitteringer og feilmeldinger, må meldes til Skatteetaten på skjema: [RF-1312 Nye opplysninger til oppgavegiverregisteret – tredjepartsopplysninger](https://www.skatteetaten.no/skjema/tredjepartsopplysninger---nye-opplysninger-til-oppgavegiverregisteret/).

### Kontaktinformasjon for leveransen

Ved innsending må du oppgi kontaktinformasjon for leveransen, dvs. navn og telefonnummer for kontaktperson for den spesifikke leveransen. Du bør i tillegg oppgi en e-postadresse og et mobilnummer hvor varsel (SMS) om meldinger (kvitteringer/feilmeldinger) kan sendes.

### Tilbakemelding fra Skatteetaten

Den opplysningspliktige får en tilbakemelding i innboksen på skatteetaten.no når Skatteetaten har behandlet opplysningene. Har du oppgitt mobilnummer eller e-post i innsendingen, får du varsel på SMS/e-post når tilbakemeldingen har kommet.

Det er viktig at du kontrollerer tilbakemeldingen ved mottak, slik at eventuelle feil i de innleverte oppgavene kan rettes opp snarest mulig. Har du ikke mottatt tilbakemeldingen innen et par dager, må du kontakte oss på e-post: grunnlagsdata@skatteetaten.no

### Feil på innsendte leveranser

Leveranser som er avvist vil vises på tilbakemelding og feilliste. Avviste leveranser kan skyldes at det er for mange feil eller avvik på innsendte oppgaver, eller at oppgitt leveransetype på leveransen er feil eller mangler. Det er derfor viktig at du setter deg inn i hvordan korreksjoner rapporteres. Ta kontakt for å avklare fremgangsmåte for å korrigere feil hvis du er usikker.

### Annullering av leveranser

Dersom du har behov for å annullere en leveranse, må Skatteetaten kontaktes.

### Testing

For å avdekke mulige feil slik at selve rapporteringen blir mest mulig korrekt, anbefaler Skatteetaten at opplysningspliktig sender inn testoppgaver. Les mer om [innsending av testoppgaver her](https://www.skatteetaten.no/no/Bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/Testinnsending-xml/).

### Roller og rettigheter

Når du skal sende inn tredjepartsopplysninger må du ha tilgang på vegne av virksomheten du skal rapportere for. For å logge inn på Skatteetaten.no må du ha et norsk fødselsnummer eller D-nummer.

For å fylle ut og sende inn skjemaet må du ha en av disse tilgangspakkene, eller tilgang via enkelttjenestedelegering.

- Ansvarlig revisor
- Regnskapsfører med signeringsrett
- Regnskapsfører uten signeringsrett
- Revisormedarbeider
- Skattegrunnlag
- [Enkelttjenestedelegering](https://info.altinn.no/hjelp/ny-tilgangsstyring/enkelttjenester/) må gjøres på nytt for de nye skjemaene.

Hvis tilgangen til Altinn II-skjemaet var gjort med direkte tjenestedelegering, det vil si tilgang uten rolle eller pakke, må tilgangen delegeres på nytt.

Hvis du ikke har noen av disse rollene, må du kontakte en person i virksomheten din som kan administrere tilganger i Altinn.

Kontakt [Altinn brukerservice](https://www.altinn.no/hjelp/) hvis du har problemer med tilganger.

### Innhenting av fødsels- og organisasjonsnummer

Dersom du som opplysningspliktig har behov for å innhente fødselsnummer eller D-nummer fra andre enn eier, må du sende en skriftlig og begrunnet søknad til skattekontoret. Du kan kostnadsfritt få utlevert inntil 4 opplysninger per uke.

Har du en lengre liste med opplysninger du ønsker å få utlevert, må du betale for å få opplysningene. Omfatter forespørselen mer enn 4 personer, skal den sendes til:

Skatteetaten Postboks 9200 Grønland 0134 Oslo

Du kan også bruke vårt [kontaktskjema](https://www.skatteetaten.no/skjema/rf-1306-kontaktskjema-skatteetaten-bedrift/).

Organisasjonsnummer kan innhentes hos:

Brønnøysundregistrene Enhetsregisteret Postboks 900 8910 Brønnøysund [www.brreg.no](https://www.brreg.no/)

### Tildeling av D-nummer

Tildeling av D-nummer er regulert i forskrift 14. juli 2017 nr. 1201 til folkeregisterloven. Det kommer frem av forskriften hvem som fysisk kan tildeles et D-nummer og hvem som kan rekvirere D-nummer, se [§ 2-2-3](https://lovdata.no/SF/forskrift/2017-07-14-1201/%C2%A72-2-3) og [§ 2-2-4](https://lovdata.no/SF/forskrift/2017-07-14-1201/%C2%A72-2-4)

Skattepliktige som ikke har/kan få fødselsnummer skal ha D-nummer. De skattepliktige kan henvende seg til spesifikke skattekontor for tildeling av D-nummer. For mer informasjon om fremgangsmåten for å rekvirere D-nummer, se [her.](https://www.skatteetaten.no/person/folkeregister/identitetsnummer-og-elektronisk-id/d-nummer/)

### Årsoppgave til skattepliktig

Den skattepliktige skal ha kopi av de opplysningene som er sendt til Skatteetaten innen 15. februar året etter inntektsåret. Det skal alltid komme frem av årsoppgaven at opplysningene også er sendt skattemyndighetene.

Det er ikke gitt spesielle formkrav til årsoppgaven, men den skal inneholde de samme opplysninger om identifikasjon og oppgitte beløp som er gitt til Skatteetaten.

Tredjepartsopplysningene brukes i produksjon av skattemeldingen. I den nye skattemeldingen er poster erstattet med temaer.

Årsoppgaven skal inneholde:

- navn og fødselsnummer/organisasjonsnummer på skattepliktig
- navn og organisasjonsnummer på den opplysningspliktige
- oversikt over rapporterte opplysninger om skattepliktig
- melding om at opplysningene også er sendt til Skatteetaten
- temahenvisning til skattemeldingen

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/bank-finans-og-forsikring/livsforsikring/rettledning/) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-27** Første gang hentet
