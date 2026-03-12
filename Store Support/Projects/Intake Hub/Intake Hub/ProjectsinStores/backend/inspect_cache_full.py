#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('projects_cache.db')
c = conn.cursor()

# Get schema
c.execute("PRAGMA table_info(projects)")
print('=== SCHEMA ===')
for row in c.fetchall():
    print(row)

# Get sample data
print('\n=== SAMPLE DATA (first 5 rows) ===')
c.execute('SELECT * FROM projects LIMIT 5')
cols = [description[0] for description in c.description]
print('Columns:', cols)
for row in c.fetchall():
    print(row)

# Check data distribution
print('\n=== DATA DISTRIBUTION ===')
c.execute('SELECT COUNT(*) as total FROM projects')
print('Total:', c.fetchone()[0])

c.execute('SELECT COUNT(*) FROM projects WHERE partner IS NOT NULL')
print('With partner:', c.fetchone()[0])

c.execute('SELECT COUNT(*) FROM projects WHERE partner IS NULL')
print('NULL partner:', c.fetchone()[0])

c.execute('SELECT DISTINCT partner FROM projects WHERE partner IS NOT NULL LIMIT 10')
print('\nSample partner values:', [row[0] for row in c.fetchall()])

# Check last sync
c.execute('SELECT * FROM sync_status ORDER BY id DESC LIMIT 1')
sync = c.fetchone()
if sync:
    print(f'\n=== LAST SYNC ===')
    print(f'ID: {sync[0]}')
    print(f'Timestamp: {sync[1]}')
    print(f'Record Count: {sync[2]}')
    print(f'Status: {sync[3]}')

conn.close()
