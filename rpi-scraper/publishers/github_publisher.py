"""
Publiserer scrapede filer til GitHub via git.

SIKKERHET: GitHub-token leses KUN fra miljøvariabelen GITHUB_TOKEN.
Token lagres aldri i filer eller i koden.

Oppsett på Raspberry Pi:
    export GITHUB_TOKEN=ghp_dintoken   # legg i ~/.norges-lover-env
"""

import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

from config import REPO_ROOT, GITHUB_REPO, GIT_USER_NAME, GIT_USER_EMAIL

logger = logging.getLogger(__name__)


class GitHubPublisher:
    def __init__(self):
        self.repo_root = REPO_ROOT
        self._token = os.environ.get("GITHUB_TOKEN", "")
        if not self._token:
            logger.warning(
                "GITHUB_TOKEN er ikke satt! Sett miljøvariabelen: export GITHUB_TOKEN=ghp_..."
            )

    def publish(self, changed_files: list[Path]) -> bool:
        """
        Committer og pusher kun de filene som faktisk ble endret.
        Commit-meldingen beskriver konkret hva som endret seg.
        Returnerer True om push lyktes.
        """
        if not changed_files:
            logger.info("Ingen endrede filer å publisere")
            return True

        if not self._token:
            logger.error("Kan ikke publisere uten GITHUB_TOKEN")
            return False

        try:
            self._konfigurer_git()
            self._konfigurer_remote()

            relative_paths = [str(f.relative_to(self.repo_root)) for f in changed_files]
            self._run(["git", "add", "--"] + relative_paths)

            # Sjekk om det faktisk er noe å committe (unngå tomme commits)
            result = self._run(["git", "diff", "--cached", "--quiet"], check=False)
            if result.returncode == 0:
                logger.info("Ingen git-diff å committe (innhold identisk)")
                return True

            # Finn ut hvilke filer som faktisk er endret vs nye
            nye, endrede = self._kategoriser_endringer()
            msg = self._lag_commit_melding(nye, endrede, changed_files)

            self._run(["git", "commit", "-m", msg])

            branch = self._gjeldende_branch()
            # Rebase mot remote før push – håndterer samtidige commits (f.eks. kode-oppdateringer)
            self._run(["git", "pull", "--rebase", "origin", branch], check=False)
            self._run(["git", "push", "-u", "origin", branch])
            logger.info("Pushet til %s: %d nye, %d endrede filer", branch, len(nye), len(endrede))
            return True

        except subprocess.CalledProcessError as e:
            logger.error("Git-kommando feilet: %s\nstderr: %s", e.cmd, e.stderr)
            return False
        except Exception as e:
            logger.error("Uventet feil ved publisering: %s", e)
            return False

    def _kategoriser_endringer(self) -> tuple[list[str], list[str]]:
        """Skiller mellom nye filer (A) og endrede filer (M) i staging-area."""
        result = self._run(["git", "diff", "--cached", "--name-status"])
        nye = []
        endrede = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            status, _, path = line.partition("\t")
            status = status.strip()
            path = path.strip()
            if status == "A":
                nye.append(path)
            elif status in ("M", "R"):
                endrede.append(path)
        return nye, endrede

    def _lag_commit_melding(
        self,
        nye: list[str],
        endrede: list[str],
        alle_filer: list[Path],
    ) -> str:
        """
        Lager en lesbar commit-melding som konkret beskriver hva som endret seg.
        Eksempel:
            oppdatering: arbeidsmiljoeloven endret, skatteloven endret (2 endringer)
            ny: barnetrygd/satser, pleiepenger/om (2 nye dokumenter)
        """
        deler = []

        if endrede:
            navn = [self._filnavn_lesbart(p) for p in endrede[:5]]
            ekstra = f" (+{len(endrede) - 5} til)" if len(endrede) > 5 else ""
            deler.append(f"oppdatering: {', '.join(navn)}{ekstra}")

        if nye:
            navn = [self._filnavn_lesbart(p) for p in nye[:5]]
            ekstra = f" (+{len(nye) - 5} til)" if len(nye) > 5 else ""
            deler.append(f"ny: {', '.join(navn)}{ekstra}")

        if not deler:
            deler.append(f"auto: {len(alle_filer)} filer oppdatert")

        tittel = " | ".join(deler)

        # Detaljert liste i commit-body
        linjer = [tittel, ""]
        if endrede:
            linjer.append("Endrede dokumenter (innhold endret siden forrige kjøring):")
            for p in endrede:
                linjer.append(f"  - {p}")
            linjer.append("")
        if nye:
            linjer.append("Nye dokumenter:")
            for p in nye:
                linjer.append(f"  - {p}")
            linjer.append("")

        linjer.append("Kilde-URL er dokumentert i hvert enkelt dokument.")
        linjer.append("Se git diff for eksakt hva som endret seg i lovteksten.")

        return "\n".join(linjer)

    @staticmethod
    def _filnavn_lesbart(path: str) -> str:
        """Gjør filsti lesbar: data/lover/arbeidsmiljoeloven.md → arbeidsmiljoeloven"""
        from pathlib import Path as P
        return P(path).stem.replace("-", " ")

    def _konfigurer_git(self):
        self._run(["git", "config", "user.name", GIT_USER_NAME])
        self._run(["git", "config", "user.email", GIT_USER_EMAIL])

    def _konfigurer_remote(self):
        """Sett remote URL med token fra miljøvariabel (aldri lagret på disk)."""
        remote_url = f"https://{self._token}@github.com/{GITHUB_REPO}.git"
        self._run(["git", "remote", "set-url", "origin", remote_url])

    def _gjeldende_branch(self) -> str:
        result = self._run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        return result.stdout.strip()

    def _run(self, cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
        result = subprocess.run(
            cmd,
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=check,
        )
        if result.stdout:
            logger.debug("git stdout: %s", result.stdout.strip())
        if result.stderr:
            logger.debug("git stderr: %s", result.stderr.strip())
        return result

    def pull_latest(self) -> bool:
        """Hent siste endringer fra remote før scraping starter."""
        try:
            self._konfigurer_remote()
            branch = self._gjeldende_branch()
            self._run(["git", "pull", "--ff-only", "origin", branch])
            logger.info("Hentet siste endringer fra origin/%s", branch)
            return True
        except subprocess.CalledProcessError as e:
            logger.warning("git pull feilet: %s", e.stderr)
            return False
