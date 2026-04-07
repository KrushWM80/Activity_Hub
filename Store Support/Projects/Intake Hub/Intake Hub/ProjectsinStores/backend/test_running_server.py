#!/usr/bin/env python3
"""Test the running server's /api/projects endpoint."""

import requests
import time

print("[TEST] Waiting 2 seconds for server startup...")
time.sleep(2)

tests = [
    ("/api/summary", {}),
    ("/api/projects", {"limit": 10}),
    ("/api/projects", {"limit": 100}),
]

for endpoint, params in tests:
    try:
        url = f"http://localhost:8001{endpoint}"
        print(f"[TEST] GET {url} with {params}...")
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"[TEST]   SUCCESS: Got {len(data)} items")
            elif isinstance(data, dict):
                print(f"[TEST]   SUCCESS: Got dict with {len(data)} keys")
        else:
            print(f"[TEST]   Status {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"[TEST]   ERROR: {e}")

print("[TEST] Done")
