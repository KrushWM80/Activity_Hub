import sqlite3

conn = sqlite3.connect('projects_cache.db')
cursor = conn.cursor()

# Check how many projects have partner data
cursor.execute('SELECT COUNT(*), COUNT(CASE WHEN partner IS NOT NULL AND partner != "" THEN 1 END) FROM projects')
total, with_partner = cursor.fetchone()
print(f'Total projects: {total}')
print(f'Projects with partner value: {with_partner}')

# Show sample partners
cursor.execute('SELECT DISTINCT partner FROM projects WHERE partner IS NOT NULL AND partner != "" ORDER BY partner LIMIT 15')
partners = cursor.fetchall()
print(f'\nSample partners ({len(partners)} unique):')
for p in partners:
    print(f'  - {p[0]}')

conn.close()
