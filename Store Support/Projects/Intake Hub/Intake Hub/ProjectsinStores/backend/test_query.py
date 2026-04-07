import sqlite3

conn = sqlite3.connect('projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Test the new GROUP BY query
query = """
    SELECT 
        project_id, 
        MIN(intake_card) as intake_card, 
        MIN(title) as title, 
        project_source, 
        MIN(division) as division, 
        MIN(region) as region,
        MIN(market) as market, 
        MIN(store) as store, 
        MIN(facility) as facility, 
        MIN(phase) as phase, 
        MIN(wm_week) as wm_week, 
        MIN(fy) as fy, 
        MIN(status) as status,
        MIN(owner) as owner, 
        MIN(partner) as partner, 
        MIN(store_area) as store_area, 
        MIN(business_area) as business_area, 
        MIN(health) as health,
        MIN(business_type) as business_type, 
        MIN(associate_impact) as associate_impact, 
        MIN(customer_impact) as customer_impact, 
        MAX(last_updated) as last_updated
    FROM projects
    WHERE project_source = 'Realty'
    GROUP BY project_id, project_source
    ORDER BY title, wm_week
    LIMIT 10
"""

try:
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"SUCCESS: Query returned {len(rows)} rows")
    if rows:
        print(f"First row keys: {list(rows[0].keys())}")
        print(f"First row: {dict(rows[0])}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

conn.close()
