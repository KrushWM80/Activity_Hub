#!/usr/bin/env python3
"""
Debug script to see actual API response structure
"""

import urllib.request
import json

url = "http://127.0.0.1:5001/api/summary"

print("Fetching from:", url)
print()

with urllib.request.urlopen(url, timeout=5) as response:
    data = json.loads(response.read().decode())
    print(json.dumps(data, indent=2))
