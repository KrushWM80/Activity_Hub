# Email Notifications & Integration

## Overview

While the Job Code Teaming Dashboard doesn't currently implement email in the code, it's designed to support email notifications for:
- **User Registration Approval/Rejection**
- **Request Status Updates** (when admin approves/rejects)
- **Job Code Assignment Confirmations**
- **Admin Alerts** (new requests, pending approvals)

This guide covers the patterns and implementation approach.

---

## 📧 Email Use Cases

### 1. User Registration Approval

**Scenario**: New user registers → Admin approves → Email sent

```
User submits registration form
        ↓
Admin reviews in dashboard
        ↓
Admin clicks "Approve"
        ↓
Email sent: "Your account has been approved! Login at http://..."
```

### 2. Request Status Notifications

**Scenario**: User submits teaming request → Admin approves → Email sent

```
User: "I want to assign Job Code 1234 to Team A"
        ↓
Request stored in data/update_requests.json
        ↓
Admin reviews pending requests
        ↓
Admin clicks "Approve"
        ↓
Email to User: "Your request has been approved! Team A will be updated."
↓
Email to Admin Team: "Request for Job Code 1234 approved and ready for TMS export"
```

### 3. Admin Alerts

**Scenario**: User submits request → Admin receives alert email

```
User submits request
        ↓
New file created/data updated
        ↓
Automated email to admins: "You have 1 new pending request"
```

---

## 🔌 Implementation Patterns

### Pattern 1: SMTP Email Service

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

class EmailService:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_email(self, recipient, subject, html_body, text_body=None):
        """Send email with HTML and plain text fallback"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient
            msg["Date"] = formatdate(localtime=True)
            
            # Plain text fallback
            if text_body:
                msg.attach(MIMEText(text_body, "plain"))
            
            # HTML version
            msg.attach(MIMEText(html_body, "html"))
            
            # Send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient, msg.as_string())
            
            print(f"✓ Email sent to {recipient}")
            return True
        
        except Exception as e:
            print(f"✗ Failed to send email to {recipient}: {e}")
            return False
    
    def send_to_multiple(self, recipients, subject, html_body, text_body=None):
        """Send email to multiple recipients"""
        results = {}
        for recipient in recipients:
            results[recipient] = self.send_email(recipient, subject, html_body, text_body)
        return results

# Initialize email service
email_service = EmailService(
    smtp_server="smtp.gmail.com",  # or your organization's SMTP
    smtp_port=587,
    sender_email="jobcodes-dashboard@example.com",
    sender_password="your_email_password"  # Use environment variable!
)
```

### Pattern 2: Email on Event (FastAPI Integration)

```python
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

# ============================================
# EMAIL TEMPLATES
# ============================================

def email_template_request_approved(username, request_id, job_code, team_name):
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #2c3e50;">✓ Request Approved</h2>
        
        <p>Hi {username},</p>
        
        <p>Your teaming request has been approved!</p>
        
        <div style="background: #ecf0f1; padding: 15px; border-left: 4px solid #27ae60; margin: 20px 0;">
            <strong>Request Details:</strong><br>
            Job Code: {job_code}<br>
            Team: {team_name}<br>
            Request ID: {request_id}<br>
            Approved: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </div>
        
        <p>The change will be processed and reflected in TMS shortly.</p>
        
        <p style="color: #7f8c8d; font-size: 12px;">
            — Job Code Teaming Dashboard<br>
            <a href="http://localhost:8080">Access Dashboard</a>
        </p>
    </body>
    </html>
    """
    
    text = f"""
    Hi {username},
    
    Your teaming request has been approved!
    
    Request Details:
    - Job Code: {job_code}
    - Team: {team_name}
    - Request ID: {request_id}
    - Approved: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    
    The change will be processed and reflected in TMS shortly.
    """
    
    return html, text

