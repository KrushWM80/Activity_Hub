#!/usr/bin/env python3
"""Check sync health and error logs"""

import sqlite3
from datetime import datetime
import json

db_path = 'projects_cache.db'

try:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=== SYNC HEALTH CHECK ===\n")
    
    # Check sync_metadata
    print("1. Sync Metadata (Last Sync Records):")
    cursor.execute("""
        SELECT * FROM sync_metadata 
        ORDER BY last_sync_time DESC 
        LIMIT 5
    """)
    metadata = cursor.fetchall()
    for row in metadata:
        print(f"  Source: {row['source_name']}")
        print(f"  Last Sync: {row['last_sync_time']}")
        print(f"  Records Synced: {row['records_synced']}")
        print(f"  Status: {row['sync_status']}")
        print()
    
    # Check sync_error_log
    print("2. Sync Error Log (Last 10 Errors):")
    cursor.execute("""
        SELECT * FROM sync_error_log 
        ORDER BY error_time DESC 
        LIMIT 10
    """)
    errors = cursor.fetchall()
    if errors:
        for row in errors:
            print(f"  Time: {row['error_time']}")
            print(f"  Source: {row['source_name']}")
            print(f"  Error: {row['error_message'][:100]}...")
            print()
    else:
        print("  No errors logged\n")
    
    # Check total records in projects table
    print("3. Current Project Counts in Cache:")
    cursor.execute("""
        SELECT project_source, COUNT(*) as count, MAX(last_updated) as latest
        FROM projects
        WHERE status = 'Active'
        GROUP BY project_source
    """)
    for row in cursor.fetchall():
        print(f"  {row['project_source']}: {row['count']} projects, latest: {row['latest']}")
    
    # Check Operations specifically
    print("\n4. Operations Projects Detail:")
    cursor.execute("""
        SELECT COUNT(*) as total_operations
        FROM projects
        WHERE project_source = 'Operations'
        AND status = 'Active'
    """)
    ops_count = cursor.fetchone()['total_operations']
    print(f"  Total Active Operations: {ops_count}")
    
    cursor.execute("""
        SELECT COUNT(DISTINCT project_id) as distinct_ids
        FROM projects
        WHERE project_source = 'Operations'
        AND status = 'Active'
    """)
    distinct = cursor.fetchone()['distinct_ids']
    print(f"  Distinct Project IDs: {distinct}")
    
    cursor.execute("""
        SELECT COUNT(DISTINCT title) as distinct_titles
        FROM projects
        WHERE project_source = 'Operations'
        AND status = 'Active'
    """)
    titles = cursor.fetchone()['distinct_titles']
    print(f"  Distinct Titles: {titles}")
    
    # Check if background sync is even running
    print("\n5. Background Sync Status:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sync_log'")
    has_sync_log = cursor.fetchone() is not None
    print(f"  Sync log table exists: {has_sync_log}")
    
    conn.close()
    
except Exception as e:
    print(f"ERROR: {e}")
