#!/usr/bin/env python3
"""Ugescanning af kommunernes egne nyhedslister for klimatilpasningsstof.

KP vil have alle 98 kommuners klimatilpasningsprojekter fanget (19/10-2026).
17 kommuner er live-kilder i sources.py. De øvrige ligger i
tools/kommune_kilder.json og scannes her én gang om ugen i stedet for live:
som live-kilder ville de give ca. 800 sidehentninger pr. /news/scrape på
Render free tier, og klimatilpasning fylder kun 0-13 nyheder om året pr.
kommune.

Scanneren genbruger main.py's egne hentere (fetch_sitemap_news, scrape_news,
fetch_rss), så den læser siderne præcis som produktionen. Kun nyheder med et
egentligt tilpasningsord (TILPASNING_RE) gemmes. Resultatet flettes med
forrige uges fil (365 dage rullende, dedup på URL) og lægges af workflowet
.github/workflows/kommunenyheder.yml på branchen kommune-data.

Brug:
    python tools/scan_kommunenyheder.py --ud /tmp/ud/kommunenyheder.json --tidligere /tmp/forrige.json
    python tools/scan_kommunenyheder.py --kun Køge,Greve   # test af enkelte kommuner
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROD = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROD))
import main as m  # noqa: E402

GRUPPE = "Kommuner"
Q = "klimatilpasning"


async def scan_kommune(client, kommune: str, meta: dict) -> tuple[str, list | Exception]:
    navn = f"{kommune} Kommune"
    try:
        if meta["type"] == "sitemap":
            res = await m.fetch_sitemap_news(client, navn, {**meta, "gruppe": GRUPPE,
                                                            "antal": meta.get("antal", 15)}, Q, limit=50)
        elif meta["type"] == "scrape":
            res = await m.scrape_news(client, navn, meta["url"], GRUPPE, Q, limit=50)
        elif meta["type"] == "rss":
            res = await m.fetch_rss(client, navn, meta["url"], Q, limit=50)
        else:
            return kommune, ValueError(f"ukendt type {meta['type']}")
    except Exception as e:
        return kommune, e
    if not isinstance(res, list):
        return kommune, res if isinstance(res, Exception) else RuntimeError("kunne ikke hentes")
    # Hvor mange poster der overhovedet kunne læses - ellers ligner en død
    # kilde og en uge uden klimanyheder hinanden ("0 fund").
    if meta["type"] == "sitemap":
        laest = len((m._SITEMAP_LISTE_CACHE.get(navn) or (0, []))[1])
    elif meta["type"] == "scrape":
        laest = len(((m._UDTRAEK_CACHE.get(meta["url"]) or (0, {}))[1] or {}).get("hoved") or [])
    else:
        # fetch_rss returnerer kun relevante poster; tæl feedets egne items.
        raa = m._FEED_CACHE.get(meta["url"])
        laest = len(m.parse_feed_items(raa[1])) if raa else len(res)
    if laest == 0:
        return kommune, RuntimeError("TOM - 0 poster læst (ændret side eller sitemap-mønster?)")
    ud = []
    for a in res:
        if not m.kun_tilpasning(f"{a.get('title') or ''} {a.get('summary') or ''}"):
            continue
        ud.append({
            "source": "kommune", "feedSource": navn, "org": navn, "kommune": kommune,
            "title": a.get("title") or "", "url": a.get("url") or "", "date": a.get("date") or "",
            "summary": (a.get("summary") or "")[:300], "relevance": a.get("relevance", 0.3),
            "value": None, "gruppe": GRUPPE,
        })
    return kommune, (ud, laest)


async def scan(kilder: dict) -> tuple[list, dict]:
    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=20),
                                 timeout=httpx.Timeout(30), follow_redirects=True) as client:
        res = await asyncio.gather(*[scan_kommune(client, k, meta) for k, meta in kilder.items()])
    artikler, status = [], {}
    for kommune, r in res:
        if isinstance(r, Exception):
            status[kommune] = f"FEJL: {m._fejltekst(r)}"
        else:
            fund, laest = r
            status[kommune] = f"{len(fund)} fund ({laest} poster læst)"
            artikler.extend(fund)
    return artikler, status


def flet(nye: list, tidligere: list) -> list:
    """Nye fund først; ældre fund beholdes i 365 dage. Dedup på URL."""
    alle, sete = [], set()
    for a in nye + tidligere:
        url = a.get("url") or ""
        if not url or url in sete or m.for_gammel(a.get("date") or ""):
            continue
        sete.add(url)
        alle.append(a)
    alle.sort(key=lambda a: a.get("date") or "", reverse=True)
    return alle


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ud", default="kommunenyheder.json")
    p.add_argument("--tidligere", default=None, help="forrige uges fil (flettes ind)")
    p.add_argument("--kun", default=None, help="kommaseparerede kommunenavne (test)")
    args = p.parse_args()

    konfig = json.loads((ROD / "tools" / "kommune_kilder.json").read_text(encoding="utf-8"))
    kilder = konfig["kommuner"]
    if args.kun:
        valgt = {k.strip() for k in args.kun.split(",")}
        kilder = {k: v for k, v in kilder.items() if k in valgt}

    nye, status = asyncio.run(scan(kilder))
    tidligere = []
    if args.tidligere and Path(args.tidligere).exists():
        try:
            tidligere = json.loads(Path(args.tidligere).read_text(encoding="utf-8"))
        except ValueError:
            tidligere = []
    alle = flet(nye, tidligere if isinstance(tidligere, list) else [])

    ud = Path(args.ud)
    ud.parent.mkdir(parents=True, exist_ok=True)
    ud.write_text(json.dumps(alle, ensure_ascii=False, indent=1), encoding="utf-8")

    fejl = {k: v for k, v in status.items() if v.startswith("FEJL")}
    print(f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC | {len(kilder)} kommuner scannet, "
          f"{len(fejl)} fejl, {len(nye)} fund i denne kørsel, {len(alle)} i filen")
    for k, v in sorted(status.items()):
        print(f"  {k}: {v}")
    for k in konfig.get("ikke_laesbar", {}):
        print(f"  ! {k}: ikke læsbar - {konfig['ikke_laesbar'][k]}")
    # Fejler mere end en tredjedel, er det et reelt problem (netværk, ændret
    # side-skabelon) - workflowet skal så stå rødt i stedet for at fejle tavst.
    if len(fejl) > len(kilder) / 3:
        sys.exit(1)


if __name__ == "__main__":
    main()
