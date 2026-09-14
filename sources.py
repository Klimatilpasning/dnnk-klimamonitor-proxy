# ─────────────────────────────────────────────────────────────
# DNNK Overvågningskilder
# ─────────────────────────────────────────────────────────────

# ── NYHEDER & FAGBLADE ──
RSS_NEWS = {
    "Ingeniøren":               "https://ing.dk/rss",
    "Ingeniøren Energi & Miljø":"https://ing.dk/term/rss/1964",
    "Altinget Miljø":           "https://www.altinget.dk/miljoe/rss.aspx",
    "DR Viden":                 "https://www.dr.dk/nyheder/service/feeds/viden",
    "DR Vejret":                "https://www.dr.dk/nyheder/service/feeds/vejret",
    "Børsen":                   "https://borsen.dk/rss",
    # Fjernet (døde RSS, nu dækket af "Brede søgninger"/Bing News): Altinget
    # Plan & Byg, Politiken Klima, Jyllands-Posten Klima, Berlingske Viden.
    # KTC flyttet til SCRAPE_SOURCES (RSS nedlagt).
}

# ── VIDENSINSTITUTIONER ──
RSS_VIDEN = {
    "Klimatorium":              "https://klimatorium.dk/feed/",
    # Fjernet (døde RSS, flyttet til SCRAPE_SOURCES): IDA, DANVA, CONCITO, DMI.
    # Fjernet 14/9-2026: Vand i Byer. Domænet er IKKE længere innovations-
    # netværkets site — det er overtaget og drives nu som indholdsfarm
    # ("V.A.N.D.I. Byer mediet") med SEO-artikler om VVS'ere, printertoner,
    # ladestandere og elleverandører. Feedet svarer 200 med friske datoer, så
    # det så sundt ud udefra, og enkelte vand-nære overskrifter slap igennem
    # relevansfilteret og blev vist som "Vidensinstitutioner".
}

# ── RÅDGIVERE ──
RSS_RAADGIVERE = {
    "Sweco":                    "https://www.sweco.dk/rss",
    # GEO's HTML-nyhedsliste er AngularJS-renderet (0 overskrifter i rå HTML),
    # men deres RSS virker — derfor flyttet hertil fra SCRAPE_SOURCES 14/9-2026.
    "GEO":                      "https://www.geo.dk/medie/nyheder/rss",
    # Fjernet (døde RSS, allerede dækket af SCRAPE_SOURCES): Rambøll, COWI,
    # Niras, Krüger, Orbicon|WSP.
}

# ── FORSYNINGER RSS ──
RSS_FORSYNINGER_RSS = {
    "HOFOR":                    "https://www.hofor.dk/rss",
}

# ── NORDISKE NABOER ──
RSS_NORDEN = {
    "SVT Nyheder Klima":        "https://www.svt.se/nyheter/rss.xml",
    "VA-guiden (SE)":           "https://www.vaguiden.se/rss",
    "NRK Klima":                "https://www.nrk.no/toppsaker.rss",
    "SMHI Sverige":             "https://www.smhi.se/rss/nyheter-fran-smhi",
    "Norsk Vann":               "https://www.norskvann.no/rss",
    # Fjernet: NCCS Norge (forkert institution — CO2-lagring, ikke
    # klimaservice; rette site har intet RSS) og SYKE Finland (intet RSS).
    "HaV Sverige":              "https://www.mynewsdesk.com/rss/current_news/6994",
    "SGI nyheder (SE)":         "https://api.client.notified.com/api/rss/publish/view/41885?type=news",
    "SGI presse (SE)":          "https://api.client.notified.com/api/rss/publish/view/41885?type=press",
}

# ── EU PROJEKTER ──
RSS_EU = {
    "Interreg Baltic Sea":      "https://interreg-baltic.eu/feed/",
    "Copernicus Klima":         "https://climate.copernicus.eu/rss.xml",
    # Fjernet (intet fungerende RSS længere — EEA/EU har nedlagt deres feeds;
    # alle kandidater testet 404/500/tom): Climate-ADAPT, EEA Nyheder,
    # EU Kommissionen ENV, EU Kommissionen Klima, JRC Science Hub.
}

# ── PLATFORME & NETVÆRK ──
RSS_PLATFORME = {
    "BLOXHUB":                  "https://bloxhub.org/rss",
    "Gate 21":                  "https://www.gate21.dk/rss",
    "State of Green":           "https://stateofgreen.com/en/feed/",
    # Fjernet (døde RSS): Realdania og Forsikring & Pension (dækket af
    # SCRAPE_SOURCES); Velux Fonden (intet RSS, ingen brugbar nyhedsliste).
}

