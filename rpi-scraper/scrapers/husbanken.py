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
    # Nettstedet ble omstrukturert (f.eks. /bostotte/ → /person/bostotte/),
    # så faste prefikser avviste alle lenker – kilden leverte 2 filer på fem
    # måneder. Hele domenet handler om boligfinansiering, så vi crawler alt
    # unntatt seksjonene under.
    startpunkter = [
        "https://www.husbanken.no/person/",
        "https://www.husbanken.no/bostotte/",
        "https://www.husbanken.no/startlan/",
        "https://www.husbanken.no/tilskudd/",
        "https://www.husbanken.no/grunnlan/",
        "https://www.husbanken.no/kommuner/",
        "https://www.husbanken.no/regelverk/",
    ]
    ekskluder = re.compile(
        r"/(om-husbanken|presse|nyheter|aktuelt|kontakt|arrangementer|kurs|"
        r"statistikk|ansatte|jobb|ledige-stillinger|personvern|cookies)(/|$)",
        re.IGNORECASE,
    )
    innhold_selektorer = ["main", "article", "[role='main']", ".article-body", "#main-content"]
    dato_selektor = "time[datetime], .date, .published"
