# utils/validators.py

from typing import Dict, List, Optional
from datetime import datetime
import validators as val

class InputValidator:
    """Validates user inputs"""
    
    @staticmethod
    def validate_cgpa(cgpa: float) -> bool:
        """Validate CGPA is in valid range"""
        return 0.0 <= cgpa <= 4.0
    
    @staticmethod
    def validate_profile(profile: Dict) -> tuple:
        """Validate complete user profile"""
        errors = []
        
        required_fields = ['degree_level', 'field_of_study', 'nationality', 'country']
        for field in required_fields:
            if not profile.get(field):
                errors.append(f"Missing required field: {field}")
        
        if 'cgpa' in profile:
            if not InputValidator.validate_cgpa(profile['cgpa']):
                errors.append("CGPA must be between 0.0 and 4.0")
        
        return len(errors) == 0, errors


class ScholarshipValidator:
    """Validates scraped scholarship data"""
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        return val.url(url) if url else False
    
    @staticmethod
    def validate_date(date_str: str) -> Optional[datetime]:
        """Parse and validate date string"""
        if not date_str:
            return None
        
        date_formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%B %d, %Y",
            "%d %B %Y",
            "%Y-%m-%dT%H:%M:%S",
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    @staticmethod
    def validate_scholarship(data: Dict) -> tuple:
        """Validate and clean scholarship data"""
        required_fields = ['title', 'country']
        
        cleaned = {}
        
        # Check required fields
        for field in required_fields:
            if field not in data or not data[field]:
                return False, {}
        
        # Clean and validate fields
        cleaned['title'] = str(data.get('title', '')).strip()
        cleaned['country'] = str(data.get('country', '')).strip()
        cleaned['degree'] = str(data.get('degree', 'Not specified')).strip()
        cleaned['field'] = str(data.get('field', 'All fields')).strip()
        cleaned['duration'] = str(data.get('duration', 'Not specified')).strip()
        cleaned['funding'] = str(data.get('funding', 'Not specified')).strip()
        cleaned['eligibility'] = str(data.get('eligibility', 'Not specified')).strip()
        cleaned['documents'] = str(data.get('documents', 'See official website')).strip()
        
        # Validate and clean URL
        url = data.get('url', '')
        if ScholarshipValidator.validate_url(url):
            cleaned['url'] = url
        else:
            cleaned['url'] = 'Not available'
        
        # Validate deadline
        deadline = data.get('deadline', '')
        parsed_date = ScholarshipValidator.validate_date(deadline)
        if parsed_date:
            cleaned['deadline'] = parsed_date.strftime("%Y-%m-%d")
        else:
            cleaned['deadline'] = deadline if deadline else 'Rolling/Not specified'
        
        return True, cleaned