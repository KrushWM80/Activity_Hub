# 🚀 PROJECTS IN STORES - QUICK START

## 📂 What's in This Folder

This folder contains everything you need to manage Projects in Stores server processes.

---

## 🎯 Three Essential Files

### 1️⃣ **restart_everything.bat** ⭐ START HERE
   **Purpose:** One-click restart of ALL services in the correct order
   
   **How to use:**
   - Double-click the file
   - PowerShell window will open automatically
   - Wait 3-5 seconds for startup messages
   - Access dashboard at `http://localhost:8001`
   
   **What it does:**
   1. Stops any existing processes on port 8001
   2. Starts Keep-Awake service (background)
   3. Starts Projects in Stores backend on port 8001
   4. Shows server console output
   
   ✅ **Recommended for:** Daily restarts, troubleshooting

---

### 2️⃣ **check_status.ps1** 
   **Purpose:** View what's currently running and what's not
   
   **How to use:**
   ```powershell
   # Option A: Double-click in File Explorer (if running as Admin)
   # Option B: Run in PowerShell
   .\check_status.ps1
   ```
   
   **Shows:**
   - Keep-Awake Service status ✅/❌
   - Backend Server status ✅/❌
   - Quick action commands if something is down
   
   ✅ **Recommended for:** Quick health check before using dashboard

---

### 3️⃣ **STARTUP_GUIDE.md**
   **Purpose:** Comprehensive documentation with detailed troubleshooting
   
   **Contains:**
   - Visual diagram of what should be running
   - Step-by-step manual restart instructions
   - Troubleshooting guide for common issues
   - Quick command reference
   - Verification checklist
   
   ✅ **Recommended for:** Learning, advanced troubleshooting

---

## ⚡ "I Just Want to Restart Everything"

**Simple answer:** Double-click `restart_everything.bat`

That's it. It handles everything.

---

## 📋 What Should Be Running Automatically

After system restart, these should auto-start:

| Service | Status | Port | Where |
|---------|--------|------|-------|
| Keep Computer Awake | Auto-start | — | Windows Task Scheduler |
| Projects in Stores Backend | Auto-start | 8001 | Windows Task Scheduler |

Both are configured to start on Windows boot. If they stop, use `restart_everything.bat` to restart them.

---

## 🌐 Access Your Dashboard

**Local Computer:**
```
http://localhost:8001
```

**From Other Network Computers:**
```
http://weus42608431466.homeoffice.wal-mart.com:8001
```

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| Server won't start | Run `restart_everything.bat` |
| Don't know what's running | Run `check_status.ps1` |
| Need detailed info | Read `STARTUP_GUIDE.md` |
| Forgot the commands | See next section ↓ |

---

## 📖 Quick Reference Commands

```powershell
# Check what's running
.\check_status.ps1

# Restart everything
.\restart_everything.bat

# Check if port 8001 is in use
netstat -ano | findstr 8001

# View scheduled tasks
Get-ScheduledTask -TaskPath "\Activity Hub\"

# Restart just the backend
Restart-ScheduledTask -TaskName "Projects in Stores Server 24/7"
```

---

## 🎓 How It All Works

### **Startup Sequence**
```
1. Windows starts
   ↓
2. Task Scheduler runs "Keep Computer Awake 24/7"
   ↓
3. System keeps running (prevents sleep)
   ↓
4. Task Scheduler runs "Projects in Stores Server 24/7"
   ↓
5. Backend starts on http://localhost:8001
   ↓
6. Dashboard is ready to use ✅
```

### **File Locations**
```
Keep-Awake Script:
  C:\Users\krush\Documents\keep-awake.ps1

Projects in Stores Backend:
  Store Support\Projects\Intake Hub\ProjectsinStores\backend\main.py

Configuration:
  Both configured in Windows Task Scheduler
  → Path: Task Scheduler Library → Activity Hub
```

---

## ✅ Verification Checklist

After restarting, verify:
- [ ] `check_status.ps1` shows both services as ✅ Running
- [ ] Dashboard loads at `http://localhost:8001`
- [ ] No PowerShell error messages
- [ ] You can search/filter projects in the dashboard

---

## 🔧 Need Help?

1. **Quick status check:** `check_status.ps1`
2. **Full restart:** `restart_everything.bat`
3. **Detailed guide:** `STARTUP_GUIDE.md`
4. **Advanced troubleshooting:** See "🔧 Troubleshooting" section in `STARTUP_GUIDE.md`

---

**Location:** `Store Support\Projects\Intake Hub\ProjectsinStores\`  
**Last Updated:** February 25, 2026  
**Status:** ✅ Production Ready
