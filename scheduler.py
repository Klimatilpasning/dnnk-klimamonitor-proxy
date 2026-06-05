import asyncio
import httpx
import os
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
DIGEST_EMAIL_TO = os.environ.get("DIGEST_EMAIL_TO", "kp@dnnk.dk")
DIGEST_EMAIL_FROM = os.environ.get("DIGEST_EMAIL_FROM", "kp@dnnk.dk")
DIGEST_EMAIL_FROM_NAME = "DNNK Klimamonitor"
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://dnnk-klimamonitor-proxy.onrender.com")

# Fil til at gemme tidligere sendte artikler
SENT_ARTICLES_FILE = Path("/tmp/sent_articles.json")

QUERIES = [
    # ── Klimatilpasning – kernesøgninger ──
    "klimatilpasning skybrud oversvømmelse",
    "LAR regnvand faskine regnbed",
    "spildevand klimasikring kloakseparering",
    "kystbeskyttelse stormflod havvandsstigning",
    "klimahandlingsplan DK2020 serviceniveau",

    # ── Vandkredsløbet & grundvand ──
    "grundvand BNBO indvindingstilladelse",
    "vandløb vandløbsrestaurering rørlagt vandløb",
    "vådområde lavbund sørestaurering",
    "vandbalance afstrømning nedbør fordampning",
    "drænvand nitrat fosfor vandkvalitet",

    # ── Kreative & innovative vinkler ──
    "svampeby blå-grøn naturbaseret løsning",
    "klimakvarter skybrudsplan vandplus",
    "klimatilpasset byggeri grønt tag resiliens",
    "sponge city living shoreline biomimicry",
    "urban heat island varmeø afkøling",
    "adaptive design fremtidssikring robusthed",

    # ── Lovgivning & EU ──
    "oversvømmelsesdirektiv klimatilpasningsloven høring",
    "Interreg LIFE Horizon klimatilpasning",
    "folketing klima miljø lovforslag",

    # ── Videnskab & forskning ──
    "climate adaptation research urban flooding",
    "nature-based solutions flood groundwater",
    "water cycle resilience infrastructure",

    # ── Nordiske & svenske kystkilder ──
    "kustplanering havsnivå klimatanpassning",
    "Movium urbana landskap robusta städer",
    "SGI flexibel markanvändning stegvis planering",
    "kustskydd kusterosion stigande hav",
]

def load_sent_articles() -> set:
    """Hent liste over tidligere sendte artikel-titler"""
    try:
        if SENT_ARTICLES_FILE.exists():
            data = json.loads(SENT_ARTICLES_FILE.read_text())
            return set(data.get("titles", []))
    except Exception:
        pass
    return set()

DNNK_INDEX_URL = "https://raw.githubusercontent.com/klimatilpasning/dnnk-vidensassistent/main/search-index.json"
_dnnk_index_cache = None

async def fetch_dnnk_index() -> list:
    """Hent DNNK's webinar-indeks (cached i hukommelsen for denne koersel)."""
    global _dnnk_index_cache
    if _dnnk_index_cache is not None:
        return _dnnk_index_cache
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(DNNK_INDEX_URL)
            if r.status_code == 200:
                _dnnk_index_cache = r.json()
                print(f"Hentet DNNK-indeks: {len(_dnnk_index_cache)} webinarer")
                return _dnnk_index_cache
    except Exception as e:
        print(f"Kunne ikke hente DNNK-indeks: {e}")
    _dnnk_index_cache = []
    return []

def find_relevant_webinars(article: dict, dnnk_index: list, top_n: int = 2) -> list:
    """Find op til top_n DNNK-webinarer der matcher artiklen via noegleord-overlap."""
    if not dnnk_index:
        return []
    text = (article.get("title", "") + " " + article.get("summary", "")).lower()
    article_words = set(w for w in text.replace(",", " ").replace(".", " ").split() if len(w) > 4)
    scored = []
    for entry in dnnk_index:
        if not entry.get("youtube_url"):
            continue
        kws = [k.lower() for k in entry.get("keywords", [])]
        title_low = entry.get("title", "").lower()
        kw_score = sum(1 for kw in kws if any(w in kw or kw in w for w in article_words))
        title_score = sum(1 for w in article_words if len(w) > 5 and w in title_low)
        total = kw_score * 2 + title_score
        if total >= 3:
            scored.append((total, entry))
    scored.sort(key=lambda x: -x[0])
    return [e for _, e in scored[:top_n]]

