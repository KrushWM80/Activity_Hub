#!/usr/bin/env python3
"""
Query Polaris for users with specific job code and pay type
Job Code: 30-49-855
Pay Types: H (Hourly), S (Salary)
"""
from google.cloud import bigquery
import pandas as pd

# Use default client (no project specified)
client = bigquery.Client()

query = '''
SELECT DISTINCT
    worker_id,
    first_name,
    last_name,
    job_code,
    job_nm,
    worker_payment_type,
    location_id,
    location_nm,
    hire_date
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code = '30-49-855'
  AND worker_payment_type IN ('H', 'S')
ORDER BY worker_id
LIMIT 500
'''

try:
    print("\n" + "=" * 120)
    print("POLARIS JOB CODE LOOKUP: 30-49-855 (Pay Types: H=Hourly, S=Salary)")
    print("=" * 120)
    
    results = client.query(query).result()
    df = pd.DataFrame([dict(row) for row in results])
    
    if df.empty:
        print("\n❌ No results found for job code 30-49-855 with pay type H or S")
    else:
        print(f"\n✓ SUCCESS! Found {len(df)} user records\n")
        
        # Display results
        print(df[['worker_id', 'first_name', 'last_name', 'worker_payment_type', 'location_nm']].to_string(index=False))
        
        print("\n" + "=" * 120)
        print("SUMMARY:")
        print("=" * 120)
        
        # Summary by pay type
        pay_type_summary = df.groupby('worker_payment_type')['worker_id'].count()
        for pay_type, count in pay_type_summary.items():
            print(f"  {pay_type} (Pay Type): {count} employees")
        
        print(f"\n  TOTAL: {len(df)} employees with job code 30-49-855")
        print("=" * 120)
        
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}")
    print(f"   {e}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
