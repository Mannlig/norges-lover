<!-- innholds-hash: 0fa9c87e4aac1e2f57a1a66b988e0cbc184144ca8fab765b04473f0fa590b956 -->

# Om statistikken - Sykepenger - nav.no

## Kildeinformasjon

- **Kilde:** NAV (Arbeids- og velferdsdirektoratet) – https://www.nav.no/no/nav-og-samfunn/statistikk/sykefravar-statistikk/relatert-informasjon/om-statistikken-sykepenger
- **Sist oppdatert i arkivet:** 2026-10-10T00:50:55Z

## Innhold

Publisert 14.11.2022 | Oppdatert 20.11.2025

## Om statistikken - Sykepenger

#### 1. Administrative opplysninger

#### 1.1. Navn og emnegruppe

Navn: Sykepengestatistikk

Emnegruppe: Sykefravær

Publiseres kvartalsvis [Se publiseringskalender for neste publisering](https://www.nav.no/no/nav-og-samfunn/statistikk/publiseringskalender)

#### 1.2. Ansvarlig

Ansvarlig: Arbeids- og velferdsdirektoratet, Statistikkseksjon

Felles informasjon: [Praksis, rutiner og retningslinjer rundt offisiell og offentlig statistikk fra Nav - nav.no](https://www.nav.no/no/nav-og-samfunn/kunnskap/data-og-forskning-pa-nav/praksis-rutiner-og-retningslinjer-rundt-offisiell-og-offentlig-statistikk-fra-nav) Personvernerklæring: [Personvernerklæring for Nav - nav.no](https://www.nav.no/personvernerklaering)

#### 2. Bakgrunn og formål

#### 2.1. Formål

Statistikken gir en oversikt over sykepengeutbetalinger totalt og fordelingen utover de ulike personlige kjennemerkene ved mottakerne. Den brukes blant annet som bakgrunnsmateriale i rapporter til Arbeid- og inkluderingsdepartementet, og som bidragsyter til statsbudsjettet. Sykepengefiler oversendes i tillegg til SSB som også lager statistikk på området.

#### 2.2. Om fagområdet

Statistikken gir en oversikt over sykepenger utbetalt av folketrygden (Nav), som kompensasjon for bortfall av arbeidsinntekt for arbeidstakere i en sykdomsperiode. Dette inkluderer ikke arbeidsgiverperioden, der de første 16 dagene av sykemeldingen dekkes av arbeidsgiver. Feriepenger av sykepenger er medregnet. Enkelte mottar sykepenger uten å ha arbeidsgiver, dette inkluderer selvstendig næringsdrivende og dagpengemottakere (sykmeldte arbeidssøkere).

Selvstendig næringsdrivende får vanligvis sykepenger fra dag 17. For sykefravær grunnet covid-19 ble dette fremskyndet til dag 6 (i tidsperioden fra 1.desember 2021 og ut juni 2022). For selvstendig næringsdrivende utgjør sykepengene 80 prosent av sykepengegrunnlaget. Selvstendig næringsdrivende og frilansere har ikke rett på feriepenger av sykepengene.

Tall på utbetalt beløp publiseres ikke offentlig, men kan tas ut ved eksterne forespørsler og eventuelle analyser. Kvartalsvis beløp bidrar også til en løpende kvalitetssikring av statistikken. Statistikken omfatter ikke ytelser utbetalt på grunn av sykt barn (pleiepenger). Pleiepenger for omsorg av sykt barn ble fjernet fra sykepengestatistikken fra 1.januar 2018 og har nå sin egen statistikk ([pleiepenger sykt barn](https://www.nav.no/no/nav-og-samfunn/statistikk/familie-statistikk/pleiepenger-sykt-barn)).

#### 3. Om produksjonen av statistikken, datakilder

#### 3.1 Datakilder og datainnsamling

Fra og med 1.kvartal 2020, hvor den nye vedtaksløsningen for utbetaling av sykepenger ble tatt i bruk, bygger dataene på en kombinasjon av Infotrygd og Navs nye vedtaksløsning for sykepenger. En slik kombinasjon gjorde det mulig å reetablere sykepengestatistikken. Nav planlegger for at flest mulig utbetalingssaker skal gå i den nye vedtaksløsningen i tiden fremover. På sikt planlegges det med at Infotrygd fases ut og at alle saker håndteres i ett system og dermed at det kun benyttes én kilde til sykepengedata.

#### 3.2. Hvordan statistikken er produsert

#### Retningslinjer for produksjon av statistikken

- Data om sykepengeutbetalinger hentes primært ut fra den nye vedtaksløsningen for sykepenger, men også noe hentes ut fra Infotrygd (gammel løsning).
- Data fra den nye vedtaksløsningen hentes inn via Kafka.
- Data fra Infotrygd omdannes til SAS-filer og legges deretter ut på en egen fil-server.
- Disse filene lastes manuelt til en historikk forkammer-tabell i datavarehuset. Historikk-tabellen inneholder sykpengestatistikk fra Infotrygd tilbake til 1989.
- Filene bearbeides og data fra de to kildene (ny vedtaksløsning og Infotrygd) slås sammen og lastes inn i basen. Nøkler til ulike dimensjoner blir lagt til (f.eks. alder, kjønn, diagnose, geografi og næring).
- Pseudonymiserte statistikkopplysninger lagres i datavarehus og en databank på tilgangsstyrt sikker filkatalog.
- Data aggregeres til sluttprodukter som tabeller og statistiske mål.
- Tabeller og aggregert informasjon publiseres på Nav.no.

#### 3.3. Feilkilder og usikkerheten i statistikken

#### Endringer i lovgivning, kilder og systemer

Grunnet endringer som har skjedd over tid er det ikke alle perioder som kan direkte sammenlignes eller må sees i forhold til hverandre med en viss forsiktighet. Se «punkt 5. Historikk og sammenlignbarhet over tid» for aktuelle endringer og brudd i statistikken.

#### Refusjoner og mulige differanser

Det tas hensyn til refusjon (minusbeløp), som kan redusere antall erstattede dager i kvartalet. Men det vil alltid være tilfeller der refusjonen skjer i kvartalet etter utbetalingen. Dermed blir refusjonen med i neste kvartal. Netto antall sykepengedager vil da bli noe feil, men dette utgjør sjelden mye og er vanskelig å forhindre.

I motsetning til tapte dagsverk for sykefravær tar sykepengedager ingen hensyn til sykmeldingsgrad og stillingsprosent. Sykepengedager blir dermed mye høyere og kan ikke sammenlignes med tapte dagsverk.

I de ulike rapportene kan det forekomme små differanser, både i antall sykepengetilfeller og sykepengedager. Dette skyldes i hovedsak bruk av ulik kilde til oppbygning av de forskjellige rapportene. Ønsker man de overordnede offisielle tallene er rapporten SYKP510 (Antall sykepengedager og -tilfeller etter bosted. Kvartal) den sikreste kilden.

#### Manglende mulighet til å sammenligne

Det er ikke brukt noen nevner i statistikken. Dette gjør at man ikke direkte kan sammenligne tall i de ulike grupperingene (f.eks. antall sykepengedager i de ulike fylkene). Det er heller ikke foretatt noen vekting av tallene for bl.a. å ta hensyn til at det i et fylke er mange innbyggere sammenlignet med et mindre fylke med færre innbyggere. Antall innbyggere vil følgelig gi utslag på både sykepengedager, -tilfeller og utbetalt beløp. Ønsker man å sammenligne de ulike fylkene vil dermed sykefraværsstatistikken gi en bedre indikasjon.

#### 3.4. Publisering og produksjonstid

Det publiseres kvartalsvis sykepengestatistikk, som deles inn i periodene 1.januar-31.mars (1. kvartal), 1.april-30.juni (2.kvartal), 1.juli-30.september (3.kvartal), og fra 1.oktober-31.desember (4.kvartal). Det publiseres også årlig statistikk samtidig som 4.kvartal fra det foregående året publiseres.

Statistikkregistrene for sykepenger dannes månedlig og legger grunnlaget for kvartals- og årsfiler. Den publiserte statistikken viser antall sykepengedager, sykepengetilfeller, samt sykepengetilfeller med oppbrukt sykepengerett. Det gis fordelinger etter kjønn, alder, bosted, diagnose og næring.

#### 4. Begreper, kjennemerker og grupperinger

#### 4.1. Definisjoner av sentrale begreper

Sykepengetilfelle: Ethvert tilfelle av utbetalte sykepenger, uavhengig av varighet. Ved et opphold mellom sykmeldingene, kan samme person ha flere sykepengetilfeller innenfor samme kvartal. Et sykepengetilfelle er basert på at penger er utbetalt fra Nav, ikke på perioden som sykmeldingen dekker.

Sykepengedag: Dager som er erstattet av folketrygden. Både utbetaling og refusjon av sykepenger kan skje i kvartalet etter at sykefraværet med tilhørende sykepengedager fant sted. Refusjon og utbetaling har følgelig betydning for netto antall sykepengedager i kvartalet. Sykepengedager er ikke det samme som tapte dagsverk.

Oppbrukt sykepengerett: Tilfeller der siste utbetaling av sykepenger skjer på eller etter maksdato og maksdatoen er i kvartalet. Et sykepengetilfelle med oppbrukt sykepengerett tilsvarer dermed en person som har passert maksdato og må tjene opp ny rett til sykepenger (som krever 26 uker med sammenhengende arbeidsførhet). Perioder tre år tilbake i tid blir lagt sammen hvis det er mindre enn 26 uker mellom noen av sykepengeperiodene. Et sykepengetilfelle med oppbrukt sykepengerett vil dermed ikke nødvendigvis si at personen har fått sykepenger sammenhengende (52 uker) fram til maksdato.

#### Andre kjennetegn i statistikken

• Kjønn • Aldersgruppering: 16-19 år, 5 års aldersgrupper til og med 69 år • Næring er kodet etter Standard for næringsgruppering • Bostedsfylke er avledet fra bostedskommune • Diagnose er kodet etter standarden ICPC

#### Diagnosekoder

Diagnose settes av lege og sendes til Nav på skjema 'Vurdering av arbeidsmulighet/Sykmelding' når en person sykmeldes. De fleste sendes inn elektronisk til Nav. Diagnosene er kodet etter standarden ICPC, versjon 2 (“The International Classification of Primary Care”). ICPC er den internasjonale klassifikasjonen for helseproblemer, diagnoser og andre årsaker til kontakt med primærhelsetjenesten. Denne standarden brukes også ved søknad om arbeidsavklaringspenger.

Diagnosekodene er organisert etter organkode (bokstav), og en tallkode for den spesifikke diagnosen. Tallkodene er fordelt i «symptomer og plager» (kodenummer 1-29), «sykdomsdiagnoser» (kodenummer 70-99) og «prosesskoder» (kodenummer 30-69). En oversikt over de ulike diagnosekodene er tilgjengelig hos [Direktoratet for e-helse](https://www.helsedirektoratet.no/standarder/icpc-2-den-internasjonale-klassifikasjonen-for-primaerhelsetjenesten) som er ansvarlig for kodesystemet i Norge.

#### 4.2. Målevariable

• Antall sykepengetilfeller • Antall sykepengedager • Antall sykepengetilfeller med oppbrukt sykepengerett

#### 5. Feilkilder og svakheter i statistikken

#### 5.1. Historikk

Sykepengestatistikken ble publisert på nav.no for første gang i 2006 med tall tilbake fra og med 4.kvartal 1996. Før dette ble sykepengestatistikk publisert i Trygdestatistisk årbok.

#### 5.2. Sammenlignbarhet over tid/endringer

Statistikken ble reetablert fra og med 1.kvartal 2020. Ved behov for sykepengestatistikk fra før 2020 ligger dette tilgjengelig i arkiv på nav.no, men denne kan ikke nødvendigvis sammenlignes med den reetablerte sykepengestatistikken, grunnet endring av kilde. I den nye statistikken fra 2020 publiserer vi også flere detaljer enn hva vi gjorde tidligere, deriblant diagnoser.

Ettersom statistikken fikk en ny oppstart fra 2020 har vi foreløpig ikke det store sammenligningsgrunnlaget i den nye statistikken. Sammenligningsgrunnlaget vil bli større over tid.

#### Ny næringsstruktur fra 2009

Fra og med publiseringen for 1. kvartal 2009 benyttes en ny næringsstandard (SN2007). Sammenlignet med publiserte tall med gammel standard (SN2002) for 2008 og tidligere år vil det være et brudd i tidsserien for næringsfordelte tall.

I SN2007 benyttes i stor grad samme betegnelser på næringer som i den gamle standarden (SN2002). Men det ble blant annet laget en ny hovednæring, «Informasjon og kommunikasjon», som omfattet virksomheter som tidligere var i ulike andre næringer. Les mer om [endring i næringsstruktur](https://www.nav.no/no/nav-og-samfunn/statistikk/sykefravar-statistikk/sykefravar/om-statistikken-sykefravaer#chapter-5) her.

En ny standard for næringsgruppering for virksomheter, ble tatt i bruk i Norge fra 1. september 2025 (SN2025). Se mer om endringen hos SSB: [Ny standard for næringsgruppering innføres 1. september 2025 – SSB](https://www.ssb.no/virksomheter-foretak-og-regnskap/metoder-og-dokumentasjon/ny-standard-for-naeringsgruppering-innfores-1.september-2025).

Nav presenterer inntil videre sykepengestatistikk fordelt på gammel næringsstandard (SN2007). Det vil i praksis si at sykepengestatistikken viser næringskategoriseringen slik den var i august 2025, før ny standard ble innført fra september 2025. Nav har ikke besluttet når sykepengestatistikken endres til Standard for næringsgruppering 2025 (SN2025), men vil informere når dette skjer.

---
*Automatisk hentet fra [NAV](https://www.nav.no/no/nav-og-samfunn/statistikk/sykefravar-statistikk/relatert-informasjon/om-statistikken-sykepenger) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-10** Første gang hentet
