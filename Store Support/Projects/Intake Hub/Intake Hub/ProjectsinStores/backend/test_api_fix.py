import requests
import json

try:
    r = requests.get('http://localhost:8001/api/projects?limit=10')
    print(f"Status: {r.status_code}")
    projects = r.json()
    print(f"Total projects returned: {len(projects)}")
    print("\nFirst 5 projects:")
    for i, p in enumerate(projects[:5], 1):
        print(f"  {i}. {p.get('project_name', 'N/A')}")
    
    # Check if these are REAL projects (not "Store Renovation Project")
    if any("Store Renovation Project" in p.get('project_name', '') for p in projects):
        print("\n⚠️  WARNING: Still seeing mock projects!")
    else:
        print("\n✅ SUCCESS: Real projects returned!")
        
except Exception as e:
    print(f"Error: {e}")
