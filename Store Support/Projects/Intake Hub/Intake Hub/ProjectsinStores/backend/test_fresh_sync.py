import sys
sys.path.insert(0, '/c/Users/krush/Documents/VSCode/Intake Hub/ProjectsinStores/backend')

from sqlite_cache import get_cache
from database import db_service

print("Starting cache sync from BigQuery...")
cache = get_cache()

# Sync the cache
success = cache.sync_from_bigquery(
    db_service.client,
    db_service.project_id,
    db_service.dataset,
    db_service.table
)

print(f"Sync success: {success}")
print(f"Cache valid: {cache.is_cache_valid()}")
print(f"Record count: {cache.get_record_count()}")

# Get filters
filters = cache.get_filter_options()
print(f"Filter keys: {sorted(list(filters.keys()))}")
print(f"Owners count: {len(filters.get('owners', []))}")
