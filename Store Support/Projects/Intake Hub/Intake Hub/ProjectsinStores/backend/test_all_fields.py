import requests

# Test that all extended fields are now in the API response
print("Testing API returns all extended fields...\n")

r = requests.get('http://127.0.0.1:8001/api/projects?limit=5', timeout=10)
projects = r.json()

if len(projects) > 0:
    p = projects[0]
    print("Fields in ProjectResponse:")
    extended_fields = ['owner', 'store_area', 'business_area', 'health', 'business_type', 'associate_impact', 'customer_impact']
    
    for field in extended_fields:
        value = p.get(field, 'MISSING')
        status = "✓" if field in p else "✗"
        print(f"  {status} {field}: {value}")
    
    print(f"\nTotal fields in response: {len(p)}")
    print(f"All extended fields present: {all(field in p for field in extended_fields)}")
else:
    print("ERROR: No projects returned")
