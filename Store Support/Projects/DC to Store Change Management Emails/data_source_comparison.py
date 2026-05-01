#!/usr/bin/env python3
"""
Data Source Comparison - SDL vs ELM
Archives and compares historical SDL data with new ELM BigQuery data

Purpose:
  - Preserve April 29 SDL snapshot for audit trail
  - Compare SDL data vs ELM data to validate migration
  - Identify discrepancies or data quality issues
  - Provide reference for future analysis

Usage:
    python data_source_comparison.py
    python data_source_comparison.py --compare 2026-04-29 2026-05-01
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


def archive_sdl_data():
    """
    Archive existing SDL snapshots for historical reference.
    
    Creates: snapshots_archived/sdl_*.json (preserves April 29 synthetic data)
    """
    print("\n" + "="*60)
    print("ARCHIVING HISTORICAL SDL DATA")
    print("="*60 + "\n")
    
    snapshots_dir = Path("snapshots_local")
    archive_dir = Path("snapshots_archived")
    archive_dir.mkdir(exist_ok=True)
    
    archived_count = 0
    
    for snapshot_file in snapshots_dir.glob("manager_snapshot_*.json"):
        try:
            # Create archived filename with SDL prefix
            archive_name = f"sdl_{snapshot_file.name}"
            archive_path = archive_dir / archive_name
            
            # Skip if already archived
            if archive_path.exists():
                continue
            
            # Read and enhance with metadata
            with open(snapshot_file) as f:
                data = json.load(f)
            
            # Add archive metadata
            data['archive_metadata'] = {
                'archived_date': datetime.now().isoformat(),
                'source': 'SDL (May 1, 2026 incident - archived for reference)',
                'note': 'Preserved for audit trail and data migration comparison',
                'original_file': snapshot_file.name
            }
            
            # Save to archive
            with open(archive_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"[OK] Archived: {archive_name}")
            archived_count += 1
            
        except Exception as e:
            print(f"[WARNING] Failed to archive {snapshot_file.name}: {e}")
            continue
    
    print(f"\n[INFO] Total archived: {archived_count} snapshot(s)")
    print(f"[INFO] Archive location: {archive_dir.resolve()}\n")
    
    return archived_count


def load_snapshot(date_str: str) -> Dict:
    """
    Load snapshot from either active or archived location.
    
    Args:
        date_str: Date string (YYYY-MM-DD)
    
    Returns:
        Snapshot dictionary or empty dict if not found
    """
    # Try active location first
    active_path = Path(f"snapshots_local/manager_snapshot_{date_str}.json")
    if active_path.exists():
        with open(active_path) as f:
            return json.load(f)
    
    # Try archived SDL location
    archived_path = Path(f"snapshots_archived/sdl_manager_snapshot_{date_str}.json")
    if archived_path.exists():
        with open(archived_path) as f:
            return json.load(f)
    
    return {}


def compare_snapshots(date1: str, date2: str) -> Dict:
    """
    Compare two manager snapshots and identify changes.
    
    Args:
        date1: Earlier date (YYYY-MM-DD) - e.g., "2026-04-29" (SDL)
        date2: Later date (YYYY-MM-DD) - e.g., "2026-05-01" (ELM)
    
    Returns:
        Comparison report
    """
    print("\n" + "="*60)
    print(f"COMPARING SNAPSHOTS: {date1} vs {date2}")
    print("="*60 + "\n")
    
    snap1 = load_snapshot(date1)
    snap2 = load_snapshot(date2)
    
    if not snap1:
        print(f"[ERROR] Snapshot for {date1} not found")
        return {}
    
    if not snap2:
        print(f"[ERROR] Snapshot for {date2} not found")
        return {}
    
    # Handle both SDL format (uses 'id') and ELM format (uses 'location_id')
    def get_location_key(manager):
        if 'location_id' in manager:
            return manager['location_id']
        return manager.get('id', None)
    
    def get_manager_name(manager):
        if 'manager_name' in manager:
            return manager['manager_name']
        return manager.get('name', None)
    
    def get_location_name(manager):
        if 'location_name' in manager:
            return manager['location_name']
        return manager.get('location', None)
    
    managers1 = {get_location_key(m): m for m in snap1.get('managers', []) if get_location_key(m)}
    managers2 = {get_location_key(m): m for m in snap2.get('managers', []) if get_location_key(m)}
    
    print(f"[INFO] Date 1 ({date1}): {len(managers1)} locations")
    print(f"[INFO] Date 2 ({date2}): {len(managers2)} locations\n")
    
    # Identify changes
    new_locations = set(managers2.keys()) - set(managers1.keys())
    removed_locations = set(managers1.keys()) - set(managers2.keys())
    common_locations = set(managers1.keys()) & set(managers2.keys())
    
    manager_changes = []
    for loc_id in common_locations:
        m1 = managers1[loc_id]
        m2 = managers2[loc_id]
        
        if get_manager_name(m1) != get_manager_name(m2):
            manager_changes.append({
                'location_id': loc_id,
                'location_name': get_location_name(m2),
                'old_manager': get_manager_name(m1),
                'new_manager': get_manager_name(m2),
                'role': m2.get('role')
            })
    
    report = {
        'comparison': {
            'date1': date1,
            'date2': date2,
            'date1_source': snap1.get('source', 'Unknown'),
            'date2_source': snap2.get('source', 'Unknown')
        },
        'statistics': {
            'total_locations_date1': len(managers1),
            'total_locations_date2': len(managers2),
            'new_locations': len(new_locations),
            'removed_locations': len(removed_locations),
            'manager_changes': len(manager_changes)
        },
        'changes': {
            'new_locations': sorted(list(new_locations)),
            'removed_locations': sorted(list(removed_locations)),
            'manager_changes': manager_changes
        }
    }
    
    print(f"[STATS] New locations: {len(new_locations)}")
    print(f"[STATS] Removed locations: {len(removed_locations)}")
    print(f"[STATS] Manager changes: {len(manager_changes)}\n")
    
    if manager_changes:
        print("[MANAGER CHANGES]")
        for change in manager_changes[:10]:  # Show first 10
            print(f"  {change['location_id']} ({change['role']})")
            print(f"    {change['old_manager']} → {change['new_manager']}")
        if len(manager_changes) > 10:
            print(f"  ... and {len(manager_changes) - 10} more")
        print()
    
    # Data quality check
    print("[DATA QUALITY CHECK]")
    managers_with_email_snap1 = sum(1 for m in managers1.values() if m.get('manager_email'))
    managers_with_email_snap2 = sum(1 for m in managers2.values() if m.get('manager_email'))
    
    print(f"  Snapshot 1 - Managers with email: {managers_with_email_snap1}/{len(managers1)}")
    print(f"  Snapshot 2 - Managers with email: {managers_with_email_snap2}/{len(managers2)}\n")
    
    return report


def generate_migration_report():
    """
    Generate comprehensive SDL → ELM migration report.
    """
    print("\n" + "="*80)
    print("SDL → ELM DATA SOURCE MIGRATION REPORT")
    print("="*80 + "\n")
    
    print("SUMMARY:")
    print("  - April 29 SDL snapshot: ARCHIVED for audit trail")
    print("  - May 1 ELM snapshot: NEW data source (BigQuery)")
    print("  - Comparison: Validates data consistency across migration\n")
    
    print("FILES:")
    print("  SDL (archived): snapshots_archived/sdl_manager_snapshot_2026-04-29.json")
    print("  ELM (new):      snapshots_local/manager_snapshot_2026-05-01.json\n")
    
    print("KEY DIFFERENCES:")
    print("  SDL Scraper:")
    print("    - Manual browser automation (Playwright)")
    print("    - Subject to portal blocking/security policies")
    print("    - Dependency on Excel export parsing\n")
    print("  ELM BigQuery:")
    print("    - Direct API access to authoritative ELM catalog")
    print("    - Reliable programmatic interface")
    print("    - Consistent JSON structure from database\n")
    
    print("VALIDATION:")
    report = compare_snapshots("2026-04-29", "2026-05-01")
    
    if report:
        print(f"\n[RESULT] Migration validation complete")
        
        # Save report
        report_file = Path("reports") / f"migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"[INFO] Full report saved: {report_file}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Compare SDL and ELM data sources"
    )
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Archive existing SDL snapshots"
    )
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("DATE1", "DATE2"),
        help="Compare two snapshots (YYYY-MM-DD format)"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate migration validation report"
    )
    
    args = parser.parse_args()
    
    if args.archive:
        archive_sdl_data()
    elif args.compare:
        compare_snapshots(args.compare[0], args.compare[1])
    elif args.report:
        generate_migration_report()
    else:
        # Default: archive + compare + report
        archive_sdl_data()
        generate_migration_report()


if __name__ == "__main__":
    main()
