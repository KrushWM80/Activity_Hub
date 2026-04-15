# PID Manager - Safe Service Management

## Problem Solved

❌ **OLD WAY** (dangerous):
```powershell
Get-Process -Name python | Stop-Process -Force
```
Kills **ALL Python processes** on your machine — including Job Codes, VET Dashboard, AMP, etc.

✅ **NEW WAY** (safe):
```powershell
cd "Activity_Hub"
& ".\pid_manager.ps1" -Action stop -Service activity-hub
```
Kills **ONLY** the Activity Hub server using saved process ID.

---

## Quick Commands

### Start/Stop Activity Hub
```powershell
# PowerShell
cd "Activity_Hub"
& ".\pid_manager.ps1" -Action start -Service activity-hub
& ".\pid_manager.ps1" -Action stop -Service activity-hub

# OR use batch files
Interface\start_activity_hub_safe.bat
Interface\stop_activity_hub_safe.bat
```

### Start/Stop All Services
```powershell
cd "Activity_Hub"
& ".\pid_manager.ps1" -Action start -Service all
& ".\pid_manager.ps1" -Action stop -Service all
```

### Check Status of All Services
```powershell
cd "Activity_Hub"
& ".\pid_manager.ps1" -Action status -Service all
```

### Clean Up Stale PID Files
```powershell
cd "Activity_Hub"
& ".\pid_manager.ps1" -Action clean
```

---

## Individual Services

### Activity Hub (Port 8088)
```powershell
& ".\pid_manager.ps1" -Action start -Service activity-hub
& ".\pid_manager.ps1" -Action stop -Service activity-hub
```

### Job Codes Teaming (Port 8080)
```powershell
& ".\pid_manager.ps1" -Action start -Service job-codes
& ".\pid_manager.ps1" -Action stop -Service job-codes
```

### AMP Backend (Port 8081)
```powershell
& ".\pid_manager.ps1" -Action start -Service amp
& ".\pid_manager.ps1" -Action stop -Service amp
```

### Projects in Stores (Port 8001)
```powershell
& ".\pid_manager.ps1" -Action start -Service projects-stores
& ".\pid_manager.ps1" -Action stop -Service projects-stores
```

### V.E.T. Dashboard (Port 5001)
```powershell
& ".\pid_manager.ps1" -Action start -Service vet
& ".\pid_manager.ps1" -Action stop -Service vet
```

---

## How It Works

1. **Start Service**: Creates a `.pid_tracker/<service>.pid` file with the process ID
2. **Stop Service**: Reads the PID file and kills ONLY that specific process
3. **Status**: Shows which services are running with memory/CPU info
4. **Clean**: Removes stale PID files for dead processes

---

## PID Files Location

All PIDs stored in: `Activity_Hub\.pid_tracker\`

Files:
- `activity-hub.pid` (Activity Hub server)
- `job-codes.pid` (Job Codes dashboard)
- `amp.pid` (AMP backend)
- `projects-stores.pid` (Projects in Stores)
- `vet.pid` (V.E.T. Dashboard)

---

## Emergency: Kill All Activity Hub Services Only

Instead of:
```powershell
# ❌ NEVER DO THIS
Get-Process python | Stop-Process -Force
```

Use:
```powershell
# ✅ SAFE - Only kills Activity Hub services
cd Activity_Hub
& ".\pid_manager.ps1" -Action stop -Service all
```

---

## Notes

- **No more blanket kills**: Each service is tracked independently by PID
- **Other platforms safe**: Job Codes, VET, AMP, etc. run independently
- **Auto-cleanup**: If a process crashes, the PID file is cleaned up automatically
- **Status reporting**: See which services are actually running and their resource usage
