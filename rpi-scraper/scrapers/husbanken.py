"""
Scraper for Husbanken – bostøtte, startlån, tilskudd og boligvirkemidler.
Kilde: https://www.husbanken.no
"""

import re

from .nettsted import NettstedScraper


class HusbankScraper(NettstedScraper):
    name = "husbanken"
    kildenavn = "Husbanken"
    base_url = "https://www.husbanken.no"
    source_url = base_url
    state_fil = "husbanken-state.json"
    startpunkter = [
        "https://www.husbanken.no/bostotte/",
        "https://www.husbanken.no/startlan/",
        "https://www.husbanken.no/tilskudd/",
        "https://www.husbanken.no/boligtilskudd/",
        "https://www.husbanken.no/utleieboliger/",
        "https://www.husbanken.no/grunnlan/",
        "https://www.husbanken.no/kommuner/",
        "https://www.husbanken.no/regelverk/",
        "https://www.husbanken.no/tema/",
    ]
    inkluder_prefiks = (
        "https://www.husbanken.no/bostotte/",
        "https://www.husbanken.no/startlan/",
        "https://www.husbanken.no/tilskudd/",
        "https://www.husbanken.no/boligtilskudd/",
        "https://www.husbanken.no/utleieboliger/",
        "https://www.husbanken.no/grunnlan/",
        "https://www.husbanken.no/kommuner/",
        "https://www.husbanken.no/regelverk/",
        "https://www.husbanken.no/tema/",
        "https://www.husbanken.no/laane-og-tilskuddsordninger/",
    )
    ekskluder = re.compile(
        r"/(om-husbanken|presse|nyheter|kontakt|arrangementer|kurs|statistikk|ansatte)(/|$)",
        re.IGNORECASE,
    )
    innhold_selektorer = ["main", "article", "[role='main']", ".article-body", "#main-content"]
    dato_selektor = "time[datetime], .date, .published"
