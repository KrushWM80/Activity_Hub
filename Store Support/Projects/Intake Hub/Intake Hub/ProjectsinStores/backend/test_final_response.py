import requests

response = requests.get('http://127.0.0.1:8001/api/filters', timeout=120)
data = response.json()
print(f'Status: {response.status_code}')
print(f'Fields returned: {list(data.keys())}')
print(f'Field count: {len(data.keys())}')
print(f'Owners count: {len(data.get("owners", []))}')

if len(data.keys()) == 16:
    print("\n✓ SUCCESS: All 16 fields returned!")
else:
    print(f"\n✗ FAILED: Expected 16 fields, got {len(data.keys())}")
    print(f"Missing fields from expected:")
    expected = {'associates', 'tribes', 'stores', 'regions', 'markets', 'divisions', 'phases', 
                'fiscal_years', 'project_sources', 'owners', 'store_areas', 'business_areas', 
                'health_statuses', 'business_types', 'associate_impacts', 'customer_impacts'}
    actual = set(data.keys())
    print(f"Missing: {expected - actual}")
