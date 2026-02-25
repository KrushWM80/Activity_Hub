# 🚀 Projects in Stores - Startup & Restart Guide

## What Should Be Running Automatically

```
┌─────────────────────────────────────────┐
│   🖥️  PROJECTS IN STORES SYSTEM         │
├─────────────────────────────────────────┤
│                                         │
│  ✅ Keep Computer Awake (24/7)         │
│     └─ Prevents system sleep           │
│        Location: C:\Users\krush\       │
│                  Documents\             │
│                  keep-awake.ps1        │
│        Task: "Keep Computer Awake 24/7"│
│                                         │
│  ✅ Projects in Stores Backend         │
│     └─ Web server on port 8001         │
│        Location: Store Support\        │
│                  Projects\Intake Hub\  │
│                  ProjectsinStores\     │
│        Task: "Projects in Stores       │
│              Server 24/7"              │
│                                         │
│  🌐 Access: http://localhost:8001      │
│             (or on-network URL)        │
│                                         │
└─────────────────────────────────────────┘
```

---

## ⚡ ONE-CLICK RESTART

### Option 1: Easy Batch File (Recommended)
Run this file to restart everything in the correct order:

**📁 File:** `restart_everything.bat`  
**Location:** `c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\ProjectsinStores\`

**How to use:**
1. Double-click `restart_everything.bat`
2. A PowerShell window will open
3. Wait 3-5 seconds for all processes to start
4. Access at `http://localhost:8001`

---

## 📋 Manual Restart (Step-by-Step)

If you need to restart manually or understand the process:

### Step 1: Kill Existing Processes
Open **Admin PowerShell** and run:
```powershell
# Stop port 8001 (Projects in Stores)
Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }

# Stop Keep-Awake instances
Stop-Process -Name "powershell" -Filter "keep-awake" -ErrorAction SilentlyContinue
Write-Host "✓ All processes stopped"
```

### Step 2: Start Keep-Awake
```powershell
# Start Keep-Awake (optional - only if system sleep is a concern)
Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File "C:\Users\krush\Documents\keep-awake.ps1"'
Write-Host "✓ Keep-Awake started"
```

### Step 3: Start Projects in Stores Backend
```powershell
# Navigate to backend
cd "Store Support\Projects\Intake Hub\ProjectsinStores\backend"

# Start server (using virtual environment)
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" main.py
# Wait for message: "Uvicorn running on http://0.0.0.0:8001"
```

### Step 4: Access Dashboard
Open browser and go to:
- **Local:** `http://localhost:8001`
- **On Network:** `http://weus42608431466.homeoffice.wal-mart.com:8001`

---

## ✅ Verification Checklist

After restart, verify everything is working:

- [ ] Keep-Awake is running (processes list shows `powershell keep-awake`)
- [ ] Backend is running on port 8001 (check with `netstat -ano | findstr 8001`)
- [ ] Dashboard loads at `http://localhost:8001`
- [ ] No error messages in PowerShell console

---

## 🔧 Troubleshooting

### Server Won't Start
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```powershell
# Reinstall dependencies
pip install fastapi uvicorn google-cloud-bigquery pandas openpyxl
```

### Port 8001 Already in Use
**Error:** `Address already in use`

**Solution:**
```powershell
# Kill the process using port 8001
Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }
```

### Keep-Awake Not Preventing Sleep
**Solution:** Keep-Awake task should auto-start on Windows restart. If not running:
```powershell
# Verify task exists
Get-ScheduledTask -TaskName "Keep Computer Awake 24/7"

# Run the batch file manually
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\start_keep_awake_24_7.bat"
```

### Can't Access on External URL
**Check:** Network connectivity and firewall
```powershell
# Verify backend is listening on all interfaces
netstat -ano | findstr 8001
# Should show: 0.0.0.0:8001 (not just 127.0.0.1)
```

---

## 📊 What Each Process Does

| Process | Purpose | Port | Auto-Start |
|---------|---------|------|-----------|
| **Keep-Awake** | Prevents Windows from sleeping | N/A | ✅ Yes (Task Scheduler) |
| **Projects Backend** | FastAPI web server + BigQuery | 8001 | ✅ Yes (Task Scheduler) |

---

## 🎯 Quick Command Reference

```powershell
# Check if port 8001 is in use
netstat -ano | findstr 8001

# Check scheduled tasks
Get-ScheduledTask -TaskPath "\Activity Hub\"

# View logs (if backend logs to file)
Get-Content "Store Support\Projects\Intake Hub\ProjectsinStores\logs\*.log" -Tail 50

# Restart just the backend
Restart-ScheduledTask -TaskName "Projects in Stores Server 24/7"

# Stop everything
Get-ScheduledTask -TaskPath "\Activity Hub\" | Disable-ScheduledTask
```

---

**Last Updated:** February 25, 2026  
**Status:** ✅ Production Ready  
**Server URL:** http://weus42608431466.homeoffice.wal-mart.com:8001/
