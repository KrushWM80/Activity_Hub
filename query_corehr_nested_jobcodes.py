#!/usr/bin/env python3
"""
Query CoreHR UNIFIED_PROFILE_SENSITIVE_VW for job codes using UNNEST for nested structures
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Sample of job codes to test
test_codes = [
    '1-993-1001', '1-993-3001', '1-993-1071', '1-993-1026',
    '1-910-7250',
    '1-600-7200', '1-600-7220',
]

print("=" * 80)
print("TESTING CoreHR with UNNEST for nested job codes")
print("=" * 80)

query = f"""
SELECT DISTINCT
    pos.jobCode as job_code,
    pos.positionTitle as job_title,
    pos.payRateType as paytype,
    COUNT(DISTINCT u.employeeID) as employee_count
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` u
CROSS JOIN UNNEST(u.employmentInfo.positionInfoHistory) as pos
WHERE pos.jobCode IN ({', '.join([f"'{code}'" for code in test_codes])})
GROUP BY pos.jobCode, pos.positionTitle, pos.payRateType
ORDER BY job_code
"""

print("\nQuery:")
print(query)
print("\nExecuting...")

try:
    job_config = bigquery.QueryJobConfig(
        maximum_bytes_billed=1000000000  # 1GB
    )
    query_job = client.query(query, job_config=job_config)
    results = query_job.result(timeout=60)
    
    print(f"\n✅ SUCCESS - Found {results.total_rows} rows\n")
    
    if results.total_rows == 0:
        print("No matches found. These job codes might be in Polaris format, not CoreHR.")
    else:
        for row in results:
            print(f"Code: {row['job_code']:20} | Title: {row['job_title']:40} | Paytype: {row['paytype']:10} | Count: {row['employee_count']}")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print(f"\nError Type: {type(e).__name__}")
