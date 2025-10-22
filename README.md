# E-commerce Web Scraping System

A comprehensive web scraping system for multiple e-commerce platforms including Nykaa, Zara, Myntra, H&M, and Ajio. The system supports both individual and parallel scraping with advanced data processing utilities.

## Features

- **Multi-Platform Support**: Scrapers for 5 major e-commerce sites
- **Unified JSON Structure**: All scrapers output data in the same format
- **Parallel Execution**: Multiple scrapers run simultaneously for faster results
- **Advanced Data Processing**: Utilities for data conversion, merging, and analysis
- **Error Handling**: Robust error handling and timeout management
- **Progress Tracking**: Real-time progress updates for each scraper
- **Data Management**: Tools for Excel conversion, JSON merging, and statistics

## Unified Data Structure

All scrapers output products with this unified structure:

```json
{
  "site": "nykaa_fashion|zara|myntra",
  "product_url": "https://...",
  "keyword_id": "1",
  "keyword": "white tops",
  "product_id": "12345",
  "brand_name": "Brand Name",
  "product_name": "Product Name",
  "product_rating": "4.5",
  "product_rating_count": "150",
  "current_product_price": "₹1,500",
  "original_product_price": "₹2,000",
  "product_color": "White",
  "product_description": "Product description...",
  "product_sizes_available": ["S", "M", "L"],
  "product_sizes_coming_soon": [],
  "product_sizes_out_of_stock": [],
  "product_image_urls": ["https://..."],
  "additional_information": "Additional details..."
}
```

## Setup

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Keywords**:
   Edit `keywords.json` with your search terms:
   ```json
   [
     {
       "id": "1",
       "keyword": "white tops"
     },
     {
       "id": "2",
       "keyword": "black jeans"
     }
   ]
   ```

## Project Structure

### Core Scrapers

- **`nykaa.py`** - Nykaa Fashion scraper
- **`zara.py`** - Zara.com scraper
- **`myntra.py`** - Myntra.com scraper
- **`hm.py`** - H&M.com scraper
- **`ajio.py`** - Ajio.com scraper

### Management Scripts

- **`run_scrapers.py`** - Main entry point to run all scrapers
- **`parallel_scraper.py`** - Parallel execution engine
- **`stop_scrapers.py`** - Gracefully stop running scrapers
- **`update_ranges.py`** - Update keyword ID ranges in scrapers

### Utility Scripts

- **`scraper.py`** - Advanced web scraping framework
- **`simple_scraper.py`** - Basic scraping example
- **`test_browser.py`** - Browser functionality test
- **`utils.py`** - Common utility functions
- **`config.py`** - Configuration settings

### Data Processing Utilities (`utils/` folder)

- **`convert_excel_to_json.py`** - Convert Excel keywords to JSON format
- **`count_json_objects.py`** - Count and analyze JSON data with statistics
- **`json_to_xlsx_converter.py`** - Convert JSON data to Excel format
- **`merge_json_files.py`** - Merge multiple JSON files and remove duplicates

## Usage

### Quick Start (Recommended)

```bash
# Run all scrapers in parallel
python run_scrapers.py

# Or run parallel scraper directly
python parallel_scraper.py
```

### Individual Scrapers

```bash
# Run individual scrapers
python nykaa.py
python zara.py
python myntra.py
python hm.py
python ajio.py
```

### Data Processing

```bash
# Convert Excel to JSON
python utils/convert_excel_to_json.py

# Count JSON objects with detailed statistics
python utils/count_json_objects.py scraped_data.json --detailed

# Convert JSON to Excel
python utils/json_to_xlsx_converter.py scraped_data.json

# Merge multiple JSON files
python utils/merge_json_files.py file1.json file2.json -o merged_data.json
```

### Management

```bash
# Stop running scrapers gracefully
python stop_scrapers.py

# Update keyword ranges in all scrapers
python update_ranges.py

# Test browser functionality
python test_browser.py
```

## Output Files

### Main Output Files

- **`scraped_data.json`**: Combined results from all scrapers (main output)
- **`merged_data.json`**: Merged data from multiple JSON files

### Individual Scraper Outputs (Temporary)

- **`nykaa_scraped_data.json`**: Individual Nykaa results
- **`zara_scraped_data.json`**: Individual Zara results
- **`myntra_scraped_data.json`**: Individual Myntra results
- **`hm_scraped_data.json`**: Individual H&M results
- **`ajio_scraped_data.json`**: Individual Ajio results

### Data Analysis Files

- **`keyword_details.json`**: Keyword analysis with statistics
- **`keyword_details.xlsx`**: Excel version of keyword analysis
- **`merged_data.xlsx`**: Excel version of merged data

## How It Works

### Parallel Scraping Process

