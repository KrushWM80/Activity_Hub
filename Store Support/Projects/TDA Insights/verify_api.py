"""Verify API data after store count fix"""
import urllib.request
import json

r = urllib.request.urlopen('http://localhost:5000/api/data')
resp = json.loads(r.read())
d = resp['data'] if isinstance(resp, dict) and 'data' in resp else resp
print(f"Total records: {len(d)}")

# Check Body Worn Cameras store count
bwc = [x for x in d if 'Body Worn' in x['Initiative - Project Title']]
if bwc:
    print(f"Body Worn Cameras stores: {bwc[0]['# of Stores']} (expected: 167)")

# Check Spill Station
spill = [x for x in d if 'Spill' in x['Initiative - Project Title']]
if spill:
    print(f"Spill Station stores: {spill[0]['# of Stores']} (expected: 4442)")

# Check MyWalmart 2.0
mw = [x for x in d if 'MyWalmart 2.0' in x['Initiative - Project Title']]
if mw:
    print(f"MyWalmart 2.0 stores: {mw[0]['# of Stores']} (expected: 4449)")

# Phase counts
phases = {}
for x in d:
    p = x['Phase']
    phases[p] = phases.get(p, 0) + 1
print(f"\nPhase breakdown: {phases}")

# Health counts
health = {}
for x in d:
    h = x['Health Status']
    health[h] = health.get(h, 0) + 1
print(f"Health breakdown: {health}")

# Show top 5 store counts
sorted_d = sorted(d, key=lambda x: x['# of Stores'], reverse=True)
print("\nTop 10 by store count:")
for item in sorted_d[:10]:
    print(f"  {item['Initiative - Project Title']:<50} Stores={item['# of Stores']}")

# Show zeros
zeros = [x for x in d if x['# of Stores'] == 0]
print(f"\nProjects with 0 stores: {len(zeros)}")

# Check Project IDs for hyperlinks
with_id = [x for x in d if x.get('Project ID')]
print(f"\nProjects with Project ID: {len(with_id)} / {len(d)}")
print("Sample links:")
for item in d[:5]:
    pid = item.get('Project ID', 'NONE')
    print(f"  {item['Initiative - Project Title'][:45]:<47} ID={pid}  Link=https://hoops.wal-mart.com/intake-hub/projects/{pid}")
