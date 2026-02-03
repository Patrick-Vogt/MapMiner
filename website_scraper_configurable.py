import csv
import requests
import re
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class WebsiteScraperConfigurable:
    def __init__(self, csv_filename='businesses.csv', max_workers=10, delays=None, progress_callback=None):
        """
        Initialize the website scraper
        
        Args:
            csv_filename: Path to CSV file
            max_workers: Number of parallel workers
            delays: Dictionary with delay configurations
            progress_callback: Callback object for progress updates
        """
        self.csv_filename = csv_filename
        self.max_workers = max_workers
        self.lock = threading.Lock()
        self.progress = progress_callback
        
        self.delays = delays or {
            'delay_min': 1,
            'delay_max': 2
        }
        
        # Suppress SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Common paths to try for finding contact/imprint information
        self.info_paths = [
            '/impressum',
            '/impressum/',
            '/impressum.html',
            '/impressum.htm',
            '/imprint',
            '/imprint/',
            '/imprint.html',
            '/imprint.htm',
            '/ueber-uns',
            '/ueber-uns/',
            '/ueber-uns.html',
            '/ueber-uns.htm',
            '/about',
            '/about/',
            '/about.html',
            '/about.htm',
            '/kontakt',
            '/kontakt/',
            '/kontakt.html',
            '/kontakt.htm',
            '/contact',
            '/contact/',
            '/contact.html',
            '/contact.htm',
            '/datenschutz',
            '/datenschutz/',
            '/datenschutz.html',
            '/datenschutz.htm',
            '/privacy',
            '/privacy/',
            '/privacy.html',
            '/privacy.htm'
        ]
        
        # Email regex pattern
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        # Owner patterns (German)
        self.owner_patterns = [
            re.compile(r'(?:Inhaber|Geschäftsführer|Geschäftsführung|Inhaber/Geschäftsführer|Geschäftsführerin):\s*([^<\n\r]+)', re.IGNORECASE),
            re.compile(r'(?:Inhaber|Geschäftsführer|Geschäftsführung|Inhaber/Geschäftsführer|Geschäftsführerin)\s*([A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)*)', re.IGNORECASE),
            re.compile(r'(?:Verantwortlich|Verantwortlicher):\s*([^<\n\r]+)', re.IGNORECASE)
        ]
    
    def log(self, message, level='info'):
        """Log message via progress callback"""
        if self.progress:
            self.progress.emit_log(message, level)
        else:
            print(message)
    
    def is_mobile_de(self, url):
        """Check if URL is from mobile.de (to skip)"""
        if not url:
            return True
        return 'mobile.de' in url.lower()
    
    def clean_url(self, url):
        """Clean and validate URL"""
        if not url or self.is_mobile_de(url):
            return None
            
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        return url
    
    def create_session(self):
        """Create a new session for each thread"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        session.verify = False
        return session
    
    def get_page_content(self, url, timeout=8, session=None):
        """Get page content with error handling"""
        if session is None:
            session = self.create_session()
        
        try:
            response = session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except Exception:
            return None
    
    def extract_emails(self, text):
        """Extract email addresses from text"""
        if not text:
            return []
        
        emails = self.email_pattern.findall(text)
        filtered_emails = []
        skip_patterns = ['noreply', 'no-reply', 'support', 'info@mobile.de', 'webmaster', 'datenschutz']
        
        for email in emails:
            email_lower = email.lower()
            if not any(pattern in email_lower for pattern in skip_patterns):
                filtered_emails.append(email)
        
        return list(set(filtered_emails))
    
    def extract_owner_name(self, text):
        """Extract owner/manager name from text"""
        if not text:
            return None
        
        for pattern in self.owner_patterns:
            matches = pattern.findall(text)
            for match in matches:
                name = match.strip().replace('\n', ' ').replace('\r', ' ')
                name = re.sub(r'\s+', ' ', name)
                name = re.sub(r'[^\w\s\-äöüÄÖÜß]', '', name)
                
                if len(name) > 3 and len(name) < 50:
                    return name
        
        return None
    
    def scrape_website_info(self, base_url, session=None):
        """Scrape email and owner info from a website"""
        if not base_url or self.is_mobile_de(base_url):
            return None, None
        
        base_url = self.clean_url(base_url)
        if not base_url:
            return None, None
        
        if session is None:
            session = self.create_session()
        
        all_emails = []
        owner_name = None
        
        urls_to_try = [base_url] + [urljoin(base_url, path) for path in self.info_paths]
        
        for url in urls_to_try:
            content = self.get_page_content(url, session=session)
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                
                for script in soup(["script", "style"]):
                    script.decompose()
                
                text = soup.get_text()
                
                emails = self.extract_emails(text)
                all_emails.extend(emails)
                
                if not owner_name:
                    owner_name = self.extract_owner_name(text)
                
                if all_emails and owner_name:
                    break
        
        unique_emails = list(set(all_emails))
        email_result = ', '.join(unique_emails[:3]) if unique_emails else None
        
        return email_result, owner_name
    
    def read_csv_data(self):
        """Read existing CSV data"""
        if not os.path.exists(self.csv_filename):
            self.log(f"❌ CSV file not found: {self.csv_filename}", 'error')
            return []
        
        data = []
        with open(self.csv_filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        return data
    
    def update_single_row_csv(self, row_data):
        """Thread-safe update of a single row in CSV"""
        with self.lock:
            data = self.read_csv_data()
            if not data:
                return
            
            for i, row in enumerate(data):
                if (row.get('name') == row_data.get('name') and 
                    row.get('address') == row_data.get('address')):
                    data[i].update(row_data)
                    break
            
            fieldnames = list(data[0].keys())
            if 'email' not in fieldnames:
                fieldnames.append('email')
            if 'owner' not in fieldnames:
                fieldnames.append('owner')
            
            with open(self.csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
    
    def process_single_business(self, row_data):
        """Process a single business (for parallel execution)"""
        website = row_data.get('website', '').strip()
        name = row_data.get('name', 'Unknown')
        
        if not website or self.is_mobile_de(website):
            return {'status': 'skipped', 'reason': 'no website or mobile.de', 'name': name}
        
        if row_data.get('email') and row_data.get('owner'):
            return {'status': 'already_processed', 'name': name}
        
        session = self.create_session()
        
        email, owner = self.scrape_website_info(website, session)
        
        result = {'status': 'processed', 'name': name}
        if email:
            row_data['email'] = email
            result['email'] = email
        if owner:
            row_data['owner'] = owner
            result['owner'] = owner
        
        if not email and not owner:
            result['status'] = 'no_info'
        
        self.update_single_row_csv(row_data)
        
        return result
    
    def process_businesses(self):
        """Main processing function with parallel execution"""
        self.log(f"🚀 Starting parallel website scraping ({self.max_workers} workers)...", 'info')
        
        data = self.read_csv_data()
        if not data:
            return {'processed': 0, 'skipped': 0, 'no_info': 0, 'already_processed': 0}
        
        self.log(f"📊 Found {len(data)} businesses to process", 'info')
        
        # Update progress total
        if self.progress:
            self.progress.update_status(total=len(data))
        
        processed = 0
        skipped = 0
        no_info = 0
        already_processed = 0
        emails_found = 0
        owners_found = 0
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_row = {executor.submit(self.process_single_business, row): i 
                           for i, row in enumerate(data)}
            
            for future in as_completed(future_to_row):
                row_index = future_to_row[future]
                try:
                    result = future.result()
                    
                    if result['status'] == 'skipped':
                        skipped += 1
                        self.log(f"[{row_index+1}/{len(data)}] ⏭️  Skipped: {result['name']}", 'info')
                    elif result['status'] == 'already_processed':
                        already_processed += 1
                        self.log(f"[{row_index+1}/{len(data)}] ✅ Already: {result['name']}", 'info')
                    elif result['status'] == 'processed':
                        processed += 1
                        if result.get('email'):
                            emails_found += 1
                        if result.get('owner'):
                            owners_found += 1
                        info_parts = []
                        if result.get('email'):
                            info_parts.append(f"📧 {result['email']}")
                        if result.get('owner'):
                            info_parts.append(f"👤 {result['owner']}")
                        info_str = ' | '.join(info_parts) if info_parts else '❌ No info'
                        self.log(f"[{row_index+1}/{len(data)}] ✅ {result['name']} - {info_str}", 'success')
                    elif result['status'] == 'no_info':
                        no_info += 1
                        self.log(f"[{row_index+1}/{len(data)}] ❌ {result['name']} - No contact info", 'warning')
                    
                    # Update progress
                    if self.progress:
                        self.progress.update_status(
                            progress=row_index + 1,
                            current_item=result['name']
                        )
                        
                except Exception as e:
                    self.log(f"[{row_index+1}/{len(data)}] ❌ Error: {e}", 'error')
        
        elapsed_time = time.time() - start_time
        
        self.log(f"🎉 Parallel processing completed in {elapsed_time:.1f} seconds!", 'success')
        self.log(f"📈 Processed: {processed}", 'info')
        self.log(f"❌ No info found: {no_info}", 'info')
        self.log(f"✅ Already processed: {already_processed}", 'info')
        self.log(f"⏭️  Skipped: {skipped}", 'info')
        self.log(f"⚡ Speed: {len(data)/elapsed_time:.1f} businesses/second", 'info')
        
        return {
            'processed': processed,
            'skipped': skipped,
            'no_info': no_info,
            'already_processed': already_processed,
            'emails_found': emails_found,
            'owners_found': owners_found
        }
