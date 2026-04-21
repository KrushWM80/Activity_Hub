"""
Extract worker details (First Name, Last Name, Store) for ALL MISSING Job Codes from BigQuery
Joins Polaris schedule data with Core HR employee profile data
"""
from google.cloud import bigquery
import pandas as pd
import sys
import os

# Add backend to path to use load_job_code_data function
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard', 'backend'))

from main import load_job_code_data, cache

# Initialize BigQuery client
client = bigquery.Client()

print("[WORKER QUERY] Loading missing job codes...")

# Get all job codes and determine which are missing
job_codes = cache.get_job_codes()
merged_df, _ = load_job_code_data()

# Build status map
status_map = {}
if merged_df is not None and len(merged_df) > 0:
    for _, row in merged_df.iterrows():
        job_code_str = str(row['job_code']).strip() if pd.notna(row['job_code']) else ""
        is_assigned = pd.notna(row.get('composite_job_code'))
        status = 'Assigned' if is_assigned else 'Missing'
        status_map[job_code_str] = status

# Get all missing job codes
missing_job_codes = []
for jc in job_codes:
    job_code_str = str(jc.get("job_code", "")).strip()
    status = status_map.get(job_code_str, "Unknown")
    if status == "Missing" and jc.get("user_count", 0) > 0:
        missing_job_codes.append(job_code_str)

print(f"[WORKER QUERY] Found {len(missing_job_codes)} missing job codes")
print(f"[WORKER QUERY] Sample: {missing_job_codes[:5]}")

if len(missing_job_codes) == 0:
    print("[WORKER QUERY] ERROR: No missing job codes found")
    sys.exit(1)

# Build SQL query with all missing job codes
job_codes_sql = "', '".join(missing_job_codes)
query = f"""
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
WHERE t1.job_code IN ('{job_codes_sql}')
ORDER BY t1.job_code, emp.legalLastName, emp.legalFirstName, t1.location_nm
"""

print("[WORKER QUERY] Querying BigQuery for worker details with names...")
print(f"[WORKER QUERY] Querying {len(missing_job_codes)} job codes")
print()

try:
    # Execute query
    print("[WORKER QUERY] Executing query (this may take a moment)...")
    query_job = client.query(query)
    results = list(query_job.result())
    
    # Convert to DataFrame
    rows_list = [dict(row) for row in results]
    df = pd.DataFrame(rows_list)
    
    print(f"[WORKER QUERY] Found {len(df)} unique worker records")
    print()
    
    # Select only the required columns
    output_columns = ['first_name', 'last_name', 'store_number', 'job_code', 'job_nm']
    df_output = df[output_columns]
    
    # Save to CSV in the same directory as this script
    output_file = os.path.join(os.path.dirname(__file__), 'Worker_Names_Stores_Missing_JobCodes.csv')
    df_output.to_csv(output_file, index=False)
    print(f"✓ Saved results to: {output_file}")
    
    # Also save as JSON for frontend tooltip data
    import json
    output_json_file = os.path.join(os.path.dirname(__file__), 'Worker_Names_Stores_Missing_JobCodes.json')
    json_data = df_output.to_dict('records')
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
    print(f"✓ Saved JSON to: {output_json_file}")
    
    # Display summary
    print("\n" + "="*80)
    print("SUMMARY BY JOB CODE")
    print("="*80)
    
    for jc in sorted(missing_job_codes)[:20]:  # Show first 20
        jc_data = df[df['job_code'] == jc]
        if len(jc_data) > 0:
            job_name = jc_data['job_nm'].iloc[0]
            unique_workers = jc_data['worker_id'].nunique()
            unique_stores = jc_data['store_number'].nunique()
            with_names = jc_data[jc_data['first_name'].notna() & jc_data['last_name'].notna()]
            
            print(f"\n{jc} - {job_name}")
            print(f"  Total Records: {len(jc_data)}")
            print(f"  Unique Workers: {unique_workers}")
            print(f"  Unique Stores: {unique_stores}")
            print(f"  Workers with Names: {len(with_names)} ({len(with_names)/len(jc_data)*100:.1f}%)")
    
    print("\n" + "="*80)
    print(f"COMPLETE RESULTS SAVED:")
    print(f"  {output_file}")
    print("="*80)
    
    # Summary statistics
    total_records = len(df)
    total_with_names = len(df[df['first_name'].notna() & df['last_name'].notna()])
    unique_job_codes = df['job_code'].nunique()
    
    print(f"\nOVERALL STATISTICS:")
    print(f"  Total Records: {total_records}")
    print(f"  Unique Job Codes: {unique_job_codes}")
    print(f"  Records with Names: {total_with_names} ({total_with_names/total_records*100:.1f}%)")
    print(f"  Records without Names: {total_records - total_with_names}")
    
except Exception as e:
    import traceback
    print(f"[WORKER QUERY] ERROR: {e}")
    print(f"\n[WORKER QUERY] Full traceback:")
    traceback.print_exc()
    sys.exit(1)
