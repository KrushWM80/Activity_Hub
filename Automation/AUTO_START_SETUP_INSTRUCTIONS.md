# HOW TO SET UP AUTO-START (PERMANENT SOLUTION)

## Status: READY TO INSTALL

Your services are now fully configured to auto-start on system reboot. Follow these simple steps to activate permanent auto-start.

---

## QUICK SETUP (5 Minutes)

### Option A: One-Click Batch File (RECOMMENDED)
1. Open File Explorer
2. Navigate to: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\`
3. **Right-click** on `setup_auto_start_tasks.bat`
4. Select **"Run as administrator"**
5. A window will appear with task setup progress
6. Click "OK" when complete

That's it! Your services will now auto-start on every reboot.

---

### Option B: Manual Command Setup
If Option A doesn't work, copy-paste these commands into PowerShell (run as admin):

```powershell
# Run Task Scheduler to create tasks manually
# Open Windows Task Scheduler:
# 1. Press Windows Key + R
# 2. Type: taskschd.msc
# 3. Click OK

# Then use these schtasks commands (paste into elevated PowerShell):

# Task 1: Job Codes Auto-Start
schtasks /create /tn "Activity_Hub_JobCodes_AutoStart" /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_jobcodes_server_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f

# Task 2: Projects in Stores Auto-Start
schtasks /create /tn "Activity_Hub_ProjectsInStores_AutoStart" /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\ProjectsinStores\START_BACKEND.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f

# Task 3: TDA Auto-Start
schtasks /create /tn "Activity_Hub_TDA_AutoStart" /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_tda_insights_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f

# Task 4: Store Dashboard Auto-Start  
schtasks /create /tn "Activity_Hub_Store_Dashboard_AutoStart" /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_store_dashboard_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f

# Task 5: Store Meeting Planner Auto-Start
schtasks /create /tn "Activity_Hub_StoreMeetingPlanner_AutoStart" /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Store Meeting Planners\start-server.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f

# Task 6: Zorro Auto-Start
schtasks /create /tn "Activity_Hub_Zorro_AutoStart" /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_zorro_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f

