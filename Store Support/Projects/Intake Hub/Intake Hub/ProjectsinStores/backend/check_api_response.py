#!/usr/bin/env python3
"""Check what the API is returning after the sync"""

import requests
import json
from datetime import datetime

print("=== API DATA CHECK ===\n")

try:
    response = requests.get("http://localhost:8001/api/summary")
    data = response.json()
    
    print("API /api/summary response:")
    print(json.dumps(data, indent=2))
    
    print("\n=== VERIFICATION ===")
    print(f"Total Projects: {data.get('total_projects', 'N/A')}")
    print(f"  - Operations: {data.get('intake_hub_projects', 'N/A')}")
    print(f"  - Realty: {data.get('realty_projects', 'N/A')}")
    print(f"\nTotal Stores: {data.get('total_stores', 'N/A')}")
    print(f"  - Operations: {data.get('intake_hub_stores', 'N/A')}")
    print(f"  - Realty: {data.get('realty_stores', 'N/A')}")
    print(f"\nData freshness: {data.get('last_updated', 'N/A')}")
    
except Exception as e:
    print(f"Error connecting to API: {e}")
    print("\nNote: Make sure the backend server is running on port 8001")
    print("Run: python main.py  (in the backend directory)")
