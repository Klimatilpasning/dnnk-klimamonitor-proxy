"""Scanning af politiske dagsordener i de kommuner, der bruger det fælles dagsordenssystem
(dagsordener.<kommune>.dk med åbent /api/agenda/-API). Finder klimatilpasningsrelevante punkter
(klimaord i titel eller resumé) i møder fra FORTID dage tilbage til FREMTID dage frem.

Bruges to steder:
  - GitHub Actions (dagsordener.yml) skriver --monitor-json til branchen dagsorden-data,
    som /news/full læser som gruppen "Politiske dagsordener".
  - Kommune-rutinen om mandagen skriver en læsbar rapport med --ud-mappe og husker sete
    punkter i <ud-mappe>/seen.json, så rapporten kun viser det nye.

Systemet kræver en anonym cookie: forsiden hentes først i samme session, ellers svarer API'et 302.
dagsorden_portaler.json vedligeholdes med find_dagsorden_portaler.py (ikke del af ugekørslen)."""
import json, re, time, html, zlib, argparse, datetime as dt, requests
from pathlib import Path

HER = Path(__file__).parent
FORTID, FREMTID, PAUSE, BEHOLD_DAGE = 8, 21, 0.4, 45

# Stærke ord peger direkte på klimatilpasning og må stå i titel eller resumé.
# Svage ord er for brede til resuméet og tæller kun i punktets titel.
# 'LAR' er bevidst udeladt: i dagsordener betyder det oftest Lokalt Arbejdsmarkedsråd.
STAERK = r'klimatilpasning|skybrud|oversvøm|stormflod|højvande|kystbeskyttelse|kystsikring|klimasikring|sandfodring|' \
         r'terrænnær|havvandsstigning|havstigning|vandstandsstigning|risikostyringsplan|klimarobust|forsinkelsesbassin|' \
         r'regnvandsbassin|vandhåndteringsplan|klimalavbund|\bdige(?:r|t|rne|projekt|lag)?\b'
SVAG = r'regnvand|grundvandsstand|nedsivning|vandhåndtering|spildevandsplan|lavbund|vådområde|erosion|kystnær|vandløbsprojekt'
PLAN = r'klimatilpasningsplan|klimaplan|risikostyringsplan|kommuneplan|spildevandsplan|vandhåndteringsplan|strategi|høring'


def tekst(h):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h or ''))).strip()


def resume(punkt):
    for f in punkt.get('Felter') or []:
        m = re.search(r"<span class='resume'>(.*?)</span>\s*</div>", f.get('Html') or '', re.S)
        if m:
            return tekst(m.group(1))
    return ''


def session(host):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (DNNK dagsordensovervaagning)'
    s.get(f'https://{host}/', timeout=15)
    return s


def scan_kommune(kommune, host, fra, til):
    s = session(host)
    fund = []
    udv = s.get(f'https://{host}/api/agenda/udvalgsliste', timeout=20).json()['Udvalg']
    for gruppe in udv.values():
        for u in gruppe:
            for m in u.get('Moeder') or []:
                dato = dt.date.fromisoformat(m['Dato'][:10])
                if not (fra <= dato <= til):
                    continue
                time.sleep(PAUSE)
                try:
                    d = s.get(f"https://{host}/api/agenda/dagsorden/{m['Id']}", timeout=30).json()
                except Exception as e:
                    print(f'  ! {kommune} {u["Navn"]} {dato}: {e}')
                    continue
                for p in d.get('Dagsordenpunkter') or []:
                    titel = (p.get('Navn') or p.get('Caption') or '').strip()
                    res = resume(p)
                    tl = titel.lower()
                    hit_t = re.findall(STAERK, tl) + re.findall(SVAG, tl)
                    hit_r = re.findall(STAERK, res.lower())
                    if not (hit_t or hit_r):
                        continue
                    fund.append(dict(
                        kommune=kommune, udvalg=u['Navn'], dato=str(dato), titel=titel,
                        resume=res[:500], styrke='titel' if hit_t else 'resumé',
                        staerk_titel=bool(re.search(STAERK, tl)),
                        ord=sorted(set(hit_t + hit_r)),
                        type='plan-status' if re.search(PLAN, tl) else 'webinarlead',
                        sag=p.get('SagsNummer') or '', punkt=p.get('Punktnummer') or '',
                        url=f"https://{host}/vis?id={m['Id']}",
                        nogle=f"{host}|{dato}|{p.get('SagsNummer')}|{titel}"))
    return fund


def til_monitor(f):
    """Samme felter som de øvrige artikler i /news/full; tags og webinarer lægges på i backenden."""
    return {"source": f"Dagsorden: {f['kommune']}", "feedSource": "Politiske dagsordener",
            "org": f"{f['kommune']} Kommune",
            "title": f"{f['kommune']}: {f['titel']}",
            # Flere punkter deler mødets link; frontenden kender artikler på URL'en (læst/stemt),
            # så punktnummeret lægges på som fragment for at holde dem adskilt.
            "url": f"{f['url']}#punkt-{f['punkt'] or zlib.crc32(f['titel'].encode())}", "date": f['dato'],
            "summary": (f"{f['udvalg']}, møde {f['dato']}, pkt. {f['punkt']}. " + f['resume'])[:400],
            # Stærkt ord i titlen > kun svagt ord i titlen (fx rutinetillæg til spildevandsplanen) > kun i resuméet
            "relevance": 0.9 if f.get('staerk_titel') else 0.7 if f['styrke'] == 'titel' else 0.6, "value": "",
            "nogle": f['nogle'], "dagsordentype": f['type']}


