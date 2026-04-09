#!/usr/bin/env python
"""Diagnose Realty vs Operations data structure"""
import sqlite3

conn = sqlite3.connect('projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check a few Realty records
print('=== REALTY RECORDS (Sample) ===')
cursor.execute('SELECT project_id, title, project_source FROM projects WHERE project_source = "Realty" LIMIT 5')
for row in cursor.fetchall():
    print(f'project_id: {row["project_id"]!r}, title: {row["title"]!r}, source: {row["project_source"]!r}')

# Check a few Operations records
print('\n=== OPERATIONS RECORDS (Sample) ===')
cursor.execute('SELECT project_id, title, project_source FROM projects WHERE project_source = "Operations" LIMIT 5')
for row in cursor.fetchall():
    print(f'project_id: {row["project_id"]!r}, title: {row["title"]!r}, source: {row["project_source"]!r}')

# Count by source
print('\n=== TOTAL COUNTS ===')
cursor.execute('SELECT project_source, COUNT(*) as cnt FROM projects GROUP BY project_source')
for row in cursor.fetchall():
    print(f'{row["project_source"]}: {row["cnt"]} rows')

# Count DISTINCT by source
print('\n=== DISTINCT PROJECT COUNTS ===')
cursor.execute('''
SELECT 
    project_source,
    COUNT(DISTINCT project_id) as distinct_by_id,
    COUNT(DISTINCT title) as distinct_by_title,
    SUM(CASE WHEN project_id IS NULL THEN 1 ELSE 0 END) as null_project_ids,
    SUM(CASE WHEN project_id = '' THEN 1 ELSE 0 END) as empty_project_ids
FROM projects
GROUP BY project_source
''')
for row in cursor.fetchall():
    print(f'{row["project_source"]}: {row["distinct_by_id"]} by ID, {row["distinct_by_title"]} by title, {row["null_project_ids"]} NULLs, {row["empty_project_ids"]} empty')

# Check what the current query returns
print('\n=== CURRENT QUERY SIMULATION ===')
print('With WHERE project_source = "Realty" AND project_id IS NOT NULL AND project_id != \'\':')
cursor.execute('''
SELECT COUNT(DISTINCT project_id) FROM projects 
WHERE project_source = "Realty" 
AND project_id IS NOT NULL 
AND project_id != ''
''')
result = cursor.fetchone()[0]
print(f'Result: {result} projects')

conn.close()
