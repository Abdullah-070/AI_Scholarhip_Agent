"""
Additional scrapers for global scholarship sources.

This single file provides 10 scraper classes that extend your existing BaseScraper
and follow the same patterns used in your existing scrapers (requests.Session,
BeautifulSoup fallback parsing, robots.txt checks, robust error handling).

Classes included:
- CheveningScraper
- FulbrightScraper
- CommonwealthScraper
- ErasmusScraper
- CSCChinaScraper
- MEXTJapanScraper
- SwedishInstituteScraper
- AustraliaAwardsScraper
- VanierCanadaScraper
- GatesCambridgeScraper

Drop this file into your `scrapers/` package and import the classes where needed.
"""

from typing import List, Dict
from scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import requests
import urllib.robotparser
import urllib.parse
import time
import re

# Helper: check robots.txt for a given URL and user-agent

def is_path_allowed(session: requests.Session, page_url: str, user_agent: str = "*") -> bool:
    try:
        parsed = urllib.parse.urlparse(page_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        # Use session to respect proxies or mounts
        resp = session.get(robots_url, timeout=10)
        if resp.status_code != 200:
            # No robots.txt or inaccessible -> treat as allowed (conservative)
            return True
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(resp.text.splitlines())
        return rp.can_fetch(user_agent, page_url)
    except Exception:
        # If robots check fails for any reason, return False to be safe
        return False


# Common lightweight HTML parsing helper

def extract_scholarship_cards(soup: BeautifulSoup, keywords: List[str] = None, limit: int = 10) -> List[Dict]:
    keywords = keywords or ["scholarship", "fellowship", "grant", "funding", "award"]
    results = []

    # Strategy: find article/listing elements and anchor tags that mention keywords
    candidates = soup.find_all(['article', 'div', 'li', 'section'], limit=50)
    for block in candidates:
        txt = block.get_text(separator=' ', strip=True).lower()
        if any(k in txt for k in keywords):
            # try to extract title and link
            a = block.find('a', href=True)
            title_elem = block.find(['h1', 'h2', 'h3', 'h4', 'strong'])
            title = title_elem.get_text(strip=True) if title_elem else (a.get_text(strip=True) if a else None)
            url = a['href'] if a else None
            if title and url:
                if url.startswith('/'):
                    parsed = soup.find('base')
                    # best-effort absolute construction
                    # caller should post-process absolute URLs if needed
                results.append({
                    'title': title,
                    'country': 'Various',
                    'degree': 'Not specified',
                    'field': 'All fields',
                    'duration': 'Varies',
                    'funding': 'Varies',
                    'eligibility': 'See official site',
                    'documents': 'See official site',
                    'deadline': 'See official site',
                    'url': url
                })
            if len(results) >= limit:
                break

    # fallback: scan anchors
    if not results:
        anchors = soup.find_all('a', href=True)
        for a in anchors:
            txt = a.get_text(strip=True).lower()
            if any(k in txt for k in keywords):
                results.append({
                    'title': a.get_text(strip=True) or 'Scholarship',
                    'country': 'Various',
                    'degree': 'Not specified',
                    'field': 'All fields',
                    'duration': 'Varies',
                    'funding': 'Varies',
                    'eligibility': 'See official site',
                    'documents': 'See official site',
                    'deadline': 'See official site',
                    'url': a['href']
                })
                if len(results) >= limit:
                    break

    return results


# -------------- Individual scraper classes --------------

class CheveningScraper(BaseScraper):
    def scrape(self, profile: Dict) -> List[Dict]:
        if not is_path_allowed(self.session, self.url, self.session.headers.get('User-Agent', '*')):
            print(f"Chevening: robots.txt disallows scraping {self.url}")
            return []

        try:
            resp = self.session.get(self.url, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'lxml')
            results = extract_scholarship_cards(soup, limit=12)
            return results
        except Exception as e:
            print(f"Chevening scraping error: {e}")
            return []


class FulbrightScraper(BaseScraper):
    def scrape(self, profile: Dict) -> List[Dict]:
        if not is_path_allowed(self.session, self.url, self.session.headers.get('User-Agent', '*')):
            print(f"Fulbright: robots.txt disallows scraping {self.url}")
            return []
        try:
            resp = self.session.get(self.url, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'lxml')
            # Fulbright often lists program types; find program listing links
            results = extract_scholarship_cards(soup, limit=15)
            return results
        except Exception as e:
            print(f"Fulbright scraping error: {e}")
            return []


class CommonwealthScraper(BaseScraper):
    def scrape(self, profile: Dict) -> List[Dict]:
        if not is_path_allowed(self.session, self.url, self.session.headers.get('User-Agent', '*')):
            print(f"Commonwealth: robots.txt disallows scraping {self.url}")
            return []
        try:
            resp = self.session.get(self.url, timeout=25)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'lxml')
            items = extract_scholarship_cards(soup, limit=12)
            return items
        except Exception as e:
            print(f"Commonwealth scraping error: {e}")
            return []


