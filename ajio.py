#!/usr/bin/env python3
"""
Ajio Search Script
Navigates to Ajio.com, searches for keywords from zara_keywords.json, waits 3 seconds between searches
"""

import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def random_delay(min_seconds=1, max_seconds=3):
    """Add random delay to mimic human behavior"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def human_like_typing(element, text):
    """Type text with human-like delays between keystrokes"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

def main():
    try:
        with open('zara_keywords.json', 'r') as f:
            keywords_data = json.load(f)
        print(f"Loaded {len(keywords_data)} keywords from zara_keywords.json")
    except Exception as e:
        print(f"Error loading keywords file: {e}")
        return
    
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
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
    
    window_sizes = ["1920,1080", "1366,768", "1440,900", "1536,864"]
    chrome_options.add_argument(f"--window-size={random.choice(window_sizes)}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": random.choice([
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ])
    })
    
    try:
        wait = WebDriverWait(driver, 15)
        
        print("Navigating to Ajio...")
        driver.get("https://www.ajio.com/")
        
        random_delay(2, 4)
        
        print("Waiting for page to load...")
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Search Ajio']")))
            print("✅ Page loaded successfully - search input found")
            random_delay(1, 2)  
        except TimeoutException:
            print("❌ Page load timeout - search input not found within 15 seconds")
            return
        
        for i, keyword_obj in enumerate(keywords_data):
            keyword_id = keyword_obj["id"]
            keyword = keyword_obj["keyword"]
            print(f"\nSearching for keyword {i+1}/{len(keywords_data)}: '{keyword}' (ID: {keyword_id})")
            
            try:
                if i > 0:
                    print("Navigating back to main page...")
                    driver.get("https://www.ajio.com/")
                    random_delay(2, 4)  
                
                print(f"Looking for search input for keyword: '{keyword}'")
                search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Search Ajio']")))
                
                random_delay(0.5, 1.5)
                
                search_input.clear()
                search_input.send_keys(Keys.CONTROL + "a")
                search_input.send_keys(Keys.DELETE)
                print(f"Cleared search input for keyword: '{keyword}'")
                
                random_delay(0.3, 0.8)
                
                human_like_typing(search_input, keyword)
                print(f"Typed: {keyword}")
                
                random_delay(0.5, 1.0)
                
                search_input.send_keys(Keys.RETURN)
                print("Pressed Enter")
                
                print("Waiting for search results to load...")
                random_delay(3, 5)
                
                try:
                    print("Looking for gender filter...")
                    
                    print("Debugging: Looking for all possible gender filter elements...")
                    
                    gender_selectors = [
                        "div.facet-linkhead",
                        "[data-testid*='gender']",
                        "[data-testid*='Gender']", 
                        "div[class*='gender']",
                        "div[class*='Gender']",
                        "div[class*='filter']",
                        "div[class*='Filter']",
                        "div[class*='facet']",
                        "div[class*='Facet']"
                    ]
                    
                    gender_filter_div = None
                    for selector in gender_selectors:
                        try:
                            elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            if elements:
                                print(f"Found {len(elements)} elements with selector: {selector}")
                                for i, elem in enumerate(elements):
                                    try:
                                        text = elem.text.strip()
                                        if text and ('gender' in text.lower() or 'women' in text.lower() or 'men' in text.lower()):
                                            print(f"  Element {i}: '{text}'")
                                            gender_filter_div = elem
                                            break
                                    except:
                                        pass
                                if gender_filter_div:
                                    break
                        except:
                            continue
                    
                    if gender_filter_div:
                        print("Found gender filter div")
                        
                        women_selectors = [
                            "input[id='women']",
                            "input[value='women']",
                            "input[value='Women']",
                            "input[value='WOMEN']",
                            "input[type='checkbox'][id*='women']",
                            "input[type='checkbox'][id*='Women']",
                            "input[type='checkbox'][value*='women']",
                            "input[type='checkbox'][value*='Women']",
                            "label[for*='women'] input",
                            "label[for*='Women'] input",
                            "input[type='checkbox']",
                            "input[type='radio'][value*='women']",
                            "input[type='radio'][value*='Women']"
                        ]
                        
                        women_checkbox = None
                        for selector in women_selectors:
                            try:
                                if gender_filter_div:
                                    checkboxes = gender_filter_div.find_elements(By.CSS_SELECTOR, selector)
                                else:
                                    checkboxes = driver.find_elements(By.CSS_SELECTOR, selector)
                                
                                for checkbox in checkboxes:
                                    try:
                                        checkbox_id = checkbox.get_attribute('id') or ''
                                        checkbox_value = checkbox.get_attribute('value') or ''
                                        checkbox_name = checkbox.get_attribute('name') or ''
                                        
                                        if any(keyword in (checkbox_id + checkbox_value + checkbox_name).lower() 
                                               for keyword in ['women', 'female', 'girl']):
                                            print(f"Found potential women checkbox: id='{checkbox_id}', value='{checkbox_value}', name='{checkbox_name}'")
                                            women_checkbox = checkbox
                                            break
                                    except:
                                        pass
                                
                                if women_checkbox:
                                    break
                            except:
                                continue
                        
                        if women_checkbox:
                            print("Found women checkbox, clicking it...")
                            try:
                                driver.execute_script("arguments[0].scrollIntoView(true);", women_checkbox)
                                time.sleep(1)
                                
                                women_checkbox.click()
                                print("Clicked women checkbox using regular click")
                            except:
                                try:    
                                    driver.execute_script("arguments[0].click();", women_checkbox)
                                    print("Clicked women checkbox using JavaScript")
                                except Exception as js_error:
                                    print(f"JavaScript click also failed: {js_error}")
                            
                            print("Waiting after clicking women filter...")
                            random_delay(3, 5)
                            
                            print("Looking for product links to visit...")
                            try:
                                random_delay(2, 4)
                                
                                product_links = driver.find_elements(By.CSS_SELECTOR, "a.rilrtl-products-list_link.desktop")
                                
                                if not product_links:
                                    product_links = driver.find_elements(By.CSS_SELECTOR, "a[class*='products-list_link']")
                                
                                if not product_links:
                                    product_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
                                
                                print(f"Found {len(product_links)} product links")
                                
                                products_to_visit = min(10, len(product_links))
                                
                                for i in range(products_to_visit):
                                    try:
                                        product_link = product_links[i]
                                        product_url = product_link.get_attribute('href')
                                        product_name = product_link.get_attribute('aria-label') or product_link.text.strip()
                                        
                                        print(f"\n--- Visiting Product {i+1}/{products_to_visit} ---")
                                        print(f"Product: {product_name}")
                                        print(f"URL: {product_url}")
                                        
                                        driver.get(product_url)
                                        
                                        random_delay(3, 5)
                                        
                                        try:
                                            page_title = driver.title
                                            print(f"Page Title: {page_title}")
                                            
                                            current_url = driver.current_url
                                            print(f"Current URL: {current_url}")
                                            

                                            
                                        except Exception as detail_error:
                                            print(f"Error extracting product details: {detail_error}")
                                        
                                        driver.back()
                                        
                                        random_delay(2, 4)
                                        
                                    except Exception as product_error:
                                        print(f"Error visiting product {i+1}: {product_error}")
                                        try:
                                            driver.back()
                                            random_delay(2, 3)
                                        except:
                                            driver.get("https://www.ajio.com/")
                                            random_delay(2, 4)
                                        continue
                                
                                print(f"Completed visiting {products_to_visit} product detail pages")
                                
                            except Exception as visit_error:
                                print(f"Error during product page visits: {visit_error}")
                                import traceback
                                traceback.print_exc()
                        else:
                            print("Women checkbox not found with any selector")
                            all_checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
                            print(f"Found {len(all_checkboxes)} total checkboxes on page")
                            for i, cb in enumerate(all_checkboxes[:5]):  
                                try:
                                    cb_id = cb.get_attribute('id') or 'no-id'
                                    cb_value = cb.get_attribute('value') or 'no-value'
                                    cb_name = cb.get_attribute('name') or 'no-name'
                                    print(f"  Checkbox {i}: id='{cb_id}', value='{cb_value}', name='{cb_name}'")
                                except:
                                    pass
                            
                            print("Attempting to visit product pages without women filter...")
                            try:
                                random_delay(2, 4)
                                
                                product_links = driver.find_elements(By.CSS_SELECTOR, "a.rilrtl-products-list_link.desktop")
                                
                                if not product_links:
                                    product_links = driver.find_elements(By.CSS_SELECTOR, "a[class*='products-list_link']")
                                
                                if not product_links:
                                    product_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
                                
                                print(f"Found {len(product_links)} product links")
                                
                                products_to_visit = min(10, len(product_links))
                                
                                for i in range(products_to_visit):
                                    try:
                                        product_link = product_links[i]
                                        product_url = product_link.get_attribute('href')
                                        product_name = product_link.get_attribute('aria-label') or product_link.text.strip()
                                        
                                        print(f"\n--- Visiting Product {i+1}/{products_to_visit} ---")
                                        print(f"Product: {product_name}")
                                        print(f"URL: {product_url}")
                                        
                                        driver.get(product_url)
                                        
                                        random_delay(3, 5)
                                        
                                        try:
                                            page_title = driver.title
                                            print(f"Page Title: {page_title}")
                                            
                                            current_url = driver.current_url
                                            print(f"Current URL: {current_url}")
                                            
                                        except Exception as detail_error:
                                            print(f"Error extracting product details: {detail_error}")
                                        
                                        driver.back()
                                        
                                        random_delay(2, 4)
                                        
                                    except Exception as product_error:
                                        print(f"Error visiting product {i+1}: {product_error}")
                                        try:
                                            driver.back()
                                            random_delay(2, 3)
                                        except:
                                            driver.get("https://www.ajio.com/")
                                            random_delay(2, 4)
                                        continue
                                
                                print(f"Completed visiting {products_to_visit} product detail pages")
                                
                            except Exception as visit_error:
                                print(f"Error during product page visits: {visit_error}")
                                import traceback
                                traceback.print_exc()
                    else:
                        print("Gender filter div not found with any selector")
                        filter_elements = driver.find_elements(By.CSS_SELECTOR, "div[class*='filter'], div[class*='Filter'], div[class*='facet'], div[class*='Facet']")
                        print(f"Found {len(filter_elements)} filter-related elements")
                        for i, elem in enumerate(filter_elements[:3]):  
                            try:
                                text = elem.text.strip()[:100]  
                                print(f"  Filter element {i}: '{text}'")
                            except:
                                pass
                        
                        print("Attempting to visit product pages without any filter...")
                        try:
                            time.sleep(2)
                            
                            product_links = driver.find_elements(By.CSS_SELECTOR, "a.rilrtl-products-list_link.desktop")
                            
                            if not product_links:
                                product_links = driver.find_elements(By.CSS_SELECTOR, "a[class*='products-list_link']")
                            
                            if not product_links:
                                product_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
                            
                            print(f"Found {len(product_links)} product links")
                            
                            products_to_visit = min(10, len(product_links))
                            
                            for i in range(products_to_visit):
                                try:
                                    product_link = product_links[i]
                                    product_url = product_link.get_attribute('href')
                                    product_name = product_link.get_attribute('aria-label') or product_link.text.strip()
                                    
                                    print(f"\n--- Visiting Product {i+1}/{products_to_visit} ---")
                                    print(f"Product: {product_name}")
                                    print(f"URL: {product_url}")
                                    
                                    driver.get(product_url)
                                    
                                    random_delay(3, 5)
                                    
                                    try:
                                        page_title = driver.title
                                        print(f"Page Title: {page_title}")
                                        
                                        current_url = driver.current_url
                                        print(f"Current URL: {current_url}")
                                        
                                    except Exception as detail_error:
                                        print(f"Error extracting product details: {detail_error}")
                                    
                                    driver.back()
                                    
                                    random_delay(2, 4)
                                    
                                except Exception as product_error:
                                    print(f"Error visiting product {i+1}: {product_error}")
                                    try:
                                        driver.back()
                                        random_delay(2, 3)
                                    except:
                                        driver.get("https://www.ajio.com/")
                                        random_delay(2, 4)
                                    continue
                            
                            print(f"Completed visiting {products_to_visit} product detail pages")
                            
                        except Exception as visit_error:
                            print(f"Error during product page visits: {visit_error}")
                            import traceback
                            traceback.print_exc()
                                
                except Exception as e:
                    print(f"Error with gender filter: {e}")
                    import traceback
                    traceback.print_exc()
                
                print(f"Completed search for keyword: '{keyword}'")
                
            except TimeoutException as e:
                print(f"Timeout error searching for keyword '{keyword}': {e}")
                continue
            except Exception as e:
                print(f"Error searching for keyword '{keyword}': {e}")
                continue
        
        print("\nAll keyword searches completed!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    main()
