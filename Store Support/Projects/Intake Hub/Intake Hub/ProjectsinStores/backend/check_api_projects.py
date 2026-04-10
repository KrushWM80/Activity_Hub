#!/usr/bin/env python3
"""Check what the API is actually returning"""

import requests
import json

print("=== API RESPONSE CHECK ===\n")

try:
    # Get first 50 projects to see what's being returned
    response = requests.get("http://localhost:8001/api/projects?limit=50")
    projects = response.json()
    
    print(f"API returned {len(projects)} projects\n")
    
    # Look for "Store Renovation" or "Project" pattern
    print("Projects with 'Store Renovation' or 'Project' in name:")
    for i, p in enumerate(projects):
        title = p.get('title', '')
        if 'Store Renovation' in title or 'Project' in title:
            print(f"  [{i}] {title} ({p.get('project_source')})")
    
    print("\n\nFirst 10 projects returned:")
    for i, p in enumerate(projects[:10]):
        print(f"  [{i}] {p.get('title')} ({p.get('project_source')})")
        print(f"       ID: {p.get('project_id')}, Store: {p.get('store')}")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nNote: Make sure backend is running on port 8001")
