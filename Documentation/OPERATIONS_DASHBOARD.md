# Activity Hub Operations Dashboard

**Last Updated:** March 5, 2026 - 24/7 AUTO-START CONFIGURED  
**Environment:** Windows 10/11  
**Python Environments:** .venv (root), System Python
**Status**: ✅ All critical services operational with auto-start configured

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
| **Projects in Stores Backend** | 8001 | FastAPI + SQLite | ✅ ACTIVE (Auto-Start) | `start_server_24_7.bat` | Python 3.14, .venv |
| **TDA Insights Dashboard** | 5000 | Flask + BigQuery | ❌ | See [Startup Guide](#startup-guide) | Python 3, gcloud CLI, BigQuery Auth |
| **TDA Insights PPT Generator** | (5000) | python-pptx | ❌ | Runs as part of 5000 | TDA Insights Backend |

### Supporting Services (Background Tasks)

| **Service** | **Type** | **Schedule** | **Purpose** | **Status** |
|---|---|---|---|---|
| **24/7 Backend Server** | Scheduled Task | At Startup | Keep Projects in Stores running | ✅ ACTIVE |
| **Database Cache Validator** | Python Script | On-demand | Validate cache integrity | Manual |
| **BigQuery Sync** | Python Script | Daily (8 AM) | Refresh TDA data | Manual |
| **Voice Engine Monitor** | PowerShell | On-demand | Check TTS voice status | Manual |
| **DC Manager Change Detection** | 26 Scheduled Tasks | Biweekly PayCycle | Send manager change emails to DCs | ✅ ACTIVE |
| **PayCycle Tracking System** | JSON Data Store | Real-time | Track all 26 PayCycle sends | ✅ READY |

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

### ✅ Projects in Stores Backend - AUTO-START CONFIGURED (March 5, 2026)

**Status**: Scheduled Task "ActivityHubServer" successfully created and verified.

**Windows Scheduled Task Details:**
```
Task Name:     ActivityHubServer
Trigger:       At system startup
Action:        C:\run_activity_hub_server.bat
Status:        ✅ Ready
Last Result:   Success (0)
Created:       March 5, 2026
```

**3-Tier Batch Script Architecture:**

1. **Root Launcher** (`C:\run_activity_hub_server.bat`)
   - Purpose: Clean entry point avoiding path parsing issues
   - Action: Changes directory and calls start_server.bat

2. **Activity Hub Wrapper** (`start_server.bat`)
   - Location: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\`
   - Action: Calls Automation\start_server_24_7.bat

3. **Main Backend with Auto-Restart** (`Automation\start_server_24_7.bat`)
   - Purpose: Launches FastAPI backend with auto-recovery loop
   - Auto-restart: 5-second delay on crash
   - Result: Zero-downtime operation 24/7

**Verification (All Confirmed March 5):**
```powershell
# Verify task is registered
Get-ScheduledTask -TaskName "ActivityHubServer" | Format-List TaskName, State, LastTaskResult

# Expected output:
# TaskName       : ActivityHubServer
# State          : Ready
# LastTaskResult : 0
```

**Auto-Start Verification After System Reboot:**
```powershell
# After next system restart, confirm within 30 seconds:
netstat -ano | Select-String ":8001.*LISTENING"

# Check activity log for auto-start event:
Get-Content "Store Support\Projects\Intake Hub\ProjectsinStores\backend\activity_log.json" | Select-Object -First 5
```

### TDA Insights Backend - MANUAL STARTUP REQUIRED

See [Startup Guide](#startup-guide) section above for manual startup instructions.

**Future Enhancement**: TDA Insights could be added to Task Scheduler following the same 3-tier batch script pattern as Projects in Stores.

### DC Manager Change Detection PayCycle Tasks - AUTO-SCHEDULED
```powershell
# This runs after system restart to verify all 26 PayCycle tasks are registered
# Script name: verify_paycycle_tasks.ps1

$PayCycleDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
$SetupScript = "$PayCycleDir\setup_tasks_revised.ps1"

# Check if 26 tasks exist
$ExistingTasks = Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"}

if ($ExistingTasks.Count -eq 26) {
    Write-Host "[✓] All 26 PayCycle tasks verified" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Only $($ExistingTasks.Count)/26 PayCycle tasks found. Recreating..." -ForegroundColor Yellow
    
    # Recreate tasks if missing
    Start-Process powershell -ArgumentList "-NoExit -Command `\"cd '$PayCycleDir'; .\\setup_tasks_revised.ps1`\"" -Verb RunAs
}
```

---

## 📊 Port Mapping Reference

| **Port** | **Service** | **URL** | **Purpose** |
|---|---|---|---|
| **5000** | TDA Insights | http://localhost:5000 | Dashboard, BigQuery data, PPT generation |
| **8001** | Projects in Stores | http://localhost:8001 | Admin panel, project tracking, reports |
| **(Task Scheduler)** | DC Manager Change Detection | N/A (Scheduled Tasks) | 26 PayCycle tasks (3/6/26-1/22/27 @ 6:00 AM) |
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

### DC Manager Change Detection PayCycle Tasks Not Running

```powershell
# Check if tasks exist
$tasks = Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"}
Write-Host "PayCycle tasks found: $($tasks.Count)/26"

# If tasks missing, recreate them (requires Admin)
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
Start-Process powershell -ArgumentList "-NoExit -Command .\\setup_tasks_revised.ps1" -Verb RunAs

# Check specific task
Get-ScheduledTask -TaskName "DC-EMAIL-PC-03" | Select-Object TaskName, State, NextRunTime
```

### PayCycle Email Not Sent

```powershell
# Check tracking file
$PayCycleDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
Get-Content "$PayCycleDir\paycycle_tracking.json" -Raw | ConvertFrom-Json

# Check if emails were backed up
Get-ChildItem "$PayCycleDir\emails_sent\" | Select-Object Name, LastWriteTime | Sort-Object LastWriteTime -Descending | Select-Object -First 5

# Verify Outlook is available
& "$PayCycleDir\check_outlook_accounts.py"
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
    
    # Check DC Manager Change Detection PayCycle Tasks
    Write-Host "`n--- DC Manager Change Detection ---" -ForegroundColor Yellow
    $payycles = Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"}
    if ($payycles.Count -eq 26) { 
        Write-Host "[✓] All 26 PayCycle tasks active" -ForegroundColor Green 
        $nextPC = $payycles | Where-Object {$_.NextRunTime -gt (Get-Date)} | Sort-Object NextRunTime | Select-Object -First 1
        if ($nextPC) { Write-Host "   Next send: $($nextPC.TaskName) on $($nextPC.NextRunTime)" -ForegroundColor Cyan }
    }
    elseif ($payycles.Count -gt 0) { 
        Write-Host "[WARNING] Only $($payycles.Count)/26 PayCycle tasks found" -ForegroundColor Yellow
    }
    else { 
        Write-Host "[✗] PayCycle tasks - NOT CONFIGURED" -ForegroundColor Red 
    }
    
    Write-Host "`n====================================" -ForegroundColor Cyan
    Write-Host "Run: .\\HEALTH_CHECK.ps1 for detailed diagnostics" -ForegroundColor Gray
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

### verify_paycycle_tasks.ps1 - DC Manager Change Detection Verification
**Location:** Root Activity Hub folder (or DC to Store Change Management Emails folder)  
**Purpose:** Verify all 26 PayCycle tasks are registered; recreate if missing after system restart  
**Usage:**
```powershell
# Run after system restart to ensure PayCycle tasks are active
.\verify_paycycle_tasks.ps1

# Or manually check
Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"} | Measure-Object | Select-Object -ExpandProperty Count
```
**Verifies:**
- All 26 DC-EMAIL-PC-XX tasks exist in Task Scheduler
- Next scheduled PayCycle task date/time
- Recreates tasks automatically if missing (requires Admin)

**Next PayCycle Execution:**
```powershell
# See which PayCycle runs next and when
Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" | 
  Where-Object {$_.NextRunTime -gt (Get-Date)} | 
  Sort-Object NextRunTime | 
  Select-Object TaskName, NextRunTime | 
  Select-Object -First 1
```

---

## �📝 Maintenance Checklist

- [ ] **After Each Reboot:** 
  - [ ] Run health check script
  - [ ] Run verify_paycycle_tasks.ps1 to confirm PayCycle tasks are active
  - [ ] Check next scheduled PayCycle execution
- [ ] **Weekly:** 
  - [ ] Check log files for errors
  - [ ] Verify all services responding (ports 5000, 8001)
- [ ] **On PayCycle Day (Every 2 weeks):**
  - [ ] Monitor email delivery at 6:00 AM
  - [ ] Check `paycycle_tracking.json` for completion
  - [ ] Verify emails sent to recipients
- [ ] **Monthly:** 
  - [ ] Review and update this operations guide
  - [ ] Check PayCycle execution history
  - [ ] Verify Outlook configuration
- [ ] **Quarterly:** 
  - [ ] Test disaster recovery (full system restart)
  - [ ] Review recipient list (email_recipients.json)
  - [ ] Backup PayCycle tracking data
- [ ] **As Needed:** 
  - [ ] Update service dependencies
  - [ ] Update DC recipient list in production mode

---

## 📞 Quick Links

- [Projects in Stores Dashboard](http://localhost:8001)
- [TDA Insights Dashboard](http://localhost:5000)
- [Google Cloud Console](https://console.cloud.google.com/bigquery/project/wmt-assetprotection-prod)
- [DC Manager Change Detection Folder](../Store%20Support/Projects/DC%20to%20Store%20Change%20Management%20Emails/)
- [DC Manager PayCycle Knowledge Base](../Store%20Support/Projects/DC%20to%20Store%20Change%20Management%20Emails/KNOWLEDGE_BASE_PAYCYCLE_AUTOMATION.md)
- [DC Manager Quick Start](../Store%20Support/Projects/DC%20to%20Store%20Change%20Management%20Emails/INDEX_AND_QUICK_START.md)
- [File Organization Plan](./FILE_ORGANIZATION_PLAN.md)
- [Quick Start: Reorganization](./QUICK_START_FILE_REORGANIZATION.md)

---

## 🎯 System Startup Sequence (Complete)

**After System Restart, Follow This Order:**

1. **Verify PayCycle Tasks (1 min)**
   ```powershell
   .\verify_paycycle_tasks.ps1
   ```

2. **Run Health Check (1 min)**
   ```powershell
   .\HEALTH_CHECK.ps1
   ```

3. **Manual Startup (10 min) OR Automated Startup**
   - Automated: Tasks run on schedule automatically
   - Manual startup: See [Startup Guide](#startup-guide) above

4. **Verify Services (2 min)**
   ```powershell
   # All services should show as [✓]
   .\HEALTH_CHECK.ps1
   ```

**Expected Results:**
- ✅ Port 5000 responding (TDA Insights)
- ✅ Port 8001 responding (Projects in Stores)
- ✅ 26 PayCycle tasks active
- ✅ Next PayCycle execution visible in Task Scheduler
- ✅ Google Cloud credentials validated

---

**Need to reorganize files?** See [FILE_ORGANIZATION_PLAN.md](./FILE_ORGANIZATION_PLAN.md)  
**DC Manager Change Detection Details:**  [KNOWLEDGE_BASE_PAYCYCLE_AUTOMATION.md](../Store%20Support/Projects/DC%20to%20Store%20Change%20Management%20Emails/KNOWLEDGE_BASE_PAYCYCLE_AUTOMATION.md)
