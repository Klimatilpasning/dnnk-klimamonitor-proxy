from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from bs4 import BeautifulSoup
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import asyncio
import hmac
import re
import os
import time
import collections


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ÉN delt httpx-client for hele app'en i stedet for en ny client pr.
    # request (og pr. feed i /test-feeds) — sparer connection-setup og holder
    # antallet af samtidige forbindelser nede på Render free tier.
    app.state.client = httpx.AsyncClient(
        limits=httpx.Limits(max_connections=20),
        timeout=httpx.Timeout(30),
        follow_redirects=True,
    )
    # Intern scheduler er som standard slået FRA (digest-mails stoppet på
    # brugerens anmodning). Sæt SCHEDULER_ENABLED=true på Render for at
    # aktivere igen.
    if os.environ.get("SCHEDULER_ENABLED", "").lower() in ("1", "true", "yes"):
        asyncio.create_task(_scheduler_loop())
    else:
        print("Scheduler deaktiveret (SCHEDULER_ENABLED ikke sat) – sender ingen digest-mails.")
    # MCP-serverens session-manager skal køre så længe appen lever — uden
    # den afviser streamable-HTTP-transporten alle kald til /mcp.
    # (mcp_server/mcp-app'en er oprettet på modulniveau nederst i filen.)
    async with mcp_server.session_manager.run():
        yield
    await app.state.client.aclose()


app = FastAPI(title="DNNK Klimamonitor Proxy", lifespan=lifespan)

# CORS låst til DNNK's GitHub Pages-domæne (begge frontends ligger her).
# Sæt evt. ekstra domæner via miljøvariablen DNNK_ALLOWED_ORIGINS (komma-sep).
ALLOWED_ORIGINS = ["https://klimatilpasning.github.io"]
_extra = os.environ.get("DNNK_ALLOWED_ORIGINS", "")
if _extra:
    ALLOWED_ORIGINS += [o.strip() for o in _extra.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Model-id ét sted (bruges i /expand-query og scheduler.py) — kan
# skiftes uden deploy via miljøvariablen HAIKU_MODEL.
HAIKU_MODEL = os.environ.get("HAIKU_MODEL", "claude-haiku-4-5")
# Chatten (vidensassistenten) kører på en større model: præcision og
# kildetro svar vejer tungere end pris her. Kan skiftes via CHAT_MODEL.
CHAT_MODEL = os.environ.get("CHAT_MODEL", "claude-sonnet-5")

# ── Misbrugsbeskyttelse på de endpoints der bruger serverens API-nøgle ──
_RATE = collections.defaultdict(list)
RATE_LIMIT = int(os.environ.get("DNNK_RATE_LIMIT", "20"))   # kald pr. vindue pr. IP
RATE_WINDOW = 60                                            # sekunder

def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    if fwd:
        # SIDSTE element: Render appender den ægte klient-IP sidst i XFF —
        # det første element kan klienten selv sætte og dermed spoofe sig
        # uden om rate-limiteren.
        return fwd.split(",")[-1].strip()
    return request.client.host if request.client else "ukendt"

def is_rate_limited(request: Request) -> bool:
    ip = _client_ip(request)
    now = time.time()
    # Ryd IP-nøgler hvor alle timestamps er forældede, så _RATE ikke vokser
    # ubegrænset med gamle klient-IP'er.
    stale = [k for k, v in _RATE.items() if not v or now - v[-1] >= RATE_WINDOW]
    for k in stale:
        del _RATE[k]
    hits = [t for t in _RATE[ip] if now - t < RATE_WINDOW]
    hits.append(now)
    _RATE[ip] = hits
    return len(hits) > RATE_LIMIT

def access_ok(request: Request) -> bool:
    """Delt adgangskode. Hvis DNNK_ACCESS_CODE ikke er sat, er checket slået fra.
    Bemærk: koden sendes fra frontenden og kan ses i klient-JS — det er et
    værn mod tilfældigt/automatiseret misbrug, ikke mod en målrettet bruger."""
    code = os.environ.get("DNNK_ACCESS_CODE", "")
    if not code:
        return True
    return hmac.compare_digest(request.headers.get("x-dnnk-code", ""), code)

def trigger_ok(request: Request) -> bool:
    """Beskytter de trigger-endpoints der koster API/e-mail. Token kan gives
    som ?token=... eller X-DNNK-Code-header. Slået fra hvis DNNK_ACCESS_CODE
    ikke er sat."""
    code = os.environ.get("DNNK_ACCESS_CODE", "")
    if not code:
        return True
    token = request.query_params.get("token", "") or request.headers.get("x-dnnk-code", "")
    return hmac.compare_digest(token, code)

KEYWORDS = [
    # ── Klimatilpasning – kerneord ──
    "klimatilpasning", "skybrud", "oversvømmelse", "regnvand", "LAR",
    "spildevand", "kloak", "kloakseparering", "vandforsyning", "vandværk",
    "kystbeskyttelse", "stormflod", "havvandsstigning", "klimasikring",
    "regnvandsbassin", "grøn infrastruktur", "permeable belægning",
    "faskine", "regnbed", "klimahandlingsplan", "DK2020",
    "separatkloakering", "renseanlæg", "pumpestation", "vandmiljø",
    "klimarisiko", "klimasårbarhed", "klimatilpasningsplan", "serviceniveau",
    "oversvømmelsesdirektiv", "klimatilpasningsloven",

    # ── Vandkredsløbet – grundvand & vandløb ──
    "grundvand", "grundvandsstand", "grundvandsforurening", "grundvandssænkning",
    "BNBO", "indvindingstilladelse", "vandindvinding", "vandbalance",
    "vandkredsløb", "fordampning", "nedbør", "afstrømning",
    "vandløb", "vandløbsrestaurering", "åbning af rørlagt vandløb",
    "meandering", "vandløbsvedligeholdelse", "okker", "vandkvalitet",
    "sørestaurering", "vådområde", "lavbundsareal", "højmose",
    "drænvand", "dræning", "landbrugsdræn", "nitrat", "fosfor",

    # ── Kreative & innovative vinkler ──
    "svampeby", "sponge city", "naturbaseret løsning", "nature-based solutions",
    "blå-grøn infrastruktur", "living shoreline", "biomimicry",
    "vandgenbrug", "regnvandsopsamling", "genanvendelse af vand",
    "klimakvarter", "vandplus", "skybrudsplan", "skybrudsvej",
    "klimatilpasset byggeri", "grønt tag", "grøn facade",
    "urban heat island", "varmeø", "afkøling", "skygge og vand",
    "robusthed", "resiliens", "adaptive design", "fremtidssikring",

    # ── Nordiske & internationale termer ──
    "klimatanpassning", "översvämning", "dagvatten", "overvannshåndtering",
    "kustplanering", "havsnivå", "kustskydd", "kusterosion",
    "kustzon", "havsplanering", "flexibel markanvändning", "stegvis planering",
    "robusta städer", "urbana landskap", "Movium", "SGI",
    "Interreg", "LIFE programme", "Horizon Europe", "Climate-ADAPT",
    "flood risk", "coastal adaptation", "water resilience",
    "DHI", "SCALGO", "Stormrådet", "Realdania", "Deltares",
    "C40", "ICLEI", "waterboards", "Rijkswaterstaat",

    # ── Brede nøgleord ──
    # Bevidst smal: "natur" og "water" fjernet pga. falsk-positiv-match
    # mod engelske ord ("natural", "watercolor") ved ordstarts-matching.
    # Specifikke termer som "naturbaseret løsning" og "water resilience"
    # dækker stadig de relevante koncepter.
    "klima", "vand", "miljø", "bæredygtig",
    "climate", "flood", "urban", "infrastructure",
]

RSS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "da,en;q=0.9",
}

