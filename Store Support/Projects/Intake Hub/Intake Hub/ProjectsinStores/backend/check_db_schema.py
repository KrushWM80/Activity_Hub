#!/usr/bin/env python3
"""Check database schema and sync tables"""

import sqlite3

db_path = 'projects_cache.db'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=== DATABASE SCHEMA ===\n")
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table in tables:
        print(f"  - {table[0]}")
    
    print("\n=== TABLE SCHEMAS ===\n")
    
    for table_name in [t[0] for t in tables]:
        print(f"{table_name}:")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        print()
    
    # Check data in each sync-related table
    print("=== SYNC TABLE DATA ===\n")
    
    for table_name in ['sync_error_log', 'sync_metadata']:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"{table_name}: {count} rows")
        
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            rows = cursor.fetchall()
            for row in rows:
                print(f"  {row}")
        print()
    
    conn.close()
    
except Exception as e:
    print(f"ERROR: {e}")
