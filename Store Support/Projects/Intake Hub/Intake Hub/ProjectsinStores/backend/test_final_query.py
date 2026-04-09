#!/usr/bin/env python
"""Test fixed query with proper parameter binding"""
import sqlite3

conn = sqlite3.connect('projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Test 1: Filter by Realty
print('=== TEST 1: Filter by project_source=Realty ===')
cursor.execute('''
SELECT COUNT(*) as cnt FROM (
    SELECT MIN(project_id) as project_id FROM projects 
    WHERE project_source = 'Realty'
    GROUP BY title, project_source
)
''')
result = cursor.fetchone()[0]
print(f'Realty projects: {result} (expected 239)')

# Test 2: Filter by Operations
print('\n=== TEST 2: Filter by project_source=Operations ===')
cursor.execute('''
SELECT COUNT(*) as cnt FROM (
    SELECT project_id FROM projects 
    WHERE project_source IN ('Operations', 'Intake Hub')
    GROUP BY project_id, project_source
)
''')
result = cursor.fetchone()[0]
print(f'Operations projects: {result} (expected 280)')

# Test 3: No filter (UNION both)
print('\n=== TEST 3: No filter - UNION both sources ===')
cursor.execute('''
SELECT COUNT(*) as cnt FROM (
    SELECT project_id FROM projects 
    WHERE project_source IN ('Operations', 'Intake Hub')
    GROUP BY project_id, project_source
    UNION ALL
    SELECT MIN(project_id) FROM projects 
    WHERE project_source = 'Realty'
    GROUP BY title, project_source
)
''')
result = cursor.fetchone()[0]
print(f'Total projects: {result} (expected 519)')

# Test 4: Sample results for Realty
print('\n=== TEST 4: Sample Realty results ===')
cursor.execute('''
SELECT title, MIN(project_id) as project_id FROM projects 
WHERE project_source = 'Realty'
GROUP BY title, project_source
LIMIT 5
''')
for row in cursor.fetchall():
    print(f'{row["project_id"]:8} {row["title"][:40]}')

conn.close()
