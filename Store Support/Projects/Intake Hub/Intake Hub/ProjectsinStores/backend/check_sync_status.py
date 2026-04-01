"""Check sync status and debug why Realty records are NULL"""
import sqlite3
import os
from datetime import datetime

db_path = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check sync status
try:
    cursor.execute("SELECT * FROM sync_status ORDER BY sync_timestamp DESC LIMIT 5")
    print("Recent sync status:")
    for row in cursor.fetchall():
        print(f"  {row}")
except Exception as e:
    print(f"Error checking sync_status: {e}")

print("\n" + "="*60 + "\n")

# Check if there's an error log
try:
    cursor.execute("SELECT message, timestamp FROM sync_error_log ORDER BY timestamp DESC LIMIT 3")
    print("Recent sync errors:")
    for row in cursor.fetchall():
        print(f"  {row}")
except Exception as e:
    print(f"Error checking sync_error_log: {e}")

print("\n" + "="*60 + "\n")

# Check actual Realty records in cache
cursor.execute("""SELECT project_id, facility, title FROM projects 
                  WHERE project_source = 'Realty' LIMIT 5""")
print("Sample Realty records in cache:")
for row in cursor.fetchall():
    print(f"  project_id={row[0]}, facility={row[1]}, title={row[2][:30]}")

conn.close()
