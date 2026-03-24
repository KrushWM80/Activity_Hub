# Activity Hub Services - Quick Reference Guide

## Service Inventory (Updated March 24, 2026)

### Core Infrastructure Services

| Service | Port | URL | Type | Status Check |
|---------|------|-----|------|--------------|
| **Job Codes Dashboard** | 8080 | http://10.97.114.181:8080/static/index.html# | FastAPI | netstat :8080 |
| **Projects in Stores** | 8001 | http://10.97.114.181:8001/ | Teaming | netstat :8001 |
| **TDA Insights** | 5000 | http://localhost:5000/dashboard.html | Flask | netstat :5000 |
| **AMP Store Dashboard** | 8081 | http://localhost:8081/ | Flask | HTTP GET verification |
| **Zorro Podcast Server** | 8888 | http://localhost:8888/ | HTTP | netstat :8888 |
| **V.E.T. Dashboard** | 5001 | http://localhost:5001/vet_dashboard.html | Flask | netstat :5001 |
| **Store Meeting Planner** | 8090 | http://localhost:8090/ | FastAPI | netstat :8090 |

---

## Health Check & Auto-Restart System

### Monitoring Schedule
```
Daily at 6:00 AM EST        → Full health check + email report
On System Startup           → Startup detection + health check + notification
Every 6 Hours (Background)  → Automatic restart if services offline
```

### What Gets Monitored
✅ Job Codes (Port 8080)  
✅ Projects in Stores (Port 8001)  
✅ TDA Insights (Port 5000)  
✅ AMP Store Dashboard (Port 8081)  
✅ Zorro (Port 8888)  
✅ V.E.T. Dashboard (Port 5001)  
✅ Store Meeting Planner (Port 8090)  
✅ DC Manager Tasks (26 tasks)  
✅ TDA Weekly Email Task (Thursday 11 AM)

### Auto-Restart Actions
When monitoring detects a service is offline:

1. **Job Codes** → Triggers scheduled task `JobCodes-Backend-Server`
2. **TDA Insights** → Starts `backend_simple.py` via `start_tda_insights_24_7.bat`
3. **AMP Store Dashboard** → Starts `amp_backend_server.py` via `start_store_dashboard_24_7.bat`
4. **Zorro** → Starts `podcast_server.py` via `start_zorro_24_7.bat`
5. **V.E.T. Dashboard** → Starts `backend.py` via `start_vet_dashboard_24_7.bat`
6. **Store Meeting Planner** → Starts `main.py` via `start_meeting_planner_24_7.bat`

Each service:
- Auto-restarts on crash (5-second interval)
- Logs all activity to service-specific log file
- Verifies successful startup
- Reports status in daily email

---

## Accessing Each Service

### From Local Machine (Same Computer)
```
TDA Insights              → http://localhost:5000/dashboard.html
AMP Store Dashboard       → http://localhost:8081/
Zorro Podcast Server      → http://localhost:8888/
  ↳ Audio Generator       → http://localhost:8888/create-audio
V.E.T. Dashboard          → http://localhost:5001/vet_dashboard.html
Store Meeting Planner     → http://localhost:8090/
```

### From Network (IP-Based Access)
```
Job Codes Dashboard       → http://10.97.114.181:8080/static/index.html#
Projects in Stores        → http://10.97.114.181:8001/
```

### From Remote/Other Locations
- Job Codes & Projects: Use IP address (10.97.114.181) - already network accessible
- TDA, Dashboard, Zorro: Use localhost only OR configure network access

---

## Key Features by Service

### Job Codes Teaming Dashboard
- 24/7 auto-restart via scheduled tasks
- Daily reconciliation (2 AM)
- IP-based access (localhost redirects to wrong hostname)
- Triggers: Startup + 3 AM + Every 6 hours

### TDA Insights Dashboard
- BigQuery integration for store data
- Requires Google Cloud credentials
- Auto-restart if offline
- Health check every 6 hours

### Store Activity & Communication Dashboard
- Audio synthesis with Jenny Neural voice
- MP4-based message platform
- Requires Google Cloud credentials
- Auto-restart if offline

### Zorro Podcast Server
- Jenny Neural voice audio generation
- Podcast and message management
- Web-based audio editor
- Auto-restart if offline

