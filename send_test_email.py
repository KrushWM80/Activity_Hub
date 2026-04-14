#!/usr/bin/env python3
"""
Test Email Script - Activity Hub Projects Dashboard
Sends a test email to verify SMTP configuration is working
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email configuration
SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
SMTP_PORT = 25
SENDER_EMAIL = "activity-hub@walmart.com"
RECIPIENT_EMAIL = "kendall.rush@walmart.com"

# Create message
msg = MIMEMultipart("alternative")
msg["Subject"] = "Test Email - Impact Platform Projects Dashboard"
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL

# HTML body
html = f"""
<html>
  <body style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: #0071CE;">Impact Platform - Test Email</h2>
    
    <p>Hi Kendall,</p>
    
    <p>This is a test email from the Activity Hub Projects Dashboard.</p>
    
    <h3>Test Information:</h3>
    <ul>
      <li><strong>Sent At:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
      <li><strong>From:</strong> {SENDER_EMAIL}</li>
      <li><strong>To:</strong> {RECIPIENT_EMAIL}</li>
      <li><strong>Server:</strong> {SMTP_SERVER}:{SMTP_PORT}</li>
    </ul>
    
    <p>If you received this email successfully, the email system is working correctly!</p>
    
    <hr/>
    <p style="font-size: 12px; color: #666;">Activity Hub Projects Dashboard | Visit: http://weus42608431466:8088/activity-hub/projects</p>
  </body>
</html>
"""

part = MIMEText(html, "html")
msg.attach(part)

try:
    # Connect to SMTP server
    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
    
    # Send email
    print(f"Sending email to {RECIPIENT_EMAIL}...")
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    server.quit()
    
    print("✅ Email sent successfully!")
    print(f"   From: {SENDER_EMAIL}")
    print(f"   To: {RECIPIENT_EMAIL}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
except Exception as e:
    print(f"❌ Error sending email: {str(e)}")
    print(f"   Error Type: {type(e).__name__}")
