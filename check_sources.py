#!/usr/bin/env python3
"""Kilde-sundhedstjek for Klimamonitoren.

Svarer på ét spørgsmål pr. kilde: ville monitoren kunne trække indhold ud af
den lige nu? Derfor genbruges main.py's EGNE funktioner (_vaelg_kandidater,
_titel_element, RSS_HEADERS) i stedet for et selvstændigt tjek — ellers tester
vi noget andet end det produktionen gør, og det er præcis dér falske alarmer
opstår. Konkret gælder for scrape-kilder, at HTTP-statuskoden IKKE afgør noget:
flere danske CMS-sider svarer 404 og leverer alligevel hele nyhedslisten i
body'en, og scrape_news() parser dem derfor uanset status.

Kategorier:
  OK      — indhold kunne udtrækkes
  TOM     — svarer, men intet kunne udtrækkes. Den farlige kategori: kilden
            fejler TAVST, fordi monitoren bare ser 0 artikler og ikke kan
            skelne det fra "ingen nyheder i denne uge".
  NETVAERK — DNS-fejl, TLS-fejl, timeout eller afvist forbindelse. Kan skyldes
            bot-filtre eller det netværk tjekket køres fra, snarere end reel
            nedetid — verificér manuelt før en kilde fjernes.

Bing-søgefeeds med 0 items rapporteres som OK: de er fangnet der kun slår ud,
når der faktisk er nyheder om et smalt fagord, så tomhed er forventet.

Brug:
    python check_sources.py             # alle kilder
    python check_sources.py --kun-fejl  # kun kilder der ikke er OK

Exit-kode 1 hvis der findes TOM-kilder, så det ugentlige sundhedstjek fanger
det automatisk.
"""

import argparse
import re
import socket
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup

import main as prod
from sources import ALL_FEEDS_FLAT, SCRAPE_SOURCES

TIMEOUT = 20
ITEM_RE = re.compile(rb"<(?:item|entry)[\s>]", re.IGNORECASE)
# Samme tærskel som scrape_news(): under dette parser produktionen slet ikke.
MIN_BODY = 2000


def hent(url):
    """Returnér (status, body). Status er et tal eller en fejlstreng."""
    req = urllib.request.Request(url, headers=prod.RSS_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.getcode(), r.read(2_000_000)
    except urllib.error.HTTPError as e:
        # Statuskoden er med vilje ikke diskvalificerende for scrape-kilder —
        # body'en kan sagtens indeholde nyhedslisten alligevel.
        try:
            return e.code, e.read(2_000_000)
        except Exception:
            return e.code, b""
    except (urllib.error.URLError, socket.timeout, ConnectionError, OSError) as e:
        return f"NETVAERK ({type(getattr(e, 'reason', e)).__name__})", b""


def tael_titler(html):
    """Kør produktionens udtrækskæde og tæl brugbare titler."""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["nav", "footer", "script", "style", "header"]):
        tag.decompose()
    kandidater = prod._vaelg_kandidater(soup)
    if not kandidater:
        soup = BeautifulSoup(html, "lxml")
        for tag in soup(["script", "style"]):
            tag.decompose()
        kandidater = prod._vaelg_kandidater(soup)

    titler = set()
    for el in kandidater[:25]:
        titel_el = prod._titel_element(el)
        if not titel_el:
            continue
        titel = titel_el.get_text(strip=True)
        if titel and len(titel) >= 8:
            titler.add(titel)
    return len(titler)


def tjek(navn, url, gruppe, er_feed):
    status, body = hent(url)

    if isinstance(status, str):
        return navn, gruppe, url, "NETVAERK", status

    if er_feed:
        antal = len(ITEM_RE.findall(body))
        if antal:
            return navn, gruppe, url, "OK", f"{antal} items"
        if "Bing News" in navn:
            return navn, gruppe, url, "OK", "0 items (forventet for soegefeed)"
        return navn, gruppe, url, "TOM", f"HTTP {status}, 0 feed-items"

    if len(body) < MIN_BODY:
        return navn, gruppe, url, "TOM", f"HTTP {status}, body kun {len(body)} tegn"

    try:
        antal = tael_titler(body)
    except Exception as e:
        return navn, gruppe, url, "TOM", f"HTTP {status}, parse-fejl {type(e).__name__}"

    if antal == 0:
        return navn, gruppe, url, "TOM", f"HTTP {status}, 0 titler udtrukket"
    return navn, gruppe, url, "OK", f"{antal} titler"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kun-fejl", action="store_true", help="udelad kilder der er OK")
    args = p.parse_args()

    opgaver = [(n, m["url"], m["gruppe"], True) for n, m in ALL_FEEDS_FLAT.items()]
    opgaver += [(n, m["url"], m["gruppe"], False) for n, m in SCRAPE_SOURCES.items()]

    with ThreadPoolExecutor(max_workers=12) as pool:
        resultater = list(pool.map(lambda a: tjek(*a), opgaver))

    raekkefoelge = {"TOM": 0, "NETVAERK": 1, "OK": 2}
    resultater.sort(key=lambda r: (raekkefoelge[r[3]], r[1], r[0]))

    tael = {}
    for _, _, _, status, _ in resultater:
        tael[status] = tael.get(status, 0) + 1

    for navn, gruppe, url, status, note in resultater:
        if args.kun_fejl and status == "OK":
            continue
        print(f"{status:9s} {gruppe:26s} {navn:34s} {note:34s} {url}")

    print(f"\n{len(resultater)} kilder tjekket: " +
          ", ".join(f"{tael.get(s, 0)} {s}" for s in ("OK", "TOM", "NETVAERK")))

    if tael.get("TOM"):
        print("\nTOM = kilden svarer, men intet kunne udtrækkes. Den fejler tavst: "
              "monitoren ser bare 0 artikler.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
