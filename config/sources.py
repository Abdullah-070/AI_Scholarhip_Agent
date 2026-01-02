# config/sources.py - WITH API, RSS, AND SELENIUM CONFIGURATION

SCHOLARSHIP_SOURCES = {
    "daad": {
        "name": "DAAD (German Academic Exchange Service)",
        "url": "https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/",
        "api_endpoint": None,  # DAAD API requires authentication
        "rss_feed": None,
        "use_selenium": False,
        "type": "hybrid",
        "enabled": True,
        "priority": 1
    },
    
    "hec": {
        "name": "HEC Pakistan",
        "url": "https://hec.gov.pk/english/scholarshipsgrants/Pages/default.aspx",
        "api_endpoint": None,
        "rss_feed": None,
        "use_selenium": False,
        "type": "hybrid",
        "enabled": True,
        "priority": 2
    },
    
    "scholars4dev": {
        "name": "Scholars4Dev",
        "url": "https://www.scholars4dev.com/category/scholarships/",
        "api_endpoint": None,
        "rss_feed": "https://www.scholars4dev.com/feed/",  # ✅ HAS RSS
        "use_selenium": False,
        "type": "hybrid",
        "enabled": True,
        "priority": 3
    },
    
    "opportunitiescorners": {
        "name": "Opportunities Corners",
        "url": "https://opportunitiescorners.com/",
        "api_endpoint": None,
        "rss_feed": "https://opportunitiescorners.com/feed/",  # ✅ HAS RSS
        "use_selenium": False,
        "type": "hybrid",
        "enabled": True,
        "priority": 4
    },
    
    "youthopportunities": {
        "name": "Youth Opportunities",
        "url": "https://www.youthopportunities.com/category/scholarships",
        "api_endpoint": None,
        "rss_feed": "https://www.youthopportunities.com/feed/",  # ✅ HAS RSS
        "use_selenium": False,
        "type": "hybrid",
        "enabled": True,
        "priority": 5
    },
    
    "scholarshipportal": {
        "name": "ScholarshipPortal (EU)",
        "url": "https://www.scholarshipportal.com/scholarships",
        "api_endpoint": None,  # They have API but requires key
        "rss_feed": "https://www.scholarshipportal.com/feed",  # ✅ HAS RSS
        "use_selenium": False,
        "type": "hybrid",
        "enabled": True,
        "priority": 6
    },
    
    "chevening": {
        "name": "Chevening Scholarships",
        "url": "https://www.chevening.org/scholarships/",
        "api_endpoint": None,
        "rss_feed": None,
        "use_selenium": True,  # ✅ JavaScript-heavy site
        "type": "hybrid",
        "enabled": True,
        "priority": 7
    },
    
    "fulbright": {
        "name": "Fulbright Program",
        "url": "https://foreign.fulbrightonline.org/",
        "api_endpoint": None,
        "rss_feed": None,
        "use_selenium": True,  # ✅ JavaScript-heavy site
        "type": "hybrid",
        "enabled": True,
        "priority": 8
    },
    
    "commonwealth": {
        "name": "Commonwealth Scholarships",
        "url": "https://cscuk.fcdo.gov.uk/scholarships/",
        "api_endpoint": None,
        "rss_feed": None,
        "use_selenium": False,
        "type": "hybrid",
        "enabled": True,
        "priority": 9
    },
    
    "erasmus": {
        "name": "Erasmus+",
        "url": "https://erasmus-plus.ec.europa.eu/opportunities",
        "api_endpoint": None,
        "rss_feed": None,
        "use_selenium": True,  # ✅ JavaScript-heavy site
        "type": "hybrid",
        "enabled": True,
        "priority": 10
    }
}

# Global RSS feeds (used by GenericScraper)
RSS_FEEDS = [
    "https://www.scholars4dev.com/feed/",
    "https://www.scholarshipportal.com/feed",
    "https://opportunitiescorners.com/feed/",
    "https://www.youthopportunities.com/feed/"
]

# Sitemaps for discovery
SITEMAPS = [
    "https://www.daad.de/sitemap.xml",
    "https://www.scholarshipportal.com/sitemap.xml",
    "https://www.scholars4dev.com/sitemap.xml"
]