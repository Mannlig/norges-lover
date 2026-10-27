<!-- innholds-hash: 2f5bbc4cbf23aeef35ffdea4b15ab853f4bbc830eab1eb4bcf31590fe2f9a543 -->

# OECD veiledning og XSD-krav

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/veiledninger-fra-oecd/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-27T13:20:57Z

## Innhold

## OECD veiledning og XSD-krav

Krav til innhold og teknisk format i melding for suppleringsskatt (GIR) følger OECDs internasjonale krav for GloBE Information Return.

Dette innebærer at veiledningene utarbeidet av OECD for utfylling av GloBE Information Return også skal legges til grunn ved utfylling av melding for suppleringsskatt (GIR) i Norge.

OECD har publisert to sentrale veiledninger om utfylling av GloBE Information Return:

### Veiledning for utfylling av GloBE Information Return

[OECDs veiledning til utfylling av GloBE Information Return](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/01/tax-challenges-arising-from-the-digitalisation-of-the-economy-globe-information-return-january-2025_b03274ed/a05ec99a-en.pdf)

Her finner du veiledning knyttet til innholdet og datapunktene i GloBE Information Return som skal inn i XML-filen.

Veiledningen gir en skjematisk fremstilling av innhold og datapunktene i GloBE Information Return og avviker derfor noe fra oppbyggingen av XML-formatet. Forskjellen skal kun være av teknisk art, og veiledningen vil være førende for hvilke opplysninger du skal oppgi i de ulike delene av XML-filen ved innsending av melding for suppleringsskatt (GIR).

### XML veiledning: XML Schema User Guide

[OECDs XML Schema User Guide](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/01/globe-information-return-pillar-two-xml-schema_3980638f/c594935a-en.pdf)

Her finner du en teknisk brukerveiledning til XML-filen for GloBE Information Return.

Veiledningen beskriver oppbyggingen av XML-filen og gir en systematisk gjennomgang av de enkelte dataelementene med tilhørende attributter. Veiledningen redegjør også for de tekniske kravene til utfylling, herunder hvilke dataelementer som er obligatoriske (valideringselementer) og som må være med for at filen skal godtas, samt tekniske formateringskrav som bruk av boolean-verdier, avrunding av beløp og angivelse av prosentandeler.

Merk at XML Schema User Guide primært er utarbeidet for utveksling av opplysninger mellom skattemyndigheter. Enkelte elementer i filen er derfor ikke relevante for virksomheter som leverer melding for suppleringsskatt (GIR) til Skatteetaten. Noen av disse elementene må likevel fylles ut for å tilfredsstille våre XSD-krav.

Den delen av veiledningen som gjelder Corrections i OECDs XML Schema User Guide er ikke aktuell for virksomheter som leverer melding for suppleringsskatt (GIR) i Norge. Hvis du har behov for å gjøre endringer i melding for suppleringsskatt (GIR) etter at meldingen er sendt inn, må du [sende en forespørsel om endring til oss](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/melding-om-suppleringsskatt-gir/).

### XSD-krav

[Support Materials - GloBE Information Return (Pillar Two) XML Schema (OECD)](https://www.oecd.org/en/publications/globe-information-return-pillar-two-xml-schema_c594935a-en/support-materials.html)

XSD-kravene fastsetter tekniske krav til XML-filens struktur og innhold som må oppfylles for at filen skal være gyldig.

Melding for suppleringsskatt (GIR) må leveres i XML-format. XML-filen må følge XSD-krav (XML Schema Definition) som publisert av OECD.

I OECDs XML Schema User Guide er de ulike dataelementene markert enten som obligatoriske «validation» eller valgfrie eller betinget obligatoriske«optional». Alle elementer som er et «validation» element må være til stede og fylles ut ved levering av melding for suppleringsskatt (GIR) for å oppfylle våre XSD-krav.

Vi anbefaler å validere XML-filen gjennom en ekstern XSD-validator før du sender den inn. Som offentlig virksomhet kan ikke Skatteetaten anbefale noen valideringsverktøy fremfor andre. Det finnes mange gratis valideringsverktøy på internett som kan brukes. Det er også en XSD-validator i Skatteetatens innleveringsløsning og valideringstjeneste, slik at filvedlegg med formatfeil ikke er mulig å sende inn.

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/veiledninger-fra-oecd/) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-27** Første gang hentet
