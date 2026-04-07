"""
Comprehensive cache validation and debugging script
Tests sqlite_cache.py methods directly to ensure they work correctly
"""
import sys
import sqlite3
from sqlite_cache import SQLiteCache, get_cache

print("="*60)
print("CACHE VALIDATION & DEBUG REPORT")
print("="*60)

try:
    # Initialize cache the same way main.py does
    cache = get_cache()
    print("\n[OK] SQLiteCache initialized successfully")
    
    # Test 1: Record count
    print("\n--- TEST 1: Record Count ---")
    count = cache.get_record_count()
    print(f"Total records in cache: {count:,}")
    if count == 0:
        print("[WARN] Cache is empty!")
    elif count > 1000000:
        print("[OK] Cache has expected volume of data")
    
    # Test 2: Get projects without filters
    print("\n--- TEST 2: Get Projects (No Filters) ---")
    projects = cache.get_projects(limit=10)
    print(f"Retrieved {len(projects)} projects")
    if projects:
        p = projects[0]
        print(f"\nFirst project:")
        print(f"  ID: {p.get('project_id')}")
        print(f"  Source: {p.get('project_source')}")
        print(f"  Title: {p.get('title')}")
        print(f"  Keys in dict: {list(p.keys())}")
        if 'partner' in p:
            print(f"  [OK] 'partner' field present: {p['partner']}")
        else:
            print(f"  [WARN] 'partner' field MISSING")
    
    # Test 3: Get Realty projects
    print("\n--- TEST 3: Get Realty Projects ---")
    realty_projects = cache.get_projects(
        filters={'project_source': 'Realty'},
        limit=5
    )
    print(f"Retrieved {len(realty_projects)} Realty projects")
    if realty_projects:
        for i, p in enumerate(realty_projects):
            print(f"  {i+1}. {p.get('project_id')}: {p.get('title')}")
    
    # Test 4: Get Operations projects  
    print("\n--- TEST 4: Get Operations Projects ---")
    ops_projects = cache.get_projects(
        filters={'project_source': 'Operations'},
        limit=5
    )
    print(f"Retrieved {len(ops_projects)} Operations projects")
    if ops_projects:
        for i, p in enumerate(ops_projects):
            print(f"  {i+1}. {p.get('project_id')}: {p.get('title')}")
    
    # Test 5: Summary
    print("\n--- TEST 5: Summary Stats ---")
    try:
        summary = cache.get_summary()
        print(f"Summary keys: {list(summary.keys())}")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"[WARN] Error getting summary: {e}")
    
    # Test 6: Direct SQL test
    print("\n--- TEST 6: Direct SQL Query Test ---")
    conn = sqlite3.connect('projects_cache.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # List columns to verify structure
    cursor.execute("PRAGMA table_info(projects)")
    columns = [row['name'] for row in cursor.fetchall()]
    print(f"Database columns ({len(columns)}):")
    print(f"  {', '.join(columns)}")
    
    # Test query
    cursor.execute("""
        SELECT COUNT(*) as count FROM projects 
        WHERE project_source = 'Realty' AND project_id IS NOT NULL
    """)
    realty_count = cursor.fetchone()['count']
    print(f"\nRealty records with non-NULL project_id: {realty_count:,}")
    
    cursor.execute("""
        SELECT project_id, title FROM projects
        WHERE project_source = 'Realty' AND project_id IS NOT NULL
        LIMIT 5
    """)
    print(f"Sample Realty IDs:")
    for row in cursor.fetchall():
        print(f"  {row['project_id']}: {row['title']}")
    
    conn.close()
    
    print("\n" + "="*60)
    print("VALIDATION COMPLETE")
    print("="*60)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
