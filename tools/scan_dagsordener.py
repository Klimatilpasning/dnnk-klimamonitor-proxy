"""Scanning af politiske dagsordener i de kommuner, der bruger det fælles dagsordenssystem
(dagsordener.<kommune>.dk med åbent /api/agenda/-API). Finder klimatilpasningsrelevante punkter
(klimaord i titel eller resumé) i møder fra FORTID dage tilbage til FREMTID dage frem.

Bruges to steder:
  - GitHub Actions (dagsordener.yml) skriver --monitor-json til branchen dagsorden-data,
    som /news/full læser som gruppen "Politiske dagsordener".
  - Kommune-rutinen om mandagen skriver en læsbar rapport med --ud-mappe og husker sete
    punkter i <ud-mappe>/seen.json, så rapporten kun viser det nye.

Systemet kræver en anonym cookie: forsiden hentes først i samme session, ellers svarer API'et 302.
dagsorden_portaler.json vedligeholdes med find_dagsorden_portaler.py (ikke del af ugekørslen).
En værdi i filen er enten en FirstAgenda-vært (streng) eller et objekt med 'type' for kommuner
med andre systemer (se ADAPTERE: København = kk_jsonapi, Aalborg = aalborg)."""
import json, re, time, html, zlib, argparse, datetime as dt, requests
from urllib.parse import quote, unquote
from pathlib import Path

HER = Path(__file__).parent
FORTID, FREMTID, PAUSE, BEHOLD_DAGE = 8, 21, 0.4, 45

# Stærke ord peger direkte på klimatilpasning og må stå i titel eller resumé.
# Svage ord er for brede til resuméet og tæller kun i punktets titel.
# 'LAR' er bevidst udeladt: i dagsordener betyder det oftest Lokalt Arbejdsmarkedsråd.
STAERK = r'klimatilpasning|skybrud|oversvøm|stormflod|højvande|kystbeskyttelse|kystsikring|klimasikring|sandfodring|' \
         r'terrænnær|havvandsstigning|havstigning|vandstandsstigning|risikostyringsplan|klimarobust|forsinkelsesbassin|' \
         r'regnvandsbassin|vandhåndteringsplan|klimalavbund|\bdige(?:r|t|rne|projekt|lag)?\b'
# Udvidet 6/10-2026 efter måling på 12.979 dagsordenspunkter fra 77 kommuner: de svage ord
# gav lav støj i titler, men meget i resuméer ("forsinket", "genopretningsplan", affaldsregulativ).
# "klima", "vand", "forsyning" og "medfinansiering" alene er bevidst udeladt (for meget støj).
SVAG = r'regnvand|regnbed|grundvand|nedsivning|vandhåndtering|spildevandsplan|lavbund|vådområde|erosion|kyst|' \
       r'vandløb|grødeskæring|separatkloak|fælleskloak|overløb|forsinkelsesvolumen|naturgenopret|genslyng|' \
       r'grøn trepart|klimaplan|klimahandleplan|klimahandlingsplan|skovrejsning'
PLAN = r'klimatilpasningsplan|klimaplan|klimahandle|klimahandlings|risikostyringsplan|kommuneplan|spildevandsplan|' \
       r'vandhåndteringsplan|omlægningsplan|regulativ|strategi|høring'


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
                    d = s.get(f"https://{host}/api/agenda/dagsorden/{m['Id']}", timeout=60).json()
                except Exception as e:
                    print(f'  ! {kommune} {u["Navn"]} {dato}: {e}')
                    continue
                for p in d.get('Dagsordenpunkter') or []:
                    f = match_punkt(kommune, u['Navn'], dato, p.get('Navn') or p.get('Caption') or '', resume(p),
                                    f"https://{host}/vis?id={m['Id']}", p.get('SagsNummer') or '',
                                    p.get('Punktnummer') or '', host)
                    if f:
                        fund.append(f)
    return fund


def match_punkt(kommune, udvalg, dato, titel, res, url, sag, punkt, kilde):
    """Fælles for alle adaptere: returnerer et fund, hvis punktet er klimarelevant, ellers None."""
    # Nogle kommuner sætter punktnummeret foran titlen ("11. Orientering ..."); fjernes,
    # så samme sag i udvalg og byråd kan slås sammen i skriv_monitor.
    titel = re.sub(r'^\d+\.\s*', '', re.sub(r'\s+', ' ', titel).strip())
    tl = titel.lower()
    hit_t = re.findall(STAERK, tl) + re.findall(SVAG, tl)
    hit_r = re.findall(STAERK, (res or '').lower())
    if not (hit_t or hit_r):
        return None
    return dict(
        kommune=kommune, udvalg=udvalg, dato=str(dato), titel=titel,
        resume=(res or '')[:500], styrke='titel' if hit_t else 'resumé',
        staerk_titel=bool(re.search(STAERK, tl)),
        ord=sorted(set(hit_t + hit_r)),
        type='plan-status' if re.search(PLAN, tl) else 'webinarlead',
        sag=sag, punkt=punkt, url=url, nogle=f"{kilde}|{dato}|{sag}|{titel}")


# ── København: Drupal JSON:API på kk.dk ─────────────────────────────────────
# Ét pagineret kald giver alle udvalgs (inkl. lokaludvalgs) punkter med titel, dato og sti.
# Udvalget er 2. led i path.alias, og hvert punkt har sin egen side (/.../punkt-N).
# Samme punkt findes både under /dagsorden/ og /referat/ - de slås sammen her.
# Klammerne i filter-parametrene skal sendes uændret (requests' params URL-koder dem korrekt).
KK = 'https://www.kk.dk'


