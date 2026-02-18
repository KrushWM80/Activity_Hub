#!/usr/bin/env python3
"""
Create Manager Snapshot
Creates a baseline snapshot from SDL export for first-time setup.

Usage:
    python create_snapshot.py
    python create_snapshot.py --date 2026-01-05  # For a specific date
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

import config
from onedrive_helper import OneDriveHelper


def infer_role_from_location_type(location_type: str) -> str:
    """
    Infer the manager role based on location type.
    
    Args:
        location_type: Location Type Desc from SDL
    
    Returns:
        Inferred role (Store Manager, DC GM, etc.)
    """
    location_type = location_type.lower()
    
    # DC/Warehouse roles
    if any(keyword in location_type for keyword in ['warehouse', 'dc', 'distribution']):
        return 'DC General Manager'
    
    # Club roles
    if 'wholesale' in location_type or 'club' in location_type:
        return 'Club Manager'
    
    # eCommerce/Fulfillment
    if 'ecommerce' in location_type or 'fulfillment' in location_type:
        return 'Fulfillment Center Manager'
    
    # Transportation
    if 'transportation' in location_type or 'logistics' in location_type:
        return 'Transportation Manager'
    
    # Return Center
    if 'return' in location_type:
        return 'Return Center Manager'
    
    # Manufacturing
    if 'manufacturing' in location_type:
        return 'Manufacturing Manager'
    
    # Admin/Corporate (these likely won't have meaningful manager names)
    if 'admin' in location_type or 'corporate' in location_type:
        return 'Administrative Manager'
    
    # Default to Store Manager for Retail and others
    return 'Store Manager'


# Roles to track for change detection
TRACKED_ROLES = {
    'Store Manager',
    'Market Manager', 
    'Region Manager'
}


def parse_sdl_export(export_file: Path) -> list:
    """
    Parse SDL Excel export and extract manager data.
    Only tracks Store Manager, Market Manager, and Region Manager.
    
    Args:
        export_file: Path to Excel file
    
    Returns:
        List of manager dictionaries
    """
    try:
        import pandas as pd
        
        print(f"[INFO] Reading file: {export_file}")
        
        # SDL exports HTML disguised as .xlsx, try HTML first
        try:
            df = pd.read_html(str(export_file))[0]
            print(f"[OK] Parsed as HTML table")
        except:
            # Fallback to actual Excel
            try:
                df = pd.read_excel(export_file, engine='openpyxl')
                print(f"[OK] Parsed as Excel (openpyxl)")
            except:
                df = pd.read_excel(export_file)
                print(f"[OK] Parsed as Excel (default)")
        
        print(f"[INFO] Found {len(df)} rows")
        print(f"[INFO] Columns: {list(df.columns)[:5]}... (showing first 5)")
        
        # Apply location filters if enabled
        if config.FILTER_ENABLED:
            print(f"\n[FILTER] Applying location filters...")
            initial_count = len(df)
            
            # Filter 1: Exclude specific operating status codes
            if config.EXCLUDE_OPERATING_STATUS_CODES and 'Operating Status Code' in df.columns:
                df = df[~df['Operating Status Code'].isin(config.EXCLUDE_OPERATING_STATUS_CODES)]
                print(f"  Operating Status: {initial_count} -> {len(df)} (-{initial_count - len(df)})")
            
            # Filter 2: Include only specific base divisions
            if config.INCLUDE_BASE_DIVISIONS and 'Base Division Description' in df.columns:
                df = df[df['Base Division Description'].isin(config.INCLUDE_BASE_DIVISIONS)]
                print(f"  Base Division: {initial_count} -> {len(df)} (-{initial_count - len(df)})")
            
            # Filter 3: Include only specific banners
            if config.INCLUDE_BANNERS and 'Banner Desc' in df.columns:
                df = df[df['Banner Desc'].isin(config.INCLUDE_BANNERS)]
                print(f"  Banner Type: {initial_count} -> {len(df)} (-{initial_count - len(df)})")
            
            print(f"\n[FILTER] Final location count: {len(df)} (expected ~{config.EXPECTED_LOCATION_COUNT})")
            
            # Show breakdown by banner
            if 'Banner Desc' in df.columns:
                print(f"\n[FILTER] Breakdown by Banner:")
                for banner, count in df['Banner Desc'].value_counts().items():
                    print(f"  {banner:30} {count:5} locations")
            print()
        
        managers = []
        skipped = 0
        
        for idx, row in df.iterrows():
            # Extract values from actual SDL columns
            location_id = row.get('Location Number', '')
            location_name = row.get('Location Name', '')
            manager_name = row.get('Manager Name', '')
            location_type_desc = row.get('Location Type Desc', 'Store')
            phone = row.get('Primary Phone', '')
            address = row.get('Physical Address Line 1', '')
            city = row.get('Physical City', '')
            state = row.get('Physical State', '')
            zip_code = row.get('Physical Zip Code', '')
            
            # Convert to strings and clean
            if pd.notna(location_id):
                location_id = str(int(location_id)) if isinstance(location_id, float) else str(location_id)
            else:
                location_id = ''
            
            if pd.notna(manager_name):
                manager_name = str(manager_name).strip()
            else:
                manager_name = ''
            
            if pd.notna(location_name):
                location_name = str(location_name).strip()
            else:
                location_name = ''
            
            # Skip if no location ID
            if not location_id:
                skipped += 1
                continue
            
            # Extract hierarchy fields (if available)
            market = row.get('Market', '')
            market_name = row.get('Market Name', '')
            market_manager = row.get('Market Manager', '')
            region = row.get('Region', '')
            region_name = row.get('Region Name', '')
            region_manager = row.get('Region Manager', '')
            
            # 1. Store Manager (from Manager Name field)
            if manager_name and manager_name.strip() and 'TBD' not in manager_name.upper():
                role = infer_role_from_location_type(str(location_type_desc))
                
                # Only track if it's in our tracked roles
                if role in TRACKED_ROLES:
                    manager = {
                        'location_id': location_id,
                        'location_name': location_name,
                        'location_type': str(location_type_desc) if pd.notna(location_type_desc) else 'Store',
                        'role': role,
                        'manager_name': str(manager_name).strip(),
                        'manager_email': '',
                        'manager_phone': str(phone) if pd.notna(phone) else '',
                        'address': str(address) if pd.notna(address) else '',
                        'city': str(city) if pd.notna(city) else '',
                        'state': str(state) if pd.notna(state) else '',
                        'zip_code': str(zip_code) if pd.notna(zip_code) else '',
                        'market': str(market) if pd.notna(market) else '',
                        'region': str(region) if pd.notna(region) else ''
                    }
                    managers.append(manager)
            
            # 2. Market Manager (from hierarchy fields)
            if market_manager and pd.notna(market_manager) and 'TBD' not in str(market_manager).upper():
                # Create unique key for market
                market_key = f"MKT-{market}" if pd.notna(market) else f"MKT-{location_id}"
                market_loc_name = str(market_name) if pd.notna(market_name) else f"Market {market}"
                
                market_mgr = {
                    'location_id': market_key,
                    'location_name': market_loc_name,
                    'location_type': 'Market',
                    'role': 'Market Manager',
                    'manager_name': str(market_manager).strip(),
                    'manager_email': '',
                    'manager_phone': '',
                    'address': '',
                    'city': '',
                    'state': '',
                    'zip_code': '',
                    'market': str(market) if pd.notna(market) else '',
                    'region': str(region) if pd.notna(region) else ''
                }
                # Only add if not already added (avoid duplicates)
                if not any(m['location_id'] == market_key and m['role'] == 'Market Manager' for m in managers):
                    managers.append(market_mgr)
            
            # 3. Region Manager (from hierarchy fields)
            if region_manager and pd.notna(region_manager) and 'TBD' not in str(region_manager).upper():
                # Create unique key for region
                region_key = f"RGN-{region}" if pd.notna(region) else f"RGN-{location_id}"
                region_loc_name = str(region_name) if pd.notna(region_name) else f"Region {region}"
                
                region_mgr = {
                    'location_id': region_key,
                    'location_name': region_loc_name,
                    'location_type': 'Region',
                    'role': 'Region Manager',
                    'manager_name': str(region_manager).strip(),
                    'manager_email': '',
                    'manager_phone': '',
                    'address': '',
                    'city': '',
                    'state': '',
                    'zip_code': '',
                    'market': '',
                    'region': str(region) if pd.notna(region) else ''
                }
                # Only add if not already added (avoid duplicates)
                if not any(m['location_id'] == region_key and m['role'] == 'Region Manager' for m in managers):
                    managers.append(region_mgr)
        
        print(f"[OK] Parsed {len(managers)} manager records")
        print(f"[INFO] Skipped {skipped} rows (TBD managers or missing data)\n")
        return managers
    
    except ImportError:
        print("[ERROR] pandas not installed!")
        print("[INFO] Install with: uv pip install pandas openpyxl")
        print("       or: pip install pandas openpyxl\n")
        return []
    except Exception as e:
        print(f"[ERROR] Failed to parse Excel: {e}")
        import traceback
        traceback.print_exc()
        return []


def main():
    """
    Main snapshot creation workflow.
    """
    parser = argparse.ArgumentParser(description="Create a manager snapshot from SDL export")
    parser.add_argument(
        '--date',
        type=str,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Date for the snapshot (YYYY-MM-DD). Defaults to today."
    )
    parser.add_argument(
        '--export',
        type=str,
        help="Path to SDL export file. If not provided, uses most recent file in data_input/"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("CREATE MANAGER SNAPSHOT")
    print(f"Date: {args.date}")
    print("="*60 + "\n")
    
    # Find export file
    if args.export:
        export_file = Path(args.export)
        if not export_file.exists():
            print(f"[ERROR] Export file not found: {export_file}")
            return
    else:
        data_input_dir = Path("data_input")
        data_input_dir.mkdir(exist_ok=True)
        
        # Get all Excel files, excluding temp files (starting with ~$)
        all_files = list(data_input_dir.glob("*.xlsx")) + list(data_input_dir.glob("*.xls"))
        export_files = [f for f in all_files if not f.name.startswith('~$')]
        
        if not export_files:
            print("[ERROR] No SDL export file found!")
            print("[INFO] Please:")
            print("  1. Visit SDL: wmlink/sdl or https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/")
            print("  2. Search for stores/locations")
            print("  3. Export results to Excel")
            print("  4. Save the file to data_input/ folder")
            print("  5. Run this script again\n")
            return
        
        # Use most recent file
        export_file = max(export_files, key=lambda p: p.stat().st_mtime)
    
    print(f"[INFO] Using export file: {export_file.name}")
    print(f"[INFO] Last modified: {datetime.fromtimestamp(export_file.stat().st_mtime)}\n")
    
    # Parse the export
    managers = parse_sdl_export(export_file)
    
    if not managers:
        print("[ERROR] No manager records found or parsing failed")
        print("[INFO] Check the column names in your Excel file")
        print("[INFO] Expected columns: Store Number, Store Name, Role, Manager Name, Email, etc.\n")
        return
    
    # Create snapshot
    snapshot = {
        "date": args.date,
        "timestamp": datetime.now().isoformat(),
        "source": f"SDL Manual Export: {export_file.name}",
        "managers": managers
    }
    
    # Save locally
    local_dir = Path("snapshots_local")
    local_dir.mkdir(exist_ok=True)
    
    filename = config.SNAPSHOT_FILENAME_PATTERN.format(date=args.date)
    filepath = local_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    
    print(f"[SAVED] Local snapshot: {filepath}")
    
    # Upload to OneDrive
    print("[INFO] Saving to OneDrive...")
    onedrive = OneDriveHelper()
    onedrive.ensure_folder_exists()
    onedrive.save_locally(snapshot, args.date)
    # onedrive.upload_snapshot(snapshot, args.date)  # Enable when ready
    
    print("\n" + "="*60)
    print("SNAPSHOT CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"Date: {args.date}")
    print(f"Managers: {len(managers)}")
    print(f"Location: {filepath}")
    print("\nYou can now run daily_check.py to detect changes.")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[CANCELLED] Snapshot creation interrupted")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
