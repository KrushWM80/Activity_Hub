import pandas as pd
from google.cloud import bigquery
import sys

# Load the job code details with role information
csv_path = r"C:\Users\krush\Downloads\JobCodes_With_Roles.csv"
job_codes_df = pd.read_csv(csv_path)

# Create mapping of job code to role
job_code_to_role = dict(zip(job_codes_df['Workday Job Code'], job_codes_df['Role Type']))
job_code_to_details = {}
for idx, row in job_codes_df.iterrows():
    job_code_to_details[row['Workday Job Code']] = {
        'Role Type': row['Role Type'],
        'Category': row['Category'],
        'PG Level': row['PG Level'],
        'Job Title': row['Job Title'],
        'Job Family': row['Job Family']
    }

job_codes_list = sorted(job_code_to_role.keys())

print("="*80)
print(f"QUERYING COREHR FOR {len(job_codes_list)} WORKDAY JOB CODES")
print("="*80)
print(f"Hourly codes: {sum(1 for jc in job_codes_list if job_code_to_role[jc] == 'Hourly')}")
print(f"Salary codes: {sum(1 for jc in job_codes_list if job_code_to_role[jc] == 'Salary')}")
print()

# Initialize BigQuery client
client = bigquery.Client()
results_list = []

# Query template - using jobCode which should match Workday Job Code
query_template = '''
SELECT 
    t0.userID,
    t0.employeeID,
    t0.personalInfo.legalFirstName as firstName,
    t0.personalInfo.legalLastName as lastName,
    pos.jobCode,
    pos.positionTitle,
    pos.storeName,
    pos.storeNumber,
    pos.positionEffectiveDate,
    pos.active
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` t0,
UNNEST(t0.employmentInfo.positionInfoHistory) as pos
WHERE pos.jobCode = @job_code
  AND t0.personalInfo.legalFirstName IS NOT NULL
ORDER BY pos.positionEffectiveDate DESC
LIMIT 5
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
        
        details = job_code_to_details[job_code]
        
        if rows:
            # Get the first (most recent) row
            row = rows[0]
            results_list.append({
                'Job Code': job_code,
                'Role Type': details['Role Type'],
                'PG Level': details['PG Level'],
                'Job Title': details['Job Title'],
                'User ID': row.userID,
                'Employee ID': row.employeeID,
                'First Name': row.firstName,
                'Last Name': row.lastName,
                'Position Title': row.positionTitle,
                'Store Name': row.storeName,
                'Store Number': row.storeNumber,
                'Match Count': len(rows)
            })
        else:
            results_list.append({
                'Job Code': job_code,
                'Role Type': details['Role Type'],
                'PG Level': details['PG Level'],
                'Job Title': details['Job Title'],
                'User ID': None,
                'Employee ID': None,
                'First Name': None,
                'Last Name': None,
                'Position Title': None,
                'Store Name': None,
                'Store Number': None,
                'Match Count': 0
            })
        
        if i % 50 == 0:
            print(f"✓ Processed {i}/{len(job_codes_list)} job codes...")
            
    except Exception as e:
        error_msg = str(e)
        if "NOT_FOUND" in error_msg or "not found" in error_msg.lower():
            results_list.append({
                'Job Code': job_code,
                'Role Type': details['Role Type'],
                'PG Level': details['PG Level'],
                'Job Title': details['Job Title'],
                'User ID': None,
                'Employee ID': None,
                'First Name': None,
                'Last Name': None,
                'Position Title': None,
                'Store Name': None,
                'Store Number': None,
                'Match Count': 0
            })
        else:
            print(f"✗ Error with job code {job_code}: {error_msg[:100]}")
            results_list.append({
                'Job Code': job_code,
                'Role Type': details['Role Type'],
                'PG Level': details['PG Level'],
                'Job Title': details['Job Title'],
                'User ID': None,
                'Employee ID': None,
                'First Name': None,
                'Last Name': None,
                'Position Title': None,
                'Store Name': None,
                'Store Number': None,
                'Match Count': -1
            })

# Convert to DataFrame
results_df = pd.DataFrame(results_list)

# Display summary
print(f"\n" + "="*80)
print(f"RESULTS SUMMARY - JOB CODES TO USER IDS MAPPING")
print(f"="*80)
print(f"Total job codes queried: {len(results_df)}")
print(f"Job codes WITH User IDs found: {results_df['User ID'].notna().sum()}")
print(f"Job codes WITHOUT User IDs: {results_df['User ID'].isna().sum()}")

print(f"\n--- BY ROLE TYPE ---")
for role_type in sorted(results_df['Role Type'].unique()):
    role_data = results_df[results_df['Role Type'] == role_type]
    matched = role_data['User ID'].notna().sum()
    total = len(role_data)
    print(f"{role_type}: {matched}/{total} matched ({100*matched//total if total > 0 else 0}%)")

print(f"\n--- SAMPLE RESULTS (First 10 with User IDs) ---")
with_ids = results_df[results_df['User ID'].notna()].head(10)
if not with_ids.empty:
    print(with_ids[['Job Code', 'Role Type', 'User ID', 'First Name', 'Last Name', 'Position Title']].to_string(index=False))
else:
    print("No User IDs found")

print(f"\n--- UNMATCHED JOB CODES (First 20) ---")
without_ids = results_df[results_df['User ID'].isna()].head(20)
if not without_ids.empty:
    print(without_ids[['Job Code', 'Role Type', 'PG Level', 'Job Title']].to_string(index=False))
else:
    print("All job codes matched!")

# Save to CSV
output_path = r"C:\Users\krush\Downloads\JobCodes_UserIDs_Mapping.csv"
results_df.to_csv(output_path, index=False)
print(f"\n✓ Complete results saved to: {output_path}")
print(f"\nFile contains {len(results_df)} rows with columns:")
print(f"  {', '.join(results_df.columns.tolist())}")

print("="*80)
