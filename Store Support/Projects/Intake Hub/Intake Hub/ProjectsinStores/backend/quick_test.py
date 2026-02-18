#!/usr/bin/env python3
import requests
import json

response = requests.get('http://localhost:8001/api/filters')
data = response.json()
print(f"Fields returned: {list(data.keys())}")
print(f"Total count: {len(data.keys())}")
