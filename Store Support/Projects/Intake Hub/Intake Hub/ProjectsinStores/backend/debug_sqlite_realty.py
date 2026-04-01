"""Check if Realty records are in SQLite database"""
import sqlite3
import os

db_path = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db'

if not os.path.exists(db_path):
    print(f"ERROR: Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if projects table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
if not cursor.fetchone():
    print("ERROR: projects table doesn't exist in database")
    exit(1)

# Check total records
cursor.execute("SELECT COUNT(*) FROM projects")
total = cursor.fetchone()[0]
print(f"Total records in SQLite projects table: {total}\n")

# Try to find any records with 'FAC-' prefix (Realty records should have this)
cursor.execute("SELECT COUNT(*) FROM projects WHERE project_id LIKE 'FAC-%'")
fac_count = cursor.fetchone()[0]
print(f"Records with 'FAC-' prefix (Realty): {fac_count}")

# Show sample Realty records
print(f"\nSample 'FAC-' prefixed records:")
cursor.execute("SELECT project_id, title, store FROM projects WHERE project_id LIKE 'FAC-%' LIMIT 5")
for row in cursor.fetchall():
    print(f"  project_id={row[0]}, title={row[1][:30]}, store={row[2]}")

# Check what project_ids are NULL
cursor.execute("SELECT COUNT(*) FROM projects WHERE project_id IS NULL")
null_count = cursor.fetchone()[0]
print(f"\nRecords with NULL project_id: {null_count}")

# Check project_source column
cursor.execute("SELECT COUNT(DISTINCT project_source) FROM projects")
source_count = cursor.fetchone()[0]
print(f"\nDistinct project sources: {source_count}")

cursor.execute("SELECT DISTINCT project_source FROM projects")
sources = cursor.fetchall()
for source in sources:
    cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = ?", (source[0],))
    count = cursor.fetchone()[0]
    print(f"  '{source[0]}': {count}")

conn.close()
