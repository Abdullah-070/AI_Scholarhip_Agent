SCHOLARSHIP_SOURCES = {
    "daad": {
        "name": "DAAD (German Academic Exchange Service)",
        "url": "https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/",
        "api_url": "https://www2.daad.de/deutschland/stipendium/datenbank/api/scholarship/search",
        "type": "html",
        "enabled": True,
        "priority": 1
    },
    "hec": {
        "name": "HEC Pakistan",
        "url": "https://hec.gov.pk/english/scholarshipsgrants/Pages/default.aspx",
        "type": "html",
        "enabled": True,
        "priority": 2
    },
    "scholarshipportal": {
        "name": "ScholarshipPortal (EU)",
        "url": "https://www.scholarshipportal.com/scholarships",
        "type": "html",
        "enabled": True,
        "priority": 3
    },
    "scholars4dev": {
        "name": "Scholars4Dev",
        "url": "https://www.scholars4dev.com/category/scholarships/",
        "type": "html",
        "enabled": True,
        "priority": 4
    },
    "opportunitiescorners": {
        "name": "Opportunities Corners",
        "url": "https://opportunitiescorners.com/",
        "type": "html",
        "enabled": True,
        "priority": 5
    },
    "youthopportunities": {
        "name": "Youth Opportunities",
        "url": "https://www.youthopportunities.com/category/scholarships",
        "type": "html",
        "enabled": True,
        "priority": 6
    },
    "nuffic": {
        "name": "Study in NL (Nuffic)",
        "url": "https://www.studyinnl.org/scholarships",
        "type": "html",
        "enabled": True,
        "priority": 7
    },
    "swedish_institute": {
        "name": "Swedish Institute Scholarships",
        "url": "https://si.se/en/apply/scholarships/",
        "type": "html",
        "enabled": True,
        "priority": 8
    },
    "turkiye_burslari": {
        "name": "Türkiye Bursları Scholarships",
        "url": "https://www.turkiyeburslari.gov.tr/",
        "type": "html",
        "enabled": True,
        "priority": 9
    },
    "oas": {
        "name": "OAS Scholarships",
        "url": "https://www.oas.org/en/scholarships/",
        "type": "html",
        "enabled": True,
        "priority": 10
    },
    "maeci": {
        "name": "MAECI Scholarships – Spain",
        "url": "https://www.aecid.es/",
        "type": "html",
        "enabled": True,
        "priority": 11
    },
    "australia_awards": {
        "name": "Australia Awards Scholarships",
        "url": "https://www.dfat.gov.au/people-to-people/australia-awards",
        "type": "html",
        "enabled": True,
        "priority": 12
    },
    "manaaki": {
        "name": "Manaaki New Zealand Scholarships",
        "url": "https://www.nzscholarships.govt.nz/",
        "type": "html",
        "enabled": True,
        "priority": 13
    },
    "vlir": {
        "name": "VLIR-UOS Belgium Scholarships",
        "url": "https://www.vliruos.be/en/scholarships/",
        "type": "html",
        "enabled": True,
        "priority": 14
    },

    # PARTIAL JS SITES
    "chevening": {
        "name": "Chevening Scholarships",
        "url": "https://www.chevening.org/scholarships/",
        "type": "html_js",
        "enabled": True,
        "priority": 15
    },
    "fulbright": {
        "name": "Fulbright Program",
        "url": "https://foreign.fulbrightonline.org/",
        "type": "html_js",
        "enabled": True,
        "priority": 16
    },
    "commonwealth": {
        "name": "Commonwealth Scholarships",
        "url": "https://cscuk.fcdo.gov.uk/scholarships/",
        "type": "html_js",
        "enabled": True,
        "priority": 17
    },
    "erasmus": {
        "name": "Erasmus+ Study Abroad",
        "url": "https://erasmus-plus.ec.europa.eu/opportunities",
        "type": "html_js",
        "enabled": True,
        "priority": 18
    }
}

RSS_FEEDS = [
    "https://www.scholars4dev.com/feed/",
    "https://www.scholarshipportal.com/feed",
    "https://opportunitiescorners.com/feed/",
    "https://www.youthopportunities.com/feed/"
]

SITEMAPS = [
    "https://www.daad.de/sitemap.xml",
    "https://www.scholarshipportal.com/sitemap.xml",
    "https://www.scholars4dev.com/sitemap.xml"
]

SCRAPER_CLASS_MAP = {
    "daad": DAADScraper,
    "hec": HECScraper,
    "scholarshipportal": ScholarshipPortalScraper,   # if you add one
    "scholars4dev": Scholars4DevScraper,
    "opportunitiescorners": OpportunitiesCornersScraper,
    "youthopportunities": YouthOpportunitiesScraper,
    "nuffic": NufficScraper,
    "swedish_institute": SwedishInstituteScraper,
    "turkiye_burslari": TurkiyeBurslariScraper,
    "oas": OASScraper,
    "maeci": MAECIScraper,
    "australia_awards": AustraliaAwardsScraper,
    "manaaki": ManaakiScraper,
    "vlir": VLIRScraper,

    # JS-heavy ones:
    "chevening": CheveningScraper,
    "fulbright": FulbrightScraper,
    "commonwealth": CommonwealthScraper,
    "erasmus": ErasmusScraper
}
