#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DC Change Grouper
Groups manager changes by DC service territory for targeted notifications.
"""

import json
import pandas as pd
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any

def load_dc_lookup():
    """
    Load DC-to-Store lookup table.
    
    Returns:
        Dict: {DC_number: {'stores': [list], 'type': 'Ambient'|'Perishable'}}
    """
    lookup_file = Path('dc_to_stores_lookup.json')
    
    if not lookup_file.exists():
        print("[WARNING] DC lookup file not found!")
        print("[INFO] Run: python dc_alignment_refresh.py")
        return {}
    
    with open(lookup_file) as f:
        dc_lookup = json.load(f)
    
    # Convert string keys back to int
    return {int(k): v for k, v in dc_lookup.items()}

def get_dcs_for_store(store_number: int, dc_lookup: Dict) -> List[int]:
    """
    Get all DCs serving a specific store.
    
    Args:
        store_number: Store number
        dc_lookup: DC lookup dict
    
    Returns:
        List of DC numbers
    """
    dcs = []
    
    for dc_num, dc_info in dc_lookup.items():
        if store_number in dc_info.get('stores', []):
            dcs.append(dc_num)
    
    return dcs

def get_stores_in_market(market_id: str, snapshot_data: Dict) -> List[int]:
    """
    Get all store numbers in a market.
    
    Args:
        market_id: Market ID (e.g., "MKT-323")
        snapshot_data: Snapshot data with managers
    
    Returns:
        List of store numbers
    """
    stores = []
    
    # Find all Store Manager entries with this market
    for manager in snapshot_data.get('managers', []):
        if manager.get('role') == 'Store Manager':
            if manager.get('market') == market_id.replace('MKT-', ''):
                try:
                    store_num = int(manager.get('location_id', 0))
                    if store_num > 0:
                        stores.append(store_num)
                except:
                    pass
    
    return stores

def get_stores_in_region(region_id: str, snapshot_data: Dict) -> List[int]:
    """
    Get all store numbers in a region.
    
    Args:
        region_id: Region ID (e.g., "RGN-42")
        snapshot_data: Snapshot data with managers
    
    Returns:
        List of store numbers
    """
    stores = []
    
    # Find all Store Manager entries with this region
    for manager in snapshot_data.get('managers', []):
        if manager.get('role') == 'Store Manager':
            if manager.get('region') == region_id.replace('RGN-', ''):
                try:
                    store_num = int(manager.get('location_id', 0))
                    if store_num > 0:
                        stores.append(store_num)
                except:
                    pass
    
    return stores

def group_changes_by_dc(changes: List[Any], snapshot_data: Dict = None) -> Dict[int, List[Any]]:
    """
    Group manager changes by DC service territory.
    Each change gets sent to BOTH Ambient and Perishable DCs serving that store.
    
    Args:
        changes: List of ManagerChange objects
        snapshot_data: Current snapshot data (for market/region lookups)
    
    Returns:
        Dict: {DC_number: [list of changes]}
    
    Example:
        Store 1 manager changes:
        - Added to DC 6094 (Ambient) change list
        - Added to DC 6082 (Perishable) change list
    """
    dc_lookup = load_dc_lookup()
    
    if not dc_lookup:
        print("[WARNING] No DC lookup available, cannot group by DC")
        return {}
    
    dc_changes = defaultdict(list)
    
    for change in changes:
        affected_dcs = set()
        
        # Determine which DCs are affected based on manager role
        if change.role == 'Store Manager':
            # Get ALL DCs serving this store (both Ambient and Perishable)
            try:
                store_num = int(change.location_id)
                dcs = get_dcs_for_store(store_num, dc_lookup)
                affected_dcs.update(dcs)
                
                # Debug logging
                if len(dcs) > 0:
                    dc_types = [f"DC {dc} ({dc_lookup[dc].get('type', 'Unknown')})" for dc in dcs]
                    print(f"  [INFO] Store {store_num} change affects: {', '.join(dc_types)}")
            except Exception as e:
                print(f"[WARNING] Could not parse store number: {change.location_id} - {e}")
        
        elif change.role == 'Market Manager':
            # Get all stores in this market, then ALL their DCs (Ambient + Perishable)
            if snapshot_data:
                market_stores = get_stores_in_market(change.location_id, snapshot_data)
                dc_set = set()
                for store in market_stores:
                    dcs = get_dcs_for_store(store, dc_lookup)
                    dc_set.update(dcs)
                affected_dcs.update(dc_set)
                
                print(f"  [INFO] Market {change.location_id} change affects {len(dc_set)} DCs (across {len(market_stores)} stores)")
        
        elif change.role == 'Region Manager':
            # Get all stores in this region, then ALL their DCs
            if snapshot_data:
                region_stores = get_stores_in_region(change.location_id, snapshot_data)
                dc_set = set()
                for store in region_stores:
                    dcs = get_dcs_for_store(store, dc_lookup)
                    dc_set.update(dcs)
                affected_dcs.update(dc_set)
                
                print(f"  [INFO] Region {change.location_id} change affects {len(dc_set)} DCs (across {len(region_stores)} stores)")
        
        # Add this change to all affected DCs (both Ambient and Perishable)
        for dc in affected_dcs:
            dc_changes[dc].append(change)
    
    return dict(dc_changes)

def get_dc_summary(dc_changes: Dict[int, List]) -> Dict[str, Any]:
    """
    Get summary of changes by DC.
    
    Args:
        dc_changes: Dict of {DC: [changes]}
    
    Returns:
        Summary dict
    """
    summary = {
        'total_dcs_affected': len(dc_changes),
        'total_changes': sum(len(changes) for changes in dc_changes.values()),
        'dcs': []
    }
    
    for dc, changes in sorted(dc_changes.items()):
        dc_summary = {
            'dc_number': dc,
            'change_count': len(changes),
            'roles': {}
        }
        
        # Group by role
        for change in changes:
            role = change.role
            if role not in dc_summary['roles']:
                dc_summary['roles'][role] = 0
            dc_summary['roles'][role] += 1
        
        summary['dcs'].append(dc_summary)
    
    return summary

def print_dc_grouping_summary(dc_changes: Dict[int, List]):
    """
    Print a summary of how changes are grouped by DC.
    """
    summary = get_dc_summary(dc_changes)
    
    print("\n" + "="*70)
    print("DC CHANGE DISTRIBUTION")
    print("="*70)
    print(f"\nTotal DCs Affected: {summary['total_dcs_affected']}")
    print(f"Total Changes: {summary['total_changes']}\n")
    
    for dc_info in summary['dcs']:
        dc_num = dc_info['dc_number']
        count = dc_info['change_count']
        roles = dc_info['roles']
        
        print(f"DC {dc_num}: {count} change(s)")
        for role, role_count in roles.items():
            print(f"  - {role}: {role_count}")
        print()

if __name__ == "__main__":
    # Test with sample data
    from compare_snapshots import ManagerChange
    
    # Sample changes
    changes = [
        ManagerChange(
            location_id="1",
            location_name="Rogers, AR",
            location_type="Store",
            role="Store Manager",
            previous_manager="John Doe",
            new_manager="Jane Smith"
        ),
        ManagerChange(
            location_id="MKT-323",
            location_name="Market 323",
            location_type="Market",
            role="Market Manager",
            previous_manager="Bob Manager",
            new_manager="Alice Leader"
        )
    ]
    
    # Group by DC
    dc_changes = group_changes_by_dc(changes)
    
    # Print summary
    print_dc_grouping_summary(dc_changes)
