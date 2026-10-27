<!-- innholds-hash: 8d1262533c3bb2b5f808e986f183aa8bf62a6b90aaf90e8fbcd2cd60abf81b4b -->

# Jurisdiction Section

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/jurisdiction-section/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-27T13:14:14Z

## Innhold

## Jurisdiction Section

Bruk OECD veiledningene sammen med våre presiseringer for å unngå feil eller merknader i Jurisdiction Section når du skal sende inn melding for suppleringsskatt (GIR) til oss. Veiledning for utfylling av XML-filen følger av OECDs XML Schema User Guide s. 41-125.

Jurisdiction Section inneholder detaljerte opplysninger om beregninger på land og virksomhetsnivå.

Jurisdiction Section skal fylles ut i overensstemmelse med XML Schema User Guide, se s. 41-125. Dette gjelder også der XML-filen ikke er ment for utveksling ([sentralisert levering](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/sentralisert-levering/)).

Kravene til hvilken informasjon som må inngå i melding for suppleringsskatt (GIR) for at virksomheten har oppfylt sine opplysningsplikter vil avhenge av en rekke faktorer, herunder hvilke land som har beskatningsrett. Egne krav gjelder der øverste morselskap i konsernet er lokalisert i Norge.

[Se krav til fullstendighet av opplysninger i melding for suppleringsskatt (GIR)](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/krav-til-fullstendighet/)

For at en virksomhet skal anses å oppfylle opplysningsplikten må melding for suppleringsskatt (GIR) som et minimum inneholde Jurisdiction Section for samtlige virksomheter i eller med tilknytning til konsernet (konsernenheter og felleskontrollerte virksomheter og deres underenheter) hvor Norge har beskatningsrett. Informasjon om hvilke land som har beskatningsrett oppgis i elementene JurWithTaxingRights i Jurisdiction Section og Summary.

### Slik fyller du den ut

#### RecJurCode

Oppgi landkode for Norge - NO. Hvis melding for suppleringsskatt (GIR) er ment for utveksling med andre land, må elementet RecJurCode også inneholde landkoder for alle land som skal motta opplysningene i den aktuelle Jurisdiction Section. I tillegg må verdien "GIR401" eller "GIR402" oppgis i FilingCERole elementet i Filing Info for å indikere at den aktuelle Jurisdiction Section er ment for utveksling. Skal ikke opplysningene i den aktuelle Jurisdiction Section utveksles, er det tilstrekkelig å oppgi landkode for Norge. Oppgi verdien "GIR403" eller "GIR404" i FilingCERole elementet i Filing Info for å indikere at den aktuelle Jurisdiction Section ikke skal utveksles.

#### Deferred Taxes Recast

Etter XML-veiledningen skal Recast elementet under DeferTaxAdjustAmt/Adjustment/Recast fylles ut på virksomhetsnivå. Dette medfører at Recast elementet må oppgis per Adjustment for den aktuelle virksomheten. Når elementet Recast skal oppgis for en virksomhet må elementet AdjustmentItem fylltes ut med verdien GIR2516 og Amount oppgis med verdien 0 for å unngå XSD-valideringsfeil.

#### DocSpec

Oppgi verdien OECD1 i elementet DocTypeIndic. De alternative forhåndsdefinerte verdiene skal ikke benyttes ved levering av melding for suppleringsskatt (GIR) i Norge. Elementet DocRefId skal fylles ut med en valgfri tekst som gir en unik referanse, for eksempel GIR2024NOII, der II erstattes med et nytt tall for hver del av filen.

#### Prosentverdier utenfor tillatt intervall

Etter OECDs XML Schema User Guide skal prosentverdier en rekke steder i XML-filen ligge innenfor intervallet 0-100%, eller 1 til 0 der verdien skal oppgis som et desimaltall. I enkelte tilfeller vil den beregnede prosentverdien ligge utenfor dette intervallet (0-100 %). Verdien skal oppgis som 0, hvis den beregnede prosentverdien er lavere enn 0 % (negativ). Er den beregnede prosentverdien over 100 %, skal verdien oppgis som 100 % (eller 1 når verdien oppgis som desimaltall).

### AdditionalDataPoint

Ved bruk av enkelte valgregler må elementet AdditionalDataPoint fylles ut. Dette gjelder følgende valg:

Valg om ikke å inkludere økning av utsatt skatteforpliktelse i justering for utsatt skatt kan du gjøre som ett ettårs eller femårsvalg.

Velger du å gjøre et ettårsvalg, jf. suppleringsskatteforskriften § 4-2-2 (og kommentarene til modellreglene artikkel 4.4.7 punkt 112.1) skal ikke Art.4.4.7 elementet brukes. I stedet skal verdien "ADT3 Art.4.4.7" oppgis i elementet Decription. I Text elementet skal følgende tekst skrives inn «Unclaimed Accrual Annual Election». I tillegg må du oppgi informasjon om TIN for de virksomhetene valget gjelder for i Text elementet, med mindre virksomheten har valgt å bruke forenklet metode for rapportering. I Text elementet skal du også oppgi stien til elementet som Additional Data Point gjelder for. De øvrige elementene under Additional Data Point skal ikke fylles ut.

