#!/usr/bin/env python3
"""Test API endpoints using requests library."""

import requests
import time
import sys

time.sleep(3)  # Wait for server to start

urls = [
    "http://localhost:8001/api/summary",
    "http://localhost:8002/test",
]

for url in urls:
    print(f"Testing {url}...")
    try:
        response = requests.get(url, timeout=5)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
    except Exception as e:
        print(f"  Error: {e}")

print("Done")
