# 🚀 PROJECTS IN STORES - 24/7 OPERATION GUIDE

**Status:** ✅ Server is RUNNING on port 8001

---

## 📋 What Happened

The backend server **was not running 24/7** because the Windows Task Scheduler job was never created. 

### Why It Wasn't Working

The system has an established methodology for 24/7 operation:
1. **Windows Task Scheduler** should automatically start the server at system boot
2. **start_server_24_7.bat** runs the server with automatic restart on crashes
3. **check_status.ps1** verifies the system is working

However, the scheduled task "Projects in Stores Server 24/7" was **never registered in Windows Task Scheduler**, so the server only ran manually.

---

## ✅ IMMEDIATE FIX (Currently Applied)

The server is currently running:
- **Status**: ✅ RUNNING
- **Port**: 8001 (verified listening)
- **Process ID**: 42632
- **URL**: http://localhost:8001/admin.html

The server will **auto-restart** if it crashes due to the loop in `start_server_24_7.bat`.

---

## 🔧 PERMANENT 24/7 SETUP (One-Time Admin Task)

To make the server run 24/7 automatically on system startup, you need to create the Windows Task Scheduler job. This requires **Administrator privileges**.

### Option A: Automated Setup (Recommended)

1. **Right-click PowerShell** and select **"Run as Administrator"**
2. **Navigate** to the ProjectsinStores folder:
   ```powershell
   cd "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\ProjectsinStores\"
   ```
3. **Run** the setup script:
   ```powershell
   .\setup_24_7_auto_start.ps1
   ```

### Option B: Manual Setup (If Option A doesn't work)

1. **Right-click PowerShell** → "Run as Administrator"
2. **Copy and paste** this command:
   ```powershell
   schtasks /Create /TN "Projects in Stores Server 24/7" `
     /TR "cmd.exe /c 'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\start_server_24_7.bat'" `
     /SC ONSTART /RL HIGHEST /F
   ```

### Option C: Using Windows GUI

1. **Press Windows Key** → Search "Task Scheduler" → Open it
2. Click **"Create Task"** in the right panel
3. **Fill in these details:**
   - **Name**: `Projects in Stores Server 24/7`
   - **Description**: Automatically starts the Projects in Stores backend server 24/7 with auto-restart
4. **Triggers** tab:
   - Click **"New"**
   - Select **"At startup"**
   - Click **OK**
5. **Actions** tab:
   - Click **"New"**
   - **Program/script**: `cmd.exe`
   - **Add arguments**: `/c "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\start_server_24_7.bat"`
   - Click **OK**
6. **General** tab:
   - Check **"Run with highest privileges"**
7. Click **OK** at the bottom

### Verification

After setup, verify the task is working:

```powershell
.\check_status.ps1
```

You should see:
```
✅ Backend Task: RUNNING (Task Scheduler)
✅ Backend: RUNNING on port 8001
```

---

## 🔄 Daily Operations

### Starting the Server (if it's not running)

**Option 1: Automatic** (If scheduled task is set up)
- Just restart your computer, server starts automatically

**Option 2: Quick Manual Start**
Run this batch file:
```
.\restart_everything.bat
```

**Option 3: Full Manual Restart**
```powershell
cd "Store Support\Projects\Intake Hub\ProjectsinStores\backend"
..\..\..\..\..\..\.venv\Scripts\python.exe main.py
```

### Checking Status

```powershell
.\check_status.ps1
```

### Restarting the Server

```powershell
Restart-ScheduledTask -TaskName "Projects in Stores Server 24/7" -TaskPath "\Activity Hub\"
```

Or just kill the process and it will restart automatically (the batch file has auto-restart built in):
```powershell
Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | `
  Select-Object -ExpandProperty OwningProcess | `
  ForEach-Object { Stop-Process -Id $_ -Force }
```

---

## 📊 System Architecture (For Reference)

```
WINDOWS STARTUP
    ↓
Task Scheduler: "Projects in Stores Server 24/7"
    ↓
start_server_24_7.bat
    ↓
:loop
  → Run Python Main Server
  → If crashes → Wait 5 sec → Restart
  → Repeat forever
```

---

## 🐛 Troubleshooting

### Server Started But Won't Auto-Restart on Crash

**Cause**: The scheduled task isn't set up properly
**Fix**: Run Option A, B, or C above

### Task Scheduler Says "Access Denied"

**Cause**: Running without Administrator privileges
**Fix**: Right-click PowerShell → "Run as Administrator"

### Server Port 8001 in Use

**Clear it**:
```powershell
Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | `
  Select-Object -ExpandProperty OwningProcess | `
  ForEach-Object { Stop-Process -Id $_ -Force }
```

### Task Runs but Server Doesn't Start

**Check**:
1. Verify `start_server_24_7.bat` path is correct
2. Verify Python venv path is correct: `.venv\Scripts\python.exe`
3. Verify backend path: `Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\main.py`
4. Check Task Scheduler "Last Run Result" for error code

---

## 📝 Files Involved

```
Activity_Hub/
├── start_server_24_7.bat                          ✅ Server startup script
├── setup_24_7_service.ps1                         (Legacy - outdated paths)  
├── Store Support/Projects/Intake Hub/ProjectsinStores/
│   ├── backend/
│   │   ├── main.py                                ✅ Backend application
│   │   ├── admin-access.json                      ✅ Auth config
│   │   └── ...
│   ├── frontend/
│   │   └── admin.html                             ✅ Web interface
│   ├── check_status.ps1                           ✅ Status verification
│   ├── restart_everything.bat                     ✅ Manual restart
│   ├── setup_auto_startup.ps1                     (Outdated - wrong paths)
│   └── setup_24_7_auto_start.ps1                  ✅ NEW proper setup script
```

---

## ✨ Summary

- **Current Status**: ✅ Server running (PID 42632)
- **Permanent Fix**: Set up Windows Task Scheduler (requires admin)
- **Quick Commands**:
  - Status check: `.\check_status.ps1`
  - Start server: `.\restart_everything.bat`
  - Setup 24/7: Run setup script as Administrator

---

**Last Updated**: March 4, 2026  
**Server**: Projects in Stores Backend  
**Port**: 8001