def normalize_date(raw: str) -> str:
    """Normalisér en RSS/Atom-dato til YYYY-MM-DD.

    Håndterer ISO (2026-06-17, 2026-06-17T10:00:00Z) OG RFC822
    (Tue, 17 Jun 2026 10:00:00 GMT). Returnerer "" hvis dato ikke kan tolkes.
    Vigtigt: tidligere blev råteksten bare afkortet til 10 tegn, hvilket
    ødelagde RFC822-datoer (→ "Tue, 17 J") og slog både dato-sortering og
    is_recent-filteret i digesten ud."""
    if not raw:
        return ""
    raw = raw.strip()
    m = re.match(r'(\d{4}-\d{2}-\d{2})', raw)
    if m:
        return m.group(1)
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(raw)
        if dt:
            return dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    m2 = re.search(r'(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})', raw)
    if m2:
        day, month, year = int(m2.group(1)), int(m2.group(2)), m2.group(3)
        # Validér måneden: "06/17/2026" er MM/DD/YYYY — hvis "måneden" er
        # ugyldig (>12) men et bytte giver en gyldig dato, så byt.
        if not 1 <= month <= 12 and 1 <= day <= 12:
            day, month = month, day
        if 1 <= month <= 12 and 1 <= day <= 31:
            return f"{year}-{month:02d}-{day:02d}"
    return ""

def real_url(url: str) -> str:
    """Udtræk den rigtige artikel-URL fra Bing News' apiclick-omdirigering.
    Bing-links ser ud som bing.com/news/apiclick.aspx?...&url=<encoded>&... —
    vi peger direkte på kilden, så links er rene OG dubletter (samme artikel
    fanget af både et RSS-feed og et Bing-søgefeed) kan slås sammen."""
    if not url:
        return url
    if "bing.com/news/apiclick" in url:
        try:
            from urllib.parse import urlparse, parse_qs, unquote
            q = parse_qs(urlparse(url).query)
            if q.get("url"):
                return unquote(q["url"][0])
        except Exception:
            pass
    return url

def kw_match(keyword: str, text: str) -> bool:
    """Match keyword at the start of a word. Prevents 'LAR' from matching
    'klart' or 'hav' from matching 'havde', while still allowing Scandinavian
    compound matches like 'klima' in 'klimaforandring'."""
    if not keyword:
        return False
    pattern = r'(?<!\w)' + re.escape(keyword)
    # Akronymer (kun versaler/tal, fx LAR, BNBO, DHI, DK2020) skal matche som
    # helt ord — ellers rammer "LAR" navnet "Lars" og "DHI" rammer "DHILiving".
    # Almindelige ord beholder kun start-grænsen, så "klima" stadig matcher
    # sammensætninger som "klimaforandring".
    if keyword.upper() == keyword and any(c.isalpha() for c in keyword):
        pattern += r'(?!\w)'
    return bool(re.search(pattern, text, re.IGNORECASE | re.UNICODE))

# Brede nøgleord vejer let — ét enkelt match (fx kun "klima" eller "miljø")
# er IKKE nok til at en artikel regnes som relevant. Det er disse ord der
# ellers lukker ministerrokade, elpriser og "klimaaftryk"-historier ind.
# Alle øvrige KEYWORDS er kerneord og vejer tungt.
BROAD_KEYWORDS = {
    "klima", "vand", "miljø", "bæredygtig",
    "climate", "urban", "infrastructure",
}

# ── Kompilerede nøgleords-regexes (bygget én gang ved modul-load) ──
# Tidligere kørte score_article ~124 separate regex-søgninger pr. artikel
# (op til 2.800 artikler pr. request) og blokerede event-loopen. Nu samles
# alle nøgleord i to alternations-regexes (kerneord/brede ord), og hits
# tælles i ét gennemløb med findall. Akronym-logikken fra kw_match bevares:
# ord der er helt uppercase (LAR, BNBO, DHI, DK2020) kræver word-boundary
# EFTER ordet, almindelige ord matcher stadig sammensætninger (klima →
# klimaforandring). Længste ord først, så alternationen foretrækker det
# mest specifikke match.
def _kw_pattern(kw: str) -> str:
    p = re.escape(kw)
    if kw.upper() == kw and any(c.isalpha() for c in kw):
        p += r'(?!\w)'
    return p

