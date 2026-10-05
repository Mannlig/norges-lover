"""
Sonde mot de ekte kildene – kjøres manuelt fra GitHub Actions
(.github/workflows/test-kilder.yml), ikke på Pi-en.

Svarer på:
  1. Slipper nettstedene til (blokkeres GitHubs IP-er?)
  2. Gir den nye HTML-konverteren tabeller og hele setninger på ekte sider?
  3. Hvilke Skatte-ABC-utgaver finnes?
  4. Finner hver kilde lenker fra startsiden (Husbanken har nesten ingen filer)?
  5. Godtar Stortingets API sesjonid, og hva heter feltene?

Skriver en Markdown-rapport til stdout (og til $GITHUB_STEP_SUMMARY hvis satt).
"""

import os
import sys
import tempfile
import time
from pathlib import Path

os.environ.setdefault("REPO_ROOT", tempfile.mkdtemp())
os.environ.setdefault("STATE_DIR", tempfile.mkdtemp())
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scrapers import (  # noqa: E402
    ArbeidstilsynetScraper, DibkScraper, HusbankScraper, NavScraper,
    SkatteetatenScraper, StortingetScraper,
)
from scrapers.skatteetaten import skatte_abc_kandidater  # noqa: E402
from scrapers.stortinget import API_BASE  # noqa: E402

UT: list[str] = []


def skriv(s: str = ""):
    UT.append(s)
    print(s, flush=True)


def probe_side(scraper, url: str, vis_innhold: bool = False):
    start = time.time()
    page = scraper.fetch(url)
    tid = time.time() - start
    if page is None:
        skriv(f"| {url} | **{scraper.siste_status}** | – | – | – | {tid:.0f}s |")
        return None
    md = scraper.side_til_markdown(page, scraper.innhold_selektorer)
    lenker = scraper._lenker(page)
    endelig = str(getattr(page, "url", ""))
    tabeller = md.count("\n| --- ")
    skriv(f"| {url} | OK{' → ' + endelig if endelig.rstrip('/') != url.rstrip('/') else ''} "
          f"| {len(md)} | {tabeller} | {len(lenker)} | {tid:.0f}s |")
    if vis_innhold:
        UT.append(f"\n<details><summary>Innhold fra {url}</summary>\n\n```markdown\n{md[:3000]}\n```\n</details>\n")
    return page


def main():
    skriv("# Kildeprobe\n")
    skriv("| URL | Status | Tegn | Tabeller | Lenker | Tid |")
    skriv("|---|---|---|---|---|---|")

    s = SkatteetatenScraper()
    s._les_robots = lambda: False
    probe_side(s, "https://www.skatteetaten.no/satser/trinnskatt/", vis_innhold=True)
    probe_side(s, "https://www.skatteetaten.no/satser/minstefradrag/", vis_innhold=True)
    probe_side(s, "https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/")
    for url in skatte_abc_kandidater():
        probe_side(s, url)

    for klasse in (NavScraper, DibkScraper, ArbeidstilsynetScraper, HusbankScraper):
        sc = klasse()
        sc._les_robots = lambda: False
        page = probe_side(sc, sc.startpunkter[0], vis_innhold=klasse is HusbankScraper)
        if klasse is HusbankScraper and page is not None:
            rå = [str(a.attrib.get("href", "")) for a in page.css("a[href]")][:40]
            UT.append("\n<details><summary>Husbanken: rå href-er på startsiden</summary>\n\n```\n"
                      + "\n".join(rå) + "\n```\n</details>\n")

    skriv("\n## robots.txt\n")
    for klasse in (SkatteetatenScraper, NavScraper, DibkScraper, ArbeidstilsynetScraper, HusbankScraper):
        sc = klasse()
        rp = sc._les_robots()
        if rp is False:
            skriv(f"- {sc.kildenavn}: ikke tilgjengelig (ingen begrensning)")
        else:
            blokkert = [u for u in sc.startpunkter if not rp.can_fetch("NorgesLoverBot", u)]
            skriv(f"- {sc.kildenavn}: {len(blokkert)} av {len(sc.startpunkter)} startpunkter blokkert {blokkert[:3]}")

    skriv("\n## Stortinget\n")
    st = StortingetScraper()
    data = st.get_json(f"{API_BASE}/sesjoner", {"format": "json"}) or {}
    skriv(f"- /sesjoner nøkler: {sorted(data.keys())}")
    sesjoner = st._hent_sesjoner()
    skriv(f"- valgte sesjoner: {sesjoner}")
    saker = []
    for sesjon in sesjoner[:2]:
        rå = st.get_json(f"{API_BASE}/saker", {"format": "json", "sesjonid": sesjon}) or {}
        saker = st._hent_saker(sesjon)
        skriv(f"- {sesjon}: svar sesjon_id={rå.get('sesjon_id')!r}, {len(saker)} saker")
    if saker:
        skriv(f"- felt i en sak: {sorted(saker[0].keys())}")

    sammendrag = os.environ.get("GITHUB_STEP_SUMMARY")
    if sammendrag:
        Path(sammendrag).write_text("\n".join(UT), encoding="utf-8")


if __name__ == "__main__":
    main()
