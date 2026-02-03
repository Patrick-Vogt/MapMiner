import sys
import os

# Add parent directory to path to import scrapers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maps_scraper_configurable import MapMiner
from website_scraper_configurable import WebsiteScraperConfigurable
import time

class ScraperOrchestrator:
    """Orchestrates the two-stage scraping process"""
    
    def __init__(self, config, progress_callback=None):
        """
        Initialize orchestrator with configuration
        
        Args:
            config: Dictionary containing:
                - search_term: Search term (e.g., "Autohaus")
                - cities: List of cities or comma-separated string
                - entries_per_city: Max results per city
                - required_words: Words that must be in company name (comma-separated)
                - output_path: Where to save CSV
                - delay_min: Minimum delay between requests (default: 2)
                - delay_max: Maximum delay between requests (default: 5)
                - scroll_delay_min: Min scroll delay (default: 3)
                - scroll_delay_max: Max scroll delay (default: 7)
                - click_delay_min: Min click delay (default: 3)
                - click_delay_max: Max click delay (default: 7)
                - headless: Run browser in headless mode (default: False)
                - use_chrome: Use Chrome instead of Edge (default: False)
                - max_workers: Max parallel workers for website scraping (default: 10)
                - run_stage_2: Whether to run website enrichment (default: True)
            progress_callback: Callback object with emit methods for progress updates
        """
        self.config = config
        self.progress = progress_callback
        
        # Parse cities if string
        if isinstance(config['cities'], str):
            self.cities = [city.strip() for city in config['cities'].split(',') if city.strip()]
        else:
            self.cities = config['cities']
        
        # Parse required_words if string
        required_words_str = config.get('required_words', '')
        if isinstance(required_words_str, str) and required_words_str.strip():
            self.required_words = [word.strip() for word in required_words_str.split(',') if word.strip()]
        else:
            self.required_words = []
        
        self.search_term = config['search_term']
        self.entries_per_city = config.get('entries_per_city', 20)
        self.output_path = config['output_path']
        self.browser = config.get('browser', 'safari')
        self.max_workers = config.get('max_workers', 10)
        self.run_stage_2 = config.get('run_stage_2', True)
        self.require_website = config.get('require_website', True)
        
        # Delays configuration
        self.delays = {
            'delay_min': config.get('delay_min', 2),
            'delay_max': config.get('delay_max', 5),
            'scroll_delay_min': config.get('scroll_delay_min', 3),
            'scroll_delay_max': config.get('scroll_delay_max', 7),
            'click_delay_min': config.get('click_delay_min', 3),
            'click_delay_max': config.get('click_delay_max', 7)
        }
    
    def log(self, message, level='info'):
        """Log message via progress callback"""
        if self.progress:
            self.progress.emit_log(message, level)
        else:
            print(message)
    
    def update_status(self, **kwargs):
        """Update status via progress callback"""
        if self.progress:
            self.progress.update_status(**kwargs)
    
    def run_stage_1_maps_scraping(self):
        """Stage 1: Scrape Google Maps for basic business information"""
        self.log('📍 Stage 1: Starting Google Maps scraping...', 'info')
        self.update_status(stage='maps_scraping', progress=0, total=len(self.cities))
        
        try:
            # Initialize MapMiner scraper
            scraper = MapMiner(
                csv_filename=self.output_path,
                browser=self.browser,
                delays=self.delays,
                required_words=self.required_words,
                require_website=self.require_website
            )
            
            self.log(f'✓ Browser initialized: {self.browser.capitalize()}', 'info')
            
            total_scraped = 0
            
            for idx, city in enumerate(self.cities, 1):
                self.update_status(
                    progress=idx,
                    current_item=f'Scraping {city}'
                )
                
                query = f"{self.search_term} {city}, Deutschland"
                self.log(f'🔍 [{idx}/{len(self.cities)}] Searching: {query}', 'info')
                
                # Search location
                scraper.search_location(query)
                
                # Scroll to load more results
                scraper.scroll_results(max_scrolls=5)
                
                # Scrape listings
                results = scraper.scrape_listings(max_results=self.entries_per_city)
                total_scraped += len(results)
                
                self.log(f'✓ [{idx}/{len(self.cities)}] {city}: Scraped {len(results)} listings', 'success')
                self.update_status(stats={'maps_scraped': total_scraped})
                
                # Delay between cities
                if idx < len(self.cities):
                    time.sleep(self.delays['delay_min'])
            
            # Close browser
            scraper.close()
            
            self.log(f'✅ Stage 1 completed: {total_scraped} total listings scraped', 'success')
            return total_scraped
            
        except Exception as e:
            self.log(f'❌ Stage 1 error: {str(e)}', 'error')
            raise
    
    def run_stage_2_website_enrichment(self):
        """Stage 2: Enrich data with email and owner information from websites"""
        self.log('🌐 Stage 2: Starting website enrichment...', 'info')
        self.update_status(stage='website_enrichment', progress=0, total=0)
        
        try:
            # Initialize Website scraper
            scraper = WebsiteScraperConfigurable(
                csv_filename=self.output_path,
                max_workers=self.max_workers,
                delays=self.delays,
                progress_callback=self.progress
            )
            
            self.log(f'✓ Website scraper initialized ({self.max_workers} parallel workers)', 'info')
            
            # Process businesses
            stats = scraper.process_businesses()
            
            self.log(f'✅ Stage 2 completed: {stats["processed"]} websites processed', 'success')
            self.update_status(stats={
                'websites_scraped': stats['processed'],
                'emails_found': stats.get('emails_found', 0),
                'owners_found': stats.get('owners_found', 0)
            })
            
            return stats
            
        except Exception as e:
            self.log(f'❌ Stage 2 error: {str(e)}', 'error')
            raise
    
    def run(self):
        """Run the complete two-stage scraping process"""
        self.log('🚀 Starting two-stage scraping process...', 'info')
        self.log('Configuration:', 'info')
        self.log(f'   Search term: {self.search_term}', 'info')
        self.log(f'   Cities: {", ".join(self.cities)}', 'info')
        self.log(f'   Entries per city: {self.entries_per_city}', 'info')
        if self.required_words:
            self.log(f'   Required words filter: {", ".join(self.required_words)}', 'info')
        self.log(f'   Require website: {self.require_website}', 'info')
        self.log(f'   Output: {self.output_path}', 'info')
        self.log(f'   Browser: {self.browser.capitalize()}', 'info')
        self.log(f'   Run Stage 2: {self.run_stage_2}', 'info')
        
        try:
            # Stage 1: Google Maps scraping
            maps_count = self.run_stage_1_maps_scraping()
            
            # Stage 2: Website enrichment (if enabled)
            if self.run_stage_2:
                self.log('⏳ Waiting 3 seconds before starting Stage 2...', 'info')
                time.sleep(3)
                website_stats = self.run_stage_2_website_enrichment()
            else:
                self.log('⏭️ Stage 2 skipped (disabled in configuration)', 'info')
            
            # Final summary
            self.log('', 'info')
            self.log('🎉 ═══════════════════════════════════════', 'success')
            self.log('🎉 SCRAPING COMPLETED SUCCESSFULLY!', 'success')
            self.log('🎉 ═══════════════════════════════════════', 'success')
            self.log(f'📊 Total listings scraped: {maps_count}', 'success')
            if self.run_stage_2:
                self.log(f'🌐 Websites processed: {website_stats["processed"]}', 'success')
                self.log(f'📧 Emails found: {website_stats.get("emails_found", 0)}', 'success')
                self.log(f'👤 Owners found: {website_stats.get("owners_found", 0)}', 'success')
            self.log(f'💾 Data saved to: {self.output_path}', 'success')
            
            self.update_status(stage='completed')
            
        except KeyboardInterrupt:
            self.log('⏹️ Scraping interrupted by user', 'warning')
            self.update_status(stage='stopped')
        except Exception as e:
            self.log(f'❌ Fatal error: {str(e)}', 'error')
            self.update_status(stage='error')
            raise
