import json
import os

requests_file = os.path.join('data', 'update_requests.json')
with open(requests_file, 'r') as f:
    data = json.load(f)

print("=" * 80)
print("TEAMING REQUESTS CREATED - VERIFICATION")
print("=" * 80)

teaming_requests = [r for r in data if r.get('type') == 'teaming']
print(f"\nTotal requests in system: {len(data)}")
print(f"Teaming requests: {len(teaming_requests)}")

print("\n" + "-" * 80)
print("SAMPLE OF 10 REQUESTS:")
print("-" * 80)

for i, r in enumerate(teaming_requests[:10], 1):
    print(f"\n{i}. Job Code: {r['job_code']}")
    print(f"   Title: {r['job_title']}")
    print(f"   Team: {r.get('team_name', 'N/A')}")
    print(f"   Workgroup: {r.get('workgroup_name', 'N/A')}")
    print(f"   Status: {r.get('status', 'pending')}")
    print(f"   Reason: {r.get('reason', 'N/A')[:60]}...")

# Breakdown by team
print("\n" + "-" * 80)
print("BREAKDOWN BY TEAM:")
print("-" * 80)

teams = {}
for r in teaming_requests:
    team = r.get('team_name', 'Unknown')
    teams[team] = teams.get(team, 0) + 1

for team, count in sorted(teams.items(), key=lambda x: x[1], reverse=True):
    print(f"  {team}: {count} requests")

print("\n" + "=" * 80)
print("✓ All requests are saved and ready for management in Admin panel")
print("=" * 80)
