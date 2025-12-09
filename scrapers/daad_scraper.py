# scrapers/daad_scraper.py

from typing import List, Dict
from scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import json
import re

class DAADScraper(BaseScraper):
    """Stable DAAD scraper – HTML-only (API disabled)"""

    def scrape(self, profile: Dict) -> List[Dict]:
        """Main scrape entry"""
        try:
            return self._scrape_html(profile)
        except Exception as e:
            print(f"DAAD HTML FAILED → {e}")
            return []

    def _scrape_html(self, profile: Dict) -> List[Dict]:
        scholarships = []

        response = self.session.get(
            self.url,
            timeout=40,
            verify=True,
            allow_redirects=True
        )

        soup = BeautifulSoup(response.text, "lxml")

        # DAAD embeds JSON directly inside <script> tags
        script_tag = soup.find("script", text=re.compile("JSON"))
        if script_tag:
            try:
                json_text = re.search(r"JSON\.parse\('(.*)'\)", script_tag.text)
                if json_text:
                    parsed = json.loads(json_text.group(1).encode('utf-8').decode('unicode_escape'))
                    return self._parse_json_data(parsed)
            except:
                pass

        # fallback: extract basic cards
        cards = soup.find_all("a", class_="ghp-wrapper")
        for c in cards[:20]:
            scholarships.append({
                "title": c.get_text(strip=True),
                "country": "Germany",
                "degree": "All levels",
                "field": "All fields",
                "duration": "Varies",
                "funding": "Full / partial",
                "eligibility": "International students",
                "documents": "Check portal",
                "deadline": "Varies",
                "url": "https://www2.daad.de" + c.get("href", "")
            })

        return scholarships

    def _parse_json_data(self, data: Dict) -> List[Dict]:
        scholarships = []
        items = data.get("items", [])

        for item in items[:50]:
            scholarships.append({
                "title": item.get("title", "DAAD Scholarship"),
                "country": "Germany",
                "degree": item.get("degree", "All levels"),
                "field": item.get("subject", "All fields"),
                "duration": item.get("duration", "Varies"),
                "funding": item.get("funding", "Full/partial"),
                "eligibility": item.get("eligibility", "Check portal"),
                "documents": "See DAAD",
                "deadline": item.get("deadline", "Varies"),
                "url": item.get("url", self.url)
            })

        return scholarships
