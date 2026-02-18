#!/usr/bin/env python3
"""Test the EXACT endpoint logic without server"""

import sys
sys.path.insert(0, '.')

from main import sqlite_cache, db_service

print("=" * 70)
print("TESTING ENDPOINT LOGIC EXACTLY AS WRITTEN IN main.py LINE 471-481")
print("=" * 70)

# LINE 475: record_count = sqlite_cache.get_record_count()
record_count = sqlite_cache.get_record_count()
print(f"\nLINE 475: sqlite_cache.get_record_count() = {record_count:,}")

# LINE 478: if record_count > 0:
if record_count > 0:
    print(f"LINE 478: Condition TRUE (record_count > 0)")
    print("LINE 479: Calling sqlite_cache.get_filter_options()...")
    
    # LINE 479: return sqlite_cache.get_filter_options()    
    result = sqlite_cache.get_filter_options()
    
    print(f"\nRESULT: {len(result)} fields")
    print(f"KEYS: {sorted(result.keys())}")
    
    if 'business_areas' in result:
        print(f"\n✓ business_areas: {len(result['business_areas'])} values")
        print(f"  Sample: {result['business_areas'][:3]}")
    else:
        print("\n✗ business_areas: MISSING")
else:
    print(f"LINE 478: Condition FALSE")
    print("LINE 481: Would call db_service.get_filter_options()")
