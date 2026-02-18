"""
Extract worker details with First Name, Last Name, and Store for specific Job Codes from BigQuery
Joins Polaris schedule data with Core HR employee profile data
"""
from google.cloud import bigquery
import pandas as pd

# Initialize BigQuery client
client = bigquery.Client()

# Job codes to query
job_codes = ['1-16-101', '1-993-1076']

# SQL query to get worker details with names
query = """
SELECT DISTINCT
    t1.worker_id,
    t1.win_nbr,
    emp.legalFirstName AS first_name,
    emp.legalLastName AS last_name,
    t1.location_nm AS store_number,
    t1.job_code,
    t1.job_nm
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule` AS t1
LEFT JOIN (
  SELECT DISTINCT 
    employeeID,
    personalInfo.legalFirstName AS legalFirstName,
    personalInfo.legalLastName AS legalLastName
  FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
) AS emp
  ON t1.win_nbr = SAFE_CAST(emp.employeeID AS INT64)
WHERE t1.job_code IN ('1-16-101', '1-993-1076')
ORDER BY t1.job_code, emp.legalLastName, emp.legalFirstName, t1.location_nm
"""

print("Querying BigQuery for worker details with names...")
print(f"Job Codes: {', '.join(job_codes)}")
print("Joining Polaris schedule data with Core HR employee profiles...")
print()

try:
    # Execute query
    print("Executing query (this may take a moment)...")
    query_job = client.query(query)
    results = list(query_job.result())
    
    # Convert to DataFrame
    rows_list = [dict(row) for row in results]
    df = pd.DataFrame(rows_list)
    
    print(f"Found {len(df)} unique worker records")
    print()
    
    # Select only the required columns
    output_columns = ['first_name', 'last_name', 'store_number', 'job_code', 'job_nm']
    df_output = df[output_columns]
    
    # Save to CSV
    output_file = r"C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\Worker_Names_Stores_JobCodes.csv"
    df_output.to_csv(output_file, index=False)
    print(f"✓ Saved results to: {output_file}")
    
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
            
            # Count how many have names
            with_names = jc_data[jc_data['first_name'].notna() & jc_data['last_name'].notna()]
            
            print(f"\nJob Code: {jc}")
            print(f"Job Title: {job_name}")
            print(f"Total Records: {len(jc_data)}")
            print(f"Unique Workers: {unique_workers}")
            print(f"Unique Stores: {unique_stores}")
            print(f"Workers with Names: {len(with_names)} ({len(with_names)/len(jc_data)*100:.1f}%)")
            
            # Show sample with names
            print(f"\nSample data (first 15 workers with names):")
            sample_data = jc_data[jc_data['first_name'].notna()][['first_name', 'last_name', 'store_number', 'job_code']].head(15)
            if len(sample_data) > 0:
                print(sample_data.to_string(index=False))
            else:
                print("  No workers with names found")
    
    print("\n" + "="*80)
    print(f"COMPLETE RESULTS SAVED TO:")
    print(f"  {output_file}")
    print("="*80)
    
    # Summary statistics
    total_records = len(df)
    total_with_names = len(df[df['first_name'].notna() & df['last_name'].notna()])
    print(f"\nOVERALL STATISTICS:")
    print(f"  Total Records: {total_records}")
    print(f"  Records with Names: {total_with_names} ({total_with_names/total_records*100:.1f}%)")
    print(f"  Records without Names: {total_records - total_with_names}")
    
except Exception as e:
    import traceback
    print(f"Error querying BigQuery: {e}")
    print(f"\nFull traceback:")
    traceback.print_exc()
