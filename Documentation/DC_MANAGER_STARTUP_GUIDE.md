# Activity Hub Complete Startup Guide

**Last Updated:** March 5, 2026  
**For:** Complete system startup after Windows restart

## 🎯 Complete Startup Checklist

This guide ensures all Activity Hub services are running after a system restart, including the new DC Manager Change Detection PayCycle automation system.

---

## 📋 Pre-Startup Verification (2 minutes)

Before starting services, verify the system is ready:

```powershell
# 1. Check if running in Administrator mode (recommended but not required for verification)
# 2. Verify PayCycle tasks are registered
Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"} | Measure-Object | Select-Object -ExpandProperty Count
# Expected output: 26

# 3. Check Python environments
python --version                    # System Python
& "$env:USERPROFILE\.venv\Scripts\python.exe" --version   # Root .venv
& "$env:LOCALAPPDATA\Python\bin\python.exe" --version     # AppData Python
```

---

## 🚀 Startup Sequence (After System Restart)

### **STEP 1: Verify & Recreate PayCycle Tasks (if needed)**

**Time: ~2-5 minutes**

Run this verification script:
```powershell
.\verify_paycycle_tasks.ps1
```

**What happens:**
- ✅ Checks if all 26 DC-EMAIL-PC-* tasks exist
- ✅ Displays next scheduled PayCycle execution
- ✅ Automatically recreates tasks if missing (requires Admin confirmation)

**Expected output:**
```
Current PayCycle tasks: 26/26
[✓] All 26 PayCycle tasks verified and active

Next PayCycle Execution:
  Task: DC-EMAIL-PC-03
  Time: 3/6/26 6:00:00 AM
```

**If tasks are missing:**
1. Verify output shows warning about missing tasks
2. Script will offer to recreate them automatically
3. Grant Administrator access when prompted
4. Wait for setup window to show completion

---

### **STEP 2: Run Health Check**

**Time: ~1 minute**

Run the comprehensive health check:
```powershell
.\HEALTH_CHECK.ps1
```

**What it checks:**
- Port 5000 (TDA Insights) - connectivity
- Port 8001 (Projects in Stores) - connectivity
- Scheduled tasks for background services
- Google Cloud authentication status
- DC Manager Change Detection tasks and schedule

**Expected output:**
```
=== ACTIVITY HUB HEALTH STATUS ===
Time: 3/5/2026 10:30:45 AM

[✓] Port 5000 (TDA Insights)
[✓] Port 8001 (Projects in Stores)
[✓] Scheduled Task: Projects in Stores
[✓] Google Cloud Credentials

--- DC Manager Change Detection ---
[✓] All 26 PayCycle tasks active
   Next send: DC-EMAIL-PC-03 on 3/6/26 6:00:00 AM
```

---

### **STEP 3: Start Backend Services (Manual or Automated)**

**Time: ~1-2 minutes for both to initialize**

#### **Option A: Automated Startup (Batch File)**

If configured, use the provided batch file:
```powershell
.\start_server_24_7.bat
```

This starts:
- Projects in Stores backend (Port 8001)
- TDA Insights backend (Port 5000)

#### **Option B: Manual Startup (Separate Terminals)**

**Terminal 1 - TDA Insights:**
```powershell
cd "Store Support\Projects\TDA Insights"
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"
& "C:\Users\krush\AppData\Local\Python\bin\python.exe" backend_simple.py
# Wait for: "Running on http://127.0.0.1:5000"
```

**Terminal 2 - Projects in Stores:**
```powershell
cd "Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend"
& "C:\Users\krush\.venv\Scripts\python.exe" main.py
# Wait for: "Running on http://127.0.0.1:8001"
```

---

### **STEP 4: Verify Services Are Responding**

**Time: ~1 minute**

```powershell
# Test TDA Insights
Invoke-WebRequest -Uri "http://localhost:5000/api/data" -Method Get | Select-Object StatusCode

# Test Projects in Stores
Invoke-WebRequest -Uri "http://localhost:8001/api/health" -Method Get | Select-Object StatusCode

# Both should return: StatusCode : 200
```

---

## 📊 System Status Dashboard

### PayCycle Email System

**Current Status:** ✅ READY

| **Component** | **Status** | **Details** |
|---|---|---|
| **Tasks Registered** | 26/26 | DC-EMAIL-PC-01 through DC-EMAIL-PC-26 |
| **Next Execution** | PC-03 | March 6, 2026 @ 6:00 AM |
| **Email Recipients** | 3 (Test) | Kristine Torres, Matthew Farnworth, Kendall Rush |
| **Tracking System** | Active | `paycycle_tracking.json` |
| **Management CLI** | Ready | `python manage_paycycle.py` |

