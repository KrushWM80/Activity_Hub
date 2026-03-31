"""
Digital Egg Hunt - Winner Email Notifier
Sends email notification to Kendall Rush when a winner is found
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_winner_notification(winner_name):
    """
    Send email notification to Kendall Rush about the egg hunt winner
    
    Args:
        winner_name (str): Full name of the winner
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    KENDALL_EMAIL = "kendall.rush@walmart.com"
    
    # Email configuration (Office 365)
    SMTP_SERVER = "smtp.office365.com"
    SMTP_PORT = 587
    
    # Get credentials from environment variables
    # These should be set before running
    sender_email = os.getenv('OUTLOOK_EMAIL', 'activity_team@walmart.com')
    sender_password = os.getenv('OUTLOOK_PASSWORD')
    
    if not sender_password:
        print("⚠️  WARNING: OUTLOOK_PASSWORD environment variable not set")
        print("   Email will not be sent until credentials are configured")
        print("   To set up:")
        print("   $env:OUTLOOK_EMAIL = 'your_email@walmart.com'")
        print("   $env:OUTLOOK_PASSWORD = 'your_password'")
        return False
    
    try:
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🥚 Digital Egg Hunt Winner - {winner_name}! 🥚"
        msg['From'] = sender_email
        msg['To'] = KENDALL_EMAIL
        msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        
        # Plain text version
        text = f"""\
Digital Egg Hunt Winner Announcement

Congratulations to {winner_name}!

{winner_name} has successfully found all 50 eggs and won the Digital Egg Hunt!

Please coordinate prize collection with the Activity Team.

The winner can come by the Activity Team office to collect their prize.

Date/Time: {datetime.now().strftime('%a, %B %d, %Y at %I:%M %p')}

---
Digital Egg Hunt System
"""
        
        # HTML version
        html = f"""\
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="background-color: white; border-radius: 10px; padding: 30px; max-width: 600px; margin: 0 auto; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
              <h1 style="color: #667eea; text-align: center;">🥚 Digital Egg Hunt Winner! 🥚</h1>
              
              <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
                <h2 style="margin: 0; font-size: 28px;">Congratulations!</h2>
                <p style="font-size: 20px; margin: 10px 0;"><strong>{winner_name}</strong></p>
                <p style="margin: 10px 0; font-size: 16px;">has won the Digital Egg Hunt! 🏆</p>
              </div>
              
              <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p style="margin: 10px 0;"><strong>Achievement:</strong> Found all 50 eggs</p>
                <p style="margin: 10px 0;"><strong>Time:</strong> {datetime.now().strftime('%a, %B %d, %Y at %I:%M %p')}</p>
              </div>
              
              <p style="font-size: 16px; margin: 20px 0;">
                Please coordinate with {winner_name} to collect the prize from the Activity Team office.
              </p>
              
              <div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2196F3;">
                <p style="margin: 0; color: #1565c0;"><strong>Next Steps:</strong></p>
                <ul style="margin: 10px 0; padding-left: 20px;">
                  <li>Contact {winner_name} to arrange prize pickup</li>
                  <li>Prepare winner announcement for all participants</li>
                  <li>Update activity hub with winner information</li>
                </ul>
              </div>
              
              <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
              
              <p style="text-align: center; color: #999; font-size: 12px;">
                This is an automated message from the Digital Egg Hunt System
              </p>
            </div>
          </body>
        </html>
        """
        
        # Attach both versions
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        
        # Send email
        print(f"📧 Sending winner notification email...")
        print(f"   To: {KENDALL_EMAIL}")
        print(f"   Subject: Digital Egg Hunt Winner - {winner_name}!")
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"✅ Email sent successfully!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ EMAIL ERROR: Authentication failed")
        print("   Please check your email and password credentials")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ EMAIL ERROR: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        return False

def test_email_configuration():
    """Test email configuration by sending a test email"""
    sender_email = os.getenv('OUTLOOK_EMAIL')
    sender_password = os.getenv('OUTLOOK_PASSWORD')
    
    if not sender_email or not sender_password:
        print("❌ Missing email configuration")
        print("   Set these environment variables:")
        print("   $env:OUTLOOK_EMAIL = 'your_email@walmart.com'")
        print("   $env:OUTLOOK_PASSWORD = 'your_password'")
        return False
    
    print("📧 Testing email configuration...")
    return send_winner_notification("Test Winner")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        winner_name = " ".join(sys.argv[1:])
        send_winner_notification(winner_name)
    else:
        print("🥚 Digital Egg Hunt - Winner Notification System 🥚")
        print("=" * 50)
        print()
        print("Usage:")
        print("  python send_winner_email.py \"Winner First Name\" \"Winner Last Name\"")
        print()
        print("Example:")
        print("  python send_winner_email.py \"John\" \"Smith\"")
        print()
        print("Configuration (set these environment variables):")
        print("  $env:OUTLOOK_EMAIL = 'your_email@walmart.com'")
        print("  $env:OUTLOOK_PASSWORD = 'your_password'")
        print()
        test_email_configuration()
