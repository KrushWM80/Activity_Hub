"""Test API in more detail"""
import requests

tests = [
    ("Projects limit=10", "/api/projects?limit=10"),
    ("Projects limit=100", "/api/projects?limit=100"),
    ("Projects no limit", "/api/projects"),
    ("Realty limit=10", "/api/projects?project_source=Realty&limit=10"),
    ("Operations limit=10", "/api/projects?project_source=Operations&limit=10"),
]

for name, path in tests:
    print(f"\n{name}:")
    try:
        resp = requests.get(f"http://localhost:8001{path }", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                count = len(data)
                print(f"  ✓ {count} records")
                if count > 0 and 'project_source' in data[0]:
                    sources = set(p.get('project_source') for p in data)
                    print(f"    Sources: {sources}")
            elif isinstance(data, dict) and 'result' in data:
                count = len(data['result'])
                print(f"  ✓ {count} records")
                if count > 0:
                    sources = set(p.get('project_source') for p in data['result'])
                    print(f"    Sources: {sources}")
            else:
                print(f"  Key: {list(data.keys())}")
        else:
            print(f"  ✗ Status {resp.status_code}")
    except Exception as e:
        print(f"  ✗ {str(e)[:50]}")
