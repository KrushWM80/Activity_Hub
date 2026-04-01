"""Force immediate cache resync to fix Realty project_id values"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from sqlite_cache import get_cache
from database import DatabaseService

print("🔄 Forcing cache resync to fix Realty records...\n")

# Get services
db_service = DatabaseService()
cache = get_cache()

# Check if BigQuery client is available
if not db_service.client:
    print("❌ ERROR: BigQuery client not available")
    print("   Make sure you've authenticated with: gcloud auth application-default login")
    sys.exit(1)

print(f"Connected to BigQuery project: {db_service.project_id}")
print(f"Dataset: {db_service.dataset}")
print(f"Table: {db_service.table}\n")

# Force sync
print("Starting sync...")
success = cache.force_sync(
    db_service.client,
    db_service.project_id,
    db_service.dataset,
    db_service.table
)

if success:
    count = cache.get_record_count()
    last_sync = cache.get_last_sync_time()
    print(f"\n✅ Sync completed successfully!")
    print(f"   Records in cache: {count:,}")
    print(f"   Last sync: {last_sync}")
    
    # Check Realty records specifically
    import sqlite3
    db_path = os.path.join(os.path.dirname(__file__), 'projects_cache.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty' AND project_id IS NOT NULL")
    realty_with_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty'")
    total_realty = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n   Realty records with project_id: {realty_with_id:,} / {total_realty:,}")
    if realty_with_id > 0:
        print("   ✓ Realty records now have project_id values!")
else:
    print("\n❌ Sync failed!")
    print("   Check logs above for details")
    sys.exit(1)
