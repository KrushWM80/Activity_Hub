#!/usr/bin/env python3
"""
Search Polaris with default project credentials
"""
from google.cloud import bigquery

client = bigquery.Client()  # Use default project from credentials

print('='*80)
print('SEARCHING POLARIS FOR KATHLEEN REED - STORE 30')
print('='*80)
print(f'Using project: {client.project}')
print()

try:
    query = """
    SELECT 
        worker_id,
        location_id,
        location_nm,
        first_name,
        last_name,
        job_code,
        job_nm
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE location_id = 30
      AND first_name = 'Kathleen'
      AND last_name = 'Reed'
    LIMIT 10
    """
    
    print("Querying Polaris for Kathleen Reed in Store 30...")
    results = client.query(query, timeout=60).result()
    rows = list(results)
    
    if rows:
        print(f"\n✓ FOUND {len(rows)} record(s)!\n")
        for row in rows:
            print(f"Name: {row.first_name} {row.last_name}")
            print(f"  👤 User Name (Worker ID): {row.worker_id}")
            print(f"  📋 Job Code: {row.job_code}")
            print(f"  💼 Job Title: {row.job_nm}")
            print(f"  🏪 Store: {row.location_nm} (ID: {row.location_id})")
            print("-"*80)
    else:
        print("✗ No exact match found")
        print("\nTrying with LIKE search...")
        
        query2 = """
        SELECT DISTINCT 
            worker_id,
            first_name,
            last_name,
            job_code,
            job_nm
        FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
        WHERE location_id = 30 
          AND (first_name LIKE '%Kathleen%' OR last_name LIKE '%Reed%')
        LIMIT 20
        """
        
        results2 = client.query(query2, timeout=60).result()
        rows2 = list(results2)
        
        if rows2:
            print(f"\nFound {len(rows2)} potential matches:")
            for row in rows2:
                print(f"{row.first_name:15} {row.last_name:15} | Worker ID: {str(row.worker_id):10} | Job Code: {row.job_code:6} | {row.job_nm}")
        else:
            print("✗ No matches with LIKE either")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
