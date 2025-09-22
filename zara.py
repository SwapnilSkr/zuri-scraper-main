#!/usr/bin/env python3
"""
Simple Zara Navigation Script
Navigates to Zara.com, searches for keywords, waits, and closes
"""

import time
import json
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def extract_images_from_json_data(driver):
    """Extract product images from embedded JSON data"""
    image_urls = []
    
    try:
        print("Looking for product JSON data...")
        
        # Get the page source
        page_source = driver.page_source
        
        # Look for product data JSON (common patterns)
        import re
        import json
        
        # Pattern 1: Look for window.__INITIAL_STATE__ or similar
        json_patterns = [
            r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
            r'window\.__PRELOADED_STATE__\s*=\s*({.*?});',
            r'window\.zara\s*=\s*({.*?});',
            r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>',
            r'productDetail["\']\s*:\s*({.*?})[,}]',
            r'"productDetail"\s*:\s*({.*?})[,}]'
        ]
        
        found_json = False
        for pattern in json_patterns:
            matches = re.findall(pattern, page_source, re.DOTALL)
            for match in matches:
                try:
                    # Clean up the JSON string
                    json_str = match.strip()
                    if json_str.startswith('{') and json_str.endswith('}'):
                        # Try to parse as JSON
                        data = json.loads(json_str)
                        print("✅ Found and parsed JSON data")
                        
                        # Recursively search for image URLs in the JSON
                        def extract_image_urls_from_dict(obj, urls):
                            if isinstance(obj, dict):
                                for key, value in obj.items():
                                    if isinstance(value, str) and is_valid_product_image(value):
                                        clean_url = clean_image_url(value)
                                        if clean_url and clean_url not in urls:
                                            urls.append(clean_url)
                                            print(f"    ✅ Found in JSON: {clean_url[:80]}...")
                                    elif isinstance(value, (dict, list)):
                                        extract_image_urls_from_dict(value, urls)
                            elif isinstance(obj, list):
                                for item in obj:
                                    extract_image_urls_from_dict(item, urls)
                        
                        extract_image_urls_from_dict(data, image_urls)
                        found_json = True
                        break
                except json.JSONDecodeError:
                    continue
            if found_json:
                break
        
        # Pattern 2: Look for specific product data scripts
        if not image_urls:
            print("Searching script tags for product images...")
            script_tags = driver.find_elements(By.TAG_NAME, "script")
            for i, script in enumerate(script_tags):
                script_content = script.get_attribute("innerHTML")
                if script_content and ('product' in script_content.lower() or 'image' in script_content.lower()):
                    print(f"  Found relevant script {i+1}")
                    # Look for image arrays in the script
                    img_matches = re.findall(r'https?://[^"\s]*?zara\.net[^"\s]*?\.(?:jpg|jpeg|png|webp)[^"\s]*', script_content)
                    print(f"    Found {len(img_matches)} image URLs in script")
                    
                    # Process all images from this script
                    script_valid_count = 0
                    for url in img_matches:
                        if is_valid_product_image(url):
                            clean_url = clean_image_url(url)
                            if clean_url and clean_url not in image_urls:
                                image_urls.append(clean_url)
                                script_valid_count += 1
                                print(f"    ✅ Added from script: {clean_url[:80]}...")
                        else:
                            print(f"    ❌ Invalid from script: {url[:80]}...")
                    
                    print(f"    Added {script_valid_count} valid images from this script")
        
        # Pattern 3: Look for window.__INITIAL_STATE__ or similar
        if not image_urls:
            print("Searching for window.__INITIAL_STATE__ or similar...")
            try:
                initial_state = driver.execute_script("""
                    if (window.__INITIAL_STATE__) {
                        return window.__INITIAL_STATE__;
                    }
                    if (window.__PRELOADED_STATE__) {
                        return window.__PRELOADED_STATE__;
                    }
                    if (window.__NEXT_DATA__) {
                        return window.__NEXT_DATA__;
                    }
                    return null;
                """)
                
                if initial_state:
                    print("Found initial state data")
                    # Recursively search for image URLs
                    def extract_from_state(obj, urls):
                        if isinstance(obj, dict):
                            for key, value in obj.items():
                                if isinstance(value, str) and is_valid_product_image(value):
                                    clean_url = clean_image_url(value)
                                    if clean_url and clean_url not in urls:
                                        urls.append(clean_url)
                                        print(f"    ✅ Added from state: {clean_url[:80]}...")
                                elif isinstance(value, (dict, list)):
                                    extract_from_state(value, urls)
                        elif isinstance(obj, list):
                            for item in obj:
                                extract_from_state(item, urls)
                    
                    extract_from_state(initial_state, image_urls)
                    
            except Exception as e:
                print(f"Error extracting from initial state: {e}")
        
        print(f"Found {len(image_urls)} images from JSON data")
        return image_urls
        
    except Exception as e:
        print(f"Error extracting images from JSON: {e}")
        return []

