# Activity Hub - Quick Start & Restart Guide
**Updated: April 30, 2026**

## 🚀 Quick Service Status & Restart

### Current Service Status (All Running ✅)
```
✅ TDA Insights          Port 5000  PID 22236   → http://weus42608431466:5000/tda-initiatives-insights
✅ VET Dashboard         Port 5001  PID 3256    → http://weus42608431466:5001/Dallas_Team_Report
✅ Projects in Stores    Port 8001  PID 9056    → http://weus42608431466.homeoffice.wal-mart.com:8001/
✅ Job Codes Dashboard   Port 8080  PID 11528   → http://weus42608431466:8080/Aligned#
✅ AMP Store Dashboard   Port 8081  PID 23660   → http://weus42608431466:8081/StoreActivityandCommunications
✅ Activity Hub          Port 8088  PID 21240   → http://weus42608431466:8088/activity-hub/for-you
✅ Store Meeting Planner Port 8090  PID 15540   → http://weus42608431466:8090/StoreMeetingPlanner
✅ Zorro Audio Hub       Port 8888  PID 23928   → http://weus42608431466:8888/Zorro/AudioMessageHub
```

### URLs for Access
```
✅ PRODUCTION URLS (Use These for Team Access):
├── TDA Insights:         http://weus42608431466:5000/tda-initiatives-insights
├── VET Dashboard:        http://weus42608431466:5001/Dallas_Team_Report
├── Projects in Stores:   http://weus42608431466.homeoffice.wal-mart.com:8001/
├── Job Codes:            http://weus42608431466:8080/Aligned#
├── AMP Dashboard:        http://weus42608431466:8081/StoreActivityandCommunications
├── Activity Hub:         http://weus42608431466:8088/activity-hub/for-you
├── Meeting Planner:      http://weus42608431466:8090/StoreMeetingPlanner
└── Zorro Audio:          http://weus42608431466:8888/Zorro/AudioMessageHub

📍 LOCAL URLS (Development/Testing Only):
├── TDA Insights:         http://localhost:5000/tda-initiatives-insights
├── VET Dashboard:        http://localhost:5001/Dallas_Team_Report
├── Projects in Stores:   http://localhost:8002/ (dev port)
├── Job Codes:            http://localhost:8080/Aligned#
├── AMP Dashboard:        http://localhost:8081/
├── Activity Hub:         http://localhost:8088/activity-hub/
├── Meeting Planner:      http://localhost:8090/StoreMeetingPlanner
└── Zorro Audio:          http://localhost:8888/Zorro/AudioMessageHub
```

---

## 🔧 Quick Restart Commands

### Option 1: Restart Individual Service
```powershell
# TDA Insights (Port 5000)
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_tda_insights_24_7.bat"

# VET Dashboard (Port 5001)
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_vet_dashboard_24_7.bat"

# AMP Store Dashboard (Port 8081)
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_store_dashboard_24_7.bat"

# Zorro Audio Hub (Port 8888)
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_zorro_24_7.bat"

# Store Meeting Planner (Port 8090)
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_meeting_planner_24_7.bat"

# Activity Hub (Port 8088)
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_activity_hub_24_7.bat"

# Job Codes (Port 8080) - Uses scheduled task
Start-ScheduledTask -TaskName "JobCodes-Backend-Server"

# Projects in Stores (Port 8001) - Uses scheduled task
Start-ScheduledTask -TaskName "Activity_Hub_ProjectsInStores_AutoStart"
```

### Option 2: Full Health Check & Auto-Restart
```powershell
# Run complete health check (auto-restarts any offline services)
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\MONITOR_AND_REPORT.ps1"
```

### Option 3: Kill All & Restart Everything
```powershell
# Kill all Python processes
taskkill /F /IM python.exe

# Wait a moment
Start-Sleep -Seconds 3

# Start all services via scheduled tasks
Start-ScheduledTask -TaskName "Activity_Hub_*"
```

---

## 📊 Service Health Check

### Quick Status Check
```powershell
# Check all ports
netstat -ano | findstr /i "5000\|5001\|8001\|8080\|8081\|8088\|8090\|8888" | findstr LISTENING

# Check running Python processes
Get-Process python | Select-Object Name, Id, @{Name='CPU';Expression={$_.CPU.ToString('N2')}}, WorkingSet | Format-Table
```

### Daily Health Report
- **Automatic**: Runs daily at 6:00 AM
- **Manual**: Run `MONITOR_AND_REPORT.ps1`
- **Email**: Sent to `ATCTeamsupport@walmart.com` and `kendall.rush@walmart.com`

---

## ⚙️ Troubleshooting

### If Service Won't Start
1. Check if port is already in use:
   ```powershell
   netstat -ano | findstr :PORT_NUMBER
   ```
2. Kill conflicting process:
   ```powershell
   taskkill /PID PROCESS_ID /F
   ```
3. Restart the service using commands above

### If Scheduled Tasks Not Working
- CIM is broken on this machine
- Use `schtasks.exe` commands instead:
  ```powershell
  schtasks /run /tn "TaskName"
  ```

### If Web Interface Not Loading
- Check if service is running on correct port
- Try localhost URL first, then network URL
- Check browser console for CORS errors

---

## 📋 Service Dependencies

| Service | Backend Type | Frontend | Database | External APIs |
|---------|-------------|----------|----------|---------------|
| TDA Insights | Flask/Python | HTML/JS | BigQuery | None |
| VET Dashboard | Flask/Python | HTML/JS | BigQuery | None |
| AMP Dashboard | Flask/Python | HTML/JS | BigQuery | MP4 Pipeline |
| Zorro Audio | HTTP/Python | HTML/JS | BigQuery | edge_tts/Jenny |
| Activity Hub | Node.js | React | PostgreSQL | AD Groups |
| Job Codes | FastAPI/Python | HTML/JS | BigQuery | None |
| Projects in Stores | Custom/Python | HTML | BigQuery | None |
| Meeting Planner | FastAPI/Python | HTML/JS | BigQuery | None |

---

## 🔄 Auto-Start Configuration

All services are configured with **4-layer resilience**:
1. **Bat loops**: Infinite restart on crash (within 5 seconds)
2. **Login tasks**: Start on Windows login
3. **Health monitor**: Every 5 minutes checks and restarts
4. **Daily reports**: 6 AM health check emails

**Re-register all tasks** (after Windows updates):
```powershell
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\register_tasks_cmd.bat"
```