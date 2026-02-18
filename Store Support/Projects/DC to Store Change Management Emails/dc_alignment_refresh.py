#!/usr/bin/env python3
"""
DC Alignment Refresh
Pulls fresh DC-to-Store alignments from LAS API and creates a clean lookup table.
Replaces stale Excel heat map with always-current API data.
"""

import requests
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Alignment type mappings
AMBIENT_TYPES = ['WH']  # Warehouse = Primary Ambient/Regional DC
PERISHABLE_TYPES = ['F0', 'F2']  # Food Network = Primary Perishable DC

def get_all_stores_from_dc(dc_number, alignment_types):
    """
    Get all stores aligned to a DC for specific alignment types.
    
    Returns:
        List of store numbers
    """
    url = f"http://dcalignment.telocmdm.prod.us.walmart.com/alignment/api/dcalign/dc/US/{dc_number}?fetch=ACTIVE"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        stores = set()
        for category in data['storeAlignment']['category']:
            if category['code'] in alignment_types:
                for store in category['alignmentDetails']:
                    stores.add(int(store['number']))
        
        return sorted(list(stores))
    except Exception as e:
        print(f"[ERROR] Failed to fetch DC {dc_number}: {e}")
        return []

def get_all_active_dcs():
    """
    Get list of all active DCs from the heat map or hardcoded list.
    
    Returns:
        Dict with 'ambient' and 'perishable' DC lists
    """
    # Try to read from existing heat map
    try:
        df = pd.read_excel('Lookup_Tool_Heat Map.xlsx', sheet_name=0)
        ambient_dcs = sorted(df[df['Commodity'] == 'Ambient']['DC'].dropna().unique().astype(int).tolist())
        perishable_dcs = sorted(df[df['Commodity'] == 'Perishable']['DC'].dropna().unique().astype(int).tolist())
        
        return {
            'ambient': ambient_dcs,
            'perishable': perishable_dcs
        }
    except Exception as e:
        print(f"[WARNING] Could not read heat map: {e}")
        print("[INFO] Using sample DC list")
        
        # Fallback: common DCs (can be expanded)
        return {
            'ambient': [6006, 6012, 6016, 6017, 6018, 6020, 6021, 6024, 6031, 6035, 6036, 6040, 6043, 6054, 6066, 6068, 6070, 6094, 7033, 7038],
            'perishable': [6055, 6062, 6072, 6073, 6074, 6082, 6083, 6099, 6858, 7010, 7013, 7014, 7016, 7021, 7024, 7030, 7055, 7084, 8348, 8852, 3010]
        }

def build_store_to_dc_lookup():
    """
    Build complete Store → DC lookup table.
    
    Returns:
        DataFrame with columns: Store, Ambient_DC, Perishable_DC
    """
    print("\n" + "="*70)
    print("DC ALIGNMENT REFRESH")
    print("="*70 + "\n")
    
    print("[STEP 1] Getting list of active DCs...")
    dcs = get_all_active_dcs()
    print(f"  Ambient DCs: {len(dcs['ambient'])}")
    print(f"  Perishable DCs: {len(dcs['perishable'])}\n")
    
    print("[STEP 2] Fetching store alignments from API...")
    print("  This may take a few minutes...\n")
    
    # Store → DC mappings
    store_ambient_dc = {}  # Store → Ambient DC
    store_perishable_dc = {}  # Store → Perishable DC
    
    # Fetch Ambient alignments
    print("  [2a] Ambient (Regional) DCs:")
    for i, dc in enumerate(dcs['ambient'], 1):
        stores = get_all_stores_from_dc(dc, AMBIENT_TYPES)
        print(f"    [{i}/{len(dcs['ambient'])}] DC {dc}: {len(stores)} stores")
        
        for store in stores:
            # If store already has an ambient DC, there might be overlap (edge case)
            # Keep the first one found
            if store not in store_ambient_dc:
                store_ambient_dc[store] = dc
    
    print(f"\n  [2b] Perishable (Food) DCs:")
    for i, dc in enumerate(dcs['perishable'], 1):
        stores = get_all_stores_from_dc(dc, PERISHABLE_TYPES)
        print(f"    [{i}/{len(dcs['perishable'])}] DC {dc}: {len(stores)} stores")
        
        for store in stores:
            if store not in store_perishable_dc:
                store_perishable_dc[store] = dc
    
    print()
    
    # Build combined lookup
    all_stores = set(store_ambient_dc.keys()) | set(store_perishable_dc.keys())
    
    lookup_data = []
    for store in sorted(all_stores):
        lookup_data.append({
            'Store': store,
            'Ambient_DC': store_ambient_dc.get(store),
            'Perishable_DC': store_perishable_dc.get(store)
        })
    
    df = pd.DataFrame(lookup_data)
    
    print("[STEP 3] Building lookup table...")
    print(f"  Total stores: {len(df)}")
    print(f"  Stores with Ambient DC: {df['Ambient_DC'].notna().sum()}")
    print(f"  Stores with Perishable DC: {df['Perishable_DC'].notna().sum()}")
    print(f"  Stores with both: {df[df['Ambient_DC'].notna() & df['Perishable_DC'].notna()].shape[0]}\n")
    
    return df

