import os
import sys

# Add path to email helper
sys.path.insert(0, r'C:\Users\krush\Documents\VSCode\Activity-Hub\Store Support\Projects\DC to Store Change Management Emails')

from email_helper import EmailHelper

# Read the HTML email content
email_file = r'C:\Users\krush\Documents\VSCode\Activity-Hub\Store Support\Projects\DC to Store Change Management Emails\emails_sent\DC-EMAIL-PC-03-REVIEW-20260306_140000.html'

with open(email_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Test recipients
recipients = [
    'Kristine.Torres@walmart.com',
    'Matthew.Farnworth@walmart.com',
    'Kendall.Rush@walmart.com'
]

# Send email to all recipients
subject = 'PayCycle 3 - Recent Field Leadership Updates (March 6, 2026)'

email_helper = EmailHelper(test_mode=False)
try:
    success = email_helper.send_email_via_outlook(
        to=recipients,
        subject=subject,
        body_html=html_content,
        from_email='supplychainops@email.wal-mart.com'
    )
    if success:
        print("\n✓ PayCycle 3 email sent successfully to all recipients!")
    else:
        print("\n✗ Failed to send email")
except Exception as e:
    print(f"\n✗ Error sending email: {e}")
