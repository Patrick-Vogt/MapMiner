import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
import sys

class MapMiner:
    def __init__(self, csv_filename='businesses.csv', browser='safari', delays=None, required_words=None, require_website=True):
        """
        Initialize the scraper with browser options
        
        Args:
            csv_filename: Path to CSV file for output
            browser: Browser to use ('safari', 'chrome', or 'edge')
            delays: Dictionary with delay configurations
            required_words: List of words that must be in company name (case-insensitive)
            require_website: Only save entries that have a website (default: True)
        """
        self.csv_filename = csv_filename
        self.required_words = required_words or []
        self.require_website = require_website
        self.browser = browser.lower()
        self.delays = delays or {
            'delay_min': 2,
            'delay_max': 5,
            'scroll_delay_min': 3,
            'scroll_delay_max': 7,
            'click_delay_min': 3,
            'click_delay_max': 7
        }
        
        driver_initialized = False
        last_error = None
        
        print(f"Browser selected: {self.browser.capitalize()}")
        
        # Try the selected browser
        if self.browser == 'safari':
            try:
                safari_options = SafariOptions()
                self.driver = webdriver.Safari(options=safari_options)
                driver_initialized = True
                print("✓ Safari browser initialized successfully")
            except Exception as e:
                last_error = e
                print(f"⚠️ Safari initialization failed: {str(e)}")
                print("Note: Enable Safari WebDriver in Safari > Develop > Allow Remote Automation")
                print("Or run: safaridriver --enable")
        
        elif self.browser == 'chrome':
            try:
                chrome_options = ChromeOptions()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                # Let Selenium Manager download the correct ChromeDriver automatically
                self.driver = webdriver.Chrome(options=chrome_options)
                driver_initialized = True
                print("✓ Chrome browser initialized successfully")
            except Exception as e:
                last_error = e
                print(f"⚠️ Chrome initialization failed: {str(e)}")
        
        elif self.browser == 'edge':
            try:
                from selenium.webdriver.edge.service import Service as EdgeService
                edge_options = Options()
                
                edge_binary_path = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
                if os.path.exists(edge_binary_path):
                    edge_options.binary_location = edge_binary_path
                
                edge_options.add_argument('--no-sandbox')
                edge_options.add_argument('--disable-dev-shm-usage')
                edge_options.add_argument('--disable-gpu')
                edge_options.add_argument('--disable-blink-features=AutomationControlled')
                edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                edge_options.add_experimental_option('useAutomationExtension', False)
                
                service = EdgeService()
                self.driver = webdriver.Edge(service=service, options=edge_options)
                driver_initialized = True
                print("✓ Edge browser initialized successfully")
            except Exception as e:
                last_error = e
                print(f"⚠️ Edge initialization failed: {str(e)}")
        
        if not driver_initialized:
            error_msg = (
                f"Failed to initialize {self.browser.capitalize()} browser. Last error: {str(last_error)}\n\n"
                f"Troubleshooting steps:\n"
            )
            if self.browser == 'safari':
                error_msg += (
                    f"1. Enable Safari WebDriver: Safari > Develop > Allow Remote Automation\n"
                    f"2. Or run in Terminal: safaridriver --enable\n"
                    f"3. Try selecting a different browser (Chrome or Edge)\n"
                )
            elif self.browser == 'chrome':
                error_msg += (
                    f"1. Ensure Google Chrome is installed\n"
                    f"2. Check your internet connection (ChromeDriver download may be blocked)\n"
                    f"3. Try selecting a different browser (Safari or Edge)\n"
                )
            else:  # edge
                error_msg += (
                    f"1. Ensure Microsoft Edge is installed\n"
                    f"2. Check your internet connection (EdgeDriver download may be blocked)\n"
                    f"3. Try selecting a different browser (Safari or Chrome)\n"
                )
            raise RuntimeError(error_msg)
        
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.csv_headers = ['name', 'address', 'phone', 'website', 'rating', 'reviews', 'email', 'owner']
        self._initialize_csv()
        
    def search_location(self, query):
        """Search for a specific query on Google Maps"""
        print(f"Searching for: {query}")
        try:
            print("Step 1: Loading Google Maps...")
            self.driver.get("https://www.google.com/maps")
            print("Step 2: Waiting for page load...")
            time.sleep(random.uniform(3, 6))
            
            print("Step 3: Checking page ready state...")
            # Wait for page to fully load
            self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
            print("✓ Page loaded")
            
            print("Step 4: Looking for search box...")
            # Try multiple selectors as Google Maps structure varies
            search_box = None
            selectors = [
                (By.ID, "searchboxinput"),
                (By.NAME, "q"),
                (By.CSS_SELECTOR, "input[aria-label*='Search']"),
                (By.CSS_SELECTOR, "input[placeholder*='Search']"),
                (By.XPATH, "//input[@type='search']"),
                (By.XPATH, "//input[contains(@aria-label, 'Search')]")
            ]
            
            for selector_type, selector_value in selectors:
                try:
                    print(f"  Trying selector: {selector_type} = {selector_value}")
                    search_box = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((selector_type, selector_value))
                    )
                    print(f"✓ Search box found with: {selector_type} = {selector_value}")
                    break
                except TimeoutException:
                    continue
            
            if not search_box:
                # Take a screenshot for debugging
                screenshot_path = "/tmp/google_maps_debug.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"❌ Could not find search box. Screenshot saved to: {screenshot_path}")
                raise Exception("Search box not found with any selector")
            
            print("Step 5: Clearing search box...")
            search_box.clear()
            time.sleep(0.5)
            
            print(f"Step 6: Typing query: {query}")
            search_box.send_keys(query)
            time.sleep(0.5)
            
            print("Step 7: Pressing ENTER...")
            search_box.send_keys(Keys.ENTER)
            
            print("Step 8: Waiting for results...")
            time.sleep(random.uniform(4, 7))
            print("✓ Search completed")
        except Exception as e:
            print(f"❌ Error during search at current step: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
        
    def scroll_results(self, max_scrolls=10):
        """Scroll through the results panel to load more listings"""
        print("Scrolling through results...")
        
        try:
            # Wait for results to load
            time.sleep(2)
            scrollable_div = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]'))
            )
            
            for i in range(max_scrolls):
                try:
                    self.driver.execute_script(
                        'arguments[0].scrollTo(0, arguments[0].scrollHeight)', 
                        scrollable_div
                    )
                    time.sleep(random.uniform(
                        self.delays['scroll_delay_min'],
                        self.delays['scroll_delay_max']
                    ))
                    print(f"Scroll {i+1}/{max_scrolls}")
                except Exception as scroll_error:
                    print(f"Error on scroll {i+1}: {scroll_error}")
                    break
                
        except Exception as e:
            print(f"Error while scrolling: {e}")
    
    def extract_business_info(self, element):
        """Extract information from a single business listing"""
        data = {
            'name': '',
            'address': '',
            'phone': '',
            'website': '',
            'rating': '',
            'reviews': '',
            'email': '',
            'owner': ''
        }
        
        try:
            # Scroll element into view first
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            element.click()
            time.sleep(random.uniform(
                self.delays['click_delay_min'],
                self.delays['click_delay_max']
            ))
            
            # Wait for details panel to load
            time.sleep(1)
            
            # Extract name
            try:
                name_elem = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf'))
                )
                data['name'] = name_elem.text
            except TimeoutException:
                print("  ⚠️ Could not find business name")
            except Exception as e:
                print(f"  ⚠️ Error extracting name: {e}")
            
            # Extract address
            try:
                address_elem = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    'button[data-item-id="address"]'
                )
                data['address'] = address_elem.get_attribute('aria-label').replace('Adresse: ', '').replace('Address: ', '')
            except:
                pass
            
            # Extract phone
            try:
                phone_elem = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    'button[data-item-id*="phone"]'
                )
                data['phone'] = phone_elem.get_attribute('aria-label').replace('Telefon: ', '').replace('Phone: ', '')
            except:
                pass
            
            # Extract website
            try:
                website_elem = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    'a[data-item-id="authority"]'
                )
                data['website'] = website_elem.get_attribute('href')
            except:
                pass
            
            # Extract rating
            try:
                rating_elem = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    'div.F7nice span[aria-hidden="true"]'
                )
                data['rating'] = rating_elem.text
            except:
                pass
            
            # Extract number of reviews
            try:
                reviews_elem = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    'div.F7nice span[aria-label*="reviews"], div.F7nice span[aria-label*="Rezensionen"]'
                )
                data['reviews'] = reviews_elem.get_attribute('aria-label')
            except:
                pass
                
        except Exception as e:
            print(f"Error extracting business info: {e}")
        
        return data
    
    def scrape_listings(self, max_results=100):
        """Scrape listings until we have max_results that match all filters"""
        results = []
        
        try:
            time.sleep(random.uniform(4, 8))
            
            # Wait for listings to be present
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Nv2PK'))
                )
            except TimeoutException:
                print("⚠️ No listings found on page")
                return results
            
            listings = self.driver.find_elements(
                By.CSS_SELECTOR, 
                'div.Nv2PK'
            )
            
            print(f"Found {len(listings)} listings on page")
            print(f"Target: {max_results} matching results")
            
            # Process listings until we have enough matching results or run out of listings
            processed = 0
            skipped_early = 0
            for idx, listing in enumerate(listings):
                # Stop if we have enough matching results
                if len(results) >= max_results:
                    print(f"✓ Reached target of {max_results} matching results")
                    break
                
                processed += 1
                
                try:
                    # Check if element is still valid
                    if not listing.is_displayed():
                        print(f"  ⚠️ Listing not visible, skipping")
                        continue
                    
                    # OPTIMIZATION: Check name in preview BEFORE clicking to save time
                    preview_name = self._get_listing_name_preview(listing)
                    if preview_name and self.required_words:
                        if not self._matches_required_words(preview_name):
                            skipped_early += 1
                            print(f"[{processed}/{len(listings)}] ⊘ {preview_name} - SKIPPED (doesn't match required words)")
                            continue
                    
                    print(f"[{processed}/{len(listings)}] Processing (saved: {len(results)}/{max_results})")
                    
                    data = self.extract_business_info(listing)
                    if data['name']:
                        if self.require_website and not data['website']:
                            print(f"  ⊘ {data['name']} - SKIPPED (no website)")
                        elif self.save_business(data):
                            results.append(data)
                            print(f"  ✓ {data['name']} - SAVED ({len(results)}/{max_results})")
                        else:
                            print(f"  ✗ Failed to save: {data['name']}")
                    else:
                        print(f"  ⚠️ No name found for listing")
                    
                    time.sleep(random.uniform(
                        self.delays['delay_min'],
                        self.delays['delay_max']
                    ))
                    
                except Exception as e:
                    print(f"  ✗ Error processing listing: {e}")
                    # Continue with next listing instead of crashing
                    continue
            
            if len(results) < max_results:
                print(f"⚠️ Only found {len(results)}/{max_results} matching results")
                print(f"   Processed: {processed} listings | Skipped early: {skipped_early} | Clicked: {processed - skipped_early}")
                    
        except Exception as e:
            print(f"Error scraping listings: {e}")
            import traceback
            traceback.print_exc()
        
        return results
    
    def _initialize_csv(self):
        """Initialize CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.csv_filename):
            with open(self.csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.csv_headers)
                writer.writeheader()
            print(f"✓ Created new CSV file: {self.csv_filename}")
        else:
            print(f"✓ Appending to existing CSV file: {self.csv_filename}")
    
    def _matches_required_words(self, company_name):
        """Check if company name contains any of the required words (case-insensitive)"""
        if not self.required_words:
            return True
        
        company_name_lower = company_name.lower()
        for word in self.required_words:
            if word.lower() in company_name_lower:
                return True
        return False
    
    def _get_listing_name_preview(self, listing_element):
        """Extract company name from listing preview without clicking"""
        try:
            # Try to find the name in the listing preview
            name_elem = listing_element.find_element(By.CSS_SELECTOR, 'div.fontHeadlineSmall')
            return name_elem.text
        except:
            try:
                # Alternative selector
                name_elem = listing_element.find_element(By.CSS_SELECTOR, 'a.hfpxzc')
                return name_elem.get_attribute('aria-label')
            except:
                return None
    
    def save_business(self, data):
        """Save a single business to CSV file immediately"""
        if not data or not data.get('name'):
            return False
        
        with open(self.csv_filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.csv_headers)
            writer.writerow(data)
        
        return True
    
    def get_saved_count(self):
        """Get the number of businesses already saved in CSV"""
        if not os.path.exists(self.csv_filename):
            return 0
        
        with open(self.csv_filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return sum(1 for row in reader) - 1
    
    def close(self):
        """Close the browser"""
        self.driver.quit()
