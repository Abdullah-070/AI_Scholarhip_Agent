# scrapers/base_scraper.py

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.validators import ScholarshipValidator

class BaseScraper(ABC):
    """Abstract base class for all scholarship scrapers"""
    
    def __init__(self, source_config: Dict):
        self.name = source_config.get('name', 'Unknown Source')
        self.url = source_config.get('url', '')
        self.enabled = source_config.get('enabled', True)
        self.validator = ScholarshipValidator()
        
        # FIX: Use a standard requests.Session instead of AntiBlockSession
        # This ensures .headers and .mount attributes exist
        self.session = requests.Session()
        self._configure_robust_session()

    def _configure_robust_session(self):
        """Configures the session with retries and browser-like headers"""
        # Retry strategy: 3 retries, backoff factor (wait 1s, 2s, 4s...)
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        
        # Mount adapters
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Add headers to look like a real browser (Anti-blocking technique)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }
        self.session.headers.update(headers)
    
    @abstractmethod
    def scrape(self, profile: Dict) -> List[Dict]:
        """
        Main scraping method to be implemented by each scraper
        
        Args:
            profile: User profile with degree_level, field_of_study, nationality, country, cgpa
        
        Returns:
            List of scholarship dictionaries
        """
        pass
    
    def validate_and_clean(self, scholarships: List[Dict]) -> List[Dict]:
        """Validate and clean scraped scholarships"""
        cleaned = []
        for sch in scholarships:
            is_valid, cleaned_sch = self.validator.validate_scholarship(sch)
            if is_valid:
                cleaned.append(cleaned_sch)
        return cleaned
    
    def match_profile(self, scholarships: List[Dict], profile: Dict) -> List[Dict]:
        """Filter scholarships based on user profile"""
        matched = []
        
        for sch in scholarships:
            if self._is_match(sch, profile):
                matched.append(sch)
        
        return matched
    
    def _is_match(self, scholarship: Dict, profile: Dict) -> bool:
        """Check if scholarship matches user profile"""
        # Degree level matching
        degree = profile.get('degree_level', '')
        sch_degree = scholarship.get('degree', 'All levels')
        if degree and sch_degree != 'All levels' and sch_degree != 'Not specified':
            if degree.lower() not in sch_degree.lower():
                return False
        
        # Country matching
        desired_country = profile.get('country', 'Any Country')
        sch_country = scholarship.get('country', '')
        if desired_country != 'Any Country' and sch_country:
            if desired_country.lower() not in sch_country.lower():
                return False
        
        # Field of study matching
        field = profile.get('field_of_study', 'All Fields')
        sch_field = scholarship.get('field', 'All fields')
        if field != 'All Fields' and sch_field != 'All fields':
            # Partial match for field
            if field.lower().split()[0] not in sch_field.lower():
                return False
        
        return True
    
    def get_scholarships(self, profile: Dict) -> List[Dict]:
        """Main entry point - scrape, validate, and match"""
        if not self.enabled:
            return []
        
        try:
            raw_scholarships = self.scrape(profile)
            cleaned_scholarships = self.validate_and_clean(raw_scholarships)
            matched_scholarships = self.match_profile(cleaned_scholarships, profile)
            return matched_scholarships
        except Exception as e:
            print(f"Error in {self.name}: {str(e)}")
            return []
    
    def __del__(self):
        """Cleanup session on deletion"""
        if hasattr(self, 'session'):
            try:
                self.session.close()
            except:
                pass