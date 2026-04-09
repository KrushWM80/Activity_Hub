#!/usr/bin/env python
"""Test with higher limit"""
import requests
import json

BASE_URL = "http://localhost:8001"

print("=== TEST: GET /api/projects?project_source=Realty&limit=300 ===")
try:
    response = requests.get(f"{BASE_URL}/api/projects?project_source=Realty&limit=300", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"Got {len(data)} Realty projects (expected 239)")
        
        # Check unique titles
        titles = set()
        for p in data:
            titles.add(p.get('title'))
        print(f"Unique titles: {len(titles)}")
        
        # Check stores
        stores = set()
        for p in data:
            if p.get('store'):
                stores.add(p.get('store'))
        print(f"Unique stores: {len(stores)}")
        
        # Show first 3 records
        print("\nFirst 3 records:")
        for i, p in enumerate(data[:3]):
            print(f"  {i+1}. {p.get('project_id'):10} {p.get('title')[:40]:40} {p.get('project_source')}")
    else:
        print(f"ERROR: {response.status_code} {response.text}")
except Exception as e:
    print(f"FAILED: {e}")

print("\n=== TEST: Count Realty per title from DB ===")
import sqlite3
conn = sqlite3.connect('projects_cache.db')
cursor = conn.cursor()
cursor.execute('SELECT title, COUNT(DISTINCT store) as store_count FROM projects WHERE project_source = "Realty" GROUP BY title ORDER BY store_count DESC LIMIT 5')
print("Top 5 Realty projects by store count:")
for row in cursor.fetchall():
    print(f"  {row[0][:40]:40} - {row[1]:4} stores")
conn.close()
