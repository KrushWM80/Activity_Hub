"""
Job Code Comparison: Polaris (BigQuery) vs Teaming (TMS)
Data Source: polaris-analytics-prod.us_walmart.vw_polaris_current_schedule
"""

import pandas as pd
import os

# File paths
teaming_file = r"C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\TMS Data (3).xlsx"
polaris_file = r"C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\polaris_job_codes.csv"
output_dir = r"C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming"

print("=" * 80)
print("JOB CODE COMPARISON: POLARIS (BigQuery) vs TEAMING (TMS)")
print("=" * 80)

# Load Teaming Data
print("\n1. Loading Teaming Data...")
teaming_df = pd.read_excel(teaming_file)
print(f"   Records loaded: {len(teaming_df)}")

# Load Polaris Data
print("\n2. Loading Polaris Data (from BigQuery)...")
polaris_df = pd.read_csv(polaris_file)
print(f"   Records loaded: {len(polaris_df)}")

# Create composite job code in Teaming (Division-Dept-JobCode)
print("\n3. Processing Teaming Data...")
teaming_df['composite_job_code'] = (
    teaming_df['divNumber'].fillna(0).astype(int).astype(str) + '-' +
    teaming_df['deptNumber'].fillna(0).astype(int).astype(str) + '-' +
    teaming_df['jobCode'].fillna(0).astype(int).astype(str)
)

# Get unique job codes
teaming_codes = set(teaming_df['composite_job_code'].unique())
polaris_codes = set(polaris_df['job_code'].str.strip().unique())

print(f"   Unique Teaming job codes: {len(teaming_codes)}")
print(f"   Unique Polaris job codes: {len(polaris_codes)}")

# Find differences
missing_from_teaming = polaris_codes - teaming_codes
found_in_teaming = polaris_codes & teaming_codes
orphaned_in_teaming = teaming_codes - polaris_codes

# Filter out 0-0-0 from orphaned
orphaned_in_teaming = {c for c in orphaned_in_teaming if c != '0-0-0'}

print("\n" + "=" * 80)
print("RESULTS SUMMARY")
print("=" * 80)
print(f"   Total Polaris Job Codes:           {len(polaris_codes)}")
print(f"   Found in Teaming:                  {len(found_in_teaming)}")
print(f"   MISSING from Teaming:              {len(missing_from_teaming)}")
print(f"   Coverage:                          {len(found_in_teaming)/len(polaris_codes)*100:.1f}%")
print(f"   Teaming codes not in Polaris:      {len(orphaned_in_teaming)}")

# Details of missing codes
print("\n" + "=" * 80)
print(f"JOB CODES MISSING FROM TEAMING ({len(missing_from_teaming)} total)")
print("=" * 80)
print(f"{'Job Code':<20} {'Job Name'}")
print("-" * 80)

missing_details = polaris_df[polaris_df['job_code'].str.strip().isin(missing_from_teaming)].copy()
missing_details = missing_details.sort_values('job_code')

for _, row in missing_details.iterrows():
    print(f"{row['job_code']:<20} {row['job_nm']}")

# Parse job codes into components
def parse_job_code(code):
    try:
        parts = str(code).split('-')
        if len(parts) == 3:
            return pd.Series({
                'Division': parts[0],
                'Department': parts[1],
                'JobCode': parts[2]
            })
    except:
        pass
    return pd.Series({'Division': '', 'Department': '', 'JobCode': ''})

missing_details = pd.concat([missing_details, missing_details['job_code'].apply(parse_job_code)], axis=1)

# Summary by Division
print("\n" + "=" * 80)
print("MISSING JOB CODES BY DIVISION")
print("=" * 80)
div_summary = missing_details.groupby('Division').size().reset_index(name='Count')
div_summary = div_summary.sort_values('Count', ascending=False)
print(div_summary.to_string(index=False))

# Summary by Department (Top 15)
print("\n" + "=" * 80)
print("MISSING JOB CODES BY DEPARTMENT")
print("=" * 80)
dept_summary = missing_details.groupby('Department').size().reset_index(name='Count')
dept_summary = dept_summary.sort_values('Count', ascending=False)
print(dept_summary.to_string(index=False))

# Save missing codes
output_file = os.path.join(output_dir, "Missing_From_Teaming_POLARIS.csv")
missing_details.to_csv(output_file, index=False)
print(f"\n4. Saved missing job codes to: {output_file}")

# Show Teaming codes not in Polaris (sample)
print("\n" + "=" * 80)
print(f"TEAMING JOB CODES NOT IN POLARIS (sample of {min(30, len(orphaned_in_teaming))})")
print("=" * 80)

orphaned_df = teaming_df[teaming_df['composite_job_code'].isin(orphaned_in_teaming)][
    ['composite_job_code', 'jobCodeTitle', 'teamName']
].drop_duplicates().head(30)

for _, row in orphaned_df.iterrows():
    print(f"{row['composite_job_code']:<20} {row['jobCodeTitle']:<40} {row['teamName']}")

# Save orphaned codes
orphaned_file = os.path.join(output_dir, "Teaming_Not_In_Polaris.csv")
orphaned_full = teaming_df[teaming_df['composite_job_code'].isin(orphaned_in_teaming)][
    ['composite_job_code', 'jobCodeTitle', 'teamName', 'workgroupName', 'jobCode', 'deptNumber', 'divNumber']
].drop_duplicates()
orphaned_full.to_csv(orphaned_file, index=False)
print(f"\n5. Saved Teaming codes not in Polaris to: {orphaned_file}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
