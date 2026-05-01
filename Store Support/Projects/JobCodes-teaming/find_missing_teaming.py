"""
Find missing teaming codes and auto-assign based on Coach/Manager logic
"""
import pandas as pd

# Load sources
polaris = pd.read_csv('Teaming/polaris_job_codes.csv')
tms = pd.read_csv('Teaming/TMS_Data_3_converted.csv')
master = pd.read_excel('Job Codes/Job_Code_Master_Table.xlsx')

# Find codes missing from TMS
polaris_codes = set(polaris['job_code'].unique())
tms_codes = set(tms['jobCode'].unique())
missing_codes = sorted(polaris_codes - tms_codes)

print("=" * 120)
print("MISSING TEAMING ASSIGNMENTS - AUTO-MATCHING ANALYSIS")
print("=" * 120)
print(f"\nTotal Polaris codes: {len(polaris_codes)}")
print(f"Total with TMS teaming: {len(tms_codes)}")
print(f"Missing teaming assignments: {len(missing_codes)}")

# Apply matching logic
auto_assign_management = []
other_matches = []
no_matches = []

print("\n" + "=" * 120)
print("APPLYING ASSIGNMENT LOGIC")
print("=" * 120)

for code in missing_codes:
    job_name = polaris[polaris['job_code'] == code]['job_nm'].values[0] if len(polaris[polaris['job_code'] == code]) > 0 else "UNKNOWN"
    
    # Look up in master - try both columns (SMART Job Code and SMART Job Code.1)
    master_match = master[master['SMART Job Code'] == code]
    if len(master_match) == 0:
        # Try the second code column (remove prefix if present)
        code_stripped = code.split('-')[-1] if '-' in code else code
        master_match = master[master['SMART Job Code.1'].astype(str).str.contains(f'^{code_stripped}$', na=False, regex=True)]
    
    if len(master_match) > 0:
        row = master_match.iloc[0]
        workgroup = str(row.get('Workgroup', ''))
        team = str(row.get('Team', ''))
        
        # Apply logic: Coach or Manager = Management
        if ('Coach' in workgroup or 'Manager' in workgroup) and ('Pharmacy' not in workgroup and 'Vision' not in workgroup):
            auto_assign_management.append({
                'code': code,
                'job_name': job_name,
                'workgroup': workgroup,
                'team': team,
                'assignment': 'Management'
            })
        elif workgroup and workgroup != 'nan' and workgroup != 'nan':
            # Has workgroup but doesn't match Coach/Manager
            other_matches.append({
                'code': code,
                'job_name': job_name,
                'workgroup': workgroup,
                'team': team,
                'assignment': f'Assign to {team if team and team != "nan" else "REVIEW"}'
            })
        else:
            no_matches.append({
                'code': code,
                'job_name': job_name,
                'workgroup': workgroup or 'NO WORKGROUP',
                'team': team or 'NO TEAM',
                'assignment': 'SKIP - No role data'
            })
    else:
        no_matches.append({
            'code': code,
            'job_name': job_name,
            'workgroup': 'NOT IN MASTER',
            'team': 'N/A',
            'assignment': 'SKIP - Not in master'
        })

print(f"\n✓ AUTO-ASSIGN TO MANAGEMENT ({len(auto_assign_management)} codes):")
print("-" * 120)
if auto_assign_management:
    for item in auto_assign_management[:15]:  # Show first 15
        print(f"  {item['code']:15} | {item['job_name'][:50]:50} | {item['workgroup'][:35]}")
    if len(auto_assign_management) > 15:
        print(f"  ... and {len(auto_assign_management) - 15} more")
else:
    print("  (none)")

print(f"\n? OTHER MATCHES ({len(other_matches)} codes - need review):")
print("-" * 120)
if other_matches:
    for item in other_matches[:10]:
        print(f"  {item['code']:15} | {item['job_name'][:50]:50} | {item['workgroup'][:35]}")
    if len(other_matches) > 10:
        print(f"  ... and {len(other_matches) - 10} more")
else:
    print("  (none)")

print(f"\n✗ NO MATCH / SKIP ({len(no_matches)} codes):")
print("-" * 120)
if no_matches:
    for item in no_matches[:10]:
        print(f"  {item['code']:15} | {item['job_name'][:50]:50} | {item['assignment']}")
    if len(no_matches) > 10:
        print(f"  ... and {len(no_matches) - 10} more")
else:
    print("  (none)")

print(f"\n" + "=" * 120)
print("SUMMARY")
print("=" * 120)
print(f"Auto-assign to Management: {len(auto_assign_management)}")
print(f"Other potential matches: {len(other_matches)}")
print(f"No assignment possible: {len(no_matches)}")
print(f"TOTAL: {len(auto_assign_management) + len(other_matches) + len(no_matches)}")