class ErasmusScraper(BaseScraper):
    def scrape(self, profile: Dict) -> List[Dict]:
        if not is_path_allowed(self.session, self.url, self.session.headers.get('User-Agent', '*')):
            print(f"Erasmus: robots.txt disallows scraping {self.url}")
            return []
        try:
            resp = self.session.get(self.url, timeout=25)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'lxml')
            # Erasmus pages are often content-rich; try to find links mentioning "opportunities" or "students"
            items = extract_scholarship_cards(soup, keywords=['opportunity', 'scholarship', 'study abroad'], limit=15)
            return items
        except Exception as e:
            print(f"Erasmus scraping error: {e}")
            return []


class CSCChinaScraper(BaseScraper):
    def scrape(self, profile: Dict) -> List[Dict]:
        # China Scholarship Council site sometimes enforces stricter bot checks
        if not is_path_allowed(self.session, self.url, self.session.headers.get('User-Agent', '*')):
            print(f"CSC: robots.txt disallows scraping {self.url}")
            return []
        try:
            resp = self.session.get(self.url, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'lxml')
            items = extract_scholarship_cards(soup, limit=10)
            return items
        except Exception as e:
            print(f"CSC scraping error: {e}")
            return []


class MEXTJapanScraper(BaseScraper):
    def scrape(self, profile: Dict) -> List[Dict]:
        if not is_path_allowed(self.session, self.url, self.session.headers.get('User-Agent', '*')):
            print(f"MEXT: robots.txt disallows scraping {self.url}")
            return []
        try:
            resp = self.session.get(self.url, timeout=25)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'lxml')
            items = extract_scholarship_cards(soup, limit=12)
            return items
        except Exception as e:
            print(f"MEXT scraping error: {e}")
            return []


class SwedishInstituteScraper(BaseScraper):
    def scrape(self, profile: Dict) -> List[Dict]:
        if not is_path_allowed(self.session, self.url, self.session.headers.get('User-Agent', '*')):
            print(f"Swedish Institute: robots.txt disallows scraping {self.url}")
            return []
        try:
            resp = self.session.get(self.url, timeout=25)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'lxml')
            items = extract_scholarship_cards(soup, limit=10)
            return items
        except Exception as e:
            print(f"Swedish Institute scraping error: {e}")
            return []


class AustraliaAwardsScraper(BaseScraper):
    def scrape(self, profile: Dict) -> List[Dict]:
        if not is_path_allowed(self.session, self.url, self.session.headers.get('User-Agent', '*')):
            print(f"Australia Awards: robots.txt disallows scraping {self.url}")
            return []
        try:
            resp = self.session.get(self.url, timeout=25)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'lxml')
            items = extract_scholarship_cards(soup, limit=12)
            return items
        except Exception as e:
            print(f"Australia Awards scraping error: {e}")
            return []


class VanierCanadaScraper(BaseScraper):
    def scrape(self, profile: Dict) -> List[Dict]:
        if not is_path_allowed(self.session, self.url, self.session.headers.get('User-Agent', '*')):
            print(f"Vanier: robots.txt disallows scraping {self.url}")
            return []
        try:
            resp = self.session.get(self.url, timeout=25)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'lxml')
            items = extract_scholarship_cards(soup, limit=8)
            return items
        except Exception as e:
            print(f"Vanier scraping error: {e}")
            return []


class GatesCambridgeScraper(BaseScraper):
    def scrape(self, profile: Dict) -> List[Dict]:
        # Gates Cambridge is university-managed and may list limited info publicly
        if not is_path_allowed(self.session, self.url, self.session.headers.get('User-Agent', '*')):
            print(f"Gates Cambridge: robots.txt disallows scraping {self.url}")
            return []
        try:
            resp = self.session.get(self.url, timeout=25)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'lxml')
            items = extract_scholarship_cards(soup, limit=8)
            return items
        except Exception as e:
            print(f"Gates Cambridge scraping error: {e}")
            return []
