#!/usr/bin/env python3
import requests
import json

try:
    response = requests.get('http://localhost:8001/api/filters', timeout=5)
    data = response.json()
    
    print(f"Status Code: {response.status_code}")
    print(f"\nTotal Fields: {len(data.keys())}")
    print(f"\nField Names:")
    for field_name in sorted(data.keys()):
        field_count = len(data[field_name]) if isinstance(data[field_name], list) else "N/A"
        print(f"  - {field_name}: {field_count} items")
        
    print(f"\nFull Response:")
    print(json.dumps(data, indent=2))
    
except Exception as e:
    print(f"Error: {e}")
