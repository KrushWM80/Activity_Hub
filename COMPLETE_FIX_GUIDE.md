# Activity Hub 24/7 Operations - COMPLETE SYSTEM FIX

## THE PROBLEM (Why Nothing Was Running)

**Root Cause:** Scheduled tasks were DELETED or lost due to Windows update.

### What Happened:
1. **Scheduled tasks gone** - No auto-start configuration
2. **Old Python processes stuck** - Running for 3+ days, not responding
3. **No recovery system** - If service crashed, nothing restarted it
4. **No keep-alive** - Computer could sleep anytime
5. **No continuous monitoring** - 16-hour gap between health checks

### Why Services Seemed "Ready" But Not Responding:
- Scheduled task showed as existing (Windows cache)
- Task would have run on NEXT reboot
- But without reboot, services never started from task
- Only reason ANY Python processes existed was from manual starts weeks ago

---

## THE SOLUTION (What We're Fixing)

### Three Layers of Redundancy:

#### **Layer 1: Scheduled Auto-Start (System Reboot)**
- 6 services auto-start on every system boot
- Each runs with full Python path (works under SYSTEM user)
- File: `MASTER_SETUP_24_7.bat`

#### **Layer 2: Continuous Monitoring (Every 5 Minutes)**
- Runs 24/7, checks all 6 services every 5 minutes
- If any service is down → immediately restarts it
- Logs all activity
- File: `continuous_monitor.ps1`
- Scheduled as: `Activity_Hub_Continuous_Monitor` task

#### **Layer 3: Keep-Alive Service (24/7)**
- Prevents Windows from sleeping/hibernating
- Allows batch files and monitoring to keep running
- File: `keep_alive.ps1`
- Scheduled as: `Activity_Hub_KeepAwake` task

#### **Layer 4: Daily Health Report (6:00 AM)**
- Sends email with all service status
- Reference point for health verification
- File: `MONITOR_AND_REPORT.ps1`

---

## IMPLEMENTATION STEPS (YOU NEED TO DO THIS)

### Step 1: RUN THE MASTER SETUP (AS ADMIN)
```
1. Right-click:   MASTER_SETUP_24_7.bat
2. Select:        "Run as administrator"
3. Click:         "Yes" at the UAC prompt
4. Wait:          ~30 seconds for completion
5. Press:         Space when done
```

**What this does:**
- Kills all old stuck Python processes
- Deletes old/broken scheduled tasks
- Creates 9 new scheduled tasks:
  - 6 service auto-starters (OnSystemStart)
  - 1 keep-alive service (OnStart)
  - 1 continuous monitoring (every 5 min)
  - 1 daily health check (6:00 AM)

### Step 2: RESTART YOUR COMPUTER
```
1. Save all work
2. Restart computer (or: shutdown /r /t 30)
3. Wait 3-5 minutes after restart
4. Services should be running
```

**What happens:**
- Keep-alive service starts
- 6 services auto-start from scheduled tasks
- Services enter auto-restart loops
- Continuous monitoring begins checking

### Step 3: VERIFY EVERYTHING WORKS
```
Right-click:   VERIFY_SYSTEM_STATUS.bat
Select:        "Run as administrator"
```

**What to look for:**
```
✓ All 9 tasks found = Success
✓ All 6 ports listening = Services running
✓ Python processes visible = Execution confirmed
```

### Step 4: TEST THE SERVICES

Open your browser and visit:
- **Job Codes:** http://10.97.114.181:8080 (IP-based only)
- **Projects:** http://localhost:8001
- **TDA Insights:** http://localhost:5000
- **Store Dashboard:** http://localhost:8081
- **Meeting Planner:** http://localhost:8090
- **Zorro:** http://localhost:8888

All should load and respond.

---

## HOW IT WILL WORK GOING FORWARD

### Scenario: Service Crashes at 2 PM
```
2:00 PM  - Service crashes
2:00 PM  - Python process exits
2:00-2:05 PM - Continuous monitor (every 5 min) doesn't detect yet
2:05 PM  - Continuous monitor DETECTS port not listening
2:05:30 PM - Monitor automatically restarts the service
2:06 PM  - Service back online
Total outage: ~6 minutes (vs. 16 hours with old system)
```

### Scenario: Computer Sleeps at Midnight
```
11:59 PM - Keep-alive service running
12:00 AM - Windows tries to sleep... keep-alive prevents it
12:00 AM - Services continue running
7:00 AM  - Services still running
Total sleep: 0 minutes (computer never sleeps)
```

