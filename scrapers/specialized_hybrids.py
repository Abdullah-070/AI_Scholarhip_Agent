# scrapers/specialized_hybrids.py - SPECIALIZED HYBRID SCRAPERS

from typing import List, Dict
from scrapers.hybrid_scraper import HybridScraper

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

import re
import json

class Scholars4DevHybrid(HybridScraper):
    """Scholars4Dev with RSS + HTML fallback"""
    
    def _parse_html(self, soup: BeautifulSoup, profile: Dict) -> List[Dict]:
        """Custom HTML parsing for Scholars4Dev"""
        scholarships = []
        
        # Find article listings
        articles = soup.find_all('article', class_=re.compile('post', re.I))
        
        for article in articles[:15]:
            title_elem = article.find(['h2', 'h3'])
            link_elem = article.find('a', href=True)
            
            if title_elem and link_elem:
                scholarships.append({
                    'title': title_elem.get_text(strip=True),
                    'country': 'Various',
                    'degree': 'All levels',
                    'field': 'All fields',
                    'duration': 'Varies',
                    'funding': 'See website',
                    'eligibility': 'International students',
                    'documents': 'See website',
                    'deadline': 'Check website',
                    'url': link_elem['href']
                })
        
        return scholarships


class ScholarshipPortalHybrid(HybridScraper):
    """ScholarshipPortal with RSS + HTML"""
    
    def _parse_html(self, soup: BeautifulSoup, profile: Dict) -> List[Dict]:
        """Custom HTML parsing for ScholarshipPortal"""
        scholarships = []
        
        # Find scholarship cards
        cards = soup.find_all('div', class_=re.compile('scholarship', re.I))
        
        for card in cards[:20]:
            title_elem = card.find(['h3', 'h4', 'a'])
            link_elem = card.find('a', href=True)
            
            if title_elem and link_elem:
                url = link_elem['href']
                if not url.startswith('http'):
                    url = 'https://www.scholarshipportal.com' + url
                
                scholarships.append({
                    'title': title_elem.get_text(strip=True),
                    'country': 'Europe',
                    'degree': 'All levels',
                    'field': 'All fields',
                    'duration': 'Varies',
                    'funding': 'Varies',
                    'eligibility': 'International students',
                    'documents': 'See website',
                    'deadline': 'Varies',
                    'url': url
                })
        
        return scholarships


class DAADHybrid(HybridScraper):
    """DAAD with JSON extraction + guaranteed fallback"""
    
    def _parse_html(self, soup: BeautifulSoup, profile: Dict) -> List[Dict]:
        """Parse DAAD with JSON extraction"""
        scholarships = []
        
        # Try to find JSON data in scripts
        script_tags = soup.find_all('script', text=re.compile('scholarship|stipendium', re.I))
        
        for script in script_tags:
            try:
                json_match = re.search(r'{[\s\S]*}', script.string)
                if json_match:
                    data = json.loads(json_match.group(0))
                    if 'items' in data or 'scholarships' in data:
                        return self._parse_api_response(data)
            except:
                continue
        
        # Fallback to link extraction
        cards = soup.find_all('a', href=re.compile('stipendium', re.I))
        for card in cards[:15]:
            title = card.get_text(strip=True)
            if len(title) > 15:
                scholarships.append({
                    'title': title,
                    'country': 'Germany',
                    'degree': 'All levels',
                    'field': 'All fields',
                    'duration': 'Varies',
                    'funding': 'Full or partial',
                    'eligibility': 'International students',
                    'documents': 'See DAAD portal',
                    'deadline': 'Varies',
                    'url': 'https://www2.daad.de' + card.get('href', '')
                })
        
        return scholarships
    
    def _get_fallback_scholarships(self) -> List[Dict]:
        """DAAD guaranteed fallback"""
        return [
            {
                'title': 'DAAD Graduate School Scholarship Programme',
                'country': 'Germany',
                'degree': 'PhD',
                'field': 'All fields',
                'duration': 'Up to 3 years',
                'funding': '€1,200/month + health insurance',
                'eligibility': 'International students',
                'documents': 'CV, transcripts, language certificate',
                'deadline': 'Varies by institution',
                'url': 'https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/'
            },
            {
                'title': 'DAAD EPOS Scholarships',
                'country': 'Germany',
                'degree': 'Master\'s',
                'field': 'Engineering, Agriculture, Economics',
                'duration': '12-42 months',
                'funding': '€934/month + tuition',
                'eligibility': 'Developing country nationals',
                'documents': 'Admission letter, CV, references',
                'deadline': 'August-October',
                'url': 'https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/'
            },
            {
                'title': 'DAAD Study Scholarships',
                'country': 'Germany',
                'degree': 'Master\'s',
                'field': 'All fields',
                'duration': '10-24 months',
                'funding': '€934/month + insurance',
                'eligibility': 'International graduates',
                'documents': 'Admission, CV, transcripts',
                'deadline': 'October 31',
                'url': 'https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/'
            }
        ]


class HECHybrid(HybridScraper):
    """HEC with guaranteed fallback"""
    
    def _get_fallback_scholarships(self) -> List[Dict]:
        """HEC guaranteed fallback"""
        return [
            {
                'title': 'HEC Overseas PhD Scholarship',
                'country': 'Various',
                'degree': 'PhD',
                'field': 'All fields',
                'duration': '3-5 years',
                'funding': 'Full funding',
                'eligibility': 'Pakistani nationals under 35',
                'documents': 'Admission letter, IELTS 6.5+',
                'deadline': 'March and September',
                'url': 'https://hec.gov.pk/english/scholarshipsgrants/OSHD/Pages/default.aspx'
            },
            {
                'title': 'HEC Indigenous PhD Fellowship',
                'country': 'Pakistan',
                'degree': 'PhD',
                'field': 'All fields',
                'duration': '3-4 years',
                'funding': 'PKR 25,000-40,000/month',
                'eligibility': 'Pakistani nationals',
                'documents': 'PhD admission, transcripts',
                'deadline': 'Open year-round',
                'url': 'https://hec.gov.pk/english/scholarshipsgrants/IPDP/Pages/default.aspx'
            },
            {
                'title': 'HEC Commonwealth Scholarship',
                'country': 'United Kingdom',
                'degree': 'Master\'s/PhD',
                'field': 'All fields',
                'duration': '1-3 years',
                'funding': 'Full scholarship',
                'eligibility': 'Pakistani nationals',
                'documents': 'Admission, IELTS, references',
                'deadline': 'December',
                'url': 'https://hec.gov.pk/english/scholarshipsgrants/Pages/default.aspx'
            },
            {
                'title': 'HEC Chinese Government Scholarship',
                'country': 'China',
                'degree': 'All levels',
                'field': 'All fields',
                'duration': 'Varies',
                'funding': 'Full scholarship',
                'eligibility': 'Pakistani nationals',
                'documents': 'Admission, health certificate',
                'deadline': 'January-March',
                'url': 'https://hec.gov.pk/english/scholarshipsgrants/Pages/default.aspx'
            },
            {
                'title': 'HEC Turkey Scholarships',
                'country': 'Turkey',
                'degree': 'All levels',
                'field': 'All fields',
                'duration': 'Varies',
                'funding': 'Monthly stipend + accommodation',
                'eligibility': 'Pakistani nationals',
                'documents': 'Transcripts, references',
                'deadline': 'February',
                'url': 'https://hec.gov.pk/english/scholarshipsgrants/Pages/default.aspx'
            }
        ]