#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from google.cloud import bigquery

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

try:
    client = bigquery.Client()
    
    query = """
    SELECT DISTINCT
        CAST(worker_id AS STRING) as worker_id,
        first_name,
        last_name,
        job_code,
        job_nm,
        worker_payment_type,
        CAST(location_id AS STRING) as location_id,
        location_nm,
        hire_date,
        empl_type_code
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE job_code = '30-49-855'
      AND worker_payment_type IN ('H', 'S')
    ORDER BY location_id, worker_id
    LIMIT 500
    """
    
    print("=" * 100)
    print("QUERYING JOB CODE 30-49-855 FOR PAY TYPES H AND S")
    print("=" * 100)
    print()
    
    results = client.query(query).result()
    rows = list(results)
    
    if rows:
        print(f"FOUND {len(rows)} EMPLOYEES")
        print()
        print("=" * 100)
        for row in rows:
            print(f"Worker ID: {row.worker_id}")
            print(f"  Name: {row.first_name} {row.last_name}")
            print(f"  Job Code: {row.job_code} - {row.job_nm}")
            print(f"  Pay Type: {row.worker_payment_type}")
            print(f"  Location: {row.location_nm} (ID: {row.location_id})")
            print(f"  Hire Date: {row.hire_date}")
            print(f"  Employment Type: {row.empl_type_code}")
            print()
    else:
        print("NO H/S EMPLOYEES FOUND")
        print()
        print("Checking what pay types exist for job code 30-49-855...")
        print()
        
        alt_query = """
        SELECT 
            worker_payment_type,
            COUNT(*) as employee_count
        FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
        WHERE job_code = '30-49-855'
        GROUP BY worker_payment_type
        ORDER BY employee_count DESC
        """
        
        alt_results = client.query(alt_query).result()
        alt_rows = list(alt_results)
        
        if alt_rows:
            print("PAY TYPES AVAILABLE FOR 30-49-855:")
            print("=" * 40)
            for row in alt_rows:
                print(f"  {row.worker_payment_type}: {row.employee_count} employees")
        else:
            print("Job code 30-49-855 NOT FOUND in Polaris data")
            
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
