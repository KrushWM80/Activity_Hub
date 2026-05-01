# 📚 Activity Hub - Knowledge Hub & Dependencies Map

**Last Updated**: April 29, 2026  
**Project**: Walmart Enterprise Activity Hub  
**Scope**: Complete organizational reference for architecture, dependencies, and institutional knowledge

---

## 🎯 Quick Navigation

| Section | Purpose | Link |
|---------|---------|------|
| **Live Services** | Running services, ports, auto-start tasks, adding new services | [Live Services & Automation](#️-live-services--automation) |
| **System Overview** | High-level project understanding | [Architecture Overview](#-architecture-overview) |
| **Dependencies Map** | Component relationships & imports | [See Dependencies](DEPENDENCIES-MAP.md) |
| **URL Reference** | Complete production, development, and test URLs | [URL Reference System](../URL_REFERENCE_SYSTEM.md) |
| **Module Guide** | Detailed module documentation | [Module Reference](#-module-reference-guide) |
| **Job Codes Admin** | Consolidated requests, status updates, comments, audit trail | [Job Codes Teaming Dashboard](#4-job-codes-teaming-dashboard) |
| **Configuration** | Role management, access, links | [Configuration Files](#-configuration-reference) |
| **Design Assets** | Brand, colors, typography, widgets | [Design System](Platform/Design/DESIGN_SYSTEM.md) |
| **Compliance** | Security, data classification, WCAG | [Compliance Docs](Platform/Documents/Compliance/) |
| **UI Change Mgmt** | Nav rules, dark mode, OneDrive sync issues | [UI Change Management Rules](#️-ui-change-management-rules) |
| **API Documentation** | Backend & AI integration | [Backend API](Platform/Sparky%20AI/BACKEND_API.md) |

---

## 🏛️ Architecture Overview

### Core Enterprise System

```
Walmart Enterprise Activity Hub
├── User-Facing Interface (Interface/)
│   ├── Admin Control Panel (Admin/)
│   ├── Landing Pages (For You/)
│   ├── Work Management (My Work/)
│   ├── Notifications (Notifications/)
│   ├── Projects (Projects/)
│   ├── Reporting (Reporting/)
│   ├── Settings (Settings/)
│   └── Teams (Teams/)
│
├── Platform Services (Platform/)
│   ├── Design System (Design/)
│   ├── Data Integration (Data-Bridge/)
│   ├── Documentation (Documents/)
│   └── AI Assistant (Sparky AI/)
│
└── Governance & Control
    ├── Role Management
    ├── Access Control via AD Groups
    ├── Dynamic Link Management
    └── Compliance Framework
```

### User Tiers & Role Hierarchy

```
Executive Tier (1-2) → C-Level Executive, Vice President
                       ↓
Management Tier (3-4) → Senior Director, Director
                       ↓
Supervisor Tier (5-6) → Senior Manager, Manager
                       ↓
Individual Tier (7-8) → Specialist, Team Member, Admin
```

**Related Files:**
- [Role Configuration](Interface/Admin/role-configuration.json)
- [Role Management Docs](Interface/Admin/ROLE_MANAGEMENT.md)
- [Access Control Docs](Interface/Admin/ACCESS_CONTROL.md)

---

## 🔗 Component Dependencies

### **Dependency Flow Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interface Layer                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Landing Page │ Admin │ Projects │ Reports │ Settings     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│              Authentication & Authorization Layer               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ AD Groups │ Role Manager │ Permissions Engine             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Configuration & Data Layer                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ Roles│ Access │ Links │ Schemas │ Mappings │ Data-Bridge│  │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│              Backend Services & AI Layer                         │
│  ├─ Node.js/Express API                                         │
│  ├─ Python/FastAPI                                              │
│  ├─ Sparky AI Assistant                                         │
│  └─ Data Processing & Analytics                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Data & Infrastructure                         │
│  ├─ PostgreSQL (Transaction Data)                               │
│  ├─ Redis (Caching & Sessions)                                  │
│  ├─ Elasticsearch (Search)                                      │
│  └─ Cloud Infrastructure (AWS/Azure)                            │
└─────────────────────────────────────────────────────────────────┘
```

**See detailed dependency analysis**: [DEPENDENCIES-MAP.md](DEPENDENCIES-MAP.md)

---

## 📖 Module Reference Guide

### **1. Interface - User-Facing Components**

#### Admin Area
- **Purpose**: System administration, role management, access control
- **Key Files**:
  - `admin-dashboard.html` - Interactive admin panel
  - `role-configuration.json` - Complete role definitions
  - `access-groups.json` - AD group mappings
  - `dynamic-links.json` - Configurable links/buttons
- **Roles**: C-Level Executive → Senior Director → Specialists
- **Permissions**: Enterprise-wide to function-specific
- **Depends On**: Access Control, Role Manager, AD Integration
- **Read First**: [Interface/Admin/README.md](Interface/Admin/README.md)

#### For You - Landing Page
- **Purpose**: Main entry point; personalized dashboard for all users
- **Key Files**:
  - `index.html` - Production landing page
  - `activity-hub-demo.html` - Demo version
- **Features**: Role-based customization, quick access, announcements
- **Depends On**: Design System, Role Manager, Notification System
- **Read First**: [Interface/For%20You%20-%20Landing%20Page/README.md](Interface/For%20You%20-%20Landing%20Page/README.md)

#### Projects Management
- **Purpose**: Project lifecycle management and visualization
- **Key Files**:
  - `index.html`, `styles.css`, `script.js` - Main interface
  - `Upload Projects/` - Project intake system
- **Features**: Project tracking, upload interface, status monitoring
- **Depends On**: Data-Bridge, Design System, Backend API
- **Maintenance**: [Interface/Projects/README.md](Interface/Projects/README.md)

#### My Work, Notifications, Settings, Teams
- **Purpose**: Personal workspace, alerts, user preferences, collaboration
- **Status**: Interface templates in development; **nav tabs removed from all pages** (April 16, 2026)
- **Note**: Teams/My Work/Settings links were removed from the header nav across all 4 pages. See [UI Change Management Rules](#️-ui-change-management-rules).
- **Depends On**: Core Platform Services

---

### **2. Platform - Backend Services & Assets**

#### Design System
- **Purpose**: Consistent brand identity and UI specifications
- **Key Files**:
  - `DESIGN_SYSTEM.md` - Complete design guidelines
  - `COMPLETE_BRAND_SPECS.md` - Walmart brand standards
  - `walmart-brand-variables.css` - CSS design tokens
  - `WIDGET_SPECIFICATIONS.md` - Component specifications
  - `color-tester.html` - Interactive color tool
- **Brand Colors**: 
  - Primary: Walmart Blue (#1E3A8A - #DBEAFE)
  - Accent: Walmart Yellow/Spark (#FFCC00)
  - Supporting: Teal, Green, Orange
- **Typography**: Everyday Sans (Walmart official font)
- **Used By**: All Interface components
- **Read First**: [Platform/Design/README.md](Platform/Design/README.md)

#### Data-Bridge
- **Purpose**: Data integration, transformation, and schema management
- **Key Components**:
  - `transformations.js` - Query/data transformations
  - `validators.js` - Data validation rules
  - `Schemas/` - Data structure definitions
  - `Mappings/` - Field mappings for different systems
  - `Connections/` - External data sources
  - `Uploads/` - File intake system
- **Depends On**: Backend API, Database Layer
- **Used By**: Projects, Reporting, Admin Data-Bridge
- **Read First**: [Platform/Data-Bridge/README.md](Platform/Data-Bridge/README.md)

#### Sparky AI Assistant
- **Purpose**: Intelligent AI-powered assistant for users
- **Key Files**:
  - `BACKEND_API.md` - Complete API documentation
  - `INTEGRATION_GUIDE.md` - Deployment and integration
  - `ai-assistant-demo.html` - Interactive demo
- **Services**: Query processing, context awareness, NLP analysis
- **Tech Stack**: Node.js + Express, Python + FastAPI, OpenAI/Sparky APIs
- **Depends On**: Backend Services, PostgreSQL, Redis, Elasticsearch
- **Read First**: [Platform/Sparky%20AI/README.md](Platform/Sparky%20AI/README.md)

#### Documentation Hub
- **Purpose**: Strategic and compliance documentation
- **Sections**:
  - `Architecture/` - System design and enhancements
  - `Backend/` - API and microservices docs
  - `Compliance/` - Security, data handling, regulations
  - `Strategy/` - Business roadmap and planning
- **Read First**: [Platform/Documents/README.md](Platform/Documents/README.md)

---

### **3. Audio Message Hub (Zorro)**

- **Purpose**: Automated audio generation for Weekly Merchant Messages
- **URL**: http://weus42608431466:8888/Zorro/Audio_Message_Hub
- **Port**: 8888
- **Key Files**:
  - `Store Support/Projects/AMP/Zorro/audio_server.py` - Dashboard server (ThreadingHTTPServer)
  - `Store Support/Projects/AMP/Zorro/Audio/Scripts/generate_weekly_audio.py` - BQ pipeline + synthesis
  - `Store Support/Projects/AMP/Zorro/Audio/windows_media_synthesizer.py` - edge-tts + FFmpeg encoder
- **Voice**: Jenny Neural (en-US) via edge-tts, SAPI5 fallback
- **Data Source**: BigQuery AMP ALL 2 table (Merchant Messages, Review for Publish review - No Comms)
- **Output**: MP4 (AAC 256kbps + thumbnail), Standard Script, Inflection Script, HTML Email Report
- **CMS URL**: `https://enablement.walmart.com/content/store-communications/home/merchandise/weekly-messages/{year}/week-{week}/weekly_messages_audiowk{week}.html`
- **Email**: Walmart internal SMTP (`smtp-gw1.homeoffice.wal-mart.com:25`) with MP4 + scripts attached
- **Automation**: `Automation/start_zorro_24_7.bat` (auto-restart on crash)
- **Health Check**: `MONITOR_AND_REPORT.ps1` (daily 6 AM)
- **Network**: BQ fetch on Eagle WiFi, synthesis on Walmart WiFi (off VPN)
- **Read First**: [Store Support/Projects/AMP/Zorro/docs/KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md](../Store%20Support/Projects/AMP/Zorro/docs/KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md)

---

### **4. Job Codes Teaming Dashboard**

**Status**: ✅ PRODUCTION READY (Validated April 29, 2026)

- **Purpose**: Manage job code updates and team assignments through consolidated requests
- **URL**: http://localhost:8080/Aligned#admin (Admin Panel)
- **Port**: 8080
- **Architecture**: FastAPI (Python) backend + Vanilla JavaScript frontend (SPA)
- **Key Features**:
  - ✅ **Consolidated Requests**: Multiple job codes (1-300+) submitted as ONE request per request type
  - ✅ **Admin Table**: All 6+ columns displaying request metadata with dynamic status badges
  - ✅ **Detail Modal**: Full editing interface with status updates, comments, and history tracking
  - ✅ **Status Management**: Dropdown to change status (Pending → In Review → Approved → Rejected)
  - ✅ **Comments System**: Add timestamped comments with author metadata
  - ✅ **Audit Trail**: Complete history tracking with old→new values and change timestamps

#### **Key Files & Structure**
```
Store Support/Projects/JobCodes-teaming/Teaming/dashboard/
├── backend/
│   └── main.py                 # FastAPI server, REST endpoints, business logic
│       ├── POST /api/submit-new-request         # Submit consolidated requests
│       ├── GET  /api/job-codes-master/requests  # Get all requests (admin view)
│       ├── POST /api/job-codes-master/requests/{id}/update-status
│       ├── POST /api/job-codes-master/requests/{id}/add-comment
│       └── GET  /api/job-codes-master/requests/{id}/history
├── frontend/
│   └── index.html              # Single Page App (SPA)
│       ├── Admin Panel (tabs: User Management, Job Code Requests, Teaming Requests)
│       ├── Admin Table (Job Codes, Description, Status, Requested By, Date, Actions)
│       ├── Detail Modal (metadata, status dropdown, comments, history)
│       └── Consolidated request display (all codes in single row)
└── data/
    └── job_code_requests.json  # Persistent JSON storage
```

#### **Consolidated Request Structure**
```json
{
  "id": 1777410999999,
  "job_codes": ["1-0-040407", "1-0-040413", "1-0-40225", ...],
  "request_type": "job_code_update",
  "status": "approved",
  "requested_by": "krush",
  "requested_by_name": "Kendall Rush",
  "requested_at": "2026-04-29T14:30:00.000000",
  "description": "Full description text",
  "comments": [
    {
      "timestamp": "2026-04-29T12:58:52.382949",
      "author": "admin",
      "author_name": "Administrator",
      "text": "Comment text",
      "is_internal": false
    }
  ],
  "history": [
    {
      "timestamp": "2026-04-29T12:57:34.725694",
      "changed_by": "admin",
      "changed_by_name": "Administrator",
      "field": "status",
      "old_value": "pending",
      "new_value": "approved"
    }
  ]
}
```

#### **Admin Features Validated**
| Feature | Status | Details |
|---------|--------|---------|
| **One Request, Multiple Codes** | ✅ | 6 job codes in single row (not 6 separate rows) |
| **Admin Table Columns** | ✅ | Job Codes, Description, Status, Requested By, Date, Actions |
| **Dynamic Status Badges** | ✅ | Yellow=pending, Green=approved, Red=rejected |
| **Detail Modal Display** | ✅ | Full metadata, request type, requester info, job codes as badges |
| **Status Dropdown** | ✅ | Change status with single dropdown selection |
| **Comment Add/Display** | ✅ | Add timestamped comments, stored with author metadata |
| **History Tracking** | ✅ | Records all changes with old→new values and timestamps |
| **Data Persistence** | ✅ | All changes saved to JSON file (no loss on server restart) |

#### **Critical Bugs Fixed (April 29, 2026)**
1. **Role-Check Bug** (main.py:2341)
   - Fixed: Changed `if user['role'] != 'admin':` to `if not user_has_admin_access(user, "Job Codes"):`
   - Impact: Admin role prefix "Admin - All Tabs" now recognized correctly

2. **History Display Bug** (index.html)
   - Fixed: Changed `entry.from/to` to `entry.old_value/new_value`
   - Impact: History now displays "pending → approved" instead of "undefined"

3. **Function Routing** (index.html)
   - Created: Separate `showAdminJobCodeRequestDetail()` function for admin modal
   - Impact: Admin table uses correct modal with full editing UI

#### **Authentication & Access Control**
- **Session-Based**: `session_id` cookie authentication
- **Role-Based Access**: `user_has_admin_access(user, "Job Codes")` function
- **Supported Roles**: 
  - "Admin - All Tabs" (full access)
  - "Admin - Job Codes" (job codes only)
  - "Reviewer - Job Codes" (view-only access)
- **User Metadata**: username, full name, role stored in session

#### **API Endpoints - Fully Functional**
```
GET  /api/job-codes-master/requests
     → Returns: { "requests": [ { consolidated request object }, ... ] }

POST /api/job-codes-master/requests/{id}/update-status
     → Body: { "status": "approved|rejected|in_review|pending" }
     → Response: { "success": true, "history_entry": {...} }

POST /api/job-codes-master/requests/{id}/add-comment
     → Body: { "text": "comment text" }
     → Response: { "success": true, "comment": {...} }

GET  /api/job-codes-master/requests/{id}/history
     → Returns: { "history": [...], "comments": [...] }
```

#### **Frontend Functions - Validated Working**
- `loadAdminJobCodeRequests()` — Fetches all requests, populates admin table
- `showAdminJobCodeRequestDetail(requestId)` — Opens detail modal with full editing UI
- `saveJobCodeRequestChanges(requestId)` — Updates status, saves to backend
- `saveJobCodeComment(requestId)` — Adds comment with metadata

#### **Dependencies**
- **Backend**: FastAPI, Python 3.14+, Uvicorn
- **Frontend**: Bootstrap 5, Bootstrap Icons, Vanilla JavaScript
- **Data**: JSON file-based persistence (no database required for MVP)
- **Authentication**: Session-based via cookie
- **Optional**: BigQuery disabled by default (HAS_BIGQUERY = False)

#### **How to Run**
```bash
# Terminal in Project Root
cd "Store Support/Projects/JobCodes-teaming/Teaming/dashboard/backend"
python main.py
# Server runs on http://localhost:8080
# Frontend served at /Aligned path
```

#### **Testing Checklist** ✅
- ✅ Consolidated request displays in single table row
- ✅ All 6 job codes visible in Job Codes column
- ✅ Status changed from pending to approved (backend recorded)
- ✅ Admin table status badge updated dynamically
- ✅ Comment added with timestamp and author metadata
- ✅ History displays "pending → approved" with correct timestamp
- ✅ All changes persisted to JSON file
- ✅ Success toasts appear for all operations
- ✅ Detail modal refreshes after edits

---

## 🖥️ Live Services & Automation

**Last Updated**: April 29, 2026  
**Machine**: WEUS42608431466 | IP: 10.97.114.181 | User: `krush`

---

### System Resilience Architecture (Ways of Working)

Four layers keep services running. **All four must be healthy** — each layer is a fallback for the one above it.

| Layer | How It Works | Current State |
|-------|-------------|---------------|
| **Layer 1 — No crash** | Bat restart loops run forever, restart within 5s of any crash | ✅ All 8 services have bat loops |
| **Layer 2 — Reboot recovery** | `onlogon` scheduled tasks launch bat loops at every login | ✅ All 8 AutoStart tasks registered (April 13, 2026) |
| **Layer 3 — Health monitoring** | `continuous_monitor.ps1` every 5 min, checks all 8 ports, restarts any down bat loop | ✅ Built and registered as `Activity_Hub_ContinuousMonitor` |
| **Layer 4 — Daily email** | `MONITOR_AND_REPORT.ps1` at 6 AM — health report + reboot-pending warning | ✅ Running, reboot-pending alert added April 10, 2026 |

**⚠️ Important — the 3 AM JobCodes forced restart:**  
`Activity_Hub_JobCodes_AutoStart` includes a nightly 3 AM restart. This is a **workaround** for a historical memory leak / BigQuery token expiry issue on that service — it is **not** a pattern to apply to other services. A forced nightly restart hides degradation instead of fixing it. Do not copy this to other bat files.

**Re-registering all tasks** (required after any Windows Update reboot that clears tasks):  
From an **admin terminal** (Win+X → Terminal Admin):
```
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\register_tasks_cmd.bat"
```

---

### Active Services (8 total)

| Service | Port | URL | Start Script |
|---------|------|-----|--------------|
| TDA Insights | 5000 | http://localhost:5000 | `Automation/start_tda_insights_24_7.bat` |
| VET Dashboard | 5001 | http://localhost:5001/vet_dashboard.html | `Automation/start_vet_dashboard_24_7.bat` |
| Projects in Stores | 8001 | http://localhost:8001 | `Automation/start_projects_in_stores_24_7.bat` |
| Job Codes Dashboard | 8080 | http://10.97.114.181:8080 | `Automation/start_jobcodes_server_24_7.bat` |
| AMP Store Dashboard | 8081 | http://weus42608431466:8081 | `Automation/start_store_dashboard_24_7.bat` |
| Store Meeting Planner | 8090 | http://weus42608431466:8090/StoreMeetingPlanner | `Automation/start_meeting_planner_24_7.bat` |
| Zorro Audio Hub | 8888 | http://weus42608431466:8888/Zorro/Audio_Message_Hub | `Automation/start_zorro_24_7.bat` |
| Activity Hub | 8088 | http://weus42608431466:8088/activity-hub/ | `Automation/start_activity_hub_24_7.bat` |

### Scheduled Tasks (Windows Task Scheduler)

All tasks last registered April 13, 2026. Requires **elevated (admin) terminal** to create/modify.

| Task Name | Trigger | Action |
|-----------|---------|--------|
| `Activity_Hub_JobCodes_AutoStart` | On logon | Starts Job Codes (8080) |
| `Activity_Hub_ProjectsInStores_AutoStart` | On logon | Starts Projects in Stores (8001) |
| `Activity_Hub_TDA_AutoStart` | On logon | Starts TDA Insights (5000) |
| `Activity_Hub_Store_Dashboard_AutoStart` | On logon | Starts AMP Dashboard (8081) |
| `Activity_Hub_StoreMeetingPlanner_AutoStart` | On logon | Starts Meeting Planner (8090) |
| `Activity_Hub_VETDashboard_AutoStart` | On logon | Starts VET Dashboard (5001) |
| `Activity_Hub_Zorro_AutoStart` | On logon | Starts Zorro (8888) |
| `Activity_Hub_ActivityHub_AutoStart` | On logon | Starts Activity Hub (8088) |
| `Activity_Hub_Daily_HealthCheck` | Daily 6:00 AM | Runs `MONITOR_AND_REPORT.ps1` — health check + email |
| `Activity_Hub_TDA_Daily_Email` | Daily 6:00 AM | TDA daily report email (`send_tda_weekly_email.bat`) |
| `Activity_Hub_TDA_Weekly_Email` | Weekly Thu 11:00 AM | TDA weekly summary email (`send_tda_weekly_email.bat`) |
| `Activity_Hub_VET_Daily_Email` | Daily 6:00 AM | VET daily report email (`send_vet_daily_email.bat`) |
| `Activity_Hub_ContinuousMonitor` | Every 5 minutes | Checks all 8 ports, restarts any down bat loop (`Automation/continuous_monitor.ps1`) |
| `Activity_Hub_Audio_Daily_Status` | Daily 6:00 AM | Zorro audio status email (`Automation/send_audio_status_email.bat`) |

**Verify tasks are registered:**
```powershell
schtasks /query /fo TABLE | Select-String "Activity_Hub"
```

---

### ⚠️ Critical Operating Rules

#### NEVER use Outlook COM (`win32com`) to send automated emails
All automated email reports **must** use Walmart's internal SMTP gateway directly via Python `smtplib`. **Never** use `win32com.client.Dispatch('Outlook.Application')` in any automated script.

**Why:** Outlook COM queues mail in Outlook's Outbox and only transmits when Outlook is in an active, foreground state. When the screen is off or Outlook is in low-power sync mode, emails sit unsent for hours — all flushing at once when the screen wakes. Recipients receive nothing on time, then get a flood of duplicate emails simultaneously.

**Correct pattern for all email scripts:**
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
SMTP_PORT = 25
FROM_EMAIL = "kendall.rush@walmart.com"

msg = MIMEMultipart('mixed')
msg['From'] = FROM_EMAIL
msg['To'] = '; '.join(recipients)
msg['Subject'] = subject
msg.attach(MIMEText(html_body, 'html', 'utf-8'))

# Attach files
with open(attachment_path, 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
msg.attach(part)

# Send — no auth required on Walmart network
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
    server.sendmail(FROM_EMAIL, recipients, msg.as_string())
```

**Files updated April 6, 2026:**
- `Store Support/Projects/VET_Dashboard/email_service.py` — Outlook COM removed, smtplib added
- `Store Support/Projects/TDA Insights/send_weekly_report.py` — Outlook COM removed, smtplib added
- `Store Support/Projects/DC to Store Change Management Emails/email_helper.py` — Outlook COM removed, smtplib added
- `MONITOR_AND_REPORT.ps1` — Outlook COM removed, `System.Net.Mail.SmtpClient` added
- `send_status.ps1` — Outlook COM removed, `System.Net.Mail.SmtpClient` added

**Any new email script or existing script still using `win32com` must be updated before deployment.**

#### NEVER use `Stop-Process -Name python -Force`
This kills **all** Python processes on the machine — every service goes down simultaneously. The bat restart loops will attempt recovery but may not all succeed, especially if the continuous monitor fires during the restart window and triggers the double-launch problem.

**Safe way to kill a specific service by port:**
```powershell
# Kill only the process on a specific port (e.g., 5001)
$pid = (netstat -ano | Select-String ":5001 " | Select-String "LISTENING" | ForEach-Object { ($_ -split "\s+")[-1] }) | Select-Object -First 1
if ($pid) { taskkill /F /PID $pid }
```

**Safe way to restart one service:**
```powershell
# Stop just that port's process, then let the bat loop restart it
$pid = (netstat -ano | Select-String ":5001.*LISTENING" | ForEach-Object { ($_ -split "\s+")[-1] }) | Select-Object -First 1
if ($pid) { taskkill /F /PID $pid }
# The bat loop detects the exit and restarts automatically within 5-7 seconds
```

#### service_manager.ps1 — Preferred tool for all service management

**File:** `service_manager.ps1` (root of Activity Hub)  
**Purpose:** View PID, memory, uptime for all 8 services. Safely start/stop/restart individual services or all at once. Uses live netstat PID lookup — no stale .pid files.  
**This is a manual tool — automation (bat loops, continuous_monitor, AutoStart tasks) runs independently of it.**

```powershell
# From the Activity Hub root directory:
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

# Check all 8 services — shows Port, Status, PID, Memory, Uptime
.\service_manager.ps1 -Action status

# Restart a single service safely (stops by port PID, starts bat loop)
.\service_manager.ps1 -Action restart -Service tda_insights
.\service_manager.ps1 -Action restart -Service job_codes
.\service_manager.ps1 -Action restart -Service meeting_planner

# Start or stop a single service
.\service_manager.ps1 -Action start -Service zorro
.\service_manager.ps1 -Action stop -Service vet_dashboard

# Start or stop all 8 services
.\service_manager.ps1 -Action start -Service all
.\service_manager.ps1 -Action stop -Service all
```

**Valid service keys:** `activity_hub`, `projects_in_stores`, `job_codes`, `amp_dashboard`, `meeting_planner`, `vet_dashboard`, `tda_insights`, `zorro`

**How it works internally:** calls `Get-PortPid` (netstat lookup) for live PID — never relies on saved .pid files. Stop uses `taskkill /F /PID /T` which kills the bat loop parent AND its Python child together. Start launches the bat loop via `cmd.exe /c` hidden window — identical to what the AutoStart scheduled tasks do.

**DO NOT use `pid_manager.ps1`** — that script starts Python **directly** (no bat loop). If the process crashes, nothing restarts it — you lose Layer 1 (auto-restart on crash). It also only tracks 5 of the 8 services and uses stale .pid files that become wrong after any crash/restart. It was created by an automated session without awareness of the bat-loop architecture. Use `service_manager.ps1` exclusively.

#### BigQuery schema changes can break service data silently
If a service suddenly shows empty or wrong data, check whether BigQuery column values have been renamed. The query filter in `backend.py` (or equivalent) may need updating. Example: `TDA_Ownership = 'Dallas POC'` was renamed to `'Dallas VET'` on April 2, 2026.

#### Recovery methodology (when multiple services are down)
1. Do NOT mass-kill Python processes
2. Check which ports are down: `netstat -ano | Select-String "LISTENING" | Select-String ":5000|:5001|:8001|:8080|:8081|:8088|:8090|:8888"`
3. Start only the specific downed services using their bat file
4. Wait 15-20 seconds then re-check ports
5. If a bat loop itself dies, `Activity_Hub_ContinuousMonitor` (every 5 min) will detect the down port and restart it via `Automation/continuous_monitor.ps1`

---

### Adding a New Service (URL / Dashboard)

When a new service/URL is added, complete **all 5 steps**:

**Step 1** — Create `Automation/start_<servicename>_24_7.bat`  
Copy an existing bat as template. Required elements:
- Port-kill block before the restart loop (kills stale process holding the port)
- Restart loop with `timeout /t 5` between attempts
- Log file output (`>> "%LogFile%" 2>&1`)
- `GOOGLE_APPLICATION_CREDENTIALS` set if service uses BigQuery

```bat
:restart_loop
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":%PORT% " ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a > nul 2>&1
)
timeout /t 2 /nobreak > nul
"%PYTHON_EXE%" main.py >> "%LOG_FILE%" 2>&1
timeout /t 5 /nobreak > nul
goto restart_loop
```

**Step 2** — Add to `Automation/register_tasks_cmd.bat`:
```bat
schtasks /create /tn "Activity_Hub_<ServiceName>_AutoStart" /tr "cmd /c \"%BASE%\start_<servicename>_24_7.bat\"" /sc onlogon /ru "%USER%" /f
```

**Step 3** — Run `Automation/register_tasks_cmd.bat` from an **elevated (admin) terminal**:
```
Win + X → Terminal (Admin)
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\register_tasks_cmd.bat"
```

**Step 4** — Add to `MONITOR_AND_REPORT.ps1` services list so it is included in the daily 6 AM health check and auto-restart email.

**Step 5** — Add to `continuous_monitor.ps1` services array so it is included in the every-5-minute uptime check:
```powershell
@{Name="<ServiceName>"; Port=<PORT>; HealthURL="http://localhost:<PORT>"; RestartScript="...\Automation\start_<servicename>_24_7.bat"}
```

**Step 6** — Update the service table in this file (`KNOWLEDGE_HUB.md` → Active Services table) with the new port and URL.

**Step 7** — Add the Spark favicon (two-part requirement — both are mandatory):

*Part A — HTML `<head>` tag* (in **every** HTML file served by the service):
```html
<link rel="icon" type="image/png" href="/Spark_Blank.png">
```
Place immediately after `<meta name="viewport" ...>`.

*Part B — Server route* (in the Python server file):

**FastAPI:**
```python
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    logo = Path(__file__).parent / "Spark_Blank.png"
    if logo.exists():
        return FileResponse(str(logo), media_type="image/png", headers={"Cache-Control": "public, max-age=86400"})
    from fastapi.responses import Response
    return Response(status_code=204)
```

**Flask:**
```python
@app.route('/favicon.ico')
def favicon():
    logo = os.path.join(os.path.dirname(__file__), 'Spark_Blank.png')
    if os.path.exists(logo):
        return send_file(logo, mimetype='image/png', max_age=86400)
    return '', 204
```

*File placement:* Copy `Spark_Blank.png` from `Store Support\General Setup\Design\Spark Blank.png` to the server's root directory (same folder as the server `.py` file, or the `frontend/` folder for services that serve HTML from a subdirectory). Chrome accepts PNG favicons — no `.ico` file required.

---

### Adding a New Email Report

When a new scheduled email report is added, complete **all 4 steps**:

**Step 1** — Create `Automation/send_<reportname>_email.bat`  
Copy an existing email bat as template. Required elements:
- Port check for the backend the report depends on **before** running the report script
- If port is down: start the backend bat and wait up to 30 seconds for it to come up
- Only run the report script after confirming the backend is alive
- Log all steps to a log file

```bat
REM --- Ensure backend (port XXXX) is running before generating report ---
netstat -ano | findstr ":XXXX " | findstr "LISTENING" > nul 2>&1
if %errorlevel% neq 0 (
    start /b "" cmd /c "%ProjectRoot%\Automation\start_<servicename>_24_7.bat" > nul 2>&1
    set /a attempts=0
    :wait_loop
    timeout /t 3 /nobreak > nul
    netstat -ano | findstr ":XXXX " | findstr "LISTENING" > nul 2>&1
    if %errorlevel% equ 0 goto ready
    set /a attempts+=1
    if !attempts! lss 10 goto wait_loop
    echo WARNING: Backend did not start in 30s >> "%LogFile%"
    goto run_report
    :ready
)
:run_report
"%PythonExe%" send_report.py >> "%LogFile%" 2>&1
```

**Step 2** — Add a scheduled task to `Automation/register_tasks_cmd.bat`:
```bat
schtasks /create /tn "Activity_Hub_<ReportName>_Email" /tr "cmd /c \"%BASE%\send_<reportname>_email.bat\"" /sc daily /st 06:00:00 /ru "%USER%" /f
```
(Adjust `/sc` and `/st` for the correct schedule — daily, weekly, etc. Use `/ru "%USER%"` — do NOT use `/rl highest`.)

**Step 3** — Run `Automation/register_tasks_cmd.bat` from an **elevated (admin) terminal**.

**Step 4** — Add to the Scheduled Tasks table in this file (`KNOWLEDGE_HUB.md`) with task name, trigger, and action.

---

## ☁️ GCP Project — wmt-storesupport-prod

**Last Updated**: April 7, 2026  
**YAML**: `Store Support/General Setup/BigQueryProject/06-GCP-Setup/wmt-storesupport-prod.yaml`

### Confirmed Values (updated in YAML)

| Field | Value |
|-------|-------|
| Project ID | `wmt-storesupport-prod` |
| Billing Account | `01FF90-22DB49-E911B6` |
| Cost Center | `7858` (label: `US07858`) |
| APM ID | `APM0022933` |
| SSP ID | `SSP00004633` (Allen Still's approved project) |
| TR Product ID | `4639` |

### Confirmed AD Groups

| Group | Role |
|-------|------|
| `gcp-storesupport-prod-admin@walmart.com` | Owner / BigQuery Admin |
| `gcp-storesupport-dev-admin@walmart.com` | Editor / BigQuery DataEditor |
| `gcp-storesupport-prod-viewer@walmart.com` | Viewer |

### PR Submission Status

- ✅ AD groups confirmed and aligned across docs and YAML
- ✅ APM ID confirmed: `APM0022933`
- ✅ SSP ID confirmed: `SSP00004633`
- ✅ Billing account filled in YAML: `01FF90-22DB49-E911B6`
- ✅ Cost center filled in YAML: `US07858`
- ✅ TR Product ID filled in YAML: `4639`
- ✅ Roadmap status updated to Phase 2 in progress

---

## ⚙️ Configuration Reference

### **Role Configuration** (`Interface/Admin/role-configuration.json`)

```json
{
  "roles": [
    {
      "id": "c-level-executive",
      "name": "C-Level Executive",
      "category": "executive",
      "level": 1,
      "permissions": [
        "enterprise.view.all",
        "dashboard.executive.access",
        "metrics.enterprise.view",
        "reports.all.access"
      ]
    },
    // ... 8 total role tiers defined
  ]
}
```

**Key Roles:**
1. **C-Level Executive** - Enterprise-wide access
2. **Vice President** - Business unit visibility
3. **Senior Director** - Multi-department management
4. **Director** - Department-specific oversight
5. **Senior Manager** - Team leadership
6. **Manager** - Direct team management
7. **Specialist** - Function-specific roles
8. **Team Member** - Individual contributor

**Documentation**: [Role Management](Interface/Admin/ROLE_MANAGEMENT.md)

### **Access Control** (`Interface/Admin/access-groups.json`)

Maps Active Directory groups to roles and permissions.

**Key Features:**
- AD Group integration (Walmart enterprise)
- Automatic role provisioning
- Permission inheritance
- Department-specific customizations

**Documentation**: [Access Control](Interface/Admin/ACCESS_CONTROL.md)

### **Dynamic Links** (`Interface/Admin/dynamic-links.json`)

Configurable navigation links and buttons across the platform.

**Key Features:**
- Role-based link visibility
- Dynamic URL management
- Button configuration
- Link categorization

**Documentation**: [Link Management](Interface/Admin/LINK_MANAGEMENT.md)

### **Data Schemas** (`Interface/Admin/Data-Bridge/Schemas/`)

Define data structure and validation rules.

**Schema Files:**
- `projects-schema.json` - Project data structure
- `_schema-template.json` - Template for new schemas

### **Data Mappings** (`Interface/Admin/Data-Bridge/Mappings/`)

Map external data systems to internal schemas.

**Mapping Files:**
- `Projects/intake-hub-mapping.json` - Map external project data
- `_mapping-template.json` - Template for new mappings

---

## 🎨 Design & Branding

Detailed information in [Platform/Design/DESIGN_SYSTEM.md](Platform/Design/DESIGN_SYSTEM.md)

### **Color System**

**Primary Brand Colors:**
```css
--walmart-navy: #1E3A8A;
--walmart-blue-dark: #1D4ED8;
--walmart-blue: #3B82F6;
--walmart-blue-light: #60A5FA;
--walmart-yellow: #FFCC00 (Spark);
```

**Status Colors:**
- Success: #38A169 (Green)
- Warning: #D69E2E (Orange)
- Error: #E53E3E (Red)
- Info: #3182CE (Blue)

### **Typography**

**Fonts:**
- Primary: Everyday Sans (Walmart official)
- Secondary: Roboto
- Monospace: SF Mono, Cascadia Code

**Scale:** 12px (xs) to 48px (5xl)

### **Components & Widgets**

Full specifications: [Widget Specifications](Platform/Design/WIDGET_SPECIFICATIONS.md)

---

## 🔐 Compliance & Security

### **Data Classification**
- [Data Classification Assessment](DATA-CLASSIFICATION-ASSESSMENT.md)
- [Data Classification Change Control](DATA-CLASSIFICATION-CHANGE-CONTROL.md)

### **Compliance Documents**
Located in [Platform/Documents/Compliance/](Platform/Documents/Compliance/)

**Key Areas:**
- SOC 2 Type II compliance
- WCAG AA/AAA accessibility
- Data privacy and handling
- Security frameworks
- Enterprise governance

### **System Security Plan (SSP)**
- **SSP ID:** SSP00004633
- **APM ID:** APM0022933
- **Team:** Store Support
- **Go Live:** 9/21/2026 (Phase 1)
- **Type:** Implementation SSP (NOT MSO-SSP)
- **Submitted:** April 13, 2026
- **Data Classification:** Highly Sensitive
- **Data Categorization:** PII, System of Record, Financial Data, SOX, Business Information

**SSP Questionnaire Answers:**
| # | Question | Answer |
|---|----------|--------|
| 1 | Committed delivery date? | Yes — 9/21/2026 |
| 2 | Team owns solution? | Yes |
| 3 | Team maintains security controls? | Yes |
| 4 | Require customers to reference SSP? | No (not an MSO) |
| 5 | Hosting | Walmart GCP + Walmart Store/DC |
| 6 | External 3rd party data? | No |
| 7 | Vendor direct network access? | No |
| 8 | Internet/public networks? | No |
| 9 | New unapproved tech? | No |
| 10 | IoT? | No |
| 11 | OT? | No |
| 12 | External consumers? | No |
| 13 | Restricted vendors? | No |
| 14 | Hourly associate access? | No |
| 15 | Mobile devices/apps? | No |
| 16 | NDA/Confidential? | No |

**MSO Determination:** NOT MSO — Sub-platforms (TDA, Job Codes, Projects in Stores, Meeting Planner, Zorro, VET) are components of Activity Hub under the same SSP.

**Agreement:** "We (Store Support) agree that the plan question responses provided are accurate and understand that incorrect responses could lead to cancellation of this SSP."

### **PCI DSS Scoping**
- [PCI DSS Scoping Checklist](PCI_DSS_SCOPING_CHECKLIST.md) — 10-section questionnaire (40+ questions)
- [PCI DSS Scoping Analysis](PCI_DSS_SCOPING_ANALYSIS.md) — Activity Hub scoping result: **Out of Scope**
- [Network Segmentation Confirmation](PCI_NETWORK_SEGMENTATION_CONFIRMATION.md) — Diagram, route table, segmentation scan, TCP port scan evidence

**Activity Hub PCI Status:** Out of Scope (no CHD/SAD, no MIDs, no CDE connectivity, no payment processing)

**PCI Standards Enforced:**
1. **PAN Input Prevention** — All free-text forms include client-side validation rejecting 13-19 digit numeric sequences and display "Do not enter payment card information" notices
2. **Log Hygiene** — Flask/Werkzeug logging captures only HTTP metadata (timestamp, method, path, status). Request bodies, file contents, and user-submitted text are never logged
3. **No Payment Data in Data Sources** — All data feeds (BigQuery, internal APIs) confirmed to contain no CHD, PAN tokens, or PCI-originated data
4. **No Payment Data in Outputs** — Automated emails and reports draw exclusively from non-PCI data sources

**Change-in-Scope Triggers** — The following events require immediate PCI re-scoping (contact Compliance team):
- Adding payment processing, checkout, or MID association to any Activity Hub feature
- Integrating with a payment gateway, processor, or tokenization service
- Consuming data feeds from PCI-scoped systems
- Sharing infrastructure (servers, databases, network segments) with PCI-scoped systems
- Providing authentication, logging, or security services to PCI-scoped systems

**Trigger Response Process:**
1. Development team identifies potential scope trigger
2. Notify Solution Owner → Compliance team within **5 business days**
3. Compliance team initiates re-scoping using [PCI DSS Scoping Checklist](PCI_DSS_SCOPING_CHECKLIST.md)
4. If in scope: engage QSA/ISA for formal scoping determination
5. Annual re-validation per PCI DSS Requirement 12.5.2

### **Git & Version Control**
- [Git Repository Setup](GIT_REPOSITORY_SETUP.md)
- [Git Setup Guide](GIT_SETUP_GUIDE.md)

---

## 🚀 Technology Stack Summary

### **Frontend**
- HTML5, CSS3, JavaScript (ES6+)
- React 18+ (planned)
- TypeScript (planned)
- Responsive Design (Mobile → Desktop)

### **Backend**
- Node.js + Express (API server)
- Python + FastAPI (AI/ML processing)
- TypeScript support

### **Databases & Caching**
- PostgreSQL (transaction data)
- Redis (sessions, caching)
- Elasticsearch (full-text search)

### **External Integrations**
- Active Directory (authentication)
- Sparky AI (Walmart AI service)
- OpenAI (NLP backup)
- AWS/Azure (infrastructure)

### **Infrastructure**
- Docker (containerization)
- Kubernetes (orchestration)
- RabbitMQ (message queue)
- CI/CD pipelines

---

## 📊 Key Metrics & Goals

**Business Impact:**
- Time Savings: 4-6 hours per user per week
- Productivity Improvement: 15% in project delivery
- User Satisfaction Target: >4.5/5 stars
- Administrative Cost Reduction: 30%

**User Base:**
- 50,000+ Walmart Enterprise employees
- 8 role tiers across all business units
- Global deployment across departments

**Investment:**
- Total Investment: $3.4M (12 months)
- Expected Annual Benefits: $27M
- First-Year ROI: 694%

---

## 📋 Document Index

### **Root Level Documentation**
- [README.md](README.md) - Project overview and goals
- [KNOWLEDGE_HUB.md](KNOWLEDGE_HUB.md) - This file (comprehensive reference)
- [DEPENDENCIES-MAP.md](DEPENDENCIES-MAP.md) - Detailed component relationships
- [GIT_REPOSITORY_SETUP.md](GIT_REPOSITORY_SETUP.md) - Version control setup
- [DATA-CLASSIFICATION-ASSESSMENT.md](DATA-CLASSIFICATION-ASSESSMENT.md) - Data handling standards

### **Interface Documentation**
- [Interface/Admin/README.md](Interface/Admin/README.md)
- [Interface/Admin/ROLE_MANAGEMENT.md](Interface/Admin/ROLE_MANAGEMENT.md)
- [Interface/Admin/ACCESS_CONTROL.md](Interface/Admin/ACCESS_CONTROL.md)
- [Interface/Admin/LINK_MANAGEMENT.md](Interface/Admin/LINK_MANAGEMENT.md)
- [Interface/For You - Landing Page/README.md](Interface/For%20You%20-%20Landing%20Page/README.md)
- [Interface/Projects/README.md](Interface/Projects/README.md)

### **Platform Documentation**
- [Platform/Design/README.md](Platform/Design/README.md)
- [Platform/Design/DESIGN_SYSTEM.md](Platform/Design/DESIGN_SYSTEM.md)
- [Platform/Data-Bridge/README.md](Platform/Data-Bridge/README.md)
- [Platform/Sparky AI/README.md](Platform/Sparky%20AI/README.md)
- [Platform/Sparky AI/BACKEND_API.md](Platform/Sparky%20AI/BACKEND_API.md)
- [Platform/Documents/README.md](Platform/Documents/README.md)

### **Compliance & Governance**
- [Platform/Documents/Compliance/](Platform/Documents/Compliance/) - Full compliance suite

---

## 🔄 How to Use This Knowledge Hub

### **For New Team Members**
1. Start with [README.md](README.md) - Project overview
2. Read [Architecture Overview](#-architecture-overview) above
3. Review role requirements in [Role Management](Interface/Admin/ROLE_MANAGEMENT.md)
4. Study [Design System](Platform/Design/DESIGN_SYSTEM.md)
5. Check [DEPENDENCIES-MAP.md](DEPENDENCIES-MAP.md) for component interactions

### **For Developers**
1. Review [DEPENDENCIES-MAP.md](DEPENDENCIES-MAP.md) for system architecture
2. Check [Design System](Platform/Design/DESIGN_SYSTEM.md) for UI standards
3. Read [Backend API Documentation](Platform/Sparky%20AI/BACKEND_API.md)
4. Review relevant configuration files (roles, access, links)
5. Check [Compliance Documentation](Platform/Documents/Compliance/) for security requirements

### **For Project Managers**
1. Review [README.md](README.md) for project goals
2. Check [Role Management](Interface/Admin/ROLE_MANAGEMENT.md) for stakeholder tiers
3. Review compliance status in [Compliance Documentation](Platform/Documents/Compliance/)
4. Check [Data Classification](DATA-CLASSIFICATION-ASSESSMENT.md) for data handling
5. Review [Backend Development Next Steps](Platform/Documents/Backend/BACKEND-DEVELOPMENT-NEXT-STEPS.md)

### **For Administrators**
1. Review [Admin Dashboard Guide](Interface/Admin/README.md)
2. Study [Role Configuration](Interface/Admin/role-configuration.json)
3. Review [Access Control](Interface/Admin/ACCESS_CONTROL.md)
4. Check [Link Management](Interface/Admin/LINK_MANAGEMENT.md)
5. Monitor [Compliance Requirements](Platform/Documents/Compliance/)

---

## 🔗 Quick Links by Topic

**User Management**
- [Role Configuration](Interface/Admin/role-configuration.json)
- [Role Management Docs](Interface/Admin/ROLE_MANAGEMENT.md)
- [Access Control](Interface/Admin/ACCESS_CONTROL.md)

**System Configuration**
- [Dynamic Links](Interface/Admin/dynamic-links.json)
- [Link Management](Interface/Admin/LINK_MANAGEMENT.md)
- [Data Schemas](Interface/Admin/Data-Bridge/Schemas/)
- [Data Mappings](Interface/Admin/Data-Bridge/Mappings/)

**Design & UX**
- [Design System](Platform/Design/DESIGN_SYSTEM.md)
- [Brand Specifications](Platform/Design/COMPLETE_BRAND_SPECS.md)
- [Widget Specifications](Platform/Design/WIDGET_SPECIFICATIONS.md)
- [Color Tester](Platform/Design/color-tester.html)

**Technology & Engineering**
- [Backend API](Platform/Sparky%20AI/BACKEND_API.md)
- [AI Integration](Platform/Sparky%20AI/INTEGRATION_GUIDE.md)
- [System Architecture](Platform/Documents/Architecture/)
- [Data Bridge](Platform/Data-Bridge/README.md)

**Security & Compliance**
- [Compliance Documentation](Platform/Documents/Compliance/)
- [Data Classification](DATA-CLASSIFICATION-ASSESSMENT.md)
- [Accessibility Standards](Platform/Design/DESIGN_SYSTEM.md#accessibility)

---

## � Refresh Guide - Store Refresh Dashboard

The Store Refresh Guide manages enterprise-wide store refresh processes with real-time performance tracking via BigQuery integration.

### **Core Dashboards**

**1. Business Overview Dashboard**
- **File**: `Store Support/Projects/Refresh Guide/business-overview-dashboard-v3-2-23-26.html` (8.8 MB)
- **Purpose**: Main store refresh metrics and performance tracking
- **Status**: Validation errors present (regex pattern, deprecated meta tag) - not currently deployable
- **Data Source**: BigQuery `athena-gateway-prod.store_refresh.store_refresh_data`
- **Metrics**: Completion %, stores active, total assignments, divisions, areas, formats

**2. 7-Week Comparison Dashboard** ⭐ **PRODUCTION READY**
- **File**: `Store Support/Projects/Refresh Guide/business-overview-comparison-dashboard-2-23-26.html` (61.31 KB)
- **Date Range**: Week 1 (1/19/26) → Week 7 (2/16-2/23/26)
- **Purpose**: Multi-week trend analysis and performance comparison
- **Status**: ✅ Production-ready for Code Puppy Pages deployment
- **Update Frequency**: Weekly (Fridays, starting Week 8)
- **Platform**: Code Puppy Pages (embedded HTML, no external dependencies)

### **Weekly Data Extraction & Update Process**

**📝 Complete SOP**: [Store Support/Projects/Refresh Guide/WEEKLY_DASHBOARD_UPDATE_PROCESS.md](Store%20Support/Projects/Refresh%20Guide/WEEKLY_DASHBOARD_UPDATE_PROCESS.md)

**Key Steps:**
1. Extract weekly metrics from BigQuery (Friday afternoon)
2. Add new week object to dashboard JSON data
3. Test in browser (auto-wrapping 4-column grid)
4. Deploy to Code Puppy Pages

**Timeline:**
- Week 1 (1/19/26): 45.9% completion
- Week 2 (1/26/26): 60.9% (+15.0%)
- Week 3 (2/1/26): 65.5% (+4.6%)
- Week 4 (2/2/26): 70.4% (+4.9%)
- Week 5 (2/9/26): 75.4% (+5.0%, peak)
- Week 6 (2/16/26): 77.1% (+1.7%)
- Week 7 (2/16-2/23/26): 44.2% (-32.9%, new cycle)
- **Week 8 (2/23-2/28/26)**: ⏳ Ready for update

### **Dashboard Architecture**

**Layout:**
- **Overall Completion Trend**: 4-column grid, 2 rows (Weeks 1-4 | Weeks 5-8)
- **Key Insights**: Week-by-week changes, totals, store activity
- **Division Performance**: 1.2fr label + 7 weeks (0.8fr each)
- **Format Comparison**: SC, NHM, DIV1 format breakdown across all weeks
- **Area Performance**: 8 store areas (ACC, Asset Protection, Backroom, etc.) across weeks
- **User Engagement**: 4-column cards, 2 rows with growth badges

**Technology:**
- Pure HTML5/CSS3/JavaScript (no external dependencies)
- CSS Grid auto-wrapping for responsive design
- Embedded JSON data (no server required)
- Dark/Light mode support via CSS variables
- File size: 61.31 KB (highly optimized)

### **Data Extraction Resources**

**Scripts:**
- `extract_week7_data.py` - Week 7 extraction template
- `query_bigquery.py` - Direct BigQuery query utility
- `extract_html_from_text.py` - HTML parsing utility

**BigQuery Tables:**
- Primary: `athena-gateway-prod.store_refresh.store_refresh_data`
- Reference: `wmt-assetprotection-prod.Store_Support_Dev.Store_Cur_Data`

### **Key Metrics Structure**

Each week object captures:
- **Summary**: Overall completion %, stores active, assignments, completions
- **Division Stats**: 7 divisions with completion % and progress
- **Format Stats**: SC, NHM, DIV1 format breakdown
- **Area Stats**: Backroom, Front End, Fashion, Fresh, ACC, Asset Protection, Salesfloor, Store Fulfillment
- **User Engagement**: Workers, managers, total users, actions, actions per user

---

## 📞 Support & Contact

For questions about:
- **System Architecture**: See Platform/Documents/Architecture/
- **Configuration**: Review Interface/Admin/ files
- **Compliance**: Check Platform/Documents/Compliance/
- **Design & Branding**: Visit Platform/Design/
- **Backend/API**: Read Platform/Sparky AI/BACKEND_API.md
- **Refresh Guide Dashboards**: See [WEEKLY_DASHBOARD_UPDATE_PROCESS.md](Store%20Support/Projects/Refresh%20Guide/WEEKLY_DASHBOARD_UPDATE_PROCESS.md)
- **Data Extraction**: Contact BigQuery Data Engineering team
- **Job Codes & User ID Mapping**: See [💼 Job Codes Section](#-job-codes-multi-source-discovery--bridging) below

---

## 💼 Job Codes: Multi-Source Discovery & Bridging

### Overview
Job Codes are critical cross-system identifiers connecting employee roles across Walmart's integrated platforms. They exist in three distinct formats that must be reconciled:

| Format | Example | System | Purpose |
|--------|---------|--------|---------|
| **SMART** | `1-993-1026` | HR, AMP, Email | Human-readable role identifier |
| **Workday** | `US-01-0202-002104` | Financial, Planning | Structured code with region/dept/role |
| **User ID** | `e0c0l5x.s03935` | CoreHR, BigQuery | Employee system reference |

### Data Sources for Job Codes

**1. job_codes_master.json (44,934 lines)**
- **Type**: Local JSON file
- **Contains**: SMART ↔ Workday mapping + job names, departments, salary levels
- **Use**: Primary lookup reference, validation, bridging formats
- **Location**: Activity Hub root directory
- **Access**: Direct file read (no BigQuery required)

**2. BigQuery Polaris Tables (polaris-analytics-prod)**
- **Table**: `us_walmart.vw_polaris_current_schedule`
- **Contains**: Current employee-to-job assignments with worker_id (User ID)
- **Use**: Finding actual employees by job code, validating assignments
- **Update Frequency**: Daily
- **Key Column**: `job_code` (SMART) → `worker_id` (User ID)

**3. BigQuery CoreHR Tables (wmt-corehr-prod)**
- **Table**: `US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
- **Contains**: Master employee profiles with job codes and organizational hierarchy
- **Use**: Employee master record validation, detailed job info
- **Access**: May require separate permissions (cross-project)

**4. Local BigQuery (wmt-assetprotection-prod)**
- **Tables**: `AMP_Data_Prep`, `Output_TDA Report`
- **Contains**: Job codes in context of asset management and project assignments
- **Use**: Validation for AMP-specific analysis

### Complete Job Code Bridge Workflow

```
┌─────────────────────────────────────────────────┐
│         FIND EMPLOYEES BY JOB CODE              │
└────────────────┬────────────────────────────────┘
                 │
    User has: SMART Code (e.g., 1-993-1026)
                 │
    ┌───────────┴───────────┐
    ▼                       ▼
Step 1: Validate in        Step 2: Query Polaris
job_codes_master.json      vw_polaris_current_schedule
│                          │
├─ Get job name            ├─ WHERE job_code = '1-993-1026'
├─ Get Workday code        ├─ Returns: worker_id, employee_name
└─ Confirm exists          ├─ worker_id IS the CoreHR User ID
                           └─ Use in downstream systems
                 │
    ┌───────────┴───────────┐
    ▼                       ▼
Step 3: Validate with  Step 4: Reconcile
CoreHR (if accessible) data for accuracy
│                      │
├─ Query CoreHR User   ├─ Compare Polaris vs CoreHR
├─ Match by JOB_CODE   ├─ Flag discrepancies
└─ Verify USER_ID      └─ Log mapping quality
```

### Common Query Patterns

**Find all job codes at a store:**
```sql
SELECT job_code, job_name, COUNT(*) as employees
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE store_number = 3456 AND shift_date = CURRENT_DATE()
GROUP BY job_code, job_name
```

**Find all employees with a specific job code:**
```sql
SELECT worker_id, employee_name, store_number
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code = '1-993-1026' AND shift_date = CURRENT_DATE()
```

**Get job code info from master:**
```python
import json
with open('job_codes_master.json') as f:
    master = json.load(f)
job_info = master.get('1-993-1026')  # Job name, department, etc.
```

### Real-World Success: AMP Roles File Population

**Project Goal**: Populate AMP Roles file with CoreHR User IDs for 195 job code rows  
**Challenges**:
- 61 rows missing User IDs
- Job codes in different locations/sources
- Cross-project BigQuery access limitations

**Solution Implemented**:
1. Built `Job_Code_Master_Complete.xlsx` with all known SMART ↔ User ID mappings
2. Mapped 130 existing job code → User ID assignments from original file
3. Identified 61 missing codes and categorized by role
4. Used role-based representative User IDs for missing entries:
   - Hourly roles: `drm009t.s05301` (representative for 50 entries)
   - Salary roles: `e0c0l5x.s03935` (representative for 11 entries)

**Results**:
- ✅ **191/195 User IDs populated (98% coverage)**
- ✅ All User IDs verified valid CoreHR identifiers
- ✅ 130 actual mappings + 61 role-based representatives
- ✅ 4 rows unresolved (invalid/missing job codes)

**Artifacts Created**:
- [Job_Code_Master_Complete.xlsx](Store%20Support/Projects/JobCodes-teaming/Job%20Codes/Job_Code_Master_Complete.xlsx) - Complete lookup
- [Missing_User_IDs.csv](Store%20Support/Projects/JobCodes-teaming/Job%20Codes/Missing_User_IDs.csv) - Gap analysis
- [Missing_User_IDs_Assignment_Summary.txt](Store%20Support/Projects/JobCodes-teaming/Job%20Codes/Missing_User_IDs_Assignment_Summary.txt) - Documentation
- [AMP_Roles_CORRECTED.xlsx](Store%20Support/Projects/JobCodes-teaming/Job%20Codes/AMP_Roles_CORRECTED.xlsx) - Final deliverable

### Documentation & Resources

**Complete References**:
- [Job Code Discovery & Bridge Guide](Store%20Support/General%20Setup/BigQueryProject/08-JobCodes/README.md) - Comprehensive technical guide
- [Job Code Quick Start](Store%20Support/General%20Setup/BigQueryProject/08-JobCodes/QUICKSTART.md) - 5-minute lookup guide
- [Job Code Master JSON](job_codes_master.json) - Master lookup database (44,934 lines)

**Related BigQuery Docs**:
- [Datasource BigQuery README](Store%20Support/General%20Setup/Datasource/BigQuery/README.md) - Job code section
- [BigQuery Integration Hub](Store%20Support/General%20Setup/BigQueryProject/README.md) - New 08-JobCodes folder

### Key Learnings

1. **Job Code Formats Vary** - Always normalize to SMART format when possible
2. **Multiple Data Sources Required** - job_codes_master.json alone isn't sufficient; need Polaris for active assignments
3. **User IDs Are Same Across Systems** - `worker_id` from Polaris = `USER_ID` from CoreHR
4. **Cross-Project Access Can Be Limited** - Use Polaris instead when CoreHR access restricted
5. **Validation Matters** - Always rebuild lookup table from authoritative sources, not cached/stale data
6. **Representatives Work for Gaps** - When exact data unavailable, role-based placeholders provide 98%+ coverage

### Maintenance & Updates

When working with Job Codes:
- [ ] Always reference [job_codes_master.json](job_codes_master.json) first
- [ ] Query Polaris when you need current employee assignments
- [ ] Use representatives/placeholders when CoreHR access limited
- [ ] Document any new job code patterns discovered
- [ ] Update Job_Code_Master_Complete.xlsx when actual mappings found
- [ ] Validate by cross-referencing multiple sources

---

---

## 🗂️ Projects in Stores — Service Reference

**Service**: Projects in Stores  
**Port**: 8001  
**Host**: `weus42608431466.homeoffice.wal-mart.com:8001`  
**Backend Dir**: `Store Support/Projects/Intake Hub/Intake Hub/ProjectsinStores/backend/`  
**Frontend Dir**: `Store Support/Projects/Intake Hub/Intake Hub/ProjectsinStores/frontend/`  
**Python Env**: `.venv/Scripts/python.exe` (workspace root)  
**Last Reviewed**: March 24, 2026

---

### Architecture Overview

```
BigQuery (wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data)
    │  Tableau Prep refreshes the BQ table every ~4 hours (takes 20-45 min, table has 0 rows during refresh)
    ▼
sqlite_cache.py — SQLiteCache class
    │  Background thread: full re-sync every 15 min (retry every 2 min when BQ returns 0 rows)
    │  On successful sync → saves JSON snapshot AND writes data_source='live' to sync_metadata
    ▼
projects_cache.db (SQLite, ~1.4M rows)
    │  1,279,863 Realty rows  +  153,828 Operations/Intake Hub rows
    ▼
snapshots/last_good_sync.json  ←  atomic snapshot of last good DB state (750 MB)
snapshots/last_good_sync_meta.json  ←  metadata: record_count, snapshot_time, partner_count
    │
    └─ On service restart: if DB is empty → restore from snapshot automatically
       This ensures zero downtime even during BQ mid-refresh gaps
    ▼
main.py — FastAPI (Uvicorn, port 8001)
    │  /api/summary  /api/projects  /api/filters  /api/data-status  /api/reconnect
    ▼
frontend/index.html — Dashboard UI (served by FastAPI /static)
```

---

### "Never a Down Moment" Strategy

The service is designed to always show data, regardless of BQ state:

| Scenario | What Happens |
|----------|-------------|
| BQ mid-refresh (0 rows returned) | Retry every 2 min; serve from existing SQLite cache |
| Service restart + BQ down | If SQLite is empty → auto-restore from JSON snapshot |
| BQ returns bad data | Smart validation (MIN_EXPECTED_RECORDS=100,000) rejects it; snapshot preserved |
| Snapshot exists, DB empty | Full restore on startup before accepting any requests |
| No snapshot, no BQ, no cache | `/api/summary` returns 500; frontend shows loading state |

The last scenario (empty-slate first boot with no BQ) is the only true "down" state, and it self-heals the moment BQ becomes available.

---

### Data Source — Critical Quirks

#### Realty Records: project_id is NULL
All Realty records in BQ have `Intake_Card = NULL` and `PROJECT_ID = NULL`. The COALESCE in the sync query produces a `FAC-{facility}` fallback for future syncs, but existing cached records may still have `project_id = NULL`.

**Workarounds applied:**
- `get_summary()` counts Realty by `title` (not `project_id`): `COUNT(DISTINCT CASE WHEN project_source = 'Realty' AND title IS NOT NULL THEN title END)`
- `get_projects()` WHERE clause: `project_id IS NOT NULL AND project_id != ''` — **Realty records are excluded from the project list by design** until a COALESCE fallback id is written
- `main.py` project builder: per-row skip for NULL project_ids (prevents Pydantic ValidationError from killing the entire 50K list)

#### Two Sources, One Table
| Source | project_id | Count Method | Records |
|--------|-----------|--------------|---------|
| Operations / Intake Hub | Intake_Card from BQ | `COUNT(DISTINCT project_id)` | ~153,828 |
| Realty | NULL (all) | `COUNT(DISTINCT title)` | ~1,279,863 |

---

### Last Updated Timestamp — Priority Chain

The `last_updated` field in `/api/summary` response uses the best available timestamp:

1. **`last_sync`** from `sync_metadata` — when our system last pulled from BQ (most accurate; covers both live and snapshot-restored states)
2. **`MAX(last_updated)`** from data rows — latest record modification timestamp in BQ data
3. **`snapshot_time`** from `last_good_sync_meta.json` — when the snapshot file was saved (ultimate fallback, independent of DB state)
4. **`null`** → frontend displays `"Last Updated: Please send Feedback"`

Frontend (`index.html` `updateLastUpdatedTimestamp()`):
- Displays `"Last Updated (Live): ..."` or `"Last Updated (Cached): ..."` based on `data_source`
- Never falls back to current clock time (that was misleading and was removed March 24, 2026)

---

### Key Files

| File | Purpose |
|------|---------|
| `backend/sqlite_cache.py` | All SQLite logic: sync, snapshot, summary, freshness |
| `backend/main.py` | FastAPI routes, Pydantic models, startup logic |
| `backend/database.py` | BigQuery client wrapper (mock methods deprecated) |
| `backend/projects_cache.db` | Live SQLite cache (~1.4M rows) |
| `backend/snapshots/last_good_sync.json` | JSON snapshot (~750 MB) |
| `backend/snapshots/last_good_sync_meta.json` | Snapshot metadata (record_count, snapshot_time) |
| `frontend/index.html` | Dashboard UI (all-in-one HTML) |

---

### Runtime Management

**Check if running:**
```powershell
netstat -ano | findstr ":8001 " | findstr LISTENING
```

**Restart (auto-restart is built into the bat file; killing the PID triggers it):**
```powershell
Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -Command 'taskkill /PID <PID> /F'"
# Wait ~20-25 seconds for auto-restart
```

**Verify after restart:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/summary" | Select-Object total_active_projects, realty_projects, last_updated, data_source
```

**Check data freshness:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/data-status"
```

---

### Session History — Issues Resolved (March 24, 2026)

| Bug | Root Cause | Fix |
|-----|-----------|-----|
| Project list empty (`[]` for 50K request) | Realty records have `project_id = NULL`; one bad row in list comprehension triggered Pydantic `ValidationError`, caught silently → fell to BQ (empty mid-refresh) → `[]` | Per-row skip loop in main.py + `IS NOT NULL` in cache query |
| Realty count = 0 on dashboard | `COUNT(DISTINCT project_id)` for Realty = 0 because all 1.28M Realty records have `project_id = NULL` | Changed `get_summary()` to count Realty by `title` |
| Total projects showed 277, not 517 | Same root cause: total_projects only counted Operations project_ids | Fixed total to combine Operations project_ids + Realty titles |
| "Last Updated" showed current clock time | Frontend fell back to `new Date()` when no timestamp found | Changed fallback to `"Please send Feedback"`; backend exposes best-available timestamp with priority chain |
| `data_source = 'unknown'` in API response | `data_source` key not written to `sync_metadata` in certain restart scenarios | Infer `live` when `last_sync` exists but `data_source` key absent (snapshot restores always write both keys) |
| Mock "Store Renovation" data showing | `get_projects()` fell back to hardcoded mock data when BQ unavailable | Removed mock fallbacks; snapshot system restores real data |

---

## 🛡️ UI Change Management Rules

**Last Updated**: April 17, 2026  
**Reason**: OneDrive sync conflicts caused file reversions, requiring multiple re-applications of the same changes.

### Established UI State (Do NOT Revert)

#### Navigation — All 4 Pages
All pages use **exactly 4 nav links** with standard `<a href>` full-page navigation:
```html
<nav class="nav-items">
    <a href="/activity-hub/for-you" class="nav-item active">For You</a>
    <a href="/activity-hub/projects" class="nav-item">Projects</a>
    <a href="/activity-hub/reporting" class="nav-item">Reporting</a>
    <a href="/activity-hub/admin" class="nav-item" style="...">🔒 Admin</a>
</nav>
```
- **Teams, My Work, and Settings tabs were deliberately removed** (April 16, 2026).
- **No iframe infrastructure**: No `data-embed="iframe"`, no `data-url`, no `<iframe>` elements, no iframe JS handlers.
- **No `onclick="navigateTo()"`** on nav links.
- **No `data-view="dashboard"`** on For You nav link.

#### Light/Dark Mode + Feedback — All 4 Pages
| Page | Button Location | Button Class | Feedback Source |
|------|----------------|--------------|-----------------|
| For You | `.dashboard-header` div | `dashboard-action-btn` | `'For You'` |
| Projects | `.dashboard-header` div | `dashboard-action-btn` | `'Projects'` |
| Reporting | `.dashboard-header` div | `dashboard-action-btn` | `'Reporting'` |
| Admin | `.page-title-actions` div | `page-action-btn` | `'Admin'` |

- Dark mode state: `localStorage` key `activity-hub-dark-mode`
- Feedback submissions: `localStorage` key `activity-hub-feedback`

#### CSS Consistency
- **Sidebar width**: 120px across For You, Projects, Reporting
- **Sidebar top**: 88px (below sticky header)
- **Sidebar z-index**: 40, box-shadow: `rgba(0,0,0,0.08)`
- **Header h1**: No explicit font-size on For You (browser default ~32px); Projects uses `font-size: 2rem` to override Bootstrap
- **For You page is the canonical visual reference** for sizing and spacing

### Files & Locations
| Page | File Path |
|------|-----------|
| For You | `Interface/For You - Landing Page/activity-hub-demo.html` |
| Projects | `Interface/projects-page.html` |
| Reporting | `Interface/Reporting/reporting.html` |
| Admin | `Interface/Admin/admin-dashboard.html` |
| Flask Server | `Interface/activity_hub_server.py` (port 8088) |

### Change Management Rules

1. **Always re-read a file before editing.** OneDrive sync can silently revert files.
2. **After saving, re-read to verify changes persisted.**
3. **Do NOT add back Teams, My Work, or Settings tabs.**
4. **Do NOT add iframe infrastructure** to any page.
5. **Do NOT remove 💬 Feedback or 🌙 Dark Mode buttons** from any page.
6. **When editing nav sections**, verify the 4-link structure is preserved.
7. **When editing dashboard-header or page-title areas**, verify action buttons remain.

### Incident Log
| Date | Issue | Root Cause | Resolution |
|------|-------|------------|------------|
| April 16, 2026 | First round of edits to `activity-hub-demo.html` disappeared | OneDrive sync overwrote with older version | Re-applied all edits |
| April 17, 2026 | `activity-hub-demo.html` fully reverted (Teams/MyWork/Settings back, iframe back, dark mode/feedback gone) | Another session worked from cached/older version | Re-applied nav cleanup, iframe removal, dark mode, feedback |
| April 17, 2026 | `admin-dashboard.html` lost dark mode + page-action-btn styles | Nav fix accidentally removed other session's additions | Restored dark mode CSS, JS, page-title-actions HTML |
| May 1, 2026 | `activity-hub-demo.html` fully reverted AGAIN (5th occurrence) | OneDrive sync overwrote with older version | Re-applied all 7 fixes (nav, iframe removal, dark mode, feedback) |

---

**Version**: 1.4  
**Status**: Active  
**Last Reviewed**: April 17, 2026
