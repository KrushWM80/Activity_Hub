#!/usr/bin/env python3
"""Simple test of the /api/projects endpoint."""

import requests
import sys

print("[TEST] Testing /api/projects endpoint...")
try:
    response = requests.get("http://localhost:8001/api/projects?limit=10", timeout=5)
    print(f"[TEST] Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"[TEST] SUCCESS! Got {len(data)} projects")
        if data:
            print(f"[TEST] First project ID: {data[0].get('project_id', 'N/A')}")
            print(f"[TEST] First project title: {data[0].get('title', 'N/A')}")
    else:
        print(f"[TEST] Error: {response.status_code}")
        print(f"[TEST] Response: {response.text[:500]}")
        
except Exception as e:
    print(f"[TEST] Connection failed: {e}")
    sys.exit(1)

print("[TEST] Test completed successfully")