def force_all_images_to_load(driver):
    """Aggressively force all product images to load by simulating user interaction"""
    try:
        print("Aggressively forcing all product images to load...")
        
        # First, try to make the browser think it's visible
        driver.execute_script("""
            // Make browser think it's visible and focused
            Object.defineProperty(document, 'hidden', { value: false });
            Object.defineProperty(document, 'visibilityState', { value: 'visible' });
            
            // Trigger visibility change event
            document.dispatchEvent(new Event('visibilitychange'));
            
            // Force focus
            window.focus();
            document.body.focus();
        """)
        
        # Scroll through all product images to trigger loading
        product_images = driver.find_elements(By.CSS_SELECTOR, "img.media-image__image")
        print(f"Found {len(product_images)} product images to force load")
        
        for i, img in enumerate(product_images):
            try:
                # Scroll to each image
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", img)
                time.sleep(0.5)
                
                # Force load with JavaScript
                driver.execute_script("""
                    const img = arguments[0];
                    
                    // Force all possible loading mechanisms
                    if (img.dataset.src && img.dataset.src !== img.src) {
                        img.src = img.dataset.src;
                    }
                    if (img.dataset.lazy && img.dataset.lazy !== img.src) {
                        img.src = img.dataset.lazy;
                    }
                    if (img.dataset.original && img.dataset.original !== img.src) {
                        img.src = img.dataset.original;
                    }
                    
                    // Force intersection
                    img.style.visibility = 'visible';
                    img.style.display = 'block';
                    img.style.opacity = '1';
                    
                    // Trigger all events
                    img.dispatchEvent(new Event('load'));
                    img.dispatchEvent(new Event('error'));
                    img.dispatchEvent(new Event('click'));
                    
                    // Force parent to trigger loading
                    if (img.parentElement) {
                        img.parentElement.dispatchEvent(new Event('mouseenter'));
                        img.parentElement.dispatchEvent(new Event('mouseover'));
                    }
                """, img)
                
                print(f"  Forced load for image {i+1}")
                
            except Exception as e:
                print(f"  Error forcing load for image {i+1}: {e}")
                continue
        
        # Final aggressive loading attempt
        driver.execute_script("""
            // Force all lazy loading libraries to activate
            if (window.lazyLoad) {
                window.lazyLoad.update();
            }
            if (window.LazyLoad) {
                window.LazyLoad.update();
            }
            
            // Force any Zara-specific loading
            if (window.zara && window.zara.loadImages) {
                window.zara.loadImages();
            }
            if (window.Zara && window.Zara.loadImages) {
                window.Zara.loadImages();
            }
            
            // Force intersection observers
            const observers = document.querySelectorAll('[data-observer]');
            observers.forEach(obs => {
                obs.dispatchEvent(new Event('intersect'));
            });
            
            // Trigger all possible events
            window.dispatchEvent(new Event('scroll'));
            window.dispatchEvent(new Event('resize'));
            window.dispatchEvent(new Event('load'));
            window.dispatchEvent(new Event('DOMContentLoaded'));
            document.dispatchEvent(new Event('visibilitychange'));
        """)
        
        # Wait for all images to load
        time.sleep(3)
        
    except Exception as e:
        print(f"Error in aggressive image loading: {e}")

