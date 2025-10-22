#!/usr/bin/env python3
"""
Script to merge multiple JSON files and remove duplicate entries.

This script:
1. Reads multiple JSON files containing product data
2. Merges all data into a single list
3. Removes duplicates based on product_url, product_id, and product_name
4. Saves the merged data to a new JSON file
5. Provides statistics about the merge process

Usage:
    # Method 1: Specify files directly in command line
    python merge_json_files.py file1.json file2.json file3.json -o merged_data.json
    
    # Method 2: Use pattern matching
    python merge_json_files.py -p "*_scraped_data.json" -o merged_data.json
    
    # Method 3: Edit the FILES_TO_MERGE list below and run without arguments
    python merge_json_files.py -o merged_data.json
"""

import json
import os
import sys
from typing import List, Dict, Any, Set
from pathlib import Path

# =============================================================================
# CONFIGURATION: Edit this list to specify which files to merge by default
# =============================================================================
FILES_TO_MERGE = [
    # Add your JSON files here, for example:
    # "myntra_scraped_data.json",
    # "nykaa_scraped_data.json", 
    # "zara_scraped_data.json",
    "scraped_data.json",
    "scraped_data_2.json",
    "scraped_data_3.json",
    "scraped_data_4.json",
]

OUTPUT_FILE = "merged_data.json"  # Default output file name


def load_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Load JSON data from a file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        List of dictionaries containing the JSON data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not isinstance(data, list):
                print(f"Warning: {file_path} doesn't contain a JSON array. Skipping...")
                return []
            return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}")
        return []


def create_duplicate_key(item: Dict[str, Any]) -> str:
    """
    Create a unique key for duplicate detection.
    
    Args:
        item: Product dictionary
        
    Returns:
        String key for duplicate detection
    """
    # Use product_url as primary identifier, fallback to product_id + product_name
    product_url = item.get('product_url', '').strip()
    product_id = item.get('product_id', '').strip()
    product_name = item.get('product_name', '').strip()
    
    if product_url and product_url != 'Not found':
        return f"url:{product_url}"
    elif product_id and product_id != 'Not found':
        return f"id:{product_id}:{product_name}"
    else:
        return f"name:{product_name}"


def merge_json_files(input_files: List[str], output_file: str, verbose: bool = True) -> Dict[str, int]:
    """
    Merge multiple JSON files and remove duplicates.
    
    Args:
        input_files: List of input JSON file paths
        output_file: Path for the output merged JSON file
        verbose: Whether to print detailed progress information
        
    Returns:
        Dictionary with merge statistics
    """
    all_data = []
    seen_keys: Set[str] = set()
    duplicates_removed = 0
    files_processed = 0
    
    if verbose:
        print(f"Starting merge process...")
        print(f"Input files: {len(input_files)}")
        print(f"Output file: {output_file}")
        print("-" * 50)
    
    # Process each input file
    for file_path in input_files:
        if not os.path.exists(file_path):
            if verbose:
                print(f"Warning: File {file_path} does not exist. Skipping...")
            continue
            
        if verbose:
            print(f"Processing: {file_path}")
            
        data = load_json_file(file_path)
        if not data:
            if verbose:
                print(f"  No data loaded from {file_path}")
            continue
            
        files_processed += 1
        file_duplicates = 0
        
        # Process each item in the file
        for item in data:
            duplicate_key = create_duplicate_key(item)
            
            if duplicate_key in seen_keys:
                duplicates_removed += 1
                file_duplicates += 1
                if verbose:
                    print(f"  Duplicate found: {item.get('product_name', 'Unknown')[:50]}...")
            else:
                seen_keys.add(duplicate_key)
                all_data.append(item)
        
        if verbose:
            print(f"  Loaded: {len(data)} items, Duplicates removed: {file_duplicates}")
    
    # Save merged data
    if verbose:
        print("-" * 50)
        print(f"Saving merged data to {output_file}...")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(all_data, file, indent=2, ensure_ascii=False)
        
        if verbose:
            print(f"Successfully saved {len(all_data)} unique items to {output_file}")
            
    except Exception as e:
        print(f"Error saving merged data: {e}")
        return {}
    
    # Return statistics
    stats = {
        'total_items_processed': sum(len(load_json_file(f)) for f in input_files if os.path.exists(f)),
        'unique_items': len(all_data),
        'duplicates_removed': duplicates_removed,
        'files_processed': files_processed,
        'output_file': output_file
    }
    
    return stats


