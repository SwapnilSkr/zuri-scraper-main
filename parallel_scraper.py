#!/usr/bin/env python3
"""
Parallel Scraper Runner
Runs Nykaa and Myntra scrapers simultaneously in separate processes
and combines all results into a single scraped_data.json file
"""

import subprocess
import json
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

def run_scraper(scraper_name, scraper_file):
    """Run a single scraper and return its results"""
    print(f"🚀 Starting {scraper_name} scraper...")
    
    try:
        result = subprocess.run(
            [sys.executable, scraper_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {scraper_name} scraper completed successfully")
            return {"scraper": scraper_name, "status": "success", "output": result.stdout}
        else:
            print(f"❌ {scraper_name} scraper failed with return code {result.returncode}")
            print(f"Error output: {result.stderr}")
            return {"scraper": scraper_name, "status": "failed", "error": result.stderr}
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {scraper_name} scraper timed out (this shouldn't happen anymore)")
        return {"scraper": scraper_name, "status": "timeout", "error": "Scraper timed out"}
    except Exception as e:
        print(f"💥 {scraper_name} scraper encountered an error: {e}")
        return {"scraper": scraper_name, "status": "error", "error": str(e)}

def combine_scraped_data():
    """Combine all individual scraped data files into one unified file"""
    print("🔄 Combining scraped data from all sources...")
    
    all_products = []
    scrapers = [
        {"name": "nykaa", "file": "nykaa_scraped_data.json"},
        {"name": "myntra", "file": "myntra_scraped_data.json"}
    ]
    
    files_found = 0
    for scraper in scrapers:
        file_path = scraper["file"]
        if os.path.exists(file_path):
            files_found += 1
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_products.extend(data)
                        print(f"✅ Added {len(data)} products from {scraper['name']}")
                    else:
                        print(f"⚠️ {scraper['name']} data is not in expected list format")
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
        else:
            print(f"⚠️ {file_path} not found - {scraper['name']} may not have completed successfully")
    
    print(f"📊 Found {files_found}/2 individual scraper data files")
    
    if all_products:
        try:
            with open('scraped_data_4.json', 'w', encoding='utf-8') as f:
                json.dump(all_products, f, indent=2, ensure_ascii=False)
            print(f"🎉 Successfully combined {len(all_products)} products into scraped_data_4.json")
            return True
        except Exception as e:
            print(f"❌ Error saving combined data: {e}")
            return False
    else:
        print("⚠️ No products found to combine")
        return False

def cleanup_individual_files():
    """Clean up individual scraper output files after combining"""
    print("\n🧹 Cleaning up individual scraper files...")
    
    files_to_remove = [
        "nykaa_scraped_data.json",
        "myntra_scraped_data.json"
    ]
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Removed {file_path}_4")
            except Exception as e:
                print(f"⚠️ Could not remove {file_path}_4: {e}")

def main():
    """Main function to run all scrapers in parallel"""
    print("🌟 Starting Parallel Scraper System")
    print("=" * 50)
    
    try:
        _run_scrapers()
    except Exception as e:
        print(f"\n💥 Unexpected error in parallel scraper: {e}")
        print("🔄 Attempting emergency data combination...")
        try:
            combine_scraped_data()
        except Exception as combine_error:
            print(f"❌ Emergency combination also failed: {combine_error}")
        raise

def _run_scrapers():
    """Internal function to run scrapers with proper error handling"""
    
    scrapers = [
        {"name": "Nykaa", "file": "nykaa.py"},
        {"name": "Myntra", "file": "myntra.py"}
    ]
    
    missing_files = []
    for scraper in scrapers:
        if not os.path.exists(scraper["file"]):
            missing_files.append(scraper["file"])
    
    if missing_files:
        print(f"❌ Missing scraper files: {missing_files}")
        return
    
    if not os.path.exists("keywords.json"):
        print("❌ keywords.json file not found!")
        return
    
    print(f"📋 Found {len(scrapers)} scrapers to run in parallel")
    print("⏱️ Starting parallel execution...")
    
    start_time = time.time()
    
    results = []
    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_to_scraper = {
                executor.submit(run_scraper, scraper["name"], scraper["file"]): scraper["name"]
                for scraper in scrapers
            }
            
            for future in as_completed(future_to_scraper):
                scraper_name = future_to_scraper[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"💥 Exception in {scraper_name}: {e}")
                    results.append({
                        "scraper": scraper_name, 
                        "status": "exception", 
                        "error": str(e)
                    })
                    
    except KeyboardInterrupt:
        print("\n🛑 Parallel scraper interrupted by user (Ctrl+C)")
        print("💾 Attempting to save any partial data...")
        
        try:
            combine_scraped_data()
        except Exception as e:
            print(f"⚠️ Could not save partial data: {e}")
        
        print("🔚 Parallel scraper shutdown completed")
        return
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print("\n" + "=" * 50)
    print("📊 EXECUTION SUMMARY")
    print("=" * 50)
    
    successful_scrapers = []
    failed_scrapers = []
    
    for result in results:
        if result["status"] == "success":
            successful_scrapers.append(result["scraper"])
            print(f"✅ {result['scraper']}: SUCCESS")
        else:
            failed_scrapers.append(result["scraper"])
            print(f"❌ {result['scraper']}: {result['status'].upper()}")
            if "error" in result:
                print(f"   Error: {result['error'][:100]}...")
    
    print(f"\n⏱️ Total execution time: {execution_time:.2f} seconds")
    print(f"✅ Successful scrapers: {len(successful_scrapers)}")
    print(f"❌ Failed scrapers: {len(failed_scrapers)}")
    
    print("\n🔄 Checking for individual scraper data files...")
    combine_scraped_data()
    
    if successful_scrapers:
        print("\n" + "=" * 50)
        cleanup_choice = input("🧹 Do you want to remove individual scraper files? (y/n): ").lower().strip()
        if cleanup_choice in ['y', 'yes']:
            cleanup_individual_files()
        else:
            print("📁 Individual scraper files kept for debugging")
    else:
        print("📁 Individual scraper files kept (scrapers were interrupted)")
    
    print("\n🎉 Parallel scraping session completed!")
    print("=" * 50)
    
    print("\n🔄 Final data combination check...")
    try:
        combine_scraped_data()
    except Exception as e:
        print(f"⚠️ Final combination failed: {e}")

if __name__ == "__main__":
    main()
