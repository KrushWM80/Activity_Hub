#!/usr/bin/env python
"""Check when data was last updated from BigQuery"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect(r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=== Last Updated Timestamps ===\n")

# Check the MAX last_updated from data records
cursor.execute('''
SELECT 
    project_source,
    MIN(last_updated) as oldest_record,
    MAX(last_updated) as newest_record,
    COUNT(*) as total_rows
FROM projects
GROUP BY project_source
ORDER BY project_source
''')

print("Last Updated timestamps from data records:\n")
for row in cursor.fetchall():
    print(f"{row['project_source']}")
    print(f"  Oldest: {row['oldest_record']}")
    print(f"  Newest: {row['newest_record']}")
    print(f"  Total records: {row['total_rows']}\n")

# Check sync metadata
print("=== Cache Sync History ===\n")
cursor.execute('SELECT * FROM sync_log ORDER BY sync_timestamp DESC LIMIT 10')

if cursor.description:
    cols = [desc[0] for desc in cursor.description]
    print(f"Columns: {cols}\n")
    for row in cursor.fetchall():
        print(f"Sync Time: {row['sync_timestamp']}")
        print(f"  Status: {row['status']}")
        print(f"  Records: {row['record_count']}")
        print(f"  Duration: {row['sync_duration_seconds']}s")
        if row.get('error_message'):
            print(f"  Error: {row['error_message']}")
        print()
else:
    print("No sync_log table found")

conn.close()
