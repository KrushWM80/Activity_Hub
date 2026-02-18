"""
Diagnostic script to understand what's happening with the cache
"""
import sys
from datetime import datetime
sys.path.insert(0, '.')

from sqlite_cache import get_cache

print("=== CACHE DIAGNOSTIC ===\n")

cache = get_cache()

# Check basic cache state
record_count = cache.get_record_count()
last_sync = cache.get_last_sync_time()
is_valid_30 = cache.is_cache_valid(max_age_minutes=30)
is_valid_60 = cache.is_cache_valid(max_age_minutes=60)

print(f"Record count: {record_count}")
print(f"Last sync time: {last_sync}")
print(f"Current time: {datetime.now()}")
if last_sync:
    age_minutes = (datetime.now() - last_sync).total_seconds() / 60
    print(f"Age: {age_minutes:.1f} minutes")
print(f"\nis_cache_valid(max_age_minutes=30): {is_valid_30}")
print(f"is_cache_valid(max_age_minutes=60): {is_valid_60}")

# If cache is valid, get filter options
if is_valid_30:
    print("\n=== CACHE VALID - Getting filter options ===")
    filters = cache.get_filter_options()
    print(f"Filter keys returned: {len(filters)}")
    print(f"Keys: {sorted(filters.keys())}")
    
    # Check for new fields
    expected_fields = [
        'divisions', 'regions', 'markets', 'stores', 'phases',
        'fiscal_years', 'wm_weeks', 'project_sources', 'owners',
        'store_areas', 'business_areas', 'health_statuses',
        'business_types', 'associate_impacts', 'customer_impacts'
    ]
    missing = set(expected_fields) - set(filters.keys())
    if missing:
        print(f"\nMISSING FIELDS: {missing}")
    
    # Show counts
    print("\nField value counts:")
    for key in sorted(filters.keys()):
        print(f"  {key}: {len(filters[key])} values")
else:
    print("\n=== CACHE INVALID - Would use database fallback ===")