_CORE_KEYWORDS = [kw for kw in KEYWORDS if kw not in BROAD_KEYWORDS]
CORE_RE = re.compile(
    r'(?<!\w)(?:' + '|'.join(_kw_pattern(k) for k in sorted(_CORE_KEYWORDS, key=len, reverse=True)) + r')',
    re.IGNORECASE | re.UNICODE)
BROAD_RE = re.compile(
    r'(?<!\w)(?:' + '|'.join(_kw_pattern(k) for k in sorted(BROAD_KEYWORDS, key=len, reverse=True)) + r')',
    re.IGNORECASE | re.UNICODE)

def find_tags(combined: str, top_n: int = 3) -> list:
    """Tags = de kerneord der FAKTISK matcher artiklen (top 3, i tekst-orden).
    Tidligere kunne kun de første 6 nøgleord i KEYWORDS blive tags."""
    tags = []
    for m in CORE_RE.findall(combined):
        t = m.lower()
        if t not in tags:
            tags.append(t)
        if len(tags) >= top_n:
            break
    return tags

def score_article(combined: str, q_match: bool):
    """Returnér (relevance 0-1, keep).

    Kerneord vejer 3, brede ord 1, et søge-match giver 3. En artikel beholdes
    kun hvis den rammer mindst ét kerneord, matcher søgningen, eller rammer
    mindst to brede ord — så artikler der blot strejfer 'klima'/'miljø' (fx
    ministerrokade eller elpriser) sorteres fra i stedet for at score 1.
    Der tælles DISTINKTE matchende nøgleord (som før), ikke antal forekomster."""
    core_hits = len({m.lower() for m in CORE_RE.findall(combined)})
    broad_hits = len({m.lower() for m in BROAD_RE.findall(combined)})
    keep = core_hits >= 1 or q_match or broad_hits >= 2
    raw = core_hits * 3 + broad_hits + (3 if q_match else 0)
    return min(round(raw / 12, 2), 1.0), keep

def parse_item_bs(item):
    """Parse et RSS/Atom item med BeautifulSoup"""
    title = item.find("title")
    title = title.get_text(strip=True) if title else ""
    
    desc = item.find("description") or item.find("summary") or item.find("content")
    description = re.sub(r"<[^>]+>", "", desc.get_text(strip=True))[:400] if desc else ""
    
    link = item.find("link")
    if link:
        url = link.get("href") or link.get_text(strip=True)
    else:
        url = ""
    
    # Case-insensitivt: BeautifulSoups xml-parser bevarer versalisering, så
    # Bing News' <pubDate> ikke matches af et rent lille-bogstavs-opslag.
    d = item.find(re.compile(r'(?i)^(pubdate|published|updated|date)$'))
    pub_date = normalize_date(d.get_text(strip=True)) if d else ""

    return title, description, url, pub_date

# ── TTL-cache af rå feed-/sidetekst pr. URL (K2 — største gevinst) ──
# Frontendens auto-scan kalder /news/full 5× med forskellig q, men q påvirker
# kun scoringen — de samme ~70 feeds blev hentet 5 gange. Med cachen hentes
# hvert feed højst én gang pr. 10 minutter. Cachen er naturligt bounded af
# antallet af kilde-URL'er (feeds + scrape-mål), så den kan ikke vokse frit.
_FEED_CACHE: dict[str, tuple[float, str]] = {}
FEED_TTL = 600          # sekunder
MAX_FEED_BYTES = 2 * 1024 * 1024   # afvis svar > 2MB (512MB RAM på free tier)

# Begræns samtidige eksterne fetches ved cache-miss (scrape rammer ~100 mål)
_FETCH_SEM = asyncio.Semaphore(15)

async def get_feed_text(client, url: str, headers=None) -> str:
    """Hent rå tekst for en URL med 10 min TTL-cache og 2MB byte-cap.
    Bemærk: der filtreres ikke på statuskode her — flere danske CMS/SPA-sider
    svarer 404 men leverer alligevel indholdet i body (se scrape_news).
    Fejlsider giver naturligt 0 items/artikler i parsing-laget."""
    now = time.time()
    cached = _FEED_CACHE.get(url)
    if cached and now - cached[0] < FEED_TTL:
        return cached[1]
    async with _FETCH_SEM:
        resp = await client.get(url, timeout=15, follow_redirects=True,
                                headers=headers or RSS_HEADERS)
    if len(resp.content) > MAX_FEED_BYTES:
        raise ValueError(f"svar for stort ({len(resp.content)} bytes)")
    text = resp.text
    _FEED_CACHE[url] = (now, text)
    return text

# ── DNNK webinar-indeks (search-index.json) med 12t TTL-cache ──
# Indekset ligger offentligt i vidensassistent-repoet og ændrer sig sjældent,
# så 12 timer er rigeligt friskt. Ved indlæsning forberedes pr. webinar to
# ord-sæt (tokens fra titel+keywords hhv. alt tekst), så al efterfølgende
# matching er billige set-snit — ingen regex pr. webinar pr. artikel.
WEBINAR_INDEX_URL = "https://raw.githubusercontent.com/Klimatilpasning/dnnk-vidensassistent/main/search-index.json"
WEBINAR_INDEX_TTL = 12 * 3600
_WEBINAR_INDEX_CACHE: tuple[float, list] | None = None   # (timestamp, forberedt liste)

_TOKEN_RE = re.compile(r"[a-z0-9æøåäöéü]+")

def _tokens(text: str, min_len: int = 4) -> set:
    """Tokenisér tekst: lowercase, kun bogstaver/tal, ord ≥ min_len tegn."""
    return {t for t in _TOKEN_RE.findall((text or "").lower()) if len(t) >= min_len}

