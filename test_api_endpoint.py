#!/usr/bin/env python3
"""
Test the /api/projects endpoint to catch errors
"""

import requests
import json

url = "http://localhost:8088/api/projects?limit=5"

try:
    print(f"Testing: {url}")
    response = requests.get(url, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ SUCCESS - Endpoint working")
        print(f"   Projects returned: {len(data.get('projects', []))}")
        if data.get('projects'):
            p = data['projects'][0]
            print(f"   Sample project keys: {list(p.keys())}")
            print(f"   is_updated_this_week: {p.get('is_updated_this_week')}")
    else:
        print(f"\n❌ ERROR - Status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ EXCEPTION: {e}")