1. **Parallel Execution**: The system starts multiple scrapers simultaneously
2. **Individual Processing**: Each scraper processes keywords and saves to its own file
3. **Data Combination**: After all scrapers complete, results are merged into `scraped_data.json`
4. **Cleanup**: Option to remove individual scraper files after combination

### Data Processing Workflow

1. **Excel to JSON**: Convert keyword Excel files to JSON format
2. **Scraping**: Run individual or parallel scrapers
3. **Data Analysis**: Generate statistics and keyword analysis
4. **Data Merging**: Combine multiple JSON files and remove duplicates
5. **Format Conversion**: Convert final data to Excel format

## Field Mapping

| Field                        | Nykaa | Zara | Myntra | H&M | Ajio | Notes                             |
| ---------------------------- | ----- | ---- | ------ | --- | ---- | --------------------------------- |
| `brand_name`                 | ✅    | ❌   | ✅     | ✅  | ✅   | "Not applicable" for Zara         |
| `product_rating`             | ✅    | ❌   | ✅     | ✅  | ✅   | "Not applicable" for Zara         |
| `product_rating_count`       | ✅    | ❌   | ✅     | ✅  | ✅   | "Not applicable" for Zara         |
| `product_color`              | ❌    | ✅   | ❌     | ✅  | ✅   | "Not applicable" for Nykaa/Myntra |
| `product_sizes_coming_soon`  | ❌    | ✅   | ❌     | ✅  | ❌   | "Not applicable" for others       |
| `product_sizes_out_of_stock` | ❌    | ✅   | ❌     | ✅  | ❌   | "Not applicable" for others       |
| `additional_information`     | ❌    | ✅   | ❌     | ✅  | ✅   | "Not applicable" for Nykaa/Myntra |

## Error Handling

- **Timeout Protection**: Each scraper has a 30-minute timeout
- **Graceful Failures**: If one scraper fails, others continue
- **Error Reporting**: Detailed error messages for debugging
- **Partial Results**: System combines data from successful scrapers only

## Performance

- **Parallel Execution**: ~3x faster than sequential execution
- **Resource Management**: Each scraper runs in its own process
- **Memory Efficient**: Results are written to disk immediately

## Troubleshooting

### Common Issues

1. **Missing keywords.json**: Ensure the file exists with proper JSON format
2. **Chrome Driver Issues**: The system automatically downloads ChromeDriver
3. **Network Timeouts**: Increase timeout values in `parallel_scraper.py` if needed
4. **Memory Issues**: Close other applications if running low on memory

### Debug Mode

To run individual scrapers for debugging:

```bash
python nykaa.py    # Test Nykaa scraper
python zara.py     # Test Zara scraper
python myntra.py   # Test Myntra scraper
```

## Advanced Usage

### Data Processing Pipeline

1. **Prepare Keywords**: Convert Excel to JSON format

   ```bash
   python utils/convert_excel_to_json.py
   ```

2. **Run Scrapers**: Execute individual or parallel scraping

   ```bash
   python run_scrapers.py
   ```

3. **Analyze Data**: Generate detailed statistics

   ```bash
   python utils/count_json_objects.py scraped_data.json --detailed
   ```

4. **Merge Data**: Combine multiple JSON files

   ```bash
   python utils/merge_json_files.py file1.json file2.json -o merged_data.json
   ```

5. **Convert to Excel**: Create Excel reports
   ```bash
   python utils/json_to_xlsx_converter.py merged_data.json
   ```

### Utility Scripts Details

#### `utils/convert_excel_to_json.py`

- Converts Excel keyword files to JSON format
- Handles multiple columns (Keyword, Category, Subcategory)
- Validates data and provides statistics

#### `utils/count_json_objects.py`

- Counts objects in JSON arrays
- Generates detailed statistics and keyword analysis
- Creates Excel reports with keyword breakdowns
- Usage: `python utils/count_json_objects.py file.json [--detailed]`

#### `utils/json_to_xlsx_converter.py`

- Converts JSON data to Excel format
- Handles array fields by converting to comma-separated strings
- Auto-adjusts column widths for better readability

#### `utils/merge_json_files.py`

- Merges multiple JSON files
- Removes duplicates based on product URL, ID, and name
- Provides detailed merge statistics
- Usage: `python utils/merge_json_files.py file1.json file2.json -o output.json`

## Customization

### Adding New Scrapers

1. Create a new scraper file following the unified structure
2. Add it to the `scrapers` list in `parallel_scraper.py`
3. Update the `combine_scraped_data()` function

### Modifying Data Structure

1. Update the product data structure in all scrapers
2. Ensure all scrapers use the same field names
3. Update this README with the new structure

### Configuration

Edit `config.py` to modify:

- Browser settings (headless mode, window size, user agent)
- Scraping parameters (timeouts, delays, retries)
- Output settings (directory, format, encoding)
- Logging configuration

## Support

For issues or questions:

1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure `keywords.json` is properly formatted
4. Check network connectivity for the target websites
