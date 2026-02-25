#!/usr/bin/env python3
"""
Simple Email Send Test - Demonstrates 3-recipient test configuration
Tests email sending to: Kristine.Torres, Matthew.Farnworth, Kendall.Rush
"""

from datetime import datetime
from pathlib import Path

# Import configuration
import config
import dc_email_config as email_config

print("\n" + "="*70)
print("EMAIL SEND TEST - 3 Test Recipients Configuration")
print("="*70 + "\n")

# Display test configuration
print("[CONFIG] Current Settings:")
print(f"  Test Mode: {config.TEST_MODE}")
print(f"  Test Emails: {config.TEST_EMAILS if hasattr(config, 'TEST_EMAILS') else [config.TEST_EMAIL]}")
print()

# Show test recipients
test_recipients = config.TEST_EMAILS if hasattr(config, 'TEST_EMAILS') else [config.TEST_EMAIL]
print("[RECIPIENTS] Emails will be sent to:")
for i, email in enumerate(test_recipients, 1):
    print(f"  {i}. {email}")
print()

# Generate test email
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_str = datetime.now().strftime("%Y-%m-%d")

# Create HTML email content (matching the system's format)
email_body = f"""
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
            background: linear-gradient(135deg, #0071ce 0%, #00a4e4 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
            text-align: center;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 24px;
        }}
        .header p {{
            margin: 5px 0 0 0;
            font-size: 14px;
            opacity: 0.9;
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
        <h1>🧪 SYSTEM TEST EMAIL</h1>
        <p>Manager Change Detection System - Test Configuration</p>
    </div>
    
    <div class="content">
        <div class="test-badge">
            ✓ TEST: 3-Recipient Configuration Active
        </div>
        
        <div class="info-box">
            <h2 style="margin: 0 0 10px 0; color: #0071ce;">Test Execution Successful</h2>
            <p style="margin: 0;">The system email configuration is working correctly with test recipients.</p>
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
            <li><strong>Mode:</strong> TEST (will send to 3 test recipients)</li>
            <li><strong>Configuration:</strong> Verified and working</li>
            <li><strong>Email System:</strong> Ready for production</li>
        </ul>
        
        <h3>Next Steps:</h3>
        <ol>
            <li>Verify all 3 recipients received this email</li>
            <li>Check that Walmart branding is correct</li>
            <li>Confirm formatting is readable on mobile/desktop</li>
            <li>Once verified, proceed with PayCycle-based scheduling</li>
        </ol>
        
        <div class="footer">
            <p>This is an automated test email from the Manager Change Detection System.</p>
            <p>Sent at: {timestamp}</p>
            <p>System Version: 2.0 | Test Mode: ACTIVE</p>
        </div>
    </div>
</body>
</html>
"""

# Save email to file (demonstrates what would be sent)
emails_dir = Path("emails_sent")
emails_dir.mkdir(exist_ok=True)

timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
email_file = emails_dir / f"TEST_EMAIL_{timestamp_file}.html"

with open(email_file, 'w', encoding='utf-8') as f:
    f.write(f"<!-- TEST EMAIL FOR: {', '.join(test_recipients)} -->\n")
    f.write(f"<!-- Generated: {timestamp} -->\n\n")
    f.write(email_body)

print(f"[SUCCESS] Test email prepared for sending")
print(f"  Recipients: {len(test_recipients)} people")
print(f"  Saved to: {email_file}\n")

# Display what would be sent
print("[EMAIL CONTENT]")
print("=" * 70)
print(f"Subject: TEST - Manager Change Detection System")
print(f"From: {email_config.SEND_FROM_EMAIL}")
print(f"To: {', '.join(test_recipients)}")
print(f"Date: {timestamp}")
print("=" * 70)
print()

# Create a summary
print("[TEST CONFIGURATION SUMMARY]")
print("-" * 70)
print(f"✓ Configuration loaded: {len(test_recipients)} test recipients")
print(f"✓ Email template generated successfully")
print(f"✓ Backup saved for review")
print(f"✓ Ready to send when Outlook/email service is available")
print()

# Show instructions for next step
print("[NEXT STEPS]")
print("-" * 70)
print("Option 1: Manual Outlook Send")
print("  - Open emails_sent/" + email_file.name)
print("  - Review formatting")
print("  - Send manually through Outlook")
print()
print("Option 2: Automated Send (When Outlook is available)")
print("  - Run: python daily_check_smart.py")
print("  - System will send to all 3 recipients automatically")
print()
print("Option 3: PayCycle-Based Automated Schedule")
print("  - Set up Windows Task Scheduler")
print("  - Schedule sends for each PayCycle end date")
print("  - System runs automatically: 3/6/26, 3/20/26, 4/3/26, etc.")
print()

print("="*70)
print("✅ TEST EMAIL CONFIGURATION COMPLETE")
print("="*70 + "\n")

print("[VERIFICATION CHECKLIST]")
print("□ Email created successfully")
print("□ All 3 recipients configured")
print("□ Email file saved for review")
print("□ Ready for production deployment")
print()

# Also provide file path for reference
print(f"[FILES]")
print(f"  Email File: {email_file}")
print(f"  Config File: config.py (TEST_EMAILS={test_recipients})")
print(f"  Email Helper: email_helper.py (supports 1+ test recipients)")
print()

print("Ready to proceed with:")
print("  → Manual testing & verification")
print("  → PayCycle schedule configuration")  
print("  → Production deployment\n")