# ── INTERNATIONALE INSTITUTIONER ──
RSS_INTERNATIONAL = {
    "FloodList":                "https://floodlist.com/feed",
    "ICLEI":                    "https://iclei.org/news/rss/",
    "UN Environment":           "https://www.unep.org/rss.xml",
    "IPCC":                     "https://www.ipcc.ch/feed/",
    "World Resources Inst.":    "https://www.wri.org/insights/rss.xml",
    # Fjernet (intet fungerende RSS): Deltares, The Nature Conservancy.
    # Fjernet: C40 Cities (Cloudflare 403'er Renders server-IP — virker fra
    # almindelige IP'er men leverer aldrig indhold fra serveren).
}

# ── VANDKREDSLØB & GRUNDVAND ──
RSS_VAND = {
    "Circle of Blue":           "https://www.circleofblue.org/feed/",
    # Fjernet (døde/tomme RSS, ingen fungerende alternativ fundet): NGWA,
    # H2O Waternetwerk, Water Research Fdn, IWA Water, The Source (IWA),
    # Stormwater Report (DNS-fejl), WaterWorld, Water & Wastewater Int.
}

# ── INT. VANDMYNDIGHEDER (NL, UK, US) ──
RSS_VAND_INT = {
    "Env. Agency (UK)":         "https://www.gov.uk/search/news-and-communications.atom?organisations[]=environment-agency",
    "Dutch Water Authorities":  "https://www.uvw.nl/feed/",
    "KWR Water Research":       "https://www.kwrwater.nl/feed/",
    # Fjernet (intet fungerende RSS): Rijkswaterstaat, USGS Water.
}

# ── KREATIVE VINKLER: design, arkitektur, innovation ──
RSS_KREATIVT = {
    "Dezeen Arkitektur":        "https://www.dezeen.com/feed/",
    "ArchDaily":                "https://www.archdaily.com/feed",
    "The Conversation Env.":    "https://theconversation.com/global/environment/articles.atom",
    "Planetizen":               "https://www.planetizen.com/rss.xml",
    # Fjernet: Tredje Natur, SLA (dækket af SCRAPE_SOURCES); WEF Natur & Klima,
    # Landezine, Fast Company (403 — bot-blok); Landscape Architecture (404);
    # Citylab/Bloomberg (sitemap, ikke et nyhedsfeed).
}

# ── LOVGIVNING & POLITIK ──
RSS_LOVGIVNING = {
    "Klimarådet":               "https://klimaraadet.dk/da/rss.xml",
    # Høringsportalens Atom-feed. Tilføjet 14/9-2026, fordi mim.dk/horinger er
    # nedlagt (404) og portalens egen HTML-liste er en Angular-SPA uden server-
    # renderet indhold. NB: ?Authorities=-parameteren ignoreres af portalen, så
    # feedet dækker ALLE myndigheders høringer — relevansfilteret skiller fra.
    "Høringsportalen":          "https://hoeringsportalen.dk/Syndication/HearingsFeed",
    # Fjernet: Folketing + Folketing Dagsorden (403 — ft.dk bot-blokerer også
    # Renders server-IP, så feedet returnerer aldrig indhold).
    # Fjernet (døde RSS, allerede dækket af SCRAPE_SOURCES): Miljøministeriet,
    # Kystdirektoratet, Energistyrelsen.
}

# ── JURA & ADVOKATER ──
# Formidlingen af ny miljø- og planretspraksis sker hos advokatkontorerne, ikke
# i pressen: den eneste offentlige gennemgang af Horsens II (MFKN 23/6-2026) var
# et LinkedIn-opslag fra Codex. Nævnenes egne afgørelser hentes af gruppen
# "Nævnsafgørelser" i main.py — det her er kommentarsporet ovenpå dem.
# Testet 7/8-2026 (kandidater uden fungerende feed står i kommentaren nedenfor):
RSS_JURA = {
    "Codex Advokater":          "https://codexlaw.dk/feed/",
    "Focus Advokater":          "https://focus-advokater.dk/feed/",
    "Plesner":                  "https://plesner.com/rss.xml",
    "Bruun & Hjejle":           "https://bruunhjejle.dk/rss.xml",
    # Uden RSS, men server-renderede nyhedslister → SCRAPE_SOURCES nedenfor:
    # Kromann Reumert, Poul Schmith (Kammeradvokaten).
    # HortenDahl (tidl. Horten) hentes fra deres eget Umbraco-API — se
    # fetch_hortendahl() i main.py. horten.dk selv er umuligt: Cloudflare
    # afviser TLS-handshaket for alt der ikke er en browser.
    # Kan IKKE hentes: Bech-Bruun (JS-renderet SPA, 585k tegn HTML uden en
    # eneste overskrift), Gorrissen Federspiel (HTTP 454 bot-blok), Njord
    # (rss.xml har ét item, "Forside", fra 2019), Accura (feedet indeholder kun
    # udnævnelser), Molt Wengel/Bird & Bird/WSCO/Sirius (intet feed).
}

