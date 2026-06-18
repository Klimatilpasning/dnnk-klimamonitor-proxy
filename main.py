from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime
import asyncio
import re
import os
import time
import collections

app = FastAPI(title="DNNK Klimamonitor Proxy")

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

# ── Misbrugsbeskyttelse på de endpoints der bruger serverens API-nøgle ──
_RATE = collections.defaultdict(list)
RATE_LIMIT = int(os.environ.get("DNNK_RATE_LIMIT", "20"))   # kald pr. vindue pr. IP
RATE_WINDOW = 60                                            # sekunder

def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "ukendt"

def is_rate_limited(request: Request) -> bool:
    ip = _client_ip(request)
    now = time.time()
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
    return request.headers.get("x-dnnk-code", "") == code

def trigger_ok(request: Request) -> bool:
    """Beskytter de trigger-endpoints der koster API/e-mail. Token kan gives
    som ?token=... eller X-DNNK-Code-header. Slået fra hvis DNNK_ACCESS_CODE
    ikke er sat."""
    code = os.environ.get("DNNK_ACCESS_CODE", "")
    if not code:
        return True
    token = request.query_params.get("token", "") or request.headers.get("x-dnnk-code", "")
    return token == code

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
        return f"{m2.group(3)}-{m2.group(2).zfill(2)}-{m2.group(1).zfill(2)}"
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

def score_article(combined: str, q_match: bool):
    """Returnér (relevance 0-1, keep).

    Kerneord vejer 3, brede ord 1, et søge-match giver 3. En artikel beholdes
    kun hvis den rammer mindst ét kerneord, matcher søgningen, eller rammer
    mindst to brede ord — så artikler der blot strejfer 'klima'/'miljø' (fx
    ministerrokade eller elpriser) sorteres fra i stedet for at score 1."""
    core_hits = sum(1 for kw in KEYWORDS
                    if kw not in BROAD_KEYWORDS and kw_match(kw, combined))
    broad_hits = sum(1 for kw in BROAD_KEYWORDS if kw_match(kw, combined))
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

def parse_item_et(item):
    """Parse et RSS/Atom item med ElementTree"""
    title = ""
    description = ""
    link = ""
    pub_date = ""
    for child in item:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        text = (child.text or "").strip()
        if tag == "title" and not title:
            title = text
        elif tag in ("description", "summary", "content") and not description:
            description = re.sub(r"<[^>]+>", "", text)[:400]
        elif tag == "link" and not link:
            href = child.get("href", "")
            link = href if href else text
        elif tag == "id" and not link:
            link = text
        elif tag in ("pubDate", "published", "updated", "date") and not pub_date:
            pub_date = normalize_date(text) if text else ""
    return title, description, link, pub_date

async def fetch_rss(client, source, url, query, limit: int = 8):
    try:
        resp = await client.get(url, timeout=15, follow_redirects=True, headers=RSS_HEADERS)
        if resp.status_code != 200:
            return []
        
        content = resp.text
        items = []
        
        # Prøv først ElementTree
        try:
            clean = re.sub(r' xmlns[^=]*="[^"]*"', '', content)
            clean = re.sub(r'<\?xml[^>]*\?>', '', clean)
            root_el = ET.fromstring(clean)
            et_items = root_el.findall(".//item") + root_el.findall(".//entry")
            if et_items:
                items = [("et", i) for i in et_items]
        except ET.ParseError:
            pass
        
        # Fallback: BeautifulSoup
        if not items:
            try:
                soup = BeautifulSoup(content, "xml")
                bs_items = soup.find_all("item") + soup.find_all("entry")
                if bs_items:
                    items = [("bs", i) for i in bs_items]
            except Exception:
                try:
                    soup = BeautifulSoup(content, "lxml")
                    bs_items = soup.find_all("item") + soup.find_all("entry")
                    if bs_items:
                        items = [("bs", i) for i in bs_items]
                except Exception:
                    pass
        
        if not items:
            return []
        
        results = []
        q_lower = query.lower()

        for parser, item in items[:40]:
            if parser == "et":
                title, description, link, pub_date = parse_item_et(item)
            else:
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
                "tags": [kw for kw in KEYWORDS[:6] if kw_match(kw, combined)][:3],
                "relevance": relevance, "url": real_url(link), "value": None
            })
        results.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)
        return results[:limit]
    except Exception:
        return []

