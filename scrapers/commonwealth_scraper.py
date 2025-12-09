# scrapers/commonwealth_scraper.py

from typing import List, Dict
from scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re

class CommonwealthScraper(BaseScraper):
    """Scraper for Commonwealth Scholarships"""
    
    def scrape(self, profile: Dict) -> List[Dict]:
        scholarships = []

        try:
            response = self.session.get(self.url, timeout=40)
            soup = BeautifulSoup(response.content, "lxml")

            posts = soup.find_all("article")

            for p in posts:
                title_elem = p.find(["h2", "h3"])
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)

                if "scholar" in title.lower() or "commonwealth" in title.lower():
                    a = p.find("a", href=True)
                    link = a["href"] if a else self.url

                    scholarships.append({
                        "title": title,
                        "country": "United Kingdom",
                        "degree": "Master's/PhD",
                        "field": "All fields",
                        "duration": "1–3 years",
                        "funding": "Full scholarship",
                        "eligibility": "Commonwealth citizens",
                        "documents": "References, research proposal",
                        "deadline": "Usually Nov–Dec each year",
                        "url": link
                    })

        except Exception as e:
            print(f"Commonwealth error: {e}")

        return scholarships
