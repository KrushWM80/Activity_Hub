# TEST vs PRODUCTION - Critical Distinction

## The Rule (ABSOLUTE)

**Task Scheduler tasks = PRODUCTION ONLY**
- No test tasks ever scheduled
- No TEST_MODE environment variable in tasks
- TEST_MODE defaults to False (production)
- Real DC leadership receives real data

**Manual testing = TEST MODE ONLY**
- Only when developer/user is working at keyboard
- `$env:TEST_MODE='true'` set manually at command line
- Email goes to Kendall.Rush@walmart.com ONLY
- No DC emails ever sent during manual testing

---

## When Execution Happens

### Task Scheduler Execution (May 1, 2026 @ 06:00 AM)
```
Trigger: Scheduled task "DC-EMAIL-PC-07-FY27"
Command: python.exe send_paycycle_production_email_generic.py 7
Environment: TEST_MODE not set
Result: TEST_MODE = False (production mode)
Outcome:
  - Loads REAL snapshots from sdl_scraper.py
  - Compares real manager changes
  - Sends to atcteamsupport@walmart.com
  - BCC: All affected DC leadership
  - DC GMs/AGMs receive real email
```

### Manual Development Execution (During work sessions)
```
Trigger: User at keyboard runs script manually
Command: $env:TEST_MODE='true'; python send_paycycle_production_email_generic.py 7
Environment: TEST_MODE = 'true'
Result: TEST_MODE = True (test mode)
Outcome:
  - Loads synthetic test snapshots
  - Uses fake manager names and stores
  - Sends ONLY to Kendall.Rush@walmart.com
  - No BCC to DC leadership
  - Safe testing in development
```

---

## Code Path

**send_paycycle_production_email_generic.py**
```python
# Line ~38: Get mode from environment
TEST_MODE = os.getenv('TEST_MODE', 'False').lower() == 'true'
#
# If environment variable TEST_MODE not set:
#   → defaults to 'False'
#   → TEST_MODE = False (production)
#
# If environment variable TEST_MODE='true':
#   → TEST_MODE = True (test mode)

if TEST_MODE:
    # DEVELOPMENT: Send only to Kendall
    send_to(['Kendall.Rush@walmart.com'])
else:
    # PRODUCTION: Send to atcteamsupport + BCC DC leadership
    send_to(['atcteamsupport@walmart.com'])
    bcc_to([DC_GMs, DC_AGMs, Team])
```

---

## Task Scheduler Configuration

**File: CREATE_ALL_PAYCYCLE_TASKS.ps1**

```powershell
# CORRECT (Production only):
$action = New-ScheduledTaskAction -Execute $pythonExe `
    -Argument "`"$scriptPath`" $pcNum"

# NOT SET: TEST_MODE environment variable
# RESULT: Defaults to False (production)
```

**Verification:**
```powershell
Get-ScheduledTask -TaskName "DC-EMAIL-PC-07-FY27" | `
  Select-Object -ExpandProperty Actions | `
  Select-Object Execute, Arguments
```

Should show:
- Execute: `python.exe`
- Arguments: `"send_paycycle_production_email_generic.py" 7`
- **No TEST_MODE set** ✓

---

## Safety Mechanisms

### During Manual Testing (TEST_MODE=True)
✅ `[TEST MODE] DC EMAILS DISABLED`  
✅ Only Kendall receives email  
✅ Email clearly marked as test  
✅ Synthetic data used  
✅ Safe to run multiple times  

### During Production (TEST_MODE=False)
✅ `[PRODUCTION MODE] REAL DATA - REAL DC EMAILS`  
✅ Real DC leadership receives email  
✅ Real data from SDL system  
✅ Careful execution required  
✅ Run only at scheduled time  

---

## Red Flags 🚨

DO NOT:
- ❌ Create test tasks in Task Scheduler
- ❌ Set TEST_MODE in scheduled task arguments
- ❌ Run production script without verifying TEST_MODE handling
- ❌ Send test emails to DC distribution lists
- ❌ Schedule manual testing (always manual, interactive only)

DO:
- ✅ Manual testing only with `TEST_MODE='true'`
- ✅ Task Scheduler tasks production-only
- ✅ Verify script output shows correct mode before sending
- ✅ Archive production snapshots and emails
- ✅ Keep test and production paths completely separate

---

## Incident Prevention

**What happened (April 29):**
- Sent test email without explicit TEST_MODE check
- Real DC emails received synthetic data
- Real people received false information

**What prevents it now:**
- TEST_MODE must be explicitly set for manual testing
- Script prints `[PRODUCTION MODE]` warning when TEST_MODE=False
- Script prints `[TEST MODE]` and disables DC emails when TEST_MODE=True
- Task Scheduler never sets TEST_MODE
- Documentation makes distinction crystal clear

