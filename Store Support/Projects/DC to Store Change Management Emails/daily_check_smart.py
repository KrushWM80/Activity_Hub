#!/usr/bin/env python3
"""
Smart Daily Check - Only runs if we don't already have today's snapshot
This prevents duplicate runs and SDL scraping issues

With VPN retry logic:
- Task Scheduler runs this hourly
- Tracks when first attempt was made
- Keeps trying for up to 7 days
- Only sends error email after 7 days of no VPN
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

def main():
    today_str = datetime.now().strftime("%Y-%m-%d")
    snapshot_file = Path(f"snapshots_local/manager_snapshot_{today_str}.json")
    retry_tracker_file = Path("vpn_retry_tracker.json")
    
    print(f"\n{'='*60}")
    print(f"SMART DAILY CHECK WITH VPN RETRY")
    print(f"Date: {today_str}")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Check if we already processed today
    if snapshot_file.exists():
        print(f"[INFO] Snapshot already exists for {today_str}")
        print(f"[INFO] Skipping daily check (already completed today)")
        print(f"[INFO] File: {snapshot_file}\n")
        
        # Clear retry tracker since we successfully completed
        if retry_tracker_file.exists():
            retry_tracker_file.unlink()
            print(f"[INFO] Cleared VPN retry tracker\n")
        
        # Send confirmation email that task ran but was already completed
        print(f"[INFO] Sending 'already ran' confirmation email...\n")
        import dc_email_config as email_config
        from email_helper import EmailHelper
        
        # Create a simple confirmation email
        confirmation_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .header {{ background: #0071ce; color: white; padding: 20px; border-radius: 8px; }}
        .content {{ padding: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>✅ Daily Check - Already Completed</h1>
    </div>
    <div class="content">
        <p><strong>Date:</strong> {today_str}</p>
        <p><strong>Status:</strong> Task ran successfully but daily check was already completed earlier today.</p>
        <p><strong>Snapshot:</strong> {snapshot_file}</p>
        <p>No duplicate processing needed.</p>
    </div>
</body>
</html>
"""
        
        # Send confirmation email via Outlook COM
        try:
            email_helper = EmailHelper(test_mode=True)  # Send to admin only
            success = email_helper.send_email_via_outlook(
                to=[email_config.get_admin_email()],
                subject=f"Daily Check Confirmation - {today_str}",
                body_html=confirmation_html,
                from_email="supplychainops@email.wal-mart.com"
            )
            
            if success:
                print(f"[OK] Confirmation email sent\n")
            else:
                print(f"[ERROR] Failed to send confirmation email\n")
        except Exception as e:
            print(f"[ERROR] Failed to send confirmation: {e}\n")
        return 0
    
    # No snapshot for today - need to run daily check
    print(f"[INFO] No snapshot found for {today_str}")
    
    # Check VPN retry tracker
    if retry_tracker_file.exists():
        with open(retry_tracker_file, 'r') as f:
            tracker = json.load(f)
        
        first_attempt = datetime.fromisoformat(tracker['first_attempt'])
        target_date = tracker['target_date']
        
        print(f"[INFO] VPN retry tracking active since {first_attempt.strftime('%Y-%m-%d %H:%M')}")
        print(f"[INFO] Target snapshot date: {target_date}")
        
        # Check if we've been trying for more than 7 days
        days_trying = (datetime.now() - first_attempt).days
        if days_trying >= 7:
            print(f"\n[ERROR] VPN unavailable for {days_trying} days - exceeds 7 day limit")
            print(f"[ERROR] Sending error notification and giving up\n")
            
            # Send error email
            try:
                import dc_email_config as email_config
                from email_helper import EmailHelper
                
                email_helper = EmailHelper(test_mode=True)
                error_msg = f"VPN unavailable for {days_trying} days (since {first_attempt.strftime('%Y-%m-%d %H:%M')}). Cannot fetch SDL data. Manual intervention required."
                email_helper.send_error_notification(error_msg, today_str)
                print(f"[OK] Error email sent\n")
            except Exception as e:
                print(f"[ERROR] Could not send error email: {e}\n")
            
            # Clear tracker and exit
            retry_tracker_file.unlink()
            return 1
        
        print(f"[INFO] Will keep trying (day {days_trying + 1}/7)\n")
    else:
        # First attempt for this date
        print(f"[INFO] First attempt for {today_str}")
        tracker = {
            'first_attempt': datetime.now().isoformat(),
            'target_date': today_str
        }
        with open(retry_tracker_file, 'w') as f:
            json.dump(tracker, f, indent=2)
        print(f"[INFO] Created VPN retry tracker\n")
    
    # Try to run daily check
    print(f"[INFO] Running daily check...\n")
    
    import subprocess
    result = subprocess.run(
        [sys.executable, "daily_check.py"],
        capture_output=False,
        text=True
    )
    
    # If successful, clear the tracker
    if result.returncode == 0:
        if retry_tracker_file.exists():
            retry_tracker_file.unlink()
            print(f"\n[OK] Successfully completed - cleared retry tracker")
    
    return result.returncode

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
