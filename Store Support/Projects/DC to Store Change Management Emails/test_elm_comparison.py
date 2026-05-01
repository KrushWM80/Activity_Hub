#!/usr/bin/env python3
"""
Test: Fetch ELM snapshots for April 17 and May 1, then compare
Purpose: Validate data consistency and show real manager changes
"""

import json
from datetime import datetime
from pathlib import Path

from elm_data_fetcher import fetch_elm_data, save_elm_snapshot
from data_source_comparison import compare_snapshots


def test_elm_fetch_and_compare():
    """
    Test the complete ELM workflow:
    1. Fetch April 17 data (PC-06 baseline)
    2. Fetch May 1 data (PC-07 current)
    3. Compare for real changes
    """
    
    print("\n" + "="*80)
    print("TEST: ELM DATA FETCH AND COMPARISON")
    print("="*80)
    print("\nObjective: Validate SDL → ELM migration and detect real manager changes")
    print("Dates: April 17, 2026 (PC-06) vs May 1, 2026 (PC-07)\n")
    
    # Step 1: Fetch April 17 data
    print("[STEP 1] Fetching April 17, 2026 data from ELM...")
    print("-" * 80)
    try:
        april_path = save_elm_snapshot("2026-04-17")
        print(f"✓ April 17 snapshot created: {april_path}\n")
    except Exception as e:
        print(f"✗ Failed to fetch April 17 data: {e}\n")
        return 1
    
    # Step 2: Fetch May 1 data
    print("[STEP 2] Fetching May 1, 2026 data from ELM...")
    print("-" * 80)
    try:
        may_path = save_elm_snapshot("2026-05-01")
        print(f"✓ May 1 snapshot created: {may_path}\n")
    except Exception as e:
        print(f"✗ Failed to fetch May 1 data: {e}\n")
        return 1
    
    # Step 3: Compare snapshots
    print("[STEP 3] Comparing April 17 vs May 1...")
    print("-" * 80)
    
    snap_april = None
    snap_may = None
    
    try:
        with open(april_path) as f:
            snap_april = json.load(f)
        with open(may_path) as f:
            snap_may = json.load(f)
    except Exception as e:
        print(f"✗ Failed to load snapshots: {e}\n")
        return 1
    
    # Extract manager data
    april_managers = {m['location_id']: m for m in snap_april.get('managers', [])}
    may_managers = {m['location_id']: m for m in snap_may.get('managers', [])}
    
    print(f"\n[DATA] April 17: {len(april_managers)} locations")
    print(f"[DATA] May 1:    {len(may_managers)} locations\n")
    
    # Identify changes
    new_locations = set(may_managers.keys()) - set(april_managers.keys())
    removed_locations = set(april_managers.keys()) - set(may_managers.keys())
    common_locations = set(april_managers.keys()) & set(may_managers.keys())
    
    manager_changes = []
    for loc_id in common_locations:
        m1 = april_managers[loc_id]
        m2 = may_managers[loc_id]
        
        if m1.get('manager_name') != m2.get('manager_name'):
            manager_changes.append({
                'location_id': loc_id,
                'location_name': m2.get('location_name'),
                'old_manager': m1.get('manager_name'),
                'new_manager': m2.get('manager_name'),
                'role': m2.get('role'),
                'market': m2.get('market'),
                'region': m2.get('region')
            })
    
    # Print results
    print("="*80)
    print("COMPARISON RESULTS")
    print("="*80 + "\n")
    
    print(f"[STATISTICS]")
    print(f"  New locations (May 1):     {len(new_locations)}")
    print(f"  Removed locations:         {len(removed_locations)}")
    print(f"  Manager changes:           {len(manager_changes)}\n")
    
    if manager_changes:
        print(f"[MANAGER CHANGES] ({len(manager_changes)} total)")
        print("-" * 80)
        for i, change in enumerate(manager_changes[:20], 1):  # Show first 20
            print(f"\n{i}. {change['location_id']} - {change['location_name']}")
            print(f"   Role:     {change['role']}")
            print(f"   Market:   {change['market']}, Region: {change['region']}")
            print(f"   Before:   {change['old_manager']}")
            print(f"   After:    {change['new_manager']}")
        
        if len(manager_changes) > 20:
            print(f"\n... and {len(manager_changes) - 20} more manager changes")
    else:
        print("[MANAGER CHANGES] No changes detected between April 17 and May 1")
    
    # Data quality
    print(f"\n[DATA QUALITY]")
    april_with_email = sum(1 for m in april_managers.values() if m.get('manager_email'))
    may_with_email = sum(1 for m in may_managers.values() if m.get('manager_email'))
    
    print(f"  April 17 - Managers with email: {april_with_email}/{len(april_managers)} ({100*april_with_email/len(april_managers):.1f}%)")
    print(f"  May 1    - Managers with email: {may_with_email}/{len(may_managers)} ({100*may_with_email/len(may_managers):.1f}%)")
    
    # Save comparison report
    report = {
        'test_date': datetime.now().isoformat(),
        'purpose': 'Validate ELM data consistency and real manager changes',
        'comparison': {
            'date_1': '2026-04-17',
            'date_2': '2026-05-01',
            'source': 'ELM BigQuery (catalog_location_views.division_view)'
        },
        'statistics': {
            'locations_april_17': len(april_managers),
            'locations_may_1': len(may_managers),
            'new_locations': len(new_locations),
            'removed_locations': len(removed_locations),
            'manager_changes': len(manager_changes)
        },
        'manager_changes': manager_changes
    }
    
    report_path = Path('reports') / f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n[REPORT] Saved: {report_path}\n")
    
    # Success summary
    print("="*80)
    print("✓ TEST COMPLETE")
    print("="*80)
    print(f"\nSnapshots created:")
    print(f"  - April 17: {april_path}")
    print(f"  - May 1:    {may_path}")
    print(f"\nFiles archived for audit trail:")
    print(f"  - snapshots_archived/")
    print(f"\nComparison report saved:")
    print(f"  - {report_path}\n")
    
    return 0


if __name__ == "__main__":
    exit(test_elm_fetch_and_compare())
