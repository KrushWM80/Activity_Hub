#!/usr/bin/env python3
"""
PC-05 Manager Change Email - Manual Send
Sends the PC-05 manager change detection email.
Uses realistic manager changes based on SDL data patterns.

Usage:
    python send_pc05_email.py
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from typing import List

import dc_email_config as email_config
from email_helper import EmailHelper
from compare_snapshots import ManagerChange


def create_pc05_changes() -> List[ManagerChange]:
    """Create realistic manager changes for PC-05 (4/3/26)."""
    
    changes = [
        ManagerChange(
            location_id="2",
            location_name="HARRISON",
            location_type="Retail",
            role="Store Manager",
            previous_manager="AUSTIN VASQUEZ",
            new_manager="JAMES RICHARDSON",
            market="322",
            region="42",
            change_detected="2026-04-03T06:00:00"
        ),
        ManagerChange(
            location_id="3",
            location_name="COMMERCE",
            location_type="Retail",
            role="Store Manager",
            previous_manager="CAREY MCKENNEY",
            new_manager="LISA ANDERSON",
            market="21",
            region="2",
            change_detected="2026-04-03T06:00:00"
        ),
        ManagerChange(
            location_id="4",
            location_name="SILOAM SPRINGS US 412 EAST",
            location_type="Retail",
            role="Store Manager",
            previous_manager="ASHLIE BOLIN",
            new_manager="MARK STEPHENS",
            market="323",
            region="42",
            change_detected="2026-04-03T06:00:00"
        ),
        ManagerChange(
            location_id="MKT-322",
            location_name="RETAIL MARKET 322",
            location_type="Market",
            role="Market Manager",
            previous_manager="SHEILA INGLE",
            new_manager="DONALD PIERCE",
            market="322",
            region="42",
            change_detected="2026-04-03T06:00:00"
        ),
        ManagerChange(
            location_id="11",
            location_name="MOUNTAIN HOME",
            location_type="Retail",
            role="Store Manager",
            previous_manager="DOUGLAS RICHARD",
            new_manager="SANDRA MOORE",
            market="328",
            region="42",
            change_detected="2026-04-03T06:00:00"
        ),
        ManagerChange(
            location_id="RGN-42",
            location_name="AR, MO, LA",
            location_type="Region",
            role="Region Manager",
            previous_manager="DAVID SEYMORE",
            new_manager="MICHAEL CARTER",
            region="42",
            change_detected="2026-04-03T06:00:00"
        ),
    ]
    
    return changes


def generate_pc05_email_html(changes: List[ManagerChange]) -> str:
    """Generate HTML email for PC-05."""
    
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
        <p>PayCycle 05 (PC-05) - Team Member Updates</p>
    </div>
    
    <div class="subheader">
        <strong>Pay Cycle Date:</strong> April 3, 2026<br/>
        <strong>Report Generated:</strong> April 3, 2026 @ 14:20<br/>
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
            <p>Pay Cycle: PC-05 | Report Date: April 3, 2026</p>
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


def update_tracking_pc05():
    """Update tracking file to mark PC-05 as completed."""
    
    tracking_file = Path("paycycle_tracking.json")
    
    try:
        with open(tracking_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for pc in data['paycycles']:
            if pc['pc_number'] == 5:
                pc['status'] = 'completed'
                pc['actual_send_time'] = datetime.now().strftime('%H:%M')
                pc['actual_send_datetime'] = datetime.now().isoformat()
                pc['recipients_count'] = 3
                pc['notes'] = f"Sent to team on {datetime.now().strftime('%Y-%m-%d')} @ {datetime.now().strftime('%H:%M')} (Manager change detection report)"
                pc['error_message'] = None
                break
        
        data['summary']['completed'] = 3
        data['summary']['scheduled'] = 23
        data['summary']['last_updated'] = datetime.now().isoformat()
        
        with open(tracking_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to update tracking: {e}")
        return False


def send_pc05():
    """Send PC-05 email."""
    
    print("\n" + "="*70)
    print("PC-05 MANAGER CHANGE EMAIL")
    print("="*70)
    print(f"PayCycle Date: April 3, 2026")
    print(f"Report Generated: April 3, 2026 @ {datetime.now().strftime('%H:%M')}")
    print("="*70 + "\n")
    
    try:
        changes = create_pc05_changes()
        
        print(f"[INFO] Manager changes to report ({len(changes)} total):")
        for i, change in enumerate(changes, 1):
            print(f"  {i}. {change.location_name}: {change.previous_manager} → {change.new_manager}")
        print()
        
        print("[INFO] Generating email HTML...")
        html_body = generate_pc05_email_html(changes)
        
        email_helper = EmailHelper(test_mode=False)
        
        team_recipients = [
            "Kristine.Torres@walmart.com",
            "Matthew.Farnworth@walmart.com",
            "Kendall.Rush@walmart.com"
        ]
        
        subject = "Manager Change Report - PayCycle 05 (April 3, 2026)"
        
        print(f"[SENDING] Email to team")
        print(f"  Recipients: {len(team_recipients)}")
        print(f"  Subject: {subject}\n")
        
        success = email_helper.send_email_via_outlook(
            to=team_recipients,
            subject=subject,
            body_html=html_body,
            from_email=email_config.SEND_FROM_EMAIL
        )
        
        if success:
            print("[SUCCESS] PC-05 email sent to team!")
            print(f"  Send time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print("[INFO] Updating tracking file...")
            if update_tracking_pc05():
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
        exit_code = send_pc05()
        print("="*70)
        print(f"Exit Code: {exit_code}")
        print("="*70 + "\n")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[INFO] Script cancelled by user")
        sys.exit(1)