### Projects in Stores
- Located on port 8001
- Team-based project management
- Monitored but separate startup process
- Health check every 6 hours

---

## Log Files & Diagnostics

### Current Status Log
`C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\system_status.log`
- System-wide monitoring log
- Downtime detection
- Status persistence between runs

### Service-Specific Logs
```
Job Codes        → Automation/jobcodes_server.log
TDA Insights     → Store Support/Projects/TDA Insights/tda_insights_server.log
Store Dashboard  → Store Support/Projects/AMP/Store Updates Dashboard/store_dashboard_server.log
Zorro            → Store Support/Projects/AMP/Zorro/zorro_server.log
```

### Checking Service Status
```powershell
# Check all listening ports
netstat -ano | findstr "LISTENING" | findstr ":80\|:5000\|:8001\|:8081\|:8888"

# Check specific service
netstat -ano | findstr ":8080.*LISTENING"  # Job Codes
netstat -ano | findstr ":8888.*LISTENING"  # Zorro

# Check process list
Get-Process python  # Show all Python processes

# Check scheduled tasks
Get-ScheduledTask | Where-Object {$_.TaskName -like "*JobCodes*"}
Get-ScheduledTask | Where-Object {$_.TaskName -like "*ActivityHub*"}
```

---

## Starting Services Manually

### Start All Services
```powershell
# Kill existing instances
taskkill /F /IM python.exe

# Wait for cleanup
Start-Sleep -Seconds 2

# Start Job Codes (via scheduled task)
Start-ScheduledTask -TaskName "JobCodes-Backend-Server"

# Start others via batch files
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_tda_insights_24_7.bat"
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_store_dashboard_24_7.bat"
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_zorro_24_7.bat"
```

### Start Individual Service
```powershell
# TDA Insights
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\TDA Insights"
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" backend_simple.py

# Store Dashboard
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Store Updates Dashboard"
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" amp_backend_server.py

# Zorro
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Zorro"
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" podcast_server.py
```

---

## Monitoring Email Reports

### What's Included
- ✅ Status table of all services (Running/Offline)
- ✅ Port listening verification
- ✅ Number of services running (X/5)
- ✅ DC Manager task count (26/26)
- ✅ Downtime duration (if applicable)
- ✅ System restart detection
- ✅ Access URLs for all services
- ✅ Upcoming scheduled events
- ✅ Timestamps and log file references

### Recipients
- ATCTeamsupport@walmart.com
- kendall.rush@walmart.com

### Schedule
- **Daily:** 6:00 AM EST
- **On Startup:** Within 1 minute of system restart
- **On Error:** Immediate alert if critical services offline

---

## Port Summary

| Port | Service | Status |
|------|---------|--------|
| 5000 | TDA Insights | Monitored |
| 8001 | Projects in Stores | Monitored |
| 8081 | Store Activity Dashboard | Auto-restart |
| 8080 | Job Codes | 24/7 Auto-restart |
| 8888 | Zorro | Auto-restart |

---

## Emergency Restart

### If Everything is Down
```powershell
# As Administrator
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

# Execute full restoration
.\RESTORE_ALL_TASKS_NOW.ps1

# Then trigger health check
.\MONITOR_AND_REPORT.ps1
```

### If Specific Service Won't Start
1. Check log file for error messages
2. Verify dependencies (Python, Google Cloud SDK, etc.)
3. Kill orphaned Python processes: `taskkill /F /IM python.exe`
4. Check port: `netstat -ano | findstr ":PORT"`
5. Review error logs in service directory

---

## Configuration File Locations

| Component | Path |
|-----------|------|
| Job Codes Launcher | `Automation/start_jobcodes_server_24_7.bat` |
| TDA Launcher | `Automation/start_tda_insights_24_7.bat` |
| Store Dashboard Launcher | `Automation/start_store_dashboard_24_7.bat` |
| Zorro Launcher | `Automation/start_zorro_24_7.bat` |
| System Monitor | `MONITOR_AND_REPORT.ps1` |
| Task Restoration | `RESTORE_ALL_TASKS_NOW.ps1` |
| This Reference | `Automation/QUICK_REFERENCE_SERVICES.md` |

---

**Last Updated:** March 12, 2026  
**System:** WEUS42608431466  
**Administrator:** Kendall Rush  
**Support Email:** ATCTeamsupport@walmart.com
