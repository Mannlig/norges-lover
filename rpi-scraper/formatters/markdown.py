"""
Genererer indeksfiler (README.md) for hver datamappe, og en kort oversikt
i data/README.md. Gjør det enkelt å navigere i repoet på GitHub.

Indeksene har ikke tidsstempel: de skrives om hver runde, og et tidsstempel
gjorde at alle sju endret seg hver gang og fylte git-loggen med
«README, README, README …» selv når ingenting annet hadde skjedd.
"""

from pathlib import Path

# DATA_PATHS-nøkkel → (tittel, beskrivelse)
KATEGORI_INFO = {
    "stortinget": (
        "Data – Stortinget",
        "Saker fra Stortingets åpne API: tittel, status, komité, emner og henvisninger. "
        "**Dette er saksmetadata, ikke lovtekst.**",
    ),
    "skatt": (
        "Data – Skatteetaten",
        "Skatteregler, satser, fradrag, MVA og veiledere fra Skatteetaten, "
        "inkludert Skatte-ABC under `rettskilder/type/handboker/skatte-abc/`.",
    ),
    "byggteknisk": (
        "Data – DiBK (byggteknisk)",
        "Byggtekniske krav og veiledere fra Direktoratet for byggkvalitet. "
        "`regelverk/byggteknisk-forskrift-tek17/` er gjeldende TEK17; `regelverk/tek/` er den opphevede TEK10.",
    ),
    "nav": (
        "Data – NAV",
        "Stønader, ytelser, satser og grunnbeløp fra NAV.",
    ),
    "arbeidstilsynet": (
        "Data – Arbeidstilsynet",
        "Arbeidsmiljø, HMS og arbeidsforhold fra Arbeidstilsynet.",
    ),
    "husbanken": (
        "Data – Husbanken",
        "Bostøtte, startlån og tilskudd fra Husbanken.",
    ),
}


def lag_indeks(data_dir: Path, tittel: str, beskrivelse: str) -> Path:
    """Lager/oppdaterer README.md i en datamappe. Returnerer stien."""
    md_filer = sorted(f for f in data_dir.rglob("*.md") if f.name != "README.md")

    linjer = [
        f"# {tittel}",
        "",
        beskrivelse,
        "",
        f"**Antall dokumenter:** {len(md_filer)}",
        "",
        "## Innhold",
        "",
    ]

    grupper: dict[str, list[Path]] = {}
    for f in md_filer:
        relativ = f.relative_to(data_dir)
        gruppe = relativ.parts[0] if len(relativ.parts) > 1 else "."
        grupper.setdefault(gruppe, []).append(f)

    for gruppe, filer in sorted(grupper.items()):
        if gruppe != ".":
            linjer += [f"### {gruppe.replace('-', ' ').title()}", ""]
        for f in filer:
            linjer.append(f"- [{_hent_tittel(f)}]({f.relative_to(data_dir).as_posix()})")
        linjer.append("")

    linjer += [
        "---",
        "",
        "*Alle dokumenter inneholder referanse til originalkilden. "
        "Se [mannlig/norges-lover](https://github.com/mannlig/norges-lover) for kildekode og mer info.*",
        "",
    ]
    return _skriv(data_dir / "README.md", "\n".join(linjer))


def lag_oversikt(data_dir: Path, data_paths: dict[str, Path]) -> Path:
    """Kort oversikt i data/README.md med antall dokumenter per kilde."""
    linjer = [
        "# Data",
        "",
        "Hver mappe har sin egen README.md med full innholdsliste.",
        "",
        "| Mappe | Innhold | Dokumenter |",
        "|---|---|---|",
    ]
    for kat, (tittel, beskrivelse) in KATEGORI_INFO.items():
        sti = data_paths.get(kat)
        if not sti or not sti.exists():
            continue
        antall = sum(1 for f in sti.rglob("*.md") if f.name != "README.md")
        rel = sti.relative_to(data_dir).as_posix()
        linjer.append(f"| [`{rel}/`]({rel}/) | {tittel.removeprefix('Data – ')} | {antall} |")
    linjer += ["", "Systemstatus: [`status/heartbeat.md`](status/heartbeat.md)", ""]
    return _skriv(data_dir / "README.md", "\n".join(linjer))


def _skriv(sti: Path, innhold: str) -> Path:
    if not sti.exists() or sti.read_text(encoding="utf-8") != innhold:
        sti.write_text(innhold, encoding="utf-8")
    return sti


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