async def get_webinar_index() -> list:
    """Hent og forbered DNNK's webinar-indeks (cached 12 timer).
    Returnerer liste af {"entry": rå indeks-entry, "words": titel+keyword-tokens,
    "words_full": tokens fra titel+keywords+summary+speakers+kategori}.
    Ved netværksfejl serveres et evt. forældet indeks frem for ingenting."""
    global _WEBINAR_INDEX_CACHE
    now = time.time()
    if _WEBINAR_INDEX_CACHE and now - _WEBINAR_INDEX_CACHE[0] < WEBINAR_INDEX_TTL:
        return _WEBINAR_INDEX_CACHE[1]
    try:
        resp = await app.state.client.get(WEBINAR_INDEX_URL, timeout=20)
        resp.raise_for_status()
        raw = resp.json()
    except Exception as e:
        print(f"[webinar-indeks] kunne ikke hentes: {e}")
        return _WEBINAR_INDEX_CACHE[1] if _WEBINAR_INDEX_CACHE else []
    prepared = []
    for entry in raw if isinstance(raw, list) else []:
        words = _tokens(entry.get("title", ""))
        for kw in entry.get("keywords") or []:
            words |= _tokens(kw)
        words_full = set(words)
        words_full |= _tokens(entry.get("summary", ""))
        words_full |= _tokens(entry.get("category", ""))
        for sp in entry.get("speakers") or []:
            if isinstance(sp, dict):
                words_full |= _tokens(sp.get("name", "")) | _tokens(sp.get("org", ""))
        if words:
            prepared.append({"entry": entry, "words": words, "words_full": words_full})
    _WEBINAR_INDEX_CACHE = (now, prepared)
    print(f"[webinar-indeks] {len(prepared)} webinarer indlæst")
    return prepared

def find_relaterede_webinarer(text: str, max_n: int = 2) -> list:
    """Find op til max_n DNNK-webinarer der matcher en artikel-tekst.
    Matcher artikel-tokens (ord ≥4 tegn) mod webinarets titel+keyword-ord og
    kræver mindst 2 fælles ord, så et enkelt bredt ord ('klimatilpasning')
    ikke klistrer webinarer på alt. Læser den allerede hentede cache — kald
    get_webinar_index() først i async-kontekst. Returnerer
    [{"title", "youtube_url", "date"}] sorteret efter flest fælles ord."""
    prepared = _WEBINAR_INDEX_CACHE[1] if _WEBINAR_INDEX_CACHE else []
    art_words = _tokens(text)
    if not prepared or not art_words:
        return []
    scored = []
    for item in prepared:
        entry = item["entry"]
        if not entry.get("youtube_url"):
            continue
        hits = len(art_words & item["words"])
        if hits >= 2:
            scored.append((hits, entry))
    scored.sort(key=lambda x: -x[0])
    return [{"title": e.get("title", ""),
             "youtube_url": e.get("youtube_url", ""),
             "date": e.get("date", "")}
            for _, e in scored[:max_n]]

def parse_feed_items(content: str) -> list:
    """Find alle item/entry-elementer i et RSS/Atom-feed.
    ElementTree-vejen er droppet: den fejlede på namespace-prefixede tags
    (content:encoded m.fl.), så alt blev alligevel dobbelt-parset med
    BeautifulSoup. lxml's xml-parser håndterer namespaces korrekt."""
    try:
        soup = BeautifulSoup(content, "xml")
        items = soup.find_all("item") + soup.find_all("entry")
        if items:
            return items
    except Exception:
        pass
    try:
        soup = BeautifulSoup(content, "lxml")
        return soup.find_all("item") + soup.find_all("entry")
    except Exception:
        return []

async def fetch_rss(client, source, url, query, limit: int = 8):
    """Returnerer en liste af artikler, eller None hvis feedet fejlede
    (så /news/full kan tælle feeds_failed)."""
    try:
        content = await get_feed_text(client, url)
        items = parse_feed_items(content)
        if not items:
            return []

        results = []
        q_lower = query.lower()

        for item in items[:40]:
            title, description, link, pub_date = parse_item_bs(item)
            if not title:
                continue
            combined = title + " " + description
            q_match = any(kw_match(w, combined) for w in q_lower.split() if len(w) > 3)
            relevance, keep = score_article(combined, q_match)
            # Drop artikler der kun strejfer brede ord — ren støj fra brede feeds
            if not keep:
                continue
            results.append({
                "source": "news", "feedSource": source, "title": title,
                "org": source, "date": pub_date, "summary": description,
                "tags": find_tags(combined),
                "relevance": relevance, "url": real_url(link), "value": None
            })
        results.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)
        return results[:limit]
    except Exception as e:
        print(f"[feed-fejl] {url}: {e}")
        return None

@app.get("/test-feeds")
async def test_feeds(request: Request):
    """Test alle RSS feeds og returner status for hver"""
    if is_rate_limited(request):
        return JSONResponse(status_code=429, content={"error": "For mange forespørgsler — prøv igen om lidt"})
    from sources import ALL_FEEDS_FLAT

    async def check_feed(navn, meta):
        url = meta["url"]
        gruppe = meta["gruppe"]
        try:
            # Delt client + samme cache/parse-logik som /news/full — tidligere
            # oprettede endpointet én ny httpx-client PR. FEED og havde sin
            # egen kopi af parse-koden.
            content = await get_feed_text(app.state.client, url)
            items = parse_feed_items(content)
            if items:
                return {"navn": navn, "gruppe": gruppe, "url": url,
                        "status": "ok", "info": f"{len(items)} items"}
            return {"navn": navn, "gruppe": gruppe, "url": url,
                    "status": "fejl", "info": "Ingen items fundet"}
        except Exception as e:
            return {"navn": navn, "gruppe": gruppe, "url": url,
                    "status": "fejl", "info": str(e)[:80]}

    tasks = [check_feed(n, m) for n, m in ALL_FEEDS_FLAT.items()]
    results = await asyncio.gather(*tasks)
    ok = [r for r in results if r["status"] == "ok"]
    fejl = [r for r in results if r["status"] != "ok"]
    return {
        "total": len(results), "ok": len(ok), "fejl": len(fejl),
        "virker": sorted(ok, key=lambda x: x["gruppe"]),
        "virker_ikke": sorted(fejl, key=lambda x: x["gruppe"]),
        "testet": datetime.now(timezone.utc).isoformat()
    }

