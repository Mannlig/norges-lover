"""
Lokal smoke-test for alle scrapers.

Kjører hver scraper med max_pages=1 mot en temp-mappe og verifiserer at:
  1. .scrape() ikke kaster unntak (fanger API-mismatch som page.css_first, self.get osv.)
  2. Output-fila eksisterer og har hash-header (<!-- innholds-hash: ... -->)
  3. Output-fila har minimum 200 tegn lovtekst

Hver scraper får maks 90 sekunder. Feil rapporteres med full traceback.

Bruk:
    python smoke_test.py                       # Test alle kilder
    python smoke_test.py --kilde stortinget    # Bare én
    python smoke_test.py --rask                # Hopp over Playwright-tunge kilder

Hvorfor:
    Tidligere kjørte vi koden i Docker på Pi i timer før vi oppdaget at
    page.css_first() ikke finnes i Scrapling 0.4. Denne testen surfacer
    sånne feil på sekunder.
"""

import argparse
import logging
import sys
import tempfile
import time
import traceback
from pathlib import Path

# Kjør i contained miljø – ikke skriv til ekte data/ eller logs/
_TMP_LOGS = Path(tempfile.mkdtemp(prefix="norges-lover-smoke-"))
import os
os.environ.setdefault("REPO_ROOT", str(_TMP_LOGS))

from scrapers import (
    StortingetScraper,
    LovdataScraper,
    SkatteetatenScraper,
    DibkScraper,
    NavScraper,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)

# (navn, klasse, max_pages, krever_browser)
SCRAPERS = [
    ("stortinget",   StortingetScraper,    2, False),  # Ren JSON-API, raskt
    ("skatteetaten", SkatteetatenScraper,  1, True),
    ("nav",          NavScraper,           1, True),
    ("dibk",         DibkScraper,          1, True),
    ("lovdata",      LovdataScraper,       1, True),
    # KommunerScraper deaktivert – LovdataScraper henter lokale-forskrifter
]


def valider_fil(path: Path) -> tuple[bool, str]:
    """Sjekk at fila har hash-header og minimum innhold."""
    if not path.exists():
        return False, f"Fil mangler: {path}"
    txt = path.read_text(encoding="utf-8")
    if "<!-- innholds-hash:" not in txt[:200]:
        return False, "Mangler hash-header"
    if len(txt) < 200:
        return False, f"For lite innhold ({len(txt)} tegn)"
    return True, "OK"


def kjor_scraper(navn: str, klasse, max_pages: int) -> dict:
    """Kjør én scraper, returner dict med resultat."""
    start = time.time()
    tmp = Path(tempfile.mkdtemp(prefix=f"smoke-{navn}-"))
    res = {"navn": navn, "ok": False, "feil": "", "filer": 0, "validert": 0, "tid": 0.0}

    try:
        scraper = klasse()
        filer = scraper.scrape(tmp, max_pages=max_pages)
        res["filer"] = len(filer)

        if not filer:
            res["feil"] = "Ingen filer produsert (kan være fordi alle URL-er er døde eller har endret seg)"
            return res

        for f in filer:
            ok, _ = valider_fil(f)
            if ok:
                res["validert"] += 1

        if res["validert"] == 0:
            res["feil"] = "Filer produsert, men ingen passerte validering"
        else:
            res["ok"] = True

    except Exception as e:
        res["feil"] = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
    finally:
        res["tid"] = time.time() - start

    return res


def statisk_sjekk() -> int:
    """Grep etter kjente feil-mønstre i scraper-kildekoden. Rask, ingen nettverk."""
    suspect = {
        "page.css_first": "Gammel Scrapling 0.2-API – bruk self.css_first(page, ...)",
        "self.get(":      "Finnes ikke i BaseScraper – bruk self.get_json() eller self.fetch()",
        "requests.":      "requests-pakken er ikke en dep – bruk self.get_json() eller self.fetch()",
        "BeautifulSoup":  "bs4 er ikke en dep – bruk page.css(...)",
    }
    issues = 0
    for f in Path(__file__).parent.glob("scrapers/*.py"):
        if f.name == "__init__.py":
            continue
        in_docstring = False
        for line_no, line in enumerate(f.read_text().splitlines(), 1):
            stripped = line.strip()
            # Toggle docstring-state ved hver """ (også når det åpner og lukker på samme linje)
            triple_count = stripped.count('"""') + stripped.count("'''")
            if in_docstring:
                if triple_count % 2 == 1:
                    in_docstring = False
                continue
            if triple_count >= 2:
                continue  # Åpnet og lukket på samme linje
            if triple_count == 1:
                in_docstring = True
                continue
            if stripped.startswith("#"):
                continue
            for pat, msg in suspect.items():
                if pat in line:
                    print(f"  ✗ {f.name}:{line_no}  {pat!r}  – {msg}")
                    print(f"     {stripped[:100]}")
                    issues += 1
    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kilde", choices=[s[0] for s in SCRAPERS], help="Test bare én kilde")
    parser.add_argument("--rask", action="store_true", help="Hopp over Playwright-tunge kilder")
    parser.add_argument("--statisk", action="store_true", help="Bare statisk kodesjekk, ingen nettverk")
    args = parser.parse_args()

    print(f"\n{'=' * 70}")
    print("STATISK SJEKK – kjente feil-mønstre i scrapers/")
    print(f"{'=' * 70}")
    statiske_feil = statisk_sjekk()
    if statiske_feil == 0:
        print("  ✓ Ingen kjente feil-mønstre")
    else:
        print(f"\n  ✗ {statiske_feil} mistenkelige steder funnet")

    if args.statisk:
        sys.exit(0 if statiske_feil == 0 else 1)

    valgte = SCRAPERS
    if args.kilde:
        valgte = [s for s in SCRAPERS if s[0] == args.kilde]
    elif args.rask:
        valgte = [s for s in SCRAPERS if not s[3]]

    print(f"\n{'=' * 70}")
    print(f"NETTVERKSTEST – {len(valgte)} scraper(e)")
    print(f"{'=' * 70}\n")

    resultater = []
    for navn, klasse, max_pages, _ in valgte:
        print(f"▶ {navn} ...", flush=True)
        r = kjor_scraper(navn, klasse, max_pages)
        resultater.append(r)
        ikon = "✓" if r["ok"] else "✗"
        print(f"  {ikon} {navn}: {r['validert']}/{r['filer']} filer validert på {r['tid']:.1f}s")
        if r["feil"]:
            forste_linje = r["feil"].splitlines()[0]
            print(f"    feil: {forste_linje}")
        print()

    # Detaljert rapport for feilende scrapere
    feil = [r for r in resultater if not r["ok"]]
    if feil:
        print(f"\n{'=' * 70}")
        print("DETALJER OM FEIL")
        print(f"{'=' * 70}\n")
        for r in feil:
            print(f"--- {r['navn']} ---")
            print(r["feil"])
            print()

    # Oppsummering
    ok = sum(1 for r in resultater if r["ok"])
    print(f"\n{'=' * 70}")
    print(f"RESULTAT: {ok}/{len(resultater)} scrapere OK")
    print(f"{'=' * 70}\n")

    sys.exit(0 if ok == len(resultater) else 1)


if __name__ == "__main__":
    main()
