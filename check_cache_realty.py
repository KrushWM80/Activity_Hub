"""Check what's in the SQLite cache"""
import sqlite3
import os

db_path = 'Store Support/Projects/Intake Hub/Intake Hub/ProjectsinStores/backend/projects_cache.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check total records
    cursor.execute('SELECT COUNT(*) FROM projects')
    total = cursor.fetchone()[0]
    print(f'Total records in SQLite: {total}')
    
    # Check Realty records
    cursor.execute('SELECT COUNT(*) FROM projects WHERE project_source = ?', ('Realty',))
    realty = cursor.fetchone()[0]
    print(f'Realty records in SQLite: {realty}')
    
    # Check counts by source
    cursor.execute('''
        SELECT project_source, COUNT(*) as cnt 
        FROM projects 
        GROUP BY project_source 
        ORDER BY cnt DESC
    ''')
    print('\nRecords by Source:')
    for source, count in cursor.fetchall():
        print(f'  {source}: {count}')
    
    # Check if Realty records have project_id NULL
    cursor.execute('SELECT COUNT(*) FROM projects WHERE project_source = ? AND project_id IS NULL', ('Realty',))
    null_count = cursor.fetchone()[0]
    print(f'\nRealty records with NULL project_id: {null_count}')
    
    # Get sample Realty records
    cursor.execute('SELECT project_id, title, status FROM projects WHERE project_source = ? LIMIT 5', ('Realty',))
    print(f'\nSample Realty records:')
    for pid, title, status in cursor.fetchall():
        print(f'  ID: {pid} | Title: {title} | Status: {status}')
    
    conn.close()
else:
    print(f'Database not found at {db_path}')
