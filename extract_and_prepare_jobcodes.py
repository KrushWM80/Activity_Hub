import json
import pandas as pd
from collections import defaultdict

# Load the job codes master data
json_path = r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\data\job_codes_master.json"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract job codes by category
job_codes_by_category = defaultdict(list)

for job_code_entry in data.get('job_codes', []):
    category = job_code_entry.get('Category', 'Unknown')
    smart_code = job_code_entry.get('SMART Job Code', '')
    
    if smart_code and smart_code.strip():
        job_codes_by_category[category].append(smart_code.strip())

print("=" * 80)
print("JOB CODES EXTRACTED FROM job_codes_master.json")
print("=" * 80)

for category in sorted(job_codes_by_category.keys()):
    codes = job_codes_by_category[category]
    print(f"\n{category}: {len(codes)} job codes")
    print(f"Sample: {codes[:5]}")

# Create Roles.csv file
# Format: First column is role type (Salary/Hourly), remaining columns are job codes
max_codes = max(len(codes) for codes in job_codes_by_category.values())

# Create rows
rows = []
for category in sorted(job_codes_by_category.keys()):
    codes = job_codes_by_category[category]
    # Pad with empty strings to match max length
    row = [category] + codes + [''] * (max_codes - len(codes))
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Save to Downloads
output_path = r"C:\Users\krush\Downloads\Roles.csv"
df.to_csv(output_path, index=False, header=False)

print(f"\n" + "=" * 80)
print(f"✓ Roles.csv created at: {output_path}")
print(f"✓ Total unique job codes: {sum(len(codes) for codes in job_codes_by_category.values())}")
print(f"✓ Salary positions: {len(job_codes_by_category['Salary'])}")
print(f"✓ Hourly positions: {len(job_codes_by_category['Hourly'])}")
print("=" * 80)
