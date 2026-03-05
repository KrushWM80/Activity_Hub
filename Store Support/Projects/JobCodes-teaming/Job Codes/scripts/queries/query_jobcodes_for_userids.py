import pandas as pd
from google.cloud import bigquery
import json

# First, parse the CSV file to get job codes
csv_path = r"C:\Users\krush\Downloads\Roles.csv"
df = pd.read_csv(csv_path, header=0)

# Extract unique job codes
job_codes_set = set()
role_type_mapping = {}

for idx, row in df.iterrows():
    role_type = row.iloc[0]
    for col_idx in range(1, len(row)):
        job_code = row.iloc[col_idx]
        if pd.notna(job_code) and job_code.strip() != "":
            job_code = str(job_code).strip()
            job_codes_set.add(job_code)
            if job_code not in role_type_mapping:
                role_type_mapping[job_code] = role_type

job_codes_list = sorted(list(job_codes_set))

print(f"Retrieved {len(job_codes_list)} unique job codes from CSV")
print(f"Now querying CoreHR BigQuery for User IDs...\n")

# Query CoreHR for each job code
client = bigquery.Client()
results_list = []

query_template = '''
SELECT 
    t0.userID,
    t0.employeeID,
    t0.personalInfo.legalFirstName,
    t0.personalInfo.legalLastName,
    pos.jobCode,
    pos.positionTitle,
    pos.storeName,
    pos.storeNumber
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` t0,
UNNEST(t0.employmentInfo.positionInfoHistory) as pos
WHERE pos.jobCode = @job_code
    AND pos.active = True
LIMIT 1
'''

for i, job_code in enumerate(job_codes_list, 1):
    try:
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("job_code", "STRING", job_code),
            ]
        )
        query_job = client.query(query_template, job_config=job_config)
        results = query_job.result()
        rows = list(results)
        
        if rows:
            row = rows[0]
            results_list.append({
                'JobCode': job_code,
                'UserID': row.userID,
                'EmployeeID': row.employeeID,
                'FirstName': row.legalFirstName,
                'LastName': row.legalLastName,
                'PositionTitle': row.positionTitle,
                'StoreName': row.storeName,
                'StoreNumber': row.storeNumber,
                'RoleType': role_type_mapping.get(job_code, 'Unknown')
            })
            status = "✓"
        else:
            results_list.append({
                'JobCode': job_code,
                'UserID': None,
                'EmployeeID': None,
                'FirstName': None,
                'LastName': None,
                'PositionTitle': None,
                'StoreName': None,
                'StoreNumber': None,
                'RoleType': role_type_mapping.get(job_code, 'Unknown')
            })
            status = "✗"
        
        if i % 20 == 0:
            print(f"Processed {i}/{len(job_codes_list)} job codes...")
            
    except Exception as e:
        print(f"Error querying job code {job_code}: {e}")
        results_list.append({
            'JobCode': job_code,
            'UserID': None,
            'EmployeeID': None,
            'FirstName': None,
            'LastName': None,
            'PositionTitle': None,
            'StoreName': None,
            'StoreNumber': None,
            'RoleType': role_type_mapping.get(job_code, 'Unknown')
        })

# Convert to DataFrame
results_df = pd.DataFrame(results_list)

# Display summary
print(f"\n" + "="*80)
print(f"RESULTS SUMMARY")
print(f"="*80)
print(f"Total job codes processed: {len(results_df)}")
print(f"Job codes with User IDs: {results_df['UserID'].notna().sum()}")
print(f"Job codes WITHOUT User IDs: {results_df['UserID'].isna().sum()}")

print(f"\n--- SAMPLE RESULTS (First 20 with User IDs) ---")
with_ids = results_df[results_df['UserID'].notna()].head(20)
print(with_ids[['JobCode', 'UserID', 'FirstName', 'LastName', 'RoleType']].to_string(index=False))

# Save to CSV
output_path = r"C:\Users\krush\Downloads\JobCodes_UserIDs.csv"
results_df.to_csv(output_path, index=False)
print(f"\n✓ Results saved to: {output_path}")

# Show job codes without User IDs
print(f"\n--- JOB CODES WITHOUT USER IDS ({results_df['UserID'].isna().sum()}) ---")
no_ids = results_df[results_df['UserID'].isna()]['JobCode'].tolist()
print(", ".join(no_ids[:20]))
if len(no_ids) > 20:
    print(f"... and {len(no_ids) - 20} more")
