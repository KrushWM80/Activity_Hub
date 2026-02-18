"""
Extract unique worker details (Worker ID and Store) for specific Job Codes from BigQuery
"""
from google.cloud import bigquery
import pandas as pd

# Initialize BigQuery client
client = bigquery.Client()

# Job codes to query
job_codes = ['1-16-101', '1-993-1076']

# SQL query to get unique worker and store information
query = """
SELECT 
    DISTINCT
    worker_id,
    location_nm as store_number,
    job_code,
    job_nm
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code IN ('1-16-101', '1-993-1076')
ORDER BY job_code, store_number, worker_id
"""

print("Querying BigQuery for worker details...")
print(f"Job Codes: {', '.join(job_codes)}")
print()

try:
    # Execute query
    query_job = client.query(query)
    results = list(query_job.result())
    
    # Convert to DataFrame
    rows_list = [dict(row) for row in results]
    df = pd.DataFrame(rows_list)
    
    print(f"Found {len(df)} unique worker-store-jobcode combinations")
    print()
    
    # Save to CSV
    output_file = r"C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\Worker_Store_JobCodes.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved results to: {output_file}")
    
    # Display summary
    print("\n" + "="*80)
    print("SUMMARY BY JOB CODE")
    print("="*80)
    
    for jc in job_codes:
        jc_data = df[df['job_code'] == jc]
        if len(jc_data) > 0:
            job_name = jc_data['job_nm'].iloc[0]
            unique_workers = jc_data['worker_id'].nunique()
            unique_stores = jc_data['store_number'].nunique()
            
            print(f"\nJob Code: {jc}")
            print(f"Job Title: {job_name}")
            print(f"Unique Workers: {unique_workers}")
            print(f"Unique Stores: {unique_stores}")
            print(f"Total Records: {len(jc_data)}")
            
            # Show sample
            print(f"\nSample data (first 15 workers):")
            print(jc_data[['worker_id', 'store_number', 'job_code']].head(15).to_string(index=False))
    
    print("\n" + "="*80)
    print(f"COMPLETE RESULTS SAVED TO: {output_file}")
    print("="*80)
    
    # Additional note about names
    print("\nNOTE: The Polaris schedule view does not contain worker names (first/last name).")
    print("To get worker names, you would need to:")
    print("1. Query a different BigQuery table that contains employee master data")
    print("2. Use the worker_id values to look up names in an HR system")
    print("3. Join with another table like employee master or worker profile table")
    
except Exception as e:
    import traceback
    print(f"Error querying BigQuery: {e}")
    print(f"\nFull traceback:")
    traceback.print_exc()
