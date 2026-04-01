"""Test the SQLite cache query for Realty records"""
import sqlite3

db_path = 'projects_cache.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Test 1: Total Realty records
cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty'")
total_realty = cursor.fetchone()[0]
print(f"Total Realty records: {total_realty}")

# Test 2: Realty records with non-null project_id
cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty' AND project_id IS NOT NULL AND project_id != ''")
realty_valid = cursor.fetchone()[0]
print(f"Realty with valid project_id: {realty_valid}")

# Test 3: Run the exact cache query for Realty
query = """
    SELECT DISTINCT project_id, intake_card, title, project_source, division, region,
           market, store, facility, phase, wm_week, fy, status, 
           owner, partner, store_area, business_area, health, 
           business_type, associate_impact, customer_impact, last_updated
    FROM projects
    WHERE project_source = 'Realty'
      AND project_id IS NOT NULL
      AND project_id != ''
    ORDER BY title, wm_week
    LIMIT 50000
"""

cursor.execute(query)
rows = cursor.fetchall()
print(f"Cache query returns: {len(rows)} records")

# Test 4: Show sample distinct project_ids
cursor.execute("""
    SELECT DISTINCT project_id, COUNT(*) as cnt 
    FROM projects 
    WHERE project_source = 'Realty' 
      AND project_id IS NOT NULL 
      AND project_id != ''
    GROUP BY project_id
    ORDER BY cnt DESC
    LIMIT 10
""")
print(f"\nTop 10 project_ids by frequency:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} records")

conn.close()
