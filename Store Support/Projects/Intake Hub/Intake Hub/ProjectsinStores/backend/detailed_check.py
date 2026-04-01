import sqlite3
import os

db_path = 'projects_cache.db'
print(f"Checking {db_path}...")
print(f"Exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    size = os.path.getsize(db_path)
    print(f"Size: {size:,} bytes ({size/1024/1024:.2f} MB)")
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # List tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        print(f"Tables: {tables}")
        
        # Check projects
        c.execute("SELECT COUNT(*) FROM projects")
        total = c.fetchone()[0]
        print(f"Total projects: {total}")
        
        if total > 0:
            c.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty'")
            realty = c.fetchone()[0]
            print(f"Realty: {realty}")
            
            c.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty' AND project_id IS NOT NULL")
            realty_id = c.fetchone()[0]
            print(f"Realty with ID: {realty_id}")
        
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
