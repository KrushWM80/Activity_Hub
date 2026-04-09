#!/usr/bin/env python
"""Test corrected UNION ALL syntax"""
import sqlite3

conn = sqlite3.connect('projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Test corrected UNION ALL without extra parentheses
print("=== TEST: Corrected UNION ALL syntax ===")

where_clause = "1=1 AND project_id IS NOT NULL AND project_id != ''"

query = f"""
SELECT 
    project_id
FROM projects
WHERE {where_clause} AND project_source IN ('Operations', 'Intake Hub')
GROUP BY project_id, project_source
UNION ALL
SELECT 
    MIN(project_id) as project_id
FROM projects
WHERE {where_clause} AND project_source = 'Realty'
GROUP BY title, project_source
LIMIT 50000
"""

print("Executing UNION ALL query...")
cursor.execute(query, [])
rows = cursor.fetchall()

print(f"✅ Query executed successfully")
print(f"Result: {len(rows)} projects (expected 519)")

conn.close()
