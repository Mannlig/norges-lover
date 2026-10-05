"""
Publiserer scrapede filer til GitHub via git.

SIKKERHET: GitHub-token leses KUN fra miljøvariabelen GITHUB_TOKEN og
legges aldri i remote-URL-en. Git henter det via en credential helper
som leser miljøvariabelen når git kjører, så tokenet står ikke i
.git/config og kommer ikke med i feilmeldinger. Alt som logges fra git
sladdes i tillegg, for sikkerhets skyld.
"""

import logging
import os
import re
import subprocess
from pathlib import Path

from config import REPO_ROOT, GITHUB_REPO, GIT_USER_NAME, GIT_USER_EMAIL

logger = logging.getLogger(__name__)

_TOKEN = re.compile(r"(ghp_|github_pat_|gho_|ghs_|ghu_)[A-Za-z0-9_]+")
_URL_MED_PASSORD = re.compile(r"https://[^@/\s]+@")
_CREDENTIAL_HELPER = '!f() { echo username=x-access-token; echo "password=$GITHUB_TOKEN"; }; f'
_GIT_TIMEOUT = 300


def sladd(tekst) -> str:
    """Fjern tokens fra tekst før den logges."""
    tekst = str(tekst or "")
    tekst = _TOKEN.sub(r"\1***", tekst)
    return _URL_MED_PASSORD.sub("https://***@", tekst)


