import sqlite3

db_path = 'projects_cache.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get table schema
cursor.execute("PRAGMA table_info(projects)")
columns = cursor.fetchall()
print("Columns in projects table:")
for col in columns:
    print(f"  {col[1]:<30} {col[2]}")

conn.close()
