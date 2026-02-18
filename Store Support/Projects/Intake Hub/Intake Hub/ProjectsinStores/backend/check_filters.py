import sys
sys.path.insert(0, '.')
from sqlite_cache import SQLiteCache

cache = SQLiteCache()

print(f"Cache valid: {cache.is_cache_valid()}")

filters = cache.get_filter_options()

for key, values in filters.items():
    print(f"{key}: {len(values)} values")
    if values and len(values) <= 10:
        print(f"  -> {values}")
    elif values:
        print(f"  -> {values[:5]}...")
