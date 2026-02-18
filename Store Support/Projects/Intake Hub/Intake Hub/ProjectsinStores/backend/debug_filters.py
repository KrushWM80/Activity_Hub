#!/usr/bin/env python3
"""Debug script to check cache and filters"""
import sqlite3

conn = sqlite3.connect('projects_cache.db')
cursor = conn.cursor()

print("=== CHECKING CACHE DATABASE ===\n")

# Check table schema
print("Columns in projects table:")
cursor.execute("PRAGMA table_info(projects)")
columns = cursor.fetchall()
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

print("\n=== CHECKING DATA IN NEW COLUMNS ===\n")

new_columns = ['owner', 'store_area', 'business_area', 'health', 'business_type', 'associate_impact', 'customer_impact']

for col in new_columns:
    cursor.execute(f"SELECT COUNT(DISTINCT {col}) FROM projects WHERE {col} IS NOT NULL AND {col} != ''")
    count = cursor.fetchone()[0]
    print(f"{col}: {count} distinct values")
    
    if count > 0:
        cursor.execute(f"SELECT DISTINCT {col} FROM projects WHERE {col} IS NOT NULL AND {col} != '' LIMIT 3")
        samples = [row[0] for row in cursor.fetchall()]
        print(f"  Samples: {samples}")

conn.close()

print("\n=== CHECKING WHAT get_filter_options RETURNS ===\n")

from sqlite_cache import get_cache
cache = get_cache()
filters = cache.get_filter_options()

print("Returned filter keys:", sorted(filters.keys()))
print()
for key in sorted(filters.keys()):
    count = len(filters[key])
    print(f"{key}: {count} values")