class GitHubPublisher:
    def __init__(self):
        self.repo_root = REPO_ROOT
        self._token = os.environ.get("GITHUB_TOKEN", "")
        if not self._token:
            logger.warning("GITHUB_TOKEN er ikke satt – kan ikke pushe")

    # ── Offentlig API ───────────────────────────────────────────────────

    def sjekk_push_tilgang(self) -> tuple[bool, str]:
        """
        Sjekk at tokenet godtas for push, uten å pushe noe.

        Fetch fra et offentlig repo går anonymt, så den sier ingenting om
        tokenet. push --dry-run må autentisere mot GitHub. Det var nettopp
        dette som sviktet i aug.–okt. 2026: scrapingen gikk som normalt i to
        måneder, mens hver push feilet.
        """
        if not self._token:
            return False, "GITHUB_TOKEN er ikke satt"
        try:
            self._konfigurer_git()
            self._konfigurer_remote()
            r = self._run(["git", "push", "--dry-run", "origin", "HEAD:refs/heads/main"],
                          check=False, timeout=90)
        except subprocess.TimeoutExpired:
            return False, "tidsavbrudd mot GitHub"
        if r.returncode == 0:
            return True, ""
        return False, sladd((r.stderr or r.stdout).strip())[-500:]

    def pull_latest(self) -> bool:
        """Hent siste endringer fra remote før scraping starter."""
        try:
            self._rydd_avbrutt_rebase()
            self._konfigurer_git()
            self._konfigurer_remote()
            branch = self._gjeldende_branch()
            r = self._run(["git", "pull", "--rebase", "origin", branch], check=False)
            if r.returncode != 0:
                logger.warning("git pull feilet: %s", sladd(r.stderr))
                self._rydd_avbrutt_rebase()
                return False
            logger.info("Hentet siste endringer fra origin/%s", branch)
            return True
        except Exception as e:
            logger.warning("git pull feilet: %s", sladd(e))
            return False

    def publish(self, changed_files: list[Path]) -> bool:
        """
        Committer og pusher filene som faktisk er endret eller slettet.
        Returnerer True bare hvis endringene faktisk kom til GitHub.
        """
        if not changed_files:
            logger.info("Ingen endrede filer å publisere")
            return True
        if not self._token:
            logger.error("Kan ikke publisere uten GITHUB_TOKEN")
            return False

        try:
            self._rydd_avbrutt_rebase()
            self._konfigurer_git()
            self._konfigurer_remote()

            stier = self._stier_som_kan_stages(changed_files)
            if not stier:
                logger.info("Ingen gyldige stier å publisere")
                return True
            self._run(["git", "add", "-A", "--pathspec-from-file=-", "--pathspec-file-nul"],
                      input_="\0".join(stier))

            if self._run(["git", "diff", "--cached", "--quiet"], check=False).returncode == 0:
                logger.info("Ingen git-diff å committe (innhold identisk)")
                return True

            nye, endrede, slettede = self._kategoriser_endringer()
            self._run(["git", "commit", "-q", "-F", "-"],
                      input_=self._lag_commit_melding(nye, endrede, slettede))

            branch = self._gjeldende_branch()
            # Rebase mot remote før push – håndterer samtidige kode-commits
            r = self._run(["git", "pull", "--rebase", "origin", branch], check=False)
            if r.returncode != 0:
                logger.error("Rebase feilet: %s", sladd(r.stderr))
                self._rydd_avbrutt_rebase()
                return False
            self._run(["git", "push", "origin", f"HEAD:refs/heads/{branch}"])
            logger.info("Pushet til %s: %d nye, %d endrede, %d slettede filer",
                        branch, len(nye), len(endrede), len(slettede))
            return True

        except subprocess.CalledProcessError as e:
            logger.error("Git-kommando feilet: %s\nstderr: %s", sladd(" ".join(e.cmd)), sladd(e.stderr))
            return False
        except subprocess.TimeoutExpired as e:
            logger.error("Git-kommando tok for lang tid: %s", sladd(" ".join(e.cmd)))
            return False
        except Exception as e:
            logger.error("Uventet feil ved publisering: %s", sladd(e))
            return False

    # ── Hjelpere ────────────────────────────────────────────────────────

    def _stier_som_kan_stages(self, filer: list[Path]) -> list[str]:
        """Eksisterende filer, pluss slettede filer som git kjenner til."""
        sporet = set(self._run(["git", "ls-files", "-z"]).stdout.split("\0"))
        rot = Path(self.repo_root).resolve()
        stier = []
        for f in dict.fromkeys(filer):
            try:
                rel = str(Path(f).resolve().relative_to(rot))
            except ValueError:
                continue
            if Path(f).exists() or rel in sporet:
                stier.append(rel)
        return stier

    def _rydd_avbrutt_rebase(self):
        """En avbrutt rebase overlever entrypointens reset og blokkerer alle senere commits."""
        git_dir = Path(self.repo_root) / ".git"
        if (git_dir / "rebase-merge").exists() or (git_dir / "rebase-apply").exists():
            logger.warning("Fant avbrutt rebase – avbryter den")
            self._run(["git", "rebase", "--abort"], check=False)

    def _kategoriser_endringer(self) -> tuple[list[str], list[str], list[str]]:
        result = self._run(["git", "diff", "--cached", "--name-status", "--no-renames"])
        nye, endrede, slettede = [], [], []
        for line in result.stdout.splitlines():
            status, _, path = line.partition("\t")
            status, path = status.strip(), path.strip()
            {"A": nye, "M": endrede, "D": slettede}.get(status[:1], endrede).append(path)
        return nye, endrede, slettede

    def _lag_commit_melding(self, nye: list[str], endrede: list[str], slettede: list[str]) -> str:
        """
        Commit-tittel med navn på de faktiske dokumentene. Indeks-README-ene
        holdes utenfor tittelen, så loggen ikke blir «README, README, README».
        """
        def navn(stier):
            innhold = [p for p in stier if Path(p).name not in ("README.md", "heartbeat.md")]
            vist = [Path(p).stem.replace("-", " ") for p in innhold[:5]]
            ekstra = f" (+{len(innhold) - 5} til)" if len(innhold) > 5 else ""
            return ", ".join(vist) + ekstra, len(innhold)

        deler = []
        for etikett, stier in (("ny", nye), ("oppdatering", endrede), ("slettet", slettede)):
            tekst, antall = navn(stier)
            if antall:
                deler.append(f"{etikett}: {tekst}")
        tittel = " | ".join(deler) or "status: heartbeat og indekser"

        linjer = [tittel, ""]
        for overskrift, stier in (("Nye dokumenter:", nye),
                                  ("Endrede dokumenter (innhold endret siden forrige kjøring):", endrede),
                                  ("Slettede dokumenter:", slettede)):
            if stier:
                linjer.append(overskrift)
                linjer += [f"  - {p}" for p in stier]
                linjer.append("")
        linjer.append("Kilde-URL er dokumentert i hvert enkelt dokument.")
        return "\n".join(linjer)

    def _konfigurer_git(self):
        self._run(["git", "config", "user.name", GIT_USER_NAME])
        self._run(["git", "config", "user.email", GIT_USER_EMAIL])

    def _konfigurer_remote(self):
        """Remote uten token; credential helper leser GITHUB_TOKEN fra miljøet ved behov."""
        self._run(["git", "remote", "set-url", "origin", f"https://github.com/{GITHUB_REPO}.git"])
        self._run(["git", "config", "--replace-all", "credential.helper", _CREDENTIAL_HELPER])

    def _gjeldende_branch(self) -> str:
        return self._run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()

    def _run(self, cmd: list[str], check: bool = True, input_: str | None = None,
             timeout: int = _GIT_TIMEOUT) -> subprocess.CompletedProcess:
        miljø = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        result = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True,
                                check=check, input=input_, env=miljø, timeout=timeout)
        if result.stdout:
            logger.debug("git stdout: %s", sladd(result.stdout.strip())[:2000])
        if result.stderr:
            logger.debug("git stderr: %s", sladd(result.stderr.strip())[:2000])
        return result
