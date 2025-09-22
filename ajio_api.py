from curl_cffi import requests as cureq
from utils import get_random_headers
import json
from urllib.parse import quote
import time
import random
import os

search_url = "https://www.ajio.com/api/search?fields=SITE&currentPage=1&pageSize=45&format=json&classifier=intent&gridColumns=3&advfilter=true&platform=Desktop&is_ads_enable_plp=true&is_ads_enable_slp=true&showAdsOnNextPage=false&displayRatings=true&previousSource=Saas&vertexEnabled=false&segmentIds=,"

product_detail_url_base = "https://www.ajio.com/api/p/"

PROXY_LIST = []

current_proxy_index = 0

def get_proxy():
    """Get a proxy from the proxy list with rotation"""
    global current_proxy_index
    
    if not PROXY_LIST:
        print("Warning: No proxies configured. Running without proxy.")
        return None
    
    proxy = PROXY_LIST[current_proxy_index]
    return proxy

def load_proxies_from_file(filepath="proxies.txt"):
    """Load proxies from a text file (one proxy per line)"""
    global PROXY_LIST
    
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                PROXY_LIST = [line.strip() for line in f.readlines() 
                             if line.strip() and not line.strip().startswith('#')]
            print(f"Loaded {len(PROXY_LIST)} proxies from {filepath}")
        except Exception as e:
            print(f"Error loading proxies from {filepath}: {e}")
    else:
        print(f"Proxy file {filepath} not found. Using empty proxy list.")

def make_request_with_proxy(url, **kwargs):
    """Make a request with proxy support and fallback"""
    max_retries = 3
    
    for attempt in range(max_retries):
        proxy = get_proxy()
        
        try:
            if proxy:
                masked_proxy = proxy.split('@')[1] if '@' in proxy else proxy
                print(f"Making request with rotating proxy: {masked_proxy}")
                kwargs['proxies'] = {'http': proxy, 'https': proxy}
            else:
                print("Making request without proxy")
            
            response = cureq.get(url, **kwargs)
            return response
            
        except Exception as e:
            print(f"Request attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying with rotating proxy...")
                time.sleep(random.uniform(1, 2)) 
            else:
                print("All proxy attempts failed. Trying without proxy...")
                try:
                    kwargs.pop('proxies', None)
                    response = cureq.get(url, **kwargs)
                    return response
                except Exception as final_e:
                    print(f"Final request without proxy also failed: {final_e}")
                    raise final_e
    
    return None

def make_request_with_persistent_retry(url, max_attempts=10, **kwargs):
    """Make a request with persistent retry until success or max attempts reached"""
    attempt = 0
    base_delay = 2  
    
    while attempt < max_attempts:
        try:
            fresh_kwargs = kwargs.copy()
            fresh_kwargs['headers'] = get_random_headers()
            
            response = make_request_with_proxy(url, **fresh_kwargs)
            
            if response and response.status_code == 200:
                return response
            elif response and response.status_code in [403, 502, 503, 504]:
                attempt += 1
                delay = base_delay * (2 ** min(attempt, 5)) + random.uniform(0, 2)
                print(f"Got {response.status_code} error. Retrying with fresh headers in {delay:.1f}s (attempt {attempt}/{max_attempts})")
                time.sleep(delay)
                continue
            else:
                print(f"Unexpected status code: {response.status_code if response else 'No response'}")
                attempt += 1
                time.sleep(random.uniform(1, 3))
                continue
                
        except Exception as e:
            attempt += 1
            delay = base_delay * (2 ** min(attempt, 5)) + random.uniform(0, 2)
            print(f"Request failed: {e}. Retrying with fresh headers in {delay:.1f}s (attempt {attempt}/{max_attempts})")
            time.sleep(delay)
    
    print(f"Max attempts ({max_attempts}) reached. Giving up.")
    return None

def extract_size_stock_info(product_detail_data):
    """Extracts sizes where stockLevelStatus is 'inStock'."""
    in_stock_sizes = []
    try:
        variant_options = product_detail_data.get("variantOptions", [])

        for variant in variant_options:
            size = None
            variant_option_qualifiers = variant.get("variantOptionQualifiers", [])
            for qualifier in variant_option_qualifiers:
                if qualifier.get("name") == "Size*": 
                    size = qualifier.get("value")
                    break

            if not size:
                 size = variant.get("scDisplaySize")

            stock_info = variant.get("stock", {})
            stock_status = stock_info.get("stockLevelStatus")

            if size and stock_status == "inStock":
                in_stock_sizes.append(size)

    except Exception as e:
        print(f"Error extracting size/stock info: {e}")

    return in_stock_sizes

