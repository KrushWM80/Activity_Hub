#!/usr/bin/env python
"""Check what the API returns for store data"""
import requests
import json

BASE_URL = "http://localhost:8001"

print("=== API Summary Response ===")
response = requests.get(f"{BASE_URL}/api/summary", timeout=5)
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"ERROR: {response.status_code}")

print("\n=== Sample Projects (first 5) ===")
response = requests.get(f"{BASE_URL}/api/projects?limit=5", timeout=5)
if response.status_code == 200:
    data = response.json()
    for i, p in enumerate(data[:5], 1):
        print(f"{i}. {p['title'][:40]:40} source={p['project_source']:12} store={p.get('store'):8} store_count={p.get('store_count')}")
else:
    print(f"ERROR: {response.status_code}")

print("\n=== Realty Projects (first 3) ===")
response = requests.get(f"{BASE_URL}/api/projects?project_source=Realty&limit=3", timeout=5)
if response.status_code == 200:
    data = response.json()
    for i, p in enumerate(data[:3], 1):
        print(f"{i}. {p['title'][:40]:40} store={p.get('store'):8} store_count={p.get('store_count')}")
else:
    print(f"ERROR: {response.status_code}")

print("\n=== Check DB: Unique stores per source ===")
import sqlite3
conn = sqlite3.connect(r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('''
SELECT 
    project_source,
    COUNT(DISTINCT store) as unique_stores,
    COUNT(*) as total_rows
FROM projects
GROUP BY project_source
''')

for row in cursor.fetchall():
    print(f"{row['project_source']:12} - {row['unique_stores']:5} unique stores, {row['total_rows']:7} rows")

conn.close()
