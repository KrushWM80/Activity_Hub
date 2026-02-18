import sqlite3

conn = sqlite3.connect('projects_cache.db')
cursor = conn.cursor()

# Check if columns exist
cursor.execute('PRAGMA table_info(projects)')
columns = [row[1] for row in cursor.fetchall()]
print('Columns in projects table:')
print(columns)
print()

# Check if business_area and store_area have data
cursor.execute('SELECT COUNT(*) FROM projects WHERE business_area IS NOT NULL AND business_area != ""')
ba_count = cursor.fetchone()[0]
print(f'Rows with business_area: {ba_count:,}')

cursor.execute('SELECT COUNT(*) FROM projects WHERE store_area IS NOT NULL AND store_area != ""')
sa_count = cursor.fetchone()[0]
print(f'Rows with store_area: {sa_count:,}')

cursor.execute('SELECT COUNT(*) FROM projects WHERE owner IS NOT NULL AND owner != ""')
owner_count = cursor.fetchone()[0]
print(f'Rows with owner: {owner_count:,}')
print()

# Sample values
cursor.execute('SELECT project_id, title, business_area, store_area, owner FROM projects WHERE business_area IS NOT NULL AND business_area != "" LIMIT 5')
print('Sample projects with business_area:')
for row in cursor.fetchall():
    print(f'  {row[0]}: {row[1][:30]}... | BA: {row[2]} | SA: {row[3]} | Owner: {row[4]}')

conn.close()