@app.get("/ted")
async def search_ted(q: str = Query("klimatilpasning"), size: int = 10):
    url = "https://api.ted.europa.eu/v3/notices/search"
    params = {"q": f"{q} Denmark", "pageSize": size,
              "fields": "title,organisations,publicationDate,contractValue,cpvCodes,noticeType,tedPublicationUrl",
              "country": "DNK"}
    try:
        resp = await app.state.client.get(url, params=params, timeout=15)
        return resp.json()
    except Exception as e:
        # Frontenden forventer altid en notices-liste — fejl må ikke give 500
        return {"notices": [], "error": str(e)[:200]}

@app.get("/news/full")
async def get_news_full(request: Request, q: str = Query("klimatilpasning"), gruppe: str = Query(None), limit: int = Query(8)):
    if is_rate_limited(request):
        return JSONResponse(status_code=429, content={"error": "For mange forespørgsler — prøv igen om lidt"})
    from sources import ALL_FEEDS_FLAT, ALLE_FEEDS
    feeds = ALL_FEEDS_FLAT
    if gruppe and gruppe in ALLE_FEEDS:
        feeds = {k: {"url": v, "gruppe": gruppe} for k, v in ALLE_FEEDS[gruppe].items()}
    tasks = [fetch_rss(app.state.client, navn, meta["url"], q, limit) for navn, meta in feeds.items()]
    nested = await asyncio.gather(*tasks)
    feeds_failed = sum(1 for sub in nested if sub is None)
    articles = []
    for i, (navn, meta) in enumerate(feeds.items()):
        for art in (nested[i] or [])[:limit]:
            art["gruppe"] = meta["gruppe"]
            articles.append(art)

    # Slå dubletter sammen: samme artikel fanges ofte af både et direkte RSS-feed
    # OG et Bing-søgefeed (Bing-links er nu normaliseret til kilde-URL'en, så de
    # matcher). Behold den bedste pr. URL: foretræk det direkte feed frem for
    # Bing, derefter højere relevans, derefter den med en dato.
    def _pref(a):
        return (1 if str(a.get("feedSource", "")).startswith("Bing News") else 0,
                -(a.get("relevance") or 0),
                0 if a.get("date") else 1)
    bedste = {}
    for a in articles:
        key = a.get("url") or (a.get("title", "") + "|" + a.get("feedSource", ""))
        if key not in bedste or _pref(a) < _pref(bedste[key]):
            bedste[key] = a
    articles = list(bedste.values())

    # Berig hver artikel med relaterede DNNK-webinarer, så nyhedslæseren kan
    # se hvad DNNK allerede har dækket om emnet. Indekset er 12t-cached, og
    # matchingen er rene set-snit — koster nærmest intet pr. artikel.
    await get_webinar_index()
    for a in articles:
        a["webinarer"] = find_relaterede_webinarer(
            (a.get("title") or "") + " " + (a.get("summary") or ""))

    articles.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)
    return {"articles": articles, "total": len(articles),
            "feeds_checked": len(feeds), "feeds_failed": feeds_failed,
            "query": q,
            "scanned_at": datetime.now(timezone.utc).isoformat()}

@app.get("/news/kilder")
async def get_kilder():
    from sources import ALLE_FEEDS
    return {gruppe: list(feeds.keys()) for gruppe, feeds in ALLE_FEEDS.items()}

@app.get("/send-digest")
async def trigger_digest(request: Request):
    if not trigger_ok(request):
        return JSONResponse(status_code=401, content={"error": "Adgang nægtet"})
    asyncio.create_task(_run_digest())
    return {"status": "Digest scanning startet – e-mail sendes om ca. 60 sek"}

@app.get("/send-weekly-analysis")
async def trigger_weekly(request: Request):
    if not trigger_ok(request):
        return JSONResponse(status_code=401, content={"error": "Adgang nægtet"})
    asyncio.create_task(_run_weekly())
    return {"status": "Ugentlig indholdsanalyse startet – e-mail sendes om ca. 60 sek"}

async def _run_weekly():
    try:
        from scheduler import run_weekly_analysis
        await run_weekly_analysis()
    except Exception as e:
        print(f"Ugentlig analyse fejl: {e}")

async def _run_digest():
    try:
        from scheduler import run_daily_digest
        await run_daily_digest()
    except Exception as e:
        print(f"Digest fejl: {e}")

async def _scheduler_loop():
    try:
        from scheduler import scheduler_loop
        await scheduler_loop()
    except Exception as e:
        print(f"Scheduler fejl: {e}")


@app.post("/chat")
async def chat(payload: dict, request: Request):
    """Proxy til Anthropic API. Bruger serverens egen ANTHROPIC_API_KEY
    (sat som miljøvariabel på Render) — klienten skal IKKE sende en nøgle."""
    if not access_ok(request):
        return JSONResponse(status_code=401, content={"error": "Adgang nægtet"})
    if is_rate_limited(request):
        return JSONResponse(status_code=429, content={"error": "For mange forespørgsler — prøv igen om lidt"})

    messages = payload.get("messages", [])
    system = payload.get("system", "")
    max_tokens = int(payload.get("max_tokens", 1024))

    if not isinstance(messages, list) or not messages:
        return {"error": "Ingen beskeder"}
    # Afvis absurd store payloads før de sendes videre (og koster tokens)
    if len(str(messages)) > 100_000:
        return JSONResponse(status_code=413, content={"error": "Payload for stor"})

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"error": "Ingen server-API-nøgle konfigureret"}

    try:
        resp = await app.state.client.post(
            "https://api.anthropic.com/v1/messages",
            timeout=90,  # stor model + lang RAG-kontekst; frontenden venter op til 90s
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json={
                "model": CHAT_MODEL,
                "max_tokens": min(max(max_tokens, 1), 4096),
                "system": system,
                "messages": messages
            }
        )
        # Videregiv Anthropics egen statuskode, så klienten kan skelne
        # fx 429/529 fra et succesfuldt svar i stedet for altid at få 200.
        return JSONResponse(status_code=resp.status_code, content=resp.json())
    except Exception as e:
        return {"error": str(e)[:200]}


