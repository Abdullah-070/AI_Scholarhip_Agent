# scrapers/fulbright_scraper.py

from typing import List, Dict
from scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup

class FulbrightScraper(BaseScraper):
    """Scraper for Fulbright Foreign Student Program"""
    
    def scrape(self, profile: Dict) -> List[Dict]:
        scholarships = []

        try:
            response = self.session.get(self.url, timeout=40)
            soup = BeautifulSoup(response.content, "lxml")

            links = soup.find_all("a", href=True)

            for link in links:
                text = link.get_text(strip=True).lower()
                if "fulbright" in text or "scholar" in text:
                    scholarships.append({
                        "title": link.get_text(strip=True),
                        "country": "United States",
                        "degree": "Master's/PhD",
                        "field": "All fields",
                        "duration": "1-5 years",
                        "funding": "Full funding + stipend + health insurance",
                        "eligibility": "International applicants",
                        "documents": "GRE/TOEFL, transcripts, essays",
                        "deadline": "Varies by country",
                        "url": link["href"] if link["href"].startswith("http") else self.url
                    })

        except Exception as e:
            print(f"Fulbright scraper error: {e}")

        return scholarships