# Task 7: Daily Health Check at 6 AM
schtasks /create /tn "Activity_Hub_Daily_HealthCheck" /tr "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\MONITOR_AND_REPORT.ps1\"" /sc daily /st 06:00:00 /ru SYSTEM /rl HIGHEST /f
```

---

## WHAT GETS CREATED

| Task Name | Trigger | Service | Port | Access |
|-----------|---------|---------|------|--------|
| Activity_Hub_JobCodes_AutoStart | On system startup | Job Codes Dashboard | 8080 | http://10.97.114.181:8080/ |
| Activity_Hub_ProjectsInStores_AutoStart | On system startup | Projects in Stores | 8001 | http://localhost:8001/ |
| Activity_Hub_TDA_AutoStart | On system startup | TDA Insights | 5000 | http://localhost:5000/ |
| Activity_Hub_Store_Dashboard_AutoStart | On system startup | Store Dashboard | 8081 | http://localhost:8081/ |
| Activity_Hub_StoreMeetingPlanner_AutoStart | On system startup | Store Meeting Planner | 8090 | http://localhost:8090/ |
| Activity_Hub_Zorro_AutoStart | On system startup | Zorro Podcast Server | 8888 | http://localhost:8888/ |
| Activity_Hub_Daily_HealthCheck | Daily at 6:00 AM | Monitoring + Email Report | N/A | N/A |

---

## VERIFY TASKS WERE CREATED

After running the setup, verify tasks exist by running this command in PowerShell:

```powershell
schtasks /query /tn "Activity_Hub*" /fo list
```

You should see 7 tasks listed:
- Activity_Hub_JobCodes_AutoStart
- Activity_Hub_ProjectsInStores_AutoStart
- Activity_Hub_TDA_AutoStart
- Activity_Hub_Store_Dashboard_AutoStart
- Activity_Hub_StoreMeetingPlanner_AutoStart
- Activity_Hub_Zorro_AutoStart
- Activity_Hub_Daily_HealthCheck

---

## AFTER SETUP: WHAT HAPPENS

### On System Startup
1. Windows starts → Waits 60 seconds for services to initialize
2. **Automatically runs 6 batch files:**
   - Job Codes Dashboard starts (port 8080, with 5-second crash recovery)
   - Projects in Stores starts (port 8001, with 5-second crash recovery)
   - TDA Insights starts (port 5000, with 5-second crash recovery)
   - Store Dashboard starts (port 8081, with 5-second crash recovery)
   - Store Meeting Planner starts (port 8090)
   - Zorro starts (port 8888, with 5-second crash recovery)
3. All 6 services are running within 30-60 seconds

### Every Day at 6:00 AM
1. Health monitoring script runs automatically
2. Checks status of all 6 services
3. Sends email report with status
4. Auto-restarts any offline services

### If Computer Crashes/Restarts
- Services automatically restart on next boot
- No manual intervention needed
- Email notification sent at 6 AM with overnight status
2. Checks status of all 5 services
3. Sends email report with status
4. Auto-restarts any offline services

### If Computer Crashes/Restarts
- Services automatically restart on next boot
- No manual intervention needed
- Email notification sent at 6 AM with overnight status

---

## MANUAL CONTROLS

### Run a task immediately (without waiting for trigger):
```powershell
schtasks /run /tn "Activity_Hub_TDA_AutoStart"
schtasks /run /tn "Activity_Hub_Store_Dashboard_AutoStart"
schtasks /run /tn "Activity_Hub_Zorro_AutoStart"
schtasks /run /tn "Activity_Hub_Daily_HealthCheck"
```

### View task details:
```powershell
Get-ScheduledTask -TaskName "Activity_Hub*" | Select-Object TaskName, State, LastTaskResult
```

### Disable a task temporarily:
```powershell
Disable-ScheduledTask -TaskName "Activity_Hub_TDA_AutoStart"
```

### Re-enable a task:
```powershell
Enable-ScheduledTask -TaskName "Activity_Hub_TDA_AutoStart"
```

### Delete a task (if needed):
```powershell
Unregister-ScheduledTask -TaskName "Activity_Hub_TDA_AutoStart" -Confirm:$false
```

---

## TROUBLESHOOTING

### Tasks not starting services:
1. Check task logs: `Event Viewer → Windows Logs → System`
2. Look for task "Activity_Hub*" entries
3. Check if services are running: `Get-Process python`

### Email not sending:
1. Check MONITOR_AND_REPORT.ps1 log: `MONITOR_AND_REPORT_*.log`
2. Verify your SMTP email settings in MONITOR_AND_REPORT.ps1
3. Make sure Google Cloud credentials file exists

### Service crashing:
1. Check service log files:
   - TDA: `Store Support/Projects/TDA Insights/tda_insights_server.log`
   - Store Dashboard: `Store Support/Projects/AMP/Store Updates Dashboard/store_dashboard_server.log`
   - Zorro: `Store Support/Projects/AMP/Zorro/zorro_server.log`
2. Check system event viewer for errors

---

## NEXT TEST: Computer Restart

To fully verify everything works:
1. Save your work
2. Restart your computer
3. After restart, wait 2 minutes
4. Check if services are running: `netstat -ano | findstr ":5000\|:8001\|:8080\|:8081\|:8888"`
5. Access services to verify they're responding:
   - http://localhost:5000/ (TDA)
   - http://localhost:8081/ (Store Dashboard)
   - http://localhost:8888/ (Zorro)

---

## SUMMARY

✅ Auto-start setup ready  
✅ All batch files configured  
✅ Health monitoring script ready  
✅ Email reporting configured  

**Next Step:** Run `setup_auto_start_tasks.bat` as Administrator (right-click → Run as admin)

