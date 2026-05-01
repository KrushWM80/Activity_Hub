#!/usr/bin/env python3
"""Find the 4 stores in ELM data and extract their real manager information."""
import json

snap = json.loads(open('snapshots_local/manager_snapshot_2026-05-01.json').read())

# The stores from the synthetic email (by city and state from the UI)
store_cities = {
    'Rogers': 'AR',
    'Bentonville': 'AR',
    'Little Rock': 'AR',
    'Pine Bluff': 'AR'
}

print('\nSEARCHING FOR STORES IN ELM DATA')
print('='*80)

# First show what we have
print(f'\nTotal managers in ELM snapshot: {len(snap["managers"])}')
print('\nFirst 3 managers:')
for i, m in enumerate(snap['managers'][:3]):
    print(f'  {i+1}. ID={m.get("location_id")} | {m.get("location_name")} | {m.get("city")}, {m.get("state")}')

print('\n' + '='*80)
print('SEARCHING BY CITY/STATE:')

found_stores = {}

for city, state in store_cities.items():
    print(f'\nSearching for {city}, {state}...')
    matches = []
    for m in snap['managers']:
        if m.get('city') == city and m.get('state') == state:
            matches.append(m)
    
    if matches:
        print(f'  Found {len(matches)} match(es):')
        for m in matches[:3]:  # Show first 3
            print(f'    - ID={m.get("location_id")} | {m.get("location_name")}')
            print(f'      Manager: {m.get("manager_name")}')
            print(f'      Email: {m.get("manager_email", "NO EMAIL")}')
            found_stores[city] = m
    else:
        print(f'  NO MATCHES FOUND')

print('\n' + '='*80)
print('\nRESULTS FOR EMAIL:')
print(json.dumps({city: {
    'location_name': m.get('location_name'),
    'location_id': m.get('location_id'),
    'city': m.get('city'),
    'state': m.get('state'),
    'manager': m.get('manager_name'),
    'email': m.get('manager_email')
} for city, m in found_stores.items()}, indent=2))
