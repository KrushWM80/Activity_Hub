#!/usr/bin/env python3
"""Direct test of the cache and backend flow"""

from sqlite_cache import get_cache

cache = get_cache()

print("=== CACHE STATUS ===\n")
print(f"Record count: {cache.get_record_count():,}")
print(f"Last sync: {cache.get_last_sync_time()}")
print(f"Is cache valid: {cache.is_cache_valid(max_age_minutes=60)}")
print(f"Data freshness: {cache.get_data_freshness()}")

print("\n=== TEST QUERY ===\n")
# Test get_projects with no filters - should return many projects
projects = cache.get_projects(filters={'status': 'Active'}, limit=50)
print(f"Got {len(projects)} projects with limit=50")

if projects:
    print("\nFirst 5 projects:")
    for i, p in enumerate(projects[:5], 1):
        print(f"  [{i}] {p.get('title')} ({p.get('project_source')})")
else:
    print("ERROR: No projects returned!")
