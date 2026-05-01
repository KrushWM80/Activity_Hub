#!/usr/bin/env python3
"""Query ELM for stores (handle string location_ids)."""
import json

snap = json.loads(open('snapshots_local/manager_snapshot_2026-05-01.json').read())

# Store numbers from the synthetic email (as strings)
store_numbers = ['100', '103', '121', '130']

print('\nQUERYING ELM FOR STORE MANAGERS')
print('='*80)

found_stores = {}

for store_num in store_numbers:
    print(f'\n--- Store #{store_num} ---')
    
    # Search for the store
    for m in snap['managers']:
        loc_id = str(m.get('location_id'))
        if loc_id == store_num:
            manager_name = m.get('manager_name', 'N/A')
            manager_email = m.get('manager_email', 'N/A')
            city = m.get('city', 'N/A')
            state = m.get('state', 'N/A')
            role = m.get('role', 'N/A')
            location_name = m.get('location_name', 'N/A')
            
            print(f'  ✓ FOUND')
            print(f'  Business Unit #: {store_num}')
            print(f'  Location: {location_name}')
            print(f'  Store Manager: {manager_name}')
            print(f'  Email: {manager_email}')
            print(f'  City: {city}, {state}')
            print(f'  Role: {role}')
            
            found_stores[store_num] = {
                'store_number': store_num,
                'location_name': location_name,
                'store_manager': manager_name,
                'email': manager_email,
                'city': city,
                'state': state,
                'role': role,
                'elm_link': f'https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/search?business_unit_nbr={store_num}'
            }
            break
    else:
        print(f'  NOT FOUND')

print('\n' + '='*80)
print('\nCORRECTIVE EMAIL DATA:')
print(json.dumps(found_stores, indent=2))

print('\n' + '='*80)
print('\nEMAIL CORRECTIONS:')
print('\nStore #100:')
if '100' in found_stores:
    d = found_stores['100']
    print(f'  WRONG: JAMES RICHARDSON in Rogers, AR')
    print(f'  RIGHT: {d["store_manager"]} in {d["city"]}, {d["state"]}')
    print(f'  ELM: {d["elm_link"]}')

print('\nStore #103:')
if '103' in found_stores:
    d = found_stores['103']
    print(f'  WRONG: LISA ANDERSON in Bentonville, AR')
    print(f'  RIGHT: {d["store_manager"]} in {d["city"]}, {d["state"]}')
    print(f'  ELM: {d["elm_link"]}')

print('\nStore #121:')
if '121' in found_stores:
    d = found_stores['121']
    print(f'  WRONG: PATRICIA LOPEZ in Little Rock, AR')
    print(f'  RIGHT: {d["store_manager"]} in {d["city"]}, {d["state"]}')
    print(f'  ELM: {d["elm_link"]}')

print('\nStore #130:')
if '130' in found_stores:
    d = found_stores['130']
    print(f'  WRONG: DAVID BROWN in Pine Bluff, AR')
    print(f'  RIGHT: {d["store_manager"]} in {d["city"]}, {d["state"]}')
    print(f'  ELM: {d["elm_link"]}')
