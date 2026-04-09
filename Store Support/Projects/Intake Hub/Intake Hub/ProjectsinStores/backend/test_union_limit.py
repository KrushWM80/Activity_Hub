#!/usr/bin/env python
"""Test UNION ALL query with LIMIT directly"""
import sqlite3

conn = sqlite3.connect('projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Test the exact UNION ALL query that should be used
print("=== TEST: UNION ALL with LIMIT 50000 ===")

# Build exact WHERE clause (no filters)
where_clause = "1=1 AND project_id IS NOT NULL AND project_id != ''"

query = f"""
(
    SELECT 
        project_id
    FROM projects
    WHERE {where_clause} AND project_source IN ('Operations', 'Intake Hub')
    GROUP BY project_id, project_source
)
UNION ALL
(
    SELECT 
        MIN(project_id) as project_id
    FROM projects
    WHERE {where_clause} AND project_source = 'Realty'
    GROUP BY title, project_source
)
ORDER BY project_id
LIMIT 50000
"""

print(f"Query:\n{query}\n")

cursor.execute(query, [])
rows = cursor.fetchall()

print(f"Result: {len(rows)} rows")

# Count by checking first and last
if rows:
    print(f"First 5:")
    for i, row in enumerate(rows[:5]):
        print(f"  {row['project_id']}")
    if len(rows) > 10:
        print(f"  ... ({len(rows)-10} more)")
        print(f"Last 5:")
        for row in rows[-5:]:
            print(f"  {row['project_id']}")

conn.close()
