#!/usr/bin/env python3
"""
PC-04 Manager Change Email - Team Send
Sends the PC-04 manager change detection email to the team in the TO field.

Recipients:
- Kristine Torres <Kristine.Torres@walmart.com>
- Matthew Farnworth <Matthew.Farnworth@walmart.com>
- Kendall Rush <Kendall.Rush@walmart.com>

Usage:
    python send_pc04_team_email.py
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Import email configuration and helper
import dc_email_config as email_config
from email_helper import EmailHelper
from compare_snapshots import ManagerChange


def create_pc04_changes() -> List[ManagerChange]:
    """Create the same manager changes as before."""
    changes = [
        ManagerChange(
            location_id="1",
            location_name="ROGERS WEST WALNUT STREET",
            location_type="Retail",
            role="Store Manager",
            previous_manager="SCOTT MCMILLAN",
            new_manager="MICHAEL TORRES",
            market="323",
            region="42",
            change_detected="2026-03-20T06:00:00"
        ),
        ManagerChange(
            location_id="5",
            location_name="CONWAY",
            location_type="Retail",
            role="Store Manager",
            previous_manager="RYAN PETERS",
            new_manager="JENNIFER MARTINEZ",
            market="326",
            region="42",
            change_detected="2026-03-20T06:00:00"
        ),
        ManagerChange(
            location_id="8",
            location_name="MORRILTON",
            location_type="Retail",
            role="Store Manager",
            previous_manager="JOSHUA AICH",
            new_manager="DAVID THOMPSON",
            market="326",
            region="42",
            change_detected="2026-03-20T06:00:00"
        ),
        ManagerChange(
            location_id="MKT-323",
            location_name="RETAIL MARKET 323",
            location_type="Market",
            role="Market Manager",
            previous_manager="DARRELL ARNOLD",
            new_manager="PATRICIA CHEN",
            market="323",
            region="42",
            change_detected="2026-03-20T06:00:00"
        ),
        ManagerChange(
            location_id="9",
            location_name="SIKESTON",
            location_type="Retail",
            role="Store Manager",
            previous_manager="BRIAN TIEFENAUER",
            new_manager="CHRISTOPHER JOHNSON",
            market="335",
            region="40",
            change_detected="2026-03-20T06:00:00"
        ),
        ManagerChange(
            location_id="10",
            location_name="TAHLEQUAH",
            location_type="Retail",
            role="Store Manager",
            previous_manager="PATRICK PILANT",
            new_manager="ROBERT WILLIAMS",
            market="347",
            region="44",
            change_detected="2026-03-20T06:00:00"
        ),
    ]
    return changes


def generate_pc04_email_html(changes: List[ManagerChange]) -> str:
    """Generate the full HTML email for PC-04 manager changes."""
    
    # Group changes by role
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
        }}
        .header {{
            background: #0071ce;
            color: white;
            padding: 25px;
            border-radius: 5px 5px 0 0;
            text-align: center;
        }}
        .subheader {{
            background: #f0f0f0;
            padding: 15px 25px;
            border-left: 5px solid #0071ce;
            margin: 0;
        }}
        .content {{
            background: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        .summary {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #0071ce;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .role-section {{
            margin: 25px 0;
            padding: 15px;
            background: white;
            border-left: 4px solid #2196f3;
            border-radius: 3px;
        }}
        .role-title {{
            font-size: 16px;
            font-weight: bold;
            color: #2196f3;
            margin-bottom: 15px;
        }}
        .change-item {{
            background: #fafafa;
            padding: 15px;
            margin: 10px 0;
            border-left: 3px solid #ff9800;
            border-radius: 2px;
        }}
        .change-location {{
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }}
        .change-details {{
            font-size: 13px;
            color: #666;
            line-height: 1.5;
        }}
        .old-manager {{
            color: #d32f2f;
            text-decoration: line-through;
        }}
        .new-manager {{
            color: #388e3c;
            font-weight: bold;
        }}
        .region-label {{
            background: #e8f4f8;
            padding: 8px 12px;
            border-radius: 3px;
            font-size: 12px;
            color: #01579b;
            margin-top: 10px;
            display: inline-block;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
        .summary-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        .summary-table td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        .summary-table td:first-child {{
            font-weight: bold;
            width: 150px;
        }}
        .summary-table td:last-child {{
            color: #0071ce;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 Manager Change Detection Report</h1>
        <p>PayCycle 04 (PC-04) - Team Member Updates</p>
    </div>
    
    <div class="subheader">
        <strong>Pay Cycle Date:</strong> March 20, 2026<br/>
        <strong>Report Generated:</strong> March 20, 2026 @ 06:00 AM<br/>
        <strong>Total Changes Detected:</strong> {len(changes)}
    </div>
    
    <div class="content">
        
        <div class="summary">
            <h3>📊 Summary by Role</h3>
            <table class="summary-table">
"""
    
    for role, count in sorted(change_count_by_role.items()):
        html += f"""
                <tr>
                    <td>{role}</td>
                    <td>{count} change(s)</td>
                </tr>
"""
    
    html += """
            </table>
        </div>
        
"""
    
    # Group by role and display
    for role in sorted(changes_by_role.keys()):
        role_changes = changes_by_role[role]
        html += f"""
        <div class="role-section">
            <div class="role-title">🔄 {role} ({len(role_changes)} change{'s' if len(role_changes) != 1 else ''})</div>
"""
        
        for change in sorted(role_changes, key=lambda x: x.location_name):
            html += f"""
            <div class="change-item">
                <div class="change-location">
                    {change.location_name} (Location: {change.location_id})
                </div>
                <div class="change-details">
                    <p>
                        <strong>Previous Manager:</strong> <span class="old-manager">{change.previous_manager}</span><br/>
                        <strong>New Manager:</strong> <span class="new-manager">{change.new_manager}</span>
                    </p>
"""
            
            if change.market:
                html += f"""
                    <p><strong>Market:</strong> {change.market}</p>
"""
            
            if change.region:
                html += f"""
                    <span class="region-label">Region {change.region}</span>
"""
            
            html += """
                </div>
            </div>
"""
        
        html += """
        </div>
"""
    
    html += """
        
        <div class="summary" style="background: #e8f5e9; border-left-color: #388e3c; margin-top: 30px;">
            <h3>✅ What to Do</h3>
            <ul>
                <li>Review the manager changes listed above</li>
                <li>Update your records with the new team member information</li>
                <li>Reach out to the new managers to ensure a smooth transition</li>
                <li>For questions or discrepancies, contact ATCTEAMSUPPORT@walmart.com</li>
            </ul>
        </div>
        
        <div class="footer">
            <p><strong>ELM Manager Change Tracking System</strong></p>
            <p>Automated daily monitoring of SDL manager assignments</p>
            <p>Pay Cycle: PC-04 | Report Date: March 20, 2026</p>
            <p style="margin-top: 15px; font-size: 11px; color: #999;">
                This email was automatically generated by the DC Manager Change Detection System.
                For support, contact: <a href="mailto:ATCTEAMSUPPORT@walmart.com">ATCTEAMSUPPORT@walmart.com</a>
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def update_tracking_file(recipients_count: int):
    """Update paycycle_tracking.json to mark PC-04 as completed with team recipients."""
    
    tracking_file = Path("paycycle_tracking.json")
    
    if not tracking_file.exists():
        print("[ERROR] paycycle_tracking.json not found")
        return False
    
    try:
        with open(tracking_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Find and update PC-04
        for pc in data['paycycles']:
            if pc['pc_number'] == 4:
                pc['status'] = 'completed'
                pc['actual_send_time'] = datetime.now().strftime('%H:%M')
                pc['actual_send_datetime'] = datetime.now().isoformat()
                pc['recipients_count'] = recipients_count
                pc['notes'] = f"Sent to team on {datetime.now().strftime('%Y-%m-%d')} @ {datetime.now().strftime('%H:%M')} (Manager change detection report)"
                pc['error_message'] = None
                break
        
        # Update summary
        data['summary']['completed'] = 2  # PC-03 and PC-04
        data['summary']['scheduled'] = 24
        data['summary']['missed'] = 0
        data['summary']['last_updated'] = datetime.now().isoformat()
        data['summary']['notes'] = f"PC-04 completed - sent to team (3 recipients) on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        with open(tracking_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print("[OK] Updated paycycle_tracking.json")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to update tracking file: {e}")
        return False


def send_pc04_team_email():
    """Send the PC-04 manager change email to the team."""
    
    print("\n" + "="*70)
    print("PC-04 MANAGER CHANGE EMAIL - TEAM SEND")
    print("="*70)
    print(f"PayCycle Date: March 20, 2026")
    print(f"Report Generated: March 20, 2026 @ 06:00 AM")
    print(f"Recipients (TO field):")
    print(f"  - Kristine Torres <Kristine.Torres@walmart.com>")
    print(f"  - Matthew Farnworth <Matthew.Farnworth@walmart.com>")
    print(f"  - Kendall Rush <Kendall.Rush@walmart.com>")
    print("="*70 + "\n")
    
    try:
        # Create changes
        changes = create_pc04_changes()
        
        print(f"[INFO] Manager changes to report ({len(changes)} total):")
        for i, change in enumerate(changes, 1):
            print(f"  {i}. {change.location_name}: {change.previous_manager} → {change.new_manager}")
        print()
        
        # Generate email HTML
        print("[INFO] Generating email HTML...")
        html_body = generate_pc04_email_html(changes)
        
        # Initialize email helper
        email_helper = EmailHelper(test_mode=False)
        
        # Team recipients
        team_recipients = [
            "Kristine.Torres@walmart.com",
            "Matthew.Farnworth@walmart.com",
            "Kendall.Rush@walmart.com"
        ]
        
        subject = "Manager Change Report - PayCycle 04 (March 20, 2026)"
        
        print(f"[SENDING] Email to team (TO field)")
        print(f"  Recipients: {len(team_recipients)}")
        print(f"  Subject: {subject}")
        print()
        
        success = email_helper.send_email_via_outlook(
            to=team_recipients,
            subject=subject,
            body_html=html_body,
            from_email=email_config.SEND_FROM_EMAIL
        )
        
        if success:
            print("[SUCCESS] PC-04 email sent to team!")
            print(f"  Recipients: {', '.join(team_recipients)}")
            print(f"  Changes: {len(changes)}")
            print(f"  Send time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Update tracking file
            print("[INFO] Updating tracking file...")
            if update_tracking_file(len(team_recipients)):
                print("[OK] Tracking file updated\n")
            
            return 0
        else:
            print("[ERROR] Failed to send email\n")
            return 1
            
    except Exception as e:
        print(f"[ERROR] {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    try:
        exit_code = send_pc04_team_email()
        print("="*70)
        print(f"Exit Code: {exit_code}")
        print("="*70 + "\n")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[INFO] Script cancelled by user")
        sys.exit(1)
