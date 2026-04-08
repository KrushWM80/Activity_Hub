#!/usr/bin/env python3
"""Test the endpoint directly by simulating the actual request"""

import sys
import os
import json
import traceback

# Change to backend directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')

try:
    print("=" * 60)
    print("Direct Endpoint Logic Test")
    print("=" * 60)
    
    # Import the functions directly
    from main import cache, load_job_code_data, to_json_safe
    import pandas as pd
    import numpy as np
    
    # Step 1: Get job codes from cache
    print("\n[STEP 1] Getting job codes from cache...")
    job_codes = cache.get_job_codes()
    print(f"Got {len(job_codes)} job codes")
    
    if not job_codes:
        print("ERROR: No job codes in cache!")
        sys.exit(1)
    
    # Step 2: Load and process teaming data
    print("\n[STEP 2] Loading teaming data...")
    merged_df, _ = load_job_code_data()
    print(f"Loaded {len(merged_df)} merged rows")
    
    # Step 3: Build teaming map (THIS IS WHERE THE ERROR WAS)
    print("\n[STEP 3] Building teaming map...")
    teaming_map = {}
    
    for idx, (_, row) in enumerate(merged_df.iterrows()):
        try:
            jc = str(row['job_code']).strip() if pd.notna(row['job_code']) else ""
            
            if jc:
                # Extract team data safely - handle lists/arrays from aggregation
                if 'teamName' in row.index:
                    teams = row['teamName']
                    # Check if it's a list or numpy array
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
                    "teams": [to_json_safe(t) for t in teams],
                    "team_ids": [to_json_safe(t) for t in team_ids],
                    "workgroups": [to_json_safe(w) for w in workgroups],
                    "division": to_json_safe(row['divNumber']) if 'divNumber' in row.index else None,
                    "department": to_json_safe(row['deptNumber']) if 'deptNumber' in row.index else None,
                }
        except Exception as e:
            print(f"  ERROR on row {idx}: {type(e).__name__}: {e}")
            traceback.print_exc()
            sys.exit(1)
    
    print(f"Built teaming map with {len(teaming_map)} entries")
    
    # Step 4: Build final result
    print("\n[STEP 4] Building final response...")
    result = []
    
    for idx, jc in enumerate(job_codes):
        try:
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
            
        except Exception as e:
            print(f"  ERROR building result for idx {idx}: {type(e).__name__}: {e}")
            traceback.print_exc()
            sys.exit(1)
    
    print(f"Built response with {len(result)} entries")
    
    # Step 5: Test JSON serialization
    print("\n[STEP 5] Testing JSON serialization...")
    response_obj = {"job_codes": result, "total": len(result)}
    
    try:
        json_str = json.dumps(response_obj)
        print(f"✓ Response is valid JSON ({len(json_str)} bytes)")
        print(f"✓ First entry:\n{json.dumps(result[0], indent=2)[:300]}")
    except Exception as e:
        print(f"ERROR: JSON serialization failed: {type(e).__name__}: {e}")
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("SUCCESS: All steps passed!")
    print("=" * 60)
    
except Exception as e:
    print(f"\nFATAL ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