# ── VIDENSKAB & FORSKNING ──
RSS_VIDENSKAB = {
    "Nature Climate Change":    "https://www.nature.com/nclimate.rss",
    "Nature Water":             "https://www.nature.com/natwater.rss",
    "Science Advances":         "https://advances.sciencemag.org/rss/current.xml",
    "Climatic Change":          "https://link.springer.com/search.rss?query=climate+adaptation&search-within=Journal&facet-journal-id=10584",
    "Urban Climate":            "https://rss.sciencedirect.com/publication/science/22120955",
    "Journal Water Research":   "https://rss.sciencedirect.com/publication/science/00431354",
    # Fjernet (døde RSS, dækket af SCRAPE_SOURCES: DTU Byg, KU SCIENCE, DCE
    # Aarhus): DTU Research, AU Forskning, KU Nyheder. Fjernet: Hydrology &
    # Earth Sci. (404, intet fungerende feed).
}

# ── BREDE SØGE-FEEDS (Bing News) ──
# Query-baserede RSS-feeds der fanger danske klimatilpasningshistorier på
# tværs af ALLE medier — også dem hvis egne RSS er nedlagt (Politiken, JP,
# Berlingske, KTC m.fl.). Bing News bruges frem for Google News, fordi Google
# låser locale på serverens egress-IP (Render → norsk) og ignorerer gl/ceid;
# Bing respekterer cc=dk&setlang=da&mkt=da-DK pålideligt. Bing News RSS forstår
# IKKE OR-operatoren, så hvert kernebegreb har sit eget feed. Æøå er %-encodet.
# Relevans-scoringen i main.py frasorterer støj.
# VIGTIGT: qft=interval="8" filtrerer til seneste måned. Uden den sorterer Bing
# på relevans og blander gamle artikler ind (helt tilbage til 2010) — så vi får
# AKTUELLE nyheder i stedet for et tidløst relevans-mix.
_BING = "https://www.bing.com/news/search?q={}&format=rss&cc=dk&setlang=da&mkt=da-DK&qft=interval%3d%228%22"
RSS_BREDE_SOEGNINGER = {
    "Bing News – klimatilpasning":   _BING.format("klimatilpasning"),
    "Bing News – skybrud":           _BING.format("skybrud"),
    "Bing News – kystbeskyttelse":   _BING.format("kystbeskyttelse"),
    "Bing News – stormflod":         _BING.format("stormflod"),
    "Bing News – oversvømmelse":     _BING.format("oversv%C3%B8mmelse"),
    "Bing News – regnvand":          _BING.format("regnvand"),
    "Bing News – grundvand":         _BING.format("grundvand"),
    "Bing News – klimasikring":      _BING.format("klimasikring"),
    "Bing News – klimatilpasningsplan": _BING.format("klimatilpasningsplan"),
    "Bing News – regnvandsbassin":   _BING.format("regnvandsbassin"),
    "Bing News – kloakseparering":   _BING.format("kloakseparering"),
    "Bing News – diger":             _BING.format("diger"),
    "Bing News – spildevand":        _BING.format("spildevand"),
    # ── Kommunalt fokus + smalle fagtermer (tilføjet juli 2026) ──
    # Lav volumen er forventet: de er fangnet der slår ud, NÅR noget sker.
    "Bing News – lokalplan klima":       _BING.format("lokalplan%20klima"),
    "Bing News – spildevandsplan":       _BING.format("spildevandsplan"),
    "Bing News – skybrudssikring":       _BING.format("skybrudssikring"),
    "Bing News – stormflodssikring":     _BING.format("stormflodssikring"),
    "Bing News – terrænnært grundvand":  _BING.format("terr%C3%A6nn%C3%A6rt%20grundvand"),
    "Bing News – lavbundsjord":          _BING.format("lavbundsjord"),
    "Bing News – vandløbsrestaurering":  _BING.format("vandl%C3%B8bsrestaurering"),
    "Bing News – klimatilpasning pulje": _BING.format("klimatilpasning%20pulje"),
}

