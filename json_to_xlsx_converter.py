#!/usr/bin/env python3
"""
JSON to XLSX Converter Script

This script converts the merged_data.json file to an Excel (.xlsx) format.
It handles array fields by converting them to comma-separated strings.
"""

import json
import pandas as pd
import sys
import os
from typing import List, Dict, Any


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load JSON data from file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        List[Dict[str, Any]]: List of product dictionaries
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"Successfully loaded {len(data)} records from {file_path}")
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{file_path}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading file '{file_path}': {e}")
        sys.exit(1)


def process_array_fields(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process array fields by converting them to comma-separated strings.
    
    Args:
        record (Dict[str, Any]): Product record dictionary
        
    Returns:
        Dict[str, Any]: Processed record with array fields converted to strings
    """
    processed_record = record.copy()
    
    array_fields = [
        'product_sizes_available',
        'product_sizes_coming_soon', 
        'product_sizes_out_of_stock',
        'product_image_urls'
    ]
    
    for field in array_fields:
        if field in processed_record and isinstance(processed_record[field], list):
            processed_record[field] = ', '.join(str(item) for item in processed_record[field])
        elif field not in processed_record:
            processed_record[field] = ''
    
    return processed_record


def convert_json_to_xlsx(json_file_path: str, output_file_path: str = None) -> None:
    """
    Convert JSON data to XLSX format.
    
    Args:
        json_file_path (str): Path to input JSON file
        output_file_path (str): Path to output XLSX file (optional)
    """
    data = load_json_data(json_file_path)
    
    if not data:
        print("No data found in the JSON file.")
        return
    
    processed_data = []
    for record in data:
        processed_record = process_array_fields(record)
        processed_data.append(processed_record)
    
    df = pd.DataFrame(processed_data)
    
    column_order = [
        'site',
        'keyword_id', 
        'keyword',
        'product_id',
        'brand_name',
        'product_name',
        'product_rating',
        'product_rating_count',
        'current_product_price',
        'original_product_price',
        'product_color',
        'product_description',
        'product_sizes_available',
        'product_sizes_coming_soon',
        'product_sizes_out_of_stock',
        'product_image_urls',
        'product_url',
        'additional_information'
    ]
    
    existing_columns = [col for col in column_order if col in df.columns]
    df = df[existing_columns + [col for col in df.columns if col not in existing_columns]]
    
    if output_file_path is None:
        base_name = os.path.splitext(os.path.basename(json_file_path))[0]
        output_file_path = f"{base_name}.xlsx"
    
    try:
        with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Products', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Products']
            
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
        
        print(f"Successfully converted {len(data)} records to '{output_file_path}'")
        print(f"Output file size: {os.path.getsize(output_file_path) / (1024*1024):.2f} MB")
        
    except Exception as e:
        print(f"Error writing to Excel file '{output_file_path}': {e}")
        sys.exit(1)


def main():
    """Main function to handle command line arguments and execute conversion."""
    if len(sys.argv) < 2:
        print("Usage: python json_to_xlsx_converter.py <input_json_file> [output_xlsx_file]")
        print("Example: python json_to_xlsx_converter.py merged_data.json")
        print("Example: python json_to_xlsx_converter.py merged_data.json output.xlsx")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    
    print(f"Converting '{input_file}' to Excel format...")
    convert_json_to_xlsx(input_file, output_file)
    print("Conversion completed successfully!")


if __name__ == "__main__":
    main()
