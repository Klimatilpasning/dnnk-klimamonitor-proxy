#!/usr/bin/env python3
"""Mekanisk sundhedstjek af DNNK's online systemer (kører i GitHub Actions).

Indført 19/10-2026, så systemet overvåges under KP's barsel uden en tændt pc.
Tjekker kun det, der kører online: vidensassistentens sider og søgeindeks,
klimamonitoren på Render (nyheder, scrape-kilder, MCP) og de planlagte GitHub
Actions-jobs. Udskriver en JSON-liste [{navn, ok, tekst}] til stdout, som
.github/workflows/ugemail.yml sender videre til /send-ugemail.

Brug:  python tools/sundhedstjek.py [--uge]   (--uge tjekker også ugens vurdering)
"""
import json
import os
import sys
import time
from datetime import datetime, timezone

import httpx

RENDER = "https://dnnk-klimamonitor-proxy.onrender.com"
SIDER = {
    "Vidensassistent: søgeside": "https://klimatilpasning.github.io/dnnk-vidensassistent/",
    "Vidensassistent: dashboard": "https://klimatilpasning.github.io/dnnk-vidensassistent/dashboard.html",
    "Klimamonitor: frontend": "https://klimatilpasning.github.io/dnnk-klimamonitor-proxy/",
}
# (repo, workflow-fil eller -navn, maks. alder i dage)
JOBS = [
    ("Klimatilpasning/dnnk-klimamonitor-proxy", "dagsordener.yml", 8),
    ("Klimatilpasning/dnnk-klimamonitor-proxy", "kommunenyheder.yml", 8),
    ("Klimatilpasning/dnnk-vidensassistent", "Build Search Index", 3),
]
VURDERING = ("https://raw.githubusercontent.com/Klimatilpasning/dnnk-klimamonitor-proxy/"
             "claude/ugevurdering/ugevurdering.json")

ud = []


def tjek(navn, ok, tekst):
    ud.append({"navn": navn, "ok": bool(ok), "tekst": tekst})


def hent(c, url, forsoeg=3, **kw):
    """GET med gentagelser - Render free tier kan bruge op til et minut på at vågne."""
    sidst = None
    for i in range(forsoeg):
        try:
            r = c.get(url, timeout=120, **kw)
            if r.status_code < 500:
                return r
            sidst = f"HTTP {r.status_code}"
        except Exception as e:
            sidst = type(e).__name__
        time.sleep(20 * (i + 1))
    raise RuntimeError(sidst)


def main():
    uge = "--uge" in sys.argv
    gh = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        gh["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    with httpx.Client(follow_redirects=True, headers={"User-Agent": "dnnk-sundhedstjek"}) as c:
        for navn, url in SIDER.items():
            try:
                r = hent(c, url)
                tjek(navn, r.status_code == 200, f"HTTP {r.status_code}")
            except Exception as e:
                tjek(navn, False, f"svarer ikke ({e})")

        try:
            n = len(hent(c, "https://klimatilpasning.github.io/dnnk-vidensassistent/search-index.json").json())
            tjek("Vidensbank: søgeindeks", n >= 200, f"{n} webinarer/dokumenter")
        except Exception as e:
            tjek("Vidensbank: søgeindeks", False, f"kunne ikke læses ({e})")

        try:
            d = hent(c, f"{RENDER}/news/full", params={"q": "klimatilpasning", "gruppe": "Lovstof"}).json()
            n = len(d.get("articles") or [])
            tjek("Klimamonitor: backend (Render)", n > 0, f"{n} lovstof-artikler")
        except Exception as e:
            tjek("Klimamonitor: backend (Render)", False, f"svarer ikke ({e})")

        # Scrape-kilder: lige efter opvågning kan en hel hentebølge fejle i 60 s
        # (negativ cache). Gentag derfor én gang efter 90 s, før det er en fejl.
        try:
            for forsoeg in range(2):
                d = hent(c, f"{RENDER}/news/scrape", params={"q": "klimatilpasning"}).json()
                fejl = d.get("fejlede_kilder") or []
                if len(fejl) <= 5:
                    break
                time.sleep(90)
            kilder = len({a.get("feedSource") for a in d.get("articles") or []})
            tjek("Klimamonitor: scrape-kilder", len(fejl) <= 5 and kilder >= 15,
                 f"{kilder} kilder leverede, {len(fejl)} fejlede"
                 + (f" ({', '.join(fejl[:8])})" if fejl else ""))
        except Exception as e:
            tjek("Klimamonitor: scrape-kilder", False, f"svarer ikke ({e})")

        try:
            r = c.post(f"{RENDER}/mcp", timeout=120, headers={
                "Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
                json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                    "protocolVersion": "2025-06-18", "capabilities": {},
                    "clientInfo": {"name": "sundhedstjek", "version": "1"}}})
            tjek("Vidensbank: MCP-forbindelse", "dnnk-vidensbank" in r.text, f"HTTP {r.status_code}")
        except Exception as e:
            tjek("Vidensbank: MCP-forbindelse", False, f"svarer ikke ({e})")

        nu = datetime.now(timezone.utc)
        for repo, wf, dage in JOBS:
            navn = f"GitHub Actions: {wf.replace('.yml', '')}"
            try:
                if wf.endswith(".yml"):
                    runs = c.get(f"https://api.github.com/repos/{repo}/actions/workflows/{wf}/runs",
                                 params={"per_page": 5}, headers=gh, timeout=30).json()["workflow_runs"]
                else:
                    runs = [r for r in c.get(f"https://api.github.com/repos/{repo}/actions/runs",
                                             params={"per_page": 50}, headers=gh, timeout=30).json()["workflow_runs"]
                            if r["name"] == wf]
                faerdige = [r for r in runs if r["status"] == "completed"]
                if not faerdige:
                    tjek(navn, False, "ingen gennemførte kørsler fundet")
                    continue
                r = faerdige[0]
                alder = (nu - datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))).days
                tjek(navn, r["conclusion"] == "success" and alder <= dage,
                     f"seneste kørsel {r['created_at'][:10]}: {r['conclusion']}"
                     + (f" - over {dage} dage gammel" if alder > dage else ""))
            except Exception as e:
                tjek(navn, False, f"kunne ikke tjekkes ({type(e).__name__})")

        if uge:
            try:
                r = c.get(VURDERING, params={"x": nu.strftime("%Y%m%d%H")}, timeout=30)
                dato = r.json().get("dato", "")[:10] if r.status_code == 200 else ""
                alder = (nu.date() - datetime.fromisoformat(dato).date()).days if dato else 99
                tjek("Ugens vurdering (cloud-rutine)", alder <= 2,
                     f"seneste {dato}" if dato else "ingen vurdering fundet")
            except Exception as e:
                tjek("Ugens vurdering (cloud-rutine)", False, f"kunne ikke læses ({type(e).__name__})")

    json.dump(ud, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
