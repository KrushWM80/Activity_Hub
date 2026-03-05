import json

json_path = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\data\job_codes_master.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Analyze all available job code fields and their relationships
all_codes = {}
role_types = {}

for entry in data.get('job_codes', []):
    # Try multiple possible job code fields
    codes_in_entry = {}
    
    if entry.get('SMART Job Code'):
        codes_in_entry['SMART Job Code'] = entry.get('SMART Job Code')
    if entry.get('Workday Job Code'):
        codes_in_entry['Workday Job Code'] = entry.get('Workday Job Code')
    if entry.get('Job Code'):
        codes_in_entry['Job Code'] = entry.get('Job Code')
    
    # Get role/category information
    category = entry.get('Category', 'Unknown')
    pg_level = entry.get('PG Level', '')
    job_family = entry.get('Job Family', '')
    job_title = entry.get('Job Title', '')
    
    # Store with role info
    for code_type, code_value in codes_in_entry.items():
        if code_value and isinstance(code_value, str) and code_value.strip():
            key = (code_type, code_value.strip())
            if key not in all_codes:
                all_codes[key] = {
                    'Category': category,
                    'PG Level': pg_level,
                    'Job Family': job_family,
                    'Job Title': job_title
                }

print("="*80)
print("UNIQUE JOB CODES ANALYSIS FROM job_codes_master.json")
print("="*80)
print()

# Group by code type
by_type = {}
for (code_type, code_value), info in all_codes.items():
    if code_type not in by_type:
        by_type[code_type] = []
    by_type[code_type].append((code_value, info))

for code_type in sorted(by_type.keys()):
    entries = by_type[code_type]
    print(f"\n{code_type}:")
    print(f"  Total unique: {len(entries)}")
    
    # Count by category
    cat_count = {}
    for code, info in entries:
        cat = info['Category']
        cat_count[cat] = cat_count.get(cat, 0) + 1
    
    print(f"  By Category:")
    for cat, count in sorted(cat_count.items()):
        print(f"    {cat}: {count}")

# Find total if combining different code types
print(f"\n" + "="*80)
print(f"TOTAL IF COMBINING ALL CODE TYPES:")
print(f"Total unique codes (any type): {len(all_codes)}")

# Check if any combination gets close to 206
smart_codes = set(c[1] for c in all_codes.keys() if c[0] == 'SMART Job Code')
workday_codes = set(c[1] for c in all_codes.keys() if c[0] == 'Workday Job Code')
jobcode_codes = set(c[1] for c in all_codes.keys() if c[0] == 'Job Code')

combined = smart_codes | workday_codes | jobcode_codes
print(f"Union of all code types: {len(combined)}")

# Maybe user meant Workday codes which has 169?
print(f"\nWorkday Job Code total: {len(workday_codes)}")
print(f"SMART Job Code total: {len(smart_codes)}")
print(f"Generic Job Code total: {len(jobcode_codes)}")
print("="*80)
