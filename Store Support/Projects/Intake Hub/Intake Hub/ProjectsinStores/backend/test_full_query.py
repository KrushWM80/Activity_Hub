import sqlite3
import json

conn = sqlite3.connect('projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Test the GROUP BY query with all filters
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
    WHERE project_id IS NOT NULL AND project_id != ''
    GROUP BY project_id, project_source
    ORDER BY title, wm_week
    LIMIT 500
"""

try:
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"Query successful: {len(rows)} rows")
    
    # Try to build dictionaries like the code does
    projects = []
    for row in rows:
        p = {
            'project_id': row['project_id'],
            'intake_card': row['intake_card'],
            'title': row['title'],
            'project_source': row['project_source'],
            'division': row['division'],
            'region': row['region'],
            'market': row['market'],
            'store': row['store'],
            'facility': row['facility'],
            'phase': row['phase'],
            'wm_week': row['wm_week'],
            'fy': row['fy'],
            'status': row['status'],
            'store_count': 1,
            'owner': row['owner'],
            'partner': row['partner'],
            'store_area': row['store_area'],
            'business_area': row['business_area'],
            'health': row['health'],
            'business_type': row['business_type'],
            'associate_impact': row['associate_impact'],
            'customer_impact': row['customer_impact'],
            'last_updated': row['last_updated']
        }
        projects.append(p)
    
    print(f"Built {len(projects)} project dicts")
    
    # Try to JSON serialize (like the API does)
    json_str = json.dumps(projects)
    print(f"JSON serialization successful: {len(json_str)} bytes")
    
    if projects:
        print(f"\nFirst project:\n{json.dumps(projects[0], indent=2)}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

conn.close()
