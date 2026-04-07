#!/usr/bin/env python3
"""Test the /api/teams endpoint"""

import sys
import os
import json

# Test get_team_options function
from main import get_team_options, to_json_safe

print("[TEST] Testing get_team_options() function...")
try:
    teams = get_team_options()
    print(f"[SUCCESS] get_team_options() returned {len(teams)} teams")
    
    # Verify it's JSON serializable
    json_str = json.dumps({"teams": teams})
    print(f"[SUCCESS] Response is JSON serializable ({len(json_str)} bytes)")
    print(f"[SUCCESS] First team: {json.dumps(teams[0])}")
    
except Exception as e:
    import traceback
    print(f"[ERROR] {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n[TEST] All tests passed!")
