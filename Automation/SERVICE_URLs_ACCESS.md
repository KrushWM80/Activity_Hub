# Activity Hub Services - URL & Access Reference

## Service Access Matrix

### TDA Insights Dashboard
```
Service Name:    TDA Insights Dashboard
Backend File:    Store Support/Projects/TDA Insights/backend_simple.py
Framework:       Flask with BigQuery
Port:            5000
Status:          Running (monitored)

Access URLs:
  Local:  http://localhost:5000/dashboard.html
  Remote: Not directly accessible (use VPN/forwarding)

Data Source:
  - Google Cloud BigQuery
  - Project: wmt-assetprotection-prod
  - Dataset: Store_Support_Dev
  
Feature:
  - Store performance analytics
  - Real-time dashboards
  - Historical data visualization

Log File:
  - Store Support/Projects/TDA Insights/tda_insights_server.log

Auto-Restart Launcher:
  - Automation/start_tda_insights_24_7.bat

Health Check:
  - Monitored every 6 hours
  - Manual check: netstat -ano | findstr ":8080.*LISTENING"
```

### Store Activity & Communication Dashboard (AMP)
```
Service Name:    Store Activity & Communication Dashboard
Backend File:    Store Support/Projects/AMP/Store Updates Dashboard/amp_backend_server.py
Framework:       Flask with BigQuery
Port:            8081
Status:          Running (monitored)

Access URLs:
  Local:  http://localhost:8081/
  Remote: Not directly accessible (use VPN/forwarding)

Data Source:
  - Google Cloud BigQuery
  - Project: wmt-assetprotection-prod
  - Dataset: Store_Support_Dev
  - Table: Output - AMP ALL 2

Features:
  - Store communication platform
  - Message summarization
  - MP4 audio synthesis (Jenny voice)
  - Real-time updates

Log File:
  - Store Support/Projects/AMP/Store Updates Dashboard/store_dashboard_server.log

Auto-Restart Launcher:
  - Automation/start_store_dashboard_24_7.bat

Health Check:
  - Monitored every 6 hours
  - Manual check: netstat -ano | findstr ":5000.*LISTENING"

Note: Shares port 5000 with TDA Insights (only one can run at a time)
```

### Zorro Activity Hub - Podcast Server
```
Service Name:    Zorro Activity Hub Podcast Server
Backend File:    Store Support/Projects/AMP/Zorro/podcast_server.py
Framework:       Python HTTP Server (SimpleHTTPRequestHandler)
Port:            8888
Status:          Running (monitored)

Access URLs (Full):
  Main Interface:      http://localhost:8888/
  Audio Generator:     http://localhost:8888/create-audio
  Audio File List:     http://localhost:8888/api/audio-list
  Download Podcast:    http://localhost:8888/podcasts/[filename]
  Generated MP4 Audio: http://localhost:8888/audio/[filename]
  Metadata API:        http://localhost:8888/metadata/[json_file]

Features:
  - Jenny Neural voice MP4 generation
  - Audio message creation
  - Podcast file management
  - Web interface for generation
  - Metadata tracking

Audio Generation:
  - Voice: Jenny Neural (Windows Neural TTS)
  - Format: MP4 with AAC codec @ 256 kbps
  - Endpoint: POST /api/generate-audio
  - Parameters: title, description, area, type, priority

API Endpoints:
  POST /api/generate-jenny-audio  - Generate MP4 with Jenny voice
  POST /api/generate-audio        - Same as above
  POST /api/delete-file           - Delete audio file
  POST /api/generate-from-template- Generate from template

Output Directories:
  Podcasts:      store Support/Projects/AMP/Zorro/output/Audio/
  Generated MP4: Store Support/Projects/AMP/Zorro/Audio/mp4_output/
  Metadata:      Store Support/Projects/AMP/Zorro/output/metadata/

Log File:
  - Store Support/Projects/AMP/Zorro/zorro_server.log

Auto-Restart Launcher:
  - Automation/start_zorro_24_7.bat

Health Check:
  - Monitored every 6 hours
  - Manual check: netstat -ano | findstr ":8888.*LISTENING"

Example Usage:
  1. Navigate to http://localhost:8888/create-audio
  2. Enter title, description, area, type, priority
  3. Click "Generate MP4 Audio"
  4. Audio will be synthesized with Jenny voice
  5. Download or play directly in browser
```

