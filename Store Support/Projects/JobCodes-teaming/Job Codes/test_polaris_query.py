#!/usr/bin/env python3
"""Test Polaris query"""

from google.cloud import bigquery

client = bigquery.Client()

# Test 1: Check if Polaris dataset is accessible
query1 = """
SELECT job_code, worker_id, first_name, last_name
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
LIMIT 5
"""

print("=" * 80)
print("Test 1: Basic Polaris query")
print("=" * 80)

try:
    results = client.query(query1).result()
    rows = list(results)
    print(f"SUCCESS! Found {len(rows)} rows")
    for row in rows:
        print(f"  {dict(row)}")
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e).__name__}")

print()

# Test 2: Query for specific job codes from existing data
query2 = """
SELECT DISTINCT job_code, worker_id, first_name, last_name, job_nm
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code IN ('1-993-1026', '1-993-3001', '1-993-1085')
LIMIT 10
"""

print("=" * 80)
print("Test 2: Query for specific job codes (including missing ones)")
print("=" * 80)

try:
    results = client.query(query2).result()
    rows = list(results)
    print(f"SUCCESS! Found {len(rows)} rows")
    for row in rows:
        print(f"  {dict(row)}")
except Exception as e:
    print(f"ERROR: {e}")
    print()
    print("If this is a permission error, you may not have access to Polaris.")
    print("Try using a different dataset instead.")
