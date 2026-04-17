#!/usr/bin/env python3
"""
Generic PayCycle Manager Change Email - Production Mode
Reusable for all PayCycles (PC-06 through PC-26)

Accepts PAYCYCLE_NUMBER as environment variable or command-line argument.
Loads snapshot data for that PayCycle's date (not hardcoded).
Detects real manager changes by comparing snapshots 14 days apart.

Usage:
    PAYCYCLE_NUMBER=7 python send_paycycle_production_email_generic.py
    python send_paycycle_production_email_generic.py 7

Schedule:
    Task Scheduler calls this with PAYCYCLE_NUMBER for each PayCycle
    PC-07 @ May 1, 2026 06:00 AM → PAYCYCLE_NUMBER=7
    PC-08 @ May 15, 2026 06:00 AM → PAYCYCLE_NUMBER=8
    ... (continues through PC-26)
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

import dc_email_config as email_config
import dc_leadership_config as dc_config
from email_helper import EmailHelper
from compare_snapshots import ManagerChange, SnapshotComparator
from dc_change_grouper import group_changes_by_dc, load_dc_lookup


# ── PayCycle Calendar ────────────────────────────────────────────────────────
# Maps PayCycle number to target date (when email should send)
PAYCYCLE_DATES = {
    1: datetime(2026, 2, 6),
    2: datetime(2026, 2, 20),
    3: datetime(2026, 3, 6),
    4: datetime(2026, 3, 20),
    5: datetime(2026, 4, 3),
    6: datetime(2026, 4, 17),
    7: datetime(2026, 5, 1),
    8: datetime(2026, 5, 15),
    9: datetime(2026, 5, 29),
    10: datetime(2026, 6, 12),
    11: datetime(2026, 6, 26),
    12: datetime(2026, 7, 10),
    13: datetime(2026, 7, 24),
    14: datetime(2026, 8, 7),
    15: datetime(2026, 8, 21),
    16: datetime(2026, 9, 4),
    17: datetime(2026, 9, 18),
    18: datetime(2026, 10, 2),
    19: datetime(2026, 10, 16),
    20: datetime(2026, 10, 30),
    21: datetime(2026, 11, 13),
    22: datetime(2026, 11, 27),
    23: datetime(2026, 12, 11),
    24: datetime(2026, 12, 25),
    25: datetime(2027, 1, 8),
    26: datetime(2027, 1, 22),
}


def get_paycycle_number() -> int:
    """
    Get PayCycle number from environment variable or command-line argument.
    
    Priority:
    1. Environment variable PAYCYCLE_NUMBER
    2. Command-line argument (first positional)
    3. Error if not specified
    """
    # Check environment variable first
    if 'PAYCYCLE_NUMBER' in os.environ:
        try:
            pc_num = int(os.environ['PAYCYCLE_NUMBER'])
            print(f"[INFO] PayCycle number from environment: {pc_num}")
            return pc_num
        except ValueError:
            print(f"[ERROR] Invalid PAYCYCLE_NUMBER: {os.environ['PAYCYCLE_NUMBER']}")
            sys.exit(1)
    
    # Check command-line argument
    if len(sys.argv) > 1:
        try:
            pc_num = int(sys.argv[1])
            print(f"[INFO] PayCycle number from command line: {pc_num}")
            return pc_num
        except ValueError:
            print(f"[ERROR] Invalid PayCycle number: {sys.argv[1]}")
            sys.exit(1)
    
    # No PayCycle specified
    print("[ERROR] PayCycle number not specified!")
    print("[USAGE] PAYCYCLE_NUMBER=7 python send_paycycle_production_email_generic.py")
    print("[USAGE] python send_paycycle_production_email_generic.py 7")
    sys.exit(1)


def get_paycycle_date(pc_number: int) -> datetime:
    """Get the date for a specific PayCycle."""
    if pc_number not in PAYCYCLE_DATES:
        print(f"[ERROR] Invalid PayCycle number: {pc_number}")
        print(f"[ERROR] Valid range: 1-26")
        sys.exit(1)
    return PAYCYCLE_DATES[pc_number]


def load_snapshot(date: datetime) -> Dict:
    """
    Load manager snapshot for a specific date.
    
    Returns the snapshot JSON, or empty dict if not found.
    """
    date_str = date.strftime("%Y-%m-%d")
    snapshot_path = Path(f"snapshots_local/manager_snapshot_{date_str}.json")
    
    if not snapshot_path.exists():
        print(f"[WARNING] Snapshot not found: {snapshot_path}")
        return {"managers": []}
    
    try:
        with open(snapshot_path) as f:
            snapshot = json.load(f)
        print(f"[OK] Loaded snapshot: {snapshot_path}")
        print(f"     Managers in snapshot: {len(snapshot.get('managers', []))}")
        return snapshot
    except Exception as e:
        print(f"[ERROR] Failed to load snapshot: {e}")
        return {"managers": []}


def detect_paycycle_changes(pc_number: int) -> List[ManagerChange]:
    """
    Detect manager changes for a specific PayCycle.
    
    Compares current PayCycle snapshot with previous PayCycle snapshot (14 days prior).
    
    Returns:
        List of ManagerChange objects (real detected changes)
    """
    current_date = get_paycycle_date(pc_number)
    
    # Calculate previous PayCycle date (14 days prior)
    previous_date = current_date - timedelta(days=14)
    
    print(f"\n[INFO] PayCycle {pc_number}: {current_date.strftime('%B %d, %Y')}")
    print(f"[INFO] Comparing:")
    print(f"       Current:  {current_date.strftime('%Y-%m-%d')}")
    print(f"       Previous: {previous_date.strftime('%Y-%m-%d')}\n")
    
    # Load snapshots
    current_snapshot = load_snapshot(current_date)
    previous_snapshot = load_snapshot(previous_date)
    
    # Detect changes
    print(f"[INFO] Detecting manager changes...")
    comparator = SnapshotComparator(previous_snapshot, current_snapshot)
    changes = comparator.compare()
    
    print(f"[OK] {len(changes)} manager changes detected\n")
    
    return changes


def generate_paycycle_email_html(changes: List[ManagerChange], pc_number: int) -> str:
    """Generate HTML email for PayCycle with detected manager changes."""
    
    paycycle_date = get_paycycle_date(pc_number)
    
    changes_by_role = {}
    for change in changes:
        role = change.role
        if role not in changes_by_role:
            changes_by_role[role] = []
        changes_by_role[role].append(change)
    
    change_count_by_role = {role: len(c) for role, c in changes_by_role.items()}
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #0071ce 0%, #005a9c 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .header p {{
            margin: 8px 0 0 0;
            font-size: 14px;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .summary {{
            background-color: #f0f8ff;
            border-left: 4px solid #0071ce;
            padding: 15px 20px;
            margin-bottom: 25px;
            border-radius: 4px;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 12px;
        }}
        .summary-item {{
            background-color: white;
            padding: 12px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }}
        .summary-item-number {{
            font-size: 24px;
            font-weight: bold;
            color: #0071ce;
        }}
        .summary-item-label {{
            font-size: 12px;
            color: #666;
            margin-top: 4px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section h2 {{
            color: #0071ce;
            border-bottom: 2px solid #0071ce;
            padding-bottom: 10px;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        .change-item {{
            background-color: #f9f9f9;
            border-left: 3px solid #28a745;
            padding: 15px;
            margin-bottom: 12px;
            border-radius: 4px;
        }}
        .change-location {{
            font-weight: 600;
            color: #222;
            font-size: 15px;
            margin-bottom: 5px;
        }}
        .change-detail {{
            font-size: 13px;
            color: #555;
            margin-bottom: 3px;
        }}
        .change-detail strong {{
            color: #333;
        }}
        .arrow {{
            color: #0071ce;
            margin: 0 5px;
            font-weight: bold;
        }}
        .action-box {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 4px;
            padding: 20px;
            margin-top: 30px;
        }}
        .action-box h3 {{
            margin-top: 0;
            color: #856404;
            margin-bottom: 10px;
        }}
        .action-box p {{
            margin: 8px 0;
            color: #333;
            line-height: 1.5;
        }}
        .footer {{
            background-color: #f5f5f5;
            padding: 15px 30px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
        .no-changes {{
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 20px;
            border-radius: 4px;
            text-align: center;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✉️ Manager Change Notification</h1>
            <p>PayCycle {pc_number} • {paycycle_date.strftime('%B %d, %Y')}</p>
        </div>
        
        <div class="content">
            <div class="summary">
                <strong>📋 Summary</strong>
                <div class="summary-grid">
                    <div class="summary-item">
                        <div class="summary-item-number">{len(changes)}</div>
                        <div class="summary-item-label">Total Changes</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-item-number">{len(change_count_by_role)}</div>
                        <div class="summary-item-label">Role Types</div>
                    </div>
                </div>
            </div>
"""
    
    if not changes:
        html += """
            <div class="no-changes">
                <strong>✓ No manager changes detected for this PayCycle</strong>
                <p>All manager positions remain stable.</p>
            </div>
"""
    else:
        # Add changes by role
        for role in sorted(change_count_by_role.keys()):
            role_changes = changes_by_role[role]
            html += f"""
            <div class="section">
                <h2>{role} Changes ({len(role_changes)})</h2>
"""
            for change in role_changes:
                html += f"""
                <div class="change-item">
                    <div class="change-location">{change.location_name} (ID: {change.location_id})</div>
                    <div class="change-detail"><strong>Role:</strong> {change.role}</div>
                    <div class="change-detail">
                        <strong>Transition:</strong> 
                        {change.previous_manager}
                        <span class="arrow">→</span>
                        {change.new_manager}
                    </div>
                    <div class="change-detail"><strong>Location Type:</strong> {change.location_type}</div>
                </div>
"""
            html += """
            </div>
"""
    
    # Action box
    html += """
            <div class="action-box">
                <h3>🎯 What To Do</h3>
                <p>Please make time to meet them and introduce yourself and the team at the DC.</p>
            </div>
        </div>
        
        <div class="footer">
            <p>This is an automated notification from the DC Manager Change Detection System</p>
            <p>PayCycle: {0} | Generated: {1} | Report Type: Manager Change Notification</p>
        </div>
    </div>
</body>
</html>
""".format(pc_number, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    return html


def send_paycycle_email(pc_number: int, changes: List[ManagerChange], html_body: str) -> bool:
    """
    Send PayCycle email to affected DC leadership.
    
    Returns:
        True if sent successfully, False otherwise
    """
    paycycle_date = get_paycycle_date(pc_number)
    
    # Group changes by affected DC
    affected_dcs = group_changes_by_dc(changes)
    
    print(f"[INFO] Identifying affected DCs...")
    for dc_id, emails in affected_dcs.items():
        print(f"  - DC {dc_id}: {len(emails)} recipients")
    
    if not affected_dcs:
        print(f"[INFO] No affected DCs for this PayCycle")
        return False
    
    # Build recipient list
    recipients = []
    for dc_id, emails in affected_dcs.items():
        recipients.extend(emails)
    
    # Email configuration
    subject = f"Manager Change Report - PayCycle {pc_number:02d} ({paycycle_date.strftime('%B %d, %Y')})"
    
    # BCC recipients for internal monitoring
    bcc_recipients = email_config.BCC_RECIPIENTS if hasattr(email_config, 'BCC_RECIPIENTS') else []
    
    # Send email
    print(f"\n[SENDING] Email to affected DC leadership")
    print(f"  Affected DCs: {len(affected_dcs)}")
    print(f"  Primary Recipients: {len(recipients)}")
    print(f"  BCC Recipients: {len(bcc_recipients)}")
    print(f"  Subject: {subject}\n")
    
    email_helper = EmailHelper(test_mode=False)  # Production mode
    success = email_helper.send_email_via_outlook(
        to=recipients,
        subject=subject,
        body_html=html_body,
        from_email=email_config.SEND_FROM_EMAIL if hasattr(email_config, 'SEND_FROM_EMAIL') else "supplychainops@email.wal-mart.com",
        bcc=bcc_recipients
    )
    
    return success


def update_tracking(pc_number: int, success: bool, recipients_count: int = 0):
    """Update paycycle_tracking.json with execution results."""
    tracking_path = Path("paycycle_tracking.json")
    
    if not tracking_path.exists():
        print(f"[WARNING] Tracking file not found: {tracking_path}")
        return
    
    try:
        with open(tracking_path) as f:
            tracking = json.load(f)
        
        # Find and update PC entry
        for pc in tracking.get("paycycles", []):
            if pc.get("pc_number") == pc_number:
                pc["actual_send_time"] = datetime.now().strftime("%H:%M")
                pc["actual_send_datetime"] = datetime.now().isoformat()
                pc["status"] = "completed" if success else "failed"
                pc["recipients_count"] = recipients_count
                break
        
        with open(tracking_path, 'w') as f:
            json.dump(tracking, f, indent=2)
        
        print(f"[OK] Tracking file updated for PC-{pc_number}")
    
    except Exception as e:
        print(f"[ERROR] Failed to update tracking: {e}")


def main():
    """Main entry point."""
    print("=" * 70)
    print("GENERIC PAYCYCLE MANAGER CHANGE EMAIL - PRODUCTION")
    print("=" * 70)
    
    # Get PayCycle number
    pc_number = get_paycycle_number()
    
    # Detect changes
    changes = detect_paycycle_changes(pc_number)
    
    # Generate email
    print(f"[INFO] Generating email HTML...")
    html_body = generate_paycycle_email_html(changes, pc_number)
    print(f"[OK] Email HTML generated\n")
    
    # Send email (only if there are changes)
    if changes:
        success = send_paycycle_email(pc_number, changes, html_body)
        update_tracking(pc_number, success, len(changes) * 2)  # Roughly 2 recipients per change (GM + AGM)
        
        if success:
            print(f"\n[SUCCESS] PC-{pc_number} email sent to affected DC leadership!")
        else:
            print(f"\n[ERROR] PC-{pc_number} email send failed!")
            return 1
    else:
        print(f"[INFO] No manager changes detected for PC-{pc_number}")
        update_tracking(pc_number, True, 0)
    
    print("\n" + "=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
