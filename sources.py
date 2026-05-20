# ─────────────────────────────────────────────────────────────
# DNNK Overvågningskilder
# ─────────────────────────────────────────────────────────────

# ── BEKRÆFTEDE RSS FEEDS ──
RSS_NEWS = {
    "Ingeniøren":               "https://ing.dk/rss",
    "Ingeniøren Energi & Miljø":"https://ing.dk/term/rss/1964",
    "Altinget Miljø":           "https://www.altinget.dk/miljoe/rss.aspx",
    "Altinget Plan & Byg":      "https://www.altinget.dk/plan/rss.aspx",
    "DR Nyheder":               "https://www.dr.dk/nyheder/service/feeds/allenyheder",
    "Politiken Klima":          "https://politiken.dk/rss/sektion/klima/",
    "Jyllands-Posten Klima":    "https://jyllands-posten.dk/rss/klima/",
    "Berlingske Viden":         "https://www.berlingske.dk/rss/viden",
    "Børsen":                   "https://borsen.dk/rss",
    "KTC Nyt":                  "https://www.ktc.dk/nyt/rss",
}

RSS_VIDEN = {
    "IDA":                      "https://ida.dk/rss",
    "DANVA":                    "https://www.danva.dk/rss",
    "Vand i Byer":              "https://vandibyer.dk/feed/",
    "Klimatorium":              "https://klimatorium.dk/feed/",
    "CONCITO":                  "https://concito.dk/rss",
    "DMI":                      "https://www.dmi.dk/rss",
}

RSS_RAADGIVERE = {
    "Sweco":                    "https://www.sweco.dk/rss",
    "Rambøll":                  "https://ramboll.com/rss",
    "COWI":                     "https://www.cowi.com/rss",
    "Niras":                    "https://www.niras.dk/rss",
    "Krüger":                   "https://www.kruger.dk/rss",
    "Orbicon|WSP":              "https://www.wsp.com/rss",
    "Grontmij":                 "https://www.carl-bro.dk/rss",
}

RSS_FORSYNINGER_RSS = {
    "HOFOR":                    "https://www.hofor.dk/rss",
}

RSS_NORDEN = {
    "SVT Nyheder Klima":        "https://www.svt.se/nyheter/rss.xml",
    "VA-guiden (SE)":           "https://www.vaguiden.se/rss",
    "NCCS Norge":               "https://www.nccs.no/rss",
    "NRK Klima":                "https://www.nrk.no/toppsaker.rss",
    "SMHI Sverige":             "https://www.smhi.se/rss",
}

RSS_EU = {
    "Interreg Baltic Sea":      "https://interreg-baltic.eu/feed/",
    "Climate-ADAPT":            "https://climate-adapt.eea.europa.eu/rss",
    "EEA Nyheder":              "https://www.eea.europa.eu/rss",
}

RSS_PLATFORME = {
    "BLOXHUB":                  "https://bloxhub.org/rss",
    "Gate 21":                  "https://www.gate21.dk/rss",
    "State of Green":           "https://stateofgreen.com/en/feed/",
    "Realdania":                "https://realdania.dk/rss",
    "Velux Fonden":             "https://veluxfoundations.dk/rss",
}

RSS_INTERNATIONAL = {
    "FloodList":                "https://floodlist.com/feed",
    "ICLEI":                    "https://iclei.org/news/rss/",
    "UN Environment":           "https://www.unep.org/rss.xml",
    "C40 Cities":               "https://www.c40.org/rss",
    "Deltares":                 "https://www.deltares.nl/rss",
}

# ── VANDKREDSLØB & GRUNDVAND ──
RSS_VAND = {
    "NGWA Groundwater":         "https://www.ngwa.org/rss.xml",
    "H2O Waternetwerk (NL)":    "https://www.h2owaternetwerk.nl/rss.xml",
    "Water Research Fdn":       "https://www.waterrf.org/rss.xml",
    "IWA Water":                "https://iwa-network.org/feed/",
    "The Source (IWA)":         "https://iwa-network.org/the-source/feed/",
    "Stormwater Report":        "https://stormwaterreport.com/feed/",
    "Water Resilience":         "https://www.waterresiliencecoalition.org/feed/",
    "Circle of Blue":           "https://www.circleofblue.org/feed/",
    "WaterWorld":               "https://www.waterworld.com/rss.xml",
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
    "Tredje Natur":             "https://tredjenatur.dk/feed/",
    "SLA Arkitekter":           "https://www.sla.dk/feed/",
}