Velger du derimot å gjøre et femårsvalg gjelder veiledningen for utfylling av XML-filen i OECDs XML Schema User Guide s. 82.

Hvis øverste morselskap i konsernet er en enhet med deltakerfastsetting og den rapporterende virksomheten bruker reglene i supl. § 7-1 (modellreglene artikkel 7.1) skal UPEAdjustments elementet fylles ut. Veiledning for utfylling av XML-filen følger av OECDs XML Schema User Guide s. 65-68.

I Basis elementet som indikerer grunnlaget for justeringen, mangler det en verdi for å indikere bruk av artikkel 7.1.2 (supl. § 7-1 andre ledd). Ved utfylling av elementet skal derfor verdien GIR1910 (Article 7.2.2) oppgis. I tillegg skal Reductions elementet i stien GloBEBody/ Jurisdiction Section/ GloBETax/ ETR/ ETRStatus/ ETRComputation/ AdjustedFANIL/ Adjustment/ UPEAdjustments/ Reduction fylles ut.

Verdien "ADT1 Basis" skal oppgis i Description elementet i Additional Data Point, og verdien i Reduction elementet skalogså oppgis i elementet Amount i Additional Data Point. Elementet Text skal også fylles ut med "Article 7.1.2".

Hvis elementet Reduction/Exception fylles ut, skal elementet Text i stedet fylles ut med "Article 7.1.2, Exception", samt informasjon om stien til elementet som Additional Data Point gjelder for.

Hvis Basis fylles ut med "GIR1910" fordi det er gjort en justering etter Article 7.2.2, skal elementet Basis gjentas og benyttes to ganger.

De øvrige elementene under Additional Data Point skal ikke fylles ut.

Valg om å inkludere gevinst eller tap på egenkapitalinvesteringer jf. suppleringsskatteforskriften § 3-2-2 femte ledd er ikke inkludert i XML-filen. Hvis den rapporteringspliktige virksomheten bruker dette valget skal informasjon om dette tas inn i AdditionalDataPoint elementet.

Elementet Description skal fylles ut med verdien "ADT2 EquityGain". Den relevante gevinsten eller tapet på egenkapital som inngår i justert overskudd eller underskudd når valget om inkludering av egenkapitalinvestering brukes, skal oppgis i elementet Amount. Element Text skal fylles ut med stien til elementet som Additional Data Point gjelder for. De øvrige elementene under Additional Data Point skal ikke fylles ut.

### Valgregler

Suppleringsskatteloven og modellreglene inneholder en rekke valgregler. Valgreglene er enten ettårs- eller femårsvalg.

- Ettårsvalg gjelder bare for det regnskapsåret valget er gjort.
- Femårsvalg kan ikke oppheves for valgåret eller de fire etterfølgende regnskapsårene og gjelder inntil de blir opphevet.

Noen valg gjøres på landnivå, mens andre gjøres på virksomhetsnivå.

I XML-filen er alle valgene separate elementer der du i de fleste tilfeller angir om et valg er benyttet ved å angi TRUE i elementet. Når et femårsvalg tas, skal du i tillegg oppgi året valget tas. Når valget oppheves, må du oppgi hvilket år valget oppheves. For noen valg er det ytterligere informasjon som skal oppgis.

Valgreglene kan også brukes ved beregning av nasjonal suppleringsskatt. Unntak fra dette gjelder [bruk av forenklet metode for rapportering](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/forenklet-metode-for-levering/) hvis det aktuelle landet ikke tillater bruk av denne metoden.

Den rapporterende virksomheten må selv sette seg inn i hvilke land dette eventuelt gjelder for og sørge for at opplysningene blir riktig etter nasjonale regler i det aktuelle landet. For beregning av nasjonal suppleringsskatt i Norge kan forenklet metode for rapportering brukes.

Valg på virksomhetsnivå rapporteres som hovedregel under elementet JurisdictionSection/GlobeTax/ETR/CEComputation/ Elections og veiledning til utfylling av XML-filen er inntatt i OECDs XML User Guide s. 78-85. For veiledning knyttet til valg under suppleringsskatteloven § 7-3 og modellreglene artikkel 7.3 se OECDs XML User Guide (Adjusted Covered Tax og DeemedDistTax elementet) s. 93-97.

Valg på landnivå gjøres normalt under elementene i Jurisdiction Section/GloBETax/ETR/Election, og veiledning til utfylling av XML-filen er inntatt i OECDs XML User Guide s. 51-56. Se også OECDs XML User Guide s. 47-49 for veiledning om utfylling av InitiallntActivity elementet ved anvendelse av unntaksbestemmelsen for konsern i startfasen av internasjonal aktivitet, jf. supl. § 2-14 og modellreglene artikkel 9.3. Bruk av denne regelen skal også reflekteres i [General Section](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/general-section/).

