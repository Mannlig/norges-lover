<!-- innholds-hash: c5a91a7c7ff0aa79299f64a93b43f0c6ecece976aec7c69281c8b6c708d1dd88 -->

# Sentralisert levering

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/sentralisert-levering/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-27T13:18:41Z

## Innhold

## Sentralisert levering

Representerer du en virksomhet som skal levere melding for suppleringsskatt (GIR) på vegne av virksomheter i utlandet (sentralisert levering), må du inkludere opplysninger om hvilke land de ulike delene av filen skal utveksles til.

En virksomhets opplysningsplikt kan oppfylles gjennom sentralisert levering av melding for suppleringsskatt (GIR). Ved sentralisert levering leverer den rapporterende virksomheten en samlet melding for suppleringsskatt (GIR) på vegne av øvrige virksomheter i konsernet.

Sentralisert levering av melding for suppleringsskatt (GIR) kan bare benyttes i eller med land hvor Norge har en avtale om utveksling av suppleringsskatteopplysninger med. En oversikt over hvilke land Norge har slik utvekslingsavtale med fremgår av listen publisert på OECD sine hjemmesider;

[Signatories of the Multilateral Competent Authority Agreement on the Exchange of GloBE Information (GIR MCAA) (OECD)](https://www.oecd.org/content/dam/oecd/en/topics/policy-issues/tax-transparency-and-international-co-operation/gir-mcaa-signatories.pdf)

For at virksomheten kan anvende sentralisert levering av melding for suppleringsskatt (GIR) må utvekslingsavtalen være aktivert før leveringsfristen. Listen over aktiverte utvekslingsavtaler finner du på listen over

[Aktiverte utvekslingsavtaler (OECD)](https://www.oecd.org/en/topics/sub-issues/international-standards-on-tax-transparency/automatic-exchange-of-information-exchange-relationships.html)

I de tilfeller hvor vi ikke har anledning til å utveksle opplysninger med et land under utvekslingsavtalen, vil virksomheten kunne ha en lokal opplysningsplikt i det landet den er lokalisert. Virksomheten er selv ansvarlig for å sette seg inn i nasjonale rapporteringskrav og sørge for at opplysningsplikter i andre land overholdes.

For regnskapsåret 2024 kan du imidlertid legge til grunn at Norge kan utveksle suppleringsskatteopplysninger med landene som fremgår av [listen over land som forventes å være klare for sentralisert levering før 31. mai 2026 (OECD)](https://www.oecd.org/content/dam/oecd/en/topics/policy-sub-issues/global-minimum-tax/support-for-central-gir-filing-and-exchange-2024-reporting-fiscal-year.pdf).

Når øverste morselskap eller en annen utpekt virksomhet leverer melding for suppleringsskatt (GIR) på vegne av andre virksomheter i konsernet, skal informasjon om virksomheten som leverer melding for suppleringsskatt (GIR) oppgis i elementet FilingInfo. Ekementet FilingCE Role må fylles ut med verdien GIR401 (øverste morselskap) eller GIR402 (utpekt rapporterende virksomhet).

Videre må elementet RecJurCode i de aktuelle delene av XML-filen fylles ut med landkode for de land filen skal utveksles med, se [GloBE Information Return XML Schema s. 7-8 for veiledning om «Dissemination of GloBE Information» (OECD)](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/01/tax-challenges-arising-from-the-digitalisation-of-the-economy-globe-information-return-january-2025_b03274ed/a05ec99a-en.pdf) om hvilke deler av XML-filen som utveksles til hvilke land.

---
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/suppleringsskatt/veiledning/sentralisert-levering/) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-27** Første gang hentet
