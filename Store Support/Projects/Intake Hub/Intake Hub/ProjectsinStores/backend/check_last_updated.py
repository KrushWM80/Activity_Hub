#!/usr/bin/env python
"""Get last update timestamps from API and database"""
import sqlite3
import requests
from datetime import datetime

print("=== Data Last Updated Timestamps ===\n")

# Get from API summary
print("From API /api/summary:")
try:
    response = requests.get("http://localhost:8001/api/summary", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"  last_updated: {data.get('last_updated', 'N/A')}")
        print(f"  Total Projects: {data.get('total_active_projects')}")
        print(f"  Realty: {data.get('realty_projects')} projects, {data.get('realty_stores')} stores")
        print(f"  Operations: {data.get('intake_hub_projects')} projects, {data.get('intake_hub_stores')} stores")
    else:
        print(f"  ERROR: {response.status_code}")
except Exception as e:
    print(f"  ERROR: {e}")

# Get from database
print("\nFrom SQLite cache database:\n")
conn = sqlite3.connect(r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('''
SELECT 
    project_source,
    MAX(last_updated) as latest_update
FROM projects
WHERE last_updated IS NOT NULL
GROUP BY project_source
ORDER BY project_source
''')

for row in cursor.fetchall():
    print(f"{row['project_source']:12} latest: {row['latest_update']}")

# Also check one sample record
print("\nSample record detail:")
cursor.execute('SELECT * FROM projects LIMIT 1')
if cursor.description:
    row = cursor.fetchone()
    if row:
        print(f"  Columns: {[desc[0] for desc in cursor.description]}")
        print(f"  last_updated value: {row['last_updated']}")

# Check database metadata
print("\nDatabase tables:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
for row in cursor.fetchall():
    print(f"  - {row['name']}")

conn.close()