Det er ikke anledning til å gjøre endringer i valg etter at melding for suppleringsskatt (GIR) er levert. En fastsetting kan bare endres når fastsettingen er uriktig, jf. skatteforvaltningsloven § 12-1. En forespørsel om endring som bare gjelder endring av valg kan derfor normalt ikke tas til følge.

### Safe Harbour og unntaksregler

Valg knyttet til bruk av Safe Harbour-regler eller unntaket for bagatellmessig inntekt og resultat gjøres på landnivå. Du gjør valget ved å fylle ut de relevante elementene under ETR Exception. Veiledning for utfylling av XML-filen følger av OECDs XML Schema User Guide s. 57-61. Valgene skal også reflekteres i [Summary](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/summary-section/).

Ved bruk av testen for rutinemessig overskudd under forenklet beregningsmetode eller midlertidige Safe Harbour knyttet til land-for-land-rapportering må rapporterende virksomhet også fylle ut elementet Substance Exclusion i Jurisdiction Section. Dette gjelder imidlertid ikke dersom konsernet har rapportert null eller negativt resultat for landet. Når SubstanceExclusion fylles ut, må også de øvrige «validation» elementene i OverallComputation fylles ut med verdien 0 for å unngå XSD-valideringsfeil. Dette gjelder elementene FANIL, AdjustedFANIL, NetGlobeIncome, IncomeTaxExpense, ETRRate, TopUpTaxPercentage, ExcessProfits, TopUpTax og ExcessNegTaxExpense.

Benytter du Safe Harbour-regelen for forenklet beregningsmetode for uvesentlige konsernenheter skal relevante opplysninger for den aktuelle testen fylles ut under Non-Material CE elementene under OverallComputation. Veiledning for utfylling av XML-filen følger av OECDs XML Schema User Guide s. 117-119.

Hvis det er ikke-uvesentlige konsernenheter lokalisert i samme land eller inngår i samme undergruppe som de uvesentlige konsernenhetene, skal det gjøres fulle beregninger for disse i Jurisdiction Section.

Når testen for rutinemessig overskudd (de minimis) benyttes og det er virksomheter i den aktuelle undergruppen som ikke er uvesentlige konsernenheter, skal Financial Data og Average elementene under Globe Tax og Deminimis/SimplifiedNMCECalc også fylles ut for de virksomhetene som ikke er uvesentlige konsernenheter. Veiledning for utfylling av XML-filen følger av OECDs XML Schema User Guide s. 58.

Valg om å bruke kvalifisert nasjonal suppleringsskatt Safe Harbour oppgis i [Summary](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/summary-section/).

Kvalifisert nasjonal suppleringsskatt Safe Harbour kan ikke brukes hvis en av swich-off reglene i suppleringsskatteforskriften §5-7-10 tredje ledd kommer til anvendelse.

Safe Harbour-regelen for kvalifisert nasjonal suppleringsskatt for et land eller undergruppe kan brukes i kombinasjon med én av de andre Safe Harbour-reglene eller unntaket for bagatellmessig inntekt og resultat.

Når virksomheten som leverer melding for suppleringsskatt (GIR) velger å bruke kvalifisert nasjonal suppleringsskatt Safe Harbour for et land eller undergruppe, skal Jurisdiction Section fylles ut basert på de nasjonale reglene som gjelder i [Safe Harbour landet](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/introduksjon-til-gir/).

Slik skal du fylle ut JurisdictionSection om du velger å bruke kvalifisert nasjonal suppleringsskatt Safe Harbour:

- Hvis du bare bruker reglene om kvalifisert nasjonal suppleringsskatt, skal Jurisdiction Section fylles ut for landet eller undergruppen. Opplysninger i Jurisdiction Section skal da fylles ut basert på de [nasjonale reglene](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/introduksjon-til-gir/) i det aktuelle Safe Harbour landet.
- Hvis du gjør et tilleggsvalg for å kombinere kvalifisert nasjonal suppleringsskatt Safe Harbour med en annen Safe Harbour-regel eller unntaket for bagatellmessig inntekt og resultat, skal bare de relevante delene for denne Safe Harbour eller unntaksregelen i Jurisdiction Section fylles ut.
- Low Tax Jurisdiction eller UTPR Attribution elementene, skal ikke fylles ut ved bruk av kvalifisert nasjonal suppleringsskatt Safe Harbour, med mindre de aktuelle reglene i Safe Harbour landet fordeler nasjonal suppleringsskatt mellom virksomhetene i landet basert på deres justerte resultat.
- Ved bruk av kvalifisert nasjonal suppleringsskatt Safe Harbour for Norge eller undergrupper lokalisert i Norge skal elementene LowTaxJurisdiction/TopUpTaxAmount, LTCE/TIN, LTCE/IIR/NetGlobeIncome og LTCE/IIR/TopUpTax fylles ut når det beregnes nasjonal suppleringsskatt i Norge.

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/jurisdiction-section/) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-27** Første gang hentet
