"""
Tester for kjernelogikken – kjører uten nettleser og uten nettverk.

    cd rpi-scraper && python -m unittest discover -s tests -v

Krever bare `pip install scrapling==0.4.7` (uten [fetchers]).
"""

import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Isoler fra ekte data og kø FØR config importeres.
_TMP = Path(tempfile.mkdtemp(prefix="norges-lover-test-"))
os.environ["REPO_ROOT"] = str(_TMP / "repo")
os.environ["STATE_DIR"] = str(_TMP / "state")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scrapling import Selector  # noqa: E402

from formatters.html import html_til_markdown  # noqa: E402
from scrapers.base import BORTE, MIDLERTIDIG, OK  # noqa: E402
from scrapers.nav import NavScraper  # noqa: E402
from scrapers.skatteetaten import SkatteetatenScraper, skatte_abc_kandidater  # noqa: E402


class Konverter(unittest.TestCase):
    def test_tekst_etter_lenke_beholdes(self):
        md = html_til_markdown('<main><p>Plassert i <a href="/soner/">soner</a> etter bosted.</p></main>',
                               "https://www.skatteetaten.no/satser/")
        self.assertIn("Plassert i [soner](https://www.skatteetaten.no/soner/) etter bosted.", md)

    def test_avsnitt_som_starter_med_utheving(self):
        self.assertIn("Sats 25 prosent", html_til_markdown("<main><p><strong>Sats</strong> 25 prosent</p></main>"))

    def test_tabell(self):
        md = html_til_markdown(
            "<main><table><tr><th>Trinn</th><th>Sats</th></tr>"
            "<tr><td>1</td><td>1,7 %</td></tr></table></main>")
        self.assertIn("| Trinn | Sats |", md)
        self.assertIn("| --- | --- |", md)
        self.assertIn("| 1 | 1,7 % |", md)

    def test_nostede_lister_og_ingen_dobbel_tekst(self):
        md = html_til_markdown("<main><ul><li><p>Ytre</p><ul><li>Indre</li></ul></li></ul></main>")
        self.assertEqual(md.count("Ytre"), 1)
        self.assertIn("- Ytre", md)
        self.assertIn("  - Indre", md)

    def test_stoy_fjernes(self):
        md = html_til_markdown("<main><nav>Meny</nav><script>x()</script><p>Innhold</p>"
                               "<button>Del</button><p>Skriv ut</p></main>")
        self.assertEqual(md, "Innhold")

    def test_los_tekst_i_div(self):
        self.assertIn("Løs tekst med utheving",
                      html_til_markdown("<main><div>Løs tekst <em>med utheving</em></div></main>"))


def _side(url: str, html: str) -> Selector:
    return Selector(content=html, url=url)


class FalskNettsted:
    """Erstatter fetch(): url → (status, html, endelig_url)."""

    def __init__(self, scraper, sider: dict):
        self.scraper, self.sider, self.kall = scraper, sider, []
        scraper.fetch = self.fetch
        scraper._les_robots = lambda: False
        scraper._polite_delay = lambda: None

    def fetch(self, url, retries=2):
        self.kall.append(url)
        status, html, endelig = self.sider.get(url, (404, "", url))
        if status == OK:
            self.scraper._utfall(OK)
            return _side(endelig, html)
        return self.scraper._utfall(status)


def _innhold(tekst: str) -> str:
    return f"<html><head><title>{tekst}</title></head><body><main><h1>{tekst}</h1>" \
           f"<p>{'Regeltekst om ' + tekst + '. ' * 1}{'Mer tekst. ' * 15}</p></main></body></html>"


