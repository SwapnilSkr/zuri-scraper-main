#!/usr/bin/env python3
"""
Excel to JSON Converter
Converts keywords.xlsx to keywords.json with proper structure
"""

import pandas as pd
import json
import sys

def convert_excel_to_json():
    try:
        print("Reading keywords.xlsx...")
        df = pd.read_excel('keywords.xlsx')
        
        print(f"Columns found: {list(df.columns)}")
        print(f"Total rows: {len(df)}")
        
        required_columns = ['Keyword', 'Category', 'Subcategory']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            print("Available columns:", list(df.columns))
            return False
        
        df_clean = df.dropna(subset=required_columns)
        print(f"Rows after cleaning: {len(df_clean)}")
        
        
        keywords_data = []
        
        for index, row in df_clean.iterrows():
            keyword_data = {
                "id": str(index + 1), 
                "keyword": str(row['Keyword']).strip(),
                "category": str(row['Category']).strip(),
                "subcategory": str(row['Subcategory']).strip()
            }
            keywords_data.append(keyword_data)
        
        
        print(f"Converting {len(keywords_data)} keywords to JSON...")
        with open('keywords.json', 'w', encoding='utf-8') as f:
            json.dump(keywords_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Successfully converted keywords.xlsx to keywords.json")
        print(f"📊 Summary:")
        print(f"   - Total keywords: {len(keywords_data)}")
        print(f"   - Categories: {len(set(item['category'] for item in keywords_data))}")
        print(f"   - Subcategories: {len(set(item['subcategory'] for item in keywords_data))}")
        
        
        print("\n📋 Preview of first 3 entries:")
        for i, item in enumerate(keywords_data[:3]):
            print(f"   {i+1}. ID: {item['id']}, Keyword: '{item['keyword']}', Category: '{item['category']}', Subcategory: '{item['subcategory']}'")
        
        return True
        
    except FileNotFoundError:
        print("❌ Error: keywords.xlsx file not found in current directory")
        return False
    except Exception as e:
        print(f"❌ Error converting Excel to JSON: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Starting Excel to JSON conversion...")
    success = convert_excel_to_json()
    
    if success:
        print("\n✅ Conversion completed successfully!")
    else:
        print("\n❌ Conversion failed!")
        sys.exit(1)
