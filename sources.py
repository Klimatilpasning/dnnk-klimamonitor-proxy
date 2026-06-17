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
    "Vand i Byer":              "https://vandibyer.dk/feed/",
    "Klimatorium":              "https://klimatorium.dk/feed/",
    # Fjernet (døde RSS, flyttet til SCRAPE_SOURCES): IDA, DANVA, CONCITO, DMI.
}

# ── RÅDGIVERE ──
RSS_RAADGIVERE = {
    "Sweco":                    "https://www.sweco.dk/rss",
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
    "Climate-ADAPT":            "https://climate-adapt.eea.europa.eu/rss",
    "EEA Nyheder":              "https://www.eea.europa.eu/rss",
    "EU Kommissionen ENV":      "https://ec.europa.eu/environment/rss_en.xml",
    "EU Kommissionen Klima":    "https://ec.europa.eu/clima/rss_en.xml",
    "Copernicus Klima":         "https://climate.copernicus.eu/rss.xml",
    "JRC Science Hub":          "https://joint-research-centre.ec.europa.eu/rss.xml",
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
    "C40 Cities":               "https://www.c40.org/rss",
    "Deltares":                 "https://www.deltares.nl/rss",
    "IPCC":                     "https://www.ipcc.ch/news_and_events/rss.xml",
    "World Resources Inst.":    "https://www.wri.org/rss.xml",
    "The Nature Conservancy":   "https://www.nature.org/en-us/newsroom/rss-feeds/",
}

# ── VANDKREDSLØB & GRUNDVAND ──
RSS_VAND = {
    "NGWA Groundwater":         "https://www.ngwa.org/rss.xml",
    "H2O Waternetwerk (NL)":    "https://www.h2owaternetwerk.nl/rss.xml",
    "Water Research Fdn":       "https://www.waterrf.org/rss.xml",
    "IWA Water":                "https://iwa-network.org/feed/",
    "The Source (IWA)":         "https://iwa-network.org/the-source/feed/",
    "Stormwater Report":        "https://stormwaterreport.com/feed/",
    "Circle of Blue":           "https://www.circleofblue.org/feed/",
    "WaterWorld":               "https://www.waterworld.com/rss.xml",
    "Water & Wastewater Int.":  "https://www.waterworld.com/rss.xml",
}

# ── INT. VANDMYNDIGHEDER (NL, UK, US) ──
RSS_VAND_INT = {
    "Rijkswaterstaat (NL)":     "https://www.rijkswaterstaat.nl/rss.xml",
    "Env. Agency (UK)":         "https://www.gov.uk/search/news-and-communications.atom?organisations[]=environment-agency",
    "USGS Water":               "https://www.usgs.gov/rss.xml",
    "Dutch Water Authorities":  "https://www.uvw.nl/rss.xml",
    "KWR Water Research":       "https://www.kwrwater.nl/rss.xml",
}

# ── KREATIVE VINKLER: design, arkitektur, innovation ──
RSS_KREATIVT = {
    "Dezeen Arkitektur":        "https://www.dezeen.com/feed/",
    "ArchDaily":                "https://www.archdaily.com/feed",
    "Landscape Architecture":   "https://www.landscapearchitecturemagazine.org/feed/",
    "Landezine":                "https://landezine.com/feed/",
    "The Conversation Env.":    "https://theconversation.com/environment/articles.atom",
    "WEF Natur & Klima":        "https://www.weforum.org/agenda/feed/",
    "Fast Company Innov.":      "https://www.fastcompany.com/feed",
    # Fjernet (døde RSS, dækket af SCRAPE_SOURCES): Tredje Natur, SLA Arkitekter.
    "Citylab (Bloomberg)":      "https://www.bloomberg.com/feeds/bbiz/sitemap_index.xml",
    "Planetizen":               "https://www.planetizen.com/rss.xml",
}

# ── LOVGIVNING & POLITIK ──
RSS_LOVGIVNING = {
    "Folketing":                "https://www.ft.dk/da/aktuelt/nyheder/rss",
    "Folketing Dagsorden":      "https://www.ft.dk/da/aktuelt/kalender/rss",
    "Klimarådet":               "https://klimaraadet.dk/da/rss.xml",
    # Fjernet (døde RSS, allerede dækket af SCRAPE_SOURCES): Miljøministeriet,
    # Kystdirektoratet, Energistyrelsen.
}