@app.get("/test-feeds")
async def test_feeds():
    """Test alle RSS feeds og returner status for hver"""
    from sources import ALL_FEEDS_FLAT

    async def check_feed(navn, meta):
        url = meta["url"]
        gruppe = meta["gruppe"]
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url, follow_redirects=True, headers=RSS_HEADERS)
                if resp.status_code != 200:
                    return {"navn": navn, "gruppe": gruppe, "url": url,
                            "status": "fejl", "info": f"HTTP {resp.status_code}"}
                content = resp.text
                # Prøv ET
                try:
                    clean = re.sub(r' xmlns[^=]*="[^"]*"', '', content)
                    root = ET.fromstring(clean)
                    items = root.findall(".//item") + root.findall(".//entry")
                    if items:
                        return {"navn": navn, "gruppe": gruppe, "url": url,
                                "status": "ok", "info": f"{len(items)} items (ET)"}
                except ET.ParseError:
                    pass
                # Prøv BS
                try:
                    soup = BeautifulSoup(content, "xml")
                    items = soup.find_all("item") + soup.find_all("entry")
                    if items:
                        return {"navn": navn, "gruppe": gruppe, "url": url,
                                "status": "ok", "info": f"{len(items)} items (BS)"}
                except Exception:
                    pass
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
        "testet": datetime.utcnow().isoformat()
    }

@app.get("/ted")
async def search_ted(q: str = Query("klimatilpasning"), size: int = 10):
    url = "https://api.ted.europa.eu/v3/notices/search"
    params = {"q": f"{q} Denmark", "pageSize": size,
              "fields": "title,organisations,publicationDate,contractValue,cpvCodes,noticeType,tedPublicationUrl",
              "country": "DNK"}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params)
        return resp.json()

@app.get("/news")
async def get_news(q: str = Query("klimatilpasning")):
    from sources import RSS_NEWS
    async with httpx.AsyncClient() as client:
        tasks = [fetch_rss(client, src, url, q) for src, url in RSS_NEWS.items()]
        nested = await asyncio.gather(*tasks)
    articles = [a for sub in nested for a in sub]
    articles.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)
    return {"articles": articles, "total": len(articles), "query": q}

@app.get("/news/full")
async def get_news_full(q: str = Query("klimatilpasning"), gruppe: str = Query(None), limit: int = Query(8)):
    from sources import ALL_FEEDS_FLAT, ALLE_FEEDS
    feeds = ALL_FEEDS_FLAT
    if gruppe and gruppe in ALLE_FEEDS:
        feeds = {k: {"url": v, "gruppe": gruppe} for k, v in ALLE_FEEDS[gruppe].items()}
    async with httpx.AsyncClient() as client:
        tasks = [fetch_rss(client, navn, meta["url"], q, limit) for navn, meta in feeds.items()]
        nested = await asyncio.gather(*tasks)
    articles = []
    for i, (navn, meta) in enumerate(feeds.items()):
        for art in nested[i][:limit]:
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

    articles.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)
    return {"articles": articles, "total": len(articles),
            "feeds_checked": len(feeds), "query": q,
            "scanned_at": datetime.utcnow().isoformat()}

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

