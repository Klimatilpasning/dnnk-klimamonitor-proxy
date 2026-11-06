#!/usr/bin/env python3
"""Henter teksten fra en side til klimamonitor-vurderingen.

Brug: python3 hent_side.py URL [URL ...]   (skriver tekst pr. URL til stdout)

Metoder, i rækkefølge:
1. Kommunale dagsordensystemer (".../vis?id=...&punktid=..."): anonymt login via
   cookie, derefter API'et /api/agenda/dagsorden/<id>, og kun det relevante punkt.
2. Almindelig curl med browser-User-Agent.
3. Playwright (forudinstalleret Chromium) til JavaScript-sider som retsinformation.dk.

Svarer en dagsorden "Der kunne ikke opnåes tilstrækkelig adgang", ligger fejlen hos
kommunens server - så vurderes punktet på titel og resumé.
"""
import html
import json
import re
import subprocess
import sys
import tempfile
import urllib.parse as up

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"


def ren(h):
    h = re.sub(r"(?s)<(script|style).*?</\1>", "", h)
    h = re.sub(r"<(br|/p|/div|/li|/h\d)[^>]*>", "\n", h)
    h = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", h)).strip()


def curl(args):
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA] + args, capture_output=True, text=True)
    return r.stdout


def dagsorden(u):
    q = up.urlparse(u)
    Q = up.parse_qs(q.query)
    if q.path.lower() != "/vis" or "id" not in Q:
        return None
    jar = tempfile.mktemp()
    host = f"{q.scheme}://{q.netloc}"
    curl(["-c", jar, "-b", jar, "-o", "/dev/null", u])
    raw = curl(["-b", jar, "-H", "Accept: application/json", f"{host}/api/agenda/dagsorden/{Q['id'][0]}"])
    try:
        j = json.loads(raw)
    except ValueError:
        return None
    if not isinstance(j, dict):
        return "SERVERFEJL: " + str(j)[:200]
    pid = Q.get("punktid", [None])[0]
    pnr = Q.get("punkt", [None])[0]
    ud = []
    for p in j.get("Dagsordenpunkter", []):
        if (pid is None and pnr is None) or p.get("Id") == pid or p.get("Number") == pnr:
            felter = "\n".join(ren(f.get("Html") or f.get("Tekst") or "") for f in p.get("Felter") or [])
            ud.append((p.get("Caption") or "") + "\n" + felter)
    return "\n\n".join(ud) or None


def playwright(u):
    js = (
        "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();"
        f"const p=await b.newPage({{userAgent:{json.dumps(UA)}}});"
        f"try{{await p.goto({json.dumps(u)},{{waitUntil:'networkidle',timeout:45000}});"
        "await p.waitForTimeout(2500);console.log(await p.evaluate(()=>document.body.innerText));}"
        "catch(e){console.log('FEJL '+e.message.slice(0,150))}await b.close();})();"
    )
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=90)
    return r.stdout.strip()


def hent(u):
    t = dagsorden(u)
    if t:
        return t
    s = ren(curl([u]))
    if len(s) > 1500 and "Enable JavaScript" not in s:
        return s
    try:
        return playwright(u)
    except Exception as e:  # noqa: BLE001
        return f"FEJL: {e}"


if __name__ == "__main__":
    for u in sys.argv[1:]:
        print(f"===== {u}")
        print(hent(u)[:8000])
