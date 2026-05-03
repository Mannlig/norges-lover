"""
Scraper for Lovdata.
Bruker nodriver (headless Chromium) for å omgå bot-deteksjon.
Henter nasjonale lover og forskrifter fra lovdata.no.

Kilde: https://lovdata.no
Vilkår: Kun offentlig tilgjengelig innhold. Respekterer rate limits.
nodriver: https://github.com/ultrafunkamsterdam/nodriver
"""

import asyncio
import json
import logging
from pathlib import Path

from .base import BaseScraper

logger = logging.getLogger(__name__)

LOV_KATEGORIER = [
    ("arbeidsliv", "https://lovdata.no/register/lover?topic=arbeidsliv"),
    ("skatt", "https://lovdata.no/register/lover?topic=skatt"),
    ("trygd", "https://lovdata.no/register/lover?topic=trygd"),
    ("bygg", "https://lovdata.no/register/lover?topic=bygg"),
    ("familie", "https://lovdata.no/register/lover?topic=familie"),
    ("helse", "https://lovdata.no/register/lover?topic=helse"),
    ("miljoe", "https://lovdata.no/register/lover?topic=miljo"),
    ("naering", "https://lovdata.no/register/lover?topic=naering"),
    ("offentlig-forvaltning", "https://lovdata.no/register/lover?topic=forvaltning"),
]

PRIORITERTE_LOVER = [
    ("arbeidsmiljoeloven", "https://lovdata.no/lov/2005-06-17-62"),
    ("skatteloven", "https://lovdata.no/lov/1999-03-26-14"),
    ("merverdiavgiftsloven", "https://lovdata.no/lov/2009-06-19-58"),
    ("plan-og-bygningsloven", "https://lovdata.no/lov/2008-06-27-71"),
    ("forvaltningsloven", "https://lovdata.no/lov/1967-02-10"),
    ("folketrygdloven", "https://lovdata.no/lov/1997-02-28-19"),
    ("barnelova", "https://lovdata.no/lov/1981-04-08-7"),
    ("husleieloven", "https://lovdata.no/lov/1999-03-26-17"),
    ("avtaleloven", "https://lovdata.no/lov/1918-05-31-4"),
    ("straffeloven", "https://lovdata.no/lov/2005-05-20-28"),
    ("likestillingsloven", "https://lovdata.no/lov/2017-06-16-51"),
    ("personopplysningsloven", "https://lovdata.no/lov/2018-06-15-38"),
    ("aksjeloven", "https://lovdata.no/lov/1997-06-13-44"),
    ("regnskapsloven", "https://lovdata.no/lov/1998-07-17-56"),
    ("konkursloven", "https://lovdata.no/lov/1984-06-08-58"),
]


class LovdataScraper(BaseScraper):
    name = "lovdata"
    source_url = "https://lovdata.no"

    def scrape(self, output_dir: Path, max_pages: int = 50) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        return asyncio.run(self._scrape_async(output_dir, max_pages))

    async def _scrape_async(self, output_dir: Path, max_pages: int) -> list[Path]:
        try:
            import nodriver as uc
        except ImportError:
            logger.error(
                "nodriver er ikke installert. Kjør: pip install nodriver\n"
                "Chromium kreves: sudo apt install chromium-browser"
            )
            return []

        created = []
        browser = None
        try:
            browser = await uc.start(
                headless=True,
                browser_executable_path="/usr/bin/chromium-browser",
                browser_args=["--no-sandbox", "--disable-dev-shm-usage"],
            )

            for navn, url in PRIORITERTE_LOVER[:max_pages]:
                try:
                    path = await self._hent_lov(browser, output_dir / "lover", url, navn)
                    if path:
                        created.append(path)
                except Exception as e:
                    logger.warning("Feil ved henting av %s: %s", url, e)
                await asyncio.sleep(5)

            remaining = max_pages - len(created)
            if remaining > 0:
                for kategori, url in LOV_KATEGORIER:
                    links = await self._hent_lenker_fra_kategori(browser, url)
                    for lenke_url, tittel in links[:5]:
                        if len(created) >= max_pages:
                            break
                        slug = self.slugify(tittel)
                        try:
                            path = await self._hent_lov(
                                browser, output_dir / "kategorier" / kategori, lenke_url, slug
                            )
                            if path:
                                created.append(path)
                        except Exception as e:
                            logger.warning("Feil ved %s: %s", lenke_url, e)
                        await asyncio.sleep(6)

        finally:
            if browser:
                try:
                    await browser.stop()
                except Exception:
                    pass

        logger.info("Lovdata: %d filer endret/nye", len(created))
        return created

    async def _hent_lov(self, browser, output_dir: Path, url: str, navn: str) -> Path | None:
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / f"{navn}.md"

        page = None
        try:
            page = await browser.get(url)
            await asyncio.sleep(3)

            tittel = await page.evaluate(
                "document.querySelector('h1')?.innerText || document.title || ''"
            )

            raa_innhold = ""
            for selector in ["div.law-content", "article", "main", "#lovtekst", ".lovtekst"]:
                raa_innhold = await page.evaluate(
                    f"document.querySelector('{selector}')?.innerText || ''"
                )
                if raa_innhold.strip():
                    break

            if not raa_innhold.strip():
                logger.warning("Ingen innhold funnet for %s", url)
                return None

            oppdatert = await page.evaluate(
                "document.querySelector('.last-updated, .date-modified, time')?.innerText || ''"
            )

            formatert = self._formater_lov(tittel.strip(), raa_innhold.strip(), url, oppdatert.strip())
            # Hash kun selve lovteksten, ikke tidsstempler
            endret = self.skriv_hvis_endret(filepath, raa_innhold.strip(), formatert)
            return filepath if endret else None

        except Exception as e:
            logger.warning("Feil ved henting av %s: %s", url, e)
            return None
        finally:
            if page:
                try:
                    await page.close()
                except Exception:
                    pass

    async def _hent_lenker_fra_kategori(self, browser, url: str) -> list[tuple[str, str]]:
        page = None
        try:
            page = await browser.get(url)
            await asyncio.sleep(3)
            lenker_json = await page.evaluate("""
                JSON.stringify(
                    Array.from(document.querySelectorAll('a[href*="/lov/"]'))
                    .map(a => ({href: a.href, text: a.innerText.trim()}))
                    .filter(a => a.text.length > 5)
                    .slice(0, 20)
                )
            """)
            lenker = json.loads(lenker_json or "[]")
            return [(l["href"], l["text"]) for l in lenker]
        except Exception as e:
            logger.warning("Feil ved henting av kategori %s: %s", url, e)
            return []
        finally:
            if page:
                try:
                    await page.close()
                except Exception:
                    pass

    def _formater_lov(self, tittel: str, innhold: str, url: str, oppdatert: str) -> str:
        return "\n".join([
            f"# {tittel}",
            "",
            "## Kildeinformasjon",
            "",
            f"- **Kilde:** Lovdata – {url}",
            f"- **Sist oppdatert (kilde):** {oppdatert or 'ukjent'}",
            f"- **Sist hentet:** {self.now_iso()}",
            "",
            "## Lovtekst",
            "",
            innhold,
            "",
            "---",
            "",
            f"*Automatisk hentet fra [Lovdata]({url}) av norges-lover-bot. "
            "Se [mannlig/norges-lover](https://github.com/mannlig/norges-lover) for kildekode.*",
        ])
