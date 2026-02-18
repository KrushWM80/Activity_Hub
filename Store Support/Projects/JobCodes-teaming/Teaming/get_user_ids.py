"""
Extract User IDs for specific Job Codes
"""
import pandas as pd

# Load the TMS Data file
teaming_file = r"C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\TMS Data (3).xlsx"
df = pd.read_excel(teaming_file)

# Create composite job code
df['composite_job_code'] = (
    df['divNumber'].fillna(0).astype(int).astype(str) + '-' +
    df['deptNumber'].fillna(0).astype(int).astype(str) + '-' +
    df['jobCode'].fillna(0).astype(int).astype(str)
)

# Filter for the requested job codes
job_codes = ['1-16-101', '1-993-1076']
filtered_df = df[df['composite_job_code'].isin(job_codes)]

# Get user IDs for each job code
for jc in job_codes:
    jc_data = filtered_df[filtered_df['composite_job_code'] == jc]
    print(f"\n{'='*80}")
    print(f"Job Code: {jc}")
    if len(jc_data) > 0:
        job_title = jc_data['jobCodeTitle'].iloc[0] if 'jobCodeTitle' in jc_data.columns else 'N/A'
        print(f"Job Title: {job_title}")
        print(f"Total Users: {len(jc_data)}")
        print(f"{'='*80}\n")
        
        # Get user IDs
        if 'userId' in jc_data.columns:
            user_ids = sorted(jc_data['userId'].unique().tolist())
            print(f"User IDs ({len(user_ids)} unique):")
            for uid in user_ids:
                print(f"  {uid}")
        else:
            print("userId column not found in data")
            print("\nAvailable columns:", list(jc_data.columns))
    else:
        print(f"No users found for job code {jc}")
    print()

print("\nDONE")
