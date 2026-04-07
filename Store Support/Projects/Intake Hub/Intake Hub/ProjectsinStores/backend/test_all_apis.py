"""Test API endpoints"""
import requests
import time

endpoints = [
    ("Summary", "http://localhost:8001/api/summary"),
    ("Filters", "http://localhost:8001/api/filters"),
    ("Projects (all)", "http://localhost:8001/api/projects?limit=100"),
    ("Projects (Realty)", "http://localhost:8001/api/projects?project_source=Realty&limit=100"),
]

for name, url in endpoints:
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        start = time.time()
        resp = requests.get(url, timeout=10)
        elapsed = time.time() - start
        
        print(f"Status: {resp.status_code}")
        print(f"Time: {elapsed:.1f}s")
        
        if resp.status_code == 200:
            try:
                data = resp.json()
                if isinstance(data, dict):
                    if 'result' in data:
                        print(f"Count: {len(data['result'])}")
                    elif 'project_sources' in data:
                        print(f"Project sources: {data.get('project_sources', [])}")
                    else:
                        print(f"Keys: {list(data.keys())[:5]}...")
                elif isinstance(data, list):
                    print(f"Count: {len(data)}")
            except:
                print(f"Response (first 200 chars): {resp.text[:200]}")
        else:
            print(f"Error: {resp.text[:200]}")
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT - API is very slow or stuck")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect - backend not running on port 8001")
    except Exception as e:
        print(f"❌ Error: {e}")
