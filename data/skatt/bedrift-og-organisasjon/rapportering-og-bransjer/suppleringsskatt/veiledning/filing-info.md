<!-- innholds-hash: e07f67e1433d81267018ab2dc44f668dc046b9983d431f198fc3eaf4e4a09158 -->

# Filing Info

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/filing-info/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-27T13:09:46Z

## Innhold

## Filing Info

Bruk OECD veiledningene sammen med våre presiseringer her for å unngå feil eller merknader i Filing Info når du sender inn melding for suppleringsskatt (GIR) til oss. Veiledning for utfylling av XML-filen følger av OECDs XML User Guide s. 19-22.

Filing Info inneholder opplysninger om innsender. Filing Info består av fire hovedelementer: FilingCE, AccountingInfo, Period og NameMNE.

### Slik fyller du den ut

- ResCountryCode: oppgi landkode for Norge - NO.
- TIN elementet: oppgi organisasjonsnummer (9 siffer) til virksomheten som sender inn melding for suppleringsskatt (GIR). Organisasjonsnummeret som oppgis her må være det samme som innlogget virksomhet, som også er oppgitt i Message Header. Organisasjonsnummeret må være et gyldig norsk organisasjonsnummer. I attributtet IssuedBy skal landkode for Norge "NO" oppgis.
- FilingCERole: oppgi en av de forhåndsdefinerte verdiene "GIR401" og "GIR 404", avhengig av hvilken rolle den rapporterende virksomheten har. Elementet brukes også for å indikere om filen skal utveksles med andre land eller ikke.
- DocSpec: oppgi verdien "OECD1" i elementet DocTypeINdic. De alternative forhåndsdefinerte verdiene skal ikke benyttes ved levering av melding for suppleringsskatt (GIR) i Norge. Elementet DocRefId skal fylles ut med en valgfri tekst som gir en unik referanse, for eksempel "GIR2024NOII", der II erstattes med et nytt tall for hver del av filen.

AdditionalInfo skal ikke benyttes av virksomheter som leverer melding for suppleringsskatt (GIR) i Norge.

### FilingCERole

I elementet FilingCERole er det fem forhåndsdefinerte verdier som kan brukes. Ved levering av melding for suppleringsskatt (GIR) i Norge skal de aktuelle kodene benyttes på følgende måte;

- GIR401 – Ultimate Parent Entity: Benyttes når øverste morselskap i konsernet leverer melding for suppleringsskatt (GIR) på vegne av seg selv og andre virksomheter lokalisert i utlandet. Koden indikerer at filen skal utveksles med myndigheter i utlandet.
- GIR402 - Designated Filing Entity: Benyttes når en annen virksomhet enn øverste morselskap er utpekt til å levere melding for suppleringsskatt (GIR) på vegne av virksomheter lokalisert i utlandet. Koden indikerer at filen skal utveksles med myndigheter i utlandet.
- GIR403 - Designated Local Entity: Benyttes når en norsk virksomhet er utpekt til å levere melding for suppleringsskatt (GIR) på vegne av seg selv og andre norske virksomheter. Koden kan bare benyttes der filen ikke skal utveksles med myndigheter i utlandet. Denne koden skal også benyttes for rapportering av øverste morselskap i nasjonale konsern.
- GIR404 - Constituent Entity: Benyttes når en virksomhet leverer melding for suppleringsskatt (GIR) kun på egne vegne.
- GIR405 – Other: Denne koden skal ikke benyttes ved levering av melding for suppleringsskatt (GIR) i Norge.

Merk at når GIR401 (øverste morselskap) eller GIR402 (utpekt rapporterende virksomhet) brukes er dette en indikasjon på at filen skal utveksles med andre lands myndigheter ([sentralisert levering](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/sentralisert-levering/)). Virksomheten som leverer melding for suppleringsskatt (GIR) må da påse at landkode for de landene meldingen er ment å leveres på vegne av (og som informasjon skal utveksles med) er lagt inn i RecJurCode elementene i General Section, Summary, Jurisdiction Section og eventuelt UTPRAttribution elementene i XML-filen (Se XML Schema User Guide s. 23, 36, 42 og 123).

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/filing-info/) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-27** Første gang hentet