class Nettsted(unittest.TestCase):
    def setUp(self):
        self.ut = Path(tempfile.mkdtemp(dir=_TMP))
        for f in Path(os.environ["STATE_DIR"]).glob("*.json"):
            f.unlink()

    def test_normaliser(self):
        s = SkatteetatenScraper()
        side = "https://www.skatteetaten.no/person/skatt/"
        self.assertEqual(s.normaliser("fradrag", side), "https://www.skatteetaten.no/person/skatt/fradrag/")
        self.assertEqual(s.normaliser("https://skatteetaten.no/satser/x?a=1#b"),
                         "https://www.skatteetaten.no/satser/x/")
        self.assertEqual(s.normaliser("/person/../satser/./y"), "https://www.skatteetaten.no/satser/y/")
        self.assertIsNone(s.normaliser("https://www.altinn.no/satser/"))
        self.assertIsNone(s.normaliser("/"))
        self.assertIsNone(s.normaliser("mailto:x@y.no"))
        n = NavScraper()
        self.assertEqual(n.normaliser("/dagpenger/"), "https://www.nav.no/dagpenger")

    def test_nav_filter(self):
        n = NavScraper()
        for url in ("https://www.nav.no/arbeidsgiver/klage/nn", "https://www.nav.no/dagpenger/en",
                    "https://www.nav.no/fyllut/nav040301", "https://www.nav.no/nav/forskrift/2019/x",
                    "https://www.nav.no/no/lokalt/oslo"):
            self.assertFalse(n.er_relevant(url), url)
        self.assertTrue(n.er_relevant("https://www.nav.no/arbeidsgiver/klage"))

    def test_skatte_abc_tidligere_aar_fryses(self):
        s = SkatteetatenScraper()
        år = datetime.now(timezone.utc).year
        self.assertIsNone(s.gjenbesøk_dager("rettskilder/type/handboker/skatte-abc/2023/a-1/A-1.001"))
        self.assertIsNone(s.gjenbesøk_dager("rettskilder/type/handboker/skatte-abc/2022-2023"))
        self.assertEqual(s.gjenbesøk_dager(f"rettskilder/type/handboker/skatte-abc/{år}/x"), 7)
        self.assertEqual(s.gjenbesøk_dager("satser/trinnskatt"), 2)
        self.assertEqual(len(skatte_abc_kandidater(datetime(2026, 7, 1))), 6)

    def test_nye_sider_foran_gamle(self):
        s = SkatteetatenScraper()
        gammel = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        s._state = {"kø": {
            **{f"gammel{i}": {"url": "u", "hentet": False, "sist_hentet": gammel} for i in range(10)},
            **{f"ny{i}": {"url": "u", "hentet": False} for i in range(10)},
        }}
        valgt = [k for k, _ in s._velg_fra_ko(8)]
        self.assertEqual(valgt[:6], [f"ny{i}" for i in range(6)])
        self.assertEqual(len(valgt), 8)

    def test_full_runde_mot_falskt_nettsted(self):
        b = "https://www.skatteetaten.no"
        s = SkatteetatenScraper()
        s.startpunkter = [f"{b}/satser/"]
        s.hub_urler = lambda: s.startpunkter
        sider = {
            f"{b}/satser/": (OK, '<main><a href="trinnskatt/">T</a><a href="borte/">B</a>'
                                 '<a href="feil/">F</a><a href="/person/flyttet/">R</a>'
                                 '<a href="/satser/logg-inn/">L</a></main>', f"{b}/satser/"),
            f"{b}/satser/trinnskatt/": (OK, _innhold("Trinnskatt"), f"{b}/satser/trinnskatt/"),
            f"{b}/satser/borte/": (BORTE, "", ""),
            f"{b}/satser/feil/": (MIDLERTIDIG, "", ""),
            f"{b}/person/flyttet/": (OK, _innhold("Ny"), f"{b}/person/ny-adresse/"),
            f"{b}/person/ny-adresse/": (OK, _innhold("Ny adresse"), f"{b}/person/ny-adresse/"),
        }
        nett = FalskNettsted(s, sider)
        filer = s.scrape(self.ut, max_pages=10)
        kø = s._state["kø"]

        self.assertTrue((self.ut / "satser/trinnskatt.md").exists())
        self.assertIn("Regeltekst om Trinnskatt", (self.ut / "satser/trinnskatt.md").read_text())
        self.assertNotIn("satser/logg-inn", kø)                       # filtrert bort
        self.assertTrue(kø["satser/borte"]["borte"])                  # 404 = borte
        self.assertFalse(kø["satser/feil"]["hentet"])                 # midlertidig feil = prøv igjen
        self.assertEqual(kø["satser/feil"]["feil"], 1)
        self.assertFalse((self.ut / "person/flyttet.md").exists())    # omdirigert = ingen kopi
        self.assertIn("person/ny-adresse", kø)                        # ... men målet havner i køen
        self.assertEqual(s.teller["omdirigert"], 1)

        # Neste runde: feil-siden prøves igjen, ny-adresse hentes, trinnskatt hentes ikke
        nett.kall.clear()
        s2 = SkatteetatenScraper()
        s2.hub_urler = lambda: []
        FalskNettsted(s2, sider)
        s2.scrape(self.ut, max_pages=10)
        self.assertIn(f"{b}/satser/feil/", nett.kall + s2.fetch.__self__.kall)
        self.assertTrue((self.ut / "person/ny-adresse.md").exists())

    def test_gir_opp_etter_tre_feil(self):
        b = "https://www.skatteetaten.no"
        for runde in range(3):
            s = SkatteetatenScraper()
            s.hub_urler = lambda: []
            if runde == 0:
                s._les_state = lambda: {"sist_hub_crawl": datetime.now(timezone.utc).isoformat(),
                                        "kø": {"satser/x": {"url": f"{b}/satser/x/", "hentet": False}}}
            FalskNettsted(s, {f"{b}/satser/x/": (MIDLERTIDIG, "", "")})
            s.scrape(self.ut, max_pages=5)
        self.assertTrue(s._state["kø"]["satser/x"]["hentet"])

    def test_rydd_ko(self):
        n = NavScraper()
        n._state = {"kø": {"a/nn": {"url": "https://www.nav.no/a/nn"},
                           "dagpenger": {"url": "https://www.nav.no/dagpenger"}}}
        self.assertEqual(n._rydd_ko(), 1)
        self.assertEqual(list(n._state["kø"]), ["dagpenger"])


