#!/usr/bin/env python3
"""Check Realty data issue - missing last_updated"""

import sqlite3

db_path = 'projects_cache.db'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=== REALTY DATA INVESTIGATION ===\n")
    
    # Check how many Realty rows have NULL last_updated
    cursor.execute("""
        SELECT COUNT(*) as null_count, COUNT(*) as total_count
        FROM projects
        WHERE project_source = 'Realty'
        AND last_updated IS NULL
    """)
    null_count, total = cursor.fetchone()
    print(f"Realty records with NULL last_updated: {null_count} out of 1,273,272")
    
    # Check a few Realty records
    print("\nSample Realty records:")
    cursor.execute("""
        SELECT project_id, title, last_updated 
        FROM projects
        WHERE project_source = 'Realty'
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Title: {row[1][:40]}, Updated: {row[2]}")
    
    # Check Operations records for comparison
    print("\nSample Operations records:")
    cursor.execute("""
        SELECT project_id, title, last_updated 
        FROM projects
        WHERE project_source = 'Operations'
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Title: {row[1][:40]}, Updated: {row[2]}")
    
    # Check if there's a difference in how data was loaded
    print("\n=== DATA LOAD PATTERN ===")
    cursor.execute("""
        SELECT project_source, 
               COUNT(DISTINCT intake_card) as distinct_intake_cards,
               COUNT(*) as total_records
        FROM projects
        GROUP BY project_source
    """)
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]:,} intake cards, {row[2]:,} total records")
    
    conn.close()
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
