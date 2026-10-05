"""
Scraper for Arbeidstilsynet – HMS-regler, arbeidsforhold og veiledere.
Kilde: https://www.arbeidstilsynet.no
"""

import re

from .nettsted import NettstedScraper


class ArbeidstilsynetScraper(NettstedScraper):
    name = "arbeidstilsynet"
    kildenavn = "Arbeidstilsynet"
    base_url = "https://www.arbeidstilsynet.no"
    source_url = base_url
    state_fil = "arbeidstilsynet-state.json"
    startpunkter = [
        "https://www.arbeidstilsynet.no/arbeidsforhold/",
        "https://www.arbeidstilsynet.no/hms/",
        "https://www.arbeidstilsynet.no/regelverk/",
        "https://www.arbeidstilsynet.no/tema/",
        "https://www.arbeidstilsynet.no/arbeidsmiljo/",
        "https://www.arbeidstilsynet.no/arbeidskontrakt/",
        "https://www.arbeidstilsynet.no/permittering-og-oppsigelse/",
        "https://www.arbeidstilsynet.no/ferie-og-fritid/",
        "https://www.arbeidstilsynet.no/lonn/",
        "https://www.arbeidstilsynet.no/sikkerhet/",
    ]
    inkluder_prefiks = (
        "https://www.arbeidstilsynet.no/arbeidsforhold/",
        "https://www.arbeidstilsynet.no/hms/",
        "https://www.arbeidstilsynet.no/regelverk/",
        "https://www.arbeidstilsynet.no/tema/",
        "https://www.arbeidstilsynet.no/arbeidsmilj",
        "https://www.arbeidstilsynet.no/arbeidskontrakt/",
        "https://www.arbeidstilsynet.no/permittering",
        "https://www.arbeidstilsynet.no/ferie",
        "https://www.arbeidstilsynet.no/lonn/",
        "https://www.arbeidstilsynet.no/sikkerhet/",
        "https://www.arbeidstilsynet.no/veiledere/",
    )
    ekskluder = re.compile(
        r"/(om-oss|presse|nyheter|kontakt|arrangementer|kurs|statistikk)(/|$)",
        re.IGNORECASE,
    )
    innhold_selektorer = ["main", "article", "[role='main']", ".article-body", "#main-content"]
    ekstra_metadata = ["- **Kategori:** Arbeidsmiljø og HMS"]
