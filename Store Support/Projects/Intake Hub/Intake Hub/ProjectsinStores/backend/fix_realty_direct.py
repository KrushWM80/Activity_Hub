"""Fix NULL project_id for Realty records directly in SQLite"""
import sqlite3
import os

db_path = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db'

print("🔧 Fixing Realty project_id values directly in SQLite...\n")

# First, delete the problematic cache and use the snapshot if available
snapshot_path = os.path.join(os.path.dirname(db_path), 'snapshots', 'last_good_sync.json')
if os.path.exists(snapshot_path):
    print(f"Found snapshot at {snapshot_path}")
    print("Restoring from snapshot...")
    
    import json
    import shutil
    
    # Restore from snapshot
    with open(snapshot_path, 'r') as f:
        data = json.load(f)
    
    # Delete current database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Recreate database from snapshot
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT,
            intake_card TEXT,
            title TEXT,
            project_source TEXT,
            division TEXT,
            region TEXT,
            market TEXT,
            store TEXT,
            facility TEXT,
            phase TEXT,
            wm_week INTEGER,
            fy INTEGER,
            status TEXT,
            owner TEXT,
            partner TEXT,
            store_area TEXT,
            business_area TEXT,
            health TEXT,
            business_type TEXT,
            associate_impact TEXT,
            customer_impact TEXT,
            last_updated TEXT
        )
    """)
    
    # Insert data from snapshot
    for record in data:
        # Calculate project_id for Realty records
        if record.get('project_source') == 'Realty' and record.get('project_id') is None:
            # Use FAC- prefix for Realty
            record['project_id'] = f"FAC-{record.get('facility', 'UNKNOWN')}"
        
        cursor.execute("""
            INSERT INTO projects (
                project_id, intake_card, title, project_source, division, region,
                market, store, facility, phase, wm_week, fy, status, owner, partner,
                store_area, business_area, health, business_type, associate_impact,
                customer_impact, last_updated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.get('project_id'),
            record.get('intake_card'),
            record.get('title'),
            record.get('project_source'),
            record.get('division'),
            record.get('region'),
            record.get('market'),
            record.get('store'),
            record.get('facility'),
            record.get('phase'),
            record.get('wm_week'),
            record.get('fy'),
            record.get('status'),
            record.get('owner'),
            record.get('partner'),
            record.get('store_area'),
            record.get('business_area'),
            record.get('health'),
            record.get('business_type'),
            record.get('associate_impact'),
            record.get('customer_impact'),
            record.get('last_updated')
        ))
    
    conn.commit()
    
    # Check results
    cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty' AND project_id IS NOT NULL")
    realty_with_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty'")
    total_realty = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n✅ Fixed cache!")
    print(f"   Realty with project_id: {realty_with_id:,} / {total_realty:,}")
else:
    print(f"No snapshot found at {snapshot_path}")
    print("Snapshot would be used to restore data in case of sync failure.")
    print("\nTrying alternative: checking if OLD cache database exists as backup...")
    
    # Check if there's a projects_cache.db file
    if os.path.exists(db_path):
        print(f"Using existing cache at {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if it has tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        if tables:
            print(f"Found tables: {[t[0] for t in tables]}")
        else:
            print("Database is empty")
        
        conn.close()
