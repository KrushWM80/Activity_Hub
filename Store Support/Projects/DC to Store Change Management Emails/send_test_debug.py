#!/usr/bin/env python3
"""Debug email sending to identify the issue"""

import sys
import traceback
from datetime import datetime

import config
import dc_email_config as email_config

test_recipients = config.TEST_EMAILS if hasattr(config, 'TEST_EMAILS') else [config.TEST_EMAIL]

print("\n" + "="*70)
print("DEBUG: Testing Outlook COM Email Send")
print("="*70 + "\n")

print("[CONFIG]")
print(f"  Test Recipients: {test_recipients}")
print(f"  Test Mode: {config.TEST_MODE}")
print(f"  Send From: {email_config.SEND_FROM_EMAIL}\n")

# Create simple test email
email_subject = "✅ TEST EMAIL - Actually Sent from Python"
email_body = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .header {{ background: #0071ce; color: white; padding: 20px; }}
        .content {{ padding: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>✅ TEST EMAIL - Sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>
    </div>
    <div class="content">
        <p>If you are reading this, the email was successfully sent from Python!</p>
        <p>Recipients: {', '.join(test_recipients)}</p>
    </div>
</body>
</html>"""

print("[STEP 1] Importing win32com...")
try:
    import win32com.client
    print("  ✅ Successfully imported win32com.client\n")
except ImportError as e:
    print(f"  ❌ FAILED: {e}\n")
    sys.exit(1)

print("[STEP 2] Creating Outlook application object...")
try:
    outlook = win32com.client.Dispatch('Outlook.Application')
    print("  ✅ Successfully created Outlook.Application object\n")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    print(f"  Error type: {type(e).__name__}")
    traceback.print_exc()
    sys.exit(1)

print("[STEP 3] Creating email item...")
try:
    mail = outlook.CreateItem(0)  # 0 = olMailItem
    print("  ✅ Successfully created mail item\n")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    print(f"  Error type: {type(e).__name__}")
    traceback.print_exc()
    sys.exit(1)

print("[STEP 4] Setting email properties...")
try:
    print(f"  Setting To: {', '.join(test_recipients)}")
    mail.To = '; '.join(test_recipients)
    print("  ✅ To field set")
    
    print(f"  Setting Subject: {email_subject}")
    mail.Subject = email_subject
    print("  ✅ Subject set")
    
    print(f"  Setting HTML body ({len(email_body)} bytes)")
    mail.HTMLBody = email_body
    print("  ✅ HTMLBody set\n")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    print(f"  Error type: {type(e).__name__}")
    traceback.print_exc()
    sys.exit(1)

print("[STEP 5] Sending email...")
try:
    mail.Send()
    print("  ✅ Email sent successfully!\n")
    print("="*70)
    print("✅ SUCCESS - Email was sent to:")
    for email in test_recipients:
        print(f"   • {email}")
    print("="*70 + "\n")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    print(f"  Error type: {type(e).__name__}")
    traceback.print_exc()
    
    print("\n[TROUBLESHOOTING]")
    print("  Possible solutions:")
    print("  1. Make sure Outlook is configured with an account")
    print("  2. Check that the email addresses are valid")
    print("  3. Try sending from a different account")
    print("  4. Check Outlook settings/security\n")
    sys.exit(1)
