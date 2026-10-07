# ─────────────────────────────────────────────────────────────
# DNNK Overvågningskilder
# ─────────────────────────────────────────────────────────────

# ── NYHEDER & FAGBLADE ──
RSS_NEWS = {
    "Ingeniøren":               "https://ing.dk/rss",
    # Ingeniørens emnefeeds (tilføjet 7/10-2026): "Klimatilpasning" (term 393)
    # og "Kystbeskyttelse" (974) gav 7 af 9 hhv. kyst-/stormflodsartikler, som
    # ikke er tagget 393. "Energi & Miljø" (term 1964) er fjernet: 0 af 25
    # relevante på en måned, kun energi og mitigation.
    "Ingeniøren Klimatilpasning":   "https://ing.dk/term/rss/393",
    "Ingeniøren Kystbeskyttelse":   "https://ing.dk/term/rss/974",
    "Altinget Miljø":           "https://www.altinget.dk/miljoe/rss.aspx",
    # Altinget Klima har klimatilpasningsdebat, som Miljø-sektionen ikke har.
    # Krydspostninger har forskellig sektions-URL - se dedup i get_news_full.
    "Altinget Klima":           "https://www.altinget.dk/klima/rss.aspx",
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
    # Herning Vand: HTML-listen gav 0 titler, men WordPress-feedet på
    # nyhedsstien virker (selve /feed/ er tomt). Lav klimatilpasningsværdi -
    # mest drift - men det genopretter forsyningsdækningen.
    "Herning Vand":             "https://herningvand.dk/nyheder/feed/",
    # viborgvand.dk har intet DNS-opslag længere; forsyningen er en del af
    # Energi Viborg. Mest el og varme, men bedre end en død kilde.
    "Energi Viborg (tidl. Viborg Vand)": "https://www.energiviborg.dk/nyheder/feed/",
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
    # Fjernet 7/10-2026 (STILLESTÅENDE i check_sources.py): FloodList - nyeste
    # item 2024-06-03 - og UN Environment - nyeste item 2024-02-22. Feedsene
    # svarer med items, så de så sunde ud, men har stået stille i over et år.
    "ICLEI":                    "https://iclei.org/news/rss/",
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
    # Ny feed-URL 7/10-2026 (den gamle gav 403). Kun kosmetisk: 0 af 83 items
    # består relevansfilteret, og science.org ligger bag Cloudflare. Får Render
    # 403 eller en udfordringsside, så fjern kilden frem for at bygge en omvej.
    "Science Advances":         "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=sciadv",
    "Climatic Change":          "https://link.springer.com/search.rss?query=climate+adaptation&search-within=Journal&facet-journal-id=10584",
    "Urban Climate":            "https://rss.sciencedirect.com/publication/science/22120955",
    "Journal Water Research":   "https://rss.sciencedirect.com/publication/science/00431354",
    # Fjernet (døde RSS, dækket af SCRAPE_SOURCES: KU SCIENCE, DCE Aarhus):
    # DTU Research, AU Forskning, KU Nyheder. Fjernet: Hydrology & Earth Sci.
    # (404, intet fungerende feed). KENDT HUL: efter at DTU Byg blev fjernet
    # 7/10-2026 (se SCRAPE_SOURCES) har monitoren ingen DTU-dækning.
}

