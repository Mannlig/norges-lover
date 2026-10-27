<!-- innholds-hash: 08935e18b6c56c59e4cc763f59887c8a330286b1ac2681ab41ff0fb531caceb6 -->

# Message Header

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/message-header/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-27T13:17:35Z

## Innhold

## Message Header

Bruk veiledningen i OECDs XML Schema User Guide sammen med våre presiseringer i veiledningen her for å unngå feil eller merknader i Message Header (MessageSpec) når du skal sende inn melding for suppleringsskatt (GIR) til oss.

Message Header inneholder metadata og informasjon for å identifisere filen.

Message Header i XML-filen og i veiledningen fra OECD er bygget opp med formål for utveksling av opplysninger mellom land. Dette gjør at ikke alle dataelementene er relevante når du skal sende inn melding for suppleringsskatt (GIR) til oss. Vi har derfor laget en oppsummering av hvilke dataelementer som er relevant og må fylles ut for levering av melding for suppleringsskatt (GIR) via løsningen på våre nettsider.

### Slik fyller du den ut

- SendingEntityIN: oppgi organisasjonsnummer (9 siffer) til virksomheten som sender inn melding for suppleringsskatt (GIR). Organisasjonsnummeret som oppgis her må være det samme som du velger når du er innlogget for å levere meldingen.
- TransmittingCountry: skal kun inneholde landkode for Norge - NO
- ReceivingCountry: skal kun inneholde landkode for Norge - NO
- MessageType: oppgi verdien "GIR"
- MessageRefID: fylles ut med valgfri tekst som gir en unik referanse, f.eks. StatusNO2024xxx hvor xxx erstattes med de tre første bokstavene i virksomhetens navn e.l.
- MessageTypeIndic: oppgi verdien "GIR101". Verdiene "GIR102" og "GIR103" skal ikke benyttes. Hvis du har behov for å gjøre endringer i melding for suppleringsskatt (GIR) etter at meldingen er sendt inn, må du sende en [forespørsel om endring](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/melding-om-suppleringsskatt-gir/) til oss.
- ReportingPeriod: oppgi dato for siste dag i regnskapsåret rapporteringen gjelder for (datoen skal tilsvare siste dag i regnskapsåret for det øverste morselskapet i konsernet. Datoen som oppgis her skal være lik dato i Period/-End elementet i Filing Info). Dato fylles ut i format yyyy-mm-dd.
- Timestamp: fylles ut med dato og tidspunkt for utfylling eller innsending av melding for suppleringsskatt (GIR) i format yyyy-mm-dd’T’hh:mm:ss

Hvis XML-filen ikke inneholder disse elementene, eller elementene ikke er fylt ut, vil filen ikke være i samsvar med XSD-kravene. Melding for suppleringsskatt (GIR) vil da få valideringsfeil ved opplastning av filen og det vil ikke være mulig å sende den inn.

### Følgende elementer må ikke fylles ut

Message Header består i tillegg av følgende elementer som ikke trenger å fylles ut:

- Warning
- Contact

Du vil ikke få feil eller merknader om du lar disse elementene stå uten en verdi når du sender inn melding for suppleringsskatt (GIR) til oss.

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/message-header/) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-27** Første gang hentet