def save_sent_articles(titles: set):
    """Gem sendte artikel-titler — behold kun de seneste 500"""
    try:
        titles_list = list(titles)[-500:]
        SENT_ARTICLES_FILE.write_text(json.dumps({"titles": titles_list}))
    except Exception as e:
        print(f"Kunne ikke gemme sendte artikler: {e}")

def get_yesterday_str() -> str:
    """Returner gårsdagens dato som YYYY-MM-DD"""
    from datetime import timedelta
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def is_recent(article: dict) -> bool:
    """Returner True hvis artiklen er fra de seneste 2 dage"""
    date_str = article.get("date", "")
    if not date_str or len(date_str) < 10:
        return True  # Ingen dato — inkluder altid
    try:
        from datetime import timedelta
        art_date = datetime.strptime(date_str[:10], "%Y-%m-%d")
        cutoff = datetime.now() - timedelta(days=2)
        return art_date >= cutoff
    except Exception:
        return True

async def fetch_articles(query: str, limit: int = 5) -> list:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{BASE_URL}/news/full",
                params={"q": query, "limit": limit}
            )
            data = resp.json()
            return data.get("articles", [])
    except Exception as e:
        print(f"Fejl ved hentning af artikler for '{query}': {e}")
        return []

async def fetch_scrape(query: str) -> list:
    """Hent scraped artikler fra kommuner, forsyninger og myndigheder"""
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.get(
                f"{BASE_URL}/news/scrape",
                params={"q": query}
            )
            data = resp.json()
            return data.get("articles", [])
    except Exception as e:
        print(f"Fejl ved scraping: {e}")
        return []

async def fetch_ted(query: str, size: int = 5) -> list:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{BASE_URL}/ted",
                params={"q": query, "size": size}
            )
            data = resp.json()
            return data.get("notices", data.get("results", []))
    except Exception as e:
        print(f"Fejl ved hentning af TED-udbud: {e}")
        return []

