"""Check cache contents"""
import sqlite3

db = sqlite3.connect('projects_cache.db')
c = db.cursor()

# Get counts
c.execute("SELECT COUNT(*) FROM projects")
total = c.fetchone()[0]

c.execute("SELECT COUNT(DISTINCT project_source) FROM projects")
sources_count = c.fetchone()[0]

c.execute("SELECT DISTINCT project_source, COUNT(*) FROM projects GROUP BY project_source")
sources = c.fetchall()

c.execute("SELECT COUNT(DISTINCT project_id) FROM projects")  
unique_ids = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty'")
realty = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Operations'")
ops = c.fetchone()[0]

print(f"Total records: {total}")
print(f"Unique project_ids: {unique_ids}")
print(f"Unique sources: {sources_count}")
for src, cnt in sources:
    print(f"  {src}: {cnt}")

# Test the actual cache query
print("\nTesting cache query (no filter):")
c.execute("""
    SELECT DISTINCT project_id, intake_card, title, project_source, division, region,
           market, store, facility, phase, wm_week, fy, status, 
           owner, partner, store_area, business_area, health, 
           business_type, associate_impact, customer_impact, last_updated
    FROM projects
    WHERE 1=1
      AND project_id IS NOT NULL
      AND project_id != ''
    ORDER BY title, wm_week
    LIMIT 50000
""")
rows = c.fetchall()
print(f"Query returned: {len(rows)} records")
if rows:
    print(f"First row project_source: {rows[0][3]}")

# Test with Realty filter
print("\nTesting cache query (Realty filter):")
c.execute("""
    SELECT DISTINCT project_id, intake_card, title, project_source FROM projects
    WHERE project_source = 'Realty'
      AND project_id IS NOT NULL
      AND project_id != ''
    ORDER BY title
    LIMIT 50
""")
rows = c.fetchall()
print(f"Query returned: {len(rows)} Realty records")

db.close()
