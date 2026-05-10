"""
Genererer indeksfiler (README.md) for hvert datamappe.
Gjør det enkelt å navigere i repoet på GitHub.
"""

import re
from datetime import datetime, timezone
from pathlib import Path


def lag_indeks(data_dir: Path, kategori: str, beskrivelse: str) -> Path:
    """
    Lager/oppdaterer README.md i en datamappe med oversikt over alle filer.
    Returnerer Path til indeksfilen.
    """
    md_filer = sorted(data_dir.rglob("*.md"))
    # Ikke ta med selve README
    md_filer = [f for f in md_filer if f.name != "README.md"]

    naa = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    linjer = [
        f"# {kategori}",
        "",
        beskrivelse,
        "",
        f"*Sist oppdatert: {naa}*",
        "",
        f"**Antall dokumenter:** {len(md_filer)}",
        "",
        "## Innhold",
        "",
    ]

    # Grupper filer etter undermappe
    grupper: dict[str, list[Path]] = {}
    for f in md_filer:
        try:
            relativ = f.relative_to(data_dir)
            gruppe = relativ.parts[0] if len(relativ.parts) > 1 else "."
        except ValueError:
            gruppe = "."
        grupper.setdefault(gruppe, []).append(f)

    for gruppe, filer in sorted(grupper.items()):
        if gruppe != ".":
            linjer.append(f"### {gruppe.replace('-', ' ').title()}")
            linjer.append("")
        for f in sorted(filer):
            tittel = _hent_tittel(f)
            relativ_sti = f.relative_to(data_dir)
            linjer.append(f"- [{tittel}]({relativ_sti})")
        linjer.append("")

    linjer += [
        "---",
        "",
        "*Alle dokumenter inneholder referanse til originalkilden. "
        "Se [mannlig/norges-lover](https://github.com/mannlig/norges-lover) for kildekode og mer info.*",
    ]

    readme = data_dir / "README.md"
    readme.write_text("\n".join(linjer), encoding="utf-8")
    return readme


_GENERISKE_TITLER = {"hoved­meny", "hoved-meny", "hovedmeny", "meny", "menu", "navigation", "ukjent tittel"}


def _hent_tittel(filepath: Path) -> str:
    """Les tittel fra en markdown-fil, hopper over generiske navigasjonstitler."""
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    tittel = line[2:].strip()
                    if tittel.lower() not in _GENERISKE_TITLER:
                        return tittel
    except Exception:
        pass
    return filepath.stem.replace("-", " ").title()


KATEGORI_INFO = {
    "lover": (
        "Norske lover hentet fra Stortingets API og Lovdata.",
        "Inkluderer lovtekst, metadata og kilde-URL.",
    ),
    "forskrifter": (
        "Nasjonale forskrifter og regelverk.",
        "Hentet fra Lovdata.",
    ),
    "skatt": (
        "Skatteregler, satser og veiledere fra Skatteetaten.",
        "Inkluderer skattesatser, MVA, arbeidsgiveravgift og fradrag.",
    ),
    "byggteknisk": (
        "Byggtekniske krav og veiledere fra DiBK.",
        "TEK17, SAK10, søknadsprosesser og veiledere.",
    ),
    "nav": (
        "Stønader, ytelser og rettigheter fra NAV.",
        "Dagpenger, sykepenger, foreldrepenger, uføretrygd, alderspensjon m.m.",
    ),
    "kommuner": (
        "Kommunale og lokale forskrifter.",
        "Hentet fra Lovdata sitt kommuneregister for utvalgte kommuner.",
    ),
}
