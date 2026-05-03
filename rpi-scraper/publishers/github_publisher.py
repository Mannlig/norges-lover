"""
Publiserer scrapede filer til GitHub via git.

SIKKERHET: GitHub-token leses KUN fra miljøvariabelen GITHUB_TOKEN.
Token lagres aldri i filer eller i koden.

Oppsett på Raspberry Pi:
    export GITHUB_TOKEN=ghp_dintoken   # legg i ~/.bashrc eller i systemd-tjenestens env
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
                "GITHUB_TOKEN er ikke satt! Sett miljøvariabelen før du kjører. "
                "Eksempel: export GITHUB_TOKEN=ghp_din_token"
            )

    def publish(self, changed_files: list[Path], commit_message: Optional[str] = None) -> bool:
        """
        Committer og pusher endrede filer til GitHub.
        Returnerer True om push lyktes.
        """
        if not changed_files:
            logger.info("Ingen filer å publisere")
            return True

        if not self._token:
            logger.error("Kan ikke publisere uten GITHUB_TOKEN")
            return False

        try:
            self._konfigurer_git()
            self._konfigurer_remote()

            # Stage kun de filene vi faktisk hentet
            relative_paths = [str(f.relative_to(self.repo_root)) for f in changed_files]
            self._run(["git", "add", "--"] + relative_paths)

            # Sjekk om det er noe å committe
            result = self._run(["git", "diff", "--cached", "--quiet"], check=False)
            if result.returncode == 0:
                logger.info("Ingen endringer å committe")
                return True

            msg = commit_message or self._lag_commit_melding(changed_files)
            self._run(["git", "commit", "-m", msg])

            branch = self._gjeldende_branch()
            self._run(["git", "push", "-u", "origin", branch])
            logger.info("Pushet %d filer til %s", len(changed_files), branch)
            return True

        except subprocess.CalledProcessError as e:
            logger.error("Git-kommando feilet: %s\nstderr: %s", e.cmd, e.stderr)
            return False
        except Exception as e:
            logger.error("Uventet feil ved publisering: %s", e)
            return False

    def _konfigurer_git(self):
        """Sett git-bruker for denne Pi-en (ikke sensitive opplysninger)."""
        self._run(["git", "config", "user.name", GIT_USER_NAME])
        self._run(["git", "config", "user.email", GIT_USER_EMAIL])

    def _konfigurer_remote(self):
        """Sett remote URL med token fra miljøvariabel (aldri lagret på disk)."""
        remote_url = f"https://{self._token}@github.com/{GITHUB_REPO}.git"
        self._run(["git", "remote", "set-url", "origin", remote_url])

    def _gjeldende_branch(self) -> str:
        result = self._run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        return result.stdout.strip()

    def _lag_commit_melding(self, files: list[Path]) -> str:
        kategorier = set()
        for f in files:
            # Hent første mappenivå under data/ som kategorinavn
            try:
                parts = f.relative_to(self.repo_root / "data").parts
                if parts:
                    kategorier.add(parts[0])
            except ValueError:
                pass

        kat_str = ", ".join(sorted(kategorier)) if kategorier else "diverse"
        return (
            f"auto: oppdater {len(files)} filer ({kat_str})\n\n"
            f"Automatisk scraping-kjøring fra norges-lover-bot.\n"
            f"Kilde-URL er dokumentert i hvert enkelt dokument."
        )

    def _run(
        self, cmd: list[str], check: bool = True
    ) -> subprocess.CompletedProcess:
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
        """Hent siste endringer fra remote før scraping."""
        try:
            self._konfigurer_remote()
            branch = self._gjeldende_branch()
            self._run(["git", "pull", "--ff-only", "origin", branch])
            logger.info("Hentet siste endringer fra origin/%s", branch)
            return True
        except subprocess.CalledProcessError as e:
            logger.warning("git pull feilet: %s", e.stderr)
            return False
