import json
import pandas as pd
import sqlite3

print("=" * 80)
print("COMPARING POLARIS vs EXCEL JOB CODES - DETAILED ANALYSIS")
print("=" * 80)

# Load Excel master data
json_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\job_codes_master.json"

with open(json_path, 'r', encoding='utf-8') as f:
    excel_data = json.load(f)

# Load Polaris CSV
polaris_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\polaris_job_codes.csv"
polaris_df = pd.read_csv(polaris_path)

print(f"\nDATASET OVERVIEW:")
print(f"  Polaris job codes: {len(polaris_df)}")
print(f"  Excel job codes: {len(excel_data['job_codes'])}")

# Find specific code user asked about
print("\n" + "=" * 80)
print("SEARCHING FOR: US-01-0202-002104 (in EXCEL)")
print("=" * 80)
target_code = "US-01-0202-002104"
found = None
for record in excel_data['job_codes']:
    if record.get('SMART Job Code') == target_code:
        found = record
        break

if found:
    print(f"\n✓ FOUND in EXCEL Master Table:")
    print(f"  SMART Job Code (Workday): {found.get('SMART Job Code')}")
    print(f"  Job Title: {found.get('Job Title')}")
    print(f"  Workday Job Code: {found.get('Workday Job Code')}")
    print(f"  Category: {found.get('Category')}")
    print(f"  Job Family: {found.get('Job Family')}")
    print(f"  PG Level: {found.get('PG Level')}")
    print(f"  Task/Team: {found.get('Team')}")
    print(f"  Workgroup: {found.get('Workgroup')}")
    
    job_title = found.get('Job Title', '').lower()
    print(f"\n  Searching Polaris for similar job title '{job_title}'...")
    
    # Search Polaris by job title
    matches = polaris_df[polaris_df['job_nm'].str.lower().str.contains(job_title.split()[0], na=False)]
    if not matches.empty:
        print(f"  ✓ Found {len(matches)} Polaris records with similar title:")
        for idx, row in matches.head(5).iterrows():
            print(f"    - SMART: {row['job_code']} | Title: {row['job_nm']}")
    else:
        print(f"  ✗ No Polaris records with title '{job_title}'")
else:
    print(f"\n✗ NOT FOUND: {target_code}")

# Show comparison of formats
print("\n" + "=" * 80)
print("CODE FORMAT COMPARISON - First 10 each")
print("=" * 80)

print(f"\nPOLARIS Job Codes (SMART internal format):")
for idx, row in polaris_df.head(10).iterrows():
    print(f"  {row['job_code']:<15} {row['job_nm']}")

print(f"\nEXCEL Job Codes (Workday format):")
for i, rec in enumerate(excel_data['job_codes'][:10]):
    print(f"  {rec.get('SMART Job Code', 'N/A'):<15} {rec.get('Job Title', 'N/A')}")

# Check if Workday Job Code column matches Polaris codes
print("\n" + "=" * 80)
print("EXPLORING MAPPING POSSIBILITIES")
print("=" * 80)

print(f"\nChecking if Excel 'Workday Job Code' column might map to Polaris...")
excel_workday_codes = set()
for rec in excel_data['job_codes']:
    wdc = str(rec.get('Workday Job Code', '')).strip()
    if wdc:
        excel_workday_codes.add(wdc)

polaris_codes = set(polaris_df['job_code'].astype(str))

# Check for any overlap
overlap = excel_workday_codes & polaris_codes
print(f"  Excel Workday codes that match Polaris: {len(overlap)} of {len(excel_workday_codes)}")
if overlap:
    print(f"  Examples: {list(overlap)[:5]}")

# Check job name matches
print(f"\nChecking if Job Titles match between datasets...")
polaris_titles = set(polaris_df['job_nm'].str.lower())
excel_titles = set(rec.get('Job Title', '').lower() for rec in excel_data['job_codes'])
title_overlap = polaris_titles & excel_titles
print(f"  Exact job title matches: {len(title_overlap)}")
if title_overlap:
    print(f"  Examples: {list(title_overlap)[:5]}")

print("\n" + "=" * 80)
