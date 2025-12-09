# scrapers/scraper_factory.py

from typing import Dict, List
from scrapers.base_scraper import BaseScraper
from scrapers.daad_scraper import DAADScraper
from scrapers.hec_scraper import HECScraper
from scrapers.generic_scraper import GenericScraper
from config.sources import SCHOLARSHIP_SOURCES
from scrapers.additional_scholarship_scrapers import (
    CheveningScraper,
    FulbrightScraper,
    CommonwealthScraper,
    ErasmusScraper,
    CSCChinaScraper,
    MEXTJapanScraper,
    SwedishInstituteScraper,
    AustraliaAwardsScraper,
    VanierCanadaScraper,
    GatesCambridgeScraper
)


class ScraperFactory:
    """Factory for creating and managing scrapers"""
    
    @staticmethod
    def create_scraper(source_name: str) -> BaseScraper:
        """Create scraper instance based on source name"""
        source_config = SCHOLARSHIP_SOURCES.get(source_name)
        
        if not source_config:
            raise ValueError(f"Unknown source: {source_name}")
        
        # Map to specific scraper classes
        scraper_map = {
            'daad': DAADScraper,
            'hec': HECScraper,
        }
        
        scraper_class = scraper_map.get(source_name, GenericScraper)
        return scraper_class(source_config)
    
    @staticmethod
    def get_all_scrapers() -> List[BaseScraper]:
        """Get all enabled scrapers"""
        scrapers = []
        
        for source_name, config in SCHOLARSHIP_SOURCES.items():
            if config.get('enabled', False):
                try:
                    scraper = ScraperFactory.create_scraper(source_name)
                    scrapers.append(scraper)
                except Exception as e:
                    print(f"Failed to create scraper for {source_name}: {e}")
        
        # Sort by priority
        scrapers.sort(key=lambda s: SCHOLARSHIP_SOURCES.get(
            s.name.lower().replace(' ', '_').split('(')[0].strip(), {}
        ).get('priority', 99))
        
        return scrapers
    
    @staticmethod
    def get_scrapers_by_country(country: str) -> List[BaseScraper]:
        """Get scrapers relevant to specific country"""
        all_scrapers = ScraperFactory.get_all_scrapers()
        
        # Country-specific filtering logic
        country_map = {
            'Germany': ['daad'],
            'Pakistan': ['hec'],
        }
        
        if country == 'Any Country':
            return all_scrapers
        
        preferred_sources = country_map.get(country, [])
        
        # Prioritize country-specific scrapers
        prioritized = []
        others = []
        
        for scraper in all_scrapers:
            source_key = scraper.name.lower().split()[0]
            if source_key in preferred_sources:
                prioritized.append(scraper)
            else:
                others.append(scraper)
        
        return prioritized + others