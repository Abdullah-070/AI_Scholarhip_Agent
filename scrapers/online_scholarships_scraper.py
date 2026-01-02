# scrapers/online_scholarships_scraper.py - RELIABLE ONLINE SCRAPER

from typing import List, Dict
from scrapers.base_scraper import BaseScraper
import feedparser
import requests
import re

class OnlineScholarshipsScraper(BaseScraper):
    """Scraper for online scholarship databases using APIs and RSS feeds"""

    def scrape(self, profile: Dict) -> List[Dict]:
        """Scrape from multiple online sources"""
        scholarships = []
        
        # Try Scholars4Dev RSS
        scholarships.extend(self._scrape_scholars4dev())
        
        # Try Opportunities Corners RSS
        scholarships.extend(self._scrape_opportunities())
        
        # Try Youth Opportunities RSS
        scholarships.extend(self._scrape_youth_opportunities())
        
        print(f"    ✓ Online Scholarships: {len(scholarships)} scholarships")
        return scholarships if scholarships else self._get_fallback_scholarships()

    def _scrape_scholars4dev(self) -> List[Dict]:
        """Parse Scholars4Dev RSS feed"""
        scholarships = []
        try:
            feed = feedparser.parse("https://www.scholars4dev.com/feed/")
            
            for entry in feed.entries[:20]:  # Limit to 20 latest
                try:
                    scholarship = {
                        'title': entry.get('title', 'Unknown'),
                        'url': entry.get('link', ''),
                        'country': 'Multiple',
                        'degree': 'Various',
                        'field': 'All fields',
                        'funding': 'Partial/Full',
                        'deadline': entry.get('published', 'Rolling'),
                        'eligibility': 'Check website',
                        'documents': 'See official website',
                        'description': entry.get('summary', '')[:200]
                    }
                    
                    # Extract country from description if possible
                    if entry.get('summary'):
                        desc = entry['summary'].lower()
                        if 'germany' in desc or 'daad' in desc:
                            scholarship['country'] = 'Germany'
                        elif 'uk' in desc or 'britain' in desc or 'chevening' in desc:
                            scholarship['country'] = 'United Kingdom'
                        elif 'canada' in desc:
                            scholarship['country'] = 'Canada'
                        elif 'australia' in desc:
                            scholarship['country'] = 'Australia'
                        elif 'usa' in desc or 'united states' in desc or 'fulbright' in desc:
                            scholarship['country'] = 'United States'
                    
                    scholarships.append(scholarship)
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"      Scholars4Dev error: {e}")
        
        return scholarships

    def _scrape_opportunities(self) -> List[Dict]:
        """Parse Opportunities Corners RSS feed"""
        scholarships = []
        try:
            feed = feedparser.parse("https://opportunitiescorners.com/feed/")
            
            for entry in feed.entries[:20]:
                try:
                    scholarship = {
                        'title': entry.get('title', 'Unknown'),
                        'url': entry.get('link', ''),
                        'country': 'Multiple',
                        'degree': 'Various',
                        'field': 'All fields',
                        'funding': 'Varies',
                        'deadline': entry.get('published', 'Rolling'),
                        'eligibility': 'Check website',
                        'documents': 'See official website',
                        'description': entry.get('summary', '')[:200]
                    }
                    
                    scholarships.append(scholarship)
                except:
                    continue
                    
        except Exception as e:
            print(f"      Opportunities Corners error: {e}")
        
        return scholarships

    def _scrape_youth_opportunities(self) -> List[Dict]:
        """Parse Youth Opportunities RSS feed"""
        scholarships = []
        try:
            feed = feedparser.parse("https://www.youthopportunities.com/feed/")
            
            for entry in feed.entries[:20]:
                try:
                    scholarship = {
                        'title': entry.get('title', 'Unknown'),
                        'url': entry.get('link', ''),
                        'country': 'Global',
                        'degree': 'Various',
                        'field': 'Multiple',
                        'funding': 'Varies',
                        'deadline': entry.get('published', 'Rolling'),
                        'eligibility': 'Check website',
                        'documents': 'See official website',
                        'description': entry.get('summary', '')[:200]
                    }
                    
                    scholarships.append(scholarship)
                except:
                    continue
                    
        except Exception as e:
            print(f"      Youth Opportunities error: {e}")
        
        return scholarships

    def _get_fallback_scholarships(self) -> List[Dict]:
        """Fallback scholarships when scraping fails"""
        return [
            {
                'title': 'DAAD Scholarships - Germany',
                'country': 'Germany',
                'degree': "Master's",
                'field': 'All fields',
                'funding': 'Full scholarship',
                'deadline': '2024-12-31',
                'url': 'https://www.daad.de/en/',
                'eligibility': 'Bachelor degree required, English/German language',
                'documents': 'Academic records, language certificate, motivation letter'
            },
            {
                'title': 'Fulbright Foreign Student Program - USA',
                'country': 'United States',
                'degree': "Master's",
                'field': 'All fields',
                'funding': 'Full scholarship',
                'deadline': '2024-10-31',
                'url': 'https://foreign.fulbrightonline.org/',
                'eligibility': 'Bachelor degree, TOEFL/IELTS, work experience preferred',
                'documents': 'Academic transcripts, English language test, CV'
            },
            {
                'title': 'Chevening Scholarships - UK',
                'country': 'United Kingdom',
                'degree': "Master's",
                'field': 'All fields',
                'funding': 'Full scholarship',
                'deadline': '2024-11-07',
                'url': 'https://www.chevening.org/',
                'eligibility': 'Bachelor degree, 2+ years work experience',
                'documents': 'Academic records, employment records, references'
            },
            {
                'title': 'Erasmus Mundus Scholarships - Europe',
                'country': 'Multiple - Europe',
                'degree': "Master's",
                'field': 'All fields',
                'funding': 'Partial/Full',
                'deadline': '2024-12-15',
                'url': 'https://www.erasmusmundus.eu/',
                'eligibility': 'Bachelor degree, language proficiency',
                'documents': 'Transcripts, language certificate, motivation letter'
            }
        ]
