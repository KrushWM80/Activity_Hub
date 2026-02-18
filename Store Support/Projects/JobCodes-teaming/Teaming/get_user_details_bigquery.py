"""
Extract user details (First Name, Last Name, Store) for specific Job Codes from BigQuery
"""
from google.cloud import bigquery
import pandas as pd
import os

# Initialize BigQuery client
client = bigquery.Client()

# Job codes to query
job_codes = ['1-16-101', '1-993-1076']

# First, let's discover the available columns
discovery_query = """
SELECT * 
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code IN ('1-16-101', '1-993-1076')
LIMIT 5
"""

print("Querying BigQuery for user details...")
print(f"Job Codes: {', '.join(job_codes)}")
print()

try:
    # First discover the columns
    print("Discovering available columns...")
    query_job = client.query(discovery_query)
    print(f"Query job created, waiting for results...")
    results = list(query_job.result())
    print(f"Query returned {len(results)} rows")
    
    if not results:
        print("No data found for the specified job codes.")
        exit(1)
    
    # Get column names from first row
    first_row = results[0]
    column_names = list(first_row.keys())
    print(f"Available columns ({len(column_names)}): {column_names}")
    print(f"\nSample data (first row):")
    print(dict(first_row))
    
    # Now query all matching records
    query = f"""
    SELECT *
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE job_code IN ('1-16-101', '1-993-1076')
    """
    
    print("\n" + "="*80)
    print("Querying for all users...")
    query_job = client.query(query)
    results = list(query_job.result())
    
    # Convert to list of dicts
    rows_list = [dict(row) for row in results]
    print(f"Found {len(rows_list)} records")
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(rows_list)
    
    print(f"Found {len(df)} users")
    print()
    
    # Save to CSV
    output_file = r"C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\User_Details_JobCodes.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved results to: {output_file}")
    
    # Display summary
    print("\nSummary by Job Code:")
    print("="*80)
    for jc in job_codes:
        jc_data = df[df['job_code'] == jc]
        if len(jc_data) > 0:
            # Try to get job name from various possible columns
            job_name = jc_data.iloc[0].get('job_nm', jc_data.iloc[0].get('job_title', 'Unknown'))
            print(f"\nJob Code: {jc} - {job_name}")
            print(f"Total Records: {len(jc_data)}")
            
            # Show available columns in the data
            print(f"\nColumns available: {list(jc_data.columns)}")
            print("\nFirst 10 records:")
            print(jc_data.head(10).to_string(index=False))
    
    print("\n" + "="*80)
    print("Complete results saved to CSV file.")
    
except Exception as e:
    import traceback
    print(f"Error querying BigQuery: {e}")
    print(f"\nFull traceback:")
    traceback.print_exc()
    print("\nMake sure you have:")
    print("1. Google Cloud credentials configured")
    print("2. Access to polaris-analytics-prod.us_walmart dataset")
    print("3. google-cloud-bigquery package installed (pip install google-cloud-bigquery)")
