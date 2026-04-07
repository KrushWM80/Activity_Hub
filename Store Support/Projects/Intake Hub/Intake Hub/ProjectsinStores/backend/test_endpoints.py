#!/usr/bin/env python3
"""Test debug endpoint and main endpoint."""

import requests
import time

time.sleep(2)

print("[TEST] Testing debug endpoint...")
try:
    r = requests.get("http://localhost:8001/api/projects-debug?limit=5", timeout=10)
    print(f"  Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"  Got {len(data)} items")
        if data and isinstance(data, list):
            print(f"  First item: {data[0].get('project_id', 'N/A')}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n[TEST] Testing main endpoint...")
try:
    r = requests.get("http://localhost:8001/api/projects?limit=5", timeout=10)
    print(f"  Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"  Got {len(data)} items")
        if data and isinstance(data, list):
            print(f"  First item: {data[0].get('project_id', 'N/A')}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n[TEST] Testing summary endpoint...")
try:
    r = requests.get("http://localhost:8001/api/summary", timeout=10)
    print(f"  Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"  Realty: {data.get('realty_projects', 'N/A')}")
        print(f"  Operations: {data.get('intake_hub_projects', 'N/A')}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n[TEST] Done")
