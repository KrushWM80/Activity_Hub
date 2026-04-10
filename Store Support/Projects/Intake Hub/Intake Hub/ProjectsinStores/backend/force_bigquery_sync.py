#!/usr/bin/env python3
"""Force immediate sync from BigQuery to refresh stale cache"""

from database import DatabaseService
from sqlite_cache import get_cache
import time

db_service = DatabaseService()
sqlite_cache = get_cache()

print("=== FORCE BIGQUERY SYNC ===\n")

print(f"Current cache status:")
print(f"  Records: {sqlite_cache.get_record_count():,}")
print(f"  Last sync: {sqlite_cache.get_last_sync_time()}")

if not db_service.client:
    print("\nInitializing BigQuery connection...")
    db_service._initialize_client()

if db_service.client:
    print(f"\nBigQuery connected: {db_service.project_id}.{db_service.dataset}.{db_service.table}")
    print("Starting force sync...")
    
    start_time = time.time()
    success = sqlite_cache.force_sync(
        db_service.client,
        db_service.project_id,
        db_service.dataset,
        db_service.table
    )
    duration = time.time() - start_time
    
    print(f"\n=== SYNC RESULTS ===")
    print(f"Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"New record count: {sqlite_cache.get_record_count():,}")
    print(f"Last sync time: {sqlite_cache.get_last_sync_time()}")
    
    # Show breakdown by source
    from sqlite3 import connect
    conn = connect('projects_cache.db')
    cursor = conn.cursor()
    
    print(f"\nData by source:")
    cursor.execute("""
        SELECT project_source, COUNT(DISTINCT title) as titles, COUNT(*) as total_rows
        FROM projects
        WHERE status = 'Active'
        GROUP BY project_source
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} titles, {row[2]:,} total rows")
    
    cursor.execute("""
        SELECT project_source, 
               COUNT(*) filter (WHERE last_updated IS NOT NULL) as with_timestamp,
               COUNT(*) filter (WHERE last_updated IS NULL) as null_timestamp
        FROM projects
        WHERE status = 'Active'
        GROUP BY project_source
    """)
    print(f"\nTimestamp coverage:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]:,} with timestamps, {row[2]:,} NULL")
    
    conn.close()
else:
    print("❌ Failed to connect to BigQuery")