# ── PODCASTS (RSS til nye episoder) ──
RSS_PODCASTS = {
    "Warm Regards (klima)":     "https://feeds.feedburner.com/WarmRegardsPodcast",
    # Fjernet (døde/placeholder-RSS): Vandkanten (DNNK) (dummy-ID), Hav og
    # himmel (DMI), The Water Values, Sustainability Defined, Drilled (alle
    # 404 — feeds nedlagt/flyttet).
}

ALLE_FEEDS = {
    "Brede søgninger":          RSS_BREDE_SOEGNINGER,
    "Nyheder & fagblade":       RSS_NEWS,
    "Vidensinstitutioner":      RSS_VIDEN,
    "Rådgivere":                RSS_RAADGIVERE,
    "Forsyninger":              RSS_FORSYNINGER_RSS,
    "Nordiske naboer":          RSS_NORDEN,
    "EU projekter":             RSS_EU,
    "Platforme & netværk":      RSS_PLATFORME,
    "Internationale inst.":     RSS_INTERNATIONAL,
    "Vandkredsløb & grundvand": RSS_VAND,
    "Int. vandmyndigheder":     RSS_VAND_INT,
    "Kreative vinkler":         RSS_KREATIVT,
    "Lovgivning & politik":     RSS_LOVGIVNING,
    "Jura & advokater":         RSS_JURA,
    "Videnskab & forskning":    RSS_VIDENSKAB,
    "Podcasts":                 RSS_PODCASTS,
}

ALL_FEEDS_FLAT = {}
for gruppe, feeds in ALLE_FEEDS.items():
    for navn, url in feeds.items():
        ALL_FEEDS_FLAT[navn] = {"url": url, "gruppe": gruppe}

# ─────────────────────────────────────────────────────────────
# SCRAPING — kommuner, forsyninger, styrelser, ministerier
# ─────────────────────────────────────────────────────────────

