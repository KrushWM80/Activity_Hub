"""
Job Code Comparison Script
Compares HR job codes with Teaming (TMS) data to find missing job codes.

Job Code Format: Division-Dept-JobCode (e.g., 1-993-1026)
In Teaming data: jobCode=1026, deptNumber=993, divNumber=1
"""

import pandas as pd
import os

# File paths
teaming_file = r"C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\TMS Data (3).xlsx"
hr_file = r"C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\archive\OLD_ANALYSIS\Store_Employees_20251223_083853.csv"

# Output directory
output_dir = r"C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming"

print("=" * 80)
print("JOB CODE COMPARISON: HR DATA vs TEAMING DATA")
print("=" * 80)

# Load Teaming Data
print("\n1. Loading Teaming Data...")
teaming_df = pd.read_excel(teaming_file)
print(f"   Teaming records loaded: {len(teaming_df)}")

# Load HR Data
print("\n2. Loading HR Data...")
hr_df = pd.read_csv(hr_file)
print(f"   HR records loaded: {len(hr_df)}")

# Create composite job code in Teaming data (Division-Dept-JobCode)
print("\n3. Processing Teaming Data...")
teaming_df['composite_job_code'] = (
    teaming_df['divNumber'].fillna(0).astype(int).astype(str) + '-' +
    teaming_df['deptNumber'].fillna(0).astype(int).astype(str) + '-' +
    teaming_df['jobCode'].fillna(0).astype(int).astype(str)
)

# Get unique job codes from Teaming
teaming_job_codes = set(teaming_df['composite_job_code'].unique())
print(f"   Unique job codes in Teaming: {len(teaming_job_codes)}")

# Extract job codes from HR data
print("\n4. Processing HR Data...")
hr_df['Job_Code_Clean'] = hr_df['Job_Code'].str.strip()
hr_job_codes = set(hr_df['Job_Code_Clean'].dropna().unique())
print(f"   Unique job codes in HR: {len(hr_job_codes)}")

# Find job codes NOT in Teaming
print("\n5. Comparing Job Codes...")
missing_from_teaming = hr_job_codes - teaming_job_codes
found_in_teaming = hr_job_codes & teaming_job_codes

print(f"\n" + "=" * 80)
print("RESULTS SUMMARY")
print("=" * 80)
print(f"   Total HR Job Codes:                {len(hr_job_codes)}")
print(f"   Found in Teaming:                  {len(found_in_teaming)}")
print(f"   MISSING from Teaming:              {len(missing_from_teaming)}")
print(f"   Coverage:                          {len(found_in_teaming)/len(hr_job_codes)*100:.1f}%")

# Create detailed report of missing job codes
print("\n6. Creating detailed report of missing job codes...")

# Get HR records for missing job codes
missing_hr_records = hr_df[hr_df['Job_Code_Clean'].isin(missing_from_teaming)].copy()

# Summarize by job code
missing_summary = missing_hr_records.groupby('Job_Code_Clean').agg({
    'WIN_Number': 'count',
    'Job_Title': 'first'
}).reset_index()
missing_summary.columns = ['Job_Code', 'Employee_Count', 'Job_Title']
missing_summary = missing_summary.sort_values('Employee_Count', ascending=False)

print(f"\n" + "=" * 80)
print("JOB CODES MISSING FROM TEAMING (Top 30)")
print("=" * 80)
print(f"{'Job Code':<15} {'Count':>8} {'Job Title'}")
print("-" * 80)
for _, row in missing_summary.head(30).iterrows():
    print(f"{row['Job_Code']:<15} {row['Employee_Count']:>8} {row['Job_Title']}")

# Parse the job code components for easier analysis
def parse_job_code(code):
    try:
        parts = code.split('-')
        if len(parts) == 3:
            return {
                'Division': parts[0],
                'Department': parts[1],
                'JobCode': parts[2]
            }
    except:
        pass
    return {'Division': '', 'Department': '', 'JobCode': ''}

# Add parsed components
parsed = missing_summary['Job_Code'].apply(parse_job_code).apply(pd.Series)
missing_summary = pd.concat([missing_summary, parsed], axis=1)

# Save results to CSV
output_file = os.path.join(output_dir, "Missing_JobCodes_From_Teaming.csv")
missing_summary.to_csv(output_file, index=False)
print(f"\n7. Saved missing job codes report to: {output_file}")

# Summary by Division
print(f"\n" + "=" * 80)
print("MISSING JOB CODES BY DIVISION")
print("=" * 80)
div_summary = missing_summary.groupby('Division').agg({
    'Job_Code': 'count',
    'Employee_Count': 'sum'
}).reset_index()
div_summary.columns = ['Division', 'Unique_JobCodes', 'Total_Employees']
div_summary = div_summary.sort_values('Total_Employees', ascending=False)
print(div_summary.to_string(index=False))

# Summary by Department (Top 20)
print(f"\n" + "=" * 80)
print("MISSING JOB CODES BY DEPARTMENT (Top 20)")
print("=" * 80)
dept_summary = missing_summary.groupby('Department').agg({
    'Job_Code': 'count',
    'Employee_Count': 'sum'
}).reset_index()
dept_summary.columns = ['Department', 'Unique_JobCodes', 'Total_Employees']
dept_summary = dept_summary.sort_values('Total_Employees', ascending=False)
print(dept_summary.head(20).to_string(index=False))

# Show job codes that ARE in Teaming (sample)
print(f"\n" + "=" * 80)
print("JOB CODES FOUND IN TEAMING (Sample)")
print("=" * 80)
found_sample = list(found_in_teaming)[:20]
for code in found_sample:
    hr_title = hr_df[hr_df['Job_Code_Clean'] == code]['Job_Title'].iloc[0] if len(hr_df[hr_df['Job_Code_Clean'] == code]) > 0 else 'N/A'
    print(f"   {code:<15} {hr_title}")

# Also show what Teaming job codes are NOT in HR (orphaned in Teaming)
print(f"\n" + "=" * 80)
print("TEAMING JOB CODES NOT IN HR DATA")
print("=" * 80)
orphaned_in_teaming = teaming_job_codes - hr_job_codes
# Filter out invalid codes like 0-0-0
orphaned_in_teaming = {c for c in orphaned_in_teaming if c != '0-0-0'}
print(f"   Total orphaned Teaming job codes: {len(orphaned_in_teaming)}")

if orphaned_in_teaming:
    orphaned_df = teaming_df[teaming_df['composite_job_code'].isin(orphaned_in_teaming)][
        ['composite_job_code', 'jobCodeTitle', 'teamName', 'workgroupName']
    ].drop_duplicates().head(30)
    print("\nSample of Teaming job codes not in HR data:")
    print(orphaned_df.to_string(index=False))
    
    # Save orphaned Teaming codes
    orphaned_file = os.path.join(output_dir, "Teaming_JobCodes_Not_In_HR.csv")
    orphaned_full = teaming_df[teaming_df['composite_job_code'].isin(orphaned_in_teaming)][
        ['composite_job_code', 'jobCodeTitle', 'teamName', 'workgroupName', 'jobCode', 'deptNumber', 'divNumber']
    ].drop_duplicates()
    orphaned_full.to_csv(orphaned_file, index=False)
    print(f"\n   Saved orphaned Teaming job codes to: {orphaned_file}")

print(f"\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
