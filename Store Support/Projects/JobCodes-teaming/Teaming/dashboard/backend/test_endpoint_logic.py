#!/usr/bin/env python3
"""Direct test of /api/job-codes by creating valid session"""

import sys
import os
import json

# Set up path
sys.path.insert(0, os.getcwd())

# Import main functions
from main import load_users, load_sessions, save_sessions, cache, load_job_code_data, get_team_options

print("=" * 60)
print("Testing /api/job-codes Logic Directly")
print("=" * 60)

# Create test user and session
print("\n[STEP 1] Creating test user and session...")
users = {
    "krush": {
        "password_hash": "",
        "role": "admin",
        "name": "Kendall Rush",
        "email": "kendall.rush@walmart.com",
        "approved": True
    }
}

sessions = {
    "test_session_123": {
        "username": "krush",
        "created": "2026-04-08T00:00:00"
    }
}

print("Test session created")

# Step 2: Simulate cache.get_job_codes()
print("\n[STEP 2] Testing cache.get_job_codes()...")
try:
    job_codes = cache.get_job_codes()
    print(f"Got {len(job_codes)} job codes from cache")
    if job_codes:
        sample = job_codes[0]
        print(f"Sample keys: {list(sample.keys())[:5]}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Test load_job_code_data and teaming map building
print("\n[STEP 3] Testing load_job_code_data() and teaming map...")
try:
    merged_df, _ = load_job_code_data()
    print(f"Loaded {len(merged_df)} merged rows")
    
    # Build teaming map (this is what the endpoint does)
    teaming_map = {}
    import pandas as pd
    import numpy as np
    
    for idx, (_, row) in enumerate(merged_df.iterrows()):
        jc = str(row['job_code']).strip() if pd.notna(row['job_code']) else ""
        if jc:
            # Extract team data safely - handle lists/arrays from aggregation
            if 'teamName' in row.index:
                teams = row['teamName']
                if isinstance(teams, (list, np.ndarray)):
                    teams = list(teams) if isinstance(teams, np.ndarray) else teams
                elif not pd.isna(teams):
                    teams = [teams]
                else:
                    teams = []
            else:
                teams = []
            
            if 'teamId' in row.index:
                team_ids = row['teamId']
                if isinstance(team_ids, (list, np.ndarray)):
                    team_ids = list(team_ids) if isinstance(team_ids, np.ndarray) else team_ids
                elif not pd.isna(team_ids):
                    team_ids = [team_ids]
                else:
                    team_ids = []
            else:
                team_ids = []
            
            if 'workgroupName' in row.index:
                workgroups = row['workgroupName']
                if isinstance(workgroups, (list, np.ndarray)):
                    workgroups = list(workgroups) if isinstance(workgroups, np.ndarray) else workgroups
                elif not pd.isna(workgroups):
                    workgroups = [workgroups]
                else:
                    workgroups = []
            else:
                workgroups = []
            
            teaming_map[jc] = {
                "teams": teams,
                "team_ids": team_ids,
                "workgroups": workgroups,
                "division": row['divNumber'] if 'divNumber' in row.index else None,
                "department": row['deptNumber'] if 'deptNumber' in row.index else None,
            }
        
        if idx % 50 == 0:
            print(f"  Processed {idx} rows...")
    
    print(f"Built teaming map with {len(teaming_map)} entries")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Test final response building
print("\n[STEP 4] Testing final response building...")
try:
    from main import to_json_safe
    import json
    
    result = []
    for idx, (jc_idx, jc) in enumerate(enumerate(job_codes[:10])):  # Test with first 10
        job_code_str = jc.get("job_code", "")
        teaming_info = teaming_map.get(job_code_str, {})
        
        entry = {
            "job_code": job_code_str,
            "job_title": jc.get("job_nm", ""),
            "job_name": jc.get("job_nm", ""),
            "status": "Assigned" if jc.get("updated_at") else "Missing",
            "teams": teaming_info.get("teams", []),
            "team_ids": teaming_info.get("team_ids", []),
            "workgroups": teaming_info.get("workgroups", []),
            "division": teaming_info.get("division"),
            "department": teaming_info.get("department"),
            "user_count": to_json_safe(jc.get("user_count", 0)),
            "workday_code": jc.get("workday_code", ""),
            "category": jc.get("category", ""),
            "job_family": jc.get("job_family", ""),
            "pg_level": jc.get("pg_level", ""),
            "supervisor": jc.get("supervisor", False),
            "notes": jc.get("notes", ""),
        }
        result.append(entry)
    
    print(f"Built {len(result)} result entries")
    
    # Test JSON serialization
    response = {"job_codes": result, "total": len(result)}
    json_str = json.dumps(response)
    print(f"Response is JSON serializable ({len(json_str)} bytes)")
    print(f"First job code: {json.dumps(result[0], indent=2)[:500]}")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
