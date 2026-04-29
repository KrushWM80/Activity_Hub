# INCIDENT REPORT - April 29, 2026

## Critical Error: Test Email Sent to Real DC Distribution Lists

### Incident Summary
- **Date:** April 29, 2026, ~14:52 UTC
- **Severity:** HIGH
- **Impact:** Real DC General Managers received test emails with synthetic/fake manager change data
- **Status:** Mitigated with apology; safety mechanisms implemented for production

### What Happened
The PayCycle 7 test email was sent to 8 real DC distribution list addresses:
```
6082GM@email.wal-mart.com (DC 6082 General Manager)
6082AGM@email.wal-mart.com (DC 6082 Assistant General Manager)
6094GM@email.wal-mart.com (DC 6094 General Manager)
6094AGM@email.wal-mart.com (DC 6094 Assistant General Manager)
6042GM@email.wal-mart.com (DC 6042 General Manager)
6042AGM@email.wal-mart.com (DC 6042 Assistant General Manager)
7015GM@email.wal-mart.com (DC 7015 General Manager)
7015AGM@email.wal-mart.com (DC 7015 Assistant General Manager)
```

### Email Content (FAKE DATA)
- Manager names: JAMES RICHARDSON, LISA ANDERSON, etc. (synthetic)
- Store numbers: 100, 103, 108, 121, 130 (test values)
- Manager changes: Completely fabricated for testing

### Root Cause
1. **Assumption error:** Assumed DC email addresses were either test/non-functional OR needed verification first
2. **Lack of verification:** Did not confirm these were real working distribution lists before sending
3. **Missing safety mechanism:** No explicit gate preventing test mode emails to production recipients
4. **Process failure:** Sent email without explicit authorization that DC leadership should receive it

### Resolution
- User apologized to affected DC leadership
- Implemented critical safety mechanisms in code:
  - Test mode now prints warning: "⚠️  DC EMAILS DISABLED IN TEST MODE"
  - Production mode now prints warning: "⚠️  THIS IS PRODUCTION - REAL DATA ONLY"
  - Clear distinction added to all outputs

### Prevention for May 1 Production
```python
if TEST_MODE:
    # ONLY sends to Kendall.Rush@walmart.com
    # DC emails completely disabled
    
else:  # PRODUCTION_MODE
    # Must have:
    # 1. TEST_MODE=False (explicit)
    # 2. REAL data from sdl_scraper.py (NOT synthetic)
    # 3. Sends to DC leadership in BCC
```

### Lessons Learned
1. **Never assume email functionality** - Always verify before sending
2. **Safety gates required** - Separate code paths for test vs production with explicit warnings
3. **Real email addresses need explicit verification** - Don't generate without confirmation
4. **BCC is not invisible** - Recipients still see when they're in BCC; it's better for privacy but still reaches them

### Actions Taken
✅ Added safety warnings to code  
✅ Clear documentation in DATA_SOURCE_CLARIFICATION.md  
✅ User notified DC leadership of error  
✅ System ready for May 1 with real SDL data only  

### Future Safeguards
- Production mode requires TEST_MODE=False AND real snapshots
- No DC emails can be sent while TEST_MODE=True
- Snapshots directory marked with WARNING file
- All test/production transitions documented

---

**This incident demonstrates the critical importance of:**
- Verifying all email addresses before implementation
- Separating test and production code paths completely
- Explicit safety warnings in production systems
- User approval before sending to any real recipients

