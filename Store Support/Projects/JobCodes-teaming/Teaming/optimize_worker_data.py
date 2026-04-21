"""
Generate optimized worker data: count + 1 sample worker per job code
This dramatically reduces data size from 15.7MB to ~1-2MB for faster loading
"""
import pandas as pd
import json
import os

csv_file = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\Worker_Names_Stores_Missing_JobCodes.csv'
json_file = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\Worker_Names_Stores_Missing_JobCodes_Optimized.json'
csv_export_file = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\Worker_Names_Stores_Missing_JobCodes_Optimized.csv'

print("[OPTIMIZATION] Loading full worker data...")
df = pd.read_csv(csv_file)

print(f"[OPTIMIZATION] Total records: {len(df):,}")

# Group by job_code and get count + first worker as sample
print("[OPTIMIZATION] Generating optimized data structure...")
optimized_data = []
job_code_groups = df.groupby('job_code')

for job_code, group in job_code_groups:
    # Get count of unique workers for this job code
    worker_count = group['worker_id'].nunique() if 'worker_id' in group.columns else len(group)
    
    # Get first worker as sample
    first_worker = group.iloc[0]
    
    record = {
        'job_code': job_code,
        'job_nm': first_worker['job_nm'],
        'worker_count': int(worker_count),
        'sample_worker': {
            'first_name': first_worker['first_name'],
            'last_name': first_worker['last_name'],
            'store_number': int(first_worker['store_number']) if pd.notna(first_worker['store_number']) else None
        }
    }
    optimized_data.append(record)

print(f"[OPTIMIZATION] Optimized records: {len(optimized_data)}")

# Save as JSON
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(optimized_data, f, indent=2)

print(f"✓ JSON file created: {os.path.getsize(json_file) / 1024:.1f} KB")

# Also save as CSV for export
df_optimized = pd.DataFrame(optimized_data)
# Expand the sample_worker dict into columns
df_optimized['sample_worker_name'] = df_optimized['sample_worker'].apply(
    lambda x: f"{x['first_name']} {x['last_name']}"
)
df_optimized['sample_worker_store'] = df_optimized['sample_worker'].apply(
    lambda x: x['store_number']
)
df_export = df_optimized[['job_code', 'job_nm', 'worker_count', 'sample_worker_name', 'sample_worker_store']]
df_export.to_csv(csv_export_file, index=False)

print(f"✓ CSV file created: {os.path.getsize(csv_export_file) / 1024:.1f} KB")

print()
print("Sample optimized records:")
for i, r in enumerate(optimized_data[:3]):
    print(f"  {i+1}. Job Code: {r['job_code']}")
    print(f"     Workers: {r['worker_count']}")
    print(f"     Sample: {r['sample_worker']['first_name']} {r['sample_worker']['last_name']} - Store {r['sample_worker']['store_number']}")
    print()

print(f"✓ Optimization complete! Reduced from 15.7MB to ~{os.path.getsize(json_file) / 1024 / 1024:.1f}MB")
