#!/usr/bin/env python3
"""Compare what endpoint RETURNS vs what it SHOULD return"""

import sys
import asyncio
sys.path.insert(0, '.')

# Test what sqlite_cache.get_filter_options() returns
print('=' * 70)
print('TESTING: sqlite_cache.get_filter_options()')
print('=' * 70)

from sqlite_cache import get_cache
cache = get_cache()

cache_valid = cache.is_cache_valid()
print(f'\n1. Cache validity check: {cache_valid}')

if cache_valid:
    print('   ✓ Cache is VALID - endpoint SHOULD use cache')
else:
    print('   ✗ Cache is INVALID - endpoint will use database.py fallback')
    
    # Debug WHY it's invalid
    record_count = cache.get_record_count()
    last_sync = cache.get_last_sync_time()
    print(f'\n   Debug info:')
    print(f'     - Record count: {record_count:,}')
    print(f'     - Last sync time: {last_sync}')

print('\n2. Getting filter options from cache...')
filters_from_cache = cache.get_filter_options()

print(f'\n3. Cache returns {len(filters_from_cache)} fields:')
for key in sorted(filters_from_cache.keys()):
    count = len(filters_from_cache[key])
    sample = filters_from_cache[key][:3] if count > 0 else []
    print(f'     {key}: {count} values {sample}')

# Now test what database.py would return
print('\n' + '=' * 70)
print('TESTING: database.py get_filter_options() (FALLBACK)')
print('=' * 70)

from database import DatabaseService
db_service = DatabaseService()

print('\nNote: database.py may connect to BigQuery or return mock data')
# database.py method is NOT async, check the actual method
try:
    filters_from_db = db_service.get_filter_options()
except Exception as e:
    print(f'Error calling get_filter_options: {e}')
    filters_from_db = {}

print(f'\nDatabase/Mock returns {len(filters_from_db)} fields:')
for key in sorted(filters_from_db.keys()):
    count = len(filters_from_db[key])
    sample = filters_from_db[key][:3] if count > 0 else []
    print(f'     {key}: {count} values {sample}')

# Compare
print('\n' + '=' * 70)
print('COMPARISON: Cache vs Database/Mock')
print('=' * 70)

cache_keys = set(filters_from_cache.keys())
db_keys = set(filters_from_db.keys())

print(f'\nCache has {len(cache_keys)} fields')
print(f'Database/Mock has {len(db_keys)} fields')

missing_in_db = cache_keys - db_keys
extra_in_db = db_keys - cache_keys

if missing_in_db:
    print(f'\n❌ MISSING in Database/Mock (these are the 6 fields NOT returned):')
    for key in sorted(missing_in_db):
        print(f'     - {key}')

if extra_in_db:
    print(f'\n⚠️  EXTRA in Database/Mock:')
    for key in sorted(extra_in_db):
        print(f'     - {key}')

# Final verdict
print('\n' + '=' * 70)
print('VALIDATION RESULT')
print('=' * 70)

if cache_valid:
    print('\n✓ Cache is VALID')
    print(f'✓ Cache has all {len(cache_keys)} expected fields including business_areas')
    print('❌ BUT endpoint still returns 9 fields instead of 15')
    print('\n⚠️  DIAGNOSIS: Cache validity check PASSES in standalone test')
    print('⚠️            but FAILS when running in FastAPI server')
    print('⚠️            This suggests a state/initialization issue in the running server')
else:
    print('\n❌ Cache is INVALID even in standalone test')
    print('❌ The is_cache_valid() check is broken')
    print(f'\n   Record count: {record_count}')
    print(f'   Last sync: {last_sync}')
