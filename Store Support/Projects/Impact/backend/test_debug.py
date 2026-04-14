#!/usr/bin/env python3
import requests

# Test projects with debugging
print("=== Testing Projects Endpoint ===")
r = requests.get('http://localhost:8002/api/impact/projects')
print(f"Status Code: {r.status_code}")
print(f"Response Headers: {r.headers}")
print(f"Response Text: {r.text[:500]}")