### Scenario: System Reboot (Windows Update)
```
Before reboot - Continuous monitor running
Windows reboots...
At boot - Keep-alive starts
At boot - All 6 services auto-start from scheduled tasks
10 seconds - Services fully operational
```

---

## FILES CREATED/MODIFIED

### New/Updated Files:
1. **MASTER_SETUP_24_7.bat** - Master setup script (YOU RUN THIS FIRST)
2. **continuous_monitor.ps1** - Continuous monitoring (runs every 5 min)
3. **keep_alive.ps1** - System keep-alive (24/7)
4. **VERIFY_SYSTEM_STATUS.bat** - Verification tool
5. **SYSTEM_AUDIT_GAPS.md** - Complete gap analysis

### Already Working (Unchanged):
1. **6 service start files** - `start_*.bat` files
2. **MONITOR_AND_REPORT.ps1** - Daily health check
3. **All backend service files** - Python apps

---

## ERROR RECOVERY REFERENCE

### If Services Stop Working Again:

**Option 1: Quick Restart**
```powershell
# From PowerShell
Restart-Computer -Force
# OR from cmd
shutdown /r /t 10
```

**Option 2: Manual Service Restart**
```
1. Open Automation folder
2. Double-click the relevant .bat file:
   - start_jobcodes_server_24_7.bat
   - start_projects_in_stores_24_7.bat
   - start_tda_insights_24_7.bat
   - start_store_dashboard_24_7.bat
   - etc.
3. Service starts in new window
```

**Option 3: Check What's Broken**
```
Right-click: VERIFY_SYSTEM_STATUS.bat
Run as administrator
- Shows test results
- Tells you what's wrong
```

**Option 4: Nuclear Option (Full Reset)**
```
1. Right-click: MASTER_SETUP_24_7.bat
2. Run as administrator
3. Restart computer
4. Everything fresh
```

---

## LOGS & DIAGNOSTICS

### Check Logs:
```
-- Continuous monitoring:  continuous_monitor.log
-- Service logs:            Automation/[service]_server.log
-- Keep-alive:              keep-alive.log
-- System status:           system_status.log
```

### View logs in PowerShell:
```powershell
Get-Content C:\Users\krush\OneDrive\ -\ Walmart\ Inc\Documents\VSCode\Activity_Hub\continuous_monitor.log -Tail 20
```

---

## CRITICAL SUCCESS FACTORS

✅ **Do This:**
1. Run MASTER_SETUP_24_7.bat as Admin
2. Restart your computer
3. Wait 5 minutes before testing
4. Run VERIFY_SYSTEM_STATUS.bat after restart

❌ **Don't Do This:**
1. Don't run setup script without Admin rights
2. Don't expect services to start without restart (first time)
3. Don't close batch file windows (they're monitoring)
4. Don't turn off keep-alive (computer will sleep)
5. Don't skip the final verification step

---

## WHAT EACH TASK DOES

| Task Name | Trigger | Frequency | What It Does |
|-----------|---------|-----------|------------|
| Activity_Hub_JobCodes_AutoStart | System Start | Once at boot | Starts Job Codes server (port 8080) |
| Activity_Hub_ProjectsInStores_AutoStart | System Start | Once at boot | Starts Projects server (port 8001) |
| Activity_Hub_TDA_AutoStart | System Start | Once at boot | Starts TDA Insights (port 5000) |
| Activity_Hub_Store_Dashboard_AutoStart | System Start | Once at boot | Starts Store Dashboard (port 8081) |
| Activity_Hub_StoreMeetingPlanner_AutoStart | System Start | Once at boot | Starts Meeting Planner (port 8090) |
| Activity_Hub_Zorro_AutoStart | System Start | Once at boot | Starts Zorro (port 8888) |
| Activity_Hub_KeepAwake | System Start | Continuous | Prevents Windows sleep (24/7) |
| Activity_Hub_Continuous_Monitor | Every 5 min | Every 5 min | Checks all services, restarts if down |
| Activity_Hub_Daily_HealthCheck | Daily @ 6 AM | Once per day | Sends email with status report |

---

## NEXT STEPS

1. **RIGHT NOW:** Read this document completely
2. **IMMEDIATELY:** Run MASTER_SETUP_24_7.bat as Administrator
3. **NEXT:** Restart your computer
4. **AFTER RESTART:** Run VERIFY_SYSTEM_STATUS.bat
5. **TEST:** Visit each service URL in browser
6. **DONE:** Services now run 24/7 with automatic recovery

---

**Questions/Issues?** Check the logs or re-run VERIFY_SYSTEM_STATUS.bat to see what's happening.

**Last Updated:** March 16, 2026