### Backend Services

| **Service** | **Port** | **Command** | **Status** |
|---|---|---|---|
| **Projects in Stores** | 8001 | `main.py` from Intake Hub | See STEP 3B |
| **TDA Insights** | 5000 | `backend_simple.py` | See STEP 3B |
| **Google Cloud** | N/A | gcloud CLI | Pre-configured ✅ |

---

## ⚠️ Troubleshooting

### PayCycle Tasks Not Found After Restart

**Problem:** Health check shows 0/26 PayCycle tasks

**Solution:**
1. Run `verify_paycycle_tasks.ps1` (includes automatic recreation)
2. If that doesn't work, manually recreate:
   ```powershell
   cd "Store Support\Projects\DC to Store Change Management Emails"
   Start-Process powershell -ArgumentList "-NoExit -Command .\\setup_tasks_revised.ps1" -Verb RunAs
   ```

### Port Already in Use

**Problem:** "Port 8001 or 5000 already in use"

**Solution:**
```powershell
# Find and kill process using the port
netstat -ano | Select-String "8001"
taskkill /PID <PID> /F

# Or clear all Python processes
Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force
```

### Outlook Email Delivery Failing

**Problem:** PayCycle emails not being sent

**Solution:**
```powershell
# Verify Outlook COM is available
cd "Store Support\Projects\DC to Store Change Management Emails"
python check_outlook_accounts.py

# Check email tracking
python manage_paycycle.py recipients    # See current recipients
python manage_paycycle.py schedule      # See all PayCycles
```

### Google Cloud Credentials Missing

**Problem:** "GoogleCloudError: credentials not found"

**Solution:**
```powershell
# Re-authenticate
gcloud auth application-default login
gcloud config set project wmt-assetprotection-prod

# Restart TDA Insights backend
```

---

## 🔄 Automated Startup Configuration (Optional)

To make services start automatically on system restart:

### 1. Create Scheduled Task for PayCycle Verification

```powershell
# Run as Administrator
$action = New-ScheduledTaskAction -Execute "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\verify_paycycle_tasks.ps1"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity Hub - Verify PayCycle Tasks" -Action $action -Trigger $trigger -Principal $principal
```

### 2. Create Scheduled Task for Projects in Stores

```powershell
# Run as Administrator
$action = New-ScheduledTaskAction -Execute "START" -Argument "/D C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub start_server_24_7.bat"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity Hub - Services Startup" -Action $action -Trigger $trigger -Principal $principal
```

---

## ✅ Post-Startup Checklist

After following all steps, verify:

- [ ] PayCycle verification completed (26 tasks found)
- [ ] Health check shows all services [✓]
- [ ] Port 5000 responding to requests
- [ ] Port 8001 responding to requests
- [ ] Next PayCycle execution date visible
- [ ] Google Cloud credentials valid
- [ ] Can access dashboards:
  - [ ] http://localhost:5000 (TDA Insights)
  - [ ] http://localhost:8001 (Projects in Stores)

---

## 📞 Quick References

- **DC Manager Knowledge Base:** [KNOWLEDGE_BASE_PAYCYCLE_AUTOMATION.md](Store%20Support/Projects/DC%20to%20Store%20Change%20Management%20Emails/KNOWLEDGE_BASE_PAYCYCLE_AUTOMATION.md)
- **PayCycle Quick Start:** [INDEX_AND_QUICK_START.md](Store%20Support/Projects/DC%20to%20Store%20Change%20Management%20Emails/INDEX_AND_QUICK_START.md)
- **Operations Dashboard:** [Documentation/OPERATIONS_DASHBOARD.md](Documentation/OPERATIONS_DASHBOARD.md)
- **System Capabilities Check:** `.\test_system_capabilities.ps1`

---

## 📧 Next PayCycle Email

| **PayCycle** | **Date** | **Time** | **Status** |
|---|---|---|---|
| **PC 03** | 3/6/2026 | 6:00 AM | ⏰ NEXT - Scheduled |
| **PC 04** | 3/20/2026 | 6:00 AM | Scheduled |
| **PC 05** | 4/3/2026 | 6:00 AM | Scheduled |

**Monitor PayCycle Execution:** Check `paycycle_tracking.json` after each scheduled send time

---

**Questions?** See [Documentation/OPERATIONS_DASHBOARD.md](Documentation/OPERATIONS_DASHBOARD.md#troubleshooting) for detailed troubleshooting
