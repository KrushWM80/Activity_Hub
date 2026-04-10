#!/usr/bin/env python3
"""Check what projects are in the database"""

from sqlite3 import connect

db_path = 'projects_cache.db'
conn = connect(db_path)
cursor = conn.cursor()

print("=== CHECKING SAMPLE PROJECTS ===\n")

# Check for "Store Renovation" projects
print("1. Store Renovation Projects:")
cursor.execute("""
    SELECT DISTINCT title, project_source, COUNT(*) as count
    FROM projects
    WHERE title LIKE '%Store Renovation%'
    GROUP BY title, project_source
    ORDER BY title
""")
for row in cursor.fetchall():
    print(f"   {row[0]} ({row[1]}): {row[2]} records")

# Check for "Project 1", "Project 10", "Project 11"
print("\n2. 'Project N' pattern matches:")
cursor.execute("""
    SELECT DISTINCT title, project_source, COUNT(*) as count
    FROM projects
    WHERE title LIKE 'Project %'
    GROUP BY title, project_source
    ORDER BY title
""")
for row in cursor.fetchall():
    print(f"   {row[0]} ({row[1]}): {row[2]} records")

# Check top 20 projects by volume
print("\n3. Top 20 projects by store count:")
cursor.execute("""
    SELECT title, project_source, COUNT(*) as store_count
    FROM projects
    WHERE status = 'Active'
    GROUP BY title, project_source
    ORDER BY store_count DESC
    LIMIT 20
""")
for row in cursor.fetchall():
    print(f"   {row[0]} ({row[1]}): {row[2]} stores")

# Check for intake_card patterns
print("\n4. Check intake_card values:")
cursor.execute("""
    SELECT intake_card, COUNT(*) as count
    FROM projects
    WHERE title LIKE '%Store Renovation%'
    GROUP BY intake_card
""")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} records")

conn.close()