# In-memory cache for query expansions (resets on restart).
# Cappet til 500 entries (FIFO) så den ikke kan vokse ubegrænset på 512MB RAM.
_expand_cache = {}
_EXPAND_CACHE_MAX = 500

@app.get("/expand-query")
async def expand_query(request: Request, q: str = Query(..., min_length=2)):
    """Udvider en søgeforespørgsel med relaterede danske fagudtryk via Claude Haiku."""
    import json as _json
    q_key = q.strip().lower()
    if q_key in _expand_cache:
        return {"query": q, "terms": _expand_cache[q_key], "cached": True}

    if is_rate_limited(request):
        return JSONResponse(status_code=429, content={"query": q, "terms": [], "error": "For mange forespørgsler"})

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"query": q, "terms": [], "error": "Ingen server-API-nøgle konfigureret"}

    try:
        resp = await app.state.client.post(
            "https://api.anthropic.com/v1/messages",
            timeout=15,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": HAIKU_MODEL,
                "max_tokens": 200,
                "messages": [{
                    "role": "user",
                    "content": (
                        f'Brugeren søger på "{q}" i en vidensbank om klimatilpasning og vandkredsløb. '
                        f"Giv 8-12 relaterede danske fagudtryk og synonymer der ville matche relevante webinarer. "
                        f"Inkluder både brede og specifikke termer. Svar KUN med valid JSON-liste, fx: "
                        f'["term1","term2","term3"]'
                    )
                }]
            }
        )
        data = resp.json()
        if "content" not in data:
            return {"query": q, "terms": [], "error": "Ugyldigt svar fra Claude"}
        raw = data["content"][0]["text"].strip()
        # Strip code fences
        import re as _re
        raw = _re.sub(r"^```(?:json)?\s*", "", raw)
        raw = _re.sub(r"\s*```$", "", raw)
        terms = _json.loads(raw)
        if isinstance(terms, list):
            terms = [str(t) for t in terms if t][:15]
            if len(_expand_cache) >= _EXPAND_CACHE_MAX:
                _expand_cache.pop(next(iter(_expand_cache)))  # FIFO
            _expand_cache[q_key] = terms
            return {"query": q, "terms": terms}
    except Exception as e:
        return {"query": q, "terms": [], "error": str(e)[:200]}

    return {"query": q, "terms": []}

@app.get("/")
def root():
    return {"status": "ok", "service": "DNNK Klimamonitor Proxy",
            "endpoints": ["/ted", "/news/full", "/news/scrape", "/news/kilder", "/test-feeds", "/mcp"]}


# ─────────────────────────────────────────────────────────────
# SCRAPING — til sider uden RSS
# ─────────────────────────────────────────────────────────────

# SCRAPE_SOURCES importeres fra sources.py
from sources import SCRAPE_SOURCES

async def scrape_news(client, source, url, gruppe, query, limit: int = 8):
    """Scraper nyhedsartikler direkte fra hjemmeside HTML"""
    from urllib.parse import urlparse, urljoin
    try:
        # Bemærk: flere danske CMS/SPA-sider (DMI, IDA, Klimarådet, SLA, HOFOR)
        # svarer HTTP 404 på serverniveau, men leverer alligevel hele nyhedslisten
        # i body. Vi afviser derfor IKKE på statuskode alene — vi forsøger at parse
        # så længe der er substantielt indhold. Selektorerne + relevans-filteret
        # giver naturligt 0 resultater for ægte (tomme) fejlsider.
        # Hentes via TTL-cachen (10 min) med semafor + 2MB byte-cap.
        text = await get_feed_text(client, url)
        if not text or len(text) < 2000:
            return []

        soup = BeautifulSoup(text, "lxml")
        base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

        for tag in soup(["nav", "footer", "script", "style", "header"]):
            tag.decompose()

        q_lower = query.lower()

        # Find kandidater — prøv progressivt mere generelle selektorer
        candidates = (
            soup.find_all("article") or
            soup.find_all(class_=re.compile(r"news[-_]?item|nyhed|artikel|post[-_]?item|teaser|card[-_]?item", re.I)) or
            soup.find_all("li", class_=re.compile(r"news|nyhed|post|item|article", re.I)) or
            soup.find_all(class_=re.compile(r"news|nyheder|articles|posts", re.I)) or
            []
        )

        # Fallback: alle h2/h3 med links
        if not candidates:
            candidates = [a.parent for a in soup.find_all("a", href=True)
                         if a.find_parent(["h2","h3"]) or a.find(["h2","h3"])][:20]

        seen_titles = set()
        articles = []

        for el in candidates[:25]:
            # Find titel
            title_el = el.find(["h1","h2","h3","h4"])
            if not title_el:
                if el.name in ["h2","h3","h4"]:
                    title_el = el
                else:
                    continue

            title = title_el.get_text(strip=True)
            if not title or len(title) < 8 or title in seen_titles:
                continue
            seen_titles.add(title)

            # Find link — søg i titel først, derefter hele elementet
            link_el = title_el.find("a") or el.find("a", href=True)
            article_url = ""
            if link_el and link_el.get("href"):
                href = link_el["href"]
                article_url = urljoin(base_url, href)

            # Find dato — søg i <time>, datetime-attribut, eller dato-klasser.
            # Altid via normalize_date: ren [:10]-afkortning genindførte
            # dato-truncation-buggen for ikke-ISO-datoer ("Tue, 17 J").
            pub_date = ""
            time_el = el.find("time")
            if time_el:
                pub_date = normalize_date(time_el.get("datetime") or time_el.get_text(strip=True))
            if not pub_date:
                date_el = el.find(class_=re.compile(r"date|dato|time|published|created", re.I))
                if date_el:
                    raw = date_el.get("datetime") or date_el.get("content") or date_el.get_text(strip=True)
                    pub_date = normalize_date(raw or "")

            # Find beskrivelse
            desc_el = el.find("p")
            description = desc_el.get_text(strip=True)[:300] if desc_el else ""

            combined = title + " " + description
            q_match = any(kw_match(w, combined) for w in q_lower.split() if len(w) > 3)
            relevance, keep = score_article(combined, q_match)
            # Drop artikler der kun strejfer brede ord — samme tærskel som RSS
            if not keep:
                continue

            articles.append({
                "source": "scrape",
                "feedSource": source,
                "title": title,
                "org": source,
                "date": pub_date,
                "summary": description,
                "tags": find_tags(combined),
                "relevance": relevance,
                "url": article_url,
                "value": None,
                "gruppe": gruppe,
            })

        articles.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)
        return articles[:limit]

    except Exception as e:
        print(f"[feed-fejl] {url}: {e}")
        return []


