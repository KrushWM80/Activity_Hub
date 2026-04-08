import json
import pandas as pd
import re

print("=" * 80)
print("DISCOVERED PATTERN - Potential Code Mapping")
print("=" * 80)

# Load data
json_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\job_codes_master.json"
with open(json_path, 'r', encoding='utf-8') as f:
    excel_data = json.load(f)

polaris_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\polaris_job_codes.csv"
polaris_df = pd.read_csv(polaris_path)

print("\nEXAMPLE MATCH FOUND:")
print("  Excel SMART Code: US-01-0202-002104")
print("  Excel Job Title: Adult Beverage DM")
print("  Polaris Code: 1-202-2104")
print("  Polaris Title: Adult Beverage DM 1-202-2104")
print("\n  PATTERN: US-01-0202-002104 might extract to 1-202-2104")
print("           (Take digits: 01, 0202, 002104 = extract digits and format as 1-202-2104)")

# Try to build mapping from Workday codes
print("\n" + "=" * 80)
print("STRATEGY: Map using Excel 'Workday Job Code' column")
print("=" * 80)

# Extract mapping possibilities
mapping_dict = {}
direct_matches = 0

for excel_rec in excel_data['job_codes']:
    workday_code = str(excel_rec.get('Workday Job Code', '')).strip()
    smart_code = excel_rec.get('SMART Job Code', '')
    job_title = excel_rec.get('Job Title', '')
    
    if workday_code and workday_code in polaris_df['job_code'].values:
        polaris_row = polaris_df[polaris_df['job_code'] == workday_code].iloc[0]
        mapping_dict[workday_code] = {
            'excel_smart': smart_code,
            'excel_title': job_title,
            'polaris_code': workday_code,
            'polaris_title': polaris_row['job_nm'],
            'match_type': 'EXACT_WORKDAY_MATCH'
        }
        direct_matches += 1

print(f"\nDirect matches using Workday Job Code: {direct_matches} / 271 Polaris codes")
print(f"\nExamples of successful mappings:")
for i, (code, mapping) in enumerate(list(mapping_dict.items())[:5]):
    print(f"\n  {i+1}. Excel -> Polaris")
    print(f"     Excel: {mapping['excel_smart']} ({mapping['excel_title']})")
    print(f"     Polaris: {mapping['polaris_code']} ({mapping['polaris_title']})")

# Look for name-based matches
print("\n" + "=" * 80)
print("STRATEGY: Map by matching Job Titles")
print("=" * 80)

title_mapping = {}
for idx, polaris_row in polaris_df.iterrows():
    polaris_code = polaris_row['job_code']
    polaris_title = polaris_row['job_nm'].lower()
    
    # Remove the code from end of title (e.g., "Adult Beverage DM 1-202-2104" -> "adult beverage dm")
    polaris_title_clean = re.sub(r'\s+\d+-\d+-\d+$', '', polaris_title).strip()
    
    # Look for matching Excel title
    for excel_rec in excel_data['job_codes']:
        excel_title = str(excel_rec.get('Job Title', '')).lower()
        if polaris_title_clean == excel_title:
            title_mapping[polaris_code] = {
                'excel_smart': excel_rec.get('SMART Job Code'),
                'excel_title': excel_rec.get('Job Title'),
                'polaris_code': polaris_code,
                'polaris_title': polaris_row['job_nm']
            }
            break

print(f"Exact title matches: {len(title_mapping)} / 271 Polaris codes")
print(f"\nExamples of title-based matches:")
for i, (code, mapping) in enumerate(list(title_mapping.items())[:5]):
    print(f"\n  {i+1}. Excel: {mapping['excel_smart']} ({mapping['excel_title']})")
    print(f"      Polaris: {mapping['polaris_code']} ({mapping['polaris_title']})")

# Combined summary
total_mapped = len(mapping_dict) + len(set(title_mapping.keys()) - set(mapping_dict.keys()))
print("\n" + "=" * 80)
print(f"TOTAL POTENTIAL MAPPINGS: {total_mapped} / 271 Polaris codes ({(total_mapped/271)*100:.1f}%)")
print("=" * 80)

print(f"\nUniverse of Excel Master Table: {len(excel_data['job_codes'])} total records")
print(f"  - Can map via Workday Code: {direct_matches}")
print(f"  - Can map via Title match: {len(title_mapping)}")
print(f"  - Cannot map: {271 - total_mapped} Polaris codes may not be in Excel")
