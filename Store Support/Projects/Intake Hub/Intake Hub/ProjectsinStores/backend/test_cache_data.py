#!/usr/bin/env python3
"""Test what cache actually returns"""
import time
from sqlite_cache import SQLiteCache

cache = SQLiteCache()

print("Cache valid:", cache.is_cache_valid())
print("Cache record count:", cache.get_record_count())

print("\nCalling cache.get_filter_options()...")
start = time.time()
filters = cache.get_filter_options()
elapsed = time.time() - start

print(f"Query took: {elapsed:.2f}s")
print(f"Returned {len(filters)} filter keys")
print("\nFilter keys:")
for key in sorted(filters.keys()):
    count = len(filters[key])
    print(f"  {key}: {count} values")
