import sqlite3

try:
    conn = sqlite3.connect('projects_cache.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get counts
    cursor.execute("SELECT COUNT(*) as count FROM projects")
    total = cursor.fetchone()['count']
    
    cursor.execute("SELECT project_source, COUNT(*) as count FROM projects GROUP BY project_source")
    sources = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT project_id FROM projects WHERE project_source='Realty' LIMIT 10")
    sample_ids = cursor.fetchall()
    
    print(f"Total records: {total}")
    print(f"\nBy source:")
    for row in sources:
        print(f"  {row['project_source']}: {row['count']}")
    
    print(f"\nSample Realty project_ids:")
    for row in sample_ids:
        print(f"  {row['project_id']}")
    
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
