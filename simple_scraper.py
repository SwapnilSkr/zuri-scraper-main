#!/usr/bin/env python3
"""
Simple Web Scraper using Selenium
Basic example for beginners
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def simple_scraper():
    """Simple example of web scraping"""
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Navigate to a website
        print("Navigating to quotes.toscrape.com...")
        driver.get("https://quotes.toscrape.com/")
        
        # Wait for page to load
        time.sleep(3)
        
        # Find all quote elements
        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        
        print(f"\nFound {len(quotes)} quotes:")
        print("-" * 50)
        
        # Extract and display quote information
        for i, quote in enumerate(quotes[:5], 1):  # Show first 5 quotes
            try:
                text = quote.find_element(By.CLASS_NAME, "text").text
                author = quote.find_element(By.CLASS_NAME, "author").text
                
                print(f"{i}. Quote: {text}")
                print(f"   Author: {author}")
                print()
                
            except Exception as e:
                print(f"Error extracting quote {i}: {e}")
                continue
        
        # Get page title
        page_title = driver.title
        print(f"Page Title: {page_title}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    simple_scraper()