def build_html_email(articles: list, scrape_articles: list, ted_notices: list, scan_date: str, new_count: int, dnnk_index: list = None, analysis_html: str = "") -> str:

    def article_row(art, badge="", related=None):
        tags = ", ".join(art.get("tags", []))
        url = art.get("url", "#") or "#"
        gruppe = art.get("gruppe", "")
        gruppe_html = f'<span style="background:#e8f4fd;color:#1a4d6e;padding:2px 6px;border-radius:3px;font-size:11px;margin-left:6px;">{gruppe}</span>' if gruppe else ""
        related_html = ""
        if related:
            items = "".join([
                f'<div style="margin-top:3px;"><a href="{w.get("youtube_url","#")}" style="color:#5B9BBF;text-decoration:none;font-size:12px;">&#9654; {w.get("title","")[:90]}</a></div>'
                for w in related
            ])
            related_html = f'<div style="margin-top:8px;padding:6px 10px;background:#F4F8FB;border-left:3px solid #5B9BBF;border-radius:0 3px 3px 0;"><div style="color:#5B9BBF;font-size:10px;font-weight:bold;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:3px;">Fra DNNKs arkiv</div>{items}</div>'
        return f"""
        <tr>
          <td style="padding:12px 0; border-bottom:1px solid #e8f0e0;">
            {f'<span style="background:#52b788;color:white;padding:2px 6px;border-radius:3px;font-size:10px;font-weight:bold;margin-right:6px;">NY</span>' if badge == 'ny' else ''}
            <a href="{url}" style="color:#2d6a4f;font-weight:bold;text-decoration:none;">{art.get('title','')}</a>{gruppe_html}<br>
            <span style="color:#666;font-size:12px;">{art.get('feedSource','')} &middot; {art.get('date','')}</span><br>
            <span style="color:#444;font-size:13px;">{(art.get('summary','') or '')[:200]}{'...' if len(art.get('summary','') or '') > 200 else ''}</span><br>
            {'<span style="color:#888;font-size:11px;">' + tags + '</span>' if tags else ''}
            {related_html}
          </td>
        </tr>"""

    article_rows = "".join([article_row(a, "ny", find_relevant_webinars(a, dnnk_index or [])) for a in articles])
    scrape_rows = "".join([article_row(a, "ny", find_relevant_webinars(a, dnnk_index or [])) for a in scrape_articles[:10]])

    ted_rows = ""
    for notice in ted_notices[:5]:
        title = notice.get("title", {})
        if isinstance(title, dict):
            title = title.get("dan", title.get("eng", "Uden titel"))
        url = notice.get("tedPublicationUrl", "#")
        date = notice.get("publicationDate", "")[:10]
        ted_rows += f"""
        <tr>
          <td style="padding:10px 0; border-bottom:1px solid #e8f0e0;">
            <a href="{url}" style="color:#1a4d6e;font-weight:bold;text-decoration:none;">{title}</a><br>
            <span style="color:#666;font-size:12px;">TED EU · {date}</span>
          </td>
        </tr>"""

    if not ted_rows:
        ted_rows = "<tr><td style='color:#888;padding:10px 0;'>Ingen nye EU-udbud fundet i dag.</td></tr>"

    scrape_section = ""
    if scrape_rows:
        scrape_section = f"""
    <h2 style="color:#1a3d2b;border-bottom:2px solid #b7e4c7;padding-bottom:8px;margin-top:32px;">🏛️ Kommuner, forsyninger og myndigheder</h2>
    <table width="100%" cellpadding="0" cellspacing="0">
      {scrape_rows}
    </table>"""

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;max-width:680px;margin:0 auto;background:#f9fdf6;padding:20px;">
  <div style="background:#2d6a4f;padding:24px;border-radius:8px 8px 0 0;">
    <h1 style="color:white;margin:0;font-size:22px;">🌿 DNNK Klimamonitor</h1>
    <p style="color:#b7e4c7;margin:6px 0 0;">Daglig scanning · {scan_date} · <strong style="color:white;">{new_count} nye artikler</strong></p>
  </div>
  <div style="background:white;padding:24px;border-radius:0 0 8px 8px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
    {analysis_html}
    <h2 style="color:#2d6a4f;border-bottom:2px solid #b7e4c7;padding-bottom:8px;">📰 Nyheder og fagartikler</h2>
    <table width="100%" cellpadding="0" cellspacing="0">
      {article_rows if article_rows else "<tr><td style='color:#888;padding:10px 0;'>Ingen nye nyheder siden sidst.</td></tr>"}
    </table>
    {scrape_section}
    <h2 style="color:#1a4d6e;border-bottom:2px solid #bee3f8;padding-bottom:8px;margin-top:32px;">🇪🇺 EU-udbud (TED)</h2>
    <table width="100%" cellpadding="0" cellspacing="0">
      {ted_rows}
    </table>
    <p style="color:#aaa;font-size:11px;margin-top:32px;border-top:1px solid #eee;padding-top:12px;">
      Sendt automatisk af DNNK Klimamonitor · 
      <a href="https://kornelius-stack.github.io/dnnk-klimamonitor-proxy/" style="color:#2d6a4f;">Åbn klimamonitor</a>
    </p>
  </div>
</body>
</html>"""

async def send_brevo_email(subject: str, html_content: str):
    if not BREVO_API_KEY:
        print("ADVARSEL: BREVO_API_KEY ikke sat – e-mail ikke sendt")
        return

    payload = {
        "sender": {"name": DIGEST_EMAIL_FROM_NAME, "email": DIGEST_EMAIL_FROM},
        "to": [{"email": DIGEST_EMAIL_TO}],
        "subject": subject,
        "htmlContent": html_content
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.brevo.com/v3/smtp/email",
            json=payload,
            headers={
                "api-key": BREVO_API_KEY,
                "Content-Type": "application/json"
            }
        )
        if resp.status_code in (200, 201):
            print(f"E-mail sendt til {DIGEST_EMAIL_TO} via Brevo ✅")
        else:
            print(f"Brevo fejl {resp.status_code}: {resp.text}")

# ─────────────────────────────────────────────────────────────
# INDHOLDS- & RELEVANSANALYSE (Claude Haiku, server-side nøgle)
# ─────────────────────────────────────────────────────────────

async def claude_analysis(prompt: str, max_tokens: int = 700) -> str:
    """Kør en analyse via Claude Haiku med serverens egen nøgle.
    Returnerer ren HTML-tekst, eller '' ved fejl (så mailen stadig sendes)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return ""
    try:
        async with httpx.AsyncClient(timeout=40) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            data = resp.json()
            if "content" in data and data["content"]:
                return data["content"][0].get("text", "").strip()
    except Exception as e:
        print(f"Analyse-fejl: {e}")
    return ""