# ── BREDE SØGE-FEEDS (Bing News) ──
# Query-baserede RSS-feeds der fanger danske klimatilpasningshistorier på
# tværs af ALLE medier — også dem hvis egne RSS er nedlagt (Politiken, JP,
# Berlingske, KTC m.fl.). Bing News bruges frem for Google News, fordi Google
# låser locale på serverens egress-IP (Render → norsk) og ignorerer gl/ceid;
# Bing respekterer cc=dk&setlang=da&mkt=da-DK pålideligt. Bing News RSS forstår
# IKKE OR-operatoren, så hvert kernebegreb har sit eget feed. Æøå er %-encodet.
# Relevans-scoringen i main.py frasorterer støj.
# VIGTIGT: qft=interval filtrerer på alder. Uden den sorterer Bing på relevans
# og blander gamle artikler ind (helt tilbage til 2010). Værdierne er:
# "7" = 24 timer, "8" = 7 DAGE, "9" = 30 dage. (Her stod tidligere, at "8" var
# en måned - det var forkert, målt på datoerne 5.-6/10-2026.)
# Bing giver højst ca. 14 items pr. feed, så de brede termer med mange nyheder
# bruger 7 dage (ellers fortrænges dagens nyheder), mens de smalle fagtermer,
# der ofte gav 0, bruger 30 dage. count=50 hæver Bings standardloft lidt.
_BING_7D = "https://www.bing.com/news/search?q={}&format=rss&cc=dk&setlang=da&mkt=da-DK&qft=interval%3d%228%22&count=50"
_BING_30D = "https://www.bing.com/news/search?q={}&format=rss&cc=dk&setlang=da&mkt=da-DK&qft=interval%3d%229%22&count=50"
RSS_BREDE_SOEGNINGER = {
    # ── Brede termer: seneste 7 dage ──
    "Bing News – klimatilpasning":   _BING_7D.format("klimatilpasning"),
    "Bing News – skybrud":           _BING_7D.format("skybrud"),
    "Bing News – stormflod":         _BING_7D.format("stormflod"),
    "Bing News – oversvømmelse":     _BING_7D.format("oversv%C3%B8mmelse"),
    "Bing News – regnvand":          _BING_7D.format("regnvand"),
    "Bing News – grundvand":         _BING_7D.format("grundvand"),
    "Bing News – spildevand":        _BING_7D.format("spildevand"),
    # ── Smalle fagtermer: seneste 30 dage ──
    "Bing News – kystbeskyttelse":   _BING_30D.format("kystbeskyttelse"),
    "Bing News – kystsikring":       _BING_30D.format("kystsikring"),
    "Bing News – klimasikring":      _BING_30D.format("klimasikring"),
    "Bing News – klimatilpasningsplan": _BING_30D.format("klimatilpasningsplan"),
    "Bing News – regnvandsbassin":   _BING_30D.format("regnvandsbassin"),
    "Bing News – kloakseparering":   _BING_30D.format("kloakseparering"),
    # "diger" erstattet af "dige" 7/10-2026: Bing læste "diger" som tyrkisk
    # "diğer" (= andre) og gav 11-12 items om alt andet, 0 beholdt - også fra
    # Render. "dige" gav 10 danske items, hvoraf halvdelen nævner termen.
    "Bing News – dige":              _BING_30D.format("dige"),
    # ── Kommunalt fokus + smalle fagtermer (tilføjet juli 2026) ──
    # Lav volumen er forventet: de er fangnet der slår ud, NÅR noget sker.
    # Tomme feeds koster kun ét cachet kald og laver ingen støj.
    "Bing News – lokalplan klima":       _BING_30D.format("lokalplan%20klima"),
    "Bing News – spildevandsplan":       _BING_30D.format("spildevandsplan"),
    "Bing News – skybrudssikring":       _BING_30D.format("skybrudssikring"),
    "Bing News – stormflodssikring":     _BING_30D.format("stormflodssikring"),
    "Bing News – terrænnært grundvand":  _BING_30D.format("terr%C3%A6nn%C3%A6rt%20grundvand"),
    "Bing News – lavbundsjord":          _BING_30D.format("lavbundsjord"),
    "Bing News – vandløbsrestaurering":  _BING_30D.format("vandl%C3%B8bsrestaurering"),
    "Bing News – klimatilpasning pulje": _BING_30D.format("klimatilpasning%20pulje"),
}

