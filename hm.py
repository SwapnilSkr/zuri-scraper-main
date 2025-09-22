#!/usr/bin/env python3
"""
H&M Fashion Search Script
Navigates to H&M.com, searches for keywords from zara_keywords.json, waits 3 seconds between searches
"""

import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def main():
    try:
        with open('zara_keywords.json', 'r') as f:
            keywords_data = json.load(f)
        print(f"Loaded {len(keywords_data)} keywords from zara_keywords.json")
    except Exception as e:
        print(f"Error loading keywords file: {e}")
        return
    
    all_scraped_data = []
    
    chrome_options = Options()
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    selected_ua = random.choice(user_agents)
    chrome_options.add_argument(f"--user-agent={selected_ua}")
    
    viewports = [
        "--window-size=1920,1080",
        "--window-size=1366,768", 
        "--window-size=1440,900",
        "--window-size=1536,864",
        "--window-size=1280,720"
    ]
    chrome_options.add_argument(random.choice(viewports))
    
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
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-gpu-logging")
    chrome_options.add_argument("--silent")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-web-resources")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-component-extensions-with-background-pages")
    chrome_options.add_argument("--disable-background-mode")
    chrome_options.add_argument("--disable-features=Translate")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values": {
            "notifications": 2,
            "geolocation": 2,
            "media_stream": 2,
        },
        "profile.managed_default_content_settings": {
            "images": 1
        },
        "profile.default_content_settings": {
            "popups": 0
        }
    })
    
   
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
   
    stealth_scripts = [
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
        "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
        "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
        "Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})})",
        "window.chrome = {runtime: {}}",
        "Object.defineProperty(navigator, 'platform', {get: () => 'MacIntel'})",
        "Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8})",
        "Object.defineProperty(navigator, 'deviceMemory', {get: () => 8})",
        "Object.defineProperty(navigator, 'maxTouchPoints', {get: () => 0})",
        "Object.defineProperty(navigator, 'vendor', {get: () => 'Google Inc.'})",
        "Object.defineProperty(navigator, 'vendorSub', {get: () => ''})",
        "Object.defineProperty(navigator, 'productSub', {get: () => '20030107'})",
        "Object.defineProperty(navigator, 'appCodeName', {get: () => 'Mozilla'})",
        "Object.defineProperty(navigator, 'appName', {get: () => 'Netscape'})",
        "Object.defineProperty(navigator, 'appVersion', {get: () => '5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})",
        "Object.defineProperty(navigator, 'userAgent', {get: () => arguments[0]})"
    ]
    
   
    for script in stealth_scripts:
        try:
            if 'arguments[0]' in script:
                driver.execute_script(script, selected_ua)
            else:
                driver.execute_script(script)
        except:
            pass
    
    try:
       
        wait = WebDriverWait(driver, 10)
        
       
        print("Navigating to H&M...")
        driver.get("https://www2.hm.com/en_in")
        
       
        time.sleep(random.uniform(3, 6))
        
       
        actions = ActionChains(driver)
        
       
        for _ in range(random.randint(2, 5)):
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            actions.move_by_offset(x_offset, y_offset)
            actions.perform()
            time.sleep(random.uniform(0.1, 0.3))
        
       
        for _ in range(random.randint(1, 3)):
            scroll_amount = random.randint(100, 500)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.5))
        
       
        print("Waiting for page to load...")
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-elid='header-search-button']")))
            print("✅ Page loaded successfully - search button found")
        except TimeoutException:
            print("❌ Page load timeout - search button not found within 10 seconds")
            return
        
       
        for i, keyword_obj in enumerate(keywords_data):
            keyword_id = keyword_obj["id"]
            keyword = keyword_obj["keyword"]
            print(f"\nSearching for keyword {i+1}/{len(keywords_data)}: '{keyword}' (ID: {keyword_id})")
            
            try:
               
                if i > 0:
                    print("Navigating back to main page...")
                    driver.get("https://www2.hm.com/en_in")
                   
                    time.sleep(random.uniform(3, 7))
                    
                   
                    if i > 0:
                        print(f"Waiting {random.uniform(5, 10):.1f} seconds between keyword searches...")
                        time.sleep(random.uniform(5, 10))
                
               
                print(f"Looking for search button for keyword: '{keyword}'")
                search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-elid='header-search-button']")))
                
               
                time.sleep(random.uniform(1, 3))
                
               
                actions = ActionChains(driver)
                actions.move_to_element(search_button)
                actions.pause(random.uniform(0.1, 0.5))
                actions.click(search_button)
                actions.perform()
                print("Clicked search button")
                
               
                wait_time = random.uniform(2, 4)
                print(f"Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                
               
                print(f"Looking for search input for keyword: '{keyword}'")
                search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-elid='search-drawer-input']")))
                
               
                time.sleep(random.uniform(0.5, 1.5))
                
               
                search_input.clear()
               
                search_input.send_keys(Keys.CONTROL + "a")
                search_input.send_keys(Keys.DELETE)
                print(f"Cleared search input for keyword: '{keyword}'")
                
               
                for char in keyword:
                    search_input.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))  
                print(f"Typed: {keyword}")
                

                time.sleep(random.uniform(0.5, 1.5))
                
               
                search_input.send_keys(Keys.RETURN)
                print("Pressed Enter")
                
                
                wait_time = random.uniform(4, 7)
                print(f"Waiting {wait_time:.1f} seconds for search results to load...")
                time.sleep(wait_time)
                
                
                for _ in range(random.randint(1, 3)):
                    scroll_amount = random.randint(200, 800)
                    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(random.uniform(0.5, 1.5))
                

                try:
                    found_products = driver.find_elements(By.CSS_SELECTOR, ".product-item")
                    if not found_products:
                        found_products = driver.find_elements(By.CSS_SELECTOR, "[data-articlecode]")
                    if not found_products:
                        found_products = driver.find_elements(By.CSS_SELECTOR, ".hm-product-item")
                    
                    print(f"Found {len(found_products)} products")
                    
                    products_to_visit = min(3, len(found_products))
                    print(f"Visiting first {products_to_visit} product pages...")
                    
                    for j in range(products_to_visit):
                        try:
                            print(f"\nVisiting product {j+1}/{products_to_visit}")
                            
                            found_products = driver.find_elements(By.CSS_SELECTOR, ".product-item")
                            if not found_products:
                                found_products = driver.find_elements(By.CSS_SELECTOR, "[data-articlecode]")
                            if not found_products:
                                found_products = driver.find_elements(By.CSS_SELECTOR, ".hm-product-item")
                            
                            if j >= len(found_products):
                                print(f"No more product elements available (tried to access index {j})")
                                break
                            
                            product = found_products[j]
                            
                            try:
                                product_link = product.find_element(By.CSS_SELECTOR, "a")
                                product_url = product_link.get_attribute("href")
                            except:
                                try:
                                    article_code = product.get_attribute("data-articlecode")
                                    if article_code:
                                        product_url = f"https://www2.hm.com/en_in/productpage.{article_code}.html"
                                    else:
                                        print("No product URL found, skipping...")
                                        continue
                                except:
                                    print("No product URL found, skipping...")
                                    continue
                            
                            print(f"Product URL: {product_url}")
                            
                            print(f"Navigating directly to: {product_url}")
                            driver.get(product_url)
                            
                            wait_time = random.uniform(4, 8)
                            print(f"Waiting {wait_time:.1f} seconds for product page to load...")
                            time.sleep(wait_time)
                            
                            for _ in range(random.randint(2, 4)):
                                scroll_amount = random.randint(100, 400)
                                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                                time.sleep(random.uniform(0.8, 2.0))
                            
                            actions = ActionChains(driver)
                            for _ in range(random.randint(1, 3)):
                                x_offset = random.randint(-50, 50)
                                y_offset = random.randint(-50, 50)
                                actions.move_by_offset(x_offset, y_offset)
                                actions.perform()
                                time.sleep(random.uniform(0.2, 0.8))
                            
                            product_data = {
                                "site": "h&m",
                                "product_url": product_url,
                                "keyword_id": keyword_id,
                                "keyword": keyword,
                                "product_id": "Not found",
                                "brand_name": "H&M",
                                "product_name": "Not found",
                                "product_rating": "Not found",
                                "product_rating_count": "Not found",
                                "current_product_price": "Not found",
                                "original_product_price": "Not found",
                                "product_sizes": [],
                                "product_image_urls": [],
                            }
                            
                            try:
                                current_url = driver.current_url
                                import re
                                product_id_match = re.search(r'productpage\.(\d+)\.html', current_url)
                                if product_id_match:
                                    product_data["product_id"] = product_id_match.group(1)
                                    print(f"Product ID: {product_data['product_id']}")
                            except Exception as e:
                                print(f"Product ID not found: {e}")
                            
                            try:
                                product_name = driver.find_element(By.CSS_SELECTOR, "div.a0c9d8>h1.be6471").text
                                product_data["product_name"] = product_name
                                print(f"Product name: {product_name}")
                            except Exception as e:
                                print(f"Product name not found: {e}")
                            
                            try:
                                price_element = driver.find_element(By.CSS_SELECTOR, "div.f4e18c>span.a15559")
                                product_data["current_product_price"] = price_element.text
                                print(f"Product price: {price_element.text}")
                            except Exception as e:
                                print(f"Product price not found: {e}")

                            try:
                                color_element = driver.find_element(By.CSS_SELECTOR, "[data-testid='color-selector']")
                                color_name = color_element.find_element(By.CSS_SELECTOR, "p.b136ca").text
                                product_data["color_name"] = color_name
                                print(f"Color name: {color_name}")
                            except Exception as e:
                                print(f"Color name not found: {e}")
                            
                            try:
                                size_elements = driver.find_elements(By.CSS_SELECTOR, "ul.c3421a>li>div.af6b46")
                                for size_element in size_elements:
                                    size_text = size_element.text.strip()
                                    if size_text:
                                        product_data["product_sizes"].append(size_text)
                                print(f"Product sizes: {product_data['product_sizes']}")
                            except Exception as e:
                                print(f"Product sizes not found: {e}")
                            
                            try:
                                image_elements = driver.find_elements(By.CSS_SELECTOR, ".product-detail-main-image img")
                                for image_element in image_elements:
                                    image_url = image_element.get_attribute("src")
                                    if image_url:
                                        product_data["product_image_urls"].append(image_url)
                                print(f"Product images: {len(product_data['product_image_urls'])} found")
                            except Exception as e:
                                print(f"Product images not found: {e}")
                            
                            all_scraped_data.append(product_data)
                            print(f"Added product data for: {product_data['product_name']}")
                            
                            print("Going back to search results...")
                            driver.back()
                            time.sleep(random.uniform(2, 4))
                            
                        except Exception as e:
                            print(f"Error visiting product {j+1}: {e}")
                            try:
                                driver.back()
                                time.sleep(random.uniform(2, 4))
                            except:
                                pass
                            continue
                    
                except Exception as e:
                    print(f"Error finding products: {e}")
                    continue
                
                wait_time = random.uniform(5, 10)
                print(f"Waiting {wait_time:.1f} seconds before next keyword...")
                time.sleep(wait_time)
                
                print(f"Completed search for keyword: '{keyword}'")
                
            except TimeoutException as e:
                print(f"Timeout error searching for keyword '{keyword}': {e}")
                continue
            except Exception as e:
                print(f"Error searching for keyword '{keyword}': {e}")
                continue
        
        print(f"\nSaving {len(all_scraped_data)} products to h&m_scraped_data.json...")
        try:
            with open('h&m_scraped_data.json', 'w', encoding='utf-8') as f:
                json.dump(all_scraped_data, f, indent=2, ensure_ascii=False)
            print("Data saved successfully to h&m_scraped_data.json")
        except Exception as e:
            print(f"Error saving data: {e}")
        
        print("\nAll keyword searches completed!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    main()
