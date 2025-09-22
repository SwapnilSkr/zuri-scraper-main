"""
Utility functions for the web scraping project
"""

import requests
import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any
import random

def create_output_directory(directory_name: str = "scraped_data") -> str:
    """Create output directory if it doesn't exist"""
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Created output directory: {directory_name}")
    return directory_name

def save_as_json(data: List[Dict[str, Any]], filename: str, directory: str = "scraped_data") -> str:
    """Save data as JSON file"""
    create_output_directory(directory)
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Data saved to JSON: {filepath}")
    return filepath

def save_as_csv(data: List[Dict[str, Any]], filename: str, directory: str = "scraped_data") -> str:
    """Save data as CSV file"""
    if not data:
        print("No data to save")
        return ""
    
    create_output_directory(directory)
    filepath = os.path.join(directory, filename.replace('.json', '.csv'))
    
    # Get fieldnames from first item
    fieldnames = list(data[0].keys())
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Data saved to CSV: {filepath}")
    return filepath

def save_as_xml(data: List[Dict[str, Any]], filename: str, directory: str = "scraped_data") -> str:
    """Save data as XML file"""
    if not data:
        print("No data to save")
        return ""
    
    create_output_directory(directory)
    filepath = os.path.join(directory, filename.replace('.json', '.xml'))
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += f'<data scraped_at="{datetime.now().isoformat()}">\n'
    
    for item in data:
        xml_content += '  <item>\n'
        for key, value in item.items():
            if isinstance(value, list):
                xml_content += f'    <{key}>\n'
                for sub_item in value:
                    xml_content += f'      <subitem>{sub_item}</subitem>\n'
                xml_content += f'    </{key}>\n'
            else:
                xml_content += f'    <{key}>{value}</{key}>\n'
        xml_content += '  </item>\n'
    
    xml_content += '</data>'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"Data saved to XML: {filepath}")
    return filepath

def export_data(data: List[Dict[str, Any]], filename: str, formats: List[str] = None, directory: str = "scraped_data") -> Dict[str, str]:
    """Export data in multiple formats"""
    if formats is None:
        formats = ["json", "csv", "xml"]
    
    exported_files = {}
    
    for format_type in formats:
        try:
            if format_type.lower() == "json":
                exported_files["json"] = save_as_json(data, filename, directory)
            elif format_type.lower() == "csv":
                exported_files["csv"] = save_as_csv(data, filename, directory)
            elif format_type.lower() == "xml":
                exported_files["xml"] = save_as_xml(data, filename, directory)
        except Exception as e:
            print(f"Error saving as {format_type}: {e}")
    
    return exported_files

def load_data(filepath: str) -> List[Dict[str, Any]]:
    """Load data from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data from {filepath}: {e}")
        return []

def print_data_summary(data: List[Dict[str, Any]], title: str = "Data Summary") -> None:
    """Print a summary of the scraped data"""
    if not data:
        print(f"{title}: No data available")
        return
    
    print(f"\n{title}")
    print("=" * 50)
    print(f"Total items: {len(data)}")
    
    if data:
        # Show sample of first item
        print(f"Sample item structure:")
        for key, value in list(data[0].items())[:3]:  # Show first 3 keys
            print(f"  {key}: {value}")
        
        if len(data[0]) > 3:
            print(f"  ... and {len(data[0]) - 3} more fields")
    
    print()

def filter_data(data: List[Dict[str, Any]], **filters) -> List[Dict[str, Any]]:
    """Filter data based on key-value pairs"""
    filtered_data = []
    
    for item in data:
        match = True
        for key, value in filters.items():
            if key not in item or item[key] != value:
                match = False
                break
        
        if match:
            filtered_data.append(item)
    
    return filtered_data

def sort_data(data: List[Dict[str, Any]], key: str, reverse: bool = False) -> List[Dict[str, Any]]:
    """Sort data by a specific key"""
    try:
        return sorted(data, key=lambda x: x.get(key, ""), reverse=reverse)
    except Exception as e:
        print(f"Error sorting data: {e}")
        return data

def get_unique_values(data: List[Dict[str, Any]], key: str) -> List[Any]:
    """Get unique values for a specific key"""
    unique_values = set()
    
    for item in data:
        if key in item:
            unique_values.add(item[key])
    
    return list(unique_values)

def count_by_field(data: List[Dict[str, Any]], key: str) -> Dict[str, int]:
    """Count occurrences by field value"""
    counts = {}
    
    for item in data:
        if key in item:
            value = item[key]
            counts[value] = counts.get(value, 0) + 1
    
    return counts

def get_random_headers():
    """Get random headers"""
    response = requests.get(
    url='https://headers.scrapeops.io/v1/browser-headers',
    params={
      'api_key': '421c1b6c-c329-4935-8536-733a209e04f1',
      'num_results': '10'}
    )
    fake_headers = response.json().get('result', [])
    return random.choice(fake_headers)
    