def skriv_monitor(alle, sti, tidligere, idag):
    """Rullende fil: ugens fund + tidligere fund fra de sidste BEHOLD_DAGE dage (pr. mødedato)."""
    graense = str(idag - dt.timedelta(BEHOLD_DAGE))
    samlet = {a['nogle']: a for a in tidligere if a.get('date', '') >= graense}
    samlet.update({f['nogle']: til_monitor(f) for f in alle})
    # Samme sag behandles ofte i udvalg og derefter byråd: vis den kun én gang, med det seneste møde.
    pr_sag = {}
    for a in sorted(samlet.values(), key=lambda a: a['date']):
        pr_sag[(a['org'], a['title'])] = a
    ud = sorted(pr_sag.values(), key=lambda a: a['date'], reverse=True)
    Path(sti).parent.mkdir(parents=True, exist_ok=True)
    json.dump(ud, open(sti, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'monitor-json: {len(ud)} punkter -> {sti}')


def skriv_rapport(nye, mappe, idag, fra, til, n, fejl):
    (mappe / 'fund').mkdir(parents=True, exist_ok=True)
    nye.sort(key=lambda f: (f['styrke'] != 'titel', f['type'], f['kommune'], f['dato']))
    L = [f'# Dagsordensscanning {idag}', '',
         f'Møder {fra} til {til} i {n} kommuner. {len(nye)} nye klimarelevante punkter.'
         + (f' Fejl: {", ".join(fejl)}.' if fejl else ''), '']
    for styrke, overskrift in (('titel', 'Klimaord i punktets titel'), ('resumé', 'Klimaord kun i resuméet')):
        grp = [f for f in nye if f['styrke'] == styrke]
        if not grp:
            continue
        L += [f'## {overskrift} ({len(grp)})', '']
        for f in grp:
            L.append(f"- **{f['kommune']}** - {f['udvalg']} {f['dato']}, pkt. {f['punkt']} - "
                     f"[{f['titel']}]({f['url']}) `{f['type']}` _({', '.join(f['ord'])})_")
            if f['resume']:
                L.append(f"  > {f['resume'][:300]}")
        L.append('')
    (mappe / 'fund' / f'dagsorden_fund_{idag}.md').write_text('\n'.join(L), encoding='utf-8')
    json.dump(nye, open(mappe / 'fund' / f'dagsorden_fund_{idag}.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kommuner', help='kommasepareret delmængde, fx Herlev,Vejle')
    ap.add_argument('--ud-mappe', help='skriv læsbar rapport + seen.json her (kommune-rutinen)')
    ap.add_argument('--alle', action='store_true', help='ignorér seen.json')
    ap.add_argument('--monitor-json', help='skriv rullende JSON til klimamonitoren her')
    ap.add_argument('--tidligere', help='forrige monitor-json, der flettes ind')
    a = ap.parse_args()
    portaler = {k: v for k, v in json.load(open(HER / 'dagsorden_portaler.json', encoding='utf-8')).items() if v}
    if a.kommuner:
        portaler = {k: v for k, v in portaler.items() if k in a.kommuner.split(',')}
    idag = dt.date.today()
    fra, til = idag - dt.timedelta(FORTID), idag + dt.timedelta(FREMTID)
    alle, fejl = [], []
    for k, h in portaler.items():
        try:
            f = scan_kommune(k, h, fra, til)
            alle += f
            print(f'{k}: {len(f)}', flush=True)
        except Exception as e:
            fejl.append(k)
            print(f'! {k}: {e}', flush=True)
    if a.monitor_json:
        tidl = []
        if a.tidligere and Path(a.tidligere).exists():
            try:
                tidl = json.load(open(a.tidligere, encoding='utf-8'))
            except ValueError:
                pass
        skriv_monitor(alle, a.monitor_json, tidl, idag)
    if a.ud_mappe:
        mappe = Path(a.ud_mappe)
        seen_f = mappe / 'seen.json'
        seen = set() if a.alle or not seen_f.exists() else set(json.load(open(seen_f, encoding='utf-8')))
        nye = [f for f in alle if f['nogle'] not in seen]
        mappe.mkdir(parents=True, exist_ok=True)
        json.dump(sorted(seen | {f['nogle'] for f in alle}), open(seen_f, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=0)
        skriv_rapport(nye, mappe, idag, fra, til, len(portaler), fejl)
        print(f'{len(nye)} nye fund til rapporten')
    print(f'\n{len(alle)} fund i {len(portaler)} kommuner; fejl: {fejl or "ingen"}')


if __name__ == '__main__':
    main()
