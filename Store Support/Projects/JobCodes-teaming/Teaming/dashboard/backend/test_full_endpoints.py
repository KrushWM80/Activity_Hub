#!/usr/bin/env python3
"""Comprehensive test of dashboard endpoints"""

import sys
import os
import json

# Test both key functions
from main import get_team_options, load_job_code_data, to_json_safe

print("[TEST] =" * 40)
print("[TEST] Testing Team Options Endpoint")  
print("[TEST] =" * 40)

try:
    teams = get_team_options()
    print(f"[PASS] get_team_options() returned {len(teams)} teams")
    
    # Verify JSON serializable
    json_str = json.dumps({"teams": teams})
    print(f"[PASS] Response is JSON serializable ({len(json_str)} bytes)")
    
except Exception as e:
    import traceback
    print(f"[FAIL] {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n[TEST] =" * 40)
print("[TEST] Testing Job Code Data Loading")
print("[TEST] =" * 40)

try:
    merged_df, teaming_df = load_job_code_data()
    print(f"[PASS] load_job_code_data() returned {len(merged_df)} rows")
    
    # Test conversion to JSON
    sample_jc = merged_df.iloc[0].to_dict() if len(merged_df) > 0 else {}
    json_str = json.dumps({k: to_json_safe(v) for k,v in sample_jc.items()})
    print(f"[PASS] Job code data is JSON serializable")
    
except Exception as e:
    import traceback
    print(f"[FAIL] {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n[TEST] =" * 40)
print("[TEST] ALL TESTS PASSED!")
print("[TEST] =" * 40)
