"""
Scraper for NAV.
Kilde: https://www.nav.no
"""

import re

from .nettsted import NettstedScraper


class NavScraper(NettstedScraper):
    name = "nav"
    kildenavn = "NAV"
    kilde_beskrivelse = "NAV (Arbeids- og velferdsdirektoratet)"
    base_url = "https://www.nav.no"
    source_url = base_url
    state_fil = "nav-state.json"
    skråstrek_slutt = False
    startpunkter = [
        "https://www.nav.no/dagpenger",
        "https://www.nav.no/sykepenger",
        "https://www.nav.no/foreldrepenger",
        "https://www.nav.no/barnetrygd",
        "https://www.nav.no/kontantstotte",
        "https://www.nav.no/uforetrygd",
        "https://www.nav.no/alderspensjon",
        "https://www.nav.no/arbeidsavklaringspenger",
        "https://www.nav.no/sosialhjelp",
        "https://www.nav.no/hjelpemidler",
        "https://www.nav.no/overgangsstonad-enslig",
        "https://www.nav.no/omsorgspenger",
        "https://www.nav.no/pleiepenger-sykt-barn",
        "https://www.nav.no/svangerskapspenger",
        "https://www.nav.no/grunnbelopet",
        "https://www.nav.no/pensjonsgivende-inntekt",
        "https://www.nav.no/arbeid",
        "https://www.nav.no/permittering",
        "https://www.nav.no/gjenlevendepensjon",
        "https://www.nav.no/barnepensjon",
        # Arbeidsgiver-sider
        "https://www.nav.no/arbeidsgiver",
        "https://www.nav.no/arbeidsgiver/sykepenger",
        "https://www.nav.no/arbeidsgiver/foreldrepenger",
        "https://www.nav.no/arbeidsgiver/rekruttering",
        # Satser og regelverk
        "https://www.nav.no/satser",
        "https://www.nav.no/saksbehandlingstider",
        "https://www.nav.no/klagerettigheter",
        # Spesifikke ytelser
        "https://www.nav.no/omstillingsstonad",
        "https://www.nav.no/yrkesskade",
        "https://www.nav.no/lonnsgaranti",
        "https://www.nav.no/tiltakspenger",
        "https://www.nav.no/supplerende-stonad",
    ]
    # Lovtekst under /nav/lov|forskrift|rundskriv svarer 404 hos NAV.
    # fyllut* er skjemasteg, redirects gir kopier, no/lokalt er kontorsider.
    ekskluder = re.compile(
        r"/(kontakt|kontakt-oss|om-nav|presse|nyheter|arrangementer|minside|"
        r"samarbeidspartner|[a-z]{2}/person|nav/lov|nav/forskrift|nav/rundskriv|"
        r"nav-loven|fyllut|fyllut-ettersending|redirects|no/lokalt)(/|$)",
        re.IGNORECASE,
    )
    innhold_selektorer = ["main", "article", "[role='main']", ".article-body", "#maincontent"]
    gjenbesøk = [("satser", 2), ("grunnbelopet", 2)]
