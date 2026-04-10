#!/usr/bin/env python3
"""Check database state - is it real or mock data?"""

from sqlite3 import connect

db_path = 'projects_cache.db'
conn = connect(db_path)
cursor = conn.cursor()

print("=== DATABASE STATE ===\n")

# Show total count
cursor.execute("SELECT COUNT(*) as count FROM projects")
total = cursor.fetchone()[0]
print(f"Total records in DB: {total:,}")

# Show count by source
cursor.execute("""
    SELECT project_source, COUNT(*) as count
    FROM projects
    GROUP BY project_source
""")
print("\nBy source:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

# Show count distinct titles
cursor.execute("SELECT COUNT(DISTINCT title) as count FROM projects")
distinct_titles = cursor.fetchone()[0]
print(f"\nDistinct titles: {distinct_titles}")

# Check what's actually in projects table - sample rows
print("\n\nFirst 10 rows in database:")
cursor.execute("SELECT project_id, title, project_source FROM projects LIMIT 10")
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"  [{i}] {row[1]} ({row[2]})")

# Check for mock data pattern
cursor.execute("""
    SELECT COUNT(*) 
    FROM projects 
    WHERE title LIKE 'Store Renovation Project%'
""")
mock_count = cursor.fetchone()[0]
print(f"\n'Store Renovation Project' count: {mock_count}")

# Check remodel project count
cursor.execute("""
    SELECT COUNT(*) 
    FROM projects 
    WHERE title LIKE 'Remodel%'
""")
remodel_count = cursor.fetchone()[0]
print(f"'Remodel' project count: {remodel_count}")

conn.close()
