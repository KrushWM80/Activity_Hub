"""
Load generated requests into dashboard storage
"""
import json
import os

# Load the generated requests
with open('pending_requests_to_create.json', 'r') as f:
    new_requests = json.load(f)

# Load existing requests
requests_file = 'Teaming/dashboard/data/job_code_requests.json'

if os.path.exists(requests_file):
    with open(requests_file, 'r') as f:
        existing_requests = json.load(f)
else:
    existing_requests = []

print("=" * 100)
print("LOADING REQUESTS INTO DASHBOARD")
print("=" * 100)
print(f"\nExisting requests: {len(existing_requests)}")
print(f"New requests to add: {len(new_requests)}")

# Add new requests
all_requests = existing_requests + new_requests

# Save back
with open(requests_file, 'w') as f:
    json.dump(all_requests, f, indent=2)

print(f"Total requests after adding: {len(all_requests)}")
print(f"\n✓ Saved to: {requests_file}")

# Summary
print("\n" + "=" * 100)
print("REQUEST SUMMARY")
print("=" * 100)

total_codes = 0
for req in new_requests:
    print(f"  Team: {req['description'].split(': ')[-1].split(' job')[0]:30} | Codes: {len(req['job_codes']):2} | ID: {req['id']}")
    total_codes += len(req['job_codes'])

print(f"\nTotal codes in new requests: {total_codes}")

# Show which teams got requests
print(f"\nTeams assigned:")
teams = {}
for req in new_requests:
    desc = req['description']
    team = desc.split("assigned to ")[-1].split(" team")[0]
    teams[team] = len(req['job_codes'])

for team in sorted(teams.keys()):
    print(f"  {team}: {teams[team]} codes")
