#!/usr/bin/env python3
"""Test /api/summary endpoint."""

import requests
import sys

print("[TEST] Testing /api/summary endpoint...")
try:
    response = requests.get("http://localhost:8001/api/summary", timeout=5)
    print(f"[TEST] Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"[TEST] SUCCESS!")
        print(f"[TEST] Total projects: {data.get('total_active_projects', 'N/A')}")
        print(f"[TEST] Realty projects: {data.get('realty_projects', 'N/A')}")
    else:
        print(f"[TEST] Error: {response.status_code}")
        print(f"[TEST] Response: {response.text[:500]}")
        
except Exception as e:
    print(f"[TEST] Connection failed: {e}")
    sys.exit(1)

print("[TEST] Test completed")
