# DC Manager Change Detection System - Email Standards

**Last Updated:** April 17, 2026 (Production Launch)  
**Status:** OPERATIONAL - SMTP Gateway Method

---

## Email Delivery Method

### Standard: Walmart Internal SMTP Gateway
- **Server:** `smtp-gw1.homeoffice.wal-mart.com`
- **Port:** `25` (no authentication required - internal network only)
- **Method:** Python `smtplib` with MIME multipart
- **Reliability:** Proven daily in TDA, VET, and Audio systems

**Why SMTP:**
- ✅ No Outlook COM dependency
- ✅ No "Server execution failed" errors
- ✅ Works whether Outlook is running or not
- ✅ Consistent with proven Walmart email infrastructure
- ✅ Scales reliably across all PayCycles

### Previous Approach (Sunset)
- ❌ Outlook COM automation (`win32com.client.Dispatch`)
- ❌ Required `pythoncom.CoInitialize()` and `CoUninitialize()`
- ❌ Failed with `Server execution failed (-2146959355)` errors
- ❌ Unreliable SYSTEM context in Task Scheduler

---

## Implementation

### File: `email_helper.py`
**Method:** `send_email_via_outlook()` (name preserved for backward compatibility)

```python
def send_email_via_outlook(self, to: List[str], subject: str, body_html: str, 
                           from_email: str = None, bcc: List[str] = None) -> bool:
    """Send email via Walmart internal SMTP gateway"""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
    SMTP_PORT = 25
    SENDER = from_email or "supplychainops@email.wal-mart.com"
    
    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER
    msg['To'] = '; '.join(to)
    if bcc:
        msg['Bcc'] = '; '.join(bcc)
    msg['Subject'] = subject
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))
    
    recipients = to + (bcc if bcc else [])
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
        server.sendmail(SENDER, recipients, msg.as_string())
    return True
```

---

## System Consistency

All manager change email systems use identical SMTP method:

| System | Script | Method | Status |
|--------|--------|--------|--------|
| **DC Change Emails** | `send_pc06_production_email.py` | SMTP Gateway | ✅ Active |
| **TDA Insights** | `send_weekly_report.py` | SMTP Gateway | ✅ Daily |
| **VET Dashboard** | `send_vet_report.py` | SMTP Gateway | ✅ Weekly |
| **Audio Alerts** | `auto_generate_weekly_audio.py` | SMTP Gateway | ✅ Daily |

---

## Email Sending Flow

1. **Detection:** System identifies manager changes from backend data
2. **Targeting:** Smart DC routing via `group_changes_by_dc()` - only affected DCs receive emails
3. **Content:** HTML email generated with greeting line and manager details
4. **Recipients:**
   - **TO:** DC GMs and AGMs of affected distribution centers
   - **BCC:** Internal team for monitoring (Kristine Torres, Matthew Farnworth, Kendall Rush)
5. **Delivery:** SMTP gateway sends to Walmart distribution list addresses (e.g., `6018GM@email.wal-mart.com`)
6. **Tracking:** `paycycle_tracking.json` logs actual send time and BCC recipient count

---

## PayCycle Schedule (FY27)

- **PC-06:** ✅ Completed April 17, 2026 @ 08:43 (Manual execution due to Task Scheduler issue)
- **PC-07 through PC-26:** Scheduled for every other Thursday, May 1 - January 22, 2027
- **Task Names:** `DC-EMAIL-PC-XX-FY27 PC XX` format (consistent naming)
- **Execution Time:** 06:00 AM (system will auto-execute via Task Scheduler)
- **Tracking:** All entries logged in `paycycle_tracking.json` with send timestamps

---

## Known Issues & Mitigation

### Issue: Task Scheduler Disappearance
**Pattern:** Tasks disappear after system restart or certain operations
- Occurred 3/24, 4/3, 4/15, 4/17 (5 occurrences)
- Root cause: Unknown - possibly SYSTEM user context, registry permissions, or GPO interference

**Mitigation:**
- Manual backup: `CREATE_ALL_PAYCYCLE_TASKS.ps1` available for emergency recreation
- Post-launch investigation: Analyze SYSTEM task registry and elevation scope
- Monitoring: Implement task existence checks before each PayCycle execution

### Issue: COM Initialization
**Pattern:** Outlook COM dispatch failed with "Server execution failed"
- **Solution:** Switched to SMTP gateway (no COM required)
- All systems now use proven SMTP method

---

## Testing & Validation

### PC-06 Launch Test (April 17, 2026)
```
✅ 8 manager changes detected
✅ 5 affected DCs identified
✅ 10 primary recipients notified (DC leaders)
✅ 3 BCC recipients added (internal team)
✅ Email sent via SMTP at 08:43:32
✅ Tracking file updated
```

### Next Validation Points
- **PC-07 (May 1):** Monitor Task Scheduler auto-execution
- **PC-08-26:** Continuous monitoring for email delivery and task execution
- **Quarterly Review:** Task persistence and email delivery success rate analysis

---

## Configuration Files

- `dc_email_config.py` — System settings (TEST_MODE, BCC recipients)
- `email_helper.py` — Email delivery via SMTP gateway
- `paycycle_tracking.json` — Execution history and timestamps
- `CREATE_ALL_PAYCYCLE_TASKS.ps1` — Emergency task recreation script
- `send_pc06_production_email.py` — Production email sender

---

## Contact & Escalation

**System Owner:** Kendall Rush (kendall.rush@walmart.com)  
**BCC Monitoring:** Kristine Torres, Matthew Farnworth, Kendall Rush  
**Escalation:** Contact Supply Chain Operations for Task Scheduler issues