def build_dc_to_stores_lookup(store_df):
    """
    Build reverse lookup: DC → Stores.
    
    Returns:
        Dict: {DC_number: {'stores': [list], 'type': 'Ambient'|'Perishable'}}
    """
    dc_lookup = {}
    
    # Ambient DCs
    for dc in store_df['Ambient_DC'].dropna().unique():
        stores = store_df[store_df['Ambient_DC'] == dc]['Store'].tolist()
        dc_lookup[int(dc)] = {
            'stores': stores,
            'type': 'Ambient',
            'store_count': len(stores)
        }
    
    # Perishable DCs
    for dc in store_df['Perishable_DC'].dropna().unique():
        stores = store_df[store_df['Perishable_DC'] == dc]['Store'].tolist()
        if int(dc) in dc_lookup:
            # DC serves both (rare but possible)
            dc_lookup[int(dc)]['perishable_stores'] = stores
            dc_lookup[int(dc)]['type'] = 'Both'
        else:
            dc_lookup[int(dc)] = {
                'stores': stores,
                'type': 'Perishable',
                'store_count': len(stores)
            }
    
    return dc_lookup

def save_lookups(store_df, dc_lookup):
    """
    Save lookup tables to files.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Save store lookup
    store_file = f"store_to_dc_lookup_{timestamp}.xlsx"
    store_df.to_excel(store_file, index=False)
    print(f"[SAVED] Store lookup: {store_file}")
    
    # Save to standard filename too (for automation)
    store_df.to_excel('store_to_dc_lookup.xlsx', index=False)
    print(f"[SAVED] Store lookup: store_to_dc_lookup.xlsx")
    
    # Save DC lookup as JSON
    dc_file = f"dc_to_stores_lookup_{timestamp}.json"
    with open(dc_file, 'w') as f:
        json.dump(dc_lookup, f, indent=2)
    print(f"[SAVED] DC lookup: {dc_file}")
    
    # Save to standard filename
    with open('dc_to_stores_lookup.json', 'w') as f:
        json.dump(dc_lookup, f, indent=2)
    print(f"[SAVED] DC lookup: dc_to_stores_lookup.json")
    
    return store_file, dc_file

def main():
    """
    Main refresh workflow.
    """
    # Build lookups
    store_df = build_store_to_dc_lookup()
    dc_lookup = build_dc_to_stores_lookup(store_df)
    
    # Save
    print("\n[STEP 4] Saving lookup tables...")
    store_file, dc_file = save_lookups(store_df, dc_lookup)
    
    print("\n" + "="*70)
    print("REFRESH COMPLETE!")
    print("="*70)
    print(f"\nFiles created:")
    print(f"  - {store_file}")
    print(f"  - {dc_file}")
    print(f"  - store_to_dc_lookup.xlsx (latest)")
    print(f"  - dc_to_stores_lookup.json (latest)")
    print(f"\nThese files are always current as of today.")
    print(f"Run this script daily to keep them fresh!\n")

if __name__ == "__main__":
    main()
