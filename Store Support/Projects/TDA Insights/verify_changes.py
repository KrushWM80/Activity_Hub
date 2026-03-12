import urllib.request, json
raw = json.loads(urllib.request.urlopen('http://localhost:5000/api/data').read())
print(f"Type: {type(raw)}")
if isinstance(raw, dict):
    print(f"Keys: {list(raw.keys())}")
    d = raw.get('data', raw.get('results', []))
else:
    d = raw
print(f"Total records: {len(d)}")
print(f"\nColumn keys: {list(d[0].keys())}")
print(f"\nProjects with # of Stores <= 2:")
low = [r for r in d if r['# of Stores'] <= 2]
for r in low[:20]:
    print(f"  {r['Initiative - Project Title']}: {r['# of Stores']} stores")
print(f"\n... total {len(low)} projects with stores <= 2")
print(f"\nProjects with stores > 2:")
high = [r for r in d if r['# of Stores'] > 2]
for r in high:
    print(f"  {r['Initiative - Project Title']}: {r['# of Stores']} stores")
