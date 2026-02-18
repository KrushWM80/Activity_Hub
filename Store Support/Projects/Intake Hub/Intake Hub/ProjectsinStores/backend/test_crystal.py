import requests

# Test 1: Get all projects and search for Crystal Souders
print("Test 1: Searching for Crystal Souders in all projects...")
r = requests.get('http://127.0.0.1:8001/api/projects', timeout=10)
all_projects = r.json()

crystal_projects = [p for p in all_projects if p.get('owner') == 'Crystal Souders']
print(f"Found {len(crystal_projects)} projects with owner='Crystal Souders'")

for p in crystal_projects:
    print(f"  - {p['title'][:50]} | Phase: {p['phase']} | Source: {p['project_source']}")

# Test 2: Check if backend supports owner filter
print("\nTest 2: Testing if /api/projects accepts owner parameter...")
try:
    r2 = requests.get('http://127.0.0.1:8001/api/projects?owner=Crystal Souders', timeout=10)
    filtered = r2.json()
    print(f"Backend returned {len(filtered)} projects when owner='Crystal Souders' passed")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Check all distinct owners
owners = set(p.get('owner') for p in all_projects if p.get('owner'))
crystal_variations = [o for o in owners if 'crystal' in o.lower() and 'souder' in o.lower()]
print(f"\nTest 3: Name variations found: {crystal_variations}")
