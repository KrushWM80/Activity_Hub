#!/usr/bin/env python3
"""Diagnose what happened with PC-07 execution"""

import json
from pathlib import Path

print("\n" + "="*70)
print("PC-07 PRODUCTION EXECUTION DIAGNOSTIC")
print("="*70 + "\n")

# Load snapshots
april_path = Path('snapshots_local/manager_snapshot_2026-04-17.json')
may_path = Path('snapshots_local/manager_snapshot_2026-05-01.json')

with open(april_path) as f:
    april_data = json.load(f)

with open(may_path) as f:
    may_data = json.load(f)

print(f"APRIL 17, 2026 SNAPSHOT:")
print(f"  Generation Time: {april_data['generation_time']}")
print(f"  Total Managers: {len(april_data['managers'])}")
print(f"  Managers:")
for mgr in april_data['managers']:
    print(f"    - Store {mgr['location_id']}: {mgr['manager_name']} ({mgr['location_name']})")

print(f"\n\nMAY 1, 2026 SNAPSHOT:")
print(f"  Generation Time: {may_data['generation_time']}")
print(f"  Total Managers: {len(may_data['managers'])}")
print(f"  Managers:")
for mgr in may_data['managers']:
    print(f"    - Store {mgr['location_id']}: {mgr['manager_name']} ({mgr['location_name']})")

# Detect changes
print(f"\n\nCHANGES DETECTED (April 17 → May 1):")
changes = []
for apr_mgr in april_data['managers']:
    apr_key = (apr_mgr['location_id'], apr_mgr['role'])
    for may_mgr in may_data['managers']:
        may_key = (may_mgr['location_id'], may_mgr['role'])
        if apr_key == may_key and apr_mgr['manager_name'] != may_mgr['manager_name']:
            change = {
                'store': apr_mgr['location_id'],
                'location': apr_mgr['location_name'],
                'old_manager': apr_mgr['manager_name'],
                'new_manager': may_mgr['manager_name']
            }
            changes.append(change)
            print(f"  ✓ Store {apr_mgr['location_id']} ({apr_mgr['location_name']}):")
            print(f"      {apr_mgr['manager_name']} → {may_mgr['manager_name']}")

print(f"\n\nTOTAL CHANGES: {len(changes)}")

# Check if data is real or synthetic
print(f"\n\nDATA CREDIBILITY CHECK:")
known_test_names = [
    'JAMES RICHARDSON', 'LISA ANDERSON', 'MARK STEPHENS', 'PATRICIA LOPEZ',
    'ROBERT WILLIAMS', 'JENNIFER MARTINEZ', 'DAVID BROWN', 'SUSAN TAYLOR',
    'CHRISTOPHER JONES', 'MARGARET WILSON', 'LAURA ANDERSON', 'THOMAS GARCIA'
]

test_name_count = 0
for mgr in may_data['managers']:
    if mgr['manager_name'] in known_test_names:
        test_name_count += 1

if test_name_count == len(may_data['managers']):
    print("  ⚠️  WARNING: ALL manager names match known SYNTHETIC test data")
    print("  DATA SOURCE: Synthetic/Test (NOT from real SDL system)")
    print("  CREDIBILITY: TEST DATA ONLY - NOT REAL MANAGER INFORMATION")
else:
    print("  ✓ Manager names appear to be from real system")
    print("  DATA SOURCE: Real SDL data")
    print("  CREDIBILITY: REAL production data")

print("\n" + "="*70 + "\n")
