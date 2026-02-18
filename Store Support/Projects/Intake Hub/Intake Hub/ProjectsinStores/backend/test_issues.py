import requests

print("Issue 1: Testing Project Source vs Business Type filters\n")
print("=" * 70)

# Test Project Source = Realty
r1 = requests.get('http://127.0.0.1:8001/api/projects?project_source=Realty&limit=5000', timeout=15)
source_realty = r1.json()

# Test Business Type = Realty
r2 = requests.get('http://127.0.0.1:8001/api/projects?limit=5000', timeout=15)
all_projects = r2.json()

# Filter client-side for business_type=Realty
type_realty = [p for p in all_projects if p.get('business_type') == 'Realty']

print(f"Project Source = Realty: {len(source_realty)} projects")
print(f"Business Type = Realty: {len(type_realty)} projects")
print()

# Show samples
if len(source_realty) > 0:
    print("Sample Project Source=Realty:")
    p = source_realty[0]
    print(f"  Title: {p['title'][:50]}")
    print(f"  project_source: {p['project_source']}")
    print(f"  business_type: {p.get('business_type')}")
    print()

if len(type_realty) > 0:
    print("Sample Business Type=Realty:")
    p = type_realty[0]
    print(f"  Title: {p['title'][:50]}")
    print(f"  project_source: {p['project_source']}")
    print(f"  business_type: {p.get('business_type')}")
    print()

print("=" * 70)
print("\nIssue 2: Testing Store filter with store count\n")
print("=" * 70)

# Test Store 1 + Project Source Realty
r3 = requests.get('http://127.0.0.1:8001/api/projects?store=1&project_source=Realty&limit=5000', timeout=15)
filtered = r3.json()

print(f"Store=1 + Project Source=Realty: {len(filtered)} projects")

if len(filtered) > 0:
    # Count unique stores
    unique_stores = set(p['store'] for p in filtered)
    print(f"Unique stores in results: {len(unique_stores)}")
    print(f"Store values: {list(unique_stores)[:10]}")
    
    # Show project details
    for p in filtered[:3]:
        print(f"\nProject: {p['title'][:50]}")
        print(f"  Store: {p['store']}")
        print(f"  Store Count: {p['store_count']}")
        print(f"  Source: {p['project_source']}")