def get_product_images_from_page_source(driver):
    """Extract product images from page source with strict filtering"""
    try:
        import re
        
        # Get all image URLs from the page that look like product images
        page_source = driver.page_source
        # Look for Zara product image patterns
        pattern = r'https://static\.zara\.net/assets/public/[^"\s]*?\.(?:jpg|jpeg|png|webp)[^"\s]*'
        matches = re.findall(pattern, page_source)
        
        # Filter out placeholders and duplicates with strict validation
        image_urls = []
        for url in matches:
            if is_valid_product_image(url):
                clean_url = clean_image_url(url)
                if clean_url and clean_url not in image_urls:
                    image_urls.append(clean_url)
        
        print(f"Found {len(image_urls)} valid product images from page source")
        return image_urls
        
    except Exception as e:
        print(f"Error extracting images: {e}")
        return []

def extract_product_images_comprehensive(driver):
    """Extract product images using focused methods targeting actual product photos"""
    image_urls = []
    
    print("\n=== Focused Product Image Extraction ===")
    
    # Aggressively force all images to load first
    force_all_images_to_load(driver)
    
    # Method 1: Target specific product image selectors with enhanced loading
    try:
        print("Method 1: Targeting picture.media-image > img.media-image__image...")
        
        # First, try the exact selector you want
        picture_elements = driver.find_elements(By.CSS_SELECTOR, "picture.media-image")
        print(f"Found {len(picture_elements)} picture.media-image elements")
        
        for i, picture in enumerate(picture_elements):
            try:
                print(f"  Processing picture element {i+1}...")
                
                # Look for img inside the picture element
                img_elements = picture.find_elements(By.CSS_SELECTOR, "img.media-image__image")
                print(f"    Found {len(img_elements)} img.media-image__image elements in picture {i+1}")
                
                for j, img in enumerate(img_elements):
                    try:
                        # Force scroll to element and wait longer
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img)
                        time.sleep(1)  # Longer wait for loading
                        
                        # Force image loading with JavaScript - more aggressive approach
                        driver.execute_script("""
                            const img = arguments[0];
                            
                            // Log current state
                            console.log('Image src:', img.src);
                            console.log('Image data-src:', img.dataset.src);
                            console.log('Image data-lazy:', img.dataset.lazy);
                            console.log('Image data-original:', img.dataset.original);
                            
                            // Force src attribute update from any data attribute
                            if (img.dataset.src && img.dataset.src !== img.src) {
                                img.src = img.dataset.src;
                                console.log('Set src from data-src:', img.dataset.src);
                            }
                            if (img.dataset.lazy && img.dataset.lazy !== img.src) {
                                img.src = img.dataset.lazy;
                                console.log('Set src from data-lazy:', img.dataset.lazy);
                            }
                            if (img.dataset.original && img.dataset.original !== img.src) {
                                img.src = img.dataset.original;
                                console.log('Set src from data-original:', img.dataset.original);
                            }
                            
                            // Force load events
                            img.dispatchEvent(new Event('load'));
                            img.dispatchEvent(new Event('error'));
                            
                            // Force intersection observer to trigger
                            if (img.parentElement) {
                                img.parentElement.scrollIntoView();
                            }
                        """, img)
                        
                        time.sleep(1)  # Wait for JavaScript to execute
                        
                        # Try multiple attributes in order of preference
                        src = img.get_attribute('src')
                        data_src = img.get_attribute('data-src')
                        data_lazy = img.get_attribute('data-lazy')
                        data_original = img.get_attribute('data-original')
                        
                        # Debug all attributes and DOM structure
                        print(f"    Image {j+1} attributes:")
                        print(f"      src: '{src[:100] if src else 'None'}...'")
                        print(f"      data-src: '{data_src[:100] if data_src else 'None'}...'")
                        print(f"      data-lazy: '{data_lazy[:100] if data_lazy else 'None'}...'")
                        print(f"      data-original: '{data_original[:100] if data_original else 'None'}...'")
                        
                        # Check all data attributes
                        all_attrs = driver.execute_script("""
                            const img = arguments[0];
                            const attrs = {};
                            for (let attr of img.attributes) {
                                attrs[attr.name] = attr.value;
                            }
                            return attrs;
                        """, img)
                        
                        print(f"      All attributes: {all_attrs}")
                        
                        # Check parent elements for image data
                        parent_data = driver.execute_script("""
                            const img = arguments[0];
                            const parent = img.parentElement;
                            const grandparent = parent ? parent.parentElement : null;
                            
                            return {
                                parent_tag: parent ? parent.tagName : 'None',
                                parent_class: parent ? parent.className : 'None',
                                grandparent_tag: grandparent ? grandparent.tagName : 'None',
                                grandparent_class: grandparent ? grandparent.className : 'None',
                                parent_attrs: parent ? Object.fromEntries(Array.from(parent.attributes).map(attr => [attr.name, attr.value])) : {},
                                grandparent_attrs: grandparent ? Object.fromEntries(Array.from(grandparent.attributes).map(attr => [attr.name, attr.value])) : {}
                            };
                        """, img)
                        
                        print(f"      Parent structure: {parent_data}")
                        
                        # Use the best available source
                        final_src = src or data_src or data_lazy or data_original
                        
                        if final_src and final_src.strip():
                            # Check if it's a transparent background first
                            if 'transparent-background' in final_src:
                                print(f"    ❌ Skipping transparent background image")
                                continue
                                
                            # Check if it's a valid product image
                            if is_valid_product_image(final_src):
                                clean_url = clean_image_url(final_src)
                                if clean_url and clean_url not in image_urls:
                                    image_urls.append(clean_url)
                                    print(f"    ✅ Product image {len(image_urls)}: {clean_url[:80]}...")
                            else:
                                print(f"    ❌ Invalid product image: {final_src[:80]}...")
                        else:
                            print(f"    ❌ No valid src found for image {j+1}")
                            
                    except Exception as e:
                        print(f"    Error processing image {j+1} in picture {i+1}: {e}")
                        continue
                        
            except Exception as e:
                print(f"  Error processing picture {i+1}: {e}")
                continue
                
        print(f"Method 1 extracted {len(image_urls)} valid images")
                
    except Exception as e:
        print(f"Method 1 failed: {e}")
    
    # Method 2: Fallback to direct img.media-image__image selector
    if not image_urls:
        try:
            print("Method 2: Direct img.media-image__image selector...")
            img_elements = driver.find_elements(By.CSS_SELECTOR, "img.media-image__image")
            print(f"Found {len(img_elements)} img.media-image__image elements")
            
            for i, img in enumerate(img_elements):
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img)
                    time.sleep(0.5)
                    
                    src = img.get_attribute('src') or img.get_attribute('data-src') or img.get_attribute('data-lazy')
                    
                    if src and is_valid_product_image(src):
                        clean_url = clean_image_url(src)
                        if clean_url and clean_url not in image_urls:
                            image_urls.append(clean_url)
                            print(f"  ✅ Product image {len(image_urls)}: {clean_url[:80]}...")
                except Exception as e:
                    print(f"  Error processing image {i+1}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Method 2 failed: {e}")
    
    # Method 3: Extract from product JSON data (most reliable for actual product images)
    if not image_urls:
        print("Method 3: Extracting from product JSON data...")
        json_images = extract_images_from_json_data(driver)
        print(f"Found {len(json_images)} total images from JSON")
        
        # Filter JSON images to only include actual product images
        for i, url in enumerate(json_images):
            print(f"  JSON image {i+1}: {url[:100]}...")
            if is_valid_product_image(url):
                clean_url = clean_image_url(url)
                if clean_url and clean_url not in image_urls:
                    image_urls.append(clean_url)
                    print(f"    ✅ Valid product image {len(image_urls)}: {clean_url[:80]}...")
            else:
                print(f"    ❌ Invalid product image: {url[:80]}...")
    
    # Method 4: Try to extract from page source with more aggressive patterns
    if not image_urls:
        print("Method 4: Extracting from page source with aggressive patterns...")
        page_source_images = get_product_images_from_page_source(driver)
        for url in page_source_images:
            if url not in image_urls:
                image_urls.append(url)
                print(f"  ✅ Page source image {len(image_urls)}: {url[:80]}...")
    
    print(f"\nFinal product images: {len(image_urls)} images found")
    return image_urls

