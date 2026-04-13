#!/usr/bin/env python3
"""
Query CoreHR UNIFIED_PROFILE_SENSITIVE_VW for job code definitions with paytype
"""

from google.cloud import bigquery
import os

# Set up BigQuery client
client = bigquery.Client(project='wmt-assetprotection-prod')

# Sample of job codes to test - including the problematic '1-993-1001'
test_codes = [
    '1-993-1001', '1-993-3001', '1-993-1071', '1-993-1026',  # Store Manager group
    '1-910-7250',  # HR Personnel
    '1-600-7200', '1-600-7220',  # Supervisors example
]

# First, let's explore the table structure
print("=" * 80)
print("TESTING: wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW")
print("=" * 80)

query = f"""
SELECT DISTINCT
    job_code,
    job_title,
    worker_payment_type,
    COUNT(*) as employee_count
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
WHERE job_code IN ({', '.join([f"'{code}'" for code in test_codes])})
GROUP BY job_code, job_title, worker_payment_type
ORDER BY job_code
"""

print("\nQuery:")
print(query)
print("\nExecuting...")

try:
    job_config = bigquery.QueryJobConfig(
        maximum_bytes_billed=1000000000  # 1GB limit for testing
    )
    query_job = client.query(query, job_config=job_config)
    results = query_job.result(timeout=60)
    
    print(f"\n✅ SUCCESS - Found {results.total_rows} rows\n")
    
    for row in results:
        print(f"Code: {row['job_code']:15} | Title: {row['job_title']:40} | Paytype: {row['worker_payment_type']:10} | Employees: {row['employee_count']}")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print(f"\nError Type: {type(e).__name__}")
