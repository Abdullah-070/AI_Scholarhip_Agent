# ai_engine/data_processor.py

from typing import List, Dict
import hashlib

class DataProcessor:
    """Process and clean scholarship data"""
    
    def process_scholarships(self, scholarships: List[Dict]) -> List[Dict]:
        """
        Process scholarships: clean, deduplicate, validate
        
        Args:
            scholarships: Raw scholarship list
        
        Returns:
            Processed scholarship list
        """
        # Step 1: Remove invalid entries
        valid_scholarships = [s for s in scholarships if self._is_valid(s)]
        
        # Step 2: Deduplicate
        unique_scholarships = self._deduplicate(valid_scholarships)
        
        # Step 3: Standardize fields
        standardized = [self._standardize(s) for s in unique_scholarships]
        
        return standardized
    
    def _is_valid(self, scholarship: Dict) -> bool:
        """Check if scholarship has minimum required data"""
        required = ['title', 'country']
        return all(scholarship.get(field) for field in required)
    
    def _deduplicate(self, scholarships: List[Dict]) -> List[Dict]:
        """Remove duplicate scholarships"""
        seen = set()
        unique = []
        
        for sch in scholarships:
            # Create hash from title and country
            sig = self._create_signature(sch)
            
            if sig not in seen:
                seen.add(sig)
                unique.append(sch)
        
        return unique
    
    def _create_signature(self, scholarship: Dict) -> str:
        """Create unique signature for scholarship"""
        title = scholarship.get('title', '').lower().strip()
        country = scholarship.get('country', '').lower().strip()
        
        # Remove common words
        stop_words = ['scholarship', 'program', 'the', 'and', 'for']
        title_words = [w for w in title.split() if w not in stop_words]
        
        sig_string = ' '.join(title_words[:5]) + country
        return hashlib.md5(sig_string.encode()).hexdigest()
    
    def _standardize(self, scholarship: Dict) -> Dict:
        """Standardize scholarship fields"""
        standardized = scholarship.copy()
        
        # Standardize country names
        standardized['country'] = self._standardize_country(scholarship.get('country', ''))
        
        # Standardize degree levels
        standardized['degree'] = self._standardize_degree(scholarship.get('degree', ''))
        
        # Clean text fields
        for field in ['title', 'field', 'duration', 'funding', 'eligibility', 'documents']:
            if field in standardized:
                standardized[field] = self._clean_text(standardized[field])
        
        # Ensure URL is absolute
        url = standardized.get('url', '')
        if url and not url.startswith('http'):
            standardized['url'] = 'https://' + url
        
        return standardized
    
    def _standardize_country(self, country: str) -> str:
        """Standardize country names"""
        country_map = {
            'usa': 'United States',
            'uk': 'United Kingdom',
            'us': 'United States',
            'britain': 'United Kingdom',
            'deutschland': 'Germany',
        }
        
        country_lower = country.lower().strip()
        return country_map.get(country_lower, country.strip())
    
    def _standardize_degree(self, degree: str) -> str:
        """Standardize degree level names"""
        degree_lower = degree.lower()
        
        if 'bachelor' in degree_lower or 'undergraduate' in degree_lower:
            return "Bachelor's"
        elif 'master' in degree_lower or 'postgraduate' in degree_lower:
            return "Master's"
        elif 'phd' in degree_lower or 'doctoral' in degree_lower or 'doctorate' in degree_lower:
            return 'PhD'
        elif 'postdoc' in degree_lower:
            return 'Postdoctoral'
        
        return degree
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return 'Not specified'
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove HTML entities if any
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        
        return text.strip()