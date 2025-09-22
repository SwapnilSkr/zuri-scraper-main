# Unified Scraper System

This system runs three e-commerce scrapers (Nykaa, Zara, and Myntra) in parallel and combines all results into a single unified JSON file.

## Features

- **Unified JSON Structure**: All scrapers output data in the same format
- **Parallel Execution**: All three scrapers run simultaneously for faster results
- **Automatic Data Combination**: Results are automatically merged into `scraped_data.json`
- **Error Handling**: Robust error handling and timeout management
- **Progress Tracking**: Real-time progress updates for each scraper

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

## Usage

### Option 1: Run All Scrapers in Parallel (Recommended)
```bash
python run_scrapers.py
```

### Option 2: Run Parallel Scraper Directly
```bash
python parallel_scraper.py
```

### Option 3: Run Individual Scrapers
```bash
python nykaa.py
python zara.py
python myntra.py
```

## Output Files

- **`scraped_data.json`**: Combined results from all scrapers (main output)
- **`nykaa_scraped_data.json`**: Individual Nykaa results (temporary)
- **`zara_scraped_data.json`**: Individual Zara results (temporary)
- **`myntra_scraped_data.json`**: Individual Myntra results (temporary)

## How It Works

1. **Parallel Execution**: The system starts all three scrapers simultaneously
2. **Individual Processing**: Each scraper processes keywords and saves to its own file
3. **Data Combination**: After all scrapers complete, results are merged into `scraped_data.json`
4. **Cleanup**: Option to remove individual scraper files after combination

## Field Mapping

| Field | Nykaa | Zara | Myntra | Notes |
|-------|-------|------|--------|-------|
| `brand_name` | ✅ | ❌ | ✅ | "Not applicable" for Zara |
| `product_rating` | ✅ | ❌ | ✅ | "Not applicable" for Zara |
| `product_rating_count` | ✅ | ❌ | ✅ | "Not applicable" for Zara |
| `product_color` | ❌ | ✅ | ❌ | "Not applicable" for others |
| `product_sizes_coming_soon` | ❌ | ✅ | ❌ | "Not applicable" for others |
| `product_sizes_out_of_stock` | ❌ | ✅ | ❌ | "Not applicable" for others |
| `additional_information` | ❌ | ✅ | ❌ | "Not applicable" for others |

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

## Customization

### Adding New Scrapers

1. Create a new scraper file following the unified structure
2. Add it to the `scrapers` list in `parallel_scraper.py`
3. Update the `combine_scraped_data()` function

### Modifying Data Structure

1. Update the product data structure in all scrapers
2. Ensure all scrapers use the same field names
3. Update this README with the new structure

## Support

For issues or questions:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure `keywords.json` is properly formatted
4. Check network connectivity for the target websites
