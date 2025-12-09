# utils/anti_block.py

import time
import random
from typing import Dict, Optional
from fake_useragent import UserAgent
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class AntiBlockSession:
    """Enhanced requests session with anti-blocking features"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.session = self._create_session()
        
    def _create_session(self) -> requests.Session:
        """Create a session with retry strategy"""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def get_headers(self) -> Dict[str, str]:
        """Generate randomized headers"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
    
    def get(self, url: str, timeout: int = 15, delay: Optional[float] = None) -> requests.Response:
        """Make GET request with anti-blocking measures"""
        # Random delay between requests
        if delay is None:
            delay = random.uniform(1.5, 3.0)
        time.sleep(delay)
        
        headers = self.get_headers()
        
        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
    
    def post(self, url: str, data: Dict = None, json: Dict = None, timeout: int = 15) -> requests.Response:
        """Make POST request with anti-blocking measures"""
        time.sleep(random.uniform(1.5, 3.0))
        
        headers = self.get_headers()
        if json:
            headers['Content-Type'] = 'application/json'
        
        try:
            response = self.session.post(
                url,
                headers=headers,
                data=data,
                json=json,
                timeout=timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"POST request failed: {e}")
            raise
    
    def close(self):
        """Close the session"""
        self.session.close()


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, calls_per_minute: int = 20):
        self.calls_per_minute = calls_per_minute
        self.min_interval = 60.0 / calls_per_minute
        self.last_call = 0
    
    def wait(self):
        """Wait if necessary to respect rate limit"""
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()