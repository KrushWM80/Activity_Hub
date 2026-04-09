#!/usr/bin/env python
"""Test Realty filter with detailed debugging"""
import requests
import json

BASE_URL = "http://localhost:8001"

print("=== Direct DB query test ===")
import sqlite3
conn = sqlite3.connect('projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('''
SELECT COUNT(DISTINCT title) as cnt FROM projects WHERE project_source = "Realty"
''')
count = cursor.fetchone()['cnt']
print(f"Direct DB: Realty has {count} unique projects")
conn.close()

print("\n=== API Test with project_source=Realty ===")
response = requests.get(f"{BASE_URL}/api/projects?project_source=Realty&limit=500", timeout=10)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"API returned: {len(data)} projects")
    
    # Count by source
    ops_count = 0
    realty_count = 0
    sources = {}
    for p in data:
        src = p.get('project_source')
        sources[src] = sources.get(src, 0) + 1
        if src == 'Operations':
            ops_count += 1
        elif src == 'Realty':
            realty_count += 1
    
    print(f"\nBreakdown:")
    for src, cnt in sorted(sources.items()):
        print(f"  {src}: {cnt}")
    
    # Check titles
    realty_titles = set()
    for p in data:
        if p.get('project_source') == 'Realty':
            realty_titles.add(p['title'])
    print(f"\nUnique Realty titles: {len(realty_titles)}")
else:
    print(f"ERROR: {response.text}")
