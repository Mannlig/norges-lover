"""
Scraper for Direktoratet for byggkvalitet (DiBK).
Kilde: https://www.dibk.no
"""

import re

from .nettsted import NettstedScraper


class DibkScraper(NettstedScraper):
    name = "dibk"
    kildenavn = "DiBK"
    kilde_beskrivelse = "Direktoratet for byggkvalitet (DiBK)"
    base_url = "https://www.dibk.no"
    source_url = base_url
    state_fil = "dibk-state.json"
    startpunkter = [
        "https://www.dibk.no/regelverk/byggteknisk-forskrift-tek17/",
        "https://www.dibk.no/regelverk/byggesaksforskriften-sak10/",
        "https://www.dibk.no/regelverk/",
        "https://www.dibk.no/byggeregler/",
        "https://www.dibk.no/byggesok/",
        "https://www.dibk.no/soknadspliktig-eller-ikke/",
        "https://www.dibk.no/tilsyn/",
        "https://www.dibk.no/veiledere/",
    ]
    inkluder_prefiks = (
        "https://www.dibk.no/regelverk/",
        "https://www.dibk.no/byggeregler/",
        "https://www.dibk.no/byggesok/",
        "https://www.dibk.no/soknadspliktig-eller-ikke/",
        "https://www.dibk.no/tilsyn/",
        "https://www.dibk.no/veiledere/",
        "https://www.dibk.no/produkter-og-materialer/",
    )
    ekskluder = re.compile(
        r"/(nyheter|presse|om-dibk|kontakt|arrangementer|kurs)(/|$)",
        re.IGNORECASE,
    )
    innhold_selektorer = ["main", "article", ".article-body", "#main", "[role='main']"]
    dato_selektor = "time[datetime], .date, .published"
    # TEK10 er opphevet og endres ikke – behold, men ikke hent på nytt hver uke.
    gjenbesøk = [("regelverk/tek", None)]
