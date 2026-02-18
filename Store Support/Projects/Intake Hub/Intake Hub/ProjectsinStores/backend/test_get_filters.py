from sqlite_cache import get_cache

cache = get_cache()
print("Cache valid:", cache.is_cache_valid())
print("Record count:", cache.get_record_count())

filters = cache.get_filter_options()
print("\nFilter keys returned by get_filter_options():")
for key in sorted(filters.keys()):
    print(f"  {key}: {len(filters[key])} values")

print("\nExpected 16 keys, got:", len(filters.keys()))
missing = {'owners', 'store_areas', 'business_areas', 'health_statuses', 'business_types', 'associate_impacts', 'customer_impacts'} - set(filters.keys())
if missing:
    print("Missing:", missing)