class Stortinget(unittest.TestCase):
    def setUp(self):
        import copy
        import json
        from scrapers import stortinget
        self.st = stortinget
        self.sak = json.loads((Path(__file__).parent / "eksempel_sak.json").read_text())
        self.copy = copy.deepcopy
        self.ut = Path(tempfile.mkdtemp(dir=_TMP))
        (Path(os.environ["STATE_DIR"]) / "stortinget-state.json").unlink(missing_ok=True)

    def _api(self, saker_per_sesjon: dict):
        def get_json(url, params=None, retries=3):
            if url.endswith("/sesjoner"):
                return {"innevaerende_sesjon": {"id": "2025-2026"},
                        "sesjoner_liste": [{"id": s} for s in ["2026-2027", *saker_per_sesjon]]}
            sesjon = params["sesjonid"]
            return {"sesjon_id": sesjon, "saker_liste": saker_per_sesjon.get(sesjon, [])}
        return get_json

    def test_hash_ignorerer_cachetidsstempler(self):
        a, b = self.copy(self.sak), self.copy(self.sak)
        b["respons_dato_tid"] = "/Date(1+0200)/"
        b["komite"]["respons_dato_tid"] = "/Date(2+0200)/"
        for e in b["emne_liste"]:
            e["respons_dato_tid"] = "/Date(3+0200)/"
        self.assertEqual(self.st.stabilt_innhold(a), self.st.stabilt_innhold(b))
        b["status"] = "behandlet"
        self.assertNotEqual(self.st.stabilt_innhold(a), self.st.stabilt_innhold(b))

    def test_perioder(self):
        self.assertEqual(self.st.stortingsperiode("2025-2026"), "2025-2029")
        self.assertEqual(self.st.stortingsperiode("2024-2025"), "2021-2025")
        self.assertEqual(self.st.stortingsperiode("2017-2018"), "2017-2021")
        self.assertEqual(self.st.sesjoner_fra_dato(datetime(2026, 9, 1), 2), ["2025-2026", "2024-2025"])

    def test_runder_tar_resten_uten_evig_loekke(self):
        saker = {}
        for sesjon, start in (("2025-2026", 1000), ("2024-2025", 2000)):
            saker[sesjon] = []
            for i in range(5):
                s = self.copy(self.sak)
                s["id"], s["tittel"] = start + i, f"Sak {start + i}"
                saker[sesjon].append(s)
        saker["2024-2025"].append(self.copy(saker["2025-2026"][0]))   # samme sak i to sesjoner

        skrevet = []
        for runde in range(4):
            s = self.st.StortingetScraper()
            s.get_json = self._api(saker)
            skrevet.append(len(s.scrape(self.ut, max_pages=4)))
        self.assertEqual(skrevet, [4, 4, 2, 0])
        self.assertTrue((self.ut / "2021-2025").exists())
        self.assertEqual(len(list(self.ut.glob("*/1000-*.md"))), 1)   # ingen duplikat

        # Tittelendring gir ikke ny fil
        saker["2025-2026"][1]["tittel"] = "Helt ny tittel"
        s = self.st.StortingetScraper()
        s.get_json = self._api(saker)
        self.assertEqual(len(s.scrape(self.ut, max_pages=10)), 1)
        self.assertEqual(len(list(self.ut.glob("*/1001-*.md"))), 1)