def scan_kk(kommune, cfg, fra, til):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (DNNK dagsordensovervaagning)'
    params = {
        'filter[fra][condition][path]': 'agenda_meeting_date',
        'filter[fra][condition][operator]': '>=',
        'filter[fra][condition][value]': str(fra),
        'filter[til][condition][path]': 'agenda_meeting_date',
        'filter[til][condition][operator]': '<',
        'filter[til][condition][value]': str(til + dt.timedelta(1)),
        'fields[node--agenda_element]': 'title,path,agenda_meeting_date,agenda_element_serial_no',
        'sort': 'agenda_meeting_date',
        'page[limit]': '50',
    }
    url, fund, set_punkter, sider = f'{KK}/jsonapi/node/agenda_element', [], set(), 0
    while url and sider < 200:          # loft mod løbske løkker (~10.000 punkter)
        r = s.get(url, params=params if sider == 0 else None, timeout=60)
        r.raise_for_status()
        d = r.json()
        sider += 1
        for x in d.get('data') or []:
            a = x.get('attributes') or {}
            dato = dt.date.fromisoformat((a.get('agenda_meeting_date') or '')[:10])
            if not (fra <= dato <= til):
                continue
            alias = (a.get('path') or {}).get('alias') or ''
            led = alias.strip('/').split('/')
            udvalg = led[1] if len(led) > 1 else 'Ukendt udvalg'
            titel = a.get('title') or ''
            k = (udvalg, dato, re.sub(r'\s+', ' ', titel).strip())
            if k in set_punkter:
                continue
            set_punkter.add(k)
            f = match_punkt(kommune, udvalg, dato, titel, '', KK + quote(alias),
                            '', str(a.get('agenda_element_serial_no') or ''), 'kk.dk')
            if f:
                fund.append(f)
        url = ((d.get('links') or {}).get('next') or {}).get('href')
        time.sleep(PAUSE)
    print(f'  {kommune}: {len(set_punkter)} punkter på {sider} sider', flush=True)
    if not set_punkter:
        print(f'  ! {kommune}: 0 punkter i vinduet - tjek om API\'et har ændret sig', flush=True)
    return fund


# ── Aalborg: egen app på apps.aalborgkommune.dk ─────────────────────────────
# Mødelister pr. udvalgs-id; linkene peger på localhost:5287, så kun query-strengen bruges.
# Kun referater offentliggøres her, så punkter dukker op efter mødet.
# Udvalgs-id'erne skifter ved konstitueringer og kan ikke listes - 0 møder = alarm.
AAL = 'https://apps.aalborgkommune.dk/dagsordenreferat/'


def scan_aalborg(kommune, cfg, fra, til):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (DNNK dagsordensovervaagning)'
    fund, moeder_i_alt = [], 0
    for uid in cfg.get('udvalg_ids', []):
        html_liste = s.get(AAL, params={'Id': uid}, timeout=30).text
        links = re.findall(r'class="moede-link[^"]*"[^>]*href="[^"?]*\?([^"]+)"[^>]*title="([^"]*)"', html_liste)
        moeder_i_alt += len(links)
        if not links:
            print(f'  ! {kommune}: udvalg {uid} har 0 møder - id skiftet ved konstituering?', flush=True)
        for query, titel_attr in links:
            query = html.unescape(query)
            m = re.search(r'moedetitel=(\d{4}-\d{2}-\d{2})', unquote(query))
            if not m:
                continue
            dato = dt.date.fromisoformat(m.group(1))
            if not (fra <= dato <= til):
                continue
            time.sleep(PAUSE)
            side = s.get(AAL + 'visreferat?' + query, timeout=60).text
            udvalg = re.sub(r'^(Referat|Dagsorden) (for|fra) ', '', html.unescape(titel_attr))
            udvalg = re.sub(r'\s+\d{1,2}\. \w+ \d{4}.*$', '', udvalg)
            # Punkter: <h3>N. Titel</h3>; teksten frem til næste <h3> bruges som resumé (Indstilling m.m.)
            dele = re.split(r'<h3[^>]*>', side)[1:]
            for nr, del_ in enumerate(dele, 1):
                titel = tekst(del_.split('</h3>', 1)[0])
                if not re.match(r'^\d+\.', titel):
                    continue
                krop = re.sub(r'<(script|style|svg)[^>]*>.*?</\1>', ' ', del_.split('</h3>', 1)[-1], flags=re.S)
                f = match_punkt(kommune, udvalg, dato, titel, tekst(krop)[:600],
                                AAL + 'visreferat?' + query, '', titel.split('.', 1)[0], 'apps.aalborgkommune.dk')
                if f:
                    fund.append(f)
    print(f'  {kommune}: {moeder_i_alt} møder i listerne', flush=True)
    return fund


ADAPTERE = {'kk_jsonapi': scan_kk, 'aalborg': scan_aalborg}


def scan(kommune, cfg, fra, til):
    """En streng er en FirstAgenda-vært; et objekt har en 'type', der vælger adapteren."""
    if isinstance(cfg, str):
        return scan_kommune(kommune, cfg, fra, til)
    return ADAPTERE[cfg['type']](kommune, cfg, fra, til)


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
            f = scan(k, h, fra, til)
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
