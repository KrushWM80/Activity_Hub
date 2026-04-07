#!/usr/bin/env python3
import sqlite3
import os

db_path = "cache/jobcodes_cache.db"

if not os.path.exists(db_path):
    print(f"Cache database not found at: {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check job codes
    cursor.execute("SELECT COUNT(*) FROM polaris_job_codes")
    job_code_count = cursor.fetchone()[0]
    print(f"✓ Polaris job codes in cache: {job_code_count}")
    
    # Check master data
    cursor.execute("SELECT COUNT(*) FROM job_code_master")
    master_count = cursor.fetchone()[0]
    print(f"✓ Job code master records: {master_count}")
    
    # Sample data
    cursor.execute("SELECT job_code, job_nm, user_count FROM polaris_job_codes LIMIT 5")
    rows = cursor.fetchall()
    print(f"\n✓ Sample data:")
    for job_code, job_nm, user_count in rows:
        print(f"  {job_code}: {job_nm} (users: {user_count})")
    
    conn.close()
    print("\n✓ Cache database is healthy!")
    
except Exception as e:
    print(f"✗ Error accessing cache: {e}")