def _articles_to_lines(articles: list, limit: int = 30) -> str:
    lines = []
    for a in articles[:limit]:
        kilde = a.get("gruppe", "") or a.get("feedSource", "")
        lines.append(f"- [{kilde}] {a.get('title','')} :: {(a.get('summary','') or '')[:160]}")
    return "\n".join(lines)


async def build_daily_analysis_html(articles: list) -> str:
    """Kort daglig relevans- og temaanalyse til toppen af digesten."""
    if not articles:
        return ""
    prompt = (
        "Du er DNNK's redaktionelle analytiker for klimatilpasning. "
        "Her er dagens fundne artikler fra Klimamonitor:\n\n"
        + _articles_to_lines(articles, 30)
        + "\n\nLav en KORT analyse på dansk:\n"
        "1) Relevans: hvor stor en andel virker reelt relevant for klimatilpasning, "
        "og nævn tydeligt off-topic støj (med titel) hvis der er noget.\n"
        "2) Dagens hovedtemaer (2-4 punkter).\n"
        "3) Det vigtigste at bemærke (2-3 sætninger).\n"
        "Svar i ren HTML med <p>, <ul>, <li>, <strong> — INGEN <html>/<body>-tags."
    )
    html = await claude_analysis(prompt, max_tokens=700)
    if not html:
        return ""
    return (
        '<div style="background:#F4F8FB;border-left:4px solid #5B9BBF;'
        'padding:14px 18px;border-radius:0 6px 6px 0;margin-bottom:24px;">'
        '<div style="color:#3a6e8a;font-size:12px;font-weight:bold;text-transform:uppercase;'
        'letter-spacing:0.5px;margin-bottom:6px;">🔍 Dagens relevansanalyse</div>'
        f'<div style="color:#2c2c2c;font-size:13px;line-height:1.6;">{html}</div>'
        '<div style="color:#999;font-size:10px;margin-top:8px;">Automatisk genereret analyse — vurdér selv.</div>'
        '</div>'
    )


async def run_weekly_analysis():
    """Dybere ugentlig indholdsanalyse — sendes som separat e-mail."""
    print(f"[{datetime.now().strftime('%H:%M')}] Starter ugentlig indholdsanalyse...")
    dnnk_index = await fetch_dnnk_index()

    all_articles = []
    for query in QUERIES:
        all_articles.extend(await fetch_articles(query, limit=5))
    all_articles.extend(await fetch_scrape("klimatilpasning"))

    # Dedupliker + behold seneste uge
    seen, unique = set(), []
    for a in all_articles:
        t = a.get("title", "")
        if t and t not in seen:
            seen.add(t)
            unique.append(a)
    unique.sort(key=lambda x: (x.get("relevance", 0), x.get("date", "")), reverse=True)

    if not unique:
        print("Ugentlig analyse: ingen artikler — springer over")
        return

    webinar_titles = ", ".join(e.get("title", "") for e in (dnnk_index or [])[:60])
    prompt = (
        "Du er DNNK's redaktionelle analytiker for klimatilpasning. "
        "Her er ugens samlede artikler fra Klimamonitor:\n\n"
        + _articles_to_lines(unique, 60)
        + "\n\nDNNK's webinar-arkiv (titler):\n" + webinar_titles
        + "\n\nLav en GRUNDIG ugentlig analyse på dansk:\n"
        "1) Overordnet relevansvurdering af ugens output (signal vs. støj).\n"
        "2) De vigtigste 3-5 temaer/tendenser med kort begrundelse.\n"
        "3) Kobling til DNNK's vidensbank: hvilke eksisterende webinarer er mest "
        "relevante for ugens temaer, og hvor er der huller arkivet ikke dækker?\n"
        "4) Anbefalinger: hvad bør DNNK holde øje med eller producere indhold om.\n"
        "Svar i ren HTML med <h3>, <p>, <ul>, <li>, <strong> — INGEN <html>/<body>-tags."
    )
    analysis = await claude_analysis(prompt, max_tokens=1600)
    if not analysis:
        print("Ugentlig analyse: tom — springer over")
        return

    scan_date = datetime.now().strftime("%d. %B %Y")
    html = f"""
<!DOCTYPE html><html><head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;max-width:680px;margin:0 auto;background:#f9fdf6;padding:20px;">
  <div style="background:#3a6e8a;padding:24px;border-radius:8px 8px 0 0;">
    <h1 style="color:white;margin:0;font-size:22px;">📊 DNNK Ugentlig indholdsanalyse</h1>
    <p style="color:#cfe4f0;margin:6px 0 0;">Uge afsluttet {scan_date} · {len(unique)} artikler analyseret</p>
  </div>
  <div style="background:white;padding:24px;border-radius:0 0 8px 8px;box-shadow:0 2px 8px rgba(0,0,0,0.08);font-size:14px;line-height:1.65;color:#2c2c2c;">
    {analysis}
    <p style="color:#aaa;font-size:11px;margin-top:32px;border-top:1px solid #eee;padding-top:12px;">
      Automatisk genereret af DNNK Klimamonitor · vurdér altid indholdet selv.
    </p>
  </div>
</body></html>"""
    await send_brevo_email(f"DNNK Ugentlig indholdsanalyse · {scan_date}", html)
    print("run_weekly_analysis afsluttet")


