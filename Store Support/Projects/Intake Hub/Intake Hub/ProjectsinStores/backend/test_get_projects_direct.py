#!/usr/bin/env python
"""Test get_projects function directly"""
import sqlite3
import sys
sys.path.insert(0, r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend')

from sqlite_cache import SQLiteCache

cache = SQLiteCache()

print("=== TEST 1: No filters, limit=50000 ===")
projects = cache.get_projects(filters=None, limit=50000)
print(f"Returned: {len(projects)} projects")

print("\n=== TEST 2: Filter by Realty, limit=50000 ===")
projects = cache.get_projects(filters={'project_source': 'Realty'}, limit=50000)
print(f"Returned: {len(projects)} projects")

print("\n=== TEST 3: Filter by Operations, limit=50000 ===")
projects = cache.get_projects(filters={'project_source': 'Operations'}, limit=50000)
print(f"Returned: {len(projects)} projects")
