#!/usr/bin/env python
"""Test the API endpoints with fixed query"""
import requests
import json
import time

BASE_URL = "http://localhost:8001"
time.sleep(2)  # Give server time to fully start

print("=== TEST 1: GET /api/summary ===")
try:
    response = requests.get(f"{BASE_URL}/api/summary", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"ERROR: {response.status_code} {response.text}")
except Exception as e:
    print(f"FAILED: {e}")

print("\n=== TEST 2: GET /api/projects (no filter) ===")
try:
    response = requests.get(f"{BASE_URL}/api/projects?limit=10", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"Got {len(data)} projects")
        if data:
            print(f"First project: {data[0]}")
    else:
        print(f"ERROR: {response.status_code} {response.text}")
except Exception as e:
    print(f"FAILED: {e}")

print("\n=== TEST 3: GET /api/projects?project_source=Realty ===")
try:
    response = requests.get(f"{BASE_URL}/api/projects?project_source=Realty&limit=50000", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"Got {len(data)} Realty projects (expected 239)")
        # Group by title to verify
        titles = set()
        for p in data:
            titles.add(p.get('title'))
        print(f"Unique titles: {len(titles)} (expected 239)")
    else:
        print(f"ERROR: {response.status_code} {response.text}")
except Exception as e:
    print(f"FAILED: {e}")

print("\n=== TEST 4: GET /api/projects?project_source=Operations ===")
try:
    response = requests.get(f"{BASE_URL}/api/projects?project_source=Operations&limit=50000", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"Got {len(data)} Operations projects (expected 280)")
    else:
        print(f"ERROR: {response.status_code} {response.text}")
except Exception as e:
    print(f"FAILED: {e}")
