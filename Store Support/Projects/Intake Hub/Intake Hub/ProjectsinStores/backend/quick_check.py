import sqlite3
conn = sqlite3.connect('projects_cache.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM projects')
total = c.fetchone()[0]
print(f'Total records: {total}')
if total > 0:
    c.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty' AND project_id IS NOT NULL")
    r_with_id = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty'")
    r_total = c.fetchone()[0]
    print(f'Realty: {r_with_id}/{r_total} with project_id')
    c.execute("SELECT project_id, facility, title FROM projects WHERE project_id LIKE 'FAC-%' LIMIT 2")
    for row in c.fetchall():
        print(f'\nSample FAC: {row[0]}, facility={row[1]}, title={row[2][:40]}')
conn.close()