async def run_daily_digest():
    print(f"[{datetime.now().strftime('%H:%M')}] Starter daglig scanning...")
    dnnk_index = await fetch_dnnk_index()

    # Hent tidligere sendte artikler
    sent_titles = load_sent_articles()
    print(f"Kendte artikler fra tidligere: {len(sent_titles)}")

    # Hent RSS artikler
    all_articles = []
    for query in QUERIES:
        articles = await fetch_articles(query, limit=5)
        all_articles.extend(articles)

    # Hent scraped artikler
    scrape_articles = await fetch_scrape("klimatilpasning")

    # Hent TED udbud
    ted_notices = await fetch_ted("klimatilpasning skybrud", size=5)

    # Dedupliker RSS
    seen = set()
    unique_articles = []
    for art in all_articles:
        key = art.get("title", "")
        if key and key not in seen:
            seen.add(key)
            unique_articles.append(art)

    # Dedupliker scrape
    seen_scrape = set()
    unique_scrape = []
    for art in scrape_articles:
        key = art.get("title", "")
        if key and key not in seen_scrape and art.get("relevance", 0) > 0:
            seen_scrape.add(key)
            unique_scrape.append(art)

    # Filtrer kun NYE artikler (ikke sendt før OG fra de seneste 2 dage)
    new_articles = [a for a in unique_articles if a.get("title", "") not in sent_titles and is_recent(a)]
    new_scrape = [a for a in unique_scrape if a.get("title", "") not in sent_titles and is_recent(a)]

    new_articles.sort(key=lambda x: (x.get("relevance", 0), x.get("date", "")), reverse=True)
    new_scrape.sort(key=lambda x: (x.get("relevance", 0), x.get("date", "")), reverse=True)

    total_new = len(new_articles) + len(new_scrape)
    print(f"Nye artikler: {len(new_articles)} RSS + {len(new_scrape)} scrape = {total_new} i alt")

    # Send kun hvis der er nye artikler
    if total_new == 0:
        print("Ingen nye artikler — e-mail ikke sendt")
    else:
        scan_date = datetime.now().strftime("%d. %B %Y")
        analysis_html = await build_daily_analysis_html(new_articles[:15] + new_scrape[:10])
        html = build_html_email(new_articles[:15], new_scrape[:10], ted_notices, scan_date, total_new, dnnk_index, analysis_html)
        subject = f"DNNK Klimamonitor · {scan_date} · {total_new} nye artikler"
        await send_brevo_email(subject, html)

    # Gem alle sendte titler
    all_sent = sent_titles | {a.get("title", "") for a in unique_articles + unique_scrape}
    save_sent_articles(all_sent)
    print("run_daily_digest afsluttet")

async def scheduler_loop():
    cph = timezone(timedelta(hours=1))
    print("Scheduler startet – venter på kl. 08:00...")
    while True:
        now = datetime.now(cph)
        next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)
        if now >= next_run:
            next_run = next_run + timedelta(days=1)
        wait_seconds = (next_run - now).total_seconds()
        print(f"Næste scanning: {next_run.strftime('%d/%m %H:%M')} (om {int(wait_seconds // 3600)}t {int((wait_seconds % 3600) // 60)}m)")
        await asyncio.sleep(wait_seconds)
        await run_daily_digest()
        # Ugentlig dyb indholdsanalyse om mandagen (efter den daglige digest)
        if datetime.now(cph).weekday() == 0:
            await run_weekly_analysis()
