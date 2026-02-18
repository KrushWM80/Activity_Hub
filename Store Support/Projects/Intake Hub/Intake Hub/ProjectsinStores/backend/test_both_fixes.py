import requests

print("TESTING BOTH ISSUES AFTER FIX")
print("=" * 70)

print("\nIssue 1: Project Source vs Business Type")
print("-" * 70)

# Test both filters
r1 = requests.get('http://127.0.0.1:8001/api/projects?project_source=Realty&limit=10000', timeout=15)
source_realty = r1.json()

r2 = requests.get('http://127.0.0.1:8001/api/projects?business_type=Realty&limit=10000', timeout=15)
type_realty = r2.json()

print(f"Project Source = 'Realty': {len(source_realty)} projects")
print(f"Business Type = 'Realty': {len(type_realty)} projects")
print(f"✓ Should be similar now that both use backend filtering")

print("\n" + "=" * 70)
print("\nIssue 2: Store count when filtering")
print("-" * 70)

# Test Store 1 + Realty
r3 = requests.get('http://127.0.0.1:8001/api/projects?store=1&project_source=Realty&limit=10000', timeout=15)
filtered = r3.json()

unique_stores = set(p['store'] for p in filtered)
unique_projects = set(p['project_id'] for p in filtered)

print(f"Store=1 + Project Source=Realty:")
print(f"  Total rows: {len(filtered)}")
print(f"  Unique stores: {len(unique_stores)} {list(unique_stores)[:5]}")
print(f"  Unique projects: {len(unique_projects)}")
print(f"✓ Frontend should now show {len(unique_stores)} store(s), not {len(filtered)}")

print("\n" + "=" * 70)
print("TESTS COMPLETE")
