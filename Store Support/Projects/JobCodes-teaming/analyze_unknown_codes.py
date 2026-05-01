"""
Analyze unknown job codes to understand teaming assignment patterns
"""
import pandas as pd

# Load master data
master = pd.read_excel('Job Codes/Job_Code_Master_Table.xlsx')
export = pd.read_csv('teaming_all_actions_2026-04-27_with_roles.csv')

# Get unknown codes from export
unknowns = export[export['roleTitle'] == 'Unknown']
unknown_codes = unknowns['jobCode'].unique()

print("=" * 100)
print("UNKNOWN JOB CODES ANALYSIS")
print("=" * 100)
print(f"\nTotal unknown codes: {len(unknown_codes)}")
print(f"Total unknown records: {len(unknowns)}")

# Search master for these codes
print("\n" + "=" * 100)
print("CODE LOOKUP IN MASTER TABLE")
print("=" * 100)
print(f"{'Code':>8} | {'Workgroup (Role)':50} | {'Team':20}")
print("-" * 100)

found_count = 0
found_with_role = 0
for code in sorted(unknown_codes):
    matches = master[master['SMART Job Code.1'].astype(str).str.contains(str(code), na=False)]
    if len(matches) > 0:
        found_count += 1
        for _, row in matches.iterrows():
            workgroup = str(row.get('Workgroup', 'N/A'))[:50]
            team = str(row.get('Team', 'N/A'))[:20]
            print(f"{code:>8} | {workgroup:50} | {team:20}")
            if workgroup != 'N/A' and workgroup != 'nan':
                found_with_role += 1
    else:
        print(f"{code:>8} | {'NOT FOUND IN MASTER':50} | {'-':20}")

print(f"\nFound in master: {found_count}/{len(unknown_codes)}")
print(f"Found with Workgroup role info: {found_with_role}/{found_count}")

# Analyze by current team assignment
print("\n" + "=" * 100)
print("UNKNOWN CODES GROUPED BY CURRENT TEAM ASSIGNMENT")
print("=" * 100)

for team in sorted(unknowns['teamName'].unique()):
    team_codes = unknowns[unknowns['teamName'] == team]['jobCode'].unique()
    print(f"\n{team} ({len(team_codes)} codes):")
    for code in sorted(team_codes):
        matches = master[master['SMART Job Code.1'].astype(str).str.contains(str(code), na=False)]
        if len(matches) > 0:
            workgroup = matches.iloc[0].get('Workgroup', 'N/A')
            print(f"  {code}: {workgroup}")
        else:
            print(f"  {code}: NOT FOUND IN MASTER")

# Check which have "Coach" or "Manager" in their titles
print("\n" + "=" * 100)
print("ANALYSIS: Which codes match Coach/Manager pattern")
print("=" * 100)

coach_or_mgr = []
for code in unknown_codes:
    matches = master[master['SMART Job Code.1'].astype(str).str.contains(str(code), na=False)]
    if len(matches) > 0:
        workgroup = str(matches.iloc[0].get('Workgroup', ''))
        if 'Coach' in workgroup or 'Manager' in workgroup:
            # Check if Pharmacy or Vision
            if 'Pharmacy' not in workgroup and 'Vision' not in workgroup:
                coach_or_mgr.append((code, workgroup, 'Management'))
            else:
                coach_or_mgr.append((code, workgroup, 'SKIP - Has Pharmacy/Vision'))
        else:
            # Try keyword matching for other teams
            coach_or_mgr.append((code, workgroup, 'CHECK - No Coach/Manager'))

print(f"\nCodes analysis:")
assigned_to_mgmt = []
for code, workgroup, status in sorted(coach_or_mgr):
    if status == 'Management':
        print(f"  ✓ {code}: {workgroup} → ASSIGN to Management")
        assigned_to_mgmt.append(code)
    elif status == 'SKIP - Has Pharmacy/Vision':
        print(f"  ✗ {code}: {workgroup} → {status}")
    else:
        print(f"  ? {code}: {workgroup} → {status}")

print(f"\n\nSummary:")
print(f"  Auto-assign to Management: {len(assigned_to_mgmt)} codes")
print(f"  Skip (Pharmacy/Vision): {len([x for x in coach_or_mgr if 'SKIP' in x[2]])} codes")
print(f"  Need review/matching: {len([x for x in coach_or_mgr if 'CHECK' in x[2]])} codes")
