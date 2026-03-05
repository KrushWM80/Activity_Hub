# Activity Hub Operations Dashboard

**Last Updated:** March 5, 2026  
**Environment:** Windows 10/11  
**Python Environments:** .venv (root), System Python

---

## 🎯 Quick Status Check

Run this PowerShell command for instant service status:
```powershell
# Check all critical services
$services = @(
    @{name="Projects in Stores Backend"; port=8001; path="Store Support/Projects/Intake Hub/Intake Hub/ProjectsinStores/backend"},
    @{name="TDA Insights Backend"; port=5000; path="Store Support/Projects/TDA Insights"}
)

foreach ($svc in $services) {
    $conn = netstat -ano | Select-String ":$($svc.port).*LISTENING"
    if ($conn) { Write-Host "[✓] $($svc.name) - RUNNING on port $($svc.port)" -ForegroundColor Green }
    else { Write-Host "[✗] $($svc.name) - STOPPED" -ForegroundColor Red }
}
```

---

## 📋 Services Matrix

### Critical Services (Must Run 24/7)

| **Service** | **Port** | **Technology** | **Status** | **Start Command** | **Dependencies** |
|---|---|---|---|---|---|
| **Projects in Stores Backend** | 8001 | Flask + SQLite | ❌ | See [Startup Guide](#startup-guide) | Python 3, .venv |
| **TDA Insights Dashboard** | 5000 | Flask + BigQuery | ❌ | See [Startup Guide](#startup-guide) | Python 3, gcloud CLI, BigQuery Auth |
| **TDA Insights PPT Generator** | (5000) | python-pptx | ❌ | Runs as part of 5000 | TDA Insights Backend |

### Supporting Services (Background Tasks)

| **Service** | **Type** | **Schedule** | **Purpose** | **Status** |
|---|---|---|---|---|
| **24/7 Backend Server** | Scheduled Task | Always (BatchJob) | Keep Projects in Stores running | ❌ |
| **Database Cache Validator** | Python Script | On-demand | Validate cache integrity | Manual |
| **BigQuery Sync** | Python Script | Daily (8 AM) | Refresh TDA data | Manual |
| **Voice Engine Monitor** | PowerShell | On-demand | Check TTS voice status | Manual |

---

## 🚀 Startup Guide

### Prerequisites (One-Time Setup)

```powershell
# 1. Verify Python environments
& "C:\Users\krush\.venv\Scripts\python.exe" --version
& "C:\Users\krush\AppData\Local\Python\bin\python.exe" --version

# 2. Configure Google Cloud authentication
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"

# 3. Verify all dependencies are installed
& "C:\Users\krush\AppData\Local\Python\bin\python.exe" -m pip list | grep -E "flask|google-cloud|pptx"
```

### Startup Sequence (After System Restart)

**Step 1: Clear Ports (5 seconds)**
```powershell
# Kill any orphaned processes
Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3
netstat -ano | Select-String "8001|5000"  # Should show nothing
```

**Step 2: Start TDA Insights Backend (30-60 seconds to initialize)**
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\TDA Insights"
Write-Host "Starting TDA Insights on port 5000..." -ForegroundColor Cyan
& "C:\Users\krush\AppData\Local\Python\bin\python.exe" backend_simple.py
# Wait for: "Running on http://127.0.0.1:5000"
```

**Step 3: (NEW TERMINAL) Start Projects in Stores Backend**
```powershell
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend"
Write-Host "Starting Projects in Stores on port 8001..." -ForegroundColor Green
& "C:\Users\krush\.venv\Scripts\python.exe" main.py
# Wait for: "Running on http://127.0.0.1:8001"
```

**Step 4: Verify Both Services**
```powershell
# In a third terminal
Start-Sleep -Seconds 5
Write-Host "=== SERVICE VERIFICATION ===" -ForegroundColor Yellow

# Test TDA Insights
try {
    $resp = Invoke-WebRequest -Uri "http://localhost:5000/api/data" -Method Get -UseBasicParsing
    Write-Host "[✓] TDA Insights responding on port 5000" -ForegroundColor Green
} catch {
    Write-Host "[✗] TDA Insights not responding" -ForegroundColor Red
}

# Test Projects in Stores
try {
    $resp = Invoke-WebRequest -Uri "http://localhost:8001/api/health" -Method Get -UseBasicParsing
    Write-Host "[✓] Projects in Stores responding on port 8001" -ForegroundColor Green
} catch {
    Write-Host "[✗] Projects in Stores not responding" -ForegroundColor Red
}
```

---

## 🔄 Service Startup Automation

### Scheduled Task Setup (Windows Task Scheduler)

**Task 1: Auto-start Projects in Stores Backend**
```powershell
# Run as Administrator
$action = New-ScheduledTaskAction -Execute "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\start_server_24_7.bat"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity Hub - Projects in Stores Server" -Action $action -Trigger $trigger -Principal $principal
```

**Task 2: Auto-start TDA Insights Backend**
```powershell
# Create batch file: start_tda_insights_24_7.bat
@echo off
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\TDA Insights"
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json
"C:\Users\krush\AppData\Local\Python\bin\python.exe" backend_simple.py >> tda_insights.log 2>&1

# Then register task
$action = New-ScheduledTaskAction -Execute "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\start_tda_insights_24_7.bat"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity Hub - TDA Insights Server" -Action $action -Trigger $trigger -Principal $principal
```

---

## 📊 Port Mapping Reference

| **Port** | **Service** | **URL** | **Purpose** |
|---|---|---|---|
| **5000** | TDA Insights | http://localhost:5000 | Dashboard, BigQuery data, PPT generation |
| **8001** | Projects in Stores | http://localhost:8001 | Admin panel, project tracking, reports |
| **(reserved)** | Future services | - | - |

---

## 🔧 Troubleshooting

### Port Already in Use

```powershell
# Find process using port
$port = 8001
$process = netstat -ano | Select-String ":$port" | ForEach-Object { $_ -split '\s+' | Select-Object -Last 1 }
if ($process) {
    Write-Host "Port $port is used by PID $process"
    taskkill /PID $process /F
}
```

### Service Not Responding

```powershell
# 1. Check logs
Get-Content "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\TDA Insights\tda_insights.log" -Tail 50

# 2. Clear cache and restart
Remove-Item "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db" -Force -ErrorAction SilentlyContinue
```

### BigQuery Authentication Failed

```powershell
# Verify credentials
Test-Path "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"

# Re-authenticate
gcloud auth application-default login
gcloud config set project wmt-assetprotection-prod
```

---

## 📁 File Organization Issues (TO BE RESOLVED)

### Current Problem
**~80 Python/PowerShell files scattered in root Activity Hub folder**

### Organization Plan

**Files to Move to Zorro Project:**
- All voice/TTS related (`check_jenny_*.py`, `generate_podcast_*.py`, etc.)
- Audio processing scripts (`audio_pipeline.py`, `sapi5_engine.py`, `windows_media_engine.py`)
- Destination: `Store Support/Projects/AMP/Zorro/scripts/` or subfolder

**Files to Move to JobCodes-teaming:**
- Job code analysis scripts (`query_jobcodes_*.py`, `analyze_*_jobcodes.py`, etc.)
- Role mapping scripts (`step1_`, `step2_`, `step3_`)
- Destination: `Store Support/Projects/JobCodes-teaming/Job Codes/scripts/`

**Files to Move to TDA Insights:**
- BigQuery/Polaris queries (`query_*.py`, `search_*.py`)
- Destination: `Store Support/Projects/TDA Insights/scripts/`

**Files to Keep in Root (Core Activity Hub):**
- `setup_24_7_service.ps1` - Startup automation
- `start_server_24_7.bat` - Server launcher
- `test_system_capabilities.ps1` - System validation

---

## 🔍 Monitoring & Health Check

### Create Health Check Script

Save as `HEALTH_CHECK.ps1`:
```powershell
function Get-ServiceStatus {
    Write-Host "`n=== ACTIVITY HUB HEALTH STATUS ===" -ForegroundColor Cyan
    Write-Host "Time: $(Get-Date)" -ForegroundColor Gray
    
    # Check Port 5000
    $port5000 = netstat -ano | Select-String ":5000.*LISTENING"
    if ($port5000) { Write-Host "[✓] Port 5000 (TDA Insights)" -ForegroundColor Green }
    else { Write-Host "[✗] Port 5000 (TDA Insights) - OFFLINE" -ForegroundColor Red }
    
    # Check Port 8001
    $port8001 = netstat -ano | Select-String ":8001.*LISTENING"
    if ($port8001) { Write-Host "[✓] Port 8001 (Projects in Stores)" -ForegroundColor Green }
    else { Write-Host "[✗] Port 8001 (Projects in Stores) - OFFLINE" -ForegroundColor Red }
    
    # Check Scheduled Tasks
    $task1 = Get-ScheduledTask -TaskName "Activity Hub - Projects in Stores Server" -ErrorAction SilentlyContinue
    if ($task1.State -eq "Ready") { Write-Host "[✓] Scheduled Task: Projects in Stores" -ForegroundColor Green }
    else { Write-Host "[✗] Scheduled Task: Projects in Stores - NOT CONFIGURED" -ForegroundColor Red }
    
    # Check Google Cloud Auth
    $gcloud = Test-Path "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"
    if ($gcloud) { Write-Host "[✓] Google Cloud Credentials" -ForegroundColor Green }
    else { Write-Host "[✗] Google Cloud Credentials - MISSING" -ForegroundColor Red }
    
    Write-Host "====================================`n" -ForegroundColor Cyan
}

Get-ServiceStatus
```

---

## � Operational Scripts Reference

These supporting scripts enhance Activity Hub operations. Reference them here for easy lookup:

### MOVE_FILES.ps1 - File Reorganization
**Location:** Root Activity Hub folder  
**Purpose:** Reorganize scattered files into project-specific directories  
**Usage:**
```powershell
# Test changes without executing
.\MOVE_FILES.ps1 -DryRun -Confirm:$false

# Execute file reorganization
.\MOVE_FILES.ps1 -Confirm:$false
```
**See also:** [QUICK_START_FILE_REORGANIZATION.md](./QUICK_START_FILE_REORGANIZATION.md)

---

### start_server_24_7.bat - Service Startup
**Location:** Root Activity Hub folder  
**Purpose:** Start both backend services simultaneously (Projects in Stores + TDA Insights)  
**Usage:**
```powershell
# From root Activity Hub folder
.\start_server_24_7.bat

# Or via PowerShell
Start-Process -FilePath ".\start_server_24_7.bat" -WindowStyle Normal
```
**Starts:**
- Projects in Stores backend (Port 8001, via .venv)
- TDA Insights backend (Port 5000, via AppData Python)

---

### test_system_capabilities.ps1 - System Verification
**Location:** Root Activity Hub folder  
**Purpose:** Verify system has all required tools and dependencies  
**Usage:**
```powershell
.\test_system_capabilities.ps1
```
**Verifies:**
- Python installations (system, .venv, AppData)
- gcloud CLI availability
- Google Cloud authentication status
- Required Python packages (flask, BigQuery, pptx, etc.)
- Network port availability (5000, 8001)

---

## �📝 Maintenance Checklist

- [ ] **After Each Reboot:** Run health check script
- [ ] **Weekly:** Check log files for errors
- [ ] **Monthly:** Review and update this operations guide
- [ ] **Quarterly:** Test disaster recovery (full restart)
- [ ] **As Needed:** Update service dependencies

---

## 📞 Quick Links

- [Projects in Stores Dashboard](http://localhost:8001)
- [TDA Insights Dashboard](http://localhost:5000)
- [Google Cloud Console](https://console.cloud.google.com/bigquery/project/wmt-assetprotection-prod)
- [File Organization Plan](./FILE_ORGANIZATION_PLAN.md)
- [Quick Start: Reorganization](./QUICK_START_FILE_REORGANIZATION.md)

---

**Need to reorganize files?** See [FILE_ORGANIZATION_PLAN.md](./FILE_ORGANIZATION_PLAN.md)  
**Reference scripts above** for MOVE_FILES.ps1, start_server_24_7.bat, and test_system_capabilities.ps1