@app.get("/news/scrape")
async def get_scraped_news(request: Request, q: str = Query("klimatilpasning"), limit: int = Query(8)):
    """Hent nyheder via direkte scraping fra sider uden RSS"""
    if is_rate_limited(request):
        return JSONResponse(status_code=429, content={"error": "For mange forespørgsler — prøv igen om lidt"})
    tasks = [
        scrape_news(app.state.client, navn, meta["url"], meta["gruppe"], q, limit)
        for navn, meta in SCRAPE_SOURCES.items()
    ]
    nested = await asyncio.gather(*tasks)

    articles = [a for sub in nested for a in sub]
    articles.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)
    return {
        "articles": articles,
        "total": len(articles),
        "sources_checked": len(SCRAPE_SOURCES),
        "query": q,
        "scanned_at": datetime.now(timezone.utc).isoformat()
    }


# ─────────────────────────────────────────────────────────────
# MCP-SERVER — /mcp (streamable HTTP, stateless)
# Lader Claude (og andre MCP-klienter) søge i DNNK's vidensbank:
# webinar-indekset + transskriptionerne. Alt data er offentligt
# (offentlige GitHub-repos), så der er ingen auth på endpointet.
# ─────────────────────────────────────────────────────────────
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

TRANSCRIPTOR_RAW_BASE = "https://raw.githubusercontent.com/klimatilpasning/dnnk-transcriptor/main/"

mcp_server = FastMCP(
    "dnnk-vidensbank",
    instructions=(
        "Søg i DNNK's (Det Nationale Netværk for Klimatilpasning) vidensbank "
        "med ~227 webinarer om klimatilpasning i Danmark. Brug soeg_vidensbank "
        "til at finde webinarer, soeg_passager til at finde konkrete passager "
        "med tidsstempler og YouTube-links, og hent_transskription til at læse "
        "en hel transskription."
    ),
    stateless_http=True,
    json_response=True,
    # SDK'ens DNS-rebinding-beskyttelse tillader kun localhost som standard
    # og svarede 421 Misdirected Request på Render-domænet. Tillad de værter
    # tjenesten faktisk serveres på (+ localhost til lokale tests).
    transport_security=TransportSecuritySettings(
        allowed_hosts=[
            "dnnk-klimamonitor-proxy.onrender.com",
            "localhost", "localhost:*", "127.0.0.1", "127.0.0.1:*",
        ],
        allowed_origins=["*"],
    ),
)

# Tidsstempel på egen linje ("HH:MM:SS") adskiller transskriptionens segmenter
_TS_LINE_RE = re.compile(r"(?m)^(\d{2}:\d{2}:\d{2})\s*$")


def _ts_til_sekunder(ts: str) -> int:
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def _youtube_link_med_tid(youtube_url: str, ts: str) -> str:
    """YouTube-link der starter afspilningen ved tidsstemplet ts."""
    if not youtube_url:
        return ""
    sep = "&" if "?" in youtube_url else "?"
    return f"{youtube_url}{sep}t={_ts_til_sekunder(ts)}s"


async def _hent_transskription_raa(path: str) -> str:
    """Hent rå transskription fra transcriptor-repoet via den delte
    httpx-client. Genbruger feed-TTL-cachen, så gentagne opslag i samme
    transskription ikke rammer GitHub hver gang."""
    from urllib.parse import quote
    url = TRANSCRIPTOR_RAW_BASE + quote(path)
    now = time.time()
    cached = _FEED_CACHE.get(url)
    if cached and now - cached[0] < FEED_TTL:
        return cached[1]
    resp = await app.state.client.get(url, timeout=20)
    resp.raise_for_status()
    text = resp.text
    _FEED_CACHE[url] = (now, text)
    return text


def _chunk_transskription(text: str, maks_tegn: int = 1500) -> list:
    """Del en transskription i blokke på ~maks_tegn, brudt på tidsstempel-
    grænser. Returnerer [(tidsstempel_for_blokkens_start, tekst), ...]."""
    matches = list(_TS_LINE_RE.finditer(text))
    if not matches:
        t = text.strip()
        return [("00:00:00", t)] if t else []
    segments = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        seg = " ".join(text[m.end():end].split())
        if seg:
            segments.append((m.group(1), seg))
    blocks = []
    cur_ts, cur_parts, cur_len = None, [], 0
    for ts, seg in segments:
        if cur_parts and cur_len + len(seg) > maks_tegn:
            blocks.append((cur_ts, " ".join(cur_parts)))
            cur_ts, cur_parts, cur_len = None, [], 0
        if cur_ts is None:
            cur_ts = ts
        cur_parts.append(seg)
        cur_len += len(seg) + 1
    if cur_parts:
        blocks.append((cur_ts, " ".join(cur_parts)))
    return blocks


def _score_mod_indeks(q_words: set, item: dict) -> int:
    """Scor et forberedt indeks-item mod forespørgslens ord: titel/keyword-
    match vejer dobbelt, match i resumé/oplægsholdere/kategori vejer enkelt."""
    return len(q_words & item["words"]) * 2 + len(q_words & item["words_full"])


