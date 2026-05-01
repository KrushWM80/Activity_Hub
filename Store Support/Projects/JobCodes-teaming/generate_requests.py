"""
Generate teaming requests for all 89 missing codes
9 Management + 80 other teams
"""
import pandas as pd
import json
from datetime import datetime
import os

# Load sources
polaris = pd.read_csv('Teaming/polaris_job_codes.csv')
master = pd.read_excel('Job Codes/Job_Code_Master_Table.xlsx')

# Find codes missing from TMS
tms = pd.read_csv('Teaming/TMS_Data_3_converted.csv')
polaris_codes = set(polaris['job_code'].unique())
tms_codes = set(tms['jobCode'].unique())
missing_codes = sorted(polaris_codes - tms_codes)

# Collect assignments
requests_to_create = []

print("=" * 120)
print("GENERATING TEAMING REQUESTS FOR 89 CODES")
print("=" * 120)

for code in missing_codes:
    job_name = polaris[polaris['job_code'] == code]['job_nm'].values[0] if len(polaris[polaris['job_code'] == code]) > 0 else "UNKNOWN"
    
    # Look up in master
    master_match = master[master['SMART Job Code'] == code]
    if len(master_match) == 0:
        code_stripped = code.split('-')[-1] if '-' in code else code
        master_match = master[master['SMART Job Code.1'].astype(str).str.contains(f'^{code_stripped}$', na=False, regex=True)]
    
    if len(master_match) > 0:
        row = master_match.iloc[0]
        workgroup = str(row.get('Workgroup', ''))
        team = str(row.get('Team', ''))
        
        # Determine assignment
        assigned_team = None
        reason = None
        
        # Apply logic: Coach or Manager = Management
        if ('Coach' in workgroup or 'Manager' in workgroup) and ('Pharmacy' not in workgroup and 'Vision' not in workgroup):
            assigned_team = 'Management'
            reason = f'Auto-assigned: {workgroup}'
        elif team and team != 'nan':
            assigned_team = team
            reason = f'Auto-assigned to {team} team'
        
        if assigned_team:
            requests_to_create.append({
                'code': code,
                'job_name': job_name,
                'team': assigned_team,
                'workgroup': workgroup,
                'reason': reason
            })

print(f"\nTotal requests to create: {len(requests_to_create)}")

# Count by team
teams_count = {}
for req in requests_to_create:
    team = req['team']
    teams_count[team] = teams_count.get(team, 0) + 1

print(f"\nBreakdown by team:")
for team, count in sorted(teams_count.items()):
    print(f"  {team}: {count}")

# Now create the actual request JSON objects
print("\n" + "=" * 120)
print("CREATING REQUEST OBJECTS")
print("=" * 120)

# Group by team
requests_by_team = {}
for req in requests_to_create:
    team = req['team']
    if team not in requests_by_team:
        requests_by_team[team] = []
    requests_by_team[team].append(req['code'])

# Create consolidated requests (one per team)
final_requests = []

for team, codes in requests_by_team.items():
    request_id = int(datetime.now().timestamp() * 1000)
    
    request_obj = {
        'id': request_id,
        'job_codes': codes,
        'request_type': 'job_code_update',
        'status': 'pending',
        'requested_by': 'system',
        'requested_by_name': 'System Auto-Assignment',
        'requested_at': datetime.now().isoformat(),
        'description': f'Auto-generated teaming assignment: {len(codes)} job codes assigned to {team} team based on Master table role matching',
        'comments': [],
        'history': [
            {
                'timestamp': datetime.now().isoformat(),
                'changed_by': 'system',
                'changed_by_name': 'System Auto-Assignment',
                'field': 'status',
                'old_value': None,
                'new_value': 'pending'
            }
        ]
    }
    
    final_requests.append(request_obj)
    print(f"  ✓ Team '{team}': {len(codes)} codes → Request ID {request_id}")

# Save requests to JSON file for review
output_file = 'pending_requests_to_create.json'
with open(output_file, 'w') as f:
    json.dump(final_requests, f, indent=2)

print(f"\n✓ Requests saved to: {output_file}")
print(f"  {len(final_requests)} consolidated requests ({len(requests_to_create)} total codes)")

# Show sample
print("\n" + "=" * 120)
print("SAMPLE REQUEST (first one)")
print("=" * 120)
if final_requests:
    sample = final_requests[0]
    print(json.dumps(sample, indent=2)[:500] + "...")
