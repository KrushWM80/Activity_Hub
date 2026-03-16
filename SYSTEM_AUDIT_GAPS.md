# Activity Hub - System Audit & Gap Analysis
**Date:** March 16, 2026

---

## WHAT'S SUPPOSED TO KEEP SERVICES RUNNING

### 1. SCHEDULED TASKS (Initial Boot Only)
**File:** `Automation/setup_tasks_clean.bat`  
**Status:** ✅ Created (as of last run)  
**Scheduled Tasks (7 total):**
- Activity_Hub_JobCodes_AutoStart → `start_jobcodes_server_24_7.bat` (OnStart)
- Activity_Hub_ProjectsInStores_AutoStart → `start_projects_in_stores_24_7.bat` (OnStart)
- Activity_Hub_TDA_AutoStart → `start_tda_insights_24_7.bat` (OnStart)
- Activity_Hub_Store_Dashboard_AutoStart → `start_store_dashboard_24_7.bat` (OnStart)
- Activity_Hub_StoreMeetingPlanner_AutoStart → `start-server.bat` (OnStart)
- Activity_Hub_Zorro_AutoStart → `start_zorro_24_7.bat` (OnStart)
- Activity_Hub_Daily_HealthCheck → `MONITOR_AND_REPORT.ps1` (Daily @ 6:00 AM)

**Problem:** Only runs ONCE when computer boots. If services crash, nothing restarts them.

---

### 2. AUTO-RESTART IN BATCH FILES
**Example:** `Automation/start_tda_insights_24_7.bat`
```batch
:restart_loop
echo Launching TDA Insights...
"%PythonExe%" backend_simple.py 2>> "%LogFile%"
echo Process exited, waiting 5 seconds...
timeout /t 5 /nobreak
goto restart_loop
```

**How it works:** If Python crashes, it waits 5 seconds and restarts  
**Problem:** This ONLY works if the batch file stays running. But:
- If Windows sleeps, the batch stops
- If you close the batch window, it stops
- Batch process must be persistently running for this loop to work

**Status:** ⚠️ Works ONLY if batch file never closes

---

### 3. KEEP-ALIVE SERVICE (Prevents Sleep)
**File:** `Automation/start_keep_awake_24_7.bat`  
**What it does:** Runs `keep-awake.ps1` to prevent system sleep  
**Status:** ❌ **NOT SCHEDULED** - exists but never runs automatically

**Missing:** Should be scheduled to run continuously

---

### 4. HEALTH MONITORING
**File:** `MONITOR_AND_REPORT.ps1`  
**How often:** Daily @ 6:00 AM + System startup  
**What it does:** Checks all 6 services, reports status via email  
**Problem:** Only checks TWICE per day. Big gaps:
- If service crashes at 3 PM, won't know until 6 AM (15 hours)
- Only REPORTS status, doesn't automatically restart services

**Status:** ⚠️ Monitoring exists but recovery is manual/delayed

---

## CRITICAL GAPS

| Gap | Current State | Required State | Impact |
|-----|---------------|-----------------|--------|
| **Computer Sleep Prevention** | `keep_awake.ps1` exists but NOT scheduled | Should run 24/7 | Computer sleeps → all services stop |
| **Daytime Service Recovery** | No monitoring between 6 AM checks | Need monitoring every 5-10 min | Service crashes at 2 PM → offline for 16 hours |
| **Continuous Service Health** | Batch auto-restart only works if batch window open | Services must persistently run | If batch closes, auto-restart stops |
| **Startup Verification** | No check that services actually started after boot | Should verify and log startup success | Services might fail to start without notification |
| **Network Recovery** | No detection of internet loss | Should detect & retry on disconnect | Network outage = permanent service loss |
| **Scheduled Task Verification** | No check that tasks are still registered | Should verify Wednesday/Sunday | Tasks might disappear after Windows updates |

---

