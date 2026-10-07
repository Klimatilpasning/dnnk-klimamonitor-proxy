"""Finder hvilke kommuner der har det fælles dagsordenssystem (dagsordener.<kommune>.dk med /api/agenda/).
Skriver dagsorden_portaler.json. Køres sjældent (fx hvert halve år).
Kendte værter, der ikke genfindes (fx fordi de ligger under et uventet navn), bevares fra den
eksisterende fil, så en kørsel aldrig kan nulstille en kommune, der virker."""
import json, itertools, requests, concurrent.futures as cf
from pathlib import Path

HER = Path(__file__).parent
KOMMUNER = [x['kommune'] for x in json.load(open(HER.parent.parent / 'kommune_results.json', encoding='utf-8'))]
EKSTRA = {'København': ['kk'], 'Ringkøbing-Skjern': ['rksk'], 'Nordfyns Kommune': ['nordfyns', 'nordfynskommune'],
          'Bornholm': ['brk'], 'Lyngby-Taarbæk': ['ltk'], 'Høje-Taastrup': ['htk'], 'Aalborg': ['aalborgkommune'],
          'Faaborg-Midtfyn': ['fmk'], 'Morsø': ['mors'], 'Rødovre': ['rk'], 'Vesthimmerlands': ['vesthimmerland']}
# Samme system ligger også under disse værtspræfikser (fundet 7/10-2026, fx udvalg.kolding.dk)
PRAEFIKSER = ('dagsordener', 'dagsorden', 'dagsordner', 'udvalg', 'dagsordener-referater')

def slugs(navn):
    base = navn.lower().replace(' kommune', '')
    ud = set()
    for oe, ae, aa in itertools.product(['oe', 'o'], ['ae', 'a'], ['aa', 'a']):
        s = base.replace('ø', oe).replace('æ', ae).replace('å', aa)
        for t in (s, s.replace('-', '')):
            ud |= {t, t + 'kommune', t + '-kommune'}
    ud |= set(EKSTRA.get(navn, []))
    return sorted(ud)

def test(host):
    s = requests.Session(); s.headers['User-Agent'] = 'Mozilla/5.0 (DNNK dagsordensovervaagning)'
    try:
        s.get(f'https://{host}/', timeout=8)
        r = s.get(f'https://{host}/api/agenda/udvalgsliste', timeout=12)
        return host if r.ok and 'Udvalg' in r.json() else None
    except Exception:
        return None

def find(navn):
    for sl in slugs(navn):
        for pre in PRAEFIKSER:
            h = test(f'{pre}.{sl}.dk')
            if h: return navn, h
    return navn, None

if __name__ == '__main__':
    fil = HER / 'dagsorden_portaler.json'
    gamle = json.load(open(fil, encoding='utf-8')) if fil.exists() else {}
    with cf.ThreadPoolExecutor(12) as ex:
        res = dict(ex.map(find, KOMMUNER))
    for k, v in res.items():
        if not v and gamle.get(k) and test(gamle[k]):
            res[k] = gamle[k]
    json.dump(res, open(fil, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    ok = {k: v for k, v in res.items() if v}
    print(f'{len(ok)}/{len(res)} kommuner med fælles dagsordenssystem')
    print('Mangler:', ', '.join(k for k, v in res.items() if not v))
