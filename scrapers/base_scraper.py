# scrapers/base_scraper.py - FIXED WITH RELAXED MATCHING

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
        
        # Use a standard requests.Session
        self.session = requests.Session()
        self._configure_robust_session()

    def _configure_robust_session(self):
        """Configures the session with retries and browser-like headers"""
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
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
        """Filter scholarships based on user profile - RELAXED VERSION"""
        # If "All Fields" and "Any Country" selected, return everything
        field = profile.get('field_of_study', 'All Fields')
        country = profile.get('country', 'Any Country')
        
        if field == 'All Fields' and country == 'Any Country':
            print(f"    ℹ️  {self.name}: Returning all {len(scholarships)} scholarships (no filters)")
            return scholarships
        
        # Otherwise, apply relaxed matching
        matched = []
        for sch in scholarships:
            if self._is_match(sch, profile):
                matched.append(sch)
        
        if len(matched) < len(scholarships):
            print(f"    ℹ️  {self.name}: Filtered {len(scholarships)} → {len(matched)} scholarships")
        
        return matched
    
    def _is_match(self, scholarship: Dict, profile: Dict) -> bool:
        """Check if scholarship matches user profile - RELAXED VERSION"""
        
        # 1. Country matching (relaxed)
        desired_country = profile.get('country', 'Any Country')
        sch_country = scholarship.get('country', '').lower()
        
        if desired_country != 'Any Country':
            # Accept if scholarship country contains desired country OR is "Various"
            if desired_country.lower() not in sch_country and \
               'various' not in sch_country and \
               'multiple' not in sch_country and \
               'all' not in sch_country and \
               sch_country != '':
                return False
        
        # 2. Degree level matching (relaxed)
        degree = profile.get('degree_level', '')
        sch_degree = scholarship.get('degree', '').lower()
        
        if degree and sch_degree:
            # Skip matching if scholarship accepts all levels
            if 'all' in sch_degree or 'various' in sch_degree or 'not specified' in sch_degree:
                pass  # Accept
            # Only reject if completely mismatched
            elif degree.lower() not in sch_degree and \
                 not any(keyword in sch_degree for keyword in self._get_degree_keywords(degree)):
                return False
        
        # 3. Field of study matching (very relaxed)
        field = profile.get('field_of_study', 'All Fields')
        sch_field = scholarship.get('field', '').lower()
        
        if field != 'All Fields' and sch_field:
            # Accept if "all fields" or contains any keyword from the field
            if 'all' not in sch_field:
                field_keywords = field.lower().split()
                if not any(keyword in sch_field for keyword in field_keywords):
                    return False
        
        return True
    
    def _get_degree_keywords(self, degree: str) -> List[str]:
        """Get related keywords for degree level"""
        mapping = {
            "Bachelor's": ["bachelor", "undergraduate", "bsc", "ba"],
            "Master's": ["master", "postgraduate", "graduate", "msc", "ma", "mphil"],
            "PhD": ["phd", "doctoral", "doctorate"],
            "Postdoctoral": ["postdoc", "postdoctoral"],
            "Short Course": ["course", "training", "workshop"]
        }
        return mapping.get(degree, [degree.lower()])
    
    def get_scholarships(self, profile: Dict) -> List[Dict]:
        """Main entry point - scrape, validate, and match"""
        if not self.enabled:
            return []
        
        try:
            print(f"  🔍 Scraping {self.name}...")
            raw_scholarships = self.scrape(profile)
            print(f"    📊 Raw: {len(raw_scholarships)} scholarships")
            
            cleaned_scholarships = self.validate_and_clean(raw_scholarships)
            print(f"    ✓ Validated: {len(cleaned_scholarships)} scholarships")
            
            matched_scholarships = self.match_profile(cleaned_scholarships, profile)
            print(f"    ✓ Matched: {len(matched_scholarships)} scholarships")
            
            return matched_scholarships
        except Exception as e:
            print(f"    ✗ ERROR in {self.name}: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def __del__(self):
        """Cleanup session on deletion"""
        if hasattr(self, 'session'):
            try:
                self.session.close()
            except:
                pass