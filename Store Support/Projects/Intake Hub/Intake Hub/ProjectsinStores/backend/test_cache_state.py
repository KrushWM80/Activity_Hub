import sys
sys.path.insert(0, '/c/Users/krush/Documents/VSCode/Intake Hub/ProjectsinStores/backend')

from sqlite_cache import get_cache

cache = get_cache()
print(f"Cache valid: {cache.is_cache_valid()}")
print(f"Record count: {cache.get_record_count()}")
print(f"Last sync time: {cache.get_last_sync_time()}")

# Try getting filter options
try:
    filters = cache.get_filter_options()
    print(f"Filter keys: {list(filters.keys())}")
except Exception as e:
    print(f"Error: {e}")
