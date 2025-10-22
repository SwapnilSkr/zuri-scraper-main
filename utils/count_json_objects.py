#!/usr/bin/env python3
"""
JSON Object Counter Script

This script counts the number of objects in a JSON array with validation
to ensure the JSON has an array of objects format.
"""

import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Any, Union

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas is not available. Excel export will be skipped.")


def validate_json_array_format(data: Any) -> tuple[bool, str]:
    """
    Validate that the JSON data is an array of objects.
    
    Args:
        data: Parsed JSON data
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not isinstance(data, list):
        return False, "JSON data is not an array. Expected a list/array format."
    
    if len(data) == 0:
        return True, "JSON array is empty (0 objects)."
    
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            return False, f"Element at index {i} is not an object. Expected all elements to be objects (dictionaries)."
    
    return True, "JSON format is valid - array of objects."


def count_json_objects(file_path: str) -> int:
    """
    Count the number of objects in a JSON array file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        int: Number of objects in the JSON array
        
    Raises:
        SystemExit: If file doesn't exist, JSON is invalid, or format is incorrect
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"Successfully loaded JSON from '{file_path}'")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{file_path}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading file '{file_path}': {e}")
        sys.exit(1)
    
    is_valid, message = validate_json_array_format(data)
    print(f"Validation: {message}")
    
    if not is_valid:
        print(f"Error: {message}")
        sys.exit(1)
    
    object_count = len(data)
    print(f"Number of objects in JSON array: {object_count}")
    
    return object_count


def create_keyword_analysis_json(data: List[Dict[str, Any]], source_file_path: str) -> None:
    """
    Create a JSON file with keyword analysis showing how many products each keyword has.
    
    Args:
        data: List of product objects
        source_file_path: Path to the source JSON file for reference
    """
    try:
        keyword_counts = {}
        for obj in data:
            if isinstance(obj, dict) and 'keyword' in obj:
                keyword = obj['keyword']
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        analysis_data = {
            "source_file": source_file_path,
            "analysis_timestamp": datetime.now().isoformat(),
            "total_products": len(data),
            "unique_keywords": len(keyword_counts),
            "keyword_analysis": []
        }
        
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        
        for keyword, count in sorted_keywords:
            analysis_data["keyword_analysis"].append({
                "keyword": keyword,
                "product_count": count,
                "percentage": round((count / len(data)) * 100, 2)
            })
        
        json_dir = "json"
        xlsx_dir = "xlsx"
        for directory in [json_dir, xlsx_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        json_output_file = os.path.join(json_dir, "keyword_details.json")
        xlsx_output_file = os.path.join(xlsx_dir, "keyword_details.xlsx")
        
        for file_path in [json_output_file, xlsx_output_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        with open(json_output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        print(f"Keyword analysis saved to:")
        print(f"  JSON: {json_output_file}")
        
        if PANDAS_AVAILABLE:
            try:
                df_keywords = pd.DataFrame(analysis_data["keyword_analysis"])
                
                summary_data = {
                    "Metric": [
                        "Source File",
                        "Analysis Timestamp", 
                        "Total Products",
                        "Unique Keywords",
                        "Most Popular Keyword",
                        "Products for Most Popular Keyword"
                    ],
                    "Value": [
                        analysis_data["source_file"],
                        analysis_data["analysis_timestamp"],
                        analysis_data["total_products"],
                        analysis_data["unique_keywords"],
                        sorted_keywords[0][0] if sorted_keywords else "N/A",
                        sorted_keywords[0][1] if sorted_keywords else 0
                    ]
                }
                df_summary = pd.DataFrame(summary_data)
                
                with pd.ExcelWriter(xlsx_output_file, engine='openpyxl') as writer:
                    df_keywords.to_excel(writer, sheet_name='Keyword Analysis', index=False)
                    
                    df_summary.to_excel(writer, sheet_name='Summary', index=False)
                    
                    for sheet_name in writer.sheets:
                        worksheet = writer.sheets[sheet_name]
                        for column in worksheet.columns:
                            max_length = 0
                            column_letter = column[0].column_letter
                            
                            for cell in column:
                                try:
                                    if len(str(cell.value)) > max_length:
                                        max_length = len(str(cell.value))
                                except:
                                    pass
                            
                            adjusted_width = min(max_length + 2, 50)
                            worksheet.column_dimensions[column_letter].width = adjusted_width
                
                print(f"  Excel: {xlsx_output_file}")
                
            except Exception as e:
                print(f"  Warning: Could not create Excel file: {e}")
        else:
            print(f"  Excel: Skipped (pandas not available)")
        
        print(f"Top 5 keywords by product count:")
        for i, (keyword, count) in enumerate(sorted_keywords[:5]):
            print(f"  {i+1}. '{keyword}': {count} products")
        
    except Exception as e:
        print(f"Error creating keyword analysis JSON: {e}")


def get_detailed_statistics(file_path: str) -> None:
    """
    Get detailed statistics about the JSON array.
    
    Args:
        file_path (str): Path to the JSON file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if not isinstance(data, list):
            print("Cannot provide detailed statistics - data is not an array.")
            return
        
        if len(data) == 0:
            print("Array is empty - no statistics available.")
            return
        
        print(f"\n=== Detailed Statistics ===")
        print(f"Total objects: {len(data)}")
        
        if len(data) > 0:
            first_object_keys = set(data[0].keys()) if isinstance(data[0], dict) else set()
            all_keys = set()
            
            for obj in data:
                if isinstance(obj, dict):
                    all_keys.update(obj.keys())
            
            print(f"Unique keys across all objects: {len(all_keys)}")
            print(f"Keys in first object: {len(first_object_keys)}")
            
            if len(data) > 1:
                consistent_keys = all(
                    set(obj.keys()) == first_object_keys 
                    for obj in data[1:] 
                    if isinstance(obj, dict)
                )
                print(f"All objects have consistent keys: {consistent_keys}")
            
            if all_keys:
                print(f"Sample keys: {list(all_keys)[:10]}{'...' if len(all_keys) > 10 else ''}")
        
        keywords = []
        for obj in data:
            if isinstance(obj, dict) and 'keyword' in obj:
                keywords.append(obj['keyword'])
        
        unique_keywords = list(set(keywords))
        print(f"Unique keywords: {len(unique_keywords)}")
        if unique_keywords:
            print(f"Sample keywords: {unique_keywords[:10]}{'...' if len(unique_keywords) > 10 else ''}")
        
        create_keyword_analysis_json(data, file_path)
        
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")
        
    except Exception as e:
        print(f"Error getting detailed statistics: {e}")


def main():
    """Main function to handle command line arguments and execute counting."""
    if len(sys.argv) < 2:
        print("Usage: python count_json_objects.py <json_file> [--detailed]")
        print("Example: python count_json_objects.py merged_data.json")
        print("Example: python count_json_objects.py merged_data.json --detailed")
        print("\nOptions:")
        print("  --detailed    Show detailed statistics about the JSON array")
        sys.exit(1)
    
    json_file = sys.argv[1]
    show_detailed = "--detailed" in sys.argv
    
    print(f"Analyzing JSON file: {json_file}")
    print("=" * 50)
    
    object_count = count_json_objects(json_file)
    
    if show_detailed:
        get_detailed_statistics(json_file)
    
    print("=" * 50)
    print(f"Analysis complete. Found {object_count} objects in the JSON array.")


if __name__ == "__main__":
    main()