### Job Codes Teaming Dashboard
```
Service Name:    Job Codes Teaming Dashboard
Backend File:    Store Support/Projects/JobCodes-teaming/Teaming/dashboard/backend/main.py
Framework:       FastAPI with BigQuery
Port:            8080
IP Address:      10.97.114.181
Status:          Running (24/7 with scheduled restarts)

Access URLs:
  Local IP:       http://10.97.114.181:8080/static/index.html#
  Dashboard:      http://10.97.114.181:8080/
  API Base:       http://10.97.114.181:8080/api/

Data Source:
  - Google Cloud BigQuery
  - Real-time job code data
  - Store job assignments

Restart Schedule:
  - On system startup (15-second delay)
  - Daily at 3:00 AM
  - Every 6 hours (health check)

Scheduled Task:
  - Task Name: JobCodes-Backend-Server
  - Action: Automation/start_jobcodes_server_24_7.bat
  - Triggers: Startup + 3 AM Daily + Every 6 Hours

Log File:
  - Automation/jobcodes_server.log

Benefits:
  - Uses IP address (not hostname DNS)
  - Reliable 24/7 availability
  - Multiple restart triggers
  - Comprehensive logging

Health Check:
  - Monitored every 6 hours
  - Manual check: netstat -ano | findstr ":8080.*LISTENING"

Documentation:
  - Check JOBCODES_ACCESS_GUIDE.md
  - Configuration in config.py
  - Access decision documented
```

### Projects in Stores
```
Service Name:    Projects in Stores Teaming Platform
Port:            8001
Status:          Active (use existing startup procedures)

Access URL:
  http://10.97.114.181:8001/

Purpose:
  - Team project management
  - Store-level collaboration
  - Project tracking and reporting

Monitoring:
  - Included in daily health checks
  - Alerts if port 8001 not listening
  - Status reported in daily emails

Integration:
  - Monitored by MONITOR_AND_REPORT.ps1
  - Included in status dashboard
  - Email notifications on offline status

Note: Currently uses existing startup process
      Not automated restart (standalone service)
```

### V.E.T. Dashboard
```
Service Name:    V.E.T. (Vendor/Executive/Tracking) Dashboard
Backend File:    Store Support/Projects/VET_Dashboard/backend.py
Framework:       Flask with BigQuery
Port:            5001
Status:          Running (monitored)

Access URLs:
  Dashboard:  http://localhost:5001/vet_dashboard.html
  API Base:   http://localhost:5001/api/
  Data:       http://localhost:5001/api/data

Data Source:
  - Google Cloud BigQuery
  - Project: wmt-assetprotection-prod
  - Dataset: Store_Support_Dev
  - Table: Output- TDA Report

Features:
  - Executive report view
  - Implementation week tracking
  - Dallas POC focus
  - PowerPoint export via PPT service
  - CSV export

API Endpoints:
  GET /api/data           - All project data (with filters)
  GET /api/phases         - Distinct phase list
  GET /api/health-statuses - Distinct health status list
  GET /api/ownerships     - Distinct ownership list
  GET /api/titles         - Distinct title list
  GET /api/export/csv     - CSV export

Log File:
  - Store Support/Projects/VET_Dashboard/vet_dashboard_server.log

Auto-Restart Launcher:
  - Automation/start_vet_dashboard_24_7.bat

Health Check:
  - Monitored daily (6 AM)
  - Manual check: netstat -ano | findstr ":5001.*LISTENING"
```

### Store Meeting Planner
```
Service Name:    Store Meeting Planner API
Backend File:    Store Support/Projects/AMP/Store Meeting Planners/backend/main.py
Framework:       FastAPI with BigQuery
Port:            8090
Status:          Running (monitored)

Access URLs:
  Local:       http://localhost:8090/
  API Base:    http://localhost:8090/api/
  Health:      http://localhost:8090/api/health
  Frontend:    http://localhost:8090/ (served as static files)

Data Source:
  - Google Cloud BigQuery (AMP data via amp_ingestion.py)

Features:
  - Store meeting planning and scheduling
  - AMP data sync
  - File upload support
  - Meeting tracker report

Log File:
  - Store Support/Projects/AMP/Store Meeting Planners/backend/meeting_planner_server.log

Auto-Restart Launcher:
  - Automation/start_meeting_planner_24_7.bat

Health Check:
  - Monitored daily (6 AM)
  - Manual check: netstat -ano | findstr ":8090.*LISTENING"
```

---

## Quick Access Table

| Service | Port | Local Access | Network Access | Type |
|---------|------|--------------|----------------|------|
| Job Codes | 8080 | 127.0.0.1:8080 | 10.97.114.181:8080 | ✅ Monitored |
| Projects | 8001 | 127.0.0.1:8001 | 10.97.114.181:8001 | ✅ Monitored |
| TDA Insights | 5000 | localhost:5000 | VPN Required | ✅ Auto-Restart |
| AMP Dashboard | 8081 | localhost:8081 | VPN Required | ✅ Auto-Restart |
| Zorro | 8888 | localhost:8888 | VPN Required | ✅ Auto-Restart |
| V.E.T. Dashboard | 5001 | localhost:5001 | VPN Required | ✅ Auto-Restart |
| Store Meeting Planner | 8090 | localhost:8090 | VPN Required | ✅ Auto-Restart |

