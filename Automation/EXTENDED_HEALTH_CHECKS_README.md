# Extended Health Checks & Auto-Restart - Configuration Summary

## Overview
Enhanced the MONITOR_AND_REPORT.ps1 monitoring script to include automated health checks and auto-restart capabilities for three additional services: TDA Insights, Store Activity Dashboard, and Zorro Podcast Server.

## Services Added to Health Checks

### 1. TDA Insights Dashboard
- **Location:** `Store Support/Projects/TDA Insights`
- **Backend File:** `backend_simple.py`
- **Port:** 5000
- **URL:** `http://localhost:5000/dashboard.html`
- **Purpose:** Store support data visualization with BigQuery integration
- **Auto-Restart:** Triggered by MONITOR_AND_REPORT.ps1 if port 5000 is offline
- **Batch File:** `Automation/start_tda_insights_24_7.bat`

### 2. Store Activity & Communication Dashboard (AMP)
- **Location:** `Store Support/Projects/AMP/Store Updates Dashboard`
- **Backend File:** `amp_backend_server.py`
- **Port:** 8080
- **URL:** `http://localhost:8080/`
- **Purpose:** Store communication platform with MP4 audio synthesis
- **Auto-Restart:** Triggered by MONITOR_AND_REPORT.ps1 if port 8080 is offline
- **Batch File:** `Automation/start_store_dashboard_24_7.bat`
- **Features:** 
  - BigQuery data access
  - Jenny neural voice integration
  - Audio summarization

### 3. Zorro Activity Hub - Podcast Server
- **Location:** `Store Support/Projects/AMP/Zorro`
- **Backend File:** `podcast_server.py`
- **Port:** 8888
- **URL:** `http://localhost:8888/`
- **Audio Generator:** `http://localhost:8888/create-audio`
- **Purpose:** Podcast and audio message platform with Jenny Neural voice
- **Auto-Restart:** Triggered by MONITOR_AND_REPORT.ps1 if port 8888 is offline
- **Batch File:** `Automation/start_zorro_24_7.bat`

## Enhanced Monitoring Features

### System Status Detection
The `Get-SystemStatus` function now detects:
- ✅ Job Codes running on port 8080
- ✅ Projects in Stores running on port 8001
- ✅ TDA Insights running on port 5000
- ✅ Store Activity Dashboard running on port 8081
- ✅ Zorro running on port 8888
- ✅ All 26 DC Manager PayCycle tasks
- ✅ Job Codes scheduled task configuration

### Auto-Restart Functions
New functions added:
1. **Check-And-RestartJobCodes()** - Restarts Job Codes via scheduled task
2. **Check-And-RestartTDA()** - Starts TDA Insights backend process
3. **Check-And-RestartZorro()** - Starts Zorro podcast server

Each function:
- Checks if service is running (via netstat port check)
- Starts the service if offline
- Verifies successful startup (port listening)
- Reports status to console
- Logs errors if restart fails

### Email Reporting
Daily emails now include:
- Status table with all 5 services (+ DC tasks)
- Individual port listening status
- Running vs Offline indicators
- Number of running services (X/5)
- Downtime detection with duration
- Complete access URLs for all services

## Batch File Details

### start_tda_insights_24_7.bat
- Runs `backend_simple.py` in auto-restart loop
- Logs to: `tda_insights_server.log`
- Enables Google Cloud credentials
- 5-second restart interval on crash

### start_store_dashboard_24_7.bat
- Runs `amp_backend_server.py` in auto-restart loop
- Logs to: `store_dashboard_server.log`
- Enables Google Cloud credentials
- Includes MP4 Pipeline support
- 5-second restart interval on crash

### start_zorro_24_7.bat
- Runs `podcast_server.py` in auto-restart loop
- Logs to: `zorro_server.log`
- Serves on port 8888
- Includes Jenny voice generation capabilities
- 5-second restart interval on crash

## Integration with Existing Automation

### Daily Monitoring (6 AM)
The scheduled task `ActivityHub-DailyStatus-6AM` now:
1. Checks all 5 services health
2. Auto-restarts any offline services
3. Sends comprehensive email report
4. Documents downtime if system was offline

### System Restart
The scheduled task `ActivityHub-Startup-Report` now:
1. Detects system restart
2. Checks all services immediately
3. Restarts any offline services
4. Sends startup notification email

