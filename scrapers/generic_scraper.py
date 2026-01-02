# scrapers/generic_scraper.py - ENHANCED VERSION

from typing import List, Dict
from scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import feedparser
import re

class GenericScraper(BaseScraper):
    """Enhanced generic scraper for scholarship sources"""
    
    def scrape(self, profile: Dict) -> List[Dict]:
        """Scrape using multiple methods"""
        scholarships = []
        
        print(f"🔍 Scraping {self.name}...")
        
        # Method 1: Try RSS feed
        rss_scholarships = self._scrape_rss()
        if rss_scholarships:
            scholarships.extend(rss_scholarships)
            print(f"  📰 RSS: Found {len(rss_scholarships)} scholarships")
        
        # Method 2: Try HTML scraping
        if len(scholarships) < 10:
            html_scholarships = self._scrape_html(profile)
            if html_scholarships:
                scholarships.extend(html_scholarships)
                print(f"  🌐 HTML: Found {len(html_scholarships)} scholarships")
        
        # Method 3: Generate sample scholarships for sources without accessible data
        if len(scholarships) < 3:
            sample_scholarships = self._generate_sample_scholarships()
            scholarships.extend(sample_scholarships)
            print(f"  📋 Sample: Added {len(sample_scholarships)} entries")
        
        print(f"✅ {self.name}: Total {len(scholarships)} scholarships")
        return scholarships[:20]  # Limit results
    
    def _scrape_rss(self) -> List[Dict]:
        """Scrape scholarships from RSS feeds"""
        scholarships = []
        
        # Try RSS feeds
        rss_feeds = [
            'https://www.scholars4dev.com/feed/',
            'https://opportunitiescorners.info/feed/',
            'https://www.youthopportunities.com/feed/',
        ]
        
        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:10]:
                    scholarship = self._parse_rss_entry(entry)
                    if scholarship:
                        scholarships.append(scholarship)
            except Exception as e:
                print(f"    RSS feed error ({feed_url}): {e}")
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
            'field': self._extract_field(text_content),
            'duration': self._extract_duration(text_content),
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
            response = self.session.get(self.url, timeout=30, verify=False)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Find potential scholarship links
            links = soup.find_all('a', href=True)
            
            for link in links:
                text = link.get_text(strip=True)
                if self._is_scholarship_link(text):
                    scholarship = self._create_from_link(link, soup)
                    if scholarship:
                        scholarships.append(scholarship)
                        if len(scholarships) >= 15:
                            break
        
        except Exception as e:
            print(f"    HTML scraping error: {e}")
        
        return scholarships
    
    def _is_scholarship_link(self, text: str) -> bool:
        """Check if link text indicates a scholarship"""
        keywords = ['scholarship', 'fellowship', 'grant', 'funding', 'bursary', 'award', 'stipend']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords) and len(text) > 10
    
    def _create_from_link(self, link, soup) -> Dict:
        """Create scholarship entry from link"""
        title = link.get_text(strip=True)
        url = link.get('href', '')
        
        # Make URL absolute
        if url.startswith('/'):
            from urllib.parse import urlparse
            parsed = urlparse(self.url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            url = base_url + url
        elif not url.startswith('http'):
            url = self.url
        
        # Try to find associated content
        parent = link.find_parent(['div', 'article', 'section', 'li'])
        content = parent.get_text(strip=True) if parent else title
        
        return {
            'title': title,
            'country': self._extract_country(content),
            'degree': self._extract_degree(content),
            'field': self._extract_field(content),
            'duration': self._extract_duration(content),
            'funding': self._extract_funding(content),
            'eligibility': 'International students',
            'documents': 'See official website',
            'deadline': self._extract_deadline(content),
            'url': url
        }
    
    def _generate_sample_scholarships(self) -> List[Dict]:
        """Generate sample scholarships when scraping fails"""
        source_samples = {
            "ScholarshipPortal": {
                'country': 'Europe (Multiple)',
                'degree': 'Master\'s/PhD',
                'field': 'All fields',
                'funding': 'Varies (€500 - Full funding)'
            },
            "Scholars4Dev": {
                'country': 'Various',
                'degree': 'All levels',
                'field': 'All fields',
                'funding': 'Full or partial funding'
            },
            "default": {
                'country': 'Various',
                'degree': 'Master\'s/PhD',
                'field': 'All fields',
                'funding': 'See official website'
            }
        }
        
        # Find matching template
        template = source_samples.get("default")
        for key, data in source_samples.items():
            if key.lower() in self.name.lower():
                template = data
                break
        
        return [
            {
                'title': f'{self.name} - Check Official Website for Current Opportunities',
                'country': template['country'],
                'degree': template['degree'],
                'field': template['field'],
                'duration': 'Varies',
                'funding': template['funding'],
                'eligibility': 'See official website for requirements',
                'documents': 'Visit official portal for details',
                'deadline': 'Multiple deadlines throughout the year',
                'url': self.url
            }
        ]
    
    def _extract_country(self, text: str) -> str:
        """Extract country from text"""
        countries = {
            'germany': 'Germany', 'usa': 'United States', 'america': 'United States',
            'uk': 'United Kingdom', 'britain': 'United Kingdom', 'england': 'United Kingdom',
            'canada': 'Canada', 'australia': 'Australia', 'netherlands': 'Netherlands',
            'sweden': 'Sweden', 'norway': 'Norway', 'denmark': 'Denmark',
            'switzerland': 'Switzerland', 'france': 'France', 'japan': 'Japan',
            'china': 'China', 'singapore': 'Singapore', 'korea': 'South Korea',
            'europe': 'Europe (Multiple)', 'european': 'Europe (Multiple)'
        }
        
        text_lower = text.lower()
        for keyword, country in countries.items():
            if keyword in text_lower:
                return country
        
        return 'Various'
    
    def _extract_degree(self, text: str) -> str:
        """Extract degree level from text"""
        text_lower = text.lower()
        
        if 'phd' in text_lower or 'doctoral' in text_lower or 'doctorate' in text_lower:
            return 'PhD'
        elif 'master' in text_lower or 'postgraduate' in text_lower or 'graduate' in text_lower:
            return 'Master\'s'
        elif 'bachelor' in text_lower or 'undergraduate' in text_lower:
            return 'Bachelor\'s'
        elif 'postdoc' in text_lower:
            return 'Postdoctoral'
        
        return 'Various levels'
    
    def _extract_field(self, text: str) -> str:
        """Extract field of study from text"""
        fields = {
            'engineering': 'Engineering & Technology',
            'computer': 'Computer Science & IT',
            'business': 'Business & Management',
            'medicine': 'Medicine & Health Sciences',
            'science': 'Natural Sciences',
            'social': 'Social Sciences',
            'arts': 'Arts & Humanities',
            'law': 'Law',
            'education': 'Education',
        }
        
        text_lower = text.lower()
        for keyword, field in fields.items():
            if keyword in text_lower:
                return field
        
        return 'All fields'
    
    def _extract_duration(self, text: str) -> str:
        """Extract duration from text"""
        # Look for duration patterns
        duration_patterns = [
            r'(\d+)\s*year',
            r'(\d+)\s*month',
            r'(\d+-\d+)\s*year',
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(0)
        
        return 'Varies'
    
    def _extract_funding(self, text: str) -> str:
        """Extract funding information"""
        text_lower = text.lower()
        
        if 'fully funded' in text_lower or 'full funding' in text_lower or 'full scholarship' in text_lower:
            return 'Fully funded'
        elif 'partial' in text_lower:
            return 'Partial funding'
        elif 'tuition' in text_lower:
            if 'waiver' in text_lower:
                return 'Tuition waiver'
            return 'Tuition coverage'
        elif 'stipend' in text_lower:
            return 'Monthly stipend provided'
        
        return 'See official website'
    
    def _extract_deadline(self, text: str) -> str:
        """Extract deadline from text"""
        # Date patterns
        patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',
            r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        if 'rolling' in text.lower():
            return 'Rolling deadline'
        
        if 'open' in text.lower():
            return 'Currently open'
        
        return 'Check official website'