# ── PODCASTS (RSS til nye episoder) ──
RSS_PODCASTS = {
    # Fjernet 7/10-2026: Warm Regards - nyeste episode 2023-12-10 (STILLESTÅENDE).
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
    # Fjernet 7/10-2026: DTU Byg. Lagt sammen i DTU Construct (engelsk), og
    # construct.dtu.dk/ og /newslist giver 0 artikler med scrape_news, så der
    # er ingen erstatning. Værd at lede efter et API eller sitemap bag dtu.dk.
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
    "Aarhus Vand Innovation":           {"url": "https://aarhusvand.dk/nyheder/", "gruppe": "Vandkredsløb & grundvand"},
    # VandCenter Syd (både "Innovation" og den almindelige post) og Naturstyrelsen
    # hentes nu via SITEMAP_SOURCES - listerne her gav 0 titler.

    # ── LOVGIVNING & HØRINGER ──
    # Høringer hentes nu via Høringsportalens Atom-feed (se RSS_LOVGIVNING).
    # Fjernet 14/9-2026: Miljøministeriet Høringer (mim.dk/horinger = 404) og
    # Høringsportalens HTML-liste (Angular-SPA uden server-renderet indhold).
    # Gruppen hed før "Lovgivning", som ingen filterknap i frontenden matchede.
    "Klimarådet":                       {"url": "https://klimaraadet.dk/da/foelg-med-i-det-seneste-fra-klimaraadet", "gruppe": "Lovgivning & politik"},
    # Fjernet 7/10-2026: Forsyningstilsynet. Ingen vandemner i 571 nyheder
    # siden 2019 - det er indholdet, ikke HTTP-status, der afgør det.
    # Fjernet 14/9-2026: Kystdirektoratet og Miljøstyrelsen. Kystdirektoratet er
    # fusioneret ind i Miljøstyrelsen, og kyst.dk/nyheder/ redirecter til en
    # 404. Miljøstyrelsens egen nyhedsside er Next.js og renderes client-side:
    # 456 kB rå HTML uden et eneste artikel-link. Begge kræver headless browser.
    # Konsekvens: der er pt. INGEN direkte kilde til Kystdirektoratets nyheder —
    # kystfagligt stof må komme fra Bing-feedet "kystbeskyttelse" og fra KTC's
    # kystnetværk. Det er et reelt hul, ikke en bevidst nedprioritering.

    # ── KREATIVE VINKLER ──
    "Realdania Projekter":              {"url": "https://realdania.dk/projekter/", "gruppe": "Kreative vinkler"},
    # Fjernet 7/10-2026: Tredje Natur. Omdøbt til Third Nature Architects
    # (thirdnaturearchitects.com/news, engelsk). Listen er server-renderet, men
    # titlerne står i <a class="news-header">, som scraperen ikke læser, og
    # volumen er 3-5 nyheder om året - det står ikke mål med en særregel.
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
    # Fjernet 7/10-2026: Watertech. Overtaget af NIRAS; domænet sender 301 til
    # niras.dk, og certifikatet er udstedt til et fremmed domæne.
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
    # brs.dk/da/nyheder/ svarer 200, men listen er JS-renderet. Forsiden har
    # derimod server-renderede teasere, så vi scraper den. Brug IKKE
    # www.beredskabsstyrelsen.dk — det domæne afviser forbindelsen helt.
    "Beredskabsstyrelsen":              {"url": "https://brs.dk/", "gruppe": "Myndigheder"},
    # Stormrådet hedder nu Naturskaderådet, og Styrelsen for Dataforsyning er
    # nu Klimadatastyrelsen - begge hentes via SITEMAP_SOURCES.
    # Fjernet 7/10-2026: Vejdirektoratet. 0 klimatilpasningstitler. Hvis den
    # skal tilbage: Next.js-siden har et åbent Drupal JSON:API på
    # api.vejdirektoratet.dk.
    "Statens Byggeforskningsinstitut":  {"url": "https://sbi.dk/nyheder/", "gruppe": "Myndigheder"},

    # ── FORSYNINGER – Storkøbenhavn ──
    "HOFOR":                            {"url": "https://www.hofor.dk/om-hofor/presse-og-talspersoner/nyheder/", "gruppe": "Forsyninger"},
    # Fjernet 7/10-2026: Nordvand. Domænet sender videre til Novafos' forside
    # (0 artikler), og Novafos er allerede kilde.
    "Novafos":                          {"url": "https://novafos.dk/nyheder/", "gruppe": "Forsyninger"},
    "Frederiksberg Fors.":              {"url": "https://frb-forsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Hillerød Forsyning":               {"url": "https://hfors.dk/nyheder/", "gruppe": "Forsyninger"},
    # Fusioner (7/10-2026): Køge og Greve Forsyning er nu KLAR Forsyning, og
    # Roskilde og Holbæk Forsyning er nu Fors. De gamle domæner har intet
    # DNS-opslag eller nulstiller forbindelsen.
    "KLAR Forsyning (Køge/Greve/Solrød/Stevns)": {"url": "https://klarforsyning.dk/nyheder", "gruppe": "Forsyninger"},
    "Fors (Holbæk/Roskilde/Lejre)":     {"url": "https://www.fors.dk/nyheder/", "gruppe": "Forsyninger"},
    "BIOFOS":                           {"url": "https://www.biofos.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Jylland ──
    "Aarhus Vand":                      {"url": "https://aarhusvand.dk/nyheder/", "gruppe": "Forsyninger"},
    # Aalborg Forsyning har ikke længere en bred "nyheder"-sektion — kun presse.
    "Aalborg Forsyning":                {"url": "https://www.aalborgforsyning.dk/pressemeddelelser/", "gruppe": "Forsyninger"},
    "Silkeborg Forsyning":              {"url": "https://silkeborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    # Herning Vand og Energi Viborg (tidl. Viborg Vand) hentes nu via RSS -
    # se RSS_FORSYNINGER_RSS.
    "Horsens Vand":                     {"url": "https://horsensvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Vejle Spildevand":                 {"url": "https://www.vejlespildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    # Kolding Spildevand hedder nu BlueKolding - se SITEMAP_SOURCES.
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
    # holstebrovand.dk har intet DNS-opslag; forsyningen hedder nu Vestforsyning.
    # Brug HTML-listen, ikke sitemap'et: det koster 13 kald og gav 0 artikler.
    "Vestforsyning (tidl. Holstebro Vand)": {"url": "https://www.vestforsyning.dk/nyheder/nyheder/", "gruppe": "Forsyninger"},
    # Fjernet 7/10-2026: Lemvig Vand. lemvigvand.dk er en parkeret Dandomain-
    # side. Lemvig Vand A/S (CVR 32832296) findes, men hjemmesiden er ukendt -
    # efterfølgeren skal findes manuelt, fx ved at spørge Lemvig Kommune.

    # ── FORSYNINGER – Fyn & Sjælland ──
    "Danva":                            {"url": "https://www.danva.dk/nyheder/", "gruppe": "Forsyninger"},
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
        # Var "Lovgivning", som ingen filterknap matchede - kystkilden kunne
        # kun ses under "Alle".
        "gruppe": "Myndigheder",
    },
    # ── Tilføjet 7/10-2026. Alle bruger sidens egen udgivelsesdato, fordi
    # lastmod er redigeringsdatoen (se main.py ved SITEMAP_ANTAL). ──
    # Den nationale klimatilpasningsportal manglede helt. Nyhedslisten er JS,
    # artikelsiderne har <time datetime>. Titlerne rammer ofte kun brede ord
    # ("... gennem fysisk planlægning"), men kilden er per definition på feltet.
    "Klimatilpasning.dk": {
        "sitemap": "https://klimatilpasning.dk/sitemap.xml",
        "moenster": "/nyheder/20",
        "dato_fra_side": True,
        "altid_relevant": True,
        "antal": 6,
        "gruppe": "Myndigheder",
    },
    # sdfe.dk sender 301 til Klimadatastyrelsens 404-side, og listen er JS.
    # 222 nyheder har lastmod fra en migrering i 2022, så datoen tages fra
    # "Publiceret DD-MM-YYYY" på siden. Via Ritzau-RSS (publisherId=13561073)
    # er fravalgt: kun sjældne pressemeddelelser. NB: DMI og Klimadatastyrelsen
    # sammenlægges (nyhed 1/9-2026) - genbesøg både denne kilde og DMI-scrapen,
    # når den nye styrelse får eget site.
    "Klimadatastyrelsen (tidl. SDFE)": {
        "sitemap": "https://www.klimadatastyrelsen.dk/Handlers/Sitemap.ashx",
        "moenster": "/nyheder/nyhedsarkiv/20",
        "dato_regex": r'class="date">\s*Publiceret\s+(\d{2}-\d{2}-\d{4})',
        "antal": 8,
        "gruppe": "Myndigheder",
    },
    # stormraadet.dk sender videre til naturskaderaadet.dk. Kun /nyheder/:
    # hele pressemeddelelsesarkivet (2011-2024) har lastmod fra migreringen
    # 2026-07-10 og ville se nyt ud. Datoen står i URL'en (/20260720-...).
    # robots.txt beder om Crawl-delay 10 - artikelcachen (6 t) holder kaldene få.
    "Naturskaderådet": {
        "sitemap": "https://naturskaderaadet.dk/sitemap",
        "moenster": "/nyheder/20",
        "dato_fra_url": True,
        "antal": 6,
        "gruppe": "Myndigheder",
    },
    "VandCenter Syd": {
        "sitemap": "https://www.vandcenter.dk/xml-sitemap/",
        "moenster": "/nyheder/",
        # <p class="text-theme-grey-300 text-sm">21. august 2026</p>
        "dato_css": "p.text-theme-grey-300",
        "antal": 8,
        "gruppe": "Forsyninger",
    },
    # Kolding Spildevand hedder nu BlueKolding. Skråstregen til sidst undgår
    # en 301. Selve oversigtssiden /nws/ springes over af fetch_sitemap_news.
    "BlueKolding (tidl. Kolding Spildevand)": {
        "sitemap": "https://bluekolding.dk/nws-sitemap.xml/",
        "moenster": "/nws/",
        "antal": 6,
        "gruppe": "Forsyninger",
    },
    # Mest skov og natur, men lavbunds- og vådområdenyheder kommer med ved
    # bredere søgninger. Lokale nyheder (/kontakt-os-lokalt/lokale-nyheder/)
    # er bevidst ikke med: 89 indlæg på 120 dage, næsten kun skovdrift og events.
    "Naturstyrelsen": {
        "sitemap": "https://naturstyrelsen.dk/sitemap.xml",
        "moenster": "/nyheder/20",
        "antal": 10,
        "gruppe": "Myndigheder",
    },
}
