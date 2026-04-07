#!/usr/bin/env python3
"""Test database connectivity and integrity."""

import sqlite3
import os

db_path = "projects_cache.db"
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM projects")
        count = cursor.fetchone()[0]
        print(f"[CHECK] Database is accessible. Total records: {count}")
        conn.close()
    except Exception as e:
        print(f"[ERROR] Database check failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"[ERROR] Database file not found at {db_path}")
