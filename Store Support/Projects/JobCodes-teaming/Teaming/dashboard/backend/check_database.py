import sqlite3
import os

db_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\cache\jobcodes_cache.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check a job code that should have enrichment data
job_code_to_check = "1-0-040407"

cursor.execute("""
    SELECT 
        p.job_code,
        p.job_nm,
        m.category,
        m.job_family,
        m.pg_level,
        m.supervisor
    FROM polaris_job_codes p
    LEFT JOIN job_code_master m ON p.job_code = m.job_code
    WHERE p.job_code = ?
""", (job_code_to_check,))

row = cursor.fetchone()
if row:
    print(f"Found job code: {row[0]}")
    print(f"  Job Name: {row[1]}")
    print(f"  Category: {row[2]}")
    print(f"  Job Family: {row[3]}")
    print(f"  PG Level: {row[4]}")
    print(f"  Supervisor: {row[5]}")
else:
    print(f"Job code {job_code_to_check} not found")

# Check how many master records exist
cursor.execute("SELECT COUNT(*) FROM job_code_master")
master_count = cursor.fetchone()[0]
print(f"\nTotal master records in DB: {master_count}")

# Check first master record
cursor.execute("SELECT job_code, category, pg_level FROM job_code_master LIMIT 1")
first_master = cursor.fetchone()
if first_master:
    print(f"First master record: {first_master[0]}, category={first_master[1]}, pg_level={first_master[2]}")

conn.close()
