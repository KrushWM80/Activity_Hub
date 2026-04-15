# ⚠️ MIGRATION GUIDE: Stop Using Blanket Kill Scripts

## The Problem

Your old scripts use:
```powershell
Get-Process -Name python | Stop-Process -Force
```

This **kills ALL Python processes** on your entire machine, including:
- ✅ Activity Hub services (intended)
- ❌ Job Codes Teaming (unintended)
- ❌ Projects in Stores (unintended)
- ❌ AMP Backend (unintended)
- ❌ V.E.T. Dashboard (unintended)
- ❌ Any other Python background services

## The Solution: PID Manager

| Task | Old Way ❌ | New Way ✅ |
|------|-----------|-----------|
| **Start Activity Hub** | `start_server.bat` (kills all Python first) | `start_activity_hub_safe.bat` |
| **Stop Activity Hub** | `Get-Process python \| Stop-Process -Force` | `stop_activity_hub_safe.bat` |
| **Check status** | Manually check task manager | `check_services_status.bat` |
| **Start all services** | Multiple .bat files, order matters | `start_all_services_safe.bat` |
| **Stop all services** | Dangerous blanket kill | `stop_all_services_safe.bat` |

## Files Created

### 1. Core System
- **`pid_manager.ps1`** — Main PID tracking engine
  - Tracks services by saved process ID
  - Reads/writes `.pid_tracker/<service>.pid` files
  - Only kills tracked processes by PID

### 2. Quick Scripts (Batch Files)
- **`Interface\start_activity_hub_safe.bat`** — Start Activity Hub only
- **`Interface\stop_activity_hub_safe.bat`** — Stop Activity Hub only
- **`start_all_services_safe.bat`** — Start all 5 services
- **`stop_all_services_safe.bat`** — Stop all 5 services
- **`check_services_status.bat`** — Show which services are running

### 3. Documentation
- **`PID_MANAGER_GUIDE.md`** — Full usage guide (you're reading related content)
- **`BLANKET_KILL_MIGRATION.md`** — This migration guide

## Migration Steps

### Step 1: Stop Using Old Kill Scripts

Find and disable/delete these patterns:
```powershell
❌ Get-Process -Name python | Stop-Process -Force
❌ Get-Process python | Stop-Process -Force 2>$null
```

Check these files:
- `Interface\start_server.bat`
- `deploy_*.ps1` scripts
- `create_tasks.bat`
- Any other `.bat` or `.ps1` files with blanket kills

### Step 2: Replace with Safe Alternatives

**Old script that kills all Python:**
```batch
@echo off
Get-Process -Name python | Stop-Process -Force 2>$null
Start-Sleep 2
cd Interface
python activity_hub_server.py
```

**New script (safe):**
```batch
@echo off
cd "%~dp0"
Interface\start_activity_hub_safe.bat
```

### Step 3: Test

```powershell
# Terminal 1: Start Activity Hub
start_activity_hub_safe.bat

# Terminal 2: Check status
check_services_status.bat

# Terminal 3: Verify other services still work
# Try accessing http://localhost:8001 (Projects in Stores)
# Or http://localhost:8080 (Job Codes)

# Terminal 2: Stop safely
stop_activity_hub_safe.bat

# Verify other services still running
check_services_status.bat
```

## FAQ

**Q: What if I need to stop OTHER services too?**
```powershell
cd Activity_Hub
& ".\pid_manager.ps1" -Action stop -Service job-codes
```

**Q: What if the PID file is stale?**
```powershell
cd Activity_Hub
& ".\pid_manager.ps1" -Action clean
```
Automatically removes PID files for dead processes.

**Q: Can I still use manual PowerShell commands?**
Yes! All scripts work in PowerShell:
```powershell
cd Activity_Hub
& ".\pid_manager.ps1" -Action status -Service all
```

**Q: What if my Activity Hub crashes?**
The next start will automatically detect the dead process and clean up the PID file before starting fresh.

**Q: Do I need to update scheduler tasks?**
Only if they use the blanket kill approach. Check:
- Windows Task Scheduler
- Any scheduled PowerShell scripts
- Batch files

## Locations to Update

Search your codebase for `Get-Process.*python` to find all places using blanket kills:

```
Files to check:
- Interface\start_server.bat
- Automation\*.bat
- Deploy\*.ps1
- Any .bat or .ps1 in root
- Check Windows Task Scheduler too!
```

## Commit Guidance

When you commit these changes:
- ✅ Add `pid_manager.ps1`
- ✅ Add `*_safe.bat` files  
- ✅ Add `PID_MANAGER_GUIDE.md`
- ✅ Delete old blanket-kill scripts (or mark deprecated)
- ✅ Update any docs referencing old methods

## Support

If a service doesn't start:
```powershell
cd Activity_Hub
& ".\pid_manager.ps1" -Action status -Service all
# Check detailed error above each service
```

Look for:
- Port already in use
- Missing dependencies
- Permission errors
