<!-- innholds-hash: d0431b066f4178331180f08824def583888d61767f023061aab3db5e688f919f -->

# Rettledning for utfylling og innlevering av opplysninger om Aksjesparekonto

## Kildeinformasjon

- **Kilde:** Skatteetaten – https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/bank-finans-og-forsikring/aksjesparekonto/rettledning/
- **Sist oppdatert (kilde):** ukjent
- **Sist oppdatert i arkivet:** 2026-10-27T13:41:58Z

## Innhold

## Rettledning for utfylling og innlevering av opplysninger om Aksjesparekonto

### 1. Kort om tredjepartsordningen Aksjesparekonto

Denne rettledningen angir

- hvem som skal levere opplysninger
- hvilke opplysninger som skal gis
- andre krav og opplysninger om rapporteringen

Rettledningen er skrevet for opplysningspliktige som skal levere tredjepartsopplysninger for aksjesparekonto.

Informasjon om aksjesparekonto som ikke berører levering av tredjepartsopplysninger kan finnes [her](https://www.skatteetaten.no/person/skatt/hjelp-til-riktig-skatt/aksjer-og-verdipapirer/om/aksjesparekonto-ask/).

Rettledningen inneholder praktiske, juridiske og datatekniske opplysninger vedrørende beskatning og rapportering av aksjesparekonto. Rettledningen med tilhørende formatbeskrivelser (se "[Beskrivelse av filformatet](https://www.skatteetaten.no/contentassets/efad4cb94ff8459ba8363a3d34cc7f69/v2_0/filformat-for-aksjesparekonto_v2_0_20190829.pdf)") skal gjelde for inntektsåret 2021 og senere år, inntil ny rettledning eller formatbeskrivelse blir utarbeidet.

### 2. Hvem skal levere opplysninger

Opplysningsplikten til denne tredjepartsordningen er hjemlet etter [Skatteforvaltningsloven 7-3](https://lovdata.no/dokument/NL/lov/2016-05-27-14/KAPITTEL_7#KAPITTEL_7) med tilhørende forskrift.

### 3. Levere tredjepartsopplysninger

#### Maskin-til-maskin-rapportering (M2M)

Tredjepartsopplysninger kan sendes direkte fra sluttbrukersystemet til Skatteetaten med maskin-til-maskin-integrasjon (M2M). Rapportering kan leveres i JSON-format eller som XML-fil, avhengig av hvilken løsning og ordning som benyttes. Dette krever at systemet er koblet til Skatteetatens mottaks-API med en systembruker.

XML-baserte leveranser er særlig aktuelle for virksomheter som rapporterer større datamengder og som ønsker å sende inn opplysninger direkte fra egne fagsystemer. XML-filen må være bygget opp i samsvar med gjeldende informasjonsmodell, formatbeskrivelse (XSD) og tekniske krav for den aktuelle ordningen.

Les mer om Skatteetatens API-er i [API-dokumentasjonen](https://skatteetaten.github.io/api-dokumentasjon/) og [TPO filmottak API (XML)](https://skatteetaten.github.io/api-dokumentasjon/api/innrapportering-tpo-filmottak)

#### Vedleggskjema

Tredjepartsopplysninger leveres som XML-filvedlegg via skjema [Tredjepartsopplysninger som vedlegg](https://www.skatteetaten.no/skjema/tredjepartsopplysninger-som-vedlegg/). Filen som lastes opp, skal være i XML-format og følge Skatteetatens spesifikasjoner.

Se også avsnitt 6.3 om filformat.

#### 3.2 Særlig om rapportering av formue

Det er formues-rabatt på aksjer og verdipapirfond (aksjedel). Rabatten for 2026 er på 20%. Dette gjelder også for aksjer og aksjefondsandeler som står på ASK. Det er markedsverdi som skal rapporteres til Skatteetaten, og det er markedsverdien som vil vises i skattemeldingen til kunden. Skatteetaten beregner så rabatten slik at 80% av verdien inngår i selve skatteoppgjøret. Dette skal ikke kunden selv gjøre. Rabatten vil fremgå av eget vedlegg til skattemeldingen.

Eksempel:

På ASK har investor aksjer, aksjefond og kontanter ved utgangen av inntektsåret.

| Markedsverdi aksjer | 100 |
| --- | --- |
| Markedsverdi aksjefond | 120 |
| Kontanter | 0 |

I skattemeldingen finner du beløpene Under «Finans», hvor du kan velge temaet «Aksjesparekonto»

| Formue aksjesparekonto - aksjedel | Kr 220 |
| --- | --- |
| Formue aksjesparekonto - kontanter | Kr 30 |

#### 3.3 Overføring av aksjesparekonto fra en tilbyder til en annen (flytt)

Ved overføring mellom opplysningspliktige i løpet av året skal rapportering skje slik:

Opplysningspliktig A har konto A frem til 01.11.2026, da konto flyttes til opplysningspliktig B. Opplysningspliktig A rapporterer transaksjoner i form av innskudd, ubenyttet skjerming, anvendt skjerming, skattemessig gevinst, uttak, realisasjonsvederlag på konto, samt formuesverdi 0, inngangsverdi 0 og antall 0 per finansprodukt. Konto skal ikke merkes som avsluttet ved flytting, men merkes med verdien "True" i feltet for flytting. Ved flytting må opplysningspliktig A gi informasjon om alle bevegelser av skattemessig betydning (f.eks. laveste innskuddssaldo, ubenyttet skjerming eller uttak fra kontoen) på konto før flyttedato til opplysningspliktig B.

Opplysningspliktig B rapporterer konto som ved ordinær rapportering uten flytt. Opplysningspliktig B rapporterer alle hendelser og verdier på konto etter overtakelse. Det vil si innskudd, uttak, ubenyttet skjerming, anvendt skjerming, realisasjonsvederlag, samt formuesverdier, inngangsverdi og antall per finansprodukter. Skattemeldingen vil dermed kunne være pre-utfylt med tredjepartsopplysninger fra to opplysningspliktige for inntektsåret 2026:

Opplysningspliktig A: Rapporterer eventuelt skattemessig gevinst i perioden før flytting, til skattemeldingen.

Opplysningspliktig B: Rapporterer formuesverdier og eventuelt skattemessig gevinst/tap i perioden etter flytting, til skattemeldingen.

Om overføring av verdipapirer mellom egne konti hos ulike tilbydere, se under punkt 3.6 «Overføring av verdipapirer mellom egne konti»

#### 3.4 Uttak fra kontoen

Overføring av aksje, egenkapitalbevis, kontanter eller aksjefondsandeler fra aksjesparekontoen til kontohaver, anses som uttak fra kontoen, jf. sktl. § 10-21 sjette ledd femte punktum. Uttaket settes til verdien av aksjen, egenkapitalbeviset eller aksjefondsandelen på overføringstidspunktet. Uttak som overstiger innskuddet, tillagt skjerming anses som skattepliktig inntekt, jf. sktl. § 10-21 fjerde ledd annet punktum. Ved uttak fra kontoen, anses innskudd på kontoen for å være tatt ut først, jf. sktl. § 10-21 fjerde ledd første punktum. Fradrag for eventuelt tap kan først kreves ved opphør av kontoen, se pkt. 10 i samme paragraf. I så fall må kontoen merkes som avsluttet ved innrapporteringen.

Skattepliktig uttak etter fradrag for skjerming blir ved skatteberegningen automatisk multiplisert med en fastsatt faktor som er 1,72 for 2026. Effektiv skattesats på skattepliktig uttak er 37,84 %. Uttaksverdien for aksjen, egenkapitalbeviset eller andelen utgjør ny inngangsverdi for aksjen, egenkapitalbeviset eller andelen utenfor ordningen. Ved opphør av aksjesparekontoen skattlegges innestående på kontoen, fratrukket innskudd og ubenyttet skjermingsfradrag, som uttak fra kontoen, jf. sktl. § 10-21 syvende ledd. Er innestående på kontoen lavere enn innskudd på kontoen, anses differansen som tap ved avvikling av aksjesparekontoen. Effektiv skattesats på tapet er 37,84%. Aksjerelatert formue på kontoen formuesbeskattes på samme måte som aksjer, egenkapitalbevis og andeler som eies utenfor ordningen, og gis verdsettelsesrabatt. Kontanter på kontoen formuesbeskattes på samme måte som bankinnskudd og inngår ikke i aksjerabatten.

#### 3.5 Skjermingsfradrag

Det beregnes skjerming på grunnlag av kontohavers innskudd av kontanter, aksjer, egenkapitalbevis og andeler på kontoen. Skjermingsgrunnlaget fastsettes til den laveste innskuddssaldoen på kontoen i løpet av inntektsåret, tillagt ubenyttet skjerming fra tidligere år, jf. sktl. § 10-21 femte ledd femte punktum. Skjermingen knytter seg til kontoen som sådan, og ikke til de enkelte aksjer mv. innenfor ordningen. Skjermingen tilordnes kontohaver den 31. desember i inntektsåret, jf. sktl. § 10-21 femte ledd siste punktum. Skjermingsfradraget fastsettes ved å multiplisere skjermingsgrunnlaget med skjermingsrenten, se sktl. § 10-12 annet ledd. Se eksempel på utregning under "Mer om aksjesparekonto - Skjermingsgrunnlaget settes til det laveste innskuddsbeløpet på kontoen i løpet av året ". Det er Skattedirektoratet som fastsetter skjermingsrenten etter delegasjon fra Finansdepartementet, jf. FSFIN § 10-12-1 første ledd. Direktoratet beregner og kunngjør renten for det enkelte inntektsår i januar året etter inntektsåret, jf. FSFIN § 10-12-1 annet ledd. Skjermingsrenten kunngjøres på www.skatteetaten.no/aksjer. Skjermingsfradraget kan ikke overstige skattepliktig uttak fra ordningen og utdeling av skattepliktig utbytte fra aksjer og fondsandeler på kontoen, jf. sktl. § 10-21 femte ledd første og annet punktum. Ubenyttet skjerming legges til skjermingsgrunnlaget, og kan fremføres til fradrag i senere års uttak og utbytter, jf. sktl. § 10-21 femte ledd tredje punktum.

#### 3.6 Overføring av verdipapirer mellom egne konti

ASK-eiere som har flere aksjesparekonti kan overføre verdipapirer mellom egne konti uten beskatning. Dette gjelder både overføringer mellom kontoer hos samme tilbyder og hos forskjellige tilbydere. Ved overføring av aksjer, egenkapitalbevis, andeler i aksjefond og kontanter mellom egne aksjesparekontoer, overføres samtidig en andel av kontohavers innskudd og ubenyttet skjerming fra tidligere år på den avgivende kontoen til den mottakende kontoen. Innskudd og ubenyttet skjerming overføres i samme forhold som overføring av verdier fra den avgivende kontoen, se sktl. § 10-21 syvende ledd. Det skal ikke rapporteres "True" i feltet for flytting, ved slik del-flytt.

At verdier og skatteposisjoner fordeles korrekt på overdragende og overtakende konto ihht. ovennevnte vilkår er en forutsetning for overføring med skattemessig kontinuitet. Det krever at både overtakende og overdragende tilbyder må være involvert i flytteprosessen.

Eksempel på del-overføring/splitt av aksjesparekonto:

I eksempelet ønsker skattyter å ha verdipapir A og Verdipapir B på to forskjellige ASK-kontoer.

Aksjesparekonto A:

Innskudd 10 000

Ubenyttet skjerming fra tidligere år 500

Beholdning:

Verdipapir A 6 000

Verdipapir B 14 000

Samlet verdier på konto A ved overføringstidspunkt 20 000

Aksjesparekonto A1:

Innskudd 7 000

Ubenyttet skjerming fra tidligere år: 350

Verdipapir B: 14 000

Aksjesparekonto A2:

Innskudd 3 000

Ubenyttet skjerming fra tidligere år: 150

Verdipapir A: 6 000

Årets skjerming beregnes separat for A1 og A2 etter gjeldende regler.

Kontoen skal ikke rapporteres som avsluttet ved overføring/splitt se “Avslutning av konti” i avsnitt 3.12.

#### 3.7 Utbytte

Utbytte på aksjer, egenkapitalbevis og andeler i aksjefond som står inne på aksjesparekonto er med virkning fra og med inntektsåret 2019 skattefritt, på samme måte som realisasjonsgevinster, se sktl. § 10-21 tredje ledd annet punktum. Skattlegging skjer ved evt. uttak, og først når uttaksverdien overstiger innskutt beløp på ASK. Utbytte skal ikke regnes som innskutt kapital.

#### 3.8 Arv/dødsfall

Aksjesparekontoen kan ved død overtas av arvingen med skattemessig kontinuitet. Gjenlevende ektefelle kan også med skattemessig kontinuitet bli sittende med aksjesparekontoen i uskifte. Fra og med inntektsåret 2019 kan det ved utlodning fra dødsbo overføres aksjer, egenkapitalbevis og aksjefondsandeler fra avdødes aksjesparekontoer til arvingers aksjesparekontoer uten beskatning, se sktl. § 10-21 nytt syvende ledd fjerde punktum. Overføring må skje med kontinuitet. Innskudd og ubenyttet skjerming må overføres i samme forhold som overføring av verdier mellom kontoene, jf. § 10-21 syvende ledd tredje punktum. Se eksempel i avsnitt 6 overføring av verdipapirer mellom egne konti. Kontoen som overføres med kontinuitet ved arv eller dødsfall skal ikke rapporteres som avsluttet.

#### 3.9 Gave

En aksjesparekonto kan gis som gave dersom dette gjøres med skattemessig kontinuitet. Hele aksjesparekontoen må overføres. Kontoen som overføres med kontinuitet ved gave skal ikke rapporteres som avsluttet.

#### 3.10 Skilsmisse

Ved skilsmisse kan ektefellene bestemme at aksjesparekontoen skal overføres til den annen ektefelle enn den er registrert på. Overføringen må da skje med skattemessig kontinuitet. Fra og med inntektsåret 2019 kan det ved skilsmisse overføres aksjer, egenkapitalbevis og aksjefondsandeler mellom ektefellenes aksjesparekontoer uten skattlegging, på samme måte og på samme vilkår som mellom aksjesparekontoer tilhørende samme innehaver, se sktl. § 10-21 nytt syvende ledd fjerde punktum. Innskudd og ubenyttet skjerming må overføres i samme forhold som overføring av verdier mellom kontoene, jf. sktl. § 10-21 syvende tredje punktum. Se eksempel i avsnitt 6 overføring av verdipapirer mellom egne konti. Kontoen som overføres med kontinuitet ved skilsmisse skal ikke rapporteres som avsluttet.

#### 3.11 Flytting

Feltet for “flytt” skal brukes for å markere når en aksjesparekonto er flyttet til en annen tilbyder eller innad hos eksisterende tilbyder. Feltet vil være boolsk, altså med tillatte verdier "true" eller "false". Normalverdi for feltet vil være "false" (ikke flyttet) og er frivillig i formatet.

#### 3.12 Avslutning av konti

Konti skal merkes som avsluttet når kontoen avvikles. Det er skattemessig realisasjon av konto og det skal foretas et gevinst/taps-oppgjør. Merk at feltet for avslutning er gjort obligatorisk, dvs. at feltet skal merkes med “True eller False” Det er kun for konti som faktisk er avviklet som skal merkes som avsluttet (ikke ved flytting eller splitting). Dersom kontoen ikke merkes som avsluttet vil et eventuelt tap for kontohaver ikke bli forhåndsutfylt i skattemeldingen. Konto som overføres med kontinuitet ved gave eller dødsfall skal således ikke rapporteres som avsluttet (feltet merkes "False"). Dette kan sidestilles med å flytte konto fra en tilbyder til en annen. Kontoer som flyttes i sin helhet skal merkes særskilt som flyttet se avsnitt 1. Kontoer som er merket avsluttet eller flyttet i sin helhet skal ikke rapporteres i etterfølgende inntektsår.

"Tomme" aksjesparekontoer skal også rapporteres, til og med det året de blir rapportert som "avsluttet", også selv om saldo er 0. Tomme ASK som ikke er avsluttet skal ikke rapporteres som avsluttet, men rapporteres som ordinær konto. Kun endelig avsluttet konto skal ha gevinst/tapsoppgjør.

#### 3.13 Omdanning av investeringsvirksomhet til aksjeselskap

Ved omdanning av personlig investeringsvirksomhet til aksjeselskap, etter reglene i skatteloven § 11-20 og FSFIN § 11-20, skal aksjesparekontoen merkes som avsluttet selv om dette ikke regnes som en skattemessig realisasjon av konto. Aksjesparekontoen skal rapporteres med beløp 0 i feltet for formuesverdi kontantdel og formuesverdi for hvert enkelt finansprodukt. Inngangsverdi og opptjent skjerming skal rapporteres med verdier på tidspunkt for omdanningen. Øvrige felter skal rapporteres som normalt.

Netto inngangsverdi ved omdanning videreføres som del av inngangsverdi i vederlagsaksjene i aksjeselskapet. Opptjent skjerming på aksjesparekonto videreføres på vederlagsaksjene.

Det vises for øvrig til [bindende forhåndsuttalelse til tema.](https://www.skatteetaten.no/rettskilder/type/uttalelser/bfu/omdanning-av-investeringsvirksomhet-til-aksjeselskap/)

#### 3.14 Utvalgte tilfeller nå aksjer ikke lenger kan holdes på ASK

For aksjer som lovlig står på aksjesparekontoen kan det forekomme at det utdeles utbytte i form av eiendeler som ikke kan inngå på aksjesparekontoen. Dette kan f.eks. være utbytte i form av aksjer i selskaper hjemmehørende utenfor EØS eller at man mottar unoterte aksjer. Slike eiendeler må umiddelbart tas ut av aksjesparekontoen. Skattlegging følger reglene om uttak fra aksjesparekonto. Tilsvarende gjelder dersom man mottar slike "ulovlige" aksjer ved tilbakebetaling av innbetalt kapital.

Ved uttaket av eiendelene fra kontoen, benyttes verdien av eiendelen på utbyttetidspunktet.Aksjer og fond som oppfyller kravene til å holdes på ASK på investeringstidspunktet kan fortsatt holdes på ASK, se også skatteloven § 10-21 (2). Dette gjelder selv om selskapet eller fondet for eksempel ikke lenger skulle oppfylle kravene til å være etablert innen EØS, eller kravene om aksjeandel i fondet ikke lenger oppfylles. Men man kan da ikke anskaffe seg flere av disse aksjene/fondene på aksjesparekontoen.

#### Eksempel 1:

A kjøper aksjer i selskap B som på investeringstidspunktet er et norsk børsnotert selskap. Selskapet flytter så til USA, men denne begivenheten medfører ikke at aksjene som står på ASK må ut av kontoen. Ved senere salg av aksjene skal gevinst/tap behandles som om det fremdeles var et selskap innen EØS for denne aksjonæren. Investor A kan imidlertid ikke kjøpe flere aksjer i B innenfor ASK.

#### Eksempel 2:

A kjøper i 2021 andeler i verdipapirfond som har en aksjeandel på 89 prosent. Ved inngangen til 2022 har sammensetningen i fondet endret seg slik at aksjeandelen er 0 prosent. A kan fremdeles holde andelene på ASK kontoen, men ikke kjøpe flere, og ved realisasjon/utdelinger skal disse skattlegges på lik linje med andeler i aksjefond.

#### Eksempel 3:

Selskap A som er hjemmehørende i Sveits kjøper opp selskap B (som er hjemmehørende og børsnotert i Norge) som har norske aksjonærer. Som vederlag for oppkjøpet mottar de norske aksjonærene i B aksjer i det sveitsiske selskapet A (som er bosatt utenfor EØS). Disse aksjene kan ikke stå på aksjesparekonto, de må flyttes ut og anses som uttak. Nye kjøp av denne aksjen må også skje utenfor ASK.

#### Eksempel 4:

A kjøper aksjer i et børsnotert selskap og har de på aksjesparekonto. Noe senere blir selskapet tatt av børs eller bytter til ett marked som ikke er EU/EØS-regulert. A kan fortsatt eie og flytte disse aksjene til en annen aksjesparekonto A eier uten skattelegging siden aksjene var børsnoterte på investeringstidspunktet. A kan ikke foreta nye kjøp av aksjen på aksjesparekonto.

### 4. Spesifikasjon av utvalgte felter i formatet

#### 4.1 Inngangsverdi

Den summen som kan tas ut skattefritt ved utgangen av inntektsåret.

#### 4.2 Innskudd

Feltet innskudd utgjør alle innskudd i løpet av kalenderåret, altså sum innskutt kapital i løpet av året (brutto). (Tidligere skulle feltet rapporteres netto, med sum innskutt kapital minus uttak i samme periode). Inngangsverdi (markedsverdi på overføringstidspunktet) på overførte aksjer inngår som en del av det som skal rapporteres som innskudd her. Utbytte er ikke en del av innskudd.

#### 4.3 Uttak

Her skal det rapporteres sum uttak fra konto i løpet av inntektsåret.

#### 4.4 Ubenyttet skjerming:

Her føres ubenyttet skjerming fra tidligere år. Fremførbar skjerming rapporteres ikke.

#### 4.5 Skattepliktig gevinst/tap

Her føres skattepliktig uttak/gevinst der uttaksverdien overstiger akkumulert inngangsverdi inkl. skjerming på aksjesparekonto. Tap skal kun forekomme når konto avsluttes. Tap vil forekomme når innestående på kontoen er lavere enn innskudd på kontoen. Konto må da merkes som avsluttet, se avsnitt 3.12.

#### 4.6 Forvaltningskostnad

Her innrapporteres fradragsberettigede kostnader som har direkte tilknytning til skattepliktige inntekter. Her kan man rapportere kostnader (kontantstrømmer) som går direkte mellom tilbyder og investor via en bankkonto som ikke hører inn under ASK, eller belaste aksjesparekontoen direkte via kontantbeholdningen eller ved innløsning av andeler/aksjer. Kostnader som belastes aksjesparekontoen direkte behandles på lik linje med annet uttak. Kostnader som er innbakt indirekte, f.eks. som nedsettelse av verdi av verdipapirfond skal ikke fradragsføres her.

Forvaltningskostnader knyttet til aksjesparekonto, verdipapirfond og fondskonto kan fra og med inntektsåret 2024 rapporteres samlet via tredjepartsordningen Finansprodukter. S[e rettledningen til tredjepartsordningen Finansprodukter for mer informasjon](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/bank-finans-og-forsikring/finansprodukter/rettledning/).

Dersom dere innrapporterer samlede forvaltningskostnader på ordningen «Finansprodukter» skal dere ikke føre forvaltningskostnader knyttet til aksjesparekonto her.

#### 4.7 Returprovisjon

Her innrapporteres beløp/verdi som utbetales direkte til investor. Dette beløpet er skattepliktig som kapitalinntekt. Beløp kan betales til konto på utsiden av aksjesparekonto eller direkte til aksjesparekonto. Dersom returprovisjon utbetales til konto utenfor aksjesparekontoen skal beløpet rapporteres i feltet "returprovisjon" uten at dette får konsekvenser for andre felt på aksjesparekontoen. Velger man å utbetale returprovisjon til aksjesparekonto skal man rapportere beløp i feltet "returprovisjon" og feltet “innskudd”, og inngangsverdi økes tilsvarende utbetalt returprovisjon. Beløpet vil være forhåndsutfylt som kapitalinntekt på investors skattemelding. Dette gjelder uavhengig av om returprovisjon utbetales som kontanter eller andeler i verdipapir, i eller utenfor aksjesparekontoen.

#### 4.8 Avsluttet

Her merkes konto som avsluttet dersom konto er avsluttet og tømt. Ved flytting av aksjesparekonto til annen tilbyder skal ikke konto merkes som avsluttet. Feltet er gjort obligatorisk fra og med inntektsåret 2020.

#### 4.9 Brexit

31.januar 2020 forlot Storbritannia EU (Brexit). Fra og med 01.01.2021 kan ingen kjøpe NYE britiske aksjer/aksjefond, eller motta britiske utbytteaksjer inn på Aksjesparekonto. Dersom britiske aksjer/aksjefond er kjøpt, eller britiske aksjer er gitt i utbytte i 2026 må disse tas ut av aksjesparekontoen umiddelbart. Ved uttaket av eiendelene fra kontoen, benyttes verdien av eiendelen på kjøpstidspunktet/utbyttetidspunktet. Uttaket reduserer innskutt kapital, og skattlegges i den utstrekning det overstiger innskutt kapital tillagt skjerming.

### 5. Internasjonal rapportering – CRS/FATCA-opplysninger

Skatteetaten avviklet muligheten til å merke finansielle konti for internasjonal rapportering via tredjepartsordningene som leverer opplysninger til skattemeldingen fra og med inntektsåret 2023. Det innebærer at opplysningspliktige til tredjepartsordningen Aksjesparekonto ikke lengre kan merke finansielle konti til internasjonal rapportering. Opplysningspliktige må i stedet rapportere alle finansielle konti som skal utveksles til særskilt ordning Internasjonal rapportering CRS/FATCA.

Særskilt rapportering av finansielle konti for utveksling til tredjepartsordningen Internasjonal rapportering CRS/FATCA vil komme i tillegg til nasjonal rapportering av tredjepartsopplysninger til bruk på skattemeldingen. Det betyr at en finansiell konto merket for utveksling må rapporteres en gang for bruk på skattemeldingen og en gang til særskilt ordning for utveksling CRS/FATCA.

Rettledninger og tekniske spesifikasjoner til alle Skatteetatens tredjepartsordninger finnes på Skatteetatens nettsider under «Rapportering og bransjer».

### 6. Når skal du rapportere

Tredjepartsopplysninger skal sendes til Skatteetaten innen 10. februar året etter inntektsåret.

Tredjepartsopplysninger kan leveres fra 1. januar året etter inntektsåret.

For å unngå at oppgaver mangler på skattemeldingen, er det meget viktig at fristen overholdes. Endrings- eller erstatningsoppgaver som sendes inn etter 1. mars vil ikke automatisk komme med i skattemeldingen før skattepliktige leverer denne.

Skattemeldingene blir oppdatert med nye opplysninger frem til 30. april ved endrings- og erstatningsoppgaver, så lenge skattyter ikke allerede har sendt inn skattemeldingen sin. Skattytere som har levert skattemelding, og skattytere som har levert skattemeldingen på papir vil ikke få oppdatert utkast til skattemelding, og må selv oppdatere skattemeldingen og sende inn på nytt. Etter 30. april vil erstatnings- og endringsoppgaver ikke medføre nye skattemeldingsutkast. Alle endringer må gjøres av skattyter selv. Opplysningspliktige som må korrigere oppgaver etter 1. mars, må kontakte Skatteetaten for å avtale ny leveranse via e-post: grunnlagsdata@skatteetaten.no.

20. oktober er siste frist for innsending av endrings- eller erstatningsoppgaver.

#### 6.1 Hvordan skal du rapportere

Leveranser består av en eller flere oppgaver. Oppgaver skilles fra hverandre ved hjelp av feltene "inntektsår", "opplysningspliktig", "oppgaveeier" og "kontonummer". Disse identifikatorene utgjør til sammen oppgavens unike identifikator

- Opplysningspliktig
- Opplysningspliktige identifiseres ved organisasjonsnummer (ikke aktuelt for ASK)
- Oppgaveeier (Den som står som eier av kontoen)
- Oppgaveeier identifiseres ved fødselsnummer, D-nummer eller organisasjonsnummer (ikke aktuelt for ASK)
- Dersom oppgaveeier ikke har fødselsnummer eller organisasjonsnummer (ikke aktuelt for ASK) skal opplysningspliktige angi en unik verdi for kontoeier i feltet for Alternativ identifikator. Verdien brukes som del av unik nøkkel på oppgaven, og er grunnlag for endring/sletting av innsendte opplysninger.
- Kontonummer
- Nummer som identifiserer konto

Oppgaveeier identifiseres ved fødselsnummer, D-nummer eller organisasjonsnummer (ikke aktuelt for ASK). Internasjonale oppgaveeiere identifiseres med TIN-nummer.

#### 6.2 Innsending

Opplysningene sendes til Skatteetaten enten ved å benytte skjema Tredjepartsopplysninger som vedlegg, eller via maskin til maskin.

Tredjepartsopplysninger kan sendes direkte fra sluttbrukersystemet til Skatteetaten med maskin-til-maskin-integrasjon (M2M) i JSON-format. Dette krever at systemet ditt er koblet til Skatteetatens mottaks-API med en systembruker. [Les mer om Skatteetatens API-er her](https://eur04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fskatteetaten.github.io%2Fapi-dokumentasjon%2F&data=05%7C02%7CNorvald.Andreassen%40skatteetaten.no%7C6bf6dcf4c4454d54f38908dda27fe7e5%7Cc9b0d3b5c0354c088136760ae8c28600%7C0%7C0%7C638845392403538522%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=S6LFJ%2BKzSBhxi%2BWHnA7pDP%2B3YJJxMFU2tRW1nhCgsc0%3D&reserved=0).

Tredjepartsopplysninger som vedlegg. Filen som lastes opp i skjemaet skal være i XML-format som følger Skatteetatens spesifikasjoner (se ”Beskrivelse av filformatet”).

#### 6.3 Beskrivelse av filformatet

Formatbeskrivelsen viser hvordan JSON og XML-fil for rapportering av tredjepartsopplysninger for aksjesparekonto skal bygges opp. Dokumentene finner du ved å følge denne lenken:

[Formater og tekniske spesifikasjoner - Aksjesparekonto.](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/bank-finans-og-forsikring/aksjesparekonto/formater-og-tekniske-spesifikasjoner/)

Formatbeskrivelsen skal benyttes av opplysningspliktige/innsendere som skal rapportere tredjepartsopplysninger via maskin-til-maskin (JSON) og vedleggsskjemaet Tredjepartsopplysninger som vedlegg på skatteetaten.no.

Tredjepartsopplysninger kan sendes direkte fra sluttbrukersystemet til Skatteetaten med maskin-til-maskin-integrasjon (M2M). Rapportering kan leveres i JSON-format eller som XML-fil, avhengig av hvilken løsning og ordning som benyttes. Dette krever at systemet er koblet til Skatteetatens mottaks-API med en systembruker.

XML-baserte leveranser er særlig aktuelle for virksomheter som rapporterer større datamengder og som ønsker å sende inn opplysninger direkte fra egne fagsystemer. XML-filen må være bygget opp i samsvar med gjeldende informasjonsmodell, formatbeskrivelse (XSD) og tekniske krav for den aktuelle ordningen.

Les mer om Skatteetatens API-er i [API-dokumentasjonen](https://eur04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fskatteetaten.github.io%2Fapi-dokumentasjon%2F&data=05%7C02%7CMarenFuruholt.Frivold%40skatteetaten.no%7Cfdd2a2d3d9664d2a4a6708df0f277d55%7Cc9b0d3b5c0354c088136760ae8c28600%7C0%7C0%7C639246334415136209%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=aakVp%2BBsjRZcLp07CCnPWMvon6RbnQvOQ3KWEjYfXBw%3D&reserved=0) og [TPO filmottak API (XML)](https://eur04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fskatteetaten.github.io%2Fapi-dokumentasjon%2Fapi%2Finnrapportering-tpo-filmottak&data=05%7C02%7CMarenFuruholt.Frivold%40skatteetaten.no%7Cfdd2a2d3d9664d2a4a6708df0f277d55%7Cc9b0d3b5c0354c088136760ae8c28600%7C0%7C0%7C639246334415165331%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=IEHJ81W07sL8L0fAnYlIlCNdxAhFBoeGsXpNBcKWGA0%3D&reserved=0)»

### 7. Rette feil

#### 7.1 Korrigere oppgaver med feil

En tidligere innsendt oppgave korrigeres ved å sende inn en ny oppgave med de korrekte verdiene. Den nye oppgaven vil da erstatte den tidligere innsendte oppgaven. Ved korreksjon eller sletting av en tidligere rapportert oppgave, er kravet at den nye oppgaven har samme unike identifikator som den opprinnelige oppgaven. Grunnen til dette er at Skatteetatens systemer skal oppfatte dette som en korreksjon, og ikke som en ny oppgave. For aksjesparekonto er det oppgaveeiers kontonummer, fødselsnummer, d-nummer, sammen med inntektsår og opplysningspliktig som er unik identifikator (se "Unik identifikasjon av oppgave"). Når korrigert oppgave med korrekte verdier mottas av Skatteetaten, vil oppgaven erstatte tidligere innsendt oppgave.

#### 7.2 Korrigere en oppgave med feil i identifikator

Dersom det er feil i et eller flere av identifikatorfeltene i en tidligere innsendt oppgave, må denne oppgaven eksplisitt slettes. Det vil si at det da skal sendes inn en oppgave med korrekte verdier og en sletteoppgave for å slette den oppgaven som var feil. Sletteoppgaven må ha de samme identifikatorfeltene som oppgaven med feil identifikator.

#### 7.3 Slette en oppgave med feil

Sletting av en tidligere innsendt oppgave gjøres ved å rapportere en <sletteoppgave> med samme unike identifikator som oppgaven som skal slettes.

### 8. Temahenvisning i skattemeldingen

Tredjepartsopplysningene benyttes til forhåndsutfylling av skattemeldingen til personlige aksjonærer. Skattemeldingen er temabasert slik at opplysninger om aksjesparekonto finnes under tema «Finans» og undertema «Aksjesparekonto»

[Les mer om skattemeldingen](https://www.skatteetaten.no/person/skatt/skattemelding/skattemelding-for-person/).

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
*Automatisk hentet fra [Skatteetaten](https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/tredjepartsopplysninger/bank-finans-og-forsikring/aksjesparekonto/rettledning/) av norges-lover-bot.*

## Endringshistorikk

- **2026-10-27** Første gang hentet
