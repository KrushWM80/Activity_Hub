#!/usr/bin/env python3
import requests
import json

# Test metrics
print("=== Testing Metrics Endpoint ===")
r = requests.get('http://localhost:8002/api/impact/metrics')
print(json.dumps(r.json(), indent=2))

# Test projects
print("\n=== Testing Projects Endpoint ===")
r = requests.get('http://localhost:8002/api/impact/projects')
projects = r.json()
print(f"Projects returned: {len(projects)}")
for p in projects:
    print(f"  - {p.get('title')} ({p.get('business_area')}) - Health: {p.get('health_status')}")
