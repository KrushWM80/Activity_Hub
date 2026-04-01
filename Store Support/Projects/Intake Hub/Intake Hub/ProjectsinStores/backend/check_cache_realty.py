import sqlite3
conn = sqlite3.connect('projects_cache.db')
cursor = conn.cursor()

# Check total records
cursor.execute('SELECT COUNT(*) FROM projects')
total = cursor.fetchone()[0]
print(f'Total cache records: {total}')

# Check by project_source
cursor.execute('SELECT project_source, COUNT(*) FROM projects GROUP BY project_source')
results = cursor.fetchall()
print(f'\nBreakdown by project_source:')
for source, count in results:
    print(f'  {source}: {count}')

# Check a Realty project
cursor.execute('SELECT project_id, title, project_source FROM projects WHERE project_source = ? LIMIT 2', ('Realty',))
samples = cursor.fetchall()
if samples:
    print(f'\nSample Realty records:')
    for row in samples:
        print(f'  {row}')
else:
    print(f'\nNo Realty records in cache')
