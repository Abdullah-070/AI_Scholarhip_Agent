# scrapers/chevening_scraper.py

from typing import List, Dict
from scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re

class CheveningScraper(BaseScraper):
    """Scraper for Chevening Scholarships"""
    
    def scrape(self, profile: Dict) -> List[Dict]:
        scholarships = []

        try:
            response = self.session.get(self.url, timeout=40)
            soup = BeautifulSoup(response.content, "lxml")

            items = soup.find_all("a", href=True)
            for a in items:
                text = a.get_text(strip=True)
                if any(word in text.lower() for word in [
                    "scholarship", "chevening", "fellowship", "award"
                ]):
                    scholarships.append({
                        "title": text,
                        "country": "United Kingdom",
                        "degree": "Master's",
                        "field": "All fields",
                        "duration": "1 year",
                        "funding": "Full funding",
                        "eligibility": "Open to over 160 countries",
                        "documents": "CV, references, motivation essays",
                        "deadline": "Varies each year",
                        "url": a["href"] if a["href"].startswith("http") else self.url
                    })

        except Exception as e:
            print(f"Chevening error: {e}")

        return scholarships