### On-Demand Health Checks
Can be triggered manually via:
```powershell
PS> .\MONITOR_AND_REPORT.ps1
```

## Accessing Services

### From Inside the Network (Localhost)
- **TDA Insights:** http://localhost:5000/dashboard.html
- **Store Activity Dashboard:** http://localhost:8081/
- **Zorro Podcast Server:** http://localhost:8888/
- **Zorro Audio Generator:** http://localhost:8888/create-audio

### From Other Machines
- **Job Codes:** http://10.97.114.181:8080/static/index.html#
- **Projects in Stores:** http://10.97.114.181:8001/
- **TDA, Store Dashboard, Zorro:** Requires localhost forwarding or network configuration

## Next Steps

### Optional Scheduling Setup
To schedule auto-start of these services on system startup or specific times, you can:

1. **Manual Start from Command Line:**
   ```cmd
   start "" "%ProjectRoot%\Automation\start_tda_insights_24_7.bat"
   start "" "%ProjectRoot%\Automation\start_store_dashboard_24_7.bat"
   start "" "%ProjectRoot%\Automation\start_zorro_24_7.bat"
   ```

2. **Add to Windows Task Scheduler:**
   - Create scheduled tasks for each batch file
   - Set triggers: On system startup + Daily at specific times
   - Action: Run batch file with path variables

3. **Automated via RESTORE_ALL_TASKS_NOW.ps1:**
   - Add similar task definitions for TDA, Dashboard, and Zorro
   - Set multiple triggers (startup, daily, every N hours)

### Monitoring
The MONITOR_AND_REPORT.ps1 script will:
- ✅ Run daily at 6 AM
- ✅ Run on system startup
- ✅ Detect if services are offline
- ✅ Automatically restart offline services
- ✅ Email status report with all details
- ✅ Log all activities and errors

## Log Files Location

| Service | Log File |
|---------|----------|
| Job Codes | `Automation/jobcodes_server.log` |
| TDA Insights | `Store Support/Projects/TDA Insights/tda_insights_server.log` |
| Store Dashboard | `Store Support/Projects/AMP/Store Updates Dashboard/store_dashboard_server.log` |
| Zorro | `Store Support/Projects/AMP/Zorro/zorro_server.log` |
| System Monitor | `system_status.log` |

## Configuration Files

### Modified
- `MONITOR_AND_REPORT.ps1` - Enhanced with TDA, Store Dashboard, Zorro checks
- Email body now includes all services in status report

### Created
- `Automation/start_tda_insights_24_7.bat` - TDA auto-restart wrapper
- `Automation/start_store_dashboard_24_7.bat` - Store Dashboard auto-restart wrapper
- `Automation/start_zorro_24_7.bat` - Zorro auto-restart wrapper
- `Automation/EXTENDED_HEALTH_CHECKS_README.md` - This file

## Troubleshooting

### Service Not Restarting
1. Check log file for error messages
2. Verify Python executable path exists
3. Check Google Cloud credentials file exists (for TDA and Store Dashboard)
4. Verify port is not blocked by firewall

### Port Assignments
- TDA Insights uses port 5000 (Flask)
- Store Activity Dashboard uses port 8081 (Flask + BigQuery)
- Zorro uses unique port 8888 (HTTP Server)
- Job Codes uses unique port 8080 (FastAPI, IP-based access)
- **Note:** Each service has unique port assignment - access Job Codes via IP (10.97.114.181:8080), Store Dashboard via localhost (localhost:8081)

### Manual Restart
```powershell
# Kill running services
taskkill /F /IM python.exe

# Restart via batch files
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_tda_insights_24_7.bat"
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_store_dashboard_24_7.bat"
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_zorro_24_7.bat"
```

## Service Dependencies

- **Google Cloud SDK**: Required for TDA Insights and Store Dashboard (BigQuery)
- **MP4 Pipeline**: Required for Zorro and Store Dashboard (Jenny voice)
- **FFmpeg**: Required for audio synthesis
- **Python 3.x**: All services require Python runtime
- **Virtual Environment**: Uses .venv in Activity Hub root

---
**Last Updated:** March 12, 2026
**Monitor:** MONITOR_AND_REPORT.ps1 with Extended Health Checks
**Automation:** Task Scheduler with Daily 6 AM + Startup + Auto-Restart
