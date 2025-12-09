# ai_engine/orchestrator.py

from typing import Dict, List
from scrapers.scraper_factory import ScraperFactory
from ai_engine.matcher import ProfileMatcher
from ai_engine.data_processor import DataProcessor
import concurrent.futures

class AIOrchestrator:
    """Main AI orchestration engine for scholarship search"""
    
    def __init__(self):
        self.matcher = ProfileMatcher()
        self.processor = DataProcessor()
    
    def search_scholarships(self, profile: Dict, progress_callback=None) -> List[Dict]:
        """
        Main orchestration method for scholarship search
        
        Args:
            profile: User profile dictionary
            progress_callback: Optional callback for progress updates
        
        Returns:
            List of matched and ranked scholarships
        """
        # Step 1: Select appropriate scrapers
        scrapers = ScraperFactory.get_scrapers_by_country(profile.get('country', 'Any Country'))
        
        if progress_callback:
            progress_callback("Initializing scrapers...", 0.1)
        
        # Step 2: Execute parallel scraping
        all_scholarships = self._parallel_scrape(scrapers, profile, progress_callback)
        
        if progress_callback:
            progress_callback(f"Found {len(all_scholarships)} scholarships", 0.6)
        
        # Step 3: Process and deduplicate
        processed = self.processor.process_scholarships(all_scholarships)
        
        if progress_callback:
            progress_callback("Processing results...", 0.8)
        
        # Step 4: Match and rank
        matched = self.matcher.match_and_rank(processed, profile)
        
        if progress_callback:
            progress_callback("Complete!", 1.0)
        
        return matched
    
    def _parallel_scrape(self, scrapers: List, profile: Dict, progress_callback=None) -> List[Dict]:
        """Execute scraping in parallel for faster results"""
        all_scholarships = []
        
        # Use ThreadPoolExecutor for parallel scraping
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all scraping tasks
            future_to_scraper = {
                executor.submit(scraper.get_scholarships, profile): scraper 
                for scraper in scrapers
            }
            
            # Collect results as they complete
            completed = 0
            for future in concurrent.futures.as_completed(future_to_scraper):
                scraper = future_to_scraper[future]
                try:
                    scholarships = future.result(timeout=30)
                    all_scholarships.extend(scholarships)
                    
                    completed += 1
                    if progress_callback:
                        progress_pct = 0.1 + (completed / len(scrapers)) * 0.5
                        progress_callback(
                            f"Scraped {scraper.name}: {len(scholarships)} found",
                            progress_pct
                        )
                except Exception as e:
                    print(f"Scraper {scraper.name} failed: {e}")
        
        return all_scholarships