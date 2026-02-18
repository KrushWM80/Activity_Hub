import json
import urllib.request

try:
    req = urllib.request.Request('http://127.0.0.1:8001/api/filters')
    with urllib.request.urlopen(req, timeout=30) as response:
        body = response.read().decode('utf-8')
        data = json.loads(body)
        
        print(f"HTTP Response Fields: {len(data)} total")
        print(f"Fields: {sorted(data.keys())}")
        
        # Check which fields are missing
        all_expected = {'tribes', 'stores', 'project_sources', 'markets', 'regions', 'divisions', 
                       'phases', 'fiscal_years', 'wm_weeks', 'owners', 'store_areas', 
                       'business_areas', 'health_statuses', 'business_types', 'associate_impacts', 'customer_impacts'}
        actual = set(data.keys())
        missing = all_expected - actual
        
        print(f"\nMissing fields ({len(missing)}):")
        for m in sorted(missing):
            print(f"  - {m}")
        
        # Check body length
        print(f"\nBody size: {len(body)} bytes")
        print(f"First 200 chars: {body[:200]}")
        
except Exception as e:
    print(f"Error: {e}")