class Publisering(unittest.TestCase):
    """Mot et lokalt bart repo – ingen nettverk, ingen token-bruk."""

    def setUp(self):
        import subprocess
        self.sp = subprocess
        rot = Path(tempfile.mkdtemp(dir=_TMP))
        self.remote, self.repo = rot / "remote.git", rot / "repo"
        g = lambda *a, cwd=None: subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True)
        g("init", "-q", "--bare", "-b", "main", str(self.remote))
        g("clone", "-q", str(self.remote), str(self.repo))
        g("config", "user.email", "t@t", cwd=self.repo)
        g("config", "user.name", "t", cwd=self.repo)
        (self.repo / "data").mkdir()
        (self.repo / "data/gammel.md").write_text("x")
        g("add", ".", cwd=self.repo)
        g("commit", "-qm", "init", cwd=self.repo)
        g("push", "-q", "origin", "main", cwd=self.repo)

        from publishers import github_publisher as gp
        self.gp = gp
        os.environ["GITHUB_TOKEN"] = "ghp_" + "x" * 36
        self.pub = gp.GitHubPublisher()
        self.pub.repo_root = self.repo
        self.pub._konfigurer_remote = lambda: None     # behold lokal remote

    def test_sladd(self):
        tekst = "fatal: could not read Password for 'https://ghp_abcDEF123_xyz@github.com': nei"
        self.assertNotIn("abcDEF", self.gp.sladd(tekst))
        self.assertNotIn("github_pat_11AB", self.gp.sladd("github_pat_11AB_cd"))

    def test_publiser_ny_endret_og_slettet(self):
        (self.repo / "data/ny.md").write_text("ny")
        (self.repo / "data/gammel.md").unlink()
        filer = [self.repo / "data/ny.md", self.repo / "data/gammel.md",
                 self.repo / "data/aldri-fantes.md", self.repo / "data/README.md"]
        self.assertTrue(self.pub.publish(filer))
        logg = self.sp.run(["git", "log", "-1", "--format=%B", "main"], cwd=self.remote,
                           capture_output=True, text=True).stdout
        self.assertIn("ny: ny", logg)
        self.assertIn("slettet: gammel", logg)
        self.assertNotIn("README", logg.splitlines()[0])

    def test_push_tilgang_og_avbrutt_rebase(self):
        self.assertTrue(self.pub.sjekk_push_tilgang()[0])
        (self.repo / ".git/rebase-merge").mkdir()
        self.pub._rydd_avbrutt_rebase()   # skal ikke kaste
        self.pub._konfigurer_remote = self.gp.GitHubPublisher._konfigurer_remote.__get__(self.pub)
        self.pub._konfigurer_remote()
        url = self.sp.run(["git", "remote", "get-url", "origin"], cwd=self.repo,
                          capture_output=True, text=True).stdout
        self.assertNotIn("ghp_", url)
        helper = self.sp.run(["git", "config", "credential.helper"], cwd=self.repo,
                             capture_output=True, text=True).stdout
        self.assertIn("$GITHUB_TOKEN", helper)
        self.assertNotIn("x" * 36, (self.repo / ".git/config").read_text())


class Heartbeat(unittest.TestCase):
    def test_helse(self):
        import main
        self.assertEqual(main.vurder_helse({"hentet_ok": 150, "uendret": 140, "endret": 5})[0], "OK")
        self.assertEqual(main.vurder_helse({"hentet_ok": 0, "feil_midlertidig": 12})[0], "FEIL")
        self.assertEqual(main.vurder_helse({"krasj": "KeyError"})[0], "FEIL")
        self.assertEqual(main.vurder_helse({"hentet_ok": 40, "for_lite_innhold": 40})[0], "FEIL")
        self.assertEqual(main.vurder_helse({"hentet_ok": 0})[0], "OK")   # alt à jour

    def test_heartbeat_fil(self):
        import main
        ut = Path(tempfile.mkdtemp(dir=_TMP))
        f = main.skriv_heartbeat(ut, {"skatteetaten": {"hentet_ok": 10, "uendret": 10},
                                      "nav": {"krasj": "ValueError"}}, 3725)
        tekst = f.read_text()
        self.assertIn("<!-- helse: skatteetaten=OK nav=FEIL -->", tekst)
        self.assertIn("1 t 2 min", tekst)
        self.assertIn("**nav** (FEIL): krasj: ValueError", tekst)


if __name__ == "__main__":
    unittest.main()
