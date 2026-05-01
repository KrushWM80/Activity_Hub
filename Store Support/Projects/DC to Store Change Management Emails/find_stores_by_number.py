#!/usr/bin/env python3
"""Find stores by business_unit_nbr and extract real manager information."""
import json

snap = json.loads(open('snapshots_local/manager_snapshot_2026-05-01.json').read())

# Store numbers from the synthetic email
store_numbers = [100, 103, 121, 130]

print('\nFINDING STORES BY BUSINESS_UNIT_NBR IN ELM DATA')
print('='*80)

# First check what fields are available
print(f'\nSample manager record:')
if snap['managers']:
    m = snap['managers'][0]
    print(f'Keys: {list(m.keys())}')

print('\n' + '='*80)
print('SEARCHING BY STORE NUMBER (business_unit_nbr):')

found_stores = {}

for store_num in store_numbers:
    print(f'\nSearching for Store #{store_num}...')
    
    # Try different field names that might contain the store number
    matches = []
    for m in snap['managers']:
        # Check various possible fields
        bu_nbr = m.get('business_unit_nbr')
        loc_id = m.get('location_id')
        
        if bu_nbr == store_num or loc_id == store_num:
            matches.append(m)
    
    if matches:
        m = matches[0]
        print(f'  ✓ FOUND')
        print(f'    Store Number: {store_num}')
        print(f'    Location ID: {m.get("location_id")}')
        print(f'    Name: {m.get("location_name")}')
        print(f'    City: {m.get("city")}')
        print(f'    State: {m.get("state")}')
        print(f'    Real Manager: {m.get("manager_name")}')
        print(f'    Email: {m.get("manager_email", "NO EMAIL")}')
        print(f'    Status: {m.get("status")}')
        
        found_stores[store_num] = {
            'location_id': m.get('location_id'),
            'location_name': m.get('location_name'),
            'city': m.get('city'),
            'state': m.get('state'),
            'manager': m.get('manager_name'),
            'email': m.get('manager_email'),
            'status': m.get('status')
        }
    else:
        print(f'  ✗ NOT FOUND - checking all fields...')
        # Search more broadly
        for m in snap['managers']:
            for key, value in m.items():
                if value == store_num:
                    print(f'    Found in field "{key}": {m.get("location_name")}')
                    print(f'      Manager: {m.get("manager_name")}')

print('\n' + '='*80)
print('\nSTORE DATA FOR CORRECTIVE EMAIL:')
print(json.dumps(found_stores, indent=2))
