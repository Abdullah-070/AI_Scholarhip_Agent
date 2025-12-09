# scrapers/erasmus_scraper.py

from typing import List, Dict
from scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re

class ErasmusScraper(BaseScraper):
    """Scraper for Erasmus+ study abroad opportunities"""
    
    def scrape(self, profile: Dict) -> List[Dict]:
        scholarships = []

        try:
            response = self.session.get(self.url, timeout=45)
            soup = BeautifulSoup(response.content, "lxml")

            listings = soup.find_all("a", href=True)

            for a in listings:
                text = a.get_text(strip=True).lower()

                if any(k in text for k in ["erasmus", "scholarship", "mobility", "study"]):
                    scholarships.append({
                        "title": a.get_text(strip=True),
                        "country": "Europe (multiple countries)",
                        "degree": "Bachelor's/Master's",
                        "field": "All fields",
                        "duration": "3–12 months",
                        "funding": "Monthly stipend + travel support",
                        "eligibility": "Students enrolled in partner universities",
                        "documents": "Transcript, learning agreement",
                        "deadline": "Rolling deadlines",
                        "url": a["href"] if a["href"].startswith("http") else self.url
                    })

        except Exception as e:
            print(f"Erasmus error: {e}")

        return scholarships
