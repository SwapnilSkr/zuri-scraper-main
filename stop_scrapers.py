#!/usr/bin/env python3
"""
Stop Scrapers Script
Sends interrupt signal to running scrapers to gracefully shut them down
"""

import os
import signal
import subprocess
import sys

def find_scraper_processes():
    """Find running scraper processes"""
    try:
        result = subprocess.run(
            ['ps', 'aux'], 
            capture_output=True, 
            text=True
        )
        
        processes = []
        for line in result.stdout.split('\n'):
            if any(scraper in line for scraper in ['nykaa.py', 'myntra.py', 'zara.py', 'parallel_scraper.py']):
                parts = line.split()
                if len(parts) > 1:
                    pid = parts[1]
                    processes.append({
                        'pid': int(pid),
                        'command': ' '.join(parts[10:])
                    })
        
        return processes
    except Exception as e:
        print(f"Error finding processes: {e}")
        return []

def stop_scrapers():
    """Stop all running scrapers gracefully"""
    print("🔍 Looking for running scrapers...")
    
    processes = find_scraper_processes()
    
    if not processes:
        print("✅ No scrapers currently running")
        return
    
    print(f"📋 Found {len(processes)} running scraper(s):")
    for proc in processes:
        print(f"   PID {proc['pid']}: {proc['command'][:80]}...")
    
    print("\n🛑 Sending interrupt signal to stop scrapers gracefully...")
    print("💾 This will save all collected data before shutting down")
    
    stopped_count = 0
    for proc in processes:
        try:
            os.kill(proc['pid'], signal.SIGINT)
            print(f"✅ Sent interrupt signal to PID {proc['pid']}")
            stopped_count += 1
        except ProcessLookupError:
            print(f"⚠️ Process PID {proc['pid']} already stopped")
        except PermissionError:
            print(f"❌ Permission denied for PID {proc['pid']}")
        except Exception as e:
            print(f"❌ Error stopping PID {proc['pid']}: {e}")
    
    print(f"\n🎉 Gracefully stopped {stopped_count} scraper(s)")
    print("📁 Check for individual scraper data files:")
    print("   - nykaa_scraped_data.json")
    print("   - myntra_scraped_data.json") 
    print("   - zara_scraped_data.json")

def main():
    print("🛑 Scraper Shutdown Tool")
    print("=" * 40)
    
    try:
        stop_scrapers()
    except KeyboardInterrupt:
        print("\n⏹️ Shutdown interrupted")
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    main()
