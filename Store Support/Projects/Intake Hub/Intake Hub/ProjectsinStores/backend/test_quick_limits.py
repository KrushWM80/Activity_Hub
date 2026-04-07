#!/usr/bin/env python3
"""Quick test of different limit values."""

import requests
import json

print("Testing /api/projects with different limits...")
for limit in [10, 50, 100, 500, 1000]:
    try:
        response = requests.get(f"http://localhost:8001/api/projects?limit={limit}", timeout=10)
        data = response.json()
        count = len(data)
        print(f"limit={limit:4d}: Got {count:4d} projects", end="")
        if count > 0:
            print(f" | Sample: {data[0]['project_id']}")
        else:
            print()
    except Exception as e:
        print(f"limit={limit}: Error - {e}")

print("\nTesting /api/summary to see totals...")
try:
    response = requests.get("http://localhost:8001/api/summary", timeout=10)
    summary = response.json()
    print(f"Total active projects: {summary.get('total_active_projects', 'N/A')}")
    print(f"Intake Hub projects: {summary.get('intake_hub_projects', 'N/A')}")
    print(f"Realty projects: {summary.get('realty_projects', 'N/A')}")
except Exception as e:
    print(f"Error: {e}")
