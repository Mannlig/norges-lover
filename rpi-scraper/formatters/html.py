"""
HTML → Markdown for innholdet fra nettkildene.

Erstatter den gamle uttrekkingen som brukte `tag.text` per element. Den ga
bare teksten *før* første barneelement, så alt etter en lenke eller utheving
forsvant, avsnitt som startet med <strong> forsvant helt, og tabeller ble
aldri lest. Det gjorde at satsfilene manglet tallene sine og at
Skatte-ABC-tekst ble kuttet midt i lovhenvisninger.

Bygger på lxml, som Scrapling allerede er avhengig av – ingen ny pakke, så
endringen når Pi-en via git uten at imaget må bygges på nytt.
"""

import re
from urllib.parse import urljoin

# Elementer som er ren støy for en leser av regelverket.
_STOY_XPATH = (
    ".//script|.//style|.//noscript|.//template|.//svg|.//iframe|"
    ".//nav|.//button|.//form|.//*[@hidden]|.//*[@aria-hidden='true']"
)

_OVERSKRIFT = {"h1": "##", "h2": "###", "h3": "####", "h4": "####", "h5": "####", "h6": "####"}

# Elementer som danner egne blokker. Alt annet behandles som løpende tekst.
_BLOKK = {
    "address", "article", "aside", "blockquote", "dd", "details", "div", "dl",
    "dt", "fieldset", "figcaption", "figure", "footer", "h1", "h2", "h3", "h4",
    "h5", "h6", "header", "hr", "li", "main", "ol", "p", "pre", "section",
    "summary", "table", "tbody", "td", "tfoot", "th", "thead", "tr", "ul",
}
_UNDERBLOKK = {"ul", "ol", "table"}

# Hele linjer som bare er knapper/lenker i grensesnittet.
_UI_LINJER = {
    "skriv ut", "del", "del siden", "del side", "til toppen", "lukk", "åpne",
    "vis mer", "vis mindre", "vis alle", "kopier lenke", "hopp til innhold",
    "hopp til hovedinnhold", "tilbake", "meny",
}


def html_til_markdown(html: str, base_url: str = "") -> str:
    """Konverter et HTML-fragment (typisk <main>) til Markdown."""
    from lxml import html as lxml_html  # lat import: feil her stopper bare én kilde

    if not html or not html.strip():
        return ""
    try:
        rot = lxml_html.fromstring(html)
    except Exception:
        return ""
    for el in rot.xpath(_STOY_XPATH):
        el.drop_tree()

    ut: list[str] = []
    _blokk(rot, base_url, ut, "")
    tekst = "\n".join(ut)
    tekst = re.sub(r"[ \t]+\n", "\n", tekst)
    tekst = re.sub(r"\n{3,}", "\n\n", tekst)
    return tekst.strip()


def _tag(el) -> str:
    return el.tag.lower() if isinstance(el.tag, str) else ""


def _rens(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def _inline(el, base: str) -> str:
    """All tekst i el med lenker som [tekst](url). Underlister/tabeller utelates."""
    deler = [el.text or ""]
    for barn in el:
        deler.append(_inline_node(barn, base))
        deler.append(barn.tail or "")
    return "".join(deler)


def _inline_node(n, base: str) -> str:
    t = _tag(n)
    if not t:  # kommentar o.l.
        return ""
    if t == "br":
        return " "
    if t in _UNDERBLOKK:
        return ""
    if t == "a":
        tekst = _rens(_inline(n, base))
        href = (n.get("href") or "").strip()
        if tekst and href and not href.startswith(("#", "javascript:", "mailto:", "tel:")):
            return f"[{tekst}]({urljoin(base, href) if base else href})"
        return tekst
    s = _inline(n, base)
    return f" {s} " if t in _BLOKK else s


def _avsnitt(tekst: str, ut: list[str], prefiks: str = ""):
    tekst = _rens(tekst)
    if tekst and tekst.lower() not in _UI_LINJER:
        ut.append(f"{prefiks}{tekst}\n")


def _blokk(el, base: str, ut: list[str], innrykk: str):
    t = _tag(el)
    if t in _OVERSKRIFT:
        tekst = _rens(_inline(el, base))
        if tekst:
            ut.append(f"\n{_OVERSKRIFT[t]} {tekst}\n")
    elif t in ("ul", "ol"):
        nr = 0
        for li in el:
            if _tag(li) != "li":
                continue
            nr += 1
            _listepunkt(li, base, ut, innrykk, f"{nr}." if t == "ol" else "-")
        if not innrykk:
            ut.append("")
    elif t == "table":
        _tabell(el, base, ut)
    elif t == "dl":
        for barn in el:
            bt = _tag(barn)
            if bt == "dt":
                tekst = _rens(_inline(barn, base))
                if tekst:
                    ut.append(f"\n**{tekst}**")
            elif bt == "dd":
                _avsnitt(_inline(barn, base), ut, "  ")
            elif bt:
                _blokk(barn, base, ut, innrykk)
    elif t == "pre":
        kode = el.text_content().rstrip()
        if kode.strip():
            ut.append(f"```\n{kode}\n```\n")
    elif t == "hr":
        return
    elif t in ("p", "dt", "dd", "summary", "figcaption", "th", "td"):
        _avsnitt(_inline(el, base), ut)
        for under in _underblokker(el):
            _blokk(under, base, ut, innrykk)
    else:
        _beholder(el, base, ut, innrykk)


def _beholder(el, base: str, ut: list[str], innrykk: str):
    """div/section/main o.l.: løs tekst blir avsnitt, blokkbarn behandles hver for seg."""
    buf = [el.text or ""]

    def tøm():
        _avsnitt("".join(buf), ut)
        buf.clear()

    for barn in el:
        if _tag(barn) in _BLOKK:
            tøm()
            _blokk(barn, base, ut, innrykk)
        else:
            buf.append(_inline_node(barn, base))
        buf.append(barn.tail or "")
    tøm()


def _underblokker(el):
    """Lister/tabeller inne i el, men ikke inni andre lister/tabeller."""
    for barn in el:
        t = _tag(barn)
        if t in _UNDERBLOKK:
            yield barn
        elif t:
            yield from _underblokker(barn)


def _listepunkt(li, base: str, ut: list[str], innrykk: str, merke: str):
    tekst = _rens(_inline(li, base))
    if tekst:
        ut.append(f"{innrykk}{merke} {tekst}")
    for under in _underblokker(li):
        if _tag(under) == "table":
            _tabell(under, base, ut)
        else:
            _blokk(under, base, ut, innrykk + "  ")


def _tabell(tab, base: str, ut: list[str]):
    rader = []
    for tr in tab.iter("tr"):
        # Hopp over rader som tilhører en nøstet tabell
        if next(tr.iterancestors("table"), None) is not tab:
            continue
        celler = [
            _rens(_inline(c, base)).replace("|", "\\|")
            for c in tr if _tag(c) in ("td", "th")
        ]
        if any(celler):
            rader.append(celler)
    if not rader:
        return
    bredde = max(len(r) for r in rader)
    rader = [r + [""] * (bredde - len(r)) for r in rader]
    ut.append("")
    tittel = tab.find("caption")
    if tittel is not None and _rens(tittel.text_content()):
        ut.append(f"**{_rens(tittel.text_content())}**\n")
    ut.append("| " + " | ".join(rader[0]) + " |")
    ut.append("|" + " --- |" * bredde)
    for r in rader[1:]:
        ut.append("| " + " | ".join(r) + " |")
    ut.append("")
