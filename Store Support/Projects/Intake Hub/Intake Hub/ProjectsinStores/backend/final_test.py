import requests
import json

r = requests.get('http://127.0.0.1:8001/api/filters', timeout=10)
data = r.json()

print(f'Status: {r.status_code}')
print(f'Fields returned: {len(data)}')
print(f'Field names:')
for k in sorted(data.keys()):
    print(f'  - {k}: {len(data[k])} values')

print()
if len(data) == 16:
    print('✅ SUCCESS! All 16 filter categories are now returned!')
else:
    print(f'❌ Still missing {16 - len(data)} fields')
    expected = {'associate_impacts', 'business_areas', 'business_types', 'customer_impacts', 
                'divisions', 'fiscal_years', 'health_statuses', 'markets', 'owners', 'phases', 
                'project_sources', 'regions', 'store_areas', 'stores', 'tribes', 'wm_weeks'}
    returned = set(data.keys())
    missing = expected - returned
    print(f'Missing: {missing}')
