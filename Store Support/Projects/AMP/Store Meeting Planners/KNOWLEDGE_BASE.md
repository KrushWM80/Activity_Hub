# Store Meeting Planner - Knowledge Base

**Last Updated**: April 2, 2026

---

## Service Info

| Property | Value |
|----------|-------|
| **Port** | 8090 |
| **URL (local)** | http://localhost:8090/StoreMeetingPlanner |
| **URL (network)** | http://weus42608431466:8090/StoreMeetingPlanner |
| **Entry Point** | `backend/main.py` (FastAPI + Uvicorn) |
| **Framework** | FastAPI |

---

## ⚠️ Automation & Recovery

### Scheduled Tasks

| Task Name | Schedule | Purpose |
|-----------|----------|---------|
| `Activity_Hub_StoreMeetingPlanner_AutoStart` | On logon | Starts `start_meeting_planner_24_7.bat` → `main.py` on port 8090 |

### Bat Files (`Automation/`)
- `start_meeting_planner_24_7.bat` — Port-kill block + restart loop. Primary crash recovery (5-7 sec downtime)
- Log: `backend/meeting_planner_server.log`

### Recovery Layers
1. **Bat restart loop** — primary (5-7 sec recovery on crash)
2. **Continuous monitor** (`continuous_monitor.ps1`) — checks all 7 services every 5 min; only launches new bat if bat process is not already running

### ⚠️ Known Crash Issue (April 1, 2026)
The continuous monitor was launching a second copy of the bat while the first was between restarts. The second copy's port-kill block killed the first instance → death loop every 12 seconds. Fixed in `continuous_monitor.ps1` — now checks if bat process is already running before launching a new copy.

### ⚠️ NEVER use `Stop-Process -Name python`
This kills ALL Python processes on the machine — all 7 services go down.

**Safe way to restart only Meeting Planner (port 8090):**
```powershell
$p = (netstat -ano | Select-String ":8090.*LISTENING" | ForEach-Object { ($_ -split "\s+")[-1] }) | Select-Object -First 1
if ($p) { taskkill /F /PID $p }
# Bat loop restarts automatically within 5-7 seconds
```

### Adding/Changing This Service
If the port, entry point, or bat file changes, update ALL of:
1. `Automation/start_meeting_planner_24_7.bat`
2. `Automation/register_tasks_cmd.bat`
3. `continuous_monitor.ps1` services array
4. `MONITOR_AND_REPORT.ps1` services list
5. `Documentation/KNOWLEDGE_HUB.md` Active Services table
6. This file