SCRAPE_SOURCES = {

    # ── VIDENSINSTITUTIONER ──
    "DNNK":                             {"url": "https://www.dnnk.dk/nyheder/", "gruppe": "Vidensinstitutioner"},
    "CONCITO":                          {"url": "https://concito.dk/nyheder", "gruppe": "Vidensinstitutioner"},
    "klimamonitor.dk":                  {"url": "https://klimamonitor.dk/nyheder/klimatilpasning", "gruppe": "Vidensinstitutioner"},
    "DTU Byg":                          {"url": "https://www.byg.dtu.dk/nyheder", "gruppe": "Vidensinstitutioner"},
    "KU SCIENCE":                       {"url": "https://science.ku.dk/presse/nyheder/", "gruppe": "Vidensinstitutioner"},
    "DCE Aarhus Univ.":                 {"url": "https://dce.au.dk/aktuelt/nyheder", "gruppe": "Vidensinstitutioner"},
    # Fjernet 14/9-2026: GEUS. Den gamle sti (/om-geus/nyt-og-presse/nyheder/)
    # er 404 efter en omlægning, og efterfølgeren /om-geus/nyheder er kun en
    # hub-side — selve nyhedsarkivet er JS-renderet, så rå HTML giver 0
    # overskrifter. GEUS udgiver klimatilpasningsstof (fx "Klimatilpasning og
    # naturgenopretning kan flytte forureningsfaner", aug. 2026), så kilden er
    # værd at genbesøge hvis de får RSS eller server-renderer arkivet igen.
    "DHI":                              {"url": "https://www.dhigroup.com/news", "gruppe": "Vidensinstitutioner"},
    "Teknologisk Institut":             {"url": "https://www.teknologisk.dk/nyheder/", "gruppe": "Vidensinstitutioner"},
    "DMI":                              {"url": "https://www.dmi.dk/nyheder", "gruppe": "Vidensinstitutioner"},
    # IDA, KTC, HOFOR, SLA kan IKKE scrapes: nyhedslisterne er JavaScript-
    # renderede SPA'er (server-HTML har kun navigation), IDA/nyheder er en
    # soft-404, SLA er 403 bot-blokeret. Kræver headless browser. De dækkes
    # i stedet af de brede Bing-feeds. Kun DMI server-renderer og virker.

    # ── KTC-NETVÆRK (faglige kollegiale netværk, ikke nyhedslister) ──
    # KTC's egne NYHEDSLISTER er JS-renderede (se ovenfor), men netværks- og
    # faggruppesiderne er server-renderede med <article>-indslag og offentligt
    # synligt indhold ("Alle kan se netværkets indhold"). De var aldrig med som
    # kilde, og de kunne heller ikke scrapes: KTC's tema pakker hele siden i ét
    # <header>, som scraperen fjernede — derfor fallbacket i scrape_news.
    # Indholdet er kommunale sagsbehandleres spørgsmål/svar — praksisnær viden
    # der ikke findes i nogen nyhedsstrøm.
    "KTC Kystnetværk Sjælland":         {"url": "https://www.ktc.dk/netvaerk/netvaerk-kystbeskyttelse-region-sjaelland", "gruppe": "Platforme & netværk"},

    # ── GRUNDVAND & VANDKREDSLØB ──
    # Fjernet 14/9-2026: GEUS Grundvand (hele /vores-viden/vand/* er nedlagt;
    # grundvand ligger nu under /vandressourcer uden nyhedssektion), Vand i Byer
    # (domænet er nu en SEO-indholdsfarm — se noten i RSS_VIDEN) og Den Danske
    # Vandklynge (vandklynge.dk har intet DNS-opslag længere).
    "Naturstyrelsen Vand":              {"url": "https://naturstyrelsen.dk/nyheder/?tema=vand", "gruppe": "Vandkredsløb & grundvand"},
    "Aarhus Vand Innovation":           {"url": "https://aarhusvand.dk/nyheder/", "gruppe": "Vandkredsløb & grundvand"},
    "VandCenter Syd Innovation":        {"url": "https://vandcenter.dk/nyheder/", "gruppe": "Vandkredsløb & grundvand"},

    # ── LOVGIVNING & HØRINGER ──
    # Høringer hentes nu via Høringsportalens Atom-feed (se RSS_LOVGIVNING).
    # Fjernet 14/9-2026: Miljøministeriet Høringer (mim.dk/horinger = 404) og
    # Høringsportalens HTML-liste (Angular-SPA uden server-renderet indhold).
    "Klimarådet":                       {"url": "https://klimaraadet.dk/da/foelg-med-i-det-seneste-fra-klimaraadet", "gruppe": "Lovgivning"},
    "Forsyningstilsynet":               {"url": "https://forsyningstilsynet.dk/nyheder/", "gruppe": "Lovgivning"},
    # Fjernet 14/9-2026: Kystdirektoratet og Miljøstyrelsen. Kystdirektoratet er
    # fusioneret ind i Miljøstyrelsen, og kyst.dk/nyheder/ redirecter til en
    # 404. Miljøstyrelsens egen nyhedsside er Next.js og renderes client-side:
    # 456 kB rå HTML uden et eneste artikel-link. Begge kræver headless browser.
    # Konsekvens: der er pt. INGEN direkte kilde til Kystdirektoratets nyheder —
    # kystfagligt stof må komme fra Bing-feedet "kystbeskyttelse" og fra KTC's
    # kystnetværk. Det er et reelt hul, ikke en bevidst nedprioritering.

    # ── KREATIVE VINKLER ──
    "Realdania Projekter":              {"url": "https://realdania.dk/projekter/", "gruppe": "Kreative vinkler"},
    "Tredje Natur Blog":                {"url": "https://tredjenatur.dk/blog/", "gruppe": "Kreative vinkler"},
    "SLA Arkitekter":                   {"url": "https://www.sla.dk/nyheder/", "gruppe": "Kreative vinkler"},
    # GHB Landskabsarkitekter hedder nu LYTT Architecture — ghb-landskab.dk
    # 301'er til lytt.dk. Navnet står med begge former, så gamle artikler stadig
    # kan genkendes. NB: overskrifterne er i rå HTML, men datoer vises kun
    # sporadisk, så dato-parsing bliver svag for denne kilde.
    "LYTT (tidl. GHB Landskab)":        {"url": "https://www.lytt.dk/aktuelt", "gruppe": "Kreative vinkler"},
    "BLOXHUB":                          {"url": "https://bloxhub.org/news/", "gruppe": "Kreative vinkler"},
    # Fjernet 14/9-2026: Schønherr Landskab. Sitet er relanceret på Webflow helt
    # uden nyhedssektion — /aktuelt, /nyheder, /news, /journal, /stories,
    # /insights og /press giver alle 404, og der findes ingen oversigtsside.
    "Klimatorium":                      {"url": "https://klimatorium.dk/nyheder/", "gruppe": "Kreative vinkler"},

    # ── RÅDGIVERE ──
    "Rambøll DK":                       {"url": "https://ramboll.com/da-dk/nyheder", "gruppe": "Rådgivere"},
    # Fjernet 14/9-2026: COWI DK. /da/nyheder er 404, og efterfølgeren
    # /news-and-press/news/ er en tom SPA-skal (<div id="news-app">). COWI har
    # hverken RSS eller sitemap, men nyhederne ligger i et åbent JSON-API:
    # /api/news/GetNews?id=d8673f9b-cb9a-43c7-8c19-a81e81b33619
    #   &region=ae4218c7-4ca9-4081-a4aa-862965bcc6ee&pageNumber=1&pageSize=20
    # Kan hentes ind igen med samme mønster som fetch_hortendahl() i main.py.
    "Niras DK":                         {"url": "https://www.niras.dk/nyheder/", "gruppe": "Rådgivere"},
    "Sweco DK":                         {"url": "https://www.sweco.dk/nyheder/", "gruppe": "Rådgivere"},
    "Orbicon|WSP":                      {"url": "https://www.wsp.com/da-dk/nyheder", "gruppe": "Rådgivere"},
    "Krüger":                           {"url": "https://www.kruger.dk/nyheder/", "gruppe": "Rådgivere"},
    "MOE":                              {"url": "https://moe.dk/nyheder/", "gruppe": "Rådgivere"},
    "Watertech":                        {"url": "https://watertech.dk/nyheder/", "gruppe": "Rådgivere"},
    "EnviDan":                          {"url": "https://envidan.dk/nyheder/", "gruppe": "Rådgivere"},
    # Scalgo blogger kun på engelsk sti; /da-DK/blog giver 404.
    "Scalgo":                           {"url": "https://scalgo.com/en-US/blog", "gruppe": "Rådgivere"},
    # Fjernet 14/9-2026: GEO (flyttet til RSS_RAADGIVERE — HTML-listen er
    # AngularJS-renderet, men RSS virker), SmartBrønd (sitet lever, men har
    # ingen nyhedssektion overhovedet — kun Løsninger/Cases/Om/Kontakt) og
    # Nordiq Group (nordiqgroup.dk har intet DNS-opslag længere).
    "Forsikring & Pension":             {"url": "https://www.forsikringogpension.dk/nyheder/", "gruppe": "Rådgivere"},

    # ── JURA & ADVOKATER (uden RSS — resten ligger i RSS_JURA) ──
    # Begge har server-renderede nyhedslister. De gav 0 artikler indtil
    # kandidat-udvælgelsen i main.py blev rettet: Kromann Reumert pakker hele
    # siden i ét <article>, og Poul Schmith bruger <div class="title"> i stedet
    # for overskrifts-tags. Verificeret 7/8-2026: 19 hhv. 25 titler udtrækkes.
    "Kromann Reumert":                  {"url": "https://kromannreumert.com/nyheder", "gruppe": "Jura & advokater"},
    "Poul Schmith":                     {"url": "https://poulschmith.dk/nyheder/", "gruppe": "Jura & advokater"},

    # ── MINISTERIER ──
    "Miljøministeriet":                 {"url": "https://www.mim.dk/nyheder/", "gruppe": "Myndigheder"},
    "Klima- og Energiministeriet":      {"url": "https://kefm.dk/aktuelt/nyheder/", "gruppe": "Myndigheder"},
    "Indenrigsministeriet":             {"url": "https://www.im.dk/nyheder/", "gruppe": "Myndigheder"},

    # ── STYRELSER ──
    "Energistyrelsen":                  {"url": "https://ens.dk/presse/nyheder-og-pressemeddelelser", "gruppe": "Myndigheder"},
    "KL":                               {"url": "https://www.kl.dk/nyheder/", "gruppe": "Myndigheder"},
    "Naturstyrelsen":                   {"url": "https://naturstyrelsen.dk/nyheder/", "gruppe": "Myndigheder"},
    # brs.dk/da/nyheder/ svarer 200, men listen er JS-renderet. Forsiden har
    # derimod server-renderede teasere, så vi scraper den. Brug IKKE
    # www.beredskabsstyrelsen.dk — det domæne afviser forbindelsen helt.
    "Beredskabsstyrelsen":              {"url": "https://brs.dk/", "gruppe": "Myndigheder"},
    "Stormrådet":                       {"url": "https://www.stormraadet.dk/nyheder/", "gruppe": "Myndigheder"},
    "Vejdirektoratet":                  {"url": "https://www.vejdirektoratet.dk/nyheder", "gruppe": "Myndigheder"},
    "Styrelsen for Dataforsyning":      {"url": "https://sdfe.dk/nyheder/", "gruppe": "Myndigheder"},
    "Statens Byggeforskningsinstitut":  {"url": "https://sbi.dk/nyheder/", "gruppe": "Myndigheder"},

    # ── FORSYNINGER – Storkøbenhavn ──
    "HOFOR":                            {"url": "https://www.hofor.dk/om-hofor/presse-og-talspersoner/nyheder/", "gruppe": "Forsyninger"},
    "Nordvand":                         {"url": "https://nordvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Novafos":                          {"url": "https://novafos.dk/nyheder/", "gruppe": "Forsyninger"},
    "Frederiksberg Fors.":              {"url": "https://frb-forsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Hillerød Forsyning":               {"url": "https://hfors.dk/nyheder/", "gruppe": "Forsyninger"},
    "Køge Forsyning":                   {"url": "https://koegeforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Roskilde Forsyning":               {"url": "https://roskilde-forsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Greve Forsyning":                  {"url": "https://greveforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "BIOFOS":                           {"url": "https://www.biofos.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Jylland ──
    "Aarhus Vand":                      {"url": "https://aarhusvand.dk/nyheder/", "gruppe": "Forsyninger"},
    # Aalborg Forsyning har ikke længere en bred "nyheder"-sektion — kun presse.
    "Aalborg Forsyning":                {"url": "https://www.aalborgforsyning.dk/pressemeddelelser/", "gruppe": "Forsyninger"},
    "Silkeborg Forsyning":              {"url": "https://silkeborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Herning Vand":                     {"url": "https://herningvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Horsens Vand":                     {"url": "https://horsensvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Viborg Vand":                      {"url": "https://viborgvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Vejle Spildevand":                 {"url": "https://www.vejlespildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Kolding Spildevand":               {"url": "https://koldingspildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    # Navneskifte: sonderborgforsyning.dk 301'er til sonfor.dk.
    "SONFOR (tidl. Sønderborg Fors.)":  {"url": "https://sonfor.dk/nyheder/", "gruppe": "Forsyninger"},
    # Navneskifte: esbjergforsyning.dk 301'er til dinforsyning.dk (Esbjerg+Varde).
    # Listen navigerer med onclick i stedet for <a href>, så artikel-URL'en
    # udtrækkes af scrape_news' onclick-fallback.
    "DIN Forsyning (tidl. Esbjerg Fors.)": {"url": "https://www.dinforsyning.dk/da-dk/nyheder-1", "gruppe": "Forsyninger"},
    # Navneskifte: randersspildevand.dk 307'er til vmr.dk. Nyhedslisten er tastet
    # ind i en rich text-editor som skiftevis <p>dato</p><p><a>titel</a></p> og
    # har ingen artikel-containere — læses af _tekstblok_liste() i main.py.
    # Peger bevidst på /nyheder og ikke /presse/pressemeddelelsesarkiv: arkivet
    # er fyldt med 2020-stof, som ville fylde nyhedsstrømmen med gammelt indhold.
    "Vandmiljø Randers":                {"url": "https://www.vmr.dk/om-os/publikationer-og-nyheder/nyheder", "gruppe": "Forsyninger"},
    # Fjernet 14/9-2026: Hjørring Vandselskab — intet DNS-opslag på domænet.
    "Holstebro Vand":                   {"url": "https://holstebrovand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Lemvig Vand":                      {"url": "https://lemvigvand.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Fyn & Sjælland ──
    "VandCenter Syd":                   {"url": "https://vandcenter.dk/nyheder/", "gruppe": "Forsyninger"},
    "Danva":                            {"url": "https://www.danva.dk/nyheder/", "gruppe": "Forsyninger"},
    "Holbæk Forsyning":                 {"url": "https://holbaekforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Næstved Forsyning":                {"url": "https://naestvedforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Lolland Forsyning":                {"url": "https://lollandforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Bornholms Forsyning":              {"url": "https://bornholmsforsyning.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── KOMMUNER ──
    "Kbh. Kommune":                     {"url": "https://www.kk.dk/nyheder", "gruppe": "Kommuner"},
    "Aarhus Kommune":                   {"url": "https://www.aarhus.dk/nyheder/", "gruppe": "Kommuner"},
    "Odense Kommune":                   {"url": "https://www.odense.dk/nyheder", "gruppe": "Kommuner"},
    "Aalborg Kommune":                  {"url": "https://www.aalborg.dk/nyheder", "gruppe": "Kommuner"},
    "Frederiksberg":                    {"url": "https://www.frederiksberg.dk/nyheder", "gruppe": "Kommuner"},
    "Vejle Kommune":                    {"url": "https://www.vejle.dk/nyheder", "gruppe": "Kommuner"},
    "Roskilde Kommune":                 {"url": "https://roskilde.dk/nyheder", "gruppe": "Kommuner"},
    "Silkeborg Kommune":                {"url": "https://www.silkeborg.dk/nyheder", "gruppe": "Kommuner"},
    # Esbjerg Kommune udgiver via Ritzau. esbjerg.dk/om-kommunen/presserum er
    # kun en tom JS-embed, mens selve nyhedsrummet hos Ritzau er server-
    # renderet med overskrift + tidsstempel. Derfor peger vi paa Ritzau-URL'en,
    # selv om det er et tredjepartsdomaene — det ER kommunens officielle kanal.
    "Esbjerg Kommune":                  {"url": "https://via.ritzau.dk/nyhedsrum/esbjerg-kommune/r?publisherId=13560064", "gruppe": "Kommuner"},
    "Viborg Kommune":                   {"url": "https://viborg.dk/nyheder", "gruppe": "Kommuner"},
    "Sønderborg Kommune":               {"url": "https://www.sonderborg.dk/nyheder", "gruppe": "Kommuner"},
    "Ringkøbing-Skjern Kommune":        {"url": "https://www.rksk.dk/nyheder", "gruppe": "Kommuner"},
    "Bornholm Kommune":                 {"url": "https://www.brk.dk/nyheder", "gruppe": "Kommuner"},
    # Horsens henter selve listen med AJAX, men rå HTML har en schema.org
    # ItemList med 670 pressemeddelelser — den læses af _jsonld_liste() i
    # main.py. NB: ItemList bærer ingen datoer, så posterne kommer datoløse ind.
    "Horsens Kommune":                  {"url": "https://horsens.dk/omhorsenskommune/presse/pressemeddelelser", "gruppe": "Kommuner"},
    # Kolding bygger listen af <bui-web-card>, hvor overskrift og dato står i
    # HTML-ATTRIBUTTER (heading/tagline) i stedet for i elementteksten.
    "Kolding Kommune":                  {"url": "https://www.kolding.dk/om-kommunen/nyhedsarkiv", "gruppe": "Kommuner"},
    # Helsingør Kommune ligger i SITEMAP_SOURCES nedenfor: selve nyhedslisten
    # er en Blazor-app, men de enkelte artikelsider er server-renderede, og
    # sitemap.xml kender dem alle med dato.

    # ── NORDISKE NABOER (uden RSS) ──
    "Movium nyheder (SE)":              {"url": "https://movium.slu.se/nyheter/", "gruppe": "Nordiske naboer"},
    "Movium kalendarium (SE)":          {"url": "https://movium.slu.se/kalendarium/", "gruppe": "Nordiske naboer"},
}


# ─────────────────────────────────────────────────────────────
# SITEMAP-KILDER — sider hvor NYHEDSLISTEN kræver JavaScript,
# men de enkelte artikelsider er server-renderede
# ─────────────────────────────────────────────────────────────
# Nogle CMS'er (Blazor, React-SPA'er) bygger listen i browseren, så der er
# intet at scrape på oversigtssiden. Men artiklerne selv er almindelige,
# server-renderede sider, og sitemap.xml kender dem alle — med <lastmod> som
# dato. Så i stedet for en headless browser læses sitemap'et, de nyeste
# artikel-URL'er plukkes ud, og deres titel/manchet hentes fra siderne selv.
# Det koster SITEMAP_ANTAL ekstra sidehentninger pr. kilde (se main.py), som
# dæmpes af feed-cachen — til gengæld undgås en browser i stakken helt.
SITEMAP_SOURCES = {
    "Helsingør Kommune": {
        "sitemap": "https://www.helsingor.dk/sitemap.xml",
        # Kun denne sti er nyhedsartikler; /nyheder-og-fakta/ alene rammer også
        # kontakt- og oplysningssider.
        "moenster": "/nyheder-og-presse/nyheder/",
        "gruppe": "Kommuner",
    },
    # Kystdirektoratet er fusioneret ind i Miljøstyrelsen, og mst.dk/nyheder er
    # Next.js renderet client-side — 465 kB rå HTML uden ét artikel-link. Det
    # var DNNK's største kildehul, fordi kystfagligt stof ellers kun kom fra en
    # Bing-søgning. Sitemap'et kender 983 nyhedsartikler med dato, og de
    # enkelte artikelsider er server-renderede.
    "Miljøstyrelsen (inkl. Kystdirektoratet)": {
        "sitemap": "https://mst.dk/sitemap.xml",
        "moenster": "/nyheder/",
        "gruppe": "Lovgivning",
    },
}
