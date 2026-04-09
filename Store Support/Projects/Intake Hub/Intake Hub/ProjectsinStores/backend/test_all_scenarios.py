#!/usr/bin/env python
"""Test all filter scenarios"""
import requests
import json

BASE_URL = "http://localhost:8001"

tests = [
    ("/api/projects?limit=50000", "All projects (no filter)", 519),
    ("/api/projects?project_source=Realty&limit=50000", "Realty only", 239),
    ("/api/projects?project_source=Operations&limit=50000", "Operations only", 280),
    ("/api/projects?limit=20", "Default load (20)", 20),
]

for endpoint, label, expected_count in tests:
    print(f"\n=== TEST: {label} ===")
    print(f"Endpoint: {endpoint}")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            actual_count = len(data)
            status = "✅" if actual_count == expected_count else f"❌ (expected {expected_count})"
            print(f"Result: {actual_count} projects {status}")
            
            # Show source breakdown
            sources = {}
            for p in data:
                src = p.get('project_source', 'Unknown')
                sources[src] = sources.get(src, 0) + 1
            if sources:
                print(f"Breakdown: {sources}")
        else:
            print(f"ERROR: {response.status_code}")
    except Exception as e:
        print(f"FAILED: {e}")

# Test summary endpoint
print(f"\n=== TEST: Summary Endpoint ===")
try:
    response = requests.get(f"{BASE_URL}/api/summary", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"Realty: {data['realty_projects']} (expected 239)")
        print(f"Operations: {data['intake_hub_projects']} (expected 280)")
        print(f"Total: {data['total_active_projects']} (expected 519)")
    else:
        print(f"ERROR: {response.status_code}")
except Exception as e:
    print(f"FAILED: {e}")