def main():
    """Main function to handle command line arguments and execute merge."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Merge multiple JSON files and remove duplicates',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge specific files (recommended)
  python merge_json_files.py file1.json file2.json file3.json -o merged_data.json

  # Merge with custom pattern
  python merge_json_files.py -p "*_scraped_data.json" -o merged_data.json

  # Quiet mode (no verbose output)
  python merge_json_files.py file1.json file2.json -o merged_data.json -q

  # Merge specific files from your project
  python merge_json_files.py myntra_scraped_data.json nykaa_scraped_data.json zara_scraped_data.json -o merged_data.json
        """
    )
    
    parser.add_argument('files', nargs='*', help='Specific JSON files to merge')
    parser.add_argument('-o', '--output', default=OUTPUT_FILE, help=f'Output JSON file path (default: {OUTPUT_FILE})')
    parser.add_argument('-p', '--pattern', help='Glob pattern to find JSON files (e.g., "*_scraped_data.json")')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode (no verbose output)')
    
    args = parser.parse_args()
    
    # Determine input files
    input_files = []
    
    if args.files:
        # Use specific files provided as arguments
        input_files = args.files
    elif args.pattern:
        # Use glob pattern
        import glob
        input_files = glob.glob(args.pattern)
        if not input_files:
            print(f"No files found matching pattern: {args.pattern}")
            sys.exit(1)
    elif FILES_TO_MERGE:
        # Use files from configuration
        input_files = FILES_TO_MERGE
        if not args.quiet:
            print("Using files from configuration list:")
    else:
        # No files specified - show help
        print("Error: You must specify which JSON files to merge.")
        print("Use one of these options:")
        print("1. Specify files directly: python merge_json_files.py file1.json file2.json -o output.json")
        print("2. Use a pattern: python merge_json_files.py -p 'pattern*.json' -o output.json")
        print("3. Edit the FILES_TO_MERGE list in the script and run: python merge_json_files.py -o output.json")
        print("\nUse -h for more help.")
        sys.exit(1)
    
    # Validate input files
    valid_files = [f for f in input_files if os.path.exists(f)]
    if not valid_files:
        print("No valid input files found")
        print("Available JSON files in current directory:")
        import glob
        available_files = glob.glob("*.json")
        for f in available_files:
            print(f"  - {f}")
        sys.exit(1)
    
    # Show which files will be processed
    if not args.quiet:
        print("Files to be merged:")
        for f in valid_files:
            print(f"  - {f}")
        print()
    
    # Perform merge
    stats = merge_json_files(valid_files, args.output, verbose=not args.quiet)
    
    if stats:
        print("\n" + "="*50)
        print("MERGE STATISTICS")
        print("="*50)
        print(f"Files processed: {stats['files_processed']}")
        print(f"Total items processed: {stats['total_items_processed']}")
        print(f"Unique items in output: {stats['unique_items']}")
        print(f"Duplicates removed: {stats['duplicates_removed']}")
        print(f"Output file: {stats['output_file']}")
        
        if stats['total_items_processed'] > 0:
            duplicate_percentage = (stats['duplicates_removed'] / stats['total_items_processed']) * 100
            print(f"Duplicate percentage: {duplicate_percentage:.2f}%")
        
        print("="*50)


if __name__ == "__main__":
    main()
