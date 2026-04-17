# Email System Standards - Walmart Activity Hub

**Document:** Core Email Delivery Architecture  
**Created:** April 17, 2026  
**Scope:** All automated email systems (TDA, VET, Audio, DC Manager Changes)

---

## Executive Summary

All Walmart automation systems use **Walmart Internal SMTP Gateway** for email delivery. This approach has proven reliable across daily/weekly execution patterns since early 2026.

**Key Principle:** No Outlook COM dependency. Direct SMTP to `smtp-gw1.homeoffice.wal-mart.com:25`

---

## System Overview

### Active Email Systems

| System | Schedule | Recipients | Status |
|--------|----------|-----------|--------|
| **DC Manager Changes** | Every 2 weeks (21 cycles) | DC Leadership (GM/AGM) | ✅ Active (4/17/26+) |
| **TDA Insights Report** | Weekly (Thursdays 11:00 AM) | Retail Leadership | ✅ Daily operation |
| **VET Executive Report** | Weekly | V.E.T. Stakeholders | ✅ Weekly operation |
| **Audio Alert** | Daily (EOD check) | On-Call Team | ✅ Daily operation |

All systems confirmed working via SMTP Gateway.

---

## SMTP Gateway Configuration

**Server:** `smtp-gw1.homeoffice.wal-mart.com`  
**Port:** `25`  
**Protocol:** SMTP (no authentication required)  
**Network:** Walmart internal only  
**Timeout:** 30 seconds (recommended)  
**Scope:** All internal email distribution lists

---

## Standard Implementation

### Python Pattern (Recommended)

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_smtp(to_list, subject, html_body, from_addr=None, bcc_list=None):
    """Send email via Walmart SMTP gateway"""
    
    SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
    SMTP_PORT = 25
    SENDER = from_addr or "automation@email.wal-mart.com"
    
    # Build MIME message
    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER
    msg['To'] = '; '.join(to_list)
    if bcc_list:
        msg['Bcc'] = '; '.join(bcc_list)
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    # Send via SMTP
    recipients = to_list + (bcc_list if bcc_list else [])
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
        server.sendmail(SENDER, recipients, msg.as_string())
    
    return True
```

### Example Usage

```python
recipients = ['6018GM@email.wal-mart.com', '6018AGM@email.wal-mart.com']
bcc_team = ['kristine.torres@walmart.com', 'matthew.farnworth@walmart.com']

html = """
<html>
    <body>
        <h2>Manager Change Report</h2>
        <p>Details here...</p>
    </body>
</html>
"""

send_email_smtp(
    to_list=recipients,
    subject="Manager Change Report - PayCycle 06",
    html_body=html,
    from_addr="supplychainops@email.wal-mart.com",
    bcc_list=bcc_team
)
```

---

## Why SMTP Gateway (Not Outlook COM)

### Advantages
✅ No dependencies on Outlook application  
✅ No COM initialization required  
✅ Works in SYSTEM context (Task Scheduler)  
✅ Reliable across restarts  
✅ Scales to any number of recipients  
✅ No "Server execution failed" errors  
✅ Tested and proven in production  

### Disadvantages of Outlook COM (Deprecated)
❌ Requires Outlook desktop application  
❌ COM initialization conflicts  
❌ Fails in SYSTEM user context  
❌ Unreliable in automated scheduling  
❌ "Server execution failed (-2146959355)" errors  
❌ Not scalable for large recipient lists  

---

## Integration Points

### Walmart Email Infrastructure
- **Distribution Lists:** `[role]@email.wal-mart.com` (e.g., `6018GM@email.wal-mart.com`)
- **Service Accounts:** `[service]@email.wal-mart.com`
- **Team Mailboxes:** Shared account format (e.g., `supplychainops@email.wal-mart.com`)

### Email Recipients Pattern
**TO:** Target recipients (public distribution lists)  
**BCC:** Internal monitoring team (not visible to TO recipients)  
**FROM:** Service account with Walmart email domain  

---

## Operational Implementation

### DC Manager Change System (Reference Implementation)

**File:** `send_pc06_production_email.py`

1. Detects manager changes from backend data
2. Identifies affected distribution centers
3. Generates HTML email content
4. Sends via SMTP to DC leadership TO list
5. Adds internal team to BCC for monitoring
6. Logs execution to tracking file

**Result:** Reliable production execution since 4/17/26

### Task Scheduling Pattern

```powershell
# Schedule email script to run every 2 weeks at 6:00 AM
$trigger = New-ScheduledTaskTrigger -At "2026-05-01 06:00:00" -Once
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "send_script.py"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "EMAIL-JOB-NAME" -Trigger $trigger -Action $action `
    -Settings $settings -RunLevel Highest -User SYSTEM -Force
```

Email execution succeeds because no Outlook COM dependency.

---

## Testing Guidelines

### New System Validation

1. **SMTP Connection Test**
   ```python
   import smtplib
   with smtplib.SMTP("smtp-gw1.homeoffice.wal-mart.com", 25, timeout=30) as server:
       print("✓ SMTP gateway accessible")
   ```

2. **Recipient List Validation**
   - Confirm distribution lists exist: `[role]@email.wal-mart.com`
   - Test with at least one known user first
   - Verify BCC recipients receive copies

3. **HTML Content Testing**
   - Send test email with HTML body
   - Verify formatting in recipient mailbox
   - Check for encoding issues

4. **Task Scheduler Integration**
   - Create test task with future trigger time
   - Monitor system event log for execution
   - Verify email received at expected time

---

## Troubleshooting

### SMTP Connection Failed
- **Cause:** Network isolation or firewall
- **Check:** Internal network connectivity to `smtp-gw1.homeoffice.wal-mart.com:25`
- **Solution:** Verify network access, check firewall rules

### Recipients Not Receiving Email
- **Cause:** Distribution list doesn't exist or SMTP rejection
- **Check:** Verify email format matches `[role]@email.wal-mart.com`
- **Solution:** Test with direct user address first

### BCC Recipients Not Receiving
- **Cause:** Email header encoding or mail server filtering
- **Check:** Verify BCC addresses are properly formatted
- **Solution:** Add `-Bcc` header correctly in MIME message

### Task Scheduler Execution Issues
- **Cause:** Task disappeared or SYSTEM context mismatch
- **Check:** Run `Get-ScheduledTask -TaskName "task-name"`
- **Solution:** If missing, recreate using PowerShell script

---

## Knowledge Base Links

- [DC Manager Change Detection System](Store%20Support/Projects/DC%20to%20Store%20Change%20Management%20Emails/EMAIL_SYSTEM_STANDARDS.md)
- [Production Launch Notes](Store%20Support/Projects/DC%20to%20Store%20Change%20Management%20Emails/PRODUCTION_LAUNCH_NOTES.md)
- [Email Helper Implementation](Store%20Support/Projects/DC%20to%20Store%20Change%20Management%20Emails/email_helper.py)

---

## Version History

| Date | Version | Change |
|------|---------|--------|
| 2026-04-17 | 1.0 | Initial documentation - SMTP Gateway standard |
| 2026-04-17 | 1.1 | Added DC Manager Change implementation reference |

---

## Contact

**Email System Owner:** Kendall Rush (kendall.rush@walmart.com)  
**Escalation:** Supply Chain Operations  
**Documentation:** See linked system-specific guides above
