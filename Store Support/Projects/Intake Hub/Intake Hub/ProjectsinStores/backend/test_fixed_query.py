#!/usr/bin/env python
"""Test the fixed query"""
import sqlite3

conn = sqlite3.connect('projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Test 1: All projects
print('=== TEST 1: All projects (no filter) ===')
cursor.execute('''
SELECT COUNT(*) as cnt FROM (
    SELECT project_id FROM projects WHERE project_source IN ('Operations', 'Intake Hub') GROUP BY project_id, project_source
    UNION ALL
    SELECT MIN(project_id) FROM projects WHERE project_source = 'Realty' GROUP BY title, project_source
)
''')
print(f'Total unique projects: {cursor.fetchone()[0]}')

# Test 2: Only Realty
print('\n=== TEST 2: Realty only ===')
cursor.execute('''
SELECT COUNT(*) as cnt FROM (
    SELECT MIN(project_id) FROM projects WHERE project_source = 'Realty' GROUP BY title, project_source
)
''')
result = cursor.fetchone()[0]
print(f'Realty unique projects: {result} (expected 239)')

# Test 3: Only Operations
print('\n=== TEST 3: Operations only ===')
cursor.execute('''
SELECT COUNT(*) as cnt FROM (
    SELECT project_id FROM projects WHERE project_source IN ('Operations', 'Intake Hub') GROUP BY project_id, project_source
)
''')
result = cursor.fetchone()[0]
print(f'Operations unique projects: {result} (expected 280)')

# Test 4: Sample Realty results
print('\n=== TEST 4: Sample Realty titles ===')
cursor.execute('''
SELECT MIN(project_id) as project_id, title, project_source FROM projects WHERE project_source = 'Realty' GROUP BY title, project_source LIMIT 5
''')
for row in cursor.fetchall():
    print(f'{row["project_id"]:8} {row["title"][:40]:40} {row["project_source"]}')

conn.close()