---

## Environment Variables

### TDA Insights & Store Dashboard
```
GOOGLE_APPLICATION_CREDENTIALS = %APPDATA%\gcloud\application_default_credentials.json
GCP_PROJECT_ID = wmt-assetprotection-prod
BIGQUERY_DATASET = Store_Support_Dev
```

### Zorro
```
No special environment variables required
(Uses same Python environment as others)
```

---

## Firewall & Port Requirements

### Windows Firewall
All services require these ports open (if using Windows Firewall):
- Port 8080 (Job Codes only)
- Port 8001 (Projects)
- Port 5000 (TDA)
- Port 8081 (Store Activity Dashboard)
- Port 8888 (Zorro)

### Network Access
- Job Codes & Projects: Use IP address (10.97.114.181) - more reliable
- TDA, Store Dashboard, Zorro: localhost only or configure network access

### Hostname DNS Issue
- Hostname `leus62315243171.homeoffice.wal-mart.com` resolves to wrong IP (10.97.108.66)
- Job Codes actually runs on 10.97.114.181
- **Solution:** Use IP address directly (already implemented)

---

## Performance Monitoring

### Port Availability Check
```powershell
# Check all Activity Hub ports
$ports = 5000, 8001, 8080, 8888
foreach ($port in $ports) {
    $listening = netstat -ano | Select-String ":$port.*LISTENING"
    Write-Host "Port $port : $(if($listening) { 'LISTENING' } else { 'NOT LISTENING' })"
}
```

### Service Status Report
```powershell
# Run full monitoring
C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\MONITOR_AND_REPORT.ps1
```

### Process Verification
```powershell
# Check Python processes
Get-Process python | Select-Object Id, ProcessName, @{
    Name="Memory";
    Expression={"{0:N0} MB" -f ($_.WorkingSet / 1MB)}
}
```

---

## Troubleshooting by URL

### Can't access http://localhost:5000/dashboard.html
- Check if TDA Insights backend is running
- Verify port 5000 is listening: `netstat -ano | findstr ":5000"`
- Check log file: `Store Support/Projects/TDA Insights/tda_insights_server.log`
- Restart: `& "Automation/start_tda_insights_24_7.bat"`

### Can't access http://localhost:8888/
- Check if Zorro is running
- Verify port 8888 is listening: `netstat -ano | findstr ":8888"`
- Check log file: `Store Support/Projects/AMP/Zorro/zorro_server.log`
- Restart: `& "Automation/start_zorro_24_7.bat"`

### Can't access http://10.97.114.181:8080/
- Check if Job Codes is running: `netstat -ano | findstr ":8080"`
- Check scheduled task: `Get-ScheduledTask "JobCodes-Backend-Server"`
- Verify IP is correct (should be 10.97.114.181, not 10.97.108.66)
- Check network connectivity to machine

### Can't access http://localhost:5001/vet_dashboard.html
- Check if V.E.T. Dashboard backend is running
- Verify port 5001 is listening: `netstat -ano | findstr ":5001"`
- Check log file: `Store Support/Projects/VET_Dashboard/vet_dashboard_server.log`
- Restart: `& "Automation/start_vet_dashboard_24_7.bat"`

### Can't access http://localhost:8090/
- Check if Store Meeting Planner is running
- Verify port 8090 is listening: `netstat -ano | findstr ":8090"`
- Check log file: `Store Support/Projects/AMP/Store Meeting Planners/backend/meeting_planner_server.log`
- Restart: `& "Automation/start_meeting_planner_24_7.bat"`

### Port 8081 Assignment (Store Activity Dashboard)
- Store Activity Dashboard exclusively uses port 8081
- Can run simultaneously with Job Codes (which uses port 8080)
- Access: http://localhost:8081/
- If Store Dashboard won't start, check if port 8081 is available: `netstat -ano | findstr ":8081"`

---

## Support & Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| Extended Checks | `Automation/EXTENDED_HEALTH_CHECKS_README.md` | Health check details |
| Quick Reference | `Automation/QUICK_REFERENCE_SERVICES.md` | Service overview |
| This Document | `Automation/SERVICE_URLs_ACCESS.md` | URL and access guide |
| Job Codes Guide | `JOBCODES_ACCESS_GUIDE.md` | Job Codes specific info |
| Task Restoration | `RESTORE_ALL_TASKS_NOW.ps1` | Restore all scheduled tasks |
| System Monitor | `MONITOR_AND_REPORT.ps1` | Health check and email |

---

**Last Updated:** March 12, 2026  
**Computer:** WEUS42608431466  
**Administrator:** Kendall Rush  
**Next Review:** March 19, 2026