def is_valid_product_image(url):
    """Check if URL is a valid product image (not marketing/banner)"""
    if not url:
        return False
    
    # Exclude obvious non-product images
    exclude_patterns = [
        'transparent-background',
        'stdstatic',  # Standard static files
        'poster',     # Video posters
        'subhome',    # Homepage banners
        'xmedia',     # Marketing media
        'joinlife',   # Marketing campaigns
        'anniversary', # Marketing campaigns
        'north-woman', # Marketing campaigns
        'north-kids',  # Marketing campaigns
        'north-man',   # Marketing campaigns
        'beauty',      # Category banners
        'arizona',     # Marketing campaigns
        'image-portrait-fit',  # Marketing images
        'image-landscape-fit', # Marketing images
        'image-portrait-fill', # Marketing images
        'image-landscape-fill', # Marketing images
    ]
    
    for pattern in exclude_patterns:
        if pattern in url.lower():
            return False
    
    # Must be from Zara's CDN
    if 'static.zara.net/assets/public' not in url:
        return False
    
    # Must have a valid image extension
    if not any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
        return False
    
    # Should have product-like naming pattern (less strict validation)
    product_patterns = [
        '-p.jpg',     # Primary product image
        '-a1.jpg',    # Alternative view 1
        '-e1.jpg',    # Extra view 1
        '-e2.jpg',    # Extra view 2
        '-e3.jpg',    # Extra view 3
        '-e4.jpg',    # Extra view 4
        '-a2.jpg',    # Alternative view 2
        '-a3.jpg',    # Alternative view 3
        '-a4.jpg',    # Alternative view 4
    ]
    
    # Check if it matches any product pattern
    for pattern in product_patterns:
        if pattern in url:
            return True
    
    # Additional check: should have product ID pattern (numbers followed by -p, -a1, -e1, etc.)
    import re
    product_id_pattern = r'/\d{11}-[pae]\d*\.jpg'
    if re.search(product_id_pattern, url):
        return True
    
    # More flexible pattern: any 11-digit number followed by dash and letter/number
    flexible_pattern = r'/\d{11}-[a-z]\d*\.jpg'
    if re.search(flexible_pattern, url):
        return True
    
    # Even more flexible: any path that looks like a product image
    if '/assets/public/' in url and any(ext in url for ext in ['.jpg', '.jpeg', '.png', '.webp']):
        # Check if it has a reasonable product-like structure
        if re.search(r'/\d{6,12}', url):  # Has some numbers that could be product ID
            return True
    
    return False

