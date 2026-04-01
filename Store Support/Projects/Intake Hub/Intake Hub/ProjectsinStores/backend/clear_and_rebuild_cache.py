"""Clear and rebuild cache from scratch"""
import sqlite3
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from sqlite_cache import get_cache, SQLiteCache
from database import DatabaseService

db_path = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db'

print("🗑️  Clearing old cache database...\n")

# Delete the database file
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"✓ Deleted {db_path}")
else:
    print(f"Database didn't exist, will create new one")

print("\n🔄 Initializing fresh cache...\n")

# Create new cache instance (this will reinitialize the database)
cache = SQLiteCache()

# Get BigQuery connection
db_service = DatabaseService()

if not db_service.client:
    print("❌ ERROR: BigQuery client not available")
    sys.exit(1)

print(f"Connected to BigQuery: {db_service.project_id}.{db_service.dataset}.{db_service.table}\n")

# Force sync
print("Starting fresh sync...\n")
success = cache.force_sync(
    db_service.client,
    db_service.project_id,
    db_service.dataset,
    db_service.table
)

if success:
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check Realty records
    cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty' AND project_id IS NOT NULL")
    realty_with_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty'")
    total_realty = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Operations'")
    total_ops = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM projects")
    total = cursor.fetchone()[0]
    
    # Show sample with 'FAC-' prefix
    cursor.execute("SELECT project_id, title, facility FROM projects WHERE project_id LIKE 'FAC-%' LIMIT 3")
    fac_samples = cursor.fetchall()
    
    conn.close()
    
    print(f"\n✅ Fresh sync completed!")
    print(f"   Total records: {total:,}")
    print(f"   Operations: {total_ops:,}")
    print(f"   Realty: {total_realty:,} (with project_id: {realty_with_id:,})")
    
    if fac_samples:
        print(f"\n   Sample 'FAC-' records:")
        for sample in fac_samples:
            print(f"     project_id={sample[0]}, title={sample[1][:40]}, facility={sample[2]}")
else:
    print("\n❌ Sync failed!")
    sys.exit(1)
