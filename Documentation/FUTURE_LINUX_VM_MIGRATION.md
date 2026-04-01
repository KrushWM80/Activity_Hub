# Future Phase: Linux VM Migration (Headless 24/7 Operation)

**Status**: Future Phase — Not Started  
**Goal**: Migrate Activity Hub services to Walmart Store Linux NextGen (Ubuntu) VMs for true headless operation (services survive reboots and power outages with zero manual login)

---

## Why

Current Windows setup requires a user login before services start (tasks are registered as `onlogon`). A power outage or reboot means services stay dark until someone physically logs in. Walmart Group Policy blocks registering tasks as SYSTEM on the Windows machine.

Linux VMs use `systemd` services which start automatically at boot — no login required.

---

## Step 1: Request System User (InfoSec)

Submit request via **ServiceNow → Unix-Linux Local Accounts and Access Management**

| Field | Value |
|-------|-------|
| Server PFX | TBD (e.g., `sin01`) |
| System Username | `svchub` or `svcactivityhub` |
| UID | Assigned by InfoSec |
| GID | Assigned by InfoSec |
| Shell | `/bin/bash` |
| Home Directory | `/u/users/svcactivityhub` |

→ Receive **RITM number** from InfoSec once fulfilled.

---

## Step 2: Deployment Approval (Store Linux)

Submit to **Store Linux deployment approval Jira Service Desk** with:
- Server PFX
- System Username, UID, GID, Shell, Home Directory
- RITM from InfoSec
- Secondary groups (if needed: `devops`, `analytics`)

---

## Step 3: Verify User on VM

```bash
getent passwd svcactivityhub
# Confirm UID, GID, shell, home directory match request
```

---

## Step 4: Migrate Services

Each service gets a `systemd` unit file replacing the Windows bat file.

**Example — TDA Insights (port 5000):**
```ini
# /etc/systemd/system/activity-hub-tda.service
[Unit]
Description=Activity Hub TDA Insights
After=network.target

[Service]
User=svcactivityhub
WorkingDirectory=/opt/activity_hub/Platform
ExecStart=/opt/activity_hub/.venv/bin/python tda_server.py
Restart=always
RestartSec=5
Environment=GOOGLE_APPLICATION_CREDENTIALS=/opt/activity_hub/credentials.json

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable activity-hub-tda
sudo systemctl start activity-hub-tda
```

**Services to migrate (7 total):**

| Service | Port | Unit File Name |
|---------|------|----------------|
| TDA Insights | 5000 | `activity-hub-tda.service` |
| VET Dashboard | 5001 | `activity-hub-vet.service` |
| Projects in Stores | 8001 | `activity-hub-projects.service` |
| Job Codes Dashboard | 8080 | `activity-hub-jobcodes.service` |
| AMP Store Dashboard | 8081 | `activity-hub-amp.service` |
| Store Meeting Planner | 8090 | `activity-hub-meeting-planner.service` |
| Zorro Audio Hub | 8888 | `activity-hub-zorro.service` |

---

## Step 5: Migrate Data & Credentials

- Code: Move from OneDrive path → `/opt/activity_hub/`
- GCP credentials: Upload `application_default_credentials.json` to VM
- Python venv: Recreate with `pip install -r requirements.txt` on VM
- BigQuery access: Confirm GCP service account works from VM network

---

## Step 6: Update DNS / Access URLs

Once on Linux VM, URLs change from `weus42608431466:PORT` to the VM hostname or IP.  
Update `Documentation/KNOWLEDGE_HUB.md` service table with new URLs.

---

## What Changes vs. Stays the Same

| Item | Windows (Current) | Linux VM (Future) |
|------|------------------|-------------------|
| Auto-start | On user logon | On system boot (no login needed) |
| Restart on crash | Bat loop (5 sec) | systemd Restart=always (5 sec) |
| Power outage recovery | Manual login required | Automatic |
| Health check | MONITOR_AND_REPORT.ps1 | Same script or converted to bash |
| GCP / BigQuery | Works today | Needs credential setup on VM |
| File paths | OneDrive `C:\Users\krush\...` | `/opt/activity_hub/...` |

---

## Prerequisites Before Starting

- [ ] Confirm VM hostname/PFX with IT
- [ ] Manager approval for InfoSec request
- [ ] Confirm all Python dependencies can be installed on Ubuntu
- [ ] Confirm BigQuery access works from VM network segment
- [ ] Test one service migrated before doing all 7
