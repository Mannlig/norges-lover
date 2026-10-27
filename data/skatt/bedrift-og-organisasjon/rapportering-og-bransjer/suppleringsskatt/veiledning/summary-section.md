<!-- innholds-hash: ad04b8ca11352b9a47c79aaebdb2f42b32ff686d954a430b677809cd68e43815 -->

# Summary

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/summary-section/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-27T13:19:45Z

## Innhold

## Summary

Bruk OECD veiledningene sammen med våre presiseringer her for å unngå feil eller merknader i Summary når du skal sende inn melding for suppleringsskatt (GIR) til oss. Veiledningen for utfylling av XML-filen følger av XML Schema User Guide s. 35-41.

Summary inneholder en oppsummering av informasjon per land, herunder Safe Harbour og unntaksregler, samt opplysninger om hvilke land som har beskatningsrett.

Summary skal fylles ut i overensstemmelse med XML Schema User Guide s. 35-41. Dette gjelder også der XML-filen ikke er ment for utveksling (sentralisert levering). Dette betyr at Summary skal inneholde informasjon om alle land og eventuelt virksomheter eller undergrupper i et land som det skal foretas separat beregning for, uavhengig av hvor de er lokalisert. Der det skal foretas separate beregninger for en virksomhet eller undergruppe av virksomheter i et land, må Summary gjentas for å reflektere de aktuelle undergruppene.

### Slik fyller du den ut

#### RecJurCode

Oppgi landkode for Norge - NO. Hvis melding for suppleringsskatt (GIR) er ment for utveksling med andre land, må elementet RecJurCode også inneholde landkoder for alle land som skal motta opplysninger i Summary. I tillegg må verdien "GIR401" eller "GIR402" oppgis i FilingCERole elementet i Filing Info for å indikere at Summary er ment for utveksling. Skal opplysningene i Summary ikke utveksles er det tilstrekkelig å oppgi landkode for Norge. Oppgi verdien "GIR403" eller "GIR404" i FilingCERole elementet i Filing Info for å indikere at Summary ikke skal utveksles.

#### JurWithTaxingRights

For hvert land og eventuell undergruppe skal det i Summary fylles ut opplysninger om land med beskatningsrett i elementet JurWithTaxingRights. Alle land med beskatningsrett skal oppgis, også der det ikke beregnes noen suppleringsskatt fordi effektiv skattesats er over 15%, ved bruk av Safe Harbour-regler, unntaksregel eller liknende.

#### Subgroup

Elementet Subgroup skal brukes når konsernet har virksomheter eller undergrupper som det skal foretas separate beregninger for. Dette gjelder for felleskontrollerte virksomheter og deres underenheter, investeringsenheter og forsikringsinvesteringsenheter, minoritetseide konsernenheter og minoritetseide underkonsern, samt statsløse enheter. Oppgi en av de forhåndsdefinerte verdiene GIR1101-GIR1106 i elementet TypeofSubGroup samt TIN for virksomheten øverst i eierstrukturen for hver enkelt undergruppe. Der det skal foretas separate beregninger for en virksomhet eller undergruppe av virksomheter i et land, må Summary gjentas for å reflektere de aktuelle undergruppene i landet. Tilsvarende informasjon om Subgroup skal oppgis i Jurisdiction Section.

#### Safe Harbour

I Summary skal det oppgis informasjon om Safe Harbour-regler virksomheten som leverer melding for suppleringsskatt (GIR) har brukt. Tilsvarende skal det gis informasjon om bruk av reglene om unntaket for bagatellmessig inntekt og resultat i supl. § 5-5.

Ved bruk av reglene for forenklet beregningsmetode Safe Harbour for uvesentlige konsernenheter i suppleringsskatteforskriften §§ 5-7-20 til 5-7-21 skal en av de forhåndsdefinerte verdiene "GIR1207-GIR1209" oppgis for å indikere at en av de tre testene er brukt.

Når den rapporterende virksomheten velger å bruke en Safe Harbour-regel eller unntaket for bagatellmessig inntekt og resultat i et land eller for en undergruppe, reduseres normalt suppleringsskatten til null. I slike tilfeller skal den rapporteringspliktige virksomheten ikke fylle ut hele Jurisdiction Section, men kun den delen som gjelder ETR Exception.

- Når virksomheten har brukt forenklet beregningsmetode Safe Harbour, og den forenklede beregningen ikke gjelder for alle virksomhetene lokalisert i det aktuelle landet. I slike tilfeller skal den rapporteringspliktige virksomheten fylle ut de relevante delene av Jurisdiction Section for de virksomhetene som ikke omfattes av de forenklede beregningene.
- Når virksomheten har brukt forenklet beregningsmetode Safe Harbour, men det skal beregnes etterberegnet suppleringsskatt. I slike tilfeller må de relevante elementene i Jurisdiction Section også fylles ut.
- Når virksomheten har brukt testen om rutinemessig overskudd under reglene om forenklet beregningsmetode Safe Harbour (GIR1209) eller den midlertidige Safe Harbour-reglen knyttet til land-for-land-rapportering (GIR1205). I slike tilfeller skal den rapporterende virksomheten også fylle ut elementet Substance Exclusion i Jurisdiction Section. Når Substance Exclusion fylles ut, må også de øvrige "validation" elementene i Overall Computation fylles ut med verdien 0 for å unngå XSD-valideringsfeil. Dette gjelder elementene FANIL, AdjustedFANIL, NetGlobeIncome, IncomeTaxExpense, ETRRate, TopUpTaxPercentage, ExcessProfits, TopUpTax og ExcessNegTaxExpense.
- Når virksomheten har brukt kvalifisert nasjonal suppleringsskatt Safe Harbour (GIR1202). I slike tilfeller skal Jurisdiction Section fylles ut, men [etter de nasjonale reglene som gjelder i Safe Harbour landet](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/introduksjon-til-gir/). Merk at reglene om kvalifisert nasjonal suppleringsskatt Safe Harbour også kan brukes i kombinasjon med én av de andre Safe Harbour-reglene. Der virksomheten har valgt å bruke kvalifisert nasjonal suppleringsskatt Safe Harbour i kombinasjon med en annen Safe Harbour regel, må bare den delen som gjelder disse valgene fylles ut.

Kvalifisert nasjonal suppleringsskatt Safe Harbour (GIR1202) kan ikke velges hvis en av switch-off reglene i suppleringsskatteforskriften § 5-7-10 tredje ledd kommer til anvendelse.

[For mer informasjon om Safe Harbour-reglene se Skatte-ABC S-22-6 Safe Harbour-regler](https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/)

#### DocSpec

Oppgi verdien "OECD1" i elementet DocTypeINdic. De alternative forhåndsdefinerte verdiene skal ikke benyttes ved levering av melding for suppleringsskatt (GIR) i Norge. Elementet DocRefId skal fylles ut med en valgfri tekst som gir en unik referanse, for eksempel "GIR2024NOII", der II erstattes med et nytt tall for hver del av filen.

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/summary-section/) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-27** Første gang hentet
