#!/usr/bin/env python3
"""Test all three failing endpoints"""

import requests
import json

endpoints = [
    "http://localhost:8088/api/projects?limit=5",
    "http://localhost:8088/api/projects/metrics",
    "http://localhost:8088/api/business-areas"
]

for url in endpoints:
    print(f"\n{'='*80}")
    print(f"Testing: {url}")
    print('='*80)
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
    except Exception as e:
        print(f"Exception: {e}")