# ── INTERNATIONALE VANDMYNDIGHEDER (NL, UK, US) ──
RSS_VAND_INT = {
    "Rijkswaterstaat (NL)":     "https://www.rijkswaterstaat.nl/rss.xml",
    "Environment Agency (UK)":  "https://www.gov.uk/search/news-and-communications.atom?organisations[]=environment-agency",
    "USGS Water":               "https://www.usgs.gov/rss.xml",
    "EPA Water (US)":           "https://www.epa.gov/rss/epa-news.xml",
    "Dutch Water Authorities":  "https://www.uvw.nl/rss.xml",
}

ALLE_FEEDS = {
    "Nyheder & fagblade":       RSS_NEWS,
    "Vidensinstitutioner":      RSS_VIDEN,
    "Rådgivere":                RSS_RAADGIVERE,
    "Forsyninger":              RSS_FORSYNINGER_RSS,
    "Nordiske naboer":          RSS_NORDEN,
    "EU projekter":             RSS_EU,
    "Platforme & netværk":      RSS_PLATFORME,
    "Internationale inst.":     RSS_INTERNATIONAL,
    "Vandkredsløb & grundvand": RSS_VAND,
    "Kreative vinkler":         RSS_KREATIVT,
    "Int. vandmyndigheder":     RSS_VAND_INT,
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
    "AAU Civil":                        {"url": "https://www.en.aau.dk/news", "gruppe": "Vidensinstitutioner"},
    "KU SCIENCE":                       {"url": "https://science.ku.dk/nyheder/", "gruppe": "Vidensinstitutioner"},
    "Teknologisk Institut":             {"url": "https://www.teknologisk.dk/nyheder/", "gruppe": "Vidensinstitutioner"},
    "GEUS":                             {"url": "https://www.geus.dk/om-geus/nyt-og-presse/nyheder/", "gruppe": "Vidensinstitutioner"},
    "DCE Aarhus Univ.":                 {"url": "https://dce.au.dk/nyheder/", "gruppe": "Vidensinstitutioner"},
    "DHI":                              {"url": "https://www.dhigroup.com/news", "gruppe": "Vidensinstitutioner"},

    # ── GRUNDVAND & VANDKREDSLØB ──
    "GEUS Grundvand":                   {"url": "https://www.geus.dk/vores-viden/vand/grundvand/nyheder/", "gruppe": "Vandkredsløb & grundvand"},
    "Naturstyrelsen Vand":              {"url": "https://naturstyrelsen.dk/nyheder/?tema=vand", "gruppe": "Vandkredsløb & grundvand"},
    "Den Danske Vandklynge":            {"url": "https://vandklynge.dk/nyheder/", "gruppe": "Vandkredsløb & grundvand"},
    "Vand i Byer":                      {"url": "https://vandibyer.dk/nyheder/", "gruppe": "Vandkredsløb & grundvand"},
    "Vandcenter Syd Innovation":        {"url": "https://vandcenter.dk/nyheder/", "gruppe": "Vandkredsløb & grundvand"},
    "Aarhus Vand Innovation":           {"url": "https://aarhusvand.dk/nyheder/", "gruppe": "Vandkredsløb & grundvand"},

    # ── LOVGIVNING & HØRINGER ──
    "Miljøministeriet Høringer":        {"url": "https://www.mim.dk/horinger/", "gruppe": "Lovgivning"},
    "Høringsportalen":                  {"url": "https://hoeringsportalen.dk/Hearing/List", "gruppe": "Lovgivning"},
    "Klimarådet":                       {"url": "https://klimaraadet.dk/da/nyheder", "gruppe": "Lovgivning"},
    "Forsyningstilsynet":               {"url": "https://forsyningstilsynet.dk/nyheder/", "gruppe": "Lovgivning"},

    # ── KREATIVE VINKLER ──
    "Realdania Projekter":              {"url": "https://realdania.dk/projekter/", "gruppe": "Kreative vinkler"},
    "Byspektrum":                       {"url": "https://byspektrum.dk/nyheder/", "gruppe": "Kreative vinkler"},
    "Tredje Natur Blog":                {"url": "https://tredjenatur.dk/blog/", "gruppe": "Kreative vinkler"},
    "SLA Arkitekter":                   {"url": "https://www.sla.dk/nyheder/", "gruppe": "Kreative vinkler"},
    "Schønherr Landskab":               {"url": "https://schonherr.dk/nyheder/", "gruppe": "Kreative vinkler"},
    "GHB Landskab":                     {"url": "https://ghb-landskab.dk/nyheder/", "gruppe": "Kreative vinkler"},
    "BLOXHUB":                          {"url": "https://bloxhub.org/nyheder/", "gruppe": "Kreative vinkler"},
    "Gate 21":                          {"url": "https://gate21.dk/nyheder/", "gruppe": "Kreative vinkler"},
    "Klimatorium":                      {"url": "https://klimatorium.dk/nyheder/", "gruppe": "Kreative vinkler"},

    # ── DNNK-RELATEREDE VIRKSOMHEDER ──
    "Nordiq Group":                     {"url": "https://nordiqgroup.dk/nyheder/", "gruppe": "Rådgivere"},
    "LYCEUM":                           {"url": "https://lyceum.dk/nyheder/", "gruppe": "Rådgivere"},
    "Forsikring & Pension":             {"url": "https://www.forsikringogpension.dk/nyheder/", "gruppe": "Rådgivere"},
    "Dansk Industri Vand":              {"url": "https://www.di.dk/nyheder/", "gruppe": "Rådgivere"},
    "SmartBrønd":                       {"url": "https://smartbrond.dk/nyheder/", "gruppe": "Rådgivere"},
    "Scalgo":                           {"url": "https://scalgo.com/nyheder/", "gruppe": "Rådgivere"},
    "Realdania":                        {"url": "https://realdania.dk/nyheder/", "gruppe": "Rådgivere"},

    # ── RÅDGIVERE & TEGNESTUER ──
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
    "Arkitema":                         {"url": "https://arkitema.com/nyheder/", "gruppe": "Rådgivere"},
    "Hasløv & Kjærsgaard":              {"url": "https://hkark.dk/nyheder/", "gruppe": "Rådgivere"},

    # ── MINISTERIER ──
    "Miljøministeriet":                 {"url": "https://www.mim.dk/nyheder/", "gruppe": "Myndigheder"},
    "Klima- og Energiministeriet":      {"url": "https://kefm.dk/aktuelt/nyheder/", "gruppe": "Myndigheder"},
    "Finansministeriet":                {"url": "https://www.fm.dk/nyheder/", "gruppe": "Myndigheder"},
    "Indenrigsministeriet":             {"url": "https://www.im.dk/nyheder/", "gruppe": "Myndigheder"},

    # ── STYRELSER & MYNDIGHEDER ──
    "Miljøstyrelsen":                   {"url": "https://mst.dk/nyheder/", "gruppe": "Myndigheder"},
    "Energistyrelsen":                  {"url": "https://ens.dk/nyheder/", "gruppe": "Myndigheder"},
    "Kystdirektoratet":                 {"url": "https://kyst.dk/nyheder/", "gruppe": "Myndigheder"},
    "KL":                               {"url": "https://www.kl.dk/nyheder/", "gruppe": "Myndigheder"},
    "Naturstyrelsen":                   {"url": "https://naturstyrelsen.dk/nyheder/", "gruppe": "Myndigheder"},
    "Beredskabsstyrelsen":              {"url": "https://brs.dk/nyheder/", "gruppe": "Myndigheder"},
    "Stormrådet":                       {"url": "https://www.stormraadet.dk/nyheder/", "gruppe": "Myndigheder"},
    "Vejdirektoratet":                  {"url": "https://www.vejdirektoratet.dk/nyheder", "gruppe": "Myndigheder"},
    "Statens Byggeforskningsinstitut":  {"url": "https://sbi.dk/nyheder/", "gruppe": "Myndigheder"},
    "Styrelsen for Dataforsyning":      {"url": "https://sdfe.dk/nyheder/", "gruppe": "Myndigheder"},

    # ── FORSYNINGER – Storkøbenhavn ──
    "HOFOR":                            {"url": "https://www.hofor.dk/nyheder/", "gruppe": "Forsyninger"},
    "Nordvand":                         {"url": "https://nordvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Novafos":                          {"url": "https://novafos.dk/nyheder/", "gruppe": "Forsyninger"},
    "Frederiksberg Fors.":              {"url": "https://frb-forsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Hillerød Forsyning":               {"url": "https://hfors.dk/nyheder/", "gruppe": "Forsyninger"},
    "Køge Forsyning":                   {"url": "https://koegeforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Roskilde Forsyning":               {"url": "https://roskilde-forsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Greve Forsyning":                  {"url": "https://greveforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "SK Forsyning":                     {"url": "https://skforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "BIOFOS":                           {"url": "https://www.biofos.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Østjylland ──
    "Aarhus Vand":                      {"url": "https://aarhusvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Skanderborg Forsyning":            {"url": "https://skanderborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Horsens Vand":                     {"url": "https://horsensvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Favrskov Forsyning":               {"url": "https://favrskovforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Randers Spildevand":               {"url": "https://randersspildevand.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Midtjylland ──
    "Silkeborg Forsyning":              {"url": "https://silkeborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Herning Vand":                     {"url": "https://herningvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Viborg Vand":                      {"url": "https://viborgvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Holstebro Vand":                   {"url": "https://holstebrovand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Lemvig Vand":                      {"url": "https://lemvigvand.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Nordjylland ──
    "Aalborg Forsyning":                {"url": "https://www.aalborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Hjørring Vandselskab":             {"url": "https://hjoerringvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Thisted Vand":                     {"url": "https://thistedvand.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Sydjylland ──
    "Esbjerg Forsyning":                {"url": "https://esbjergforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Vejle Spildevand":                 {"url": "https://www.vejlespildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Kolding Spildevand":               {"url": "https://koldingspildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Fredericia Forsyning":             {"url": "https://fredericiaforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Sønderborg Forsyning":             {"url": "https://sonderborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Fyn ──
    "VandCenter Syd":                   {"url": "https://vandcenter.dk/nyheder/", "gruppe": "Forsyninger"},
    "Assens Forsyning":                 {"url": "https://assensforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Middelfart Spildevand":            {"url": "https://middelfartspildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Svendborg Spildevand":             {"url": "https://svendborgspildevand.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Sjælland ──
    "Danva":                            {"url": "https://www.danva.dk/nyheder/", "gruppe": "Forsyninger"},
    "Kalundborg Forsyning":             {"url": "https://kalundborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Holbæk Forsyning":                 {"url": "https://holbaekforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Næstved Forsyning":                {"url": "https://naestvedforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Lolland Forsyning":                {"url": "https://lollandforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Bornholms Forsyning":              {"url": "https://bornholmsforsyning.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── KOMMUNER – de største ──
    "Kbh. Kommune":                     {"url": "https://www.kk.dk/nyheder", "gruppe": "Kommuner"},
    "Aarhus Kommune":                   {"url": "https://www.aarhus.dk/nyheder/", "gruppe": "Kommuner"},
    "Odense Kommune":                   {"url": "https://www.odense.dk/nyheder", "gruppe": "Kommuner"},
    "Aalborg Kommune":                  {"url": "https://www.aalborg.dk/nyheder", "gruppe": "Kommuner"},
    "Frederiksberg":                    {"url": "https://www.frederiksberg.dk/nyheder", "gruppe": "Kommuner"},
    "Vejle Kommune":                    {"url": "https://www.vejle.dk/nyheder", "gruppe": "Kommuner"},
    "Roskilde Kommune":                 {"url": "https://roskilde.dk/nyheder", "gruppe": "Kommuner"},
    "Helsingør Kommune":                {"url": "https://www.helsingor.dk/nyheder", "gruppe": "Kommuner"},
    "Silkeborg Kommune":                {"url": "https://www.silkeborg.dk/nyheder", "gruppe": "Kommuner"},
    "Horsens Kommune":                  {"url": "https://www.horsens.dk/nyheder", "gruppe": "Kommuner"},
    "Kolding Kommune":                  {"url": "https://www.kolding.dk/nyheder", "gruppe": "Kommuner"},
    "Esbjerg Kommune":                  {"url": "https://www.esbjerg.dk/nyheder", "gruppe": "Kommuner"},
    "Viborg Kommune":                   {"url": "https://viborg.dk/nyheder", "gruppe": "Kommuner"},
    "Sønderborg Kommune":               {"url": "https://www.sonderborg.dk/nyheder", "gruppe": "Kommuner"},
    "Ringkøbing-Skjern Kommune":        {"url": "https://www.rksk.dk/nyheder", "gruppe": "Kommuner"},
    "Bornholm Kommune":                 {"url": "https://www.brk.dk/nyheder", "gruppe": "Kommuner"},
}