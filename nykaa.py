#!/usr/bin/env python3
"""
Nykaa Fashion Search Script
Navigates to NykaaFashion.com, searches for keywords from zara_keywords.json, waits 3 seconds between searches
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def main():
    try:
        with open('keywords.json', 'r') as f:
            keywords_data = json.load(f)
        print(f"Loaded {len(keywords_data)} keywords from keywords.json")
    except Exception as e:
        print(f"Error loading keywords file: {e}")
        return
    
    start_id = 421
    end_id = 525
    
    filtered_keywords = []
    for keyword_obj in keywords_data:
        keyword_id = int(keyword_obj["id"])
        if start_id <= keyword_id <= end_id:
            filtered_keywords.append(keyword_obj)
    
    print(f"Scraping keywords with IDs {start_id} to {end_id}")
    print(f"Total keywords to scrape: {len(filtered_keywords)}")
    
    if not filtered_keywords:
        print(f"No keywords found in range {start_id}-{end_id}")
        return
    
    all_scraped_data = []
    
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
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--disable-features=TranslateUI")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Error initializing Chrome driver: {e}")
        print("Trying alternative Chrome path...")
        chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        wait = WebDriverWait(driver, 10)
        
        print("Navigating to Nykaa Fashion...")
        driver.get("https://www.nykaafashion.com/")
        
        print("Waiting for page to load...")
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-at='search-input']")))
            print("✅ Page loaded successfully - search input found")
        except TimeoutException:
            print("❌ Page load timeout - search input not found within 10 seconds")
            return
        
        for i, keyword_obj in enumerate(filtered_keywords):
            keyword_id = keyword_obj["id"]
            keyword = keyword_obj["keyword"]
            print(f"\nSearching for keyword {i+1}/{len(filtered_keywords)}: '{keyword}' (ID: {keyword_id})")
            
            try:
                if i > 0:
                    print("Navigating back to main page...")
                    driver.get("https://www.nykaafashion.com/")
                    time.sleep(2)
                
                print(f"Looking for search input for keyword: '{keyword}'")
                search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-at='search-input']")))
                
                search_input.clear()
                search_input.send_keys(Keys.CONTROL + "a")
                search_input.send_keys(Keys.DELETE)
                print(f"Cleared search input for keyword: '{keyword}'")
                
                search_input.send_keys(keyword)
                print(f"Typed: {keyword}")
                
                search_input.send_keys(Keys.RETURN)
                print("Pressed Enter")
                
                print("Waiting for search results to load...")

                time.sleep(3)
                
                gender_div = driver.find_element(By.CSS_SELECTOR, "div.css-y9u3nm")
                if gender_div:
                    gender_div.click()
                    print("Clicked on gender div")
                else:
                    print("Gender div not found")

                try:
                    women_filter_div = driver.find_element(By.CSS_SELECTOR, "[title='Women']")
                    if women_filter_div:
                        women_filter_div.click()
                        print("Clicked on women filter div")
                        time.sleep(3)
                    else:
                        print("Women filter div not found")
                except Exception as e:
                    print(f"Error clicking on women filter div: {e}")
                    continue

                try:
                    found_products = driver.find_elements(By.CSS_SELECTOR,"div.css-384pms")
                    print(f"Found {len(found_products)} products")

                    products_to_visit = min(10, len(found_products))
                    print(f"Visiting first {products_to_visit} product pages...")

                    for j in range(products_to_visit):
                        try:
                            print(f"\nVisiting product {j+1}/{products_to_visit}")

                            found_products = driver.find_elements(By.CSS_SELECTOR,"div.css-384pms")
                            
                            if j >= len(found_products):
                                print(f"No more product elements available (tried to access index {j})")
                                break

                            product = found_products[j]
                            product_link = product.find_element(By.CSS_SELECTOR, "a")
                            product_url = product_link.get_attribute("href")
                            print(f"Product URL: {product_url}")

                            print(f"Navigating directly to: {product_url}")
                            driver.get(product_url)

                            print("Waiting for product page to load...")
                            time.sleep(3)
                        
                            product_data = {
                                "site": "nykaa_fashion",
                                "product_url": product_url,
                                "keyword_id": keyword_id,
                                "keyword": keyword,
                                "product_id": "Not found",
                                "brand_name": "Not found",
                                "product_name": "Not found",
                                "product_rating": "Not found",
                                "product_rating_count": "Not found",
                                "current_product_price": "Not found",
                                "original_product_price": "Not found",
                                "product_color": "Not applicable",
                                "product_description": "Not applicable",
                                "product_sizes_available": [],
                                "product_sizes_coming_soon": [],
                                "product_sizes_out_of_stock": [],
                                "product_image_urls": [],
                                "additional_information": "Not applicable"
                            }

                            try:
                                current_url = driver.current_url
                                import re
                                product_id_match = re.search(r'/p/(\d+)', current_url)
                                if product_id_match:
                                    product_data["product_id"] = product_id_match.group(1)
                                    print(f"Product ID: {product_data['product_id']}")
                            except Exception as e:
                                print(f"Product ID not found: {e}")

                            try:    
                                brand_name = driver.find_element(By.CLASS_NAME, "css-6mpq2k").text
                                product_data["brand_name"] = brand_name
                                print(f"Brand name: {brand_name}")
                            except Exception as e:
                                print(f"Brand name not found: {e}")

                            try:
                                product_name = driver.find_element(By.CLASS_NAME, "css-cmh3n9").text
                                product_data["product_name"] = product_name
                                print(f"Product name: {product_name}")
                            except Exception as e:
                                print(f"Product name not found: {e}")

                            try:
                                product_rating = driver.find_element(By.CSS_SELECTOR, "[data-at='product-rating']").text
                                product_data["product_rating"] = product_rating
                                print(f"Product rating: {product_rating}")
                            except Exception as e:
                                print(f"Product rating not found: {e}")

                            try:
                                product_rating_count = driver.find_element(By.CSS_SELECTOR, "div.css-gb84zx>span").text
                                product_data["product_rating_count"] = product_rating_count
                                print(f"Product rating count: {product_rating_count}")
                            except Exception as e:
                                print(f"Product rating count not found: {e}")

                            try:
                                product_current_price = driver.find_element(By.CSS_SELECTOR, "[data-at='sp-pdp']").text
                                product_data["current_product_price"] = product_current_price
                                print(f"Product current price: {product_current_price}")
                            except Exception as e:
                                print(f"Product current price not found: {e}")

                            try:
                                product_original_price = driver.find_element(By.CSS_SELECTOR, "[data-at='mrp-pdp']").text
                                product_data["original_product_price"] = product_original_price
                                print(f"Product original price: {product_original_price}")
                            except Exception as e:
                                print(f"Product original price not found: {e}")

                            try:
                                product_sizes_elements = driver.find_elements(By.CSS_SELECTOR, "[data-at='size-btn']")
                                for size_element in product_sizes_elements:
                                    size_text = size_element.text
                                    product_data["product_sizes_available"].append(size_text)
                                print(f"Product sizes: {product_data['product_sizes_available']}")
                            except Exception as e:
                                print(f"Product sizes not found: {e}")
                            
                            try:
                                product_images_elements = driver.find_elements(By.CSS_SELECTOR, "img.pdp-selector-img")
                                for image_element in product_images_elements:
                                    image_url = image_element.get_attribute("src")
                                    product_data["product_image_urls"].append(image_url)
                                print(f"Product images: {product_data['product_image_urls']}")
                            except Exception as e:
                                print(f"Product images not found: {e}")


                            all_scraped_data.append(product_data)
                            print(f"Added product data for: {product_data['product_name']}")
                            
                            print("Going back to search results...")
                            driver.back()
                            time.sleep(2)
                            
                        except Exception as e:
                            print(f"Error visiting product {j+1}: {e}")
                            try:
                                driver.back()
                                time.sleep(2)
                            except:
                                pass
                            continue
                        
                except Exception as e:
                    print(f"Error finding found products: {e}")
                    continue
                
                print("Waiting 3 seconds...")
                time.sleep(3)
                
                print(f"Completed search for keyword: '{keyword}'")
                
            except TimeoutException as e:
                print(f"Timeout error searching for keyword '{keyword}': {e}")
                continue
            except Exception as e:
                print(f"Error searching for keyword '{keyword}': {e}")
                continue
        
        print(f"\nSaving {len(all_scraped_data)} products to nykaa_scraped_data.json...")
        try:
            with open('nykaa_scraped_data.json', 'w', encoding='utf-8') as f:
                json.dump(all_scraped_data, f, indent=2, ensure_ascii=False)
            print("Data saved successfully to nykaa_scraped_data.json")
        except Exception as e:
            print(f"Error saving data: {e}")
        
        print("\nAll keyword searches completed!")
        
    except KeyboardInterrupt:
        print("\n🛑 Scraping interrupted by user (Ctrl+C)")
        print("💾 Saving all collected data before shutdown...")
        
        try:
            with open('nykaa_scraped_data.json', 'w', encoding='utf-8') as f:
                json.dump(all_scraped_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved {len(all_scraped_data)} products to nykaa_scraped_data.json")
        except Exception as e:
            print(f"❌ Error saving data during shutdown: {e}")
        
        print("🔚 Graceful shutdown completed")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    main()
