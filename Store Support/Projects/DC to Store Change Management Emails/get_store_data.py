#!/usr/bin/env python3
"""Extract real store data from May 1 ELM snapshot for corrective email."""
import json

# Load May 1 ELM snapshot
snap = json.loads(open('snapshots_local/manager_snapshot_2026-05-01.json').read())

# Store IDs to find
stores = [100, 103, 121, 130]

print('\nREAL DATA FROM MAY 1, 2026 ELM SNAPSHOT')
print('='*80)

results = {}

for store_id in stores:
    # Find store in managers list
    manager = None
    for m in snap['managers']:
        if m.get('location_id') == store_id:
            manager = m
            break
    
    if manager:
        results[store_id] = {
            'location_name': manager.get('location_name', 'Unknown'),
            'city': manager.get('city'),
            'state': manager.get('state'),
            'manager_name': manager.get('manager_name'),
            'manager_email': manager.get('manager_email', '[NO EMAIL ON FILE]'),
            'role': manager.get('role'),
            'status': manager.get('status')
        }
        
        print(f"\nStore #{store_id} - {manager.get('location_name', 'Unknown')}")
        print(f"  Location: {manager.get('city')}, {manager.get('state')}")
        print(f"  Real Manager: {manager.get('manager_name')}")
        print(f"  Email: {manager.get('manager_email', '[NO EMAIL ON FILE]')}")
        print(f"  Role: {manager.get('role')}")
        print(f"  Status: {manager.get('status')}")
    else:
        print(f"\nStore #{store_id} - NOT FOUND IN ELM DATA")
        results[store_id] = None

print('\n' + '='*80)
print('\nSTORE DATA FOR EMAIL DRAFT:')
print(json.dumps(results, indent=2))