def clean_image_url(url):
    """Clean and normalize image URL"""
    if not url:
        return None
    
    # Remove width parameters and normalize
    url = url.replace('&w={width}', '').replace('&w=1920', '').replace('&w=2400', '')
    url = url.replace('&amp;', '&')
    
    # Remove any trailing parameters that might cause issues
    if '?' in url:
        base_url = url.split('?')[0]
        # Keep timestamp parameter if it exists
        if 'ts=' in url:
            ts_part = url.split('ts=')[1].split('&')[0]
            url = f"{base_url}?ts={ts_part}"
        else:
            url = base_url
    
    return url.strip()

def main():
    # Load keywords from JSON file
    try:
        with open('keywords.json', 'r') as f:
            keywords_data = json.load(f)
        print(f"Loaded {len(keywords_data)} keywords from keywords.json")
    except Exception as e:
        print(f"Error loading keywords file: {e}")
        return
    
    # Define keyword range (modify these values to scrape different ranges)
    start_id = 421
    end_id = 525
    
    # Filter keywords based on ID range
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
    
    # Initialize list to store all scraped data
    all_scraped_data = []
    
    # Set up Chrome options (prevent background throttling and ensure images load when minimized)
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
    # Ensure images load even when window is not visible
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--disable-extensions")
    # Prevent throttling when minimized
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-background-networking")
    # Force visibility
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--disable-features=TranslateUI")
    
    # Initialize the driver with proper Chrome path for macOS
    try:
        # Try to get the correct ChromeDriver for ARM64 Mac
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Error initializing Chrome driver: {e}")
        print("Trying alternative Chrome path...")
        # Alternative approach for macOS
        chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Navigate to Zara.com
        print("Navigating to Zara.com...")
        driver.get("https://www.zara.com/in/")
        
        # Wait for page to load
        time.sleep(3)
        
        # Find the link with class "layout-header-action__link"
        print("Looking for link with class 'layout-header-action__link'...")
        link_element = driver.find_element(By.CLASS_NAME, "layout-header-action__link")
        
        # Get the href
        href = link_element.get_attribute("href")
        print(f"Found link with href: {href}")
        
        # Click the link
        print("Clicking the link...")
        link_element.click()
        
        # Wait for the new page to load
        time.sleep(3)
        
        # Loop through each keyword
        for i, keyword_obj in enumerate(filtered_keywords):
            keyword_id = keyword_obj["id"]
            keyword = keyword_obj["keyword"]
            print(f"\nSearching for keyword {i+1}/{len(filtered_keywords)}: '{keyword}' (ID: {keyword_id})")
            
            # Find the search input with id "search-home-form-combo-input"
            search_input = driver.find_element(By.ID, "search-home-form-combo-input")
            
            # Clear the input field
            search_input.clear()
            
            # Type the keyword
            search_input.send_keys(keyword)
            print(f"Typed: {keyword}")
            
            # Hit Enter
            search_input.send_keys(Keys.RETURN)
            print("Pressed Enter")
            
            # Wait for search results to load
            time.sleep(3)
            
            # Find all product result links
            print("Looking for product result links...")
            product_links = driver.find_elements(By.CLASS_NAME, "product-grid-product__link")
            print(f"Found {len(product_links)} product links")
            
            # Visit first 10 results (or all if less than 10)
            results_to_visit = min(10, len(product_links))
            print(f"Visiting first {results_to_visit} results...")
            
            for j in range(results_to_visit):
                try:
                    print(f"\nVisiting result {j+1}/{results_to_visit}")
                    
                    # Re-find product links each time to avoid stale element reference
                    product_links = driver.find_elements(By.CLASS_NAME, "product-grid-product__link")
                    
                    if j >= len(product_links):
                        print(f"No more product links available (tried to access index {j})")
                        break
                    
                    # Get the product link
                    product_link = product_links[j]
                    product_url = product_link.get_attribute("href")
                    print(f"Product URL: {product_url}")
                    
                    # Click on the product link
                    product_link.click()
                    print("Clicked on product link")
                    
                    # Wait for product page to load
                    time.sleep(3)

                    # Initialize product data structure with unified format
                    product_data = {
                        "site": "zara",
                        "product_url": product_url,
                        "keyword_id": keyword_id,
                        "keyword": keyword,
                        "product_id": "Not found",
                        "brand_name": "Not applicable",
                        "product_name": "Not found",
                        "product_rating": "Not applicable",
                        "product_rating_count": "Not applicable",
                        "current_product_price": "Not found",
                        "original_product_price": "Not found",
                        "product_color": "Not found",
                        "product_description": "Not found",
                        "product_sizes_available": [],
                        "product_sizes_coming_soon": [],
                        "product_sizes_out_of_stock": [],
                        "product_image_urls": [],
                        "additional_information": "Not found"
                    }

                    # Extract product ID from URL
                    try:
                        current_url = driver.current_url
                        parsed_url = urlparse(current_url)
                        query_params = parse_qs(parsed_url.query)
                        product_id = query_params.get('v1', ['Not found'])[0]
                        product_data["product_id"] = product_id
                        print(f"Product ID: {product_id}")
                    except Exception as e:
                        print(f"Product ID not found: {e}")

                    # Extract product header
                    try:
                        product_header = driver.find_element(By.CLASS_NAME, "product-detail-info__header-name")
                        product_data["product_name"] = product_header.text
                        print(f"Product header text: {product_data['product_name']}")
                    except Exception as e:
                        print(f"Product header not found: {e}")
                    
                    # Extract original product price
                    try:
                        product_price = driver.find_element(By.CSS_SELECTOR, "span.price-old__amount>div.money-amount>span.money-amount__main")
                        product_data["original_product_price"] = product_price.text
                        print(f"Product price text: {product_data['original_product_price']}")
                    except Exception as e:
                        print(f"Product price not found: {e}")

                    # Extract current product price
                    try:
                        product_price = driver.find_element(By.CSS_SELECTOR, "span.price-current__amount>div.money-amount>span.money-amount__main")
                        product_data["current_product_price"] = product_price.text
                        print(f"Product price text: {product_data['current_product_price']}")
                    except Exception as e:
                        print(f"Product price not found: {e}")

                    # Extract product color
                    try:
                        product_color = driver.find_element(By.CSS_SELECTOR, "p.product-color-extended-name")
                        product_data["product_color"] = product_color.text
                        print(f"Product color text: {product_data['product_color']}")
                    except Exception as e:
                        print(f"Product color not found: {e}")

                    # Extract product description
                    try:
                        product_description = driver.find_element(By.CSS_SELECTOR, "div.expandable-text__inner-content>p")
                        product_data["product_description"] = product_description.text
                        print(f"Product description text: {product_data['product_description']}")
                    except Exception as e:
                        print(f"Product description not found: {e}")

                    # Extract product composition (may not exist on all products)
                    try:
                        product_composition = driver.find_element(By.CSS_SELECTOR, "div.product-detail-composition>span")
                        product_data["additional_information"] = product_composition.text
                        print(f"Additional information: {product_data['additional_information']}")
                    except Exception as e:
                        print(f"Product composition not found: {e}")

                    # Extract product sizes
                    try:
                        add_to_bag_button = driver.find_element(By.CSS_SELECTOR, "div.product-detail-cart-buttons__main-action>button.product-detail-cart-buttons__button")
                        
                        # Scroll the button into view to avoid click interception
                        driver.execute_script("arguments[0].scrollIntoView();", add_to_bag_button)
                        time.sleep(1)
                        
                        # Use JavaScript click to avoid element interception
                        driver.execute_script("arguments[0].click();", add_to_bag_button)
                        print("Clicked on add to bag button")
                        time.sleep(2)
                        print("dropdown opened")
                        
                        product_size_dropdown = driver.find_elements(By.CSS_SELECTOR, "button.size-selector-sizes-size__button")
                        for size_button in product_size_dropdown:
                            size_label = size_button.find_element(By.CSS_SELECTOR, "div.size-selector-sizes-size__label")
                            size_text = size_label.text
                            data_qa_action = size_button.get_attribute("data-qa-action")
                            
                            if data_qa_action == "size-in-stock":
                                product_data["product_sizes_available"].append(size_text)
                            elif data_qa_action == "size-back-soon":
                                product_data["product_sizes_coming_soon"].append(size_text)
                            elif data_qa_action == "size-out-of-stock":
                                product_data["product_sizes_out_of_stock"].append(size_text)

                        print(f"Product sizes available: {product_data['product_sizes_available']}")
                        print(f"Product sizes coming soon: {product_data['product_sizes_coming_soon']}")
                        print(f"Product sizes out of stock: {product_data['product_sizes_out_of_stock']}")
                    except Exception as e:
                        print(f"Product sizes not found: {e}")

                    # Extract product images LAST (using comprehensive diagnostic function)
                    try:
                        product_data["product_image_urls"] = extract_product_images_comprehensive(driver)
                        print(f"Final product images: {len(product_data['product_image_urls'])} images found")
                        print(f"Product images: {product_data['product_image_urls']}")
                    except Exception as e:
                        print(f"Product images not found: {e}")

                    # Add product data to the main list
                    all_scraped_data.append(product_data)
                    print(f"Added product data for: {product_data['product_name']}")

                    # Go back to search results
                    print("Going back to search results...")
                    driver.back()
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error visiting result {j+1}: {e}")
                    continue
            
            print(f"Completed visiting {results_to_visit} results for keyword: '{keyword}'")
            
            # Go back to the previous page for next search (if not the last keyword)
            if i < len(keywords_data) - 1:
                print("Going back for next search...")
                driver.back()
                time.sleep(2)
        
        # Save all scraped data to individual JSON file
        print(f"\nSaving {len(all_scraped_data)} products to zara_scraped_data.json...")
        try:
            with open('zara_scraped_data.json', 'w', encoding='utf-8') as f:
                json.dump(all_scraped_data, f, indent=2, ensure_ascii=False)
            print("Data saved successfully to zara_scraped_data.json")
        except Exception as e:
            print(f"Error saving data: {e}")
        
        # Wait for 10 seconds after all searches are done
        print("\nAll searches completed. Waiting for 10 seconds...")
        time.sleep(10)
        
        print("Done!")
        
    except KeyboardInterrupt:
        print("\n🛑 Scraping interrupted by user (Ctrl+C)")
        print("💾 Saving all collected data before shutdown...")
        
        # Save all scraped data before shutting down
        try:
            with open('zara_scraped_data.json', 'w', encoding='utf-8') as f:
                json.dump(all_scraped_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved {len(all_scraped_data)} products to zara_scraped_data.json")
        except Exception as e:
            print(f"❌ Error saving data during shutdown: {e}")
        
        print("🔚 Graceful shutdown completed")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    main()
