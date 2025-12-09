# scrapers/hec_scraper.py

from typing import List, Dict
from scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re
import urllib3

# --- FIX: Suppress SSL Warnings ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HECScraper(BaseScraper):
    """Scraper for HEC Pakistan scholarship portal"""
    
    def scrape(self, profile: Dict) -> List[Dict]:
        """Scrape HEC scholarships"""
        scholarships = []
        
        try:
            # --- FIX: Add verify=False and increase timeout ---
            response = self.session.get(self.url, timeout=30, verify=False)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Find scholarship listings
            scholarships = self._parse_scholarship_list(soup, profile)
            
        except Exception as e:
            print(f"HEC scraping error: {e}")
            scholarships = self._get_fallback_scholarships()
        
        return scholarships
    
    # ... (Keep the rest of the file exactly as it was) ...
    def _parse_scholarship_list(self, soup: BeautifulSoup, profile: Dict) -> List[Dict]:
        scholarships = []
        content_divs = soup.find_all('div', class_=re.compile(r'(content|scholarship|news-item)', re.I))
        
        for div in content_divs[:15]:
            try:
                scholarship = self._extract_from_div(div)
                if scholarship:
                    scholarships.append(scholarship)
            except:
                continue
        
        if not scholarships:
            links = soup.find_all('a', href=True)
            for link in links:
                text = link.get_text(strip=True).lower()
                if any(keyword in text for keyword in ['scholarship', 'fellowship', 'grant', 'funding']):
                    scholarship = self._create_from_link(link)
                    if scholarship:
                        scholarships.append(scholarship)
                        if len(scholarships) >= 10:
                            break
        return scholarships

    def _extract_from_div(self, div) -> Dict:
        title_elem = div.find(['h2', 'h3', 'h4', 'strong', 'a'])
        title = title_elem.get_text(strip=True) if title_elem else None
        
        if not title or len(title) < 10:
            return None
        
        link_elem = div.find('a', href=True)
        url = link_elem['href'] if link_elem else self.url
        if url.startswith('/'):
            url = 'https://hec.gov.pk' + url
        
        content = div.get_text(strip=True)
        deadline = self._extract_deadline(content)
        country = self._extract_country(title + ' ' + content)
        
        return {
            'title': title,
            'country': country,
            'degree': self._extract_degree(content),
            'field': 'All fields',
            'duration': 'Varies',
            'funding': 'Full or partial funding',
            'eligibility': 'Pakistani nationals with strong academic records',
            'documents': 'Academic transcripts, IELTS/TOEFL, Research proposal',
            'deadline': deadline,
            'url': url
        }

    def _create_from_link(self, link) -> Dict:
        title = link.get_text(strip=True)
        url = link.get('href', self.url)
        if url.startswith('/'):
            url = 'https://hec.gov.pk' + url
        return {
            'title': title,
            'country': 'Various',
            'degree': 'Master\'s/PhD',
            'field': 'All fields',
            'duration': 'Varies',
            'funding': 'Full or partial funding',
            'eligibility': 'Pakistani nationals',
            'documents': 'See HEC portal for requirements',
            'deadline': 'Check official announcement',
            'url': url
        }

    def _extract_deadline(self, text: str) -> str:
        date_patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',
            r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        if 'deadline' in text.lower():
            deadline_idx = text.lower().find('deadline')
            snippet = text[deadline_idx:deadline_idx+100]
            return snippet.split('.')[0]
        return 'Check official announcement'

    def _extract_country(self, text: str) -> str:
        countries = ['Germany', 'USA', 'UK', 'Canada', 'Australia', 'China', 'Japan', 'France', 'Netherlands', 'Sweden', 'Norway']
        for country in countries:
            if country.lower() in text.lower():
                return country
        return 'Various'

    def _extract_degree(self, text: str) -> str:
        text_lower = text.lower()
        if 'phd' in text_lower or 'doctoral' in text_lower:
            return 'PhD'
        elif 'master' in text_lower or 'ms' in text_lower or 'mphil' in text_lower:
            return 'Master\'s'
        elif 'bachelor' in text_lower or 'undergraduate' in text_lower:
            return 'Bachelor\'s'
        elif 'postdoc' in text_lower:
            return 'Postdoctoral'
        return 'Master\'s/PhD'

    def _get_fallback_scholarships(self) -> List[Dict]:
        return [
            {'title': 'HEC Overseas Scholarship for PhD', 'country': 'Various', 'degree': 'PhD', 'field': 'All fields', 'duration': '3-5 years', 'funding': 'Full funding', 'eligibility': 'Pakistani nationals', 'documents': 'Admission letter, Transcripts', 'deadline': 'Check HEC website', 'url': 'https://hec.gov.pk/english/scholarshipsgrants/Pages/default.aspx'},
            {'title': 'HEC Indigenous PhD Scholarship', 'country': 'Pakistan', 'degree': 'PhD', 'field': 'All fields', 'duration': '3-4 years', 'funding': 'Monthly stipend', 'eligibility': 'Pakistani nationals', 'documents': 'Admission letter, Transcripts', 'deadline': 'Open year-round', 'url': 'https://hec.gov.pk/english/scholarshipsgrants/IPDP/Pages/default.aspx'}
        ]