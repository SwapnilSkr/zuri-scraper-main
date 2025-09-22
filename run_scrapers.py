#!/usr/bin/env python3
"""
Simple script to run the parallel scraper system
"""

import subprocess
import sys

def main():
    print("🚀 Starting Parallel Scraper System...")
    print("This will run Nykaa, Zara, and Myntra scrapers simultaneously")
    print("=" * 60)
    
    try:
        # Run the parallel scraper
        result = subprocess.run([sys.executable, "parallel_scraper.py"], check=True)
        print("\n✅ All scrapers completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Scrapers failed with error code: {e.returncode}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Scraping interrupted by user")
        print("💾 Individual scrapers should have saved their data automatically")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