@mcp_server.tool()
async def soeg_vidensbank(forespoergsel: str, max_resultater: int = 5) -> list:
    """Søg i DNNK's vidensbank over webinarer om klimatilpasning.

    Matcher forespørgslens ord mod webinarernes titel, nøgleord, resumé,
    kategori og oplægsholdere og returnerer de mest relevante webinarer.
    Brug danske fagtermer eller stednavne, fx "skybrudstunnel",
    "grundvandsstigning", "kystbeskyttelse Lolland" eller "LAR Vejle".

    Args:
        forespoergsel: Søgeord på dansk, fx "skybrudstunnel København".
        max_resultater: Højst antal webinarer der returneres (1-20, standard 5).

    Returns:
        Liste af webinarer med felterne titel, dato, kategori, resume,
        youtube_url, dnnk_url, type og path. Feltet path bruges videre i
        hent_transskription; tom liste hvis intet matcher.
    """
    q_words = _tokens(forespoergsel, min_len=3)
    if not q_words:
        return []
    prepared = await get_webinar_index()
    scored = []
    for item in prepared:
        score = _score_mod_indeks(q_words, item)
        if score > 0:
            scored.append((score, item["entry"]))
    scored.sort(key=lambda x: -x[0])
    n = max(1, min(int(max_resultater), 20))
    return [{
        "titel": e.get("title", ""),
        "dato": e.get("date", ""),
        "kategori": e.get("category", ""),
        "resume": (e.get("summary") or "")[:300],
        "youtube_url": e.get("youtube_url", ""),
        "dnnk_url": e.get("dnnk_url", ""),
        "type": e.get("type"),
        "path": e.get("path", ""),
    } for _, e in scored[:n]]


@mcp_server.tool()
async def soeg_passager(forespoergsel: str, max_passager: int = 6) -> list:
    """Find de mest relevante passager i DNNK's webinar-transskriptioner.

    Finder først de op til 3 mest relevante webinarer, henter deres fulde
    transskriptioner og returnerer de tekstblokke (~1500 tegn) der bedst
    matcher forespørgslen — hver med tidsstempel og et YouTube-link der
    starter afspilningen på det rigtige sted. Brug dette værktøj når du
    skal citere eller henvise præcist til hvad der blev sagt i et webinar.

    Args:
        forespoergsel: Søgeord på dansk, fx "medfinansiering af skybrudsprojekter".
        max_passager: Højst antal passager på tværs af webinarerne (1-20, standard 6).

    Returns:
        Liste af {webinar_titel, tidsstempel, youtube_link, tekst} sorteret
        efter relevans; tom liste hvis intet matcher.
    """
    q_words = _tokens(forespoergsel, min_len=3)
    if not q_words:
        return []
    prepared = await get_webinar_index()
    kandidater = []
    for item in prepared:
        e = item["entry"]
        if not e.get("path"):
            continue
        score = _score_mod_indeks(q_words, item)
        if score > 0:
            kandidater.append((score, e))
    kandidater.sort(key=lambda x: -x[0])

    passager = []
    for _, e in kandidater[:3]:
        try:
            tekst = await _hent_transskription_raa(e["path"])
        except Exception as ex:
            print(f"[mcp] transskription kunne ikke hentes ({e.get('path')}): {ex}")
            continue
        for ts, blok in _chunk_transskription(tekst):
            blok_tokens = _TOKEN_RE.findall(blok.lower())
            distinkte = len(q_words & set(blok_tokens))
            if distinkte == 0:
                continue
            forekomster = sum(1 for t in blok_tokens if t in q_words)
            passager.append((distinkte, forekomster, {
                "webinar_titel": e.get("title", ""),
                "tidsstempel": ts,
                "youtube_link": _youtube_link_med_tid(e.get("youtube_url", ""), ts),
                "tekst": blok,
            }))
    passager.sort(key=lambda p: (-p[0], -p[1]))
    n = max(1, min(int(max_passager), 20))
    return [p for _, _, p in passager[:n]]


@mcp_server.tool()
async def hent_transskription(path: str, fra_tegn: int = 0, max_tegn: int = 50000) -> dict:
    """Hent den rå transskription af et DNNK-webinar.

    path fås fra soeg_vidensbank (feltet "path"). Transskriptionen har
    tidsstempler på formen HH:MM:SS på egen linje for ca. hvert udsagn.
    Lange transskriptioner kan hentes i bidder med fra_tegn/max_tegn —
    tjek total_tegn i svaret for at se om der er mere.

    Args:
        path: Sti i transcriptor-repoet; skal starte med "transcriptions/"
            og ende på ".txt" (andet afvises).
        fra_tegn: Startposition (0-indekseret) i teksten, standard 0.
        max_tegn: Højst antal tegn der returneres (1-100000, standard 50000).

    Returns:
        {path, total_tegn, fra_tegn, til_tegn, tekst}
    """
    path = (path or "").strip().lstrip("/")
    if not path.startswith("transcriptions/") or not path.endswith(".txt") or ".." in path:
        raise ValueError('Ugyldig path — skal starte med "transcriptions/" og ende på ".txt".')
    tekst = await _hent_transskription_raa(path)
    fra = max(0, int(fra_tegn))
    maks = max(1, min(int(max_tegn), 100_000))
    udsnit = tekst[fra:fra + maks]
    return {
        "path": path,
        "total_tegn": len(tekst),
        "fra_tegn": fra,
        "til_tegn": fra + len(udsnit),
        "tekst": udsnit,
    }


# Streamable-HTTP-appen serverer selv på settings.streamable_http_path
# (default "/mcp"), så den monteres på RODEN — mount på "/mcp" ville give
# dobbelt sti (/mcp/mcp), og at omdøbe stien til "/" ville give redirects.
# Mount'en ligger sidst i filen: alle FastAPI-routes ovenfor matcher først,
# kun umatchede stier (herunder /mcp) når ned til MCP-appen. Kaldet opretter
# også session_manager, som lifespan øverst i filen holder kørende.
app.mount("/", mcp_server.streamable_http_app())
