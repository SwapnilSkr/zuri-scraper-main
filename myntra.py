#!/usr/bin/env python3
"""
Myntra Search Script
Navigates to Myntra.com, searches for keywords from zara_keywords.json, waits 10 seconds between searches
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
    # Load keywords from JSON file
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
        
        print("Navigating to Myntra.com...")
        driver.get("https://www.myntra.com/")
        
        print("Waiting for page to load...")
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "desktop-searchBar")))
            print("✅ Page loaded successfully - search bar found")
        except TimeoutException:
            print("❌ Page load timeout - search bar not found within 10 seconds")
            return
        
        for i, keyword_obj in enumerate(filtered_keywords):
            keyword_id = keyword_obj["id"]
            keyword = keyword_obj["keyword"]
            print(f"\nSearching for keyword {i+1}/{len(filtered_keywords)}: '{keyword}' (ID: {keyword_id})")
            
            try:
                print(f"Looking for search bar for keyword: '{keyword}'")
                search_input = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "desktop-searchBar")))
                
                search_input.clear()
                
                search_input.send_keys(keyword)
                print(f"Typed: {keyword}")
                
                search_input.send_keys(Keys.RETURN)
                print("Pressed Enter")
                
                print("Waiting for search results to load...")
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.product-base")))
                    print("✅ Search results loaded successfully")
                except TimeoutException:
                    print("⚠️ Search results may not have loaded properly, but continuing...")
                    
                try:
                  gender_category = driver.find_elements(By.CSS_SELECTOR, "label.gender-label")
                  for gender_category in gender_category:
                    if gender_category.text == "Women":
                      gender_category.click()
                      print("Clicked on women category")
                      break
                  else:
                    print("Gender category not found")
                except Exception as e:
                    print(f"Error clicking on gender category: {e}")
                    continue

                time.sleep(3)
                
                print("Looking for product links...")
                product_elements = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
                print(f"Found {len(product_elements)} product elements")
                
                products_to_visit = min(10, len(product_elements))
                print(f"Visiting first {products_to_visit} product pages...")
                
                for j in range(products_to_visit):
                    try:
                        print(f"\nVisiting product {j+1}/{products_to_visit}")
                        
                        product_elements = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
                        
                        if j >= len(product_elements):
                            print(f"No more product elements available (tried to access index {j})")
                            break
                        
                        product_element = product_elements[j]
                        product_link = product_element.find_element(By.CSS_SELECTOR, "a")
                        product_url = product_link.get_attribute("href")
                        print(f"Product URL: {product_url}")
                        
                        original_window = driver.current_window_handle
                        
                        
                        driver.execute_script("arguments[0].setAttribute('target', '_self');", product_link)
                        product_link.click()
                        print("Clicked on product link")
                        
                        
                        print("Waiting for product page to load...")


                        time.sleep(3)

                        
                        product_data = {
                            "site": "myntra",
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
                            "product_description": "Not found",
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
                            product_title = driver.find_element(By.CLASS_NAME, "pdp-title").text
                            product_data["brand_name"] = product_title
                            print(f"Product title: {product_title}")
                        except Exception as e:
                            print(f"Product title not found: {e}")

                        
                        try:
                            product_name = driver.find_element(By.CLASS_NAME, "pdp-name").text
                            product_data["product_name"] = product_name
                            print(f"Product name: {product_name}")
                        except Exception as e:
                            print(f"Product name not found: {e}")

                        
                        try:
                            product_current_price = driver.find_element(By.CLASS_NAME, "pdp-price").text
                            product_data["current_product_price"] = product_current_price
                            print(f"Product price: {product_current_price}")
                        except Exception as e:
                            print(f"Product price not found: {e}")

                        
                        try:
                            product_original_price = driver.find_element(By.CSS_SELECTOR, "span.pdp-mrp>s").text
                            product_data["original_product_price"] = product_original_price
                            print(f"Product original price: {product_original_price}")
                        except Exception as e:
                            print(f"Product original price not found: {e}")

                        
                        try:
                            product_description = driver.find_element(By.CLASS_NAME, "pdp-product-description-content").text
                            product_data["product_description"] = product_description
                            print(f"Product description: {product_description}")
                        except Exception as e:
                            print(f"Product description not found: {e}")


                        try:
                            rating_container = driver.find_element(By.CSS_SELECTOR, "div.index-overallRating")
                            
                            rating_text = rating_container.find_element(By.CSS_SELECTOR, "div").text
                            product_data["product_rating"] = rating_text
                            print(f"Product rating: {product_data['product_rating']}")
                            
                            ratings_count_element = rating_container.find_element(By.CSS_SELECTOR, "div.index-ratingsCount")
                            ratings_text = ratings_count_element.text
                            import re
                            ratings_match = re.search(r'(\d+)', ratings_text)
                            if ratings_match:
                                product_data["product_rating_count"] = ratings_match.group(1)
                                print(f"Total ratings: {product_data['product_rating_count']}")
                            
                        except Exception as e:
                            print(f"Error extracting rating/ratings count: {e}")

                        try:
                            product_sizes_available = driver.find_elements(By.CSS_SELECTOR, "p.size-buttons-unified-size")
                            product_data["product_sizes_available"] = []
                            for size_element in product_sizes_available:
                                if size_element.text:
                                    size_text = size_element.text
                                    product_data["product_sizes_available"].append(size_text)
                            print(f"Product sizes available: {product_data['product_sizes_available']}")
                        except Exception as e:
                            print(f"Error extracting product sizes available: {e}")

                        try:
                            try:
                                image_container = driver.find_element(By.CSS_SELECTOR, ".image-grid-container")
                                driver.execute_script("arguments[0].scrollIntoView(true);", image_container)
                                print("Scrolled to image container")
                                time.sleep(2)
                            except:
                                print("Image container not found, continuing...")
                            
                            image_divs = driver.find_elements(By.CSS_SELECTOR, "div.image-grid-col50>div.image-grid-imageContainer>div.image-grid-image")
                            print(f"Found {len(image_divs)} image-grid-image divs")
                            
                            for img_div in image_divs:
                                style_attr = img_div.get_attribute("style")
                                if style_attr and "background-image" in style_attr:
                                    import re
                                    url_match = re.search(r'url\(["\']?([^"\']+)["\']?\)', style_attr)
                                    if url_match:
                                        image_url = url_match.group(1)
                                        product_data["product_image_urls"].append(image_url)
                                        print(f"Extracted image URL: {image_url}")
                            
                            print(f"Total product images found: {len(product_data['product_image_urls'])}")
                            print(f"Product images: {product_data['product_image_urls']}")
                            
                        except Exception as e:
                            print(f"Error extracting product images: {e}")

                        all_scraped_data.append(product_data)
                        print(f"Added product data for: {product_data['product_name']}")
                        
                        print("Going back to search results...")
                        driver.back()
                        time.sleep(2)
                        
                    except Exception as e:
                        print(f"Error visiting product {j+1}: {e}")
                        continue
                
                print(f"Completed visiting {products_to_visit} product pages for keyword: '{keyword}'")
                
                print(f"Completed search for keyword: '{keyword}'")
                
            except TimeoutException as e:
                print(f"Timeout error searching for keyword '{keyword}': {e}")
                continue
            except Exception as e:
                print(f"Error searching for keyword '{keyword}': {e}")
                continue
        
        print(f"\nSaving {len(all_scraped_data)} products to myntra_scraped_data.json...")
        try:
            with open('myntra_scraped_data.json', 'w', encoding='utf-8') as f:
                json.dump(all_scraped_data, f, indent=2, ensure_ascii=False)
            print("Data saved successfully to myntra_scraped_data.json")
        except Exception as e:
            print(f"Error saving data: {e}")
        
        print("\nAll keyword searches completed!")
        
    except KeyboardInterrupt:
        print("\n🛑 Scraping interrupted by user (Ctrl+C)")
        print("💾 Saving all collected data before shutdown...")
        
        try:
            with open('myntra_scraped_data.json', 'w', encoding='utf-8') as f:
                json.dump(all_scraped_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved {len(all_scraped_data)} products to myntra_scraped_data.json")
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
