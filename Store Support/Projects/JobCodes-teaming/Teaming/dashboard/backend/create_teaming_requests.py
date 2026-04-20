"""
Create teaming requests for all Review job codes based on role criteria.

Rules:
1. If role contains: Manager, Store Manager, Coach, Store Lead → assign to "Management" teaming
2. If role has a teaming keyword (Food, Fashion, etc.) but not management → assign to that teaming  
3. Everything else → skip (no request created)

Run this script from the backend directory:
    python create_teaming_requests.py
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime
from collections import defaultdict

# Add backend dir to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Import from main module
from sqlite_cache import get_cache
from main import (
    load_requests, save_requests, get_team_options,
    load_job_code_data, TEAMING_DATA_FILE, REQUESTS_FILE
)

# Keywords for teaming categorization
MANAGEMENT_KEYWORDS = ['manager', 'store manager', 'coach', 'store lead', 'team lead']

TEAMING_KEYWORDS = {
    'Food': ['food', 'grocery', 'deli', 'bakery', 'meat', 'produce', 'dairy', 'perishable'],
    'Fashion': ['apparel', 'fashion', 'clothing', 'shoes', 'accessories', 'hosiery', 'jewelry'],
    'Home': ['home', 'furniture', 'bedding', 'kitchen', 'household', 'decor'],
    'Sports': ['sporting', 'sports', 'outdoor', 'recreation', 'athletic'],
    'Electronics': ['electronics', 'auto', 'tech', 'camera', 'wireless'],
    'Management': MANAGEMENT_KEYWORDS
}

def get_all_job_codes_with_status():
    """Get all job codes with computed status"""
    cache = get_cache()
    job_codes = cache.get_job_codes()
    
    if not job_codes:
        return []
    
    # Load merged data to compute status and enrich data
    try:
        merged_df, _ = load_job_code_data()
    except:
        merged_df = None
    
    result = []
    for jc in job_codes:
        job_code_str = jc.get('job_code')
        
        # Try to get enriched data from merged_df
        if merged_df is not None:
            job_data = merged_df[merged_df['job_code'] == job_code_str]
            if not job_data.empty:
                row = job_data.iloc[0]
                
                # Enrich with title from merged data if available
                job_title = str(row.get('job_title') or row.get('job_name', '')).strip()
                if not job_title:
                    job_title = jc.get('job_title') or jc.get('job_name', '')
                
                # Compute status safely - handle arrays from aggregation
                has_polaris = bool(pd.notna(row.get('job_code')))
                has_workforce = bool(row.get('from_workforce')) if pd.notna(row.get('from_workforce')) else False
                
                # Check team name - might be array from aggregation
                team_val = row.get('teamName')
                if isinstance(team_val, (list, np.ndarray)):
                    # If it's an array, check if it has non-empty elements
                    if len(team_val) > 0:
                        first_val = team_val[0] if isinstance(team_val, list) else team_val.flat[0]
                        has_teaming = bool(pd.notna(first_val) and str(first_val).strip())
                    else:
                        has_teaming = False
                else:
                    has_teaming = bool(pd.notna(team_val) and str(team_val).strip() if team_val is not None else False)
                
                # Simple status logic
                if has_polaris and has_teaming:
                    computed_status = "Assigned"
                elif has_polaris and not has_teaming:
                    computed_status = "Review"
                else:
                    computed_status = "Review"
            else:
                computed_status = "Assigned"
                job_title = jc.get('job_title') or jc.get('job_name', '')
        else:
            # Fallback: assume Assigned if not enough data
            computed_status = "Assigned"
            job_title = jc.get('job_title') or jc.get('job_name', '')
        
        jc['status'] = computed_status
        jc['job_title'] = job_title
        result.append(jc)
    
    return result

def determine_teaming(job_title):
    """Determine which teaming a job should be assigned to based on title"""
    if not job_title:
        return None
    
    title_lower = str(job_title).lower()
    
    # Check for management roles first (highest priority)
    for keyword in TEAMING_KEYWORDS.get('Management', []):
        if keyword in title_lower:
            return 'Management'
    
    # Check for other teaming keywords
    for teaming, keywords in TEAMING_KEYWORDS.items():
        if teaming == 'Management':
            continue
        for keyword in keywords:
            if keyword in title_lower:
                return teaming
    
    return None

def find_best_team_match(teams, teaming_name):
    """Find the best matching team for a teaming name"""
    if not teams:
        return None
    
    teaming_lower = str(teaming_name).lower()
    
    # Exact match first
    for team in teams:
        team_name = str(team.get('teamName', '')).lower()
        if teaming_lower == team_name:
            return team
    
    # Partial match
    for team in teams:
        team_name = str(team.get('teamName', '')).lower()
        if teaming_lower in team_name:
            return team
    
    # If no match, return first team with that workgroup containing teaming name
    for team in teams:
        workgroup = str(team.get('workgroupName', '')).lower()
        if teaming_lower in workgroup:
            return team
    
    # Last resort: return the first team (shouldn't reach this)
    print(f"WARNING: No team found for '{teaming_name}', using first available team")
    return teams[0] if teams else None

def create_teaming_request(job_code_data, team_info, admin_username="admin"):
    """Create a teaming request object"""
    return {
        "type": "teaming",
        "status": "pending",
        "requested_by": admin_username,
        "requested_by_name": "System Administrator",
        "requested_at": datetime.now().isoformat(),
        
        # Job code info
        "job_code": job_code_data.get('job_code'),
        "job_title": job_code_data.get('job_title') or job_code_data.get('job_name', ''),
        
        # Team assignment
        "team_id": team_info.get('teamId'),
        "team_name": team_info.get('teamName'),
        "workgroup_id": team_info.get('workgroupId'),
        "workgroup_name": team_info.get('workgroupName'),
        
        # Metadata
        "reason": f"Auto-generated request: Job assigned to {team_info.get('teamName')} team",
        "auto_generated": True,
        "matched_teaming": job_code_data.get('_matched_teaming')
    }

def main():
    print("=" * 90)
    print("CREATING TEAMING REQUESTS FOR REVIEW JOB CODES")
    print("=" * 90)
    
    # Load job codes with computed status
    print("\n[1/5] Loading job codes with status...")
    job_codes = get_all_job_codes_with_status()
    print(f"  Loaded {len(job_codes)} job codes")
    
    # Filter for Review status
    print("\n[2/5] Filtering for Review status...")
    review_items = [j for j in job_codes if j.get('status') == 'Review']
    print(f"  Found {len(review_items)} Review items")
    
    # Load available teams
    print("\n[3/5] Loading available teams...")
    try:
        teams = get_team_options()
        print(f"  Loaded {len(teams)} teams")
    except Exception as e:
        print(f"  ERROR loading teams: {e}")
        print(f"  Trying to load from CSV directly...")
        if os.path.exists(TEAMING_DATA_FILE):
            teaming_df = pd.read_csv(TEAMING_DATA_FILE)
            teams = teaming_df[['teamName', 'teamId', 'workgroupName', 'workgroupId']].drop_duplicates().to_dict('records')
            print(f"  Loaded {len(teams)} teams from CSV")
        else:
            print(f"  ERROR: Could not load teams")
            return
    
    # Categorize Review items
    print("\n[4/5] Categorizing Review items...")
    assignments = defaultdict(list)
    skipped = []
    
    for item in review_items:
        job_code = item.get('job_code')
        job_title = item.get('job_title') or item.get('job_name', '')
        
        teaming = determine_teaming(job_title)
        
        if teaming:
            item['_matched_teaming'] = teaming
            assignments[teaming].append(item)
        else:
            skipped.append(item)
    
    print(f"  To be assigned: {sum(len(v) for v in assignments.values())}")
    for teaming, items in sorted(assignments.items()):
        print(f"    - {teaming}: {len(items)} items")
    print(f"  To be skipped: {len(skipped)}")
    
    # Create requests
    print("\n[5/5] Creating teaming requests...")
    
    existing_requests = load_requests()
    new_requests = []
    request_count = 0
    
    for teaming, items in sorted(assignments.items()):
        team = find_best_team_match(teams, teaming)
        
        if not team:
            print(f"  WARNING: Could not find team for {teaming}, skipping {len(items)} items")
            continue
        
        for item in items:
            request = create_teaming_request(item, team)
            request['id'] = len(existing_requests) + len(new_requests) + 1
            new_requests.append(request)
            request_count += 1
    
    # Save requests
    print(f"  Created {request_count} new requests")
    all_requests = existing_requests + new_requests
    save_requests(all_requests)
    print(f"  Saved {len(all_requests)} total requests to {REQUESTS_FILE}")
    
    # Show summary
    print("\n" + "=" * 90)
    print("REQUEST CREATION SUMMARY")
    print("=" * 90)
    print(f"Total Review items: {len(review_items)}")
    print(f"Requests created: {request_count}")
    for teaming, items in sorted(assignments.items()):
        print(f"  - {teaming}: {len(items)} requests")
    print(f"Items skipped: {len(skipped)}")
    print("\n✓ Requests have been created and saved!")
    print("\nNext steps:")
    print("  1. Refresh the dashboard in your browser")
    print("  2. Go to 'My Requests' to see the generated teaming requests")
    print("  3. Go to 'Admin' to manage and approve the requests")
    print("\n" + "=" * 90)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
