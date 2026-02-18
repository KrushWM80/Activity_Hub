import requests

r = requests.get('http://127.0.0.1:8001/api/projects?limit=3', timeout=30)
data = r.json()

if data and len(data) > 0:
    print('Testing 3 projects for extended fields:')
    for i, project in enumerate(data[:3]):
        print(f'\nProject {i+1}:')
        print(f'  title: {project.get("title", "N/A")[:40]}...')
        print(f'  business_area: {project.get("business_area", "MISSING")}')
        print(f'  store_area: {project.get("store_area", "MISSING")}')
        print(f'  owner: {project.get("owner", "MISSING")}')
else:
    print('No projects returned')
