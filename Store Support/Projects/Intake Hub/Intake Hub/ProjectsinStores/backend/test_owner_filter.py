import requests

# Test owner filter in backend
print("Testing backend owner filter...")
r = requests.get('http://127.0.0.1:8001/api/projects?owner=Crystal Souders', timeout=15)
projects = r.json()

print(f"Status: {r.status_code}")
print(f"Projects returned: {len(projects)}")

if len(projects) > 0:
    print(f"\nAll projects have owner='Crystal Souders': {all(p.get('owner') == 'Crystal Souders' for p in projects)}")
    print(f"First 5 projects:")
    for p in projects[:5]:
        print(f"  - {p['title'][:50]} | Phase: {p['phase']} | Owner: {p['owner']}")
else:
    print("ERROR: No projects returned")
