"""
Configuration file for the web scraping project
"""

BROWSER_CONFIG = {
    "headless": False, 
    "window_size": "1920,1080",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "implicit_wait": 10,
    "page_load_timeout": 30
}

URLS = {
    "quotes": "https://quotes.toscrape.com/",
    "news": "https://news.ycombinator.com/",
    "ecommerce": "https://webscraper.io/test-sites/e-commerce/allinone",
    "books": "https://books.toscrape.com/",
    "weather": "https://www.accuweather.com/en/us/new-york/10007/weather-forecast/349727"
}

SCRAPING_CONFIG = {
    "max_pages": 5, 
    "delay_between_requests": 2, 
    "max_retries": 3, 
    "timeout": 10 
}

OUTPUT_CONFIG = {
    "output_dir": "scraped_data",
    "file_format": "json", 
    "encoding": "utf-8"
}

LOGGING_CONFIG = {
    "level": "INFO", 
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "log_file": "scraper.log"
}
