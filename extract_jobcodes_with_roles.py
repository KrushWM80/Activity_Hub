import json
import pandas as pd
from collections import defaultdict

json_path = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\data\job_codes_master.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract Workday Job Codes WITH their role/category info
job_codes_by_role = defaultdict(list)
job_code_details = {}

for entry in data.get('job_codes', []):
    workday_code = entry.get('Workday Job Code')
    if workday_code and isinstance(workday_code, str) and workday_code.strip():
        workday_code = workday_code.strip()
        
        # Get role classification
        category = entry.get('Category', 'Unknown')
        pg_level = entry.get('PG Level', '')
        job_title = entry.get('Job Title', '').strip() if entry.get('Job Title') else ''
        job_family = entry.get('Job Family', '').strip() if entry.get('Job Family') else ''
        
        # Map category to simpler role type
        if category == 'Salary':
            role_type = 'Salary'
        elif category == 'Hourly':
            role_type = 'Hourly'
        elif category == 'Invalid Salary':
            role_type = 'Salary'
        else:
            role_type = 'Unknown'
        
        job_codes_by_role[role_type].append(workday_code)
        job_code_details[workday_code] = {
            'Role': role_type,
            'Category': category,
            'PG Level': pg_level,
            'Job Title': job_title,
            'Job Family': job_family
        }

print("="*80)
print("WORKDAY JOB CODES EXTRACTED WITH ROLES")
print("="*80)
print()

for role_type in sorted(job_codes_by_role.keys()):
    codes = sorted(set(job_codes_by_role[role_type]))
    print(f"\n{role_type}: {len(codes)} unique job codes")
    print(f"  Sample: {codes[:5]}")

print(f"\n" + "="*80)
print(f"TOTAL UNIQUE WORKDAY JOB CODES: {len(job_code_details)}")
print("="*80)

# Create Roles.csv with role types and job codes preserved
# Format: First column is Role Type, remaining columns are job codes for that role
max_codes = max(len(job_codes_by_role[role]) for role in job_codes_by_role)

rows = []
for role_type in sorted(job_codes_by_role.keys()):
    codes = sorted(set(job_codes_by_role[role_type]))
    # Pad with empty strings
    row = [role_type] + codes + [''] * (max_codes - len(codes))
    rows.append(row)

# Create DataFrame and save
df = pd.DataFrame(rows)
output_path = r"C:\Users\krush\Downloads\Roles.csv"
df.to_csv(output_path, index=False, header=False)

print(f"\n✓ Created Roles.csv at: {output_path}")
print(f"\nCsv Structure:")
print(f"  Rows (Role Types): {len(rows)}")
print(f"  Max Columns per Role: {max_codes + 1}")  # +1 for Role Type column

# Create detailed mapping file for reference
mapping_path = r"C:\Users\krush\Downloads\JobCodes_With_Roles.csv"
mapping_data = []
for code, details in sorted(job_code_details.items()):
    mapping_data.append({
        'Workday Job Code': code,
        'Role Type': details['Role'],
        'Category': details['Category'],
        'PG Level': details['PG Level'],
        'Job Title': details['Job Title'],
        'Job Family': details['Job Family']
    })

mapping_df = pd.DataFrame(mapping_data)
mapping_df.to_csv(mapping_path, index=False)

print(f"✓ Created JobCodes_With_Roles.csv at: {mapping_path}")
print(f"\nREADY FOR BIGQUERY QUERY!")
