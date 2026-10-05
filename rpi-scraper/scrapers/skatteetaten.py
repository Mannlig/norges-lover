"""
Scraper for Skatteetaten.
Kilde: https://www.skatteetaten.no
"""

import re
from datetime import datetime, timezone

from .nettsted import NettstedScraper

_SKATTE_ABC_BASE = "https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/"
_SKATTE_ABC_ÅR = re.compile(r"^rettskilder/type/handboker/skatte-abc/(\d{4})(?:-(\d{4}))?(/|$)")


def skatte_abc_kandidater(i_dag: datetime | None = None) -> list[str]:
    """
    Inngangs-URL-er for Skatte-ABC-årsutgaver.

    Oversiktssiden lister utgavene i en JS-generert meny, så lenkene finnes
    ikke i HTML-en scraperen ser – uten disse blir arkivet stående på den
    utgaven som tilfeldigvis ble crawlet først (2023). Utgavene bruker to
    navnemønstre («2023» og «2022-2023»), begge gjettes ut fra årstall så
    listen fornyer seg selv. Utgaver som ikke finnes gir 404 og hoppes over.
    """
    år = (i_dag or datetime.now(timezone.utc)).year
    kandidater = []
    for y in range(år - 2, år + 1):
        kandidater.append(f"{_SKATTE_ABC_BASE}{y}/")
        kandidater.append(f"{_SKATTE_ABC_BASE}{y}-{y + 1}/")
    return kandidater


class SkatteetatenScraper(NettstedScraper):
    name = "skatteetaten"
    kildenavn = "Skatteetaten"
    base_url = "https://www.skatteetaten.no"
    source_url = base_url
    state_fil = "skatt-state.json"
    startpunkter = [
        "https://www.skatteetaten.no/satser/",
        "https://www.skatteetaten.no/person/skatt/",
        "https://www.skatteetaten.no/person/aksjer-og-verdipapirer/",
        "https://www.skatteetaten.no/person/bolig-og-eiendom/",
        "https://www.skatteetaten.no/person/arv-og-gaver/",
        "https://www.skatteetaten.no/person/skattekort/",
        "https://www.skatteetaten.no/person/skattemelding/",
        "https://www.skatteetaten.no/person/utland/",
        "https://www.skatteetaten.no/person/fradrag/",
        "https://www.skatteetaten.no/person/selvstendig-naringsdrivende/",
        "https://www.skatteetaten.no/bedrift-og-organisasjon/skatt/",
        "https://www.skatteetaten.no/bedrift-og-organisasjon/mva/",
        "https://www.skatteetaten.no/bedrift-og-organisasjon/arbeidsgiver/",
        "https://www.skatteetaten.no/bedrift-og-organisasjon/starte-bedrift/",
        "https://www.skatteetaten.no/bedrift-og-organisasjon/rapportering-og-bransjer/",
        "https://www.skatteetaten.no/naringsdrivende/",
        # Rettskilder – Skatte-ABC (Skatteetatens tolkningshåndbok) og andre
        "https://www.skatteetaten.no/rettskilder/",
        "https://www.skatteetaten.no/rettskilder/type/handboker/",
        "https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/",
    ]
    inkluder_prefiks = (
        "https://www.skatteetaten.no/person/",
        "https://www.skatteetaten.no/bedrift-og-organisasjon/",
        "https://www.skatteetaten.no/naringsdrivende/",
        "https://www.skatteetaten.no/satser/",
        "https://www.skatteetaten.no/rettskilder/",
        "https://www.skatteetaten.no/tema/",
    )
    ekskluder = re.compile(
        r"/(kontakt|om-skatteetaten|presse|kurs|arrangementer|"
        r"skjema|ettersendelse|klage)(/|$)",
        re.IGNORECASE,
    )
    innhold_selektorer = [
        "main article", "main", "article", "[role='main']",
        ".article-content", "#main-content", ".page-content",
    ]
    dato_selektor = "time[datetime], .last-updated, [class*='updated']"
    # Satsene endres ved årsskiftet og i statsbudsjettet – sjekk dem oftere.
    gjenbesøk = [("satser", 2)]

    def hub_urler(self) -> list[str]:
        return self.startpunkter + skatte_abc_kandidater()

    def gjenbesøk_dager(self, nøkkel: str) -> int | None:
        # Skatte-ABC for tidligere år endres ikke – hent én gang, aldri på nytt.
        # Den frosne 2023-utgaven brukte tidligere ~6 av 7 dagers kvote.
        m = _SKATTE_ABC_ÅR.match(nøkkel)
        if m:
            utgave = int(m.group(2) or m.group(1))
            if utgave < datetime.now(timezone.utc).year - 1:
                return None
        return super().gjenbesøk_dager(nøkkel)
