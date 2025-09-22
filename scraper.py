#!/usr/bin/env python3
"""
Web Scraping Project using Selenium
A comprehensive example showing different scraping techniques
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, headless=False):
        """Initialize the web scraper with Chrome driver"""
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Set up Chrome driver with appropriate options"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Additional options for better performance and stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
            
            # Automatically download and manage Chrome driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set implicit wait time
            self.driver.implicitly_wait(10)
            logger.info("Chrome driver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise
    
    def scrape_quotes(self, url="https://quotes.toscrape.com/"):
        """Scrape quotes from quotes.toscrape.com"""
        try:
            logger.info(f"Starting to scrape quotes from {url}")
            self.driver.get(url)
            
            quotes_data = []
            page = 1
            
            while True:
                logger.info(f"Scraping page {page}")
                
                # Wait for quotes to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "quote"))
                )
                
                # Find all quote elements
                quote_elements = self.driver.find_elements(By.CLASS_NAME, "quote")
                
                for quote_element in quote_elements:
                    try:
                        text = quote_element.find_element(By.CLASS_NAME, "text").text
                        author = quote_element.find_element(By.CLASS_NAME, "author").text
                        tags = [tag.text for tag in quote_element.find_elements(By.CLASS_NAME, "tag")]
                        
                        quotes_data.append({
                            "text": text,
                            "author": author,
                            "tags": tags,
                            "page": page
                        })
                        
                    except NoSuchElementException as e:
                        logger.warning(f"Could not extract quote data: {e}")
                        continue
                
                # Check if there's a next page
                try:
                    next_button = self.driver.find_element(By.CLASS_NAME, "next")
                    if "disabled" in next_button.get_attribute("class"):
                        logger.info("Reached last page")
                        break
                    
                    next_button.click()
                    page += 1
                    time.sleep(2)  # Wait for page to load
                    
                except NoSuchElementException:
                    logger.info("No next page found")
                    break
            
            logger.info(f"Successfully scraped {len(quotes_data)} quotes from {page} pages")
            return quotes_data
            
        except Exception as e:
            logger.error(f"Error scraping quotes: {e}")
            return []
    
    def scrape_news_headlines(self, url="https://news.ycombinator.com/"):
        """Scrape news headlines from Hacker News"""
        try:
            logger.info(f"Starting to scrape news from {url}")
            self.driver.get(url)
            
            # Wait for headlines to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "titleline"))
            )
            
            headlines = []
            title_elements = self.driver.find_elements(By.CLASS_NAME, "titleline")
            
            for i, title_element in enumerate(title_elements[:10]):  # Get first 10 headlines
                try:
                    link_element = title_element.find_element(By.TAG_NAME, "a")
                    title = link_element.text
                    link = link_element.get_attribute("href")
                    
                    # Get score if available
                    try:
                        score_element = self.driver.find_element(By.XPATH, f"//tr[{2*i + 1}]//span[@class='score']")
                        score = score_element.text
                    except:
                        score = "N/A"
                    
                    headlines.append({
                        "rank": i + 1,
                        "title": title,
                        "link": link,
                        "score": score
                    })
                    
                except NoSuchElementException as e:
                    logger.warning(f"Could not extract headline data: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(headlines)} headlines")
            return headlines
            
        except Exception as e:
            logger.error(f"Error scraping news: {e}")
            return []
    
    def scrape_ecommerce_products(self, url="https://webscraper.io/test-sites/e-commerce/allinone"):
        """Scrape product information from an e-commerce test site"""
        try:
            logger.info(f"Starting to scrape products from {url}")
            self.driver.get(url)
            
            # Wait for products to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "thumbnail"))
            )
            
            products = []
            product_elements = self.driver.find_elements(By.CLASS_NAME, "thumbnail")
            
            for product_element in product_elements[:20]:  # Get first 20 products
                try:
                    name = product_element.find_element(By.CLASS_NAME, "title").text
                    price = product_element.find_element(By.CLASS_NAME, "price").text
                    
                    # Get description if available
                    try:
                        description = product_element.find_element(By.CLASS_NAME, "description").text
                    except:
                        description = "No description available"
                    
                    # Get rating if available
                    try:
                        rating = product_element.find_element(By.CLASS_NAME, "rating").text
                    except:
                        rating = "No rating available"
                    
                    products.append({
                        "name": name,
                        "price": price,
                        "description": description,
                        "rating": rating
                    })
                    
                except NoSuchElementException as e:
                    logger.warning(f"Could not extract product data: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(products)} products")
            return products
            
        except Exception as e:
            logger.error(f"Error scraping products: {e}")
            return []
    
    def save_data(self, data, filename):
        """Save scraped data to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser driver closed")

def main():
    """Main function to demonstrate the scraper"""
    scraper = None
    
    try:
        # Initialize scraper (set headless=True for production use)
        scraper = WebScraper(headless=False)
        
        # Example 1: Scrape quotes
        logger.info("=" * 50)
        quotes = scraper.scrape_quotes()
        if quotes:
            scraper.save_data(quotes, "quotes.json")
        
        # Example 2: Scrape news headlines
        logger.info("=" * 50)
        headlines = scraper.scrape_news_headlines()
        if headlines:
            scraper.save_data(headlines, "headlines.json")
        
        # Example 3: Scrape e-commerce products
        logger.info("=" * 50)
        products = scraper.scrape_ecommerce_products()
        if products:
            scraper.save_data(products, "products.json")
        
        logger.info("=" * 50)
        logger.info("All scraping tasks completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()
