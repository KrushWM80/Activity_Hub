#!/usr/bin/env python3
"""Check if job code 30-49-855 exists in Polaris"""
from google.cloud import bigquery

client = bigquery.Client()

# First: Count total records for this job code
print("\n" + "=" * 100)
print("CHECKING IF JOB CODE 30-49-855 EXISTS IN POLARIS")
print("=" * 100)

query1 = '''
SELECT COUNT(*) as total_count
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code = '30-49-855'
'''

try:
    result = list(client.query(query1).result())[0]
    print(f"\nTotal records with job code 30-49-855: {result.total_count}")
    
    if result.total_count == 0:
        print("⚠️  No records found - checking similar job codes...")
        
        # Check for jobs starting with 30-49
        query2 = '''
        SELECT DISTINCT job_code, job_nm, COUNT(*) as count
        FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
        WHERE job_code LIKE '30-49-%'
        GROUP BY job_code, job_nm
        ORDER BY job_code
        LIMIT 20
        '''
        
        results = client.query(query2).result()
        rows = list(results)
        
        if rows:
            print(f"\nFound {len(rows)} similar job codes starting with '30-49-':")
            print("-" * 100)
            for row in rows:
                print(f"  {row.job_code:20s} | {row.job_nm:40s} | {row.count:6d} records")
        else:
            print("No job codes found starting with '30-49-'")
    else:
        # Show pay type distribution
        query3 = '''
        SELECT worker_payment_type, COUNT(*) as count
        FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
        WHERE job_code = '30-49-855'
        GROUP BY worker_payment_type
        '''
        
        results = client.query(query3).result()
        rows = list(results)
        
        print(f"\nPay Type Distribution for job code 30-49-855:")
        print("-" * 100)
        for row in rows:
            print(f"  {row.worker_payment_type:10s}: {row.count:6d} records")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
