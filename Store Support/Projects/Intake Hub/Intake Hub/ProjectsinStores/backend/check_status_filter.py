#!/usr/bin/env python
"""Check what project statuses exist in the database"""
import sqlite3

conn = sqlite3.connect(r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=== Project Status Distribution ===\n")

cursor.execute('''
SELECT 
    project_source,
    status,
    COUNT(*) as row_count,
    COUNT(DISTINCT 
        CASE 
            WHEN project_source = 'Operations' THEN project_id
            WHEN project_source = 'Realty' THEN title
        END
    ) as unique_projects
FROM projects
GROUP BY project_source, status
ORDER BY project_source, status
''')

print(f"{'Source':<12} {'Status':<15} {'Rows':<12} {'Projects'}")
print("-" * 55)

for row in cursor.fetchall():
    print(f"{row['project_source']:<12} {row['status']:<15} {row['row_count']:<12} {row['unique_projects']}")

print("\n=== What's Currently Being Shown (status='Active' only) ===\n")

cursor.execute('''
SELECT 
    project_source,
    COUNT(*) as row_count,
    COUNT(DISTINCT 
        CASE 
            WHEN project_source = 'Operations' THEN project_id
            WHEN project_source = 'Realty' THEN title
        END
    ) as unique_projects
FROM projects
WHERE status = 'Active'
GROUP BY project_source
ORDER BY project_source
''')

for row in cursor.fetchall():
    print(f"{row['project_source']:<12} {row['row_count']:<12} {row['unique_projects']} projects shown")

conn.close()