@app.on_event("startup")
async def start_scheduler():
    # Intern scheduler er som standard slået FRA (digest-mails stoppet på brugerens anmodning).
    # Sæt miljøvariablen SCHEDULER_ENABLED=true på Render for at aktivere igen.
    if os.environ.get("SCHEDULER_ENABLED", "").lower() not in ("1", "true", "yes"):
        print("Scheduler deaktiveret (SCHEDULER_ENABLED ikke sat) – sender ingen digest-mails.")
        return
    asyncio.create_task(_scheduler_loop())

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

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"error": "Ingen server-API-nøgle konfigureret"}

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": min(max(max_tokens, 1), 4096),
                    "system": system,
                    "messages": messages
                }
            )
            return resp.json()
    except Exception as e:
        return {"error": str(e)[:200]}


# In-memory cache for query expansions (resets on restart)
_expand_cache = {}

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
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "claude-haiku-4-5-20251001",
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
                _expand_cache[q_key] = terms
                return {"query": q, "terms": terms}
    except Exception as e:
        return {"query": q, "terms": [], "error": str(e)[:200]}

    return {"query": q, "terms": []}

@app.get("/")
def root():
    return {"status": "ok", "service": "DNNK Klimamonitor Proxy",
            "endpoints": ["/ted", "/news", "/news/full", "/news/kilder", "/test-feeds"]}


# ─────────────────────────────────────────────────────────────
# SCRAPING — til sider uden RSS
# ─────────────────────────────────────────────────────────────

# SCRAPE_SOURCES importeres fra sources.py
from sources import SCRAPE_SOURCES

async def scrape_news(client, source, url, gruppe, query, limit: int = 8):
    """Scraper nyhedsartikler direkte fra hjemmeside HTML"""
    from urllib.parse import urlparse, urljoin
    try:
        resp = await client.get(url, timeout=15, follow_redirects=True, headers=RSS_HEADERS)
        # Bemærk: flere danske CMS/SPA-sider (DMI, IDA, Klimarådet, SLA, HOFOR)
        # svarer HTTP 404 på serverniveau, men leverer alligevel hele nyhedslisten
        # i body. Vi afviser derfor IKKE på statuskode alene — vi forsøger at parse
        # så længe der er substantielt indhold. Selektorerne + relevans-filteret
        # giver naturligt 0 resultater for ægte (tomme) fejlsider.
        if not resp.text or len(resp.text) < 2000:
            return []

        soup = BeautifulSoup(resp.text, "lxml")
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

            # Find dato — søg i <time>, datetime-attribut, eller dato-klasser
            pub_date = ""
            time_el = el.find("time")
            if time_el:
                pub_date = (time_el.get("datetime") or time_el.get_text(strip=True))[:10]
            if not pub_date:
                date_el = el.find(class_=re.compile(r"date|dato|time|published|created", re.I))
                if date_el:
                    raw = date_el.get("datetime") or date_el.get("content") or date_el.get_text(strip=True)
                    # Forsøg at udtrække dato i format YYYY-MM-DD eller DD.MM.YYYY
                    m = re.search(r'(\d{4}-\d{2}-\d{2})', raw or "")
                    if m:
                        pub_date = m.group(1)
                    else:
                        m2 = re.search(r'(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})', raw or "")
                        if m2:
                            pub_date = f"{m2.group(3)}-{m2.group(2).zfill(2)}-{m2.group(1).zfill(2)}"

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
                "tags": [kw for kw in KEYWORDS[:6] if kw_match(kw, combined)][:3],
                "relevance": relevance,
                "url": article_url,
                "value": None,
                "gruppe": gruppe,
            })

        articles.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)
        return articles[:limit]

    except Exception:
        return []


@app.get("/news/scrape")
async def get_scraped_news(q: str = Query("klimatilpasning"), limit: int = Query(8)):
    """Hent nyheder via direkte scraping fra sider uden RSS"""
    async with httpx.AsyncClient() as client:
        tasks = [
            scrape_news(client, navn, meta["url"], meta["gruppe"], q, limit)
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
        "scanned_at": datetime.utcnow().isoformat()
    }
