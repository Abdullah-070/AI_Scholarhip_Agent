# config/settings.py

# Dropdown Options
DEGREE_LEVELS = [
    "Bachelor's",
    "Master's",
    "PhD",
    "Postdoctoral",
    "Short Course"
]

FIELDS_OF_STUDY = [
    "Engineering & Technology",
    "Computer Science & IT",
    "Business & Management",
    "Medicine & Health Sciences",
    "Natural Sciences",
    "Social Sciences",
    "Arts & Humanities",
    "Law",
    "Education",
    "Agriculture",
    "Environmental Sciences",
    "Mathematics & Statistics",
    "All Fields"
]

COUNTRIES = [
    "Germany",
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "Netherlands",
    "Sweden",
    "Norway",
    "Denmark",
    "Switzerland",
    "France",
    "Japan",
    "South Korea",
    "Singapore",
    "New Zealand",
    "Any Country"
]

NATIONALITIES = [
    "Pakistani",
    "Indian",
    "Bangladeshi",
    "Afghan",
    "Chinese",
    "Turkish",
    "Egyptian",
    "Nigerian",
    "Kenyan",
    "South African",
    "Brazilian",
    "Mexican",
    "All Developing Countries",
    "Any Nationality"
]

# Scraping Configuration
REQUEST_TIMEOUT = 15
MAX_RETRIES = 3
RETRY_DELAY = 2
USER_AGENT_ROTATION = True

# Rate Limiting
MIN_REQUEST_DELAY = 1.5
MAX_REQUEST_DELAY = 3.0

# Cache Settings
CACHE_DURATION_HOURS = 6
ENABLE_CACHING = True

# Excel Export Settings
EXCEL_SHEET_NAME = "Scholarships"
EXCEL_FREEZE_PANES = True