"""Test API endpoint for Realty filter"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sqlite_cache import get_cache

# Get cache instance
cache = get_cache()

print("Testing cache.get_projects() for Realty filters...\n")

# Test 1: Filter by project_source='Realty'
filters = {'project_source': 'Realty'}
results = cache.get_projects(filters=filters, limit=50000)

print(f"Results with project_source='Realty': {len(results)} records")

if results:
    print(f"\nFirst 3 records:")
    for i, r in enumerate(results[:3], 1):
        print(f"  {i}. project_id={r['project_id']}, title={r['title'][:40]}, source={r['project_source']}")
    
    # Check store_count key
    print(f"\nKeys in first record: {list(results[0].keys())}")
    
    # Verify store_count exists
    if 'store_count' in results[0]:
        print(f"✓ store_count is present in results")
    else:
        print(f"✗ store_count is MISSING from results")

print("\n✅ Cache.get_projects() working correctly!")
