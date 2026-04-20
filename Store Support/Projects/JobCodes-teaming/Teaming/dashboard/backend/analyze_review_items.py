"""
Generate teaming requests for all Review job codes based on role criteria.

Rules:
1. If role contains: Manager, Store Manager, Coach, Store Lead → assign to "Management" teaming
2. If role has a teaming keyword (Food, Fashion, etc.) but not management → assign to that teaming
3. Everything else → skip
"""

import requests
import json
import re
from collections import defaultdict
from datetime import datetime

# Configuration
API_BASE = "http://localhost:8080"
SESSION_COOKIE = None

# Available teamings that should be matched from job titles
TEAMING_KEYWORDS = {
    'Food': ['food', 'grocery', 'deli', 'bakery', 'meat', 'produce', 'dairy'],
    'Fashion': ['apparel', 'fashion', 'clothing', 'shoes', 'accessories', 'hosiery', 'jewelry'],
    'Home': ['home', 'furniture', 'bedding', 'kitchen', 'household'],
    'Sports': ['sporting', 'sports', 'outdoor', 'recreation'],
    'Electronics': ['electronics', 'auto', 'tech', 'camera'],
    'Management': ['manager', 'store manager', 'coach', 'store lead']
}

def get_session():
    """Get authenticated session"""
    global SESSION_COOKIE
    
    if SESSION_COOKIE:
        return SESSION_COOKIE
    
    print("Note: Using admin session from browser. Make sure you're logged in with an admin account.")
    return None

def get_review_items():
    """Fetch all review items"""
    try:
        response = requests.get(f"{API_BASE}/api/job-codes", cookies={'session_id': SESSION_COOKIE})
        if response.status_code == 401:
            print("ERROR: Not authenticated. Please log in through the browser first.")
            return None
        
        data = response.json()
        job_codes = data.get('job_codes') or data
        
        # Filter for Review status
        review_items = [j for j in job_codes if j.get('status') == 'Review']
        print(f"Found {len(review_items)} Review items out of {len(job_codes)} total")
        return review_items
    except Exception as e:
        print(f"ERROR fetching job codes: {e}")
        return None

def get_all_teams():
    """Fetch available teams"""
    try:
        response = requests.get(f"{API_BASE}/api/teams")
        teams = response.json()
        print(f"Found {len(teams)} available teams")
        return teams
    except Exception as e:
        print(f"ERROR fetching teams: {e}")
        return []

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

def find_team_by_name(teams, teaming_name):
    """Find team matching the teaming name"""
    for team in teams:
        team_name = str(team.get('teamName', '')).lower()
        if teaming_name.lower() in team_name:
            return team
    
    # If exact match not found, try first team with that teaming
    print(f"WARNING: Could not find exact match for teaming '{teaming_name}'")
    print(f"Available teams: {[t.get('teamName') for t in teams[:5]]}")
    return None

def main():
    print("=" * 80)
    print("TEAMING REQUEST GENERATOR FOR REVIEW ITEMS")
    print("=" * 80)
    
    # Get review items
    review_items = get_review_items()
    if not review_items:
        print("No review items found or error fetching data")
        return
    
    # Get available teams
    teams = get_all_teams()
    if not teams:
        print("Could not fetch teams")
        return
    
    # Analyze and categorize
    assignments = defaultdict(list)
    skipped = []
    
    print("\n" + "=" * 80)
    print("ANALYZING REVIEW ITEMS")
    print("=" * 80)
    
    for item in review_items:
        job_code = item.get('job_code')
        job_title = item.get('job_title', item.get('job_name', ''))
        
        teaming = determine_teaming(job_title)
        
        if teaming:
            assignments[teaming].append({
                'job_code': job_code,
                'job_title': job_title,
                'teaming': teaming
            })
            print(f"✓ {job_code}: {job_title[:40]:40} → {teaming}")
        else:
            skipped.append(item)
            # Uncomment to see skipped items: print(f"✗ {job_code}: {job_title[:40]:40} → SKIP")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Review items: {len(review_items)}")
    print(f"To be assigned: {sum(len(v) for v in assignments.values())}")
    for teaming, items in sorted(assignments.items()):
        print(f"  - {teaming}: {len(items)}")
    print(f"To be skipped: {len(skipped)}")
    
    # Show sample of what will be created
    print("\n" + "=" * 80)
    print("SAMPLE OF REQUESTS TO BE CREATED")
    print("=" * 80)
    
    sample_count = 0
    for teaming, items in sorted(assignments.items()):
        for item in items[:2]:
            team = find_team_by_name(teams, teaming)
            if team:
                print(f"\nJob Code: {item['job_code']}")
                print(f"  Title: {item['job_title']}")
                print(f"  Teaming: {teaming}")
                print(f"  Team ID: {team.get('teamId')}")
                print(f"  Team Name: {team.get('teamName')}")
                print(f"  Workgroup: {team.get('workgroupName')}")
                sample_count += 1
            if sample_count >= 3:
                break
        if sample_count >= 3:
            break
    
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("1. Review the summary above to ensure the categorization looks correct")
    print("2. Run 'python create_teaming_requests.py' to generate the requests")
    print("3. Check your 'My Requests' and 'Admin' sections in the UI")

if __name__ == "__main__":
    main()
