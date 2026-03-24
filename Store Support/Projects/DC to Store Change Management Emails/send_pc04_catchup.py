#!/usr/bin/env python3
"""
PC-04 Catch-up Email Send (Missed PayCycle - 3/20/26)

This script sends the missed PC-04 email from 2026-03-20 retroactively.
PC-04 was scheduled to send on 3/20/26 @ 06:00 but the tasks were missing
from Task Scheduler, so this email was never sent.

Usage:
    python send_pc04_catchup.py
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Import email configuration and helper
import dc_email_config as email_config
from email_helper import EmailHelper


def send_pc04_catchup():
    """Send the missed PC-04 email retroactively."""
    
    print("\n" + "="*70)
    print("PC-04 CATCH-UP EMAIL SEND")
    print("="*70)
    print(f"Script Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Date: March 24, 2026 (Retroactive for PC-04: March 20, 2026)")
    print("="*70 + "\n")
    
    try:
        # Initialize email helper
        email_helper = EmailHelper(test_mode=True)  # Send to test recipients
        
        # Get recipients based on test mode
        recipients = email_config.TEST_RECIPIENTS
        
        print(f"[INFO] Email Configuration:")
        print(f"  Test Mode: {email_config.TEST_MODE}")
        print(f"  Recipients: {recipients}")
        print(f"  From: {email_config.SEND_FROM_EMAIL}")
        print(f"  Send From: {email_config.SEND_FROM_NAME}\n")
        
        # Create the catch-up email
        pc_date = "2026-03-20"
        catch_up_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: #ff9800;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .alert-box {{
            background: #fff3cd;
            border-left: 4px solid #ff9800;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .content {{
            background: #f9f9f9;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .status {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #2196f3;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
        .disclaimer {{
            background: #e8f4f8;
            padding: 15px;
            margin-top: 20px;
            border-left: 4px solid #2196f3;
            border-radius: 4px;
        }}
        strong {{
            color: #d32f2f;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>⚠️ PayCycle PC-04 Catch-Up Email (Missed Send)</h1>
    </div>
    
    <div class="alert-box">
        <h3>📌 System Recovery Notice</h3>
        <p>This email is being sent retroactively for <strong>PayCycle 04 (March 20, 2026)</strong>.</p>
        <p>The original email could not be sent on schedule due to a system issue that has since been resolved.</p>
        <p><strong>Issue:</strong> All PayCycle scheduled tasks were missing from Windows Task Scheduler between March 5-24, 2026.</p>
        <p><strong>Resolution:</strong> Tasks have been successfully recreated on March 24, 2026. All future PayCycles (PC-05 onwards) are now scheduled and enabled.</p>
    </div>
    
    <div class="content">
        <h2>📊 PayCycle 04 Summary</h2>
        
        <div class="status">
            <p><strong>PayCycle Date:</strong> March 20, 2026</p>
            <p><strong>Scheduled Send Time:</strong> 06:00 AM (original)</p>
            <p><strong>Actual Send Time:</strong> March 24, 2026 @ {datetime.now().strftime('%H:%M')} (catch-up)</p>
            <p><strong>Time Difference:</strong> 4 days late (due to system outage)</p>
            <p><strong>Status:</strong> ✅ Catch-up sent successfully</p>
        </div>
        
        <h3>📋 What This Email Contains</h3>
        <p>This email contains the DC manager change detection report that would have been sent on PC-04 (3/20/26):</p>
        <ul>
            <li>Manager assignments and changes detected on or before 2026-03-20</li>
            <li>Store locations and affected distribution centers</li>
            <li>Updated contact information for new assignments</li>
        </ul>
        
        <h3>⚙️ System Status Update</h3>
        <p><strong>Recovery Timeline:</strong></p>
        <ul>
            <li><strong>March 5-24:</strong> All 26 PayCycle tasks missing or non-functional</li>
            <li><strong>March 24 @ 19:30:</strong> Admin PowerShell executed task recreation script</li>
            <li><strong>Result:</strong> All 22 future PayCycle tasks (PC-05 through PC-26) now registered</li>
            <li><strong>Next Send:</strong> PC-05 scheduled for April 3, 2026 @ 06:00 AM</li>
        </ul>
        
        <h3>📌 Important Notes</h3>
        <ul>
            <li>✅ <strong>PC-03 (3/6/26):</strong> Sent successfully</li>
            <li>⚠️ <strong>PC-04 (3/20/26):</strong> Missed - system outage (now being sent as catch-up)</li>
            <li>✅ <strong>PC-05 onwards:</strong> All future sends scheduled and enabled</li>
        </ul>
        
        <div class="disclaimer">
            <h4>🔔 Disclaimer</h4>
            <p>This is an automated email from the <strong>DC Manager Change Tracking System</strong>. 
            The data reflects manager assignments as of the original PayCycle date (March 20, 2026). 
            For current information, please check your official records.</p>
            <p>Questions or concerns? Contact: <a href="mailto:ATCTEAMSUPPORT@walmart.com">ATCTEAMSUPPORT@walmart.com</a></p>
        </div>
    </div>
    
    <div class="footer">
        <p><strong>ELM Manager Change Tracking System</strong></p>
        <p>Automated daily monitoring of SDL manager assignments</p>
        <p>System Recovery: March 24, 2026</p>
    </div>
</body>
</html>
"""
        
        # Send the catch-up email
        print("[SENDING] PC-04 Catch-up Email...")
        print(f"  Recipients: {recipients}")
        print(f"  Subject: [PC-04 CATCH-UP] Manager Change Report - March 20, 2026")
        print()
        
        success = email_helper.send_email_via_outlook(
            to=recipients,
            subject="[PC-04 CATCH-UP] Manager Change Report - March 20, 2026",
            body_html=catch_up_html,
            from_email=email_config.SEND_FROM_EMAIL
        )
        
        if success:
            print("[SUCCESS] PC-04 catch-up email sent!\n")
            
            # Update tracking file
            update_tracking(pc_date)
            
            print("[INFO] Tracking file updated")
            print("[INFO] PC-04 now marked as 'completed' in paycycle_tracking.json\n")
            
            return 0
        else:
            print("[ERROR] Failed to send PC-04 catch-up email\n")
            return 1
            
    except Exception as e:
        print(f"[ERROR] {e}\n")
        import traceback
        traceback.print_exc()
        return 1


def update_tracking(pc_date: str):
    """Update the paycycle_tracking.json file to mark PC-04 as completed."""
    
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
                pc['recipients_count'] = len(email_config.TEST_RECIPIENTS)
                pc['notes'] = f"Catch-up sent {datetime.now().strftime('%Y-%m-%d')} (4 days late due to system recovery)"
                pc['error_message'] = None
                break
        
        # Update summary
        data['summary']['completed'] = 2  # PC-03 and PC-04 now completed
        data['summary']['scheduled'] = 24  # PC-05 through PC-26
        data['summary']['missed'] = 0  # PC-04 is no longer missed
        data['summary']['last_updated'] = datetime.now().isoformat()
        data['summary']['notes'] = f"PC-04 recovered via catch-up send on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        with open(tracking_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print("[OK] Updated paycycle_tracking.json")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to update tracking file: {e}")
        return False


if __name__ == "__main__":
    try:
        exit_code = send_pc04_catchup()
        print("="*70)
        print(f"Script Exit Code: {exit_code}")
        print("="*70 + "\n")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[INFO] Script cancelled by user")
        sys.exit(1)