## EXECUTION FLOW (WHAT ACTUALLY HAPPENS)

### Scenario 1: Computer Powers On
```
1. System boots
2. Scheduled tasks trigger (OnStart)
3. Each service batch file starts
4. Batch file runs Python, enters auto-restart loop
5. Auto-restart loop works WHILE batch window is open
6. ✅ Services run
```

### Scenario 2: Service Crashes at 2 PM
```
1. Python process crashes
2. Auto-restart loop tries to restart it (works IF batch is still running)
3. 3 PM - Service still running ✅
4. 5 PM - Service runs fine ✅
5. 6:00 AM next day - Health check confirms running ✅
TOTAL SAFE TIME: 16+ hours
```

### Scenario 3: Computer Sleeps at 11 PM
```
1. Windows goes to sleep (no keep-awake scheduled)
2. All Python processes stop
3. Batch files stop
4. Auto-restart loops stop
5. Services offline (6+ hours until morning)
6. 6:00 AM - Health check runs, detects outage
7. Report sent to email
8. User reads email: "Services were down all night"
```

### Scenario 4: Batch Window Closed
```
1. User closes batch file window by mistake
2. Auto-restart loop ends
3. Next crash → no automatic restart
4. Service stays dead
5. No notification
6. Until 6 AM health check
```

---

## WHAT NEEDS TO BE FIXED (PRIORITY ORDER)

### 🔴 CRITICAL (Must Have)
1. **Schedule keep-awake.ps1** to run continuously
   - Prevents Windows sleep
   - Allows batch files to keep running

2. **Create continuous monitoring service** (every 5 minutes)
   - Check all 6 ports are listening
   - Restart any that failed
   - Log everything
   - Don't wait until 6 AM to report

3. **Verify scheduled tasks survive updates**
   - Weekly verification script
   - Recreate if missing
   - Log to file

### 🟠 HIGH (Should Have)
4. **Create service restart utility**
   - Can be called with: `restart_service.ps1 "meeting-planner"`
   - Kills and restarts specific service
   - Reports success/failure

5. **Batch file stability**
   - Ensure batch files can't be closed accidentally
   - Add logging to confirm batch is running
   - Add error handling for crashes

### 🟡 MEDIUM (Nice to Have)
6. **Network recovery**
   - Detect internet outage
   - Retry on reconnect
   
7. **Automatic email on failures**
   - Don't wait until 6 AM
   - Alert immediately on crash detection

---

## CURRENT RUNNING SERVICES (VERIFICATION NEEDED)

**To confirm what's ACTUALLY running, execute:**
```powershell
Get-Process python | Select-Object Name, Id, Path, StartTime | Format-Table
```

**Expected Output (if all working):**
- Multiple "python.exe" processes with different start times
- 6+ processes for the 6 services
- Time should be recent (within hours, not days)

**Actual Output (as of March 16):**
- [NEED USER TO RUN THIS COMMAND]

---

## REFERENCES

- Tasks created by: `Automation/setup_tasks_clean.bat`
- Health monitoring by: `MONITOR_AND_REPORT.ps1`
- Keep-alive script location: `Automation/start_keep_awake_24_7.bat` (NOT SCHEDULED)
- Service auto-restart in: Each batch file's `:restart_loop` section

---

## NEXT STEPS

1. Run this command and send output:
   ```powershell
   Get-Process python | Select-Object Name, Id, CommandLine | Format-Table -AutoSize
   ```

2. Check if keep-awake is scheduled:
   ```powershell
   Get-ScheduledTask | Where-Object {$_.TaskName -like "*[Kk]eep*" -or $_.TaskName -like "*[Ss]leep*"}
   ```

3. Verify scheduled tasks exist:
   ```powershell
   Get-ScheduledTask | Where-Object {$_.TaskName -like "Activity_Hub*"} | Select-Object TaskName
   ```

Once we get the output, I can diagnose exactly what's running and what's not.
