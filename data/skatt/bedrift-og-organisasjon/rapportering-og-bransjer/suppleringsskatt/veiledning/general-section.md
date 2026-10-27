<!-- innholds-hash: 8d6db220d85cc67b0e32430237e43cb558350a208ee0cb6430c5acd006a14fc2 -->

# General Section

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/general-section/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-27T13:12:00Z

## Innhold

## General Section

Bruk OECD veiledningene sammen med våre presiseringer her for å unngå feil eller merknader i General Section når du skal sende inn melding for suppleringsskatt (GIR) til oss. Veiledning for utfylling av XML-filen følger av OECDs XML Schema User Guide s. 22-35.

General Section inneholder opplysninger om konsernstruktur, identifikasjon av virksomheter i eller med tilknytning til konsernet, og hvilke land de er lokalisert i.

General Section skal fylles ut i overensstemmelse med XML Schema User Guide s. 22-35. Dette gjelder også der XML-filen ikke er ment for utveksling (sentralisert levering). Dette betyr at informasjon om alle virksomhetene i konsernet eller med tilknytning til konsernet (konsernenheter og felleskontrollerte virksomheter, samt deres underenheter), skal inntas i General Section uavhengig av hvor de er lokalisert.

### Slik fyller du den ut

#### RecJurCode

Oppgi landkode for Norge - NO. Hvis melding for suppleringsskatt (GIR) er ment for utveksling med andre land, må elementet RecJurCode også inneholde landkoder for alle land som skal motta opplysninger i General Section. I tillegg må verdien "GIR401" eller "GIR402" oppgis i FilingCERole i Filing Info for å indikere at General Section er ment for utveksling. Skal opplysninger ikke utveksles er det tilstrekkelig å oppgi landkode for Norge. Oppgi verdien "GIR403" eller "GIR404" i FilingCERole elementet i Filing Info for å indikere at General Section ikke skal utveksles.

#### IDType Rules

I General Section skal det i elementet IDTypeRules oppgis hvilke regler en virksomhet er omfattet av. Det vil si hvilke regler som er innført i det aktuelle landet hvor virksomheten er lokalisert, se XML Schema User Guide s. 14-15. Alle kodene som er aktuelle for et land skal oppgis for hver virksomhet. For virksomheter lokalisert i Norge, skal elementet IDType/Rules fylles ut med både "GIR202" og "GIR204". En oversikt over [hvilke land som har innført kvalifiserte regler om skatteinkludering, skattefordeling og nasjonal suppleringsskatt finner du hos OECD](https://www.oecd.org/en/topics/sub-issues/global-minimum-tax/central-record-of-legislation-with-transitional-qualified-status.html).

#### QUTPR

QUTPR elementet skal ikke fylles ut hvis det ikke er noen land som har beskatningsrett under en kvalifisert regel om skattefordeling for det aktuelle regnskapsåret. Dersom konsernet er i startfasen av sin internasjonale virksomhet kan elementet Art9.3 anvendes for å indikere at unntaksbestemmelsen i supl. § 2-14 er valgt. Se også XML User Guide s. 32-33 for veiledning om utfylling av QUTPR. Når denne valgregelen anvendes skal informasjon om valget også reflekteres i [Jurisdiction Section](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/jurisdiction-section/) i InitiallntActivity elementet.

#### AdditionalDataPoint

I General Section skal AdditionalDataPoint elementet kun fylles ut hvis et land har gitt særskilt veiledning om dette. Skatteetaten har ikke gitt slik veiledning og elementet skal derfor normalt ikke brukes ved levering av melding for suppleringsskatt (GIR) i Norge. Hvis melding for suppleringsskatt (GIR) leveres i Norge på vegne av virksomheter som er lokalisert i utlandet (sentralisert levering), må virksomheten selv sette seg inn i eventuelle lokale opplysningsplikter i de tilfeller der utfylling av melding for suppleringsskatt (GIR) skal følge [nasjonale regler](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/introduksjon-til-gir/) i utlandet.

#### DocSpec

Oppgi verdien "OECD1" elementet i DocTypeIndic. De alternative forhåndsdefinerte verdiene skal ikke benyttes ved levering av melding for suppleringsskatt (GIR) i Norge. Elementet DocRefId skal fylles ut med en valgfri tekst som gir en unik referanse, for eksempel "GIR2024NOII", der II erstattes med et nytt tall for hver del av filen.

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/general-section/) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-27** Første gang hentet
