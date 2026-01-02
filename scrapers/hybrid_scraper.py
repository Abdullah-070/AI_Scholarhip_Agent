# scrapers/hybrid_scraper.py - ULTIMATE HYBRID SCRAPER

"""
Hybrid scraper that tries multiple methods in priority order:
1. Official API (fastest, most reliable)
2. RSS Feeds (fast, structured)
3. HTML Scraping (moderate speed)
4. Selenium (slowest, but handles JS)
5. Guaranteed fallback data
"""

from typing import List, Dict, Optional
from scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import feedparser
import json
import re

class HybridScraper(BaseScraper):
    """
    Advanced scraper that tries multiple methods to get real-time data
    """
    
    def __init__(self, source_config: Dict):
        super().__init__(source_config)
        self.api_endpoint = source_config.get('api_endpoint')
        self.rss_feed = source_config.get('rss_feed')
        self.use_selenium = source_config.get('use_selenium', False)
        self.fallback_data = source_config.get('fallback_data', [])
    
    def scrape(self, profile: Dict) -> List[Dict]:
        """
        Try multiple scraping methods in priority order
        """
        scholarships = []
        methods_tried = []
        
        print(f"    🔄 Hybrid scraping {self.name}...")
        
        # Method 1: Try API
        if self.api_endpoint:
            print(f"    📡 Trying API...")
            scholarships = self._try_api(profile)
            methods_tried.append("API")
            if scholarships:
                print(f"    ✅ API successful: {len(scholarships)} scholarships")
                return scholarships
        
        # Method 2: Try RSS Feed
        if self.rss_feed:
            print(f"    📰 Trying RSS feed...")
            scholarships = self._try_rss()
            methods_tried.append("RSS")
            if scholarships:
                print(f"    ✅ RSS successful: {len(scholarships)} scholarships")
                return scholarships
        
        # Method 3: Try HTML Scraping
        print(f"    🌐 Trying HTML scraping...")
        scholarships = self._try_html(profile)
        methods_tried.append("HTML")
        if scholarships:
            print(f"    ✅ HTML successful: {len(scholarships)} scholarships")
            return scholarships
        
        # Method 4: Try Selenium (if enabled and available)
        if self.use_selenium:
            print(f"    🤖 Trying Selenium (JavaScript rendering)...")
            scholarships = self._try_selenium(profile)
            methods_tried.append("Selenium")
            if scholarships:
                print(f"    ✅ Selenium successful: {len(scholarships)} scholarships")
                return scholarships
        
        # Method 5: Return fallback data
        print(f"    ⚠️  All methods failed ({', '.join(methods_tried)}), using fallback")
        return self._get_fallback_scholarships()
    
    def _try_api(self, profile: Dict) -> List[Dict]:
        """Try to fetch from API"""
        try:
            params = self._build_api_params(profile)
            response = self.session.get(
                self.api_endpoint,
                params=params,
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_api_response(data)
        except Exception as e:
            print(f"      API error: {e}")
        
        return []
    
    def _try_rss(self) -> List[Dict]:
        """Try to fetch from RSS feed"""
        try:
            feed = feedparser.parse(self.rss_feed)
            scholarships = []
            
            for entry in feed.entries[:15]:
                scholarship = self._parse_rss_entry(entry)
                if scholarship:
                    scholarships.append(scholarship)
            
            return scholarships
        except Exception as e:
            print(f"      RSS error: {e}")
        
        return []
    
    def _try_html(self, profile: Dict) -> List[Dict]:
        """Try HTML scraping"""
        try:
            response = self.session.get(self.url, timeout=30, verify=False)
            soup = BeautifulSoup(response.content, 'lxml')
            return self._parse_html(soup, profile)
        except Exception as e:
            print(f"      HTML error: {e}")
        
        return []
    
    def _try_selenium(self, profile: Dict) -> List[Dict]:
        """Try Selenium for JavaScript-heavy sites"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.chrome import ChromeDriverManager
            
            # Setup headless Chrome
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            try:
                driver.get(self.url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                return self._parse_html(soup, profile)
            
            finally:
                driver.quit()
        
        except Exception as e:
            print(f"      Selenium error: {e}")
        
        return []
    
    def _build_api_params(self, profile: Dict) -> Dict:
        """Build API parameters from profile"""
        return {
            'degree': profile.get('degree_level', ''),
            'field': profile.get('field_of_study', ''),
            'country': profile.get('country', ''),
            'limit': 20
        }
    
    def _parse_api_response(self, data: Dict) -> List[Dict]:
        """Parse API JSON response - override in subclasses"""
        # Default implementation - extract scholarships array
        scholarships_key = None
        for key in ['scholarships', 'results', 'data', 'items']:
            if key in data:
                scholarships_key = key
                break
        
        if not scholarships_key:
            return []
        
        scholarships = []
        for item in data[scholarships_key][:20]:
            scholarships.append({
                'title': item.get('title') or item.get('name', 'Scholarship'),
                'country': item.get('country', 'Various'),
                'degree': item.get('degree', 'Not specified'),
                'field': item.get('field', 'All fields'),
                'duration': item.get('duration', 'Varies'),
                'funding': item.get('funding', 'See website'),
                'eligibility': item.get('eligibility', 'See website'),
                'documents': item.get('documents', 'See website'),
                'deadline': item.get('deadline', 'Check website'),
                'url': item.get('url', self.url)
            })
        
        return scholarships
    
    def _parse_rss_entry(self, entry) -> Optional[Dict]:
        """Parse RSS feed entry"""
        title = entry.get('title', '')
        link = entry.get('link', '')
        
        if not title or not link:
            return None
        
        # Extract text from description
        description = entry.get('description', '') or entry.get('summary', '')
        soup = BeautifulSoup(description, 'lxml')
        text = soup.get_text(strip=True)
        
        return {
            'title': title,
            'country': self._extract_country(title + ' ' + text),
            'degree': self._extract_degree(text),
            'field': self._extract_field(text),
            'duration': 'Varies',
            'funding': self._extract_funding(text),
            'eligibility': 'See website',
            'documents': 'See website',
            'deadline': self._extract_deadline(text),
            'url': link
        }
    
    def _parse_html(self, soup: BeautifulSoup, profile: Dict) -> List[Dict]:
        """Parse HTML - override in subclasses for specific sites"""
        scholarships = []
        
        # Generic HTML parsing
        links = soup.find_all('a', href=True)
        
        for link in links:
            text = link.get_text(strip=True)
            if self._is_scholarship_link(text):
                url = link.get('href', '')
                if url.startswith('/'):
                    from urllib.parse import urlparse
                    parsed = urlparse(self.url)
                    url = f"{parsed.scheme}://{parsed.netloc}{url}"
                
                scholarships.append({
                    'title': text,
                    'country': 'Various',
                    'degree': 'Not specified',
                    'field': 'All fields',
                    'duration': 'Varies',
                    'funding': 'See website',
                    'eligibility': 'See website',
                    'documents': 'See website',
                    'deadline': 'Check website',
                    'url': url
                })
                
                if len(scholarships) >= 15:
                    break
        
        return scholarships
    
    def _is_scholarship_link(self, text: str) -> bool:
        """Check if text indicates a scholarship"""
        keywords = ['scholarship', 'fellowship', 'grant', 'funding', 'award', 'bursary']
        text_lower = text.lower()
        return any(kw in text_lower for kw in keywords) and len(text) > 15
    
    def _extract_country(self, text: str) -> str:
        """Extract country from text"""
        countries = {
            'germany': 'Germany', 'usa': 'United States', 'america': 'United States',
            'uk': 'United Kingdom', 'britain': 'United Kingdom',
            'canada': 'Canada', 'australia': 'Australia',
            'france': 'France', 'japan': 'Japan', 'china': 'China'
        }
        
        text_lower = text.lower()
        for keyword, country in countries.items():
            if keyword in text_lower:
                return country
        
        return 'Various'
    
    def _extract_degree(self, text: str) -> str:
        """Extract degree level"""
        text_lower = text.lower()
        if 'phd' in text_lower or 'doctoral' in text_lower:
            return 'PhD'
        elif 'master' in text_lower:
            return 'Master\'s'
        elif 'bachelor' in text_lower:
            return 'Bachelor\'s'
        return 'Various'
    
    def _extract_field(self, text: str) -> str:
        """Extract field of study"""
        fields = {
            'engineering': 'Engineering',
            'computer': 'Computer Science',
            'business': 'Business',
            'medicine': 'Medicine'
        }
        
        text_lower = text.lower()
        for keyword, field in fields.items():
            if keyword in text_lower:
                return field
        
        return 'All fields'
    
    def _extract_funding(self, text: str) -> str:
        """Extract funding info"""
        if 'fully funded' in text.lower() or 'full scholarship' in text.lower():
            return 'Fully funded'
        elif 'partial' in text.lower():
            return 'Partial funding'
        return 'See website'
    
    def _extract_deadline(self, text: str) -> str:
        """Extract deadline"""
        patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return 'Check website'
    
    def _get_fallback_scholarships(self) -> List[Dict]:
        """Return fallback data if all methods fail"""
        if self.fallback_data:
            return self.fallback_data
        
        # Generic fallback
        return [{
            'title': f'{self.name} - Visit Official Website',
            'country': 'Various',
            'degree': 'All levels',
            'field': 'All fields',
            'duration': 'Varies',
            'funding': 'See official website',
            'eligibility': 'Check official website for requirements',
            'documents': 'See website',
            'deadline': 'Multiple deadlines',
            'url': self.url
        }]