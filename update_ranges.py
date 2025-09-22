#!/usr/bin/env python3
"""
Range Updater Script
Updates the keyword ranges in all scraper files
"""

import re
import os

def update_ranges_in_file(file_path, start_id, end_id):
    """Update the start_id and end_id values in a Python file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Update start_id
        content = re.sub(
            r'start_id = \d+',
            f'start_id = {start_id}',
            content
        )
        
        # Update end_id
        content = re.sub(
            r'end_id = \d+',
            f'end_id = {end_id}',
            content
        )
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {file_path}: range {start_id}-{end_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    print("🔄 Keyword Range Updater")
    print("=" * 40)
    
    # Get user input
    try:
        start_id = int(input("Enter start ID (e.g., 1): "))
        end_id = int(input("Enter end ID (e.g., 100): "))
    except ValueError:
        print("❌ Please enter valid numbers")
        return
    
    if start_id > end_id:
        print("❌ Start ID cannot be greater than end ID")
        return
    
    # List of scraper files to update
    scraper_files = [
        'nykaa.py',
        'myntra.py', 
        'zara.py'
    ]
    
    print(f"\n📝 Updating ranges to {start_id}-{end_id} in:")
    
    success_count = 0
    for file_path in scraper_files:
        if os.path.exists(file_path):
            if update_ranges_in_file(file_path, start_id, end_id):
                success_count += 1
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print(f"\n✅ Successfully updated {success_count}/{len(scraper_files)} files")
    print(f"🎯 All scrapers will now process keywords with IDs {start_id} to {end_id}")

if __name__ == "__main__":
    main()
