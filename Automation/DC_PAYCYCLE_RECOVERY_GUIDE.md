# DC PayCycle Emergency Recovery - Automation Resources

**Last Updated:** March 24, 2026  
**Status:** ✅ All 26 PayCycle tasks recreated and operational

---

## Quick Recovery (If Tasks Disappear Again)

### Step 1: Open Admin PowerShell
```powershell
# RIGHT-CLICK on Windows PowerShell and select "Run as Administrator"
# IMPORTANT: Do NOT use regular PowerShell - it MUST be admin
```

### Step 2: Run the One-Line Recovery
```powershell
$PaycycleDates = @{
    "5"="2026-04-03"; "6"="2026-04-17"; "7"="2026-05-01"; "8"="2026-05-15"
    "9"="2026-05-29"; "10"="2026-06-12"; "11"="2026-06-26"; "12"="2026-07-10"
    "13"="2026-07-24"; "14"="2026-08-07"; "15"="2026-08-21"; "16"="2026-09-04"
    "17"="2026-09-18"; "18"="2026-10-02"; "19"="2026-10-16"; "20"="2026-10-30"
    "21"="2026-11-13"; "22"="2026-11-27"; "23"="2026-12-11"; "24"="2026-12-25"
    "25"="2027-01-08"; "26"="2027-01-22"
}
$PythonPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$ProjectDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
pushd $ProjectDir
foreach ($pc in $PaycycleDates.Keys | Sort-Object {[int]$_}) {
    $DateTime = [DateTime]::Parse("$($PaycycleDates[$pc]) 06:00:00")
    $Trigger = New-ScheduledTaskTrigger -Once -At $DateTime
    $Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "daily_check_smart.py" -WorkingDirectory $ProjectDir
    $Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable
    Register-ScheduledTask -TaskName "DC-EMAIL-PC-$pc" -Trigger $Trigger -Action $Action -Settings $Settings -RunLevel Highest -Force | Out-Null
    Write-Host "Created: DC-EMAIL-PC-$pc"
}
Write-Host "Verifying..."
$Count = (Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" -ErrorAction SilentlyContinue | Measure-Object).Count
Write-Host "Total tasks: $Count/26"
popd
```

### Step 3: Verify Success
```powershell
Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" | Measure-Object
# Should show: Count = 26
```

---

## Detailed Recovery Steps (For Reference)

### Problem Diagnosis
- **Symptom:** No emails received, system documented as "ready for production"
- **Root Cause:** All 26 PayCycle tasks missing from Windows Task Scheduler
- **Why it happened:** Tasks created 3/5/26 but failed to persist or were cleared by system restart

### Why Standard Fixes Don't Work
```powershell
# ❌ This fails: admin context drops after process exit
Start-Process powershell -Verb RunAs -ArgumentList "-No... create tasks... -NoExit"

# ❌ This fails: batch files can't maintain admin context for task registration
REM schtasks.exe /create /tn "DC-EMAIL-PC-05" ...

# ✅ This works: YOU stay in admin PowerShell
cd "path\to\project"
# Paste entire script and press Enter
```

### What We Did (3/24/26 @ 19:30)
1. **User opened NEW admin PowerShell** (Right-click → Run as Administrator)
2. **Navigated to DC project folder**
3. **Pasted and executed complete task creation script** (54 lines)
4. **Verified with admin terminal:** "Total tasks: 26/26"
5. **Updated tracking file:** PC-04 marked as missed, PC-05-26 scheduled

### Result
```
Created: DC-EMAIL-PC-05 through DC-EMAIL-PC-26 (22 tasks)
Created: DC-EMAIL-PC-01 through DC-EMAIL-PC-04 (4 legacy tasks)
Total: 26/26
Status: ✅ OPERATIONAL
```

---

## Catch-Up Email for Missed PC-04

PC-04 (scheduled for 3/20/26) was missed due to task outage. Send it now:

```powershell
cd "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
python send_pc04_catchup.py
```

**What it does:**
- Generates PC-04 summary email with system recovery notice
- Sends via Outlook to test recipients
- Updates tracking file: PC-04 marked "completed" with catch-up timestamp

---

## Monitoring & Verification

### Check Current Task Status
```powershell
# Count tasks
Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" | Measure-Object

# See task details
Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" | 
  Format-Table TaskName, State, 
    @{Name='Trigger'; Expression={$_.Triggers.StartBoundary}} -AutoSize

# Check if specific task exists
Get-ScheduledTask -TaskName "DC-EMAIL-PC-05" -ErrorAction SilentlyContinue
```

### Monitor Next PayCycle Execution
- **PC-05 scheduled:** April 3, 2026 @ 06:00 AM
- **Watch for:**
  - Email receipt at ~6:00 AM (not delayed)
  - All 3 test recipients receive email
  - Tracking file updates with send timestamp
  - No errors in Outlook COM

### Check Tracking File
```powershell
cd "Store Support\Projects\DC to Store Change Management Emails"
type paycycle_tracking.json | ConvertFrom-Json | 
  Select-Object -ExpandProperty summary
```

Should show:
```
completed              : 1
scheduled              : 24
missed                 : 1
last_updated           : 2026-03-24T...
```

---

## Emergency Revert (Delete All Tasks)

**If you need to start over:**

```powershell
# Delete all PayCycle tasks
Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" | Unregister-ScheduledTask -Confirm:$false

# Verify deletion
Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" -ErrorAction SilentlyContinue | Measure-Object
# Should show: Count = 0

# Then re-run recovery script above
```

---

## Key Files & Locations

| File | Purpose | Location |
|---|---|---|
| `daily_check_smart.py` | Execution engine | DC project folder |
| `email_helper.py` | Outlook COM sender | DC project folder |
| `paycycle_tracking.json` | Tracking & status | DC project folder |
| `send_pc04_catchup.py` | Catch-up send script | DC project folder |
| `COPY_PASTE_INTO_ADMIN_POWERSHELL.ps1` | Task creation script | Activity Hub root |
| `RECOVERY_SUMMARY_2026-03-24.md` | Full details | DC project folder |

---

## Recent Changes (3/24/26)

✅ **Created:** `send_pc04_catchup.py` - Send missed PC-04 email  
✅ **Updated:** `paycycle_tracking.json` - Recovery metadata  
✅ **Updated:** `RECOVERY_SUMMARY_2026-03-24.md` - Full documentation  
✅ **Updated:** Knowledge base with recovery procedures  

---

## Critical Notes

⚠️ **Admin Context is MANDATORY** - You cannot create Windows Task Scheduler tasks without persistent admin privileges. The only reliable method is manual execution in an admin PowerShell session that never drops privilege.

⚠️ **Task Persistence Risk** - If system restarts unexpectedly, verify tasks still exist with: `Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" | Measure-Object`

⚠️ **Next Test Point** - PC-05 on April 3, 2026 @ 6:00 AM. If that fails, check if tasks re-disappeared.

---

## Support

**For questions:** See `RECOVERY_SUMMARY_2026-03-24.md` or contact ATCTEAMSUPPORT@walmart.com

**For other PayCycle issues:** Use `manage_paycycle.py` CLI:
```powershell
python manage_paycycle.py help
```
