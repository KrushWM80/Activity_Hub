#!/usr/bin/env python3
"""Query ELM data for specific store business_unit_nbr and get real manager info."""
import json

snap = json.loads(open('snapshots_local/manager_snapshot_2026-05-01.json').read())

# Store numbers from the synthetic email
store_numbers = [100, 103, 121, 130]

print('\nQUERYING ELM FOR STORE MANAGERS')
print('='*80)

# Check available fields
print('\nAvailable fields in ELM data:')
if snap['managers']:
    print(list(snap['managers'][0].keys()))

print('\n' + '='*80)
print('SEARCHING FOR STORES BY BUSINESS_UNIT_NBR:')

found_stores = {}

for store_num in store_numbers:
    print(f'\n--- Store #{store_num} ---')
    
    # Search for the store
    matches = []
    for m in snap['managers']:
        # Check if location_id (which is business_unit_nbr from ELM)
        if m.get('location_id') == store_num:
            matches.append(m)
    
    if matches:
        m = matches[0]
        manager_name = m.get('manager_name', 'N/A')
        manager_email = m.get('manager_email', 'N/A')
        city = m.get('city', 'N/A')
        state = m.get('state', 'N/A')
        role = m.get('role', 'N/A')
        location_name = m.get('location_name', 'N/A')
        
        print(f'  Business Unit #: {store_num}')
        print(f'  Location Name: {location_name}')
        print(f'  Store Manager: {manager_name}')
        print(f'  Email: {manager_email}')
        print(f'  City: {city}')
        print(f'  State: {state}')
        print(f'  Role: {role}')
        
        found_stores[store_num] = {
            'business_unit_nbr': store_num,
            'location_name': location_name,
            'store_manager': manager_name,
            'email': manager_email,
            'city': city,
            'state': state,
            'role': role,
            'elm_link': f'https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/?business_unit_nbr={store_num}'
        }
    else:
        print(f'  NOT FOUND')
        print(f'  Checking all location_ids to see what range exists...')
        all_ids = [m.get('location_id') for m in snap['managers'][:10]]
        print(f'  Sample location_ids: {all_ids}')

print('\n' + '='*80)
print('\nRESULTS:')
print(json.dumps(found_stores, indent=2))

print('\n' + '='*80)
print('\nSUMMARY FOR CORRECTIVE EMAIL:')
for store_num, data in found_stores.items():
    print(f"\nStore #{store_num}:")
    print(f"  Correct Manager: {data['store_manager']}")
    print(f"  City: {data['city']}, {data['state']}")
    print(f"  ELM Link: {data['elm_link']}")
