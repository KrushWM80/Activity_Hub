import requests
import json

try:
    r = requests.get('http://localhost:8001/api/projects?limit=3')
    print(f"Status: {r.status_code}")
    projects = r.json()
    print(f"Total projects: {len(projects)}\n")
    print("Full response structure:")
    print(json.dumps(projects[:1], indent=2))
        
except Exception as e:
    print(f"Error: {e}")
