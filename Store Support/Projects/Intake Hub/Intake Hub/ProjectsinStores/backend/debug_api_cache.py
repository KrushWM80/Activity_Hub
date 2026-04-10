#!/usr/bin/env python3
"""Check cache record count from running API server"""

import subprocess
import requests
import json

print("=== CHECKING CACHE STATE IN RUNNING SERVER ===\n")

# Make a request to /api/projects-debug (if it exists) or just check what the first actual call returns
try:
    resp = requests.get("http://localhost:8001/api/projects?limit=10")
    projects = resp.json()
    
    print(f"API /api/projects returned {len(projects)} projects")
    
    if projects:
        first = projects[0]
        print(f"\nFirst project:")
        print(f"  ID: {first.get('project_id')}")
        print(f"  Title: {first.get('title')}")
        print(f"  Source: {first.get('project_source')}")
        
        # Check response headers for cache info
        print(f"\nResponse headers:")
        for k, v in resp.headers.items():
            if 'cache' in k.lower() or 'x-' in k.lower():
                print(f"  {k}: {v}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
