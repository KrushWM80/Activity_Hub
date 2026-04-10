#!/usr/bin/env python3
"""Check current data state and operations count"""

import sqlite3
from datetime import datetime

db_path = 'projects_cache.db'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=== CURRENT DATA STATE ===\n")
    
    # Check Operations count
    print("1. Operations Projects (by query logic):")
    cursor.execute("""
        SELECT COUNT(DISTINCT title) as distinct_titles, 
               COUNT(DISTINCT project_id) as distinct_ids,
               COUNT(*) as total_rows
        FROM projects
        WHERE project_source = 'Operations'
        AND status = 'Active'
    """)
    row = cursor.fetchone()
    print(f"  Distinct Titles (GROUP BY title): {row[0]}")
    print(f"  Distinct Project IDs (GROUP BY project_id): {row[1]}")
    print(f"  Total Raw Rows: {row[2]}")
    
    # Check Realty count
    print("\n2. Realty Projects (by query logic):")
    cursor.execute("""
        SELECT COUNT(DISTINCT title) as distinct_titles,
               COUNT(DISTINCT project_id) as distinct_ids,
               COUNT(*) as total_rows
        FROM projects
        WHERE project_source = 'Realty'
        AND status = 'Active'
    """)
    row = cursor.fetchone()
    print(f"  Distinct Titles (GROUP BY title): {row[0]}")
    print(f"  Distinct Project IDs (GROUP BY project_id): {row[1]}")
    print(f"  Total Raw Rows: {row[2]}")
    
    # Check latest timestamp
    print("\n3. Data Timestamps:")
    cursor.execute("""
        SELECT project_source, 
               MAX(last_updated) as latest,
               MIN(last_updated) as oldest,
               COUNT(DISTINCT last_updated) as unique_timestamps
        FROM projects
        WHERE status = 'Active'
        GROUP BY project_source
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}:")
        print(f"    Latest: {row[1]}")
        print(f"    Oldest: {row[2]}")
        print(f"    Unique timestamps: {row[3]}")
    
    # Check if there are any non-Active status
    print("\n4. All Status Values:")
    cursor.execute("""
        SELECT project_source, status, COUNT(*) as count
        FROM projects
        GROUP BY project_source, status
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]} - {row[1]}: {row[2]}")
    
    # Check database size/modification time
    import os
    db_stat = os.path.stat(db_path)
    mod_time = datetime.fromtimestamp(db_stat.st_mtime)
    print(f"\n5. Database File Info:")
    print(f"  Last modified: {mod_time}")
    print(f"  Size: {db_stat.st_size:,} bytes")
    
    conn.close()
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
