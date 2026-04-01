"""Directly fix NULL project_id in existing Realty records using SQL UPDATE"""
import sqlite3
import os

db_path = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db'

print("🔧 Fixing Realty project_id values using direct SQL UPDATE...\n")

# Check if database exists
if not os.path.exists(db_path):
    print(f"❌ Database not found: {db_path}")
    print("   Please restore from backup or let sync complete first.")
    exit(1)

conn = sqlite3.connect(db_path)
conn.execute("PRAGMA journal_mode=WAL")  # Better for concurrent access
cursor = conn.cursor()

# Check current state
cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty'")
total_realty = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty' AND project_id IS NULL")
null_ids = cursor.fetchone()[0]

print(f"Current state:")
print(f"  Total Realty records: {total_realty:,}")
print(f"  With NULL project_id: {null_ids:,}\n")

if null_ids == 0:
    print("✓ All Realty records already have project_id!")
    conn.close()
    exit(0)

# Update NULL project_id using FAC- + facility  
print(f"Updating {null_ids:,} records with NULL project_id...\n")

cursor.execute("""
    UPDATE projects
    SET project_id = 'FAC-' || facility
    WHERE project_source = 'Realty' AND project_id IS NULL
""")

conn.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty' AND project_id IS NULL")
still_null = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty' AND project_id LIKE 'FAC-%'")
with_fac = cursor.fetchone()[0]

print(f"After update:")
print(f"  Still NULL: {still_null:,}")
print(f"  With 'FAC-' prefix: {with_fac:,}\n")

# Show samples
cursor.execute("SELECT project_id, title, facility FROM projects WHERE project_id LIKE 'FAC-%' LIMIT 5")
print(f"Sample fixed records:")
for i, (pid, title, fac) in enumerate(cursor.fetchall(), 1):
    print(f"  {i}. project_id={pid}, facility={fac}, title='{title[:40]}'")

conn.close()

print(f"\n✅ Fix complete! Cache now has Realty records with project_id values.")
print(f"   Restart the server to load updated cache.")
