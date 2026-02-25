#!/usr/bin/env python3
"""
Send Actual Test Email - With Multiple Delivery Methods
Tries: Outlook COM → SMTP → Queue for Code Puppy
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Import configuration
import config
import dc_email_config as email_config

print("\n" + "="*70)
print("ACTUAL EMAIL SEND TEST - 3 Recipients")
print("="*70 + "\n")

# Get test recipients
test_recipients = config.TEST_EMAILS if hasattr(config, 'TEST_EMAILS') else [config.TEST_EMAIL]

print("[RECIPIENTS] Email will be sent to:")
for i, email in enumerate(test_recipients, 1):
    print(f"  {i}. {email}")
print()

# Create test email HTML
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_str = datetime.now().strftime("%Y-%m-%d")

email_body = f"""<!DOCTYPE html>
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
            background: linear-gradient(135deg, #0071ce 0%, #00a4e4 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
            text-align: center;
        }}
        .content {{
            background: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 8px 8px;
        }}
        .test-badge {{
            display: inline-block;
            background: #ffc107;
            color: #333;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .info-box {{
            background: #e7f3ff;
            border-left: 4px solid #0071ce;
            padding: 15px;
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
        .recipient-list {{
            background: white;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>✅ SYSTEM TEST - ACTUAL SEND TEST</h1>
        <p>Manager Change Detection System - Email Delivery Verification</p>
    </div>
    
    <div class="content">
        <div class="test-badge">
            ✓ TEST: 3-Recipient Configuration Active
        </div>
        
        <div class="info-box">
            <h2 style="margin: 0 0 10px 0; color: #0071ce;">✅ This Email Was Actually Sent!</h2>
            <p style="margin: 0;">If you received this, the email system is working correctly!</p>
        </div>
        
        <h3>Email Recipients:</h3>
        <div class="recipient-list">
            <strong>This email was sent to:</strong>
            <ul style="margin: 10px 0; list-style-position: inside;">
                <li>Kristine.Torres@walmart.com</li>
                <li>Matthew.Farnworth@walmart.com</li>
                <li>Kendall.Rush@walmart.com</li>
            </ul>
        </div>
        
        <h3>System Status:</h3>
        <ul>
            <li><strong>Test Date:</strong> {date_str}</li>
            <li><strong>Test Time:</strong> {timestamp}</li>
            <li><strong>Mode:</strong> TEST (sent to 3 test recipients)</li>
            <li><strong>Configuration:</strong> Verified and working</li>
            <li><strong>Email System:</strong> Production-ready</li>
        </ul>
        
        <h3>Next Steps:</h3>
        <ol>
            <li>✓ Verify all 3 recipients received this email</li>
            <li>✓ Check that formatting looks good</li>
            <li>✓ Confirm Walmart branding is correct</li>
            <li>→ Switch to production DC recipients when ready</li>
            <li>→ System will send automatically on PayCycle dates</li>
        </ol>
        
        <div class="footer">
            <p>This is an automated test email from the DC Store Manager Change Detection System (v2.0).</p>
            <p>Sent at: {timestamp}</p>
            <p>System: Ready for Production Deployment</p>
        </div>
    </div>
</body>
</html>"""

email_subject = "✅ TEST - Manager Change Detection System (ACTUAL SEND)"

# ============================================================================
# METHOD 1: Try Outlook COM (pywin32)
# ============================================================================
print("[ATTEMPTING] Method 1: Outlook COM automation...")

try:
    import win32com.client
    print("  [FOUND] win32com.client available\n")
    
    print("[SENDING] Via Outlook COM...")
    outlook = win32com.client.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)  # 0 = olMailItem
    
    mail.To = '; '.join(test_recipients)
    mail.Subject = email_subject
    mail.HTMLBody = email_body
    mail.Send()
    
    print(f"  ✅ [SUCCESS] Email sent via Outlook!")
    print(f"     To: {', '.join(test_recipients)}\n")
    
    sys.exit(0)
    
except ImportError:
    print("  ❌ [FAILED] win32com.client not installed")
    print("     (pywin32 not in environment)\n")
    
except Exception as e:
    print(f"  ❌ [FAILED] Outlook COM error: {e}\n")

# ============================================================================
# METHOD 2: Try SMTP
# ============================================================================
print("[ATTEMPTING] Method 2: Direct SMTP...")

try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Try common Walmart SMTP servers
    smtp_servers = [
        ("relay.walmart.com", 25),
        ("mail.walmart.com", 25),
        ("smtp.office365.com", 587),
        ("localhost", 25),
    ]
    
    success = False
    for smtp_host, smtp_port in smtp_servers:
        try:
            print(f"  [TRYING] {smtp_host}:{smtp_port}...", end=" ")
            
            if smtp_port == 587:
                server = smtplib.SMTP(smtp_host, smtp_port, timeout=5)
                server.starttls()
            else:
                server = smtplib.SMTP(smtp_host, smtp_port, timeout=5)
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = email_subject
            msg['From'] = email_config.SEND_FROM_EMAIL
            msg['To'] = ', '.join(test_recipients)
            
            part = MIMEText(email_body, 'html')
            msg.attach(part)
            
            server.sendmail(email_config.SEND_FROM_EMAIL, test_recipients, msg.as_string())
            server.quit()
            
            print("✅ [SUCCESS]")
            print(f"\n✅ [SUCCESS] Email sent via SMTP ({smtp_host})!")
            print(f"   To: {', '.join(test_recipients)}\n")
            
            success = True
            sys.exit(0)
            
        except (smtplib.SMTPException, ConnectionRefusedError, TimeoutError) as e:
            print(f"✗")
            continue
    
    if not success:
        print("  ❌ [FAILED] No SMTP server available\n")
        
except Exception as e:
    print(f"  ❌ [FAILED] SMTP error: {e}\n")

# ============================================================================
# METHOD 3: Queue for Code Puppy msgraph agent
# ============================================================================
print("[ATTEMPTING] Method 3: Queue for Code Puppy msgraph agent...")

try:
    # Save backup email
    emails_dir = Path("emails_sent")
    emails_dir.mkdir(exist_ok=True)
    
    timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
    email_file = emails_dir / f"TEST_EMAIL_ACTUAL_SEND_{timestamp_file}.html"
    
    with open(email_file, 'w', encoding='utf-8') as f:
        f.write(f"<!-- To: {', '.join(test_recipients)} -->\n")
        f.write(f"<!-- Subject: {email_subject} -->\n")
        f.write(f"<!-- Sent: {timestamp} -->\n\n")
        f.write(email_body)
    
    # Queue in email_send_queue
    queue_file = Path("email_send_queue.txt")
    with open(queue_file, 'a', encoding='utf-8') as f:
        f.write(f"{email_file}|{', '.join(test_recipients)}|{email_subject}|\n")
    
    print(f"  [QUEUED] Email saved and queued for Code Puppy to send")
    print(f"     File: {email_file}")
    print(f"     Recipients: {', '.join(test_recipients)}\n")
    print("  ⏳ [INFO] Code Puppy will send this when available\n")
    
    sys.exit(0)
    
except Exception as e:
    print(f"  ❌ [FAILED] Could not queue: {e}\n")

# ============================================================================
# FALLBACK: Just generate HTML
# ============================================================================
print("[FALLBACK] Generating HTML backup only...")

emails_dir = Path("emails_sent")
emails_dir.mkdir(exist_ok=True)

timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
email_file = emails_dir / f"TEST_EMAIL_FALLBACK_{timestamp_file}.html"

with open(email_file, 'w', encoding='utf-8') as f:
    f.write(f"<!-- To: {', '.join(test_recipients)} -->\n")
    f.write(f"<!-- Subject: {email_subject} -->\n\n")
    f.write(email_body)

print(f"\n  ⚠️  [FALLBACK] Email could not be sent automatically")
print(f"      HTML file generated: {email_file}")
print(f"      Recipients: {', '.join(test_recipients)}\n")
print("\n  📧 Manual Send Options:")
print(f"      1. Open the HTML file and send manually from Outlook")
print(f"      2. Install pywin32: pip install pywin32")
print(f"      3. Configure SMTP settings")
print(f"      4. Use Code Puppy msgraph agent\n")
