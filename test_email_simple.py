import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sys

try:
    print("Starting email send...")
    SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
    SMTP_PORT = 25
    SENDER_EMAIL = "activity-hub@walmart.com"
    RECIPIENT_EMAIL = "kendall.rush@walmart.com"
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Test Email - Impact Platform Projects Dashboard"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    
    html = f"""<html><body style="font-family: Arial, sans-serif; color: #333;">
<h2 style="color: #0071CE;">Impact Platform - Test Email</h2>
<p>Hi Kendall,</p>
<p>This is a test email from the Activity Hub Projects Dashboard.</p>
<h3>Test Information:</h3>
<ul>
  <li><strong>Sent At:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
  <li><strong>From:</strong> {SENDER_EMAIL}</li>
  <li><strong>To:</strong> {RECIPIENT_EMAIL}</li>
</ul>
<p>✅ Email system is working correctly!</p>
<p style="font-size: 12px; color: #666;">Activity Hub Projects Dashboard</p>
</body></html>"""
    
    part = MIMEText(html, "html")
    msg.attach(part)
    
    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
    print("Connected!")
    
    print(f"Sending to {RECIPIENT_EMAIL}...")
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    server.quit()
    
    print("SUCCESS: Email sent!")
    sys.exit(0)
    
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
