#!/usr/bin/env python3
"""
Daily Manager Change Check
Runs daily to detect manager changes and send notifications.

Usage:
    python daily_check.py
    
This script will:
0. **Automatically download latest data from SDL** (FULLY AUTOMATED!)
1. Load yesterday's snapshot
2. Create today's snapshot (from automated SDL export)
3. Compare snapshots
4. Generate change report
5. Send email notifications
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import config
from compare_snapshots import SnapshotComparator, load_snapshot, save_report
from onedrive_helper import OneDriveHelper
from email_helper import EmailHelper
from create_snapshot import parse_sdl_export as parse_export_file
from dc_change_grouper import group_changes_by_dc, load_dc_lookup
from dc_email_generator_html import create_dc_email_package_html
import dc_leadership_config as dc_config
import dc_email_config as email_config
from collections import defaultdict

# Import SDL scraper for fully automated data fetching
try:
    from sdl_scraper import scrape_sdl_data
    SDL_SCRAPER_AVAILABLE = True
except ImportError:
    SDL_SCRAPER_AVAILABLE = False
    print("[WARNING] SDL scraper not available. Using existing export file.\n")

# Import VPN checker
try:
    from vpn_checker import quick_vpn_check, check_vpn_connectivity
    VPN_CHECKER_AVAILABLE = True
except ImportError:
    VPN_CHECKER_AVAILABLE = False
    print("[WARNING] VPN checker not available.\n")


def get_snapshot_path(date_str: str, local_only: bool = True) -> Path:
    """
    Get the path to a snapshot file.
    
    Args:
        date_str: Date string (YYYY-MM-DD)
        local_only: If True, only look in local storage
    
    Returns:
        Path to snapshot file
    """
    local_dir = Path("snapshots_local")
    filename = config.SNAPSHOT_FILENAME_PATTERN.format(date=date_str)
    return local_dir / filename


def create_snapshot_from_manual_export(export_file: Path) -> dict:
    """
    Create a snapshot from a manual SDL Excel export.
    
    Args:
        export_file: Path to the Excel export file
    
    Returns:
        Snapshot dictionary
    
    Note:
        This is a placeholder - you'll need to implement Excel parsing
        based on the actual format of your SDL export.
    """
    print(f"[INFO] Creating snapshot from {export_file}")
    
    # TODO: Implement Excel parsing
    # For now, return a template structure
    snapshot = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
        "source": f"SDL Manual Export: {export_file.name}",
        "managers": [
            # This will be populated from the Excel file
            # Example structure:
            # {
            #     "location_id": "05403",
            #     "location_name": "Store 05403",
            #     "location_type": "Store",
            #     "role": "Store Manager",
            #     "manager_name": "John Doe",
            #     "manager_email": "john.doe@walmart.com",
            #     "manager_phone": "555-1234",
            #     "market": "Market 123",
            #     "region": "Region 5"
            # }
        ]
    }
    
    print("[WARNING] Excel parsing not yet implemented!")
    print("[INFO] Please implement parse_sdl_export() function")
    
    return snapshot


def parse_sdl_export(export_file: Path) -> list:
    """
    Parse SDL Excel export and extract manager data.
    
    Args:
        export_file: Path to Excel file
    
    Returns:
        List of manager dictionaries
    
    TODO: Implement based on actual SDL export format
    """
    try:
        import pandas as pd
        
        # Read Excel file
        df = pd.read_excel(export_file)
        
        # Map columns to our schema
        # This will depend on the actual SDL export format
        # Example mapping:
        managers = []
        for _, row in df.iterrows():
            manager = {
                "location_id": str(row.get('Store Number', '')),
                "location_name": row.get('Store Name', ''),
                "location_type": "Store",  # or "DC"
                "role": row.get('Role', 'Store Manager'),
                "manager_name": row.get('Manager Name', ''),
                "manager_email": row.get('Email', ''),
                "manager_phone": row.get('Phone', ''),
                "market": row.get('Market', ''),
                "region": row.get('Region', '')
            }
            managers.append(manager)
        
        return managers
    
    except ImportError:
        print("[ERROR] pandas not installed. Install with: uv pip install pandas")
        return []
    except Exception as e:
        print(f"[ERROR] Failed to parse Excel: {e}")
        return []


def main():
    """
    Main daily check workflow.
    """
    print("\n" + "="*60)
    print("MANAGER CHANGE DETECTION - DAILY CHECK")
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    # Get date strings (needed for error notifications)
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Step 0: Quick VPN check (no long waits - Task Scheduler will retry hourly)
    if VPN_CHECKER_AVAILABLE and config.VPN_RETRY_ENABLED:
        vpn_connected, vpn_message = quick_vpn_check()
        
        if not vpn_connected:
            print(f"[VPN] Not connected: {vpn_message}")
            print(f"[VPN] Task Scheduler will retry in 1 hour")
            print(f"[VPN] Will keep trying for up to {config.VPN_MAX_RETRY_DAYS} days\n")
            sys.exit(1)  # Exit gracefully - will retry next hour
        
        print(f"[VPN] {vpn_message}\n")
    
    # Step 0: Automatically fetch latest data from SDL
    if SDL_SCRAPER_AVAILABLE:
        print("[STEP 0] Fetching latest data from SDL...")
        print("[INFO] This will take 2-10 minutes depending on export size...\n")
        try:
            scrape_sdl_data()
            print("[OK] SDL data refreshed successfully!\n")
        except Exception as e:
            print(f"[ERROR] Failed to fetch SDL data: {e}")
            
            # Don't fall back to old data - this is a real error
            error_msg = f"SDL data fetch failed even with VPN: {e}"
            print(f"[ERROR] {error_msg}\n")
            
            # Send error notification
            try:
                email_helper = EmailHelper(test_mode=True)
                email_helper.send_error_notification(error_msg, today_str)
                print("[OK] Error notification email sent\n")
            except Exception as ex:
                print(f"[WARNING] Could not send error email: {ex}\n")
            
            sys.exit(1)
    else:
        print("[INFO] Using existing SDL export (automated fetch not available)\n")
    
    # Initialize OneDrive helper
    onedrive = OneDriveHelper()
    
    # Step 1: Find the most recent snapshot (not necessarily yesterday)
    print("[STEP 1] Finding most recent snapshot...")
    
    snapshots_dir = Path("snapshots_local")
    if not snapshots_dir.exists():
        print(f"[ERROR] Snapshots directory not found: {snapshots_dir}")
        print("[INFO] This is your first run. Create a baseline snapshot first.")
        print("[INFO] Run: python create_snapshot.py\n")
        sys.exit(1)
    
    # Find all snapshot files
    snapshot_files = list(snapshots_dir.glob("manager_snapshot_*.json"))
    
    if not snapshot_files:
        print(f"[ERROR] No snapshots found in {snapshots_dir}")
        print("[INFO] Create a baseline snapshot first.")
        print("[INFO] Run: python create_snapshot.py\n")
        sys.exit(1)
    
    # Sort by date (filename contains date)
    snapshot_files.sort(reverse=True)  # Most recent first
    
    # Find the most recent snapshot that is NOT today
    previous_path = None
    previous_date = None
    
    for snapshot_file in snapshot_files:
        # Extract date from filename: manager_snapshot_YYYY-MM-DD.json
        filename = snapshot_file.stem  # Remove .json
        date_part = filename.replace("manager_snapshot_", "")
        
        if date_part != today_str:
            previous_path = snapshot_file
            previous_date = date_part
            break
    
    if not previous_path:
        print(f"[ERROR] No previous snapshot found (only today's exists)")
        print("[INFO] Wait until tomorrow to detect changes.\n")
        sys.exit(0)
    
    days_ago = (datetime.now() - datetime.strptime(previous_date, "%Y-%m-%d")).days
    print(f"[INFO] Found most recent snapshot: {previous_date} ({days_ago} day(s) ago)")
    print(f"[INFO] Checking for changes between {previous_date} and {today_str}\n")
    
    if days_ago > 1:
        print(f"[WARNING] Gap of {days_ago} days detected!")
        print(f"[WARNING] This comparison may show accumulated changes.\n")
    
    previous_snapshot = load_snapshot(str(previous_path))
    if not previous_snapshot:
        print(f"[ERROR] Failed to load previous snapshot from {previous_date}")
        sys.exit(1)
    
    print(f"[OK] Loaded {len(previous_snapshot.get('managers', []))} manager records from {previous_date}\n")
    
    # Step 2: Create today's snapshot
    print("[STEP 2] Creating today's snapshot...")
    
    # Check for manual export file
    data_input_dir = Path("data_input")
    data_input_dir.mkdir(exist_ok=True)
    
    export_files = list(data_input_dir.glob("*.xlsx")) + list(data_input_dir.glob("*.xls"))
    
    if not export_files:
        print("[ERROR] No SDL export file found in data_input/ folder")
        print("[INFO] Please:")
        print("  1. Visit SDL: wmlink/sdl")
        print("  2. Export manager data to Excel")
        print("  3. Place the file in data_input/ folder")
        print("  4. Run this script again\n")
        sys.exit(1)
    
    # Use the most recent export file
    export_file = max(export_files, key=lambda p: p.stat().st_mtime)
    print(f"[INFO] Using export file: {export_file.name}")
    
    # Parse the export and create snapshot
    managers = parse_export_file(export_file)
    
    today_snapshot = {
        "date": today_str,
        "timestamp": datetime.now().isoformat(),
        "source": f"SDL Manual Export: {export_file.name}",
        "managers": managers
    }
    
    print(f"[OK] Created snapshot with {len(managers)} manager records\n")
    
    # Save today's snapshot
    today_path = get_snapshot_path(today_str)
    with open(today_path, 'w', encoding='utf-8') as f:
        json.dump(today_snapshot, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] Today's snapshot: {today_path}")
    
    # Upload to OneDrive
    print("[INFO] Uploading to OneDrive...")
    onedrive.save_locally(today_snapshot, today_str)
    # onedrive.upload_snapshot(today_snapshot, today_str)  # Enable when ready
    print()
    
    # Step 3: Compare snapshots
    print("[STEP 3] Comparing snapshots...")
    comparator = SnapshotComparator(previous_snapshot, today_snapshot)
    changes = comparator.compare()
    
    # Print summary
    comparator.print_summary()
    
    # Step 4: Generate and save report
    if changes:
        print("[STEP 4] Generating change report...")
        report = comparator.generate_report()
        
        # Save report locally
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        report_path = reports_dir / f"change_report_{today_str}.json"
        save_report(report, str(report_path))
        
        # TODO: Upload report to OneDrive
        
        print(f"\n[SUMMARY] {len(changes)} change(s) detected!\n")
    else:
        print("[SUMMARY] No changes detected. All managers remain the same.\n")
    
    # Step 5: Send DC-segmented notifications
    if config.EMAIL_ENABLED:
        print("[STEP 5] Sending DC-segmented email notifications...")
        
        if changes:
            # Step 5a: Refresh DC alignments
            print("  [5a] Refreshing DC alignment data...")
            try:
                import subprocess
                result = subprocess.run(
                    ["python", "dc_alignment_refresh.py"],
                    capture_output=True,
                    text=True,
                    timeout=30  # Fail fast if network issues, use cached data
                )
                if result.returncode == 0:
                    print("  [OK] DC alignments refreshed\n")
                else:
                    print(f"  [WARNING] DC alignment refresh had issues, using cached data\n")
            except Exception as e:
                print(f"  [WARNING] Could not refresh DC alignments: {e}")
                print("  [INFO] Using cached DC alignment data\n")
            
            # Step 5b: Load DC lookup
            print("  [5b] Loading DC territory mappings...")
            dc_lookup = load_dc_lookup()
            if not dc_lookup:
                print("  [WARNING] No DC lookup available!")
                print("  [INFO] Run: python dc_alignment_refresh.py")
                print("  [INFO] Falling back to summary email only\n")
                # Fallback to old email method
                email_helper = EmailHelper(test_mode=config.TEST_MODE)
                email_helper.send_summary_notification([change.to_dict() for change in changes], today_str)
            else:
                print(f"  [OK] Loaded {len(dc_lookup)} DCs\n")
                
                # Step 5c: Group changes by DC and validate assignments
                print("  [5c] Grouping changes by DC territory...")
                dc_changes = group_changes_by_dc(changes, today_snapshot)
                print(f"  [OK] Changes affect {len(dc_changes)} DC(s)\n")
                
                # Step 5c.1: Validate DC assignments for each store
                print("  [5c.1] Validating DC assignments...")
                incomplete_assignments = []  # Stores with only 1 DC instead of 2
                
                for change in changes:
                    store_num = change.location_id
                    
                    # Find all DCs serving this store
                    store_dcs = []
                    dc_types_found = set()
                    
                    for dc_num, dc_info in dc_lookup.items():
                        dc_num_int = int(dc_num)
                        if store_num in dc_info.get('stores', []):
                            dc_type = dc_info.get('type', 'Unknown')
                            store_dcs.append({'dc': dc_num_int, 'type': dc_type})
                            dc_types_found.add(dc_type)
                    
                    # Check if store has both Ambient and Perishable DCs
                    if len(store_dcs) == 0:
                        incomplete_assignments.append({
                            'change': change,
                            'dcs_found': [],
                            'missing': ['Ambient/Regional DC', 'Perishable/Grocery DC']
                        })
                    elif len(store_dcs) == 1:
                        missing_type = 'Perishable/Grocery DC' if 'Ambient' in dc_types_found else 'Ambient/Regional DC'
                        incomplete_assignments.append({
                            'change': change,
                            'dcs_found': store_dcs,
                            'missing': [missing_type]
                        })
                    elif 'Ambient' not in dc_types_found or 'Perishable' not in dc_types_found:
                        missing_types = []
                        if 'Ambient' not in dc_types_found:
                            missing_types.append('Ambient/Regional DC')
                        if 'Perishable' not in dc_types_found:
                            missing_types.append('Perishable/Grocery DC')
                        incomplete_assignments.append({
                            'change': change,
                            'dcs_found': store_dcs,
                            'missing': missing_types
                        })
                
                if incomplete_assignments:
                    print(f"  [WARNING] {len(incomplete_assignments)} store(s) with incomplete DC assignments")
                    for item in incomplete_assignments:
                        store = item['change'].location_id
                        missing = ', '.join(item['missing'])
                        print(f"    - Store {store}: Missing {missing}")
                else:
                    print(f"  [OK] All stores have complete DC assignments")
                print()
                
                # Step 5d: Group by unique distribution lists
                print("  [5d] Creating unique distribution lists...")
                dc_signatures = {}
                
                for dc_num, dc_change_list in dc_changes.items():
                    change_ids = tuple(sorted([f"{c.role}:{c.location_id}" for c in dc_change_list]))
                    
                    if change_ids not in dc_signatures:
                        dc_signatures[change_ids] = {
                            'dcs': [],
                            'changes': dc_change_list,
                            'dc_types': {}
                        }
                    
                    dc_type = dc_lookup.get(str(dc_num), {}).get('type', 'Unknown')
                    dc_signatures[change_ids]['dcs'].append(dc_num)
                    dc_signatures[change_ids]['dc_types'][dc_num] = dc_type
                
                print(f"  [OK] {len(dc_signatures)} unique email(s) to send\n")
                
                # Step 5e: Generate and send emails
                print("  [5e] Generating and sending DC-segmented emails...")
                
                test_mode = email_config.is_test_mode()
                if test_mode:
                    print(f"  [TEST MODE] All emails will go to: {email_config.get_test_recipient()}")
                else:
                    print(f"  [PRODUCTION] Emails will go to DC leadership (BCC)")
                print()
                
                email_count = 0
                for i, (sig, info) in enumerate(dc_signatures.items(), 1):
                    dcs = info['dcs']
                    dc_change_list = info['changes']
                    dc_types = info['dc_types']
                    
                    # Generate intended recipients
                    intended_recipients = []
                    for dc_num in dcs:
                        dc_emails = dc_config.get_dc_emails(dc_num)
                        intended_recipients.extend(dc_emails)
                    intended_recipients = list(dict.fromkeys(intended_recipients))
                    
                    # Use first DC for email
                    primary_dc = sorted(dcs)[0]
                    primary_dc_type = dc_types[primary_dc]
                    
                    # Create email
                    email_pkg = create_dc_email_package_html(
                        dc_number=primary_dc,
                        dc_type=primary_dc_type,
                        changes=dc_change_list,
                        date_str=today_str,
                        intended_recipients=intended_recipients
                    )
                    
                    # Send email
                    print(f"    [{i}/{len(dc_signatures)}] Sending email for DC(s): {', '.join(map(str, dcs[:3]))}{'...' if len(dcs) > 3 else ''}")
                    print(f"        To: {', '.join(email_pkg['to'])}")
                    print(f"        From: {email_pkg['from_email']}")
                    print(f"        Changes: {len(dc_change_list)}")
                    
                    # Save to emails_pending for backup
                    emails_pending = Path("emails_pending")
                    emails_pending.mkdir(exist_ok=True)
                    email_file = emails_pending / f"dc_email_{today_str}_{i}.html"
                    with open(email_file, 'w', encoding='utf-8') as f:
                        f.write(email_pkg['body_html'])
                    print(f"        [SAVED] {email_file}")
                    
                    # Send via Outlook COM automation from shared mailbox
                    try:
                        email_sender = EmailHelper(test_mode=config.TEST_MODE)
                        
                        # Send using Outlook COM with shared mailbox
                        success = email_sender.send_email_via_outlook(
                            to=email_pkg['to'],
                            subject=email_pkg['subject'],
                            body_html=email_pkg['body_html'],
                            from_email=email_pkg['from_email']  # Send from shared mailbox
                        )
                        
                        if success:
                            print(f"        [SENT] Email sent successfully")
                            email_count += 1
                        else:
                            print(f"        [ERROR] Failed to send email")
                        
                    except Exception as e:
                        print(f"        [ERROR] Failed to send email: {e}")
                        print(f"        [INFO] Email saved to {email_file} for manual sending")
                
                print(f"\n  [OK] {email_count} DC-segmented email(s) sent!")
                
                # Step 5f: Send incomplete alignment notification if any stores had issues
                if incomplete_assignments:
                    print(f"\n  [5f] Sending incomplete DC alignment notification...")
                    
                    try:
                        email_helper = EmailHelper(test_mode=True)  # Always send to admin
                        
                        success = email_helper.send_incomplete_alignment_notification(
                            incomplete_assignments=incomplete_assignments,
                            date=today_str
                        )
                        
                        if success:
                            print(f"  [OK] Incomplete alignment notification sent to admin\n")
                        else:
                            print(f"  [ERROR] Failed to send alignment notification\n")
                    except Exception as e:
                        print(f"  [ERROR] Failed to send alignment notification: {e}\n")
                else:
                    print(f"\n  [OK] All stores have complete DC assignments (no alignment issues)\n")
                
                print()
        else:
            # Send "no changes" confirmation email - ALWAYS to admin only
            print(f"[INFO] No changes detected.")
            print(f"[INFO] Sending confirmation email to admin: {email_config.get_admin_email()}")
            
            # Create simple no-change notification (admin only)
            try:
                # Use email helper for no-change notification
                email_helper = EmailHelper(test_mode=True)  # Force test mode for admin-only
                email_helper.send_no_changes_notification(today_str)
                print("[OK] Confirmation email sent to admin\n")
            except Exception as e:
                print(f"[WARNING] Could not send no-change email: {e}\n")
    elif changes:
        print("[INFO] Email notifications disabled (set EMAIL_ENABLED=True in config.py)\n")
    
    print("="*60)
    print("Daily check complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[CANCELLED] Daily check interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        print(f"[ERROR] Error type: {type(e).__name__}")
        
        # Send error notification email - ALWAYS to admin only
        if config.EMAIL_ENABLED:
            try:
                from datetime import datetime
                
                print(f"[INFO] Sending error notification to admin: {email_config.get_admin_email()}")
                email_helper = EmailHelper(test_mode=True)  # Force test mode for admin-only
                error_message = f"{type(e).__name__}: {str(e)}"
                today_str = datetime.now().strftime("%Y-%m-%d")
                
                print("\n[INFO] Sending error notification email...")
                email_helper.send_error_notification(error_message, today_str)
                print("[OK] Error notification sent\n")
            except Exception as email_error:
                print(f"[ERROR] Failed to send error notification: {email_error}")
        
        sys.exit(1)
        traceback.print_exc()
        sys.exit(1)