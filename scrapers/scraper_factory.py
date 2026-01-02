# scrapers/scraper_factory.py - WITH HYBRID SCRAPER SUPPORT

from typing import Dict, List
from scrapers.base_scraper import BaseScraper
from scrapers.hybrid_scraper import HybridScraper
from scrapers.specialized_hybrids import (
    DAADHybrid,
    HECHybrid,
    Scholars4DevHybrid,
    ScholarshipPortalHybrid
)
from scrapers.chevening_scraper import CheveningScraper
from scrapers.fulbright_scraper import FulbrightScraper
from scrapers.commonwealth_scraper import CommonwealthScraper
from scrapers.erasmus_scraper import ErasmusScraper
from scrapers.generic_scraper import GenericScraper
from config.sources import SCHOLARSHIP_SOURCES

class ScraperFactory:
    """Factory for creating and managing scrapers with hybrid support"""
    
    # Map source names to specialized scraper classes
    SCRAPER_MAP = {
        # Hybrid scrapers (API + RSS + HTML + Selenium + Fallback)
        'daad': DAADHybrid,
        'hec': HECHybrid,
        'scholars4dev': Scholars4DevHybrid,
        'scholarshipportal': ScholarshipPortalHybrid,
        'opportunitiescorners': HybridScraper,  # Generic hybrid
        'youthopportunities': HybridScraper,    # Generic hybrid
        
        # Simple HTML scrapers
        'chevening': CheveningScraper,
        'fulbright': FulbrightScraper,
        'commonwealth': CommonwealthScraper,
        'erasmus': ErasmusScraper,
    }
    
    @staticmethod
    def create_scraper(source_name: str) -> BaseScraper:
        """Create scraper instance based on source name"""
        source_config = SCHOLARSHIP_SOURCES.get(source_name)
        
        if not source_config:
            raise ValueError(f"Unknown source: {source_name}")
        
        # Get specific scraper class or use GenericScraper
        scraper_class = ScraperFactory.SCRAPER_MAP.get(source_name, GenericScraper)
        
        try:
            scraper = scraper_class(source_config)
            return scraper
        except Exception as e:
            print(f"⚠️  Failed to create {source_name} scraper: {e}")
            # Fallback to GenericScraper
            return GenericScraper(source_config)
    
    @staticmethod
    def get_all_scrapers() -> List[BaseScraper]:
        """Get all enabled scrapers"""
        scrapers = []
        
        print("\n🔧 INITIALIZING SCRAPERS:")
        print("="*60)
        
        for source_name, config in SCHOLARSHIP_SOURCES.items():
            if config.get('enabled', False):
                try:
                    scraper = ScraperFactory.create_scraper(source_name)
                    scrapers.append(scraper)
                    
                    # Show scraper capabilities
                    capabilities = []
                    if isinstance(scraper, HybridScraper) or source_name in ['daad', 'hec', 'scholars4dev', 'scholarshipportal']:
                        if config.get('api_endpoint'):
                            capabilities.append('API')
                        if config.get('rss_feed'):
                            capabilities.append('RSS')
                        capabilities.append('HTML')
                        if config.get('use_selenium'):
                            capabilities.append('Selenium')
                        capabilities.append('Fallback')
                    else:
                        capabilities.append('HTML')
                    
                    cap_str = ' → '.join(capabilities)
                    print(f"  ✅ {scraper.name}")
                    print(f"     Methods: {cap_str}")
                
                except Exception as e:
                    print(f"  ❌ {source_name}: {e}")
        
        # Sort by priority
        scrapers.sort(key=lambda s: SCHOLARSHIP_SOURCES.get(
            [k for k, v in SCHOLARSHIP_SOURCES.items() if v.get('name') == s.name][0],
            {}
        ).get('priority', 99))
        
        print(f"\n📊 Total active scrapers: {len(scrapers)}")
        print("="*60 + "\n")
        
        return scrapers
    
    @staticmethod
    def get_scrapers_by_country(country: str) -> List[BaseScraper]:
        """Get scrapers relevant to specific country"""
        all_scrapers = ScraperFactory.get_all_scrapers()
        
        # Country-specific filtering
        country_map = {
            'Germany': ['daad'],
            'United Kingdom': ['chevening', 'commonwealth'],
            'United States': ['fulbright'],
            'Pakistan': ['hec'],
        }
        
        if country == 'Any Country':
            print(f"🌍 Using all {len(all_scrapers)} scrapers for 'Any Country'\n")
            return all_scrapers
        
        preferred_sources = country_map.get(country, [])
        
        # Prioritize country-specific scrapers
        prioritized = []
        others = []
        
        for scraper in all_scrapers:
            is_preferred = any(pref in scraper.name.lower() for pref in preferred_sources)
            
            if is_preferred:
                prioritized.append(scraper)
            else:
                others.append(scraper)
        
        result = prioritized + others
        print(f"🎯 Selected {len(result)} scrapers for {country}")
        if prioritized:
            print(f"   Priority: {', '.join([s.name for s in prioritized])}")
        print()
        
        return result