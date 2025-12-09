# scrapers/generic_scraper.py

from typing import List, Dict
from scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import feedparser
import re

class GenericScraper(BaseScraper):
    """Generic scraper for other scholarship sources"""
    
    def scrape(self, profile: Dict) -> List[Dict]:
        """Scrape using multiple fallback methods"""
        scholarships = []
        
        # Try RSS feed first
        scholarships.extend(self._scrape_rss())
        
        # Try HTML scraping
        if len(scholarships) < 5:
            scholarships.extend(self._scrape_html(profile))
        
        return scholarships[:20]  # Limit results
    
    def _scrape_rss(self) -> List[Dict]:
        """Scrape scholarships from RSS feeds"""
        scholarships = []
        
        rss_feeds = [
            'https://www.scholars4dev.com/feed/',
            'https://opportunitiescorners.info/feed/',
        ]
        
        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:10]:
                    scholarship = self._parse_rss_entry(entry)
                    if scholarship:
                        scholarships.append(scholarship)
            except Exception as e:
                print(f"RSS feed error ({feed_url}): {e}")
                continue
        
        return scholarships
    
    def _parse_rss_entry(self, entry) -> Dict:
        """Parse RSS feed entry into scholarship format"""
        title = entry.get('title', 'Scholarship Opportunity')
        
        # Extract text content
        content = entry.get('summary', '') or entry.get('description', '')
        
        # Clean HTML tags
        soup = BeautifulSoup(content, 'lxml')
        text_content = soup.get_text(strip=True)
        
        return {
            'title': title,
            'country': self._extract_country(title + ' ' + text_content),
            'degree': self._extract_degree(text_content),
            'field': 'All fields',
            'duration': 'Varies',
            'funding': self._extract_funding(text_content),
            'eligibility': 'International students - check official website',
            'documents': 'See official announcement',
            'deadline': self._extract_deadline(text_content),
            'url': entry.get('link', '')
        }
    
    def _scrape_html(self, profile: Dict) -> List[Dict]:
        """Scrape from HTML pages"""
        scholarships = []
        
        try:
            response = self.session.get(self.url, timeout=20)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Find potential scholarship links
            links = soup.find_all('a', href=True)
            
            for link in links:
                text = link.get_text(strip=True)
                if self._is_scholarship_link(text):
                    scholarship = self._create_from_link(link, soup)
                    if scholarship:
                        scholarships.append(scholarship)
                        if len(scholarships) >= 10:
                            break
        
        except Exception as e:
            print(f"Generic HTML scraping error: {e}")
        
        return scholarships
    
    def _is_scholarship_link(self, text: str) -> bool:
        """Check if link text indicates a scholarship"""
        keywords = ['scholarship', 'fellowship', 'grant', 'funding', 'bursary', 'award']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords) and len(text) > 15
    
    def _create_from_link(self, link, soup) -> Dict:
        """Create scholarship entry from link"""
        title = link.get_text(strip=True)
        url = link.get('href', '')
        
        # Make URL absolute
        if url.startswith('/'):
            base_url = self.url.split('/')[0] + '//' + self.url.split('/')[2]
            url = base_url + url
        
        # Try to find associated content
        parent = link.find_parent(['div', 'article', 'section'])
        content = parent.get_text(strip=True) if parent else ''
        
        return {
            'title': title,
            'country': self._extract_country(content),
            'degree': self._extract_degree(content),
            'field': 'Various',
            'duration': 'Varies',
            'funding': 'See official website',
            'eligibility': 'International students',
            'documents': 'See official website',
            'deadline': self._extract_deadline(content),
            'url': url
        }
    
    def _extract_country(self, text: str) -> str:
        """Extract country from text"""
        countries = {
            'germany': 'Germany', 'usa': 'United States', 'uk': 'United Kingdom',
            'canada': 'Canada', 'australia': 'Australia', 'netherlands': 'Netherlands',
            'sweden': 'Sweden', 'norway': 'Norway', 'denmark': 'Denmark',
            'switzerland': 'Switzerland', 'france': 'France', 'japan': 'Japan',
            'china': 'China', 'singapore': 'Singapore', 'korea': 'South Korea'
        }
        
        text_lower = text.lower()
        for keyword, country in countries.items():
            if keyword in text_lower:
                return country
        
        return 'Various'
    
    def _extract_degree(self, text: str) -> str:
        """Extract degree level from text"""
        text_lower = text.lower()
        
        if 'phd' in text_lower or 'doctoral' in text_lower:
            return 'PhD'
        elif 'master' in text_lower or 'postgraduate' in text_lower:
            return 'Master\'s'
        elif 'bachelor' in text_lower or 'undergraduate' in text_lower:
            return 'Bachelor\'s'
        
        return 'Various levels'
    
    def _extract_funding(self, text: str) -> str:
        """Extract funding information"""
        if 'fully funded' in text.lower() or 'full funding' in text.lower():
            return 'Fully funded'
        elif 'partial' in text.lower():
            return 'Partial funding'
        
        return 'See official website'
    
    def _extract_deadline(self, text: str) -> str:
        """Extract deadline from text"""
        # Date patterns
        patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        if 'rolling' in text.lower():
            return 'Rolling deadline'
        
        return 'Check official website'