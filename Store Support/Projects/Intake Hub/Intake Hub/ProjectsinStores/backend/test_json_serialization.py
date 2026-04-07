#!/usr/bin/env python3
"""Simple test to debug what's happening in /api/projects."""

import sys
sys.path.insert(0, r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend")

from sqlite_cache import get_cache
import json

print("[TEST] Initializing cache...")
cache = get_cache()

print("[TEST] Getting 10 projects from cache...")
projects = cache.get_projects(limit=10)
print(f"[TEST] Got {len(projects)} projects")

print("[TEST] Converting to list of dicts (should be already)...")
project_list = list(projects)
print(f"[TEST] {len(project_list)} items in list")

print("[TEST] Attempting JSON serialization...")
try:
    json_str = json.dumps(project_list,  default=str)
    print(f"[TEST] JSON serialization successful: {len(json_str)} bytes")
    
    # Try to parse it back
    parsed = json.loads(json_str)
    print(f"[TEST] Parsed back: {len(parsed)} items")
    
    if parsed:
        print(f"[TEST] First project keys: {list(parsed[0].keys())}")
        print(f"[TEST] First project: {parsed[0]}")
except Exception as e:
    print(f"[TEST] JSON error: {e}")
    import traceback
    traceback.print_exc()

print("[TEST] Done")