def extract_product_data(product):
    """Extract required product data from AJIO API response"""
    try:
        product_code = product.get("code", "") 

        images = []
        if "images" in product:
            for img in product["images"]:
                if "url" in img:
                    images.append(img["url"])

        current_price = product.get("price", {}).get("value", 0)
        original_price = product.get("wasPriceData", {}).get("value", current_price)

        sizes = []

        if product_code:
            try:
                time.sleep(random.uniform(0.5, 1.5))

                print(f"Fetching sizes for product {product_code}...")
                detail_response = make_request_with_persistent_retry(
                    product_detail_url_base + product_code,
                    max_attempts=3,  
                    impersonate="chrome",
                    headers=get_random_headers()
                )
                
                if detail_response and detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    sizes = extract_size_stock_info(detail_data)
                    print(f"✅ Successfully fetched sizes for product {product_code}: {sizes}")
                else:
                    print(f"❌ Failed to fetch details for {product_code} after all retries")
                    sizes = []  
            except Exception as e:
                print(f"❌ Error fetching details for {product_code}: {e}")
                sizes = []  # Empty sizes if we couldn't fetch them
        

        return {
            "name": product.get("name", ""),
            "id": product_code, 
            "images": images,
            "ratingsCount": product.get("ratingCount", "0"),
            "averageRating": product.get("averageRating", 0),
            "originalPrice": original_price,
            "currentPrice": current_price,
            "sizes": sizes
        }
    except Exception as e:
        print(f"Error extracting product data: {e}")
        return {
            "name": "",
            "id": "",
            "images": [],
            "ratingsCount": "0",
            "averageRating": 0,
            "originalPrice": 0,
            "currentPrice": 0,
            "sizes": [] 
        }

def main():
    load_proxies_from_file("proxies.txt")
    
    try:
        with open("zara_keywords.json", "r") as f:
            keywords = json.load(f)
        print(f"Loaded {len(keywords)} keywords from zara_keywords.json")
    except Exception as e:
        print(f"Error loading keywords file: {e}")
        return

    all_scraped_data = []

    for keyword in keywords:
        lowercase_keyword = keyword["keyword"].lower()
        encoded_keyword = quote(lowercase_keyword)
        print(f"Searching for keyword: {lowercase_keyword}")

        try:
            response = make_request_with_proxy(
                search_url + "&query=" + encoded_keyword + '%3Arelevance' + '&text=' + encoded_keyword,
                impersonate="chrome",
                headers=get_random_headers()
            )
            status_code = response.status_code if response else 0
            print(f"Status code for search '{lowercase_keyword}': {status_code}")

            if status_code == 200:
                print("AJIO Search API is working")
                response_data = response.json()
                products = response_data.get("products", [])

                keyword_products = []
                for i, product in enumerate(products[:10]):
                    product_data = extract_product_data(product)
                    if product_data and product_data['name']:
                        keyword_products.append(product_data)
                        print(f"Extracted product {i+1}: {product_data['name']} (ID: {product_data['id']}) - Sizes: {product_data['sizes']}")

                all_scraped_data.append({
                    "keyword": lowercase_keyword,
                    "products": keyword_products
                })

                print(f"Successfully scraped {len(keyword_products)} products for keyword: {lowercase_keyword}")
                
                print("⏳ Rate limiting: Waiting 3-5 seconds before next keyword...")
                time.sleep(random.uniform(3, 5))
                
            else:
                print(f"AJIO Search API failed for '{lowercase_keyword}'")
                all_scraped_data.append({
                    "keyword": lowercase_keyword,
                    "products": []
                })
                
                print("⏳ Rate limiting: Waiting 2-3 seconds before next keyword...")
                time.sleep(random.uniform(2, 3))

        except Exception as e:
            print(f"Error processing keyword {lowercase_keyword}: {e}")
            all_scraped_data.append({
                "keyword": lowercase_keyword,
                "products": []
            })

    try:
        with open("ajio_scraped_data.json", "w") as f:
            json.dump(all_scraped_data, f, indent=2)
        print(f"\nSuccessfully saved scraped data to ajio_scraped_data.json")
        print(f"Total keywords processed: {len(all_scraped_data)}")
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")


if __name__ == "__main__":
    main()