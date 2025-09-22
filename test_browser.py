#!/usr/bin/env python3
"""
Test script to verify browser launch works
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_browser():
    print("🚀 Testing Chrome browser launch...")
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    chrome_options.add_argument("--disable-hang-monitor")
    chrome_options.add_argument("--disable-prompt-on-repost")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--disable-extensions")
    
    # Initialize the driver with proper Chrome path for macOS
    try:
        print("Attempting to initialize Chrome driver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ Chrome driver initialized successfully!")
        
        # Test navigation
        print("Testing navigation to Google...")
        driver.get("https://www.google.com")
        print("✅ Successfully navigated to Google")
        
        # Get page title
        title = driver.title
        print(f"✅ Page title: {title}")
        
        # Wait a bit
        time.sleep(2)
        
        # Close browser
        driver.quit()
        print("✅ Browser closed successfully")
        print("🎉 Browser test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Trying alternative Chrome path...")
        
        try:
            # Alternative approach for macOS
            chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Chrome driver initialized with alternative path!")
            
            # Test navigation
            print("Testing navigation to Google...")
            driver.get("https://www.google.com")
            print("✅ Successfully navigated to Google")
            
            # Get page title
            title = driver.title
            print(f"✅ Page title: {title}")
            
            # Wait a bit
            time.sleep(2)
            
            # Close browser
            driver.quit()
            print("✅ Browser closed successfully")
            print("🎉 Browser test completed successfully!")
            return True
            
        except Exception as e2:
            print(f"❌ Alternative approach also failed: {e2}")
            return False

if __name__ == "__main__":
    success = test_browser()
    if success:
        print("\n✅ Browser is working! You can now run the scrapers.")
    else:
        print("\n❌ Browser test failed. Please check the error messages above.")