# ── VIDENSKAB & FORSKNING ──
RSS_VIDENSKAB = {
    "Nature Climate Change":    "https://www.nature.com/nclimate.rss",
    "Nature Water":             "https://www.nature.com/natwater.rss",
    "Science Advances":         "https://advances.sciencemag.org/rss/current.xml",
    "Climatic Change":          "https://link.springer.com/search.rss?query=climate+adaptation&search-within=Journal&facet-journal-id=10584",
    "Hydrology & Earth Sci.":   "https://www.hydrol-earth-syst-sci.net/xml/rss2.xml",
    "Urban Climate":            "https://rss.sciencedirect.com/publication/science/22120955",
    "Journal Water Research":   "https://rss.sciencedirect.com/publication/science/00431354",
    # Fjernet (døde RSS, dækket af SCRAPE_SOURCES: DTU Byg, KU SCIENCE, DCE
    # Aarhus): DTU Research, AU Forskning, KU Nyheder.
}

# ── BREDE SØGE-FEEDS (Bing News) ──
# Query-baserede RSS-feeds der fanger danske klimatilpasningshistorier på
# tværs af ALLE medier — også dem hvis egne RSS er nedlagt (Politiken, JP,
# Berlingske, KTC m.fl.). Bing News bruges frem for Google News, fordi Google
# låser locale på serverens egress-IP (Render → norsk) og ignorerer gl/ceid;
# Bing respekterer cc=dk&setlang=da&mkt=da-DK pålideligt. Bing News RSS forstår
# IKKE OR-operatoren, så hvert kernebegreb har sit eget feed. Æøå er %-encodet.
# Relevans-scoringen i main.py frasorterer støj.
_BING = "https://www.bing.com/news/search?q={}&format=rss&cc=dk&setlang=da&mkt=da-DK"
RSS_BREDE_SOEGNINGER = {
    "Bing News – klimatilpasning":   _BING.format("klimatilpasning"),
    "Bing News – skybrud":           _BING.format("skybrud"),
    "Bing News – kystbeskyttelse":   _BING.format("kystbeskyttelse"),
    "Bing News – stormflod":         _BING.format("stormflod"),
    "Bing News – oversvømmelse":     _BING.format("oversv%C3%B8mmelse"),
    "Bing News – regnvand":          _BING.format("regnvand"),
    "Bing News – grundvand":         _BING.format("grundvand"),
    "Bing News – klimasikring":      _BING.format("klimasikring"),
}

