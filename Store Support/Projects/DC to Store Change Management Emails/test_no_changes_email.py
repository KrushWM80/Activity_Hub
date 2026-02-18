#!/usr/bin/env python3
"""Test the no changes notification email"""

from email_helper import EmailHelper
from datetime import datetime

print("Testing 'No Changes' Notification Email...\n")

# Create email helper
email_helper = EmailHelper(test_mode=True)

# Get today's date
today_str = datetime.now().strftime("%Y-%m-%d")

print(f"Sending 'no changes' email for date: {today_str}\n")

# Send the email
success = email_helper.send_no_changes_notification(today_str)

if success:
    print("\n[SUCCESS] Email sent! Check your inbox.")
else:
    print("\n[FAILED] Email did not send.")
