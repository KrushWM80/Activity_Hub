import requests

print("Detailed analysis of Issue 1\n")
print("=" * 70)

# Get enough projects to analyze both filters
r = requests.get('http://127.0.0.1:8001/api/projects?limit=10000', timeout=20)
all_projects = r.json()

# Count by project_source
source_realty = [p for p in all_projects if p.get('project_source') == 'Realty']
source_operations = [p for p in all_projects if p.get('project_source') == 'Operations']

print(f"By Project Source field:")
print(f"  project_source='Realty': {len(source_realty)} projects")
print(f"  project_source='Operations': {len(source_operations)} projects")
print()

# Count by business_type
type_realty = [p for p in all_projects if p.get('business_type') == 'Realty']
type_store_support = [p for p in all_projects if p.get('business_type') == 'Store Support']
type_none = [p for p in all_projects if not p.get('business_type') or p.get('business_type') == '']

print(f"By Business Type field:")
print(f"  business_type='Realty': {len(type_realty)} projects")
print(f"  business_type='Store Support': {len(type_store_support)} projects")
print(f"  business_type=None/Empty: {len(type_none)} projects")
print()

# Show what business_type values exist in project_source='Realty' projects
if len(source_realty) > 0:
    bt_in_realty = {}
    for p in source_realty[:1000]:  # Sample first 1000
        bt = p.get('business_type') or 'None/Empty'
        bt_in_realty[bt] = bt_in_realty.get(bt, 0) + 1
    
    print("Business Type values in project_source='Realty' (sample):")
    for bt, count in sorted(bt_in_realty.items(), key=lambda x: -x[1]):
        print(f"  {bt}: {count}")

print("\n" + "=" * 70)
print("\nConclusion:")
print("- 'Project Source' and 'Business Type' are DIFFERENT fields")
print("- Project Source indicates where the data comes from (Operations vs Realty)")
print("- Business Type indicates the type of project (Realty, Store Support, etc.)")
print("- They should NOT produce the same count!")