# ── PODCASTS (RSS til nye episoder) ──
RSS_PODCASTS = {
    # Fjernet (døde/placeholder-RSS): "Vandkanten (DNNK)" (1234567.rss var en
    # dummy-ID) og "Hav og himmel (DMI)" (404 — feed findes ikke).
    "The Water Values":         "https://www.waterpolicygroup.com/feed/podcast/",
    "Sustainability Defined":   "https://feeds.buzzsprout.com/1086681.rss",
    "Warm Regards (klima)":     "https://feeds.feedburner.com/WarmRegardsPodcast",
    "Drilled (klima-journalisme)": "https://feeds.megaphone.fm/drilled",
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
    "KU SCIENCE":                       {"url": "https://science.ku.dk/nyheder/", "gruppe": "Vidensinstitutioner"},
    "GEUS":                             {"url": "https://www.geus.dk/om-geus/nyt-og-presse/nyheder/", "gruppe": "Vidensinstitutioner"},
    "DCE Aarhus Univ.":                 {"url": "https://dce.au.dk/nyheder/", "gruppe": "Vidensinstitutioner"},
    "DHI":                              {"url": "https://www.dhigroup.com/news", "gruppe": "Vidensinstitutioner"},
    "Teknologisk Institut":             {"url": "https://www.teknologisk.dk/nyheder/", "gruppe": "Vidensinstitutioner"},
    "DMI":                              {"url": "https://www.dmi.dk/nyheder", "gruppe": "Vidensinstitutioner"},
    "IDA":                              {"url": "https://ida.dk/nyheder", "gruppe": "Vidensinstitutioner"},
    "KTC":                              {"url": "https://www.ktc.dk/nyheder", "gruppe": "Vidensinstitutioner"},

    # ── GRUNDVAND & VANDKREDSLØB ──
    "GEUS Grundvand":                   {"url": "https://www.geus.dk/vores-viden/vand/grundvand/nyheder/", "gruppe": "Vandkredsløb & grundvand"},
    "Naturstyrelsen Vand":              {"url": "https://naturstyrelsen.dk/nyheder/?tema=vand", "gruppe": "Vandkredsløb & grundvand"},
    "Den Danske Vandklynge":            {"url": "https://vandklynge.dk/nyheder/", "gruppe": "Vandkredsløb & grundvand"},
    "Vand i Byer":                      {"url": "https://vandibyer.dk/nyheder/", "gruppe": "Vandkredsløb & grundvand"},
    "Aarhus Vand Innovation":           {"url": "https://aarhusvand.dk/nyheder/", "gruppe": "Vandkredsløb & grundvand"},
    "VandCenter Syd Innovation":        {"url": "https://vandcenter.dk/nyheder/", "gruppe": "Vandkredsløb & grundvand"},

    # ── LOVGIVNING & HØRINGER ──
    "Miljøministeriet Høringer":        {"url": "https://www.mim.dk/horinger/", "gruppe": "Lovgivning"},
    "Høringsportalen":                  {"url": "https://hoeringsportalen.dk/Hearing/List", "gruppe": "Lovgivning"},
    "Klimarådet":                       {"url": "https://klimaraadet.dk/da/nyheder", "gruppe": "Lovgivning"},
    "Forsyningstilsynet":               {"url": "https://forsyningstilsynet.dk/nyheder/", "gruppe": "Lovgivning"},
    "Miljøstyrelsen":                   {"url": "https://mst.dk/nyheder/", "gruppe": "Lovgivning"},
    "Kystdirektoratet":                 {"url": "https://kyst.dk/nyheder/", "gruppe": "Lovgivning"},

    # ── KREATIVE VINKLER ──
    "Realdania Projekter":              {"url": "https://realdania.dk/projekter/", "gruppe": "Kreative vinkler"},
    "Tredje Natur Blog":                {"url": "https://tredjenatur.dk/blog/", "gruppe": "Kreative vinkler"},
    "SLA Arkitekter":                   {"url": "https://www.sla.dk/nyheder/", "gruppe": "Kreative vinkler"},
    "Schønherr Landskab":               {"url": "https://schonherr.dk/nyheder/", "gruppe": "Kreative vinkler"},
    "GHB Landskab":                     {"url": "https://ghb-landskab.dk/nyheder/", "gruppe": "Kreative vinkler"},
    "BLOXHUB":                          {"url": "https://bloxhub.org/nyheder/", "gruppe": "Kreative vinkler"},
    "Klimatorium":                      {"url": "https://klimatorium.dk/nyheder/", "gruppe": "Kreative vinkler"},

    # ── RÅDGIVERE ──
    "Rambøll DK":                       {"url": "https://ramboll.com/da-dk/nyheder", "gruppe": "Rådgivere"},
    "COWI DK":                          {"url": "https://www.cowi.com/da/nyheder", "gruppe": "Rådgivere"},
    "Niras DK":                         {"url": "https://www.niras.dk/nyheder/", "gruppe": "Rådgivere"},
    "Sweco DK":                         {"url": "https://www.sweco.dk/nyheder/", "gruppe": "Rådgivere"},
    "Orbicon|WSP":                      {"url": "https://www.wsp.com/da-dk/nyheder", "gruppe": "Rådgivere"},
    "Krüger":                           {"url": "https://www.kruger.dk/nyheder/", "gruppe": "Rådgivere"},
    "MOE":                              {"url": "https://moe.dk/nyheder/", "gruppe": "Rådgivere"},
    "Watertech":                        {"url": "https://watertech.dk/nyheder/", "gruppe": "Rådgivere"},
    "EnviDan":                          {"url": "https://envidan.dk/nyheder/", "gruppe": "Rådgivere"},
    "GEO":                              {"url": "https://www.geo.dk/nyheder/", "gruppe": "Rådgivere"},
    "SmartBrønd":                       {"url": "https://smartbrond.dk/nyheder/", "gruppe": "Rådgivere"},
    "Scalgo":                           {"url": "https://scalgo.com/nyheder/", "gruppe": "Rådgivere"},
    "Nordiq Group":                     {"url": "https://nordiqgroup.dk/nyheder/", "gruppe": "Rådgivere"},
    "Forsikring & Pension":             {"url": "https://www.forsikringogpension.dk/nyheder/", "gruppe": "Rådgivere"},

    # ── MINISTERIER ──
    "Miljøministeriet":                 {"url": "https://www.mim.dk/nyheder/", "gruppe": "Myndigheder"},
    "Klima- og Energiministeriet":      {"url": "https://kefm.dk/aktuelt/nyheder/", "gruppe": "Myndigheder"},
    "Indenrigsministeriet":             {"url": "https://www.im.dk/nyheder/", "gruppe": "Myndigheder"},

    # ── STYRELSER ──
    "Energistyrelsen":                  {"url": "https://ens.dk/nyheder/", "gruppe": "Myndigheder"},
    "KL":                               {"url": "https://www.kl.dk/nyheder/", "gruppe": "Myndigheder"},
    "Naturstyrelsen":                   {"url": "https://naturstyrelsen.dk/nyheder/", "gruppe": "Myndigheder"},
    "Beredskabsstyrelsen":              {"url": "https://brs.dk/nyheder/", "gruppe": "Myndigheder"},
    "Stormrådet":                       {"url": "https://www.stormraadet.dk/nyheder/", "gruppe": "Myndigheder"},
    "Vejdirektoratet":                  {"url": "https://www.vejdirektoratet.dk/nyheder", "gruppe": "Myndigheder"},
    "Styrelsen for Dataforsyning":      {"url": "https://sdfe.dk/nyheder/", "gruppe": "Myndigheder"},
    "Statens Byggeforskningsinstitut":  {"url": "https://sbi.dk/nyheder/", "gruppe": "Myndigheder"},

    # ── FORSYNINGER – Storkøbenhavn ──
    "HOFOR":                            {"url": "https://www.hofor.dk/nyheder/", "gruppe": "Forsyninger"},
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
    "Aalborg Forsyning":                {"url": "https://www.aalborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Silkeborg Forsyning":              {"url": "https://silkeborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Herning Vand":                     {"url": "https://herningvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Horsens Vand":                     {"url": "https://horsensvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Viborg Vand":                      {"url": "https://viborgvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Esbjerg Forsyning":                {"url": "https://esbjergforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Vejle Spildevand":                 {"url": "https://www.vejlespildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Kolding Spildevand":               {"url": "https://koldingspildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Sønderborg Forsyning":             {"url": "https://sonderborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Hjørring Vandselskab":             {"url": "https://hjoerringvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Randers Spildevand":               {"url": "https://randersspildevand.dk/nyheder/", "gruppe": "Forsyninger"},
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
    "Horsens Kommune":                  {"url": "https://www.horsens.dk/nyheder", "gruppe": "Kommuner"},
    "Esbjerg Kommune":                  {"url": "https://www.esbjerg.dk/nyheder", "gruppe": "Kommuner"},
    "Viborg Kommune":                   {"url": "https://viborg.dk/nyheder", "gruppe": "Kommuner"},
    "Sønderborg Kommune":               {"url": "https://www.sonderborg.dk/nyheder", "gruppe": "Kommuner"},
    "Ringkøbing-Skjern Kommune":        {"url": "https://www.rksk.dk/nyheder", "gruppe": "Kommuner"},
    "Helsingør Kommune":                {"url": "https://www.helsingor.dk/nyheder", "gruppe": "Kommuner"},
    "Kolding Kommune":                  {"url": "https://www.kolding.dk/nyheder", "gruppe": "Kommuner"},
    "Bornholm Kommune":                 {"url": "https://www.brk.dk/nyheder", "gruppe": "Kommuner"},

    # ── NORDISKE NABOER (uden RSS) ──
    "Movium nyheder (SE)":              {"url": "https://movium.slu.se/nyheter/", "gruppe": "Nordiske naboer"},
    "Movium kalendarium (SE)":          {"url": "https://movium.slu.se/kalendarium/", "gruppe": "Nordiske naboer"},
}