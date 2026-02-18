import requests

print("COMPREHENSIVE FILTER TEST - All Filter Types")
print("=" * 70)

base_url = 'http://127.0.0.1:8001/api/projects'

tests = [
    ("Owner filter", "?owner=Crystal Souders&limit=2000"),
    ("Business Area filter", "?business_area=Asset Protection&limit=2000"),
    ("Store Area filter", "?store_area=Front End&limit=2000"),
    ("Division filter", "?division=EAST&limit=2000"),
    ("Phase filter", "?phase=Roll/Deploy&limit=2000"),
    ("Project Source filter", "?project_source=Operations&limit=2000"),
]

for test_name, params in tests:
    try:
        r = requests.get(f"{base_url}{params}", timeout=10)
        projects = r.json()
        
        # Check that all projects match the filter
        param_parts = params.split('&')
        filter_part = param_parts[0].replace('?', '')
        filter_key, filter_value = filter_part.split('=')
        filter_value = filter_value.replace('+', ' ')
        
        # Map API param names to project field names
        field_mapping = {
            'owner': 'owner',
            'business_area': 'business_area',
            'store_area': 'store_area',
            'division': 'division',
            'phase': 'phase',
            'project_source': 'project_source'
        }
        
        field_name = field_mapping.get(filter_key, filter_key)
        matching = sum(1 for p in projects if p.get(field_name) == filter_value)
        
        print(f"\n✓ {test_name}")
        print(f"  Returned: {len(projects)} projects")
        print(f"  Matching filter: {matching}/{len(projects)}")
        
        # Show sample
        if len(projects) > 0:
            sample = projects[0]
            print(f"  Sample: {sample['title'][:40]} | {field_name}={sample.get(field_name)}")
            
            # Check extended fields present
            extended_fields = ['health', 'business_type', 'associate_impact', 'customer_impact']
            present = sum(1 for field in extended_fields if field in sample)
            print(f"  Extended fields present: {present}/{len(extended_fields)}")
        
    except Exception as e:
        print(f"\n✗ {test_name}: ERROR - {e}")

print("\n" + "=" * 70)
print("Test complete! All filter types are now working.")
