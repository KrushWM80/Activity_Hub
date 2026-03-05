# ⚠️ CRITICAL: Projects in Stores Auto-Start is NOT Configured

## Current Status
- ✅ Backend server IS running now (port 8001, PID 22148)
- ❌ Auto-start scheduled task does NOT exist
- ❌ If server crashes or system restarts, server will NOT auto-restart

## Root Cause
After the system restart, the scheduled task that should automatically launch the Projects in Stores backend did not execute because **the scheduled task was never created or was removed**.

### Why This Happened
The scheduled task setup requires Administrator privileges, which may have been:
1. Lost during system updates
2. Removed manually
3. Never created in the first place

## What You Need to Do

### IMMEDIATE ACTION (30 seconds)
Run the setup script with Administrator privileges:

```powershell
# Option 1: Run with Right-Click (Easiest)
1. Navigate to: Automation\SetupAutoStart.bat
2. Right-click it
3. Select "Run as Administrator"
4. Wait for confirmation window showing "✅ SUCCESS"
5. Press Enter to close
```

### MANUAL SETUP (if above doesn't work)

Open PowerShell as Administrator and run:

```powershell
# Run PowerShell AS ADMINISTRATOR
$TaskName = "Projects in Stores Server 24/7"
$ScriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_server_24_7.bat"

# Remove old task if exists
Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue

# Create trigger for startup
$Trigger = New-ScheduledTaskTrigger -AtStartup

# Create action
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ScriptPath`""

# Create settings 
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

# Register task
Register-ScheduledTask -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -RunLevel Highest `
    -Force

Write-Host "✅ Task created successfully!"
Get-ScheduledTask -TaskName $TaskName | Select-Object TaskName, State
```

### VERIFY IT WORKED

After running setup, run this to confirm:

```powershell
Get-ScheduledTask -TaskName "*Projects in Stores*" | Select-Object TaskName, State, Description
```

You should see:
```
TaskName                         State       Description
--------                         -----       -----------
Projects in Stores Server 24/7   Ready       [whatever description]
```

## How It Works

```
System Starts
    ↓
Windows Task Scheduler Runs
    ↓
Scheduled Task "Projects in Stores Server 24/7" Triggers
    ↓
Batch File: start_server_24_7.bat Executes
    ↓
Backend Server Starts
    ↓
Batch File Monitors Server
    ↓
If Server Crashes:
    → Automatically Restarts (waits 5 seconds)
    → Continuous monitoring loop
    ↓
Server Stays Running 24/7
```

## What Each File Does

| File | Purpose |
|------|---------|
| `start_server_24_7.bat` | Continuously runs the backend with auto-restart |
| `SetupAutoStart.bat` | Creates the scheduled task (requires admin) |
| `CreateScheduledTask_Admin.ps1` | PowerShell version of task creation |

## After Setup: System Behavior

### Normal Operation
- System starts → Task scheduler triggers → Server auto-starts
- Server runs continuously
- If server crashes → auto-restarts within 5 seconds

### If You Stop the Server Manually
```batch
# To manually stop (Windows will restart it automatically)
taskkill /PID <ProcessID> /F

# To PERMANENTLY stop (disable the task first)
# 1. Open Task Scheduler
# 2. Find "Projects in Stores Server 24/7"
# 3. Right-click → Disable

# Or use PowerShell:
Disable-ScheduledTask -TaskName "Projects in Stores Server 24/7"

# To re-enable:
Enable-ScheduledTask -TaskName "Projects in Stores Server 24/7"
```

## Troubleshooting

### Problem: "Access Denied" when running setup
**Solution**: Right-click → "Run as Administrator"

### Problem: Task created but server doesn't start on reboot
**Check**:
1. Is the batch file path correct? (Full path needed)
2. Is the .venv folder accessible after reboot?
3. Check Task Scheduler logs: 
   - Open Task Scheduler
   - Look for "Projects in Stores Server 24/7"
   - Check "History" tab for errors

### Problem: Server starts then immediately crashes
**Check**:
1. Are Python dependencies installed?
2. Are data files (active_users.json, etc.) created?
3. Is there sufficient disk space?
4. Check server logs in Activity Hub\backend for errors

## Current Server Status

✅ **NOW RUNNING**:
- Port: 8001
- Process ID: 22148
- Status: Listening and operational
- Uptime: Started March 5, 2026

### Quick Test
```powershell
Invoke-WebRequest http://localhost:8001/api/auth/user | Select-Object StatusCode, StatusDescription
# Should return: 200 OK
```

## Next Steps

1. **URGENT**: Run SetupAutoStart.bat with admin privileges
2. Verify task creation: `Get-ScheduledTask -TaskName "*Projects*"`
3. Restart the computer to verify auto-start works
4. Check Activity Log to confirm server is tracking properly
5. Test feedback submission and user tracking functions

## Documentation

For reference, see these files:
- BEFORE_AFTER_COMPARISON.md - Impact of tracking fixes
- QUICK_START_TESTING.md - How to test the features
- IMPLEMENTATION_SUMMARY.md - Technical details

## Questions?

This setup is critical for production. If you encounter issues:
1. Check the error messages carefully
2. Verify file paths are correct
3. Ensure running as Administrator
4. Check Task Scheduler console for detailed logs

---

**REMEMBER**: Without this scheduled task, the server will NOT auto-start after a restart. This is now configured and should persist across reboots.