def email_template_admin_alert_new_request(request_count):
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #e74c3c;">⚠️ New Pending Requests</h2>
        
        <p>There are <strong>{request_count}</strong> new request(s) awaiting your approval.</p>
        
        <p><a href="http://localhost:8080/dashboard.html#pending-requests" 
              style="background: #3498db; color: white; padding: 10px 20px; 
                     text-decoration: none; border-radius: 4px;">
            Review Requests
        </a></p>
        
        <p style="color: #7f8c8d; font-size: 12px;">
            — Job Code Teaming Dashboard
        </p>
    </body>
    </html>
    """
    
    return html

# ============================================
# API ENDPOINT WITH EMAIL
# ============================================

@app.post("/api/approve-request")
async def approve_request(request_id: str, session: dict):
    """Admin approves a request and sends email notification"""
    
    if session["role"] != "admin":
        raise HTTPException(status_code=403)
    
    # Load request
    requests_file = DATA_DIR / "update_requests.json"
    with open(requests_file) as f:
        requests = json.load(f)
    
    if request_id not in requests:
        raise HTTPException(status_code=404)
    
    request = requests[request_id]
    
    # Update request status
    request["status"] = "approved"
    request["approved_by"] = session["username"]
    request["approved_at"] = datetime.now().isoformat()
    
    with open(requests_file, "w") as f:
        json.dump(requests, f, indent=2)
    
    # Get user email
    users_file = DATA_DIR / "users.json"
    with open(users_file) as f:
        users = json.load(f)
    
    user_email = users.get(request["submitted_by"], {}).get("email", "")
    
    # Send email notification
    if user_email:
        html, text = email_template_request_approved(
            username=request["submitted_by"],
            request_id=request_id,
            job_code=request["job_code"],
            team_name=request["team_name"]
        )
        
        email_service.send_email(
            recipient=user_email,
            subject=f"✓ Your Job Code Request Has Been Approved",
            html_body=html,
            text_body=text
        )
    
    return {
        "success": True,
        "message": "Request approved and email sent",
        "email_sent_to": user_email
    }

@app.post("/api/submit-request")
async def submit_request(job_code: str, team_name: str, session: dict):
    """User submits a request and admins are notified"""
    
    # Create request
    request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_request = {
        "id": request_id,
        "job_code": job_code,
        "team_name": team_name,
        "submitted_by": session["username"],
        "submitted_at": datetime.now().isoformat(),
        "status": "pending"
    }
    
    # Save request
    requests_file = DATA_DIR / "update_requests.json"
    with open(requests_file) as f:
        requests = json.load(f)
    
    requests[request_id] = new_request
    
    with open(requests_file, "w") as f:
        json.dump(requests, f, indent=2)
    
    # Alert admins
    users_file = DATA_DIR / "users.json"
    with open(users_file) as f:
        users = json.load(f)
    
    admin_emails = [
        users[username]["email"] 
        for username in users 
        if users[username]["role"] == "admin" and "email" in users[username]
    ]
    
    pending_count = sum(1 for r in requests.values() if r["status"] == "pending")
    
    if admin_emails:
        html = email_template_admin_alert_new_request(pending_count)
        
        email_service.send_to_multiple(
            recipients=admin_emails,
            subject=f"⚠️ {pending_count} New Request(s) Pending Approval",
            html_body=html
        )
    
    return {
        "success": True,
        "request_id": request_id,
        "message": "Request submitted, admins have been notified"
    }
```

### Pattern 3: Configuration with Environment Variables

```python
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Email Configuration
EMAIL_CONFIG = {
    "enabled": os.getenv("EMAIL_ENABLED", "false").lower() == "true",
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    "sender_email": os.getenv("SENDER_EMAIL", ""),
    "sender_password": os.getenv("SENDER_PASSWORD", ""),
}

# Initialize only if enabled
if EMAIL_CONFIG["enabled"]:
    email_service = EmailService(
        smtp_server=EMAIL_CONFIG["smtp_server"],
        smtp_port=EMAIL_CONFIG["smtp_port"],
        sender_email=EMAIL_CONFIG["sender_email"],
        sender_password=EMAIL_CONFIG["sender_password"]
    )
else:
    email_service = None
    print("[INFO] Email notifications are disabled")

# In endpoints
@app.post("/api/approve-request")
async def approve_request(request_id: str, session: dict):
    # ... approval logic ...
    
    # Send email if enabled
    if email_service:
        # Send email
        pass
    else:
        # Log action instead
        print(f"[LOG] Would send email to {user_email} (email disabled)")
```

**Create .env file:**

```
EMAIL_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your_app_password
```

---

## 📨 Email Services

### Option 1: Gmail

```python
# Requirements: App Password (not regular password)
# https://myaccount.google.com/apppasswords

smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@gmail.com"
sender_password = "xxxx xxxx xxxx xxxx"  # App password from Google
```

### Option 2: Microsoft 365 / Office 365

```python
smtp_server = "smtp.office365.com"
smtp_port = 587
sender_email = "your-email@company.com"
sender_password = "your_password"
```

### Option 3: Your Organization's SMTP

```python
# Ask your IT department for:
# - SMTP Server address
# - SMTP Port (usually 587 or 25)
# - Sender email
# - Credentials (if required)

smtp_server = "mail.company.com"  # Your organization
smtp_port = 587
sender_email = "automation@company.com"
sender_password = "credentials_here"
```

### Option 4: SendGrid / AWS SES / Other Services

```python
# These provide API endpoints instead of SMTP
# More reliable for high-volume email

import requests

class SendGridEmailService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.sendgrid.com/v3/mail/send"
    
    def send_email(self, recipient, subject, html_body, text_body=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "personalizations": [{"to": [{"email": recipient}]}],
            "from": {"email": "noreply@example.com"},
            "subject": subject,
            "content": [
                {"type": "text/html", "value": html_body}
            ]
        }
        
        response = requests.post(self.base_url, json=data, headers=headers)
        return response.status_code == 202
```

---

## 🔒 Security Best Practices

1. **Never hardcode credentials**
   ```python
   # ❌ BAD
   sender_password = "MyP@ssw0rd123"
   
   # ✅ GOOD
   sender_password = os.getenv("SENDER_PASSWORD")
   ```

2. **Use App Passwords for Gmail/Office 365**
   - Not your regular account password
   - More secure and can be revoked independently

3. **Validate email addresses**
   ```python
   import re
   
   def is_valid_email(email):
       pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
       return re.match(pattern, email) is not None
   ```

4. **Rate limit emails**
   ```python
   from datetime import datetime, timedelta
   
   last_email_sent = {}
   
   def can_send_email(recipient):
       """Only send max 5 emails per hour per recipient"""
       now = datetime.now()
       
       if recipient not in last_email_sent:
           last_email_sent[recipient] = []
       
       # Remove old timestamps
       last_email_sent[recipient] = [
           ts for ts in last_email_sent[recipient] 
           if now - ts < timedelta(hours=1)
       ]
       
       if len(last_email_sent[recipient]) >= 5:
           return False
       
       last_email_sent[recipient].append(now)
       return True
   ```

5. **Log email activities**
   ```python
   import logging
   
   logger = logging.getLogger(__name__)
   
   def send_email_with_logging(recipient, subject, html_body):
       try:
           result = email_service.send_email(recipient, subject, html_body)
           
           if result:
               logger.info(f"Email sent: {subject} → {recipient}")
           else:
               logger.warning(f"Email failed: {subject} → {recipient}")
           
           return result
       except Exception as e:
           logger.error(f"Email error: {e}", exc_info=True)
           return False
   ```

---

## 🎓 Key Learnings

✅ **Email templates** should have HTML + plain text versions  
✅ **Keep emails simple** - Clear subject, concise content, action links  
✅ **Event-driven approach** - Send emails when important events occur  
✅ **Configuration is key** - Use environment variables, not hardcoded values  
✅ **Error handling** - Email failures shouldn't break your application  
✅ **Testing first** - Start with test account before production  

---

## 📚 Related Documentation

- See: [USER_AUTHENTICATION.md](./USER_AUTHENTICATION.md) - User data structure with email fields
- See: [LOCAL_HOSTING_SETUP.md](./LOCAL_HOSTING_SETUP.md) - FastAPI integration
- See: [WORKFLOW_PATTERNS.md](./WORKFLOW_PATTERNS.md) - Where email fits in workflows

---

## 🚀 Next Steps

1. **Choose your SMTP service** (Gmail, Office 365, your org's SMTP)
2. **Add email fields to user registration** form
3. **Implement one email event** (e.g., "request approved")
4. **Test thoroughly** - Use test email address first
5. **Monitor** - Check email service logs for issues
