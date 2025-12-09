# ai_engine/matcher.py

from typing import Dict, List
import re

class ProfileMatcher:
    """Intelligent profile matching and ranking"""
    
    def match_and_rank(self, scholarships: List[Dict], profile: Dict) -> List[Dict]:
        """
        Match scholarships to profile and rank by relevance
        
        Args:
            scholarships: List of scholarship dictionaries
            profile: User profile
        
        Returns:
            Ranked list of scholarships
        """
        scored_scholarships = []
        
        for scholarship in scholarships:
            score = self._calculate_match_score(scholarship, profile)
            scholarship['match_score'] = score
            scored_scholarships.append(scholarship)
        
        # Sort by match score (descending)
        scored_scholarships.sort(key=lambda x: x['match_score'], reverse=True)
        
        return scored_scholarships
    
    def _calculate_match_score(self, scholarship: Dict, profile: Dict) -> float:
        """Calculate relevance score (0-100)"""
        score = 0.0
        
        # Country match (30 points)
        score += self._score_country(scholarship, profile)
        
        # Degree level match (25 points)
        score += self._score_degree(scholarship, profile)
        
        # Field of study match (20 points)
        score += self._score_field(scholarship, profile)
        
        # CGPA/eligibility match (15 points)
        score += self._score_cgpa(scholarship, profile)
        
        # Funding coverage (10 points)
        score += self._score_funding(scholarship)
        
        return min(score, 100.0)
    
    def _score_country(self, scholarship: Dict, profile: Dict) -> float:
        """Score country match"""
        desired_country = profile.get('country', 'Any Country')
        sch_country = scholarship.get('country', '').lower()
        
        if desired_country == 'Any Country':
            return 15.0  # Neutral score
        
        if desired_country.lower() in sch_country:
            return 30.0
        elif 'various' in sch_country or 'multiple' in sch_country:
            return 20.0
        
        return 5.0
    
    def _score_degree(self, scholarship: Dict, profile: Dict) -> float:
        """Score degree level match"""
        desired_degree = profile.get('degree_level', '').lower()
        sch_degree = scholarship.get('degree', '').lower()
        
        if not desired_degree or not sch_degree:
            return 10.0
        
        # Exact match
        if desired_degree in sch_degree:
            return 25.0
        
        # Partial matches
        degree_keywords = {
            "bachelor": ["undergraduate", "bachelor"],
            "master": ["master", "graduate", "postgraduate"],
            "phd": ["phd", "doctoral", "doctorate"],
            "postdoctoral": ["postdoc", "postdoctoral"]
        }
        
        for key, keywords in degree_keywords.items():
            if key in desired_degree:
                if any(kw in sch_degree for kw in keywords):
                    return 20.0
        
        # Generic levels
        if 'all' in sch_degree or 'various' in sch_degree:
            return 12.0
        
        return 5.0
    
    def _score_field(self, scholarship: Dict, profile: Dict) -> float:
        """Score field of study match"""
        desired_field = profile.get('field_of_study', 'All Fields').lower()
        sch_field = scholarship.get('field', '').lower()
        
        if desired_field == 'all fields' or 'all' in sch_field:
            return 10.0
        
        # Extract key terms
        desired_terms = set(re.findall(r'\w+', desired_field))
        sch_terms = set(re.findall(r'\w+', sch_field))
        
        # Check overlap
        overlap = desired_terms.intersection(sch_terms)
        
        if len(overlap) > 0:
            return 20.0
        
        # Check for related fields
        field_groups = {
            'engineering': ['technology', 'technical', 'stem'],
            'computer': ['it', 'technology', 'data', 'software'],
            'science': ['natural', 'stem', 'research'],
            'business': ['management', 'mba', 'commerce'],
            'medical': ['health', 'medicine', 'clinical']
        }
        
        for key, related in field_groups.items():
            if key in desired_field:
                if any(r in sch_field for r in related):
                    return 15.0
        
        return 5.0
    
    def _score_cgpa(self, scholarship: Dict, profile: Dict) -> float:
        """Score based on CGPA requirements"""
        cgpa = profile.get('cgpa', 0.0)
        
        if cgpa >= 3.5:
            return 15.0
        elif cgpa >= 3.0:
            return 12.0
        elif cgpa >= 2.5:
            return 8.0
        
        return 5.0
    
    def _score_funding(self, scholarship: Dict) -> float:
        """Score based on funding coverage"""
        funding = scholarship.get('funding', '').lower()
        
        if 'full' in funding or 'fully funded' in funding:
            return 10.0
        elif 'partial' in funding:
            return 6.0
        
        return 3.0