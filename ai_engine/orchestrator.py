# ai_engine/orchestrator.py - WITH DEBUG LOGGING

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
        print("\n" + "="*60)
        print("🚀 STARTING SCHOLARSHIP SEARCH")
        print("="*60)
        print(f"Profile: {profile}")
        print()
        
        # Step 1: Select appropriate scrapers
        scrapers = ScraperFactory.get_scrapers_by_country(profile.get('country', 'Any Country'))
        
        print(f"\n📋 Selected {len(scrapers)} scrapers:")
        for idx, scraper in enumerate(scrapers, 1):
            print(f"  {idx}. {scraper.name}")
        print()
        
        if progress_callback:
            progress_callback("Initializing scrapers...", 0.1)
        
        # Step 2: Execute parallel scraping
        all_scholarships = self._parallel_scrape(scrapers, profile, progress_callback)
        
        print(f"\n📊 RAW RESULTS: {len(all_scholarships)} scholarships scraped")
        
        if progress_callback:
            progress_callback(f"Found {len(all_scholarships)} scholarships", 0.6)
        
        # Step 3: Process and deduplicate
        processed = self.processor.process_scholarships(all_scholarships)
        
        print(f"✅ AFTER PROCESSING: {len(processed)} scholarships (after deduplication)")
        
        if progress_callback:
            progress_callback("Processing results...", 0.8)
        
        # Step 4: Match and rank
        matched = self.matcher.match_and_rank(processed, profile)
        
        print(f"🎯 FINAL MATCHES: {len(matched)} scholarships (after profile matching)")
        print()
        
        if matched:
            print("Top 5 Results:")
            for idx, sch in enumerate(matched[:5], 1):
                print(f"  {idx}. {sch.get('title', 'Unknown')} - {sch.get('match_score', 0):.0f}% match")
        else:
            print("⚠️  WARNING: No scholarships matched the profile!")
        
        print("\n" + "="*60)
        print("✅ SEARCH COMPLETE")
        print("="*60 + "\n")
        
        if progress_callback:
            progress_callback("Complete!", 1.0)
        
        return matched
    
    def _parallel_scrape(self, scrapers: List, profile: Dict, progress_callback=None) -> List[Dict]:
        """Execute scraping in parallel for faster results"""
        all_scholarships = []
        
        # Use ThreadPoolExecutor for parallel scraping
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
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
                    scholarships = future.result(timeout=40)
                    all_scholarships.extend(scholarships)
                    
                    completed += 1
                    result_msg = f"  ✓ {scraper.name}: {len(scholarships)} scholarships"
                    print(result_msg)
                    
                    if progress_callback:
                        progress_pct = 0.1 + (completed / len(scrapers)) * 0.5
                        progress_callback(result_msg, progress_pct)
                        
                except Exception as e:
                    print(f"  ✗ {scraper.name}: FAILED - {str(e)}")
        
        return all_scholarships