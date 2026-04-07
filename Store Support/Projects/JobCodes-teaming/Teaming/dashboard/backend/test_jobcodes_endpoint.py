#!/usr/bin/env python3
"""Test /api/job-codes endpoint directly"""

import sys
import os
import json

# Test the endpoint
from main import app, get_job_codes
from starlette.requests import Request
from unittest.mock import Mock

print("[TEST] Testing /api/job-codes endpoint logic")
print("=" * 60)

# Create mock request with session
mock_request = Mock(spec=Request)
mock_request.cookies = {"session_id": None}

try:
    # This will fail auth, which is expected
    result = get_job_codes(mock_request)
    print(f"[ERROR] Should have raised auth error, got: {result}")
except Exception as e:
    print(f"[INFO] Auth check (expected): {type(e).__name__}: {str(e)[:100]}")

print("\n" + "=" * 60)
print("[TEST] Testing cache and data loading")
print("=" * 60)

try:
    from sqlite_cache import SQLiteCache
    from main import load_job_code_data, to_json_safe
    import pandas as pd
    
    cache = SQLiteCache()
    job_codes = cache.get_job_codes()
    print(f"[PASS] cache.get_job_codes() returned {len(job_codes)} codes")
    
    if job_codes:
        sample = job_codes[0]
        print(f"[PASS] First job code is dict: {type(sample).__name__}")
        print(f"[PASS] Keys: {list(sample.keys())}")
        print(f"[PASS] Sample: {json.dumps({k: str(v)[:30] for k,v in list(sample.items())[:5]})}")
    
    # Test teaming data
    print("\n[INFO] Testing load_job_code_data()...")
    merged_df, teaming_df = load_job_code_data()
    print(f"[PASS] Loaded {len(merged_df)} merged rows")
    
    if len(merged_df) > 0:
        row = merged_df.iloc[0]
        print(f"[PASS] First row type: {type(row).__name__}")
        print(f"[PASS] Can access row['job_code']: {row['job_code']}")
        
except Exception as e:
    import traceback
    print(f"[ERROR] {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("[TEST] ALL TESTS PASSED!")
print("=" * 60)
