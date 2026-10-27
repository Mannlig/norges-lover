<!-- innholds-hash: 5b490e15a4a1459f11468dc0e6e999ee18501e7a9c9c27928ed4597875dd6c21 -->

# Krav til rapportering basert på rolle

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/krav-til-rapportering-type-rolle/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-27T13:16:27Z

## Innhold

## Krav til rapportering basert på rolle

Her følger en kort oppsummering av krav til rapportering basert på hvilken virksomhet du skal rapportere for.

### Sentralisert levering

Virksomheter som inngår i et konsern (konsernenheter) som er omfattet av suppleringsskatteloven, har plikt til å levere melding for suppleringsskatt (GIR). Opplysningsplikten anses imidlertid oppfylt om en rapporterende virksomhet sender inn melding for suppleringsskatt (GIR) på vegne av alle virksomhetene i konsernet. Sentralisert levering velges der virksomheten du representerer skal levere melding for suppleringsskatt (GIR) på vegne av virksomheter lokalisert i utlandet.

Her gjelder følgende:

- Message Header, Filing Info, General Section og Summary må være fylt ut i overensstemmelse med vår veiledning.
- Filing Info: Bruk koden GIR401 (UPE) eller GIR402 (Designated Filing Entity) i FilingCERole elementet.
- RecJurCode (Summary, General Section og Jurisdiction Section): må inneholde landkode for de landene som den rapporterende virksomheten ønsker å bruke sentralisert levering for.
- Safe Harbour: Den rapporteringspliktige virksomheten kan bruke kvalifisert nasjonal suppleringsskatt Safe Harbour-regelen for Norge. Se vår veiledning under [Jurisdiction Section](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/jurisdiction-section/) og [Summary](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/summary-section/) knyttet til bruk av denne Safe Harbour-regelen.
- Jurisdiction Section for alle land og undergrupper hvor enten Norge eller ett av landene filen skal utveksles med har beskatningsrett, må være fylt ut i tråd med vår veiledning. Der øverste morselskap i konsernet er lokalisert i Norge, skal melding for suppleringsskatt (GIR) inneholde [Jurisdiction Section](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/jurisdiction-section/) for alle land konsernet har virksomhet i.

### Rapportering for nasjonale konsern

Virksomheter som inngår i et nasjonalt konsern som er omfattet av suppleringsskatteloven, har plikt til å levere melding for suppleringsskatt (GIR). Melding for suppleringsskatt (GIR) skal inneholde opplysninger om alle norske virksomheter i eller med tilknytning til konsernet (konsernenheter og felleskontrollerte virksomheter og deres underenheter).

Her gjelder følgende:

- Den rapporterende virksomheten må fylle ut Message Header, Filing Info, General Section, Summary og Jurisdiction Section for Norge.
- Filing Info: Bruk koden GIR403 (rapportering for hele konsernet) eller GIR404 (rapportering for den aktuelle virksomheten) i FilingCERole elementet. Kodene GIR401 og GIR402 skal ikke brukes.
- RecJurCode (i Summary, General Section og Jurisdiction Section): I dette elementet skal du oppgi landkode for Norge (NO).
- JurWithTaxingRights (Summary): I dette elementet skal du oppgi landkode for Norge (NO).
- QDMTTuT (Summary): Dette elementet skal fylles ut når det er beregnet nasjonal suppleringsskatt.
- Safe Harbour (i Summary og Jurisdiction Section): Nasjonale konsern kan benytte de midlertidige Safe Harbour-reglene knyttet til land-for-land-rapportering i overgangsperioden (2024–2026), hvis vilkårene i suppleringsskatteforskriften § 5-7-30 flg. er oppfylt. Ved bruk av Safe Harbour-reglene knyttet til land-for-land-rapportering hvor konsernet ikke har utarbeidet en land-for-land-rapport, kan konsernet benytte seg av reglene i § 5-7-30 til § 5-7-37 ved å gi relevante opplysninger på samme vilkår i melding for suppleringsskatt (GIR) jf. suppleringsskatteforskriften § 5-7-38.
- Forenklet metode for rapportering (i Summary og Jurisdiction Section): Nasjonale konsern kan også velge å bruke [forenklet metode for rapportering](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/forenklet-metode-for-levering/) når vilkårene for dette er oppfylt.
- Separat beregning for enkelte virksomheter eller undergrupper: Hvis konsernet har virksomheter eller undergrupper som det skal foretas separat beregning for, skal informasjon om slik virksomhet eller undergrupper oppgis i Subgroup elementene i Jurisdiction section og Summary. Når det skal foretas separate beregninger for en virksomhet eller undergruppe må Summary gjentas i sin helhet for undergruppen.
- Fordeling av nasjonal suppleringsskatt mellom virksomheter i Norge (Jurisdiction Section): Dette fyller du ut i elementet LowTaxJurisdiction. Elementene LowTaxJurisdiction/TopUpTaxAmount, LTCE/TIN, LTCE/IIR/NetGlobeIncome og LTCE/IIR/TopUpTax skal brukes for informasjon om fordelingen av nasjonal suppleringsskatt mellom de norske virksomhetene.

### Lokal rapportering for norske virksomheter

Virksomheter som inngår i et konsern (konsernenheter) som er omfattet av suppleringsskatteloven, har plikt til å levere melding for suppleringsskatt (GIR). Opplysningsplikten anses oppfylt om øverste morselskap eller en annen utpekt rapporterende virksomhet leverer melding for suppleringsskatt (GIR) på vegne av de norske virksomhetene (sentralisert levering). Er ikke sentralisert levering anvendt, må virksomheten selv levere melding for suppleringsskatt (GIR).

Her gjelder følgende:

- Message Header, Filing Info, General Section og Summary fylles ut i overensstemmelse med vår veiledning.
- Filing Info: Bruk koden GIR403 (på vegne av alle norske virksomheter) eller GIR404 (for bare den aktuelle virksomheten) i FilingCERole elementet.
- RecJurCode (Summary, General Section og Jurisdiction Section): I dette elementet skal du bare oppgi landkode for Norge (NO).
- Jurisdiction Sections for Norge, og alle land og undergrupper hvor Norge har beskatningsrett, må være fylt ut i tråd med [veiledningen for utfylling av Jurisdiction Section](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/jurisdiction-section/).

### Lokal rapportering for øverste morselskap i Norge

En norsk virksomhet som er det øverste morselskapet i et flernasjonalt konsern må fylle ut melding for suppleringsskatt (GIR) med opplysninger om og beregning av suppleringsskatt for hele konsernet. Dette gjelder også der det øverste morselskapet ikke bruker sentralisert levering på vegne av virksomheter i utlandet.

Her gjelder følgende:

- Message Header, Filing Info, General Section og Summary skal fylles ut i overensstemmelse med vår veiledning.
- Filing Info: Bruk koden GIR403 (på vegne av alle norske virksomheter) eller GIR404 (for bare den aktuelle virksomheten) i FilingCERole elementet.
- RecJurCode (Summary, General Section og Jurisdiction Section): I dette elementet skal du bare oppgi landkode for Norge (NO).
- Jurisdiction Section: Melding for suppleringsskatt (GIR) der øverste morselskap i konsernet er lokalisert i Norge skal inneholde [Jurisdiction Section](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/jurisdiction-section/) for alle land konsernet har virksomhet i.

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/krav-til-rapportering-type-rolle/) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-27** Første gang hentet
