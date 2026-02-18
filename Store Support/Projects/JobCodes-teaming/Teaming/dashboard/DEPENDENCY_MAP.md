# Job Code Teaming Dashboard - Dependency Map

## System Architecture - Component Dependencies

```
┌──────────────────────────────────────────────────────────────────┐
│                         Browser Client                           │
│                      (User Interface)                            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ frontend/index.html (Static HTML/CSS/JavaScript)          │  │
│  │  - Login page                                              │  │
│  │  - Job codes display                                       │  │
│  │  - Request submission form                                 │  │
│  │  - Admin approval dashboard                                │  │
│  │  - Export interface                                        │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                    HTTP/JSON Requests
                           │
┌──────────────────────────▼───────────────────────────────────────┐
│                  FastAPI Backend Server                          │
│              backend/main.py (1584 lines)                        │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Dependencies (Python Packages)                          │    │
│  ├─ fastapi                (Web framework)                 │    │
│  ├─ uvicorn                (ASGI server)                   │    │
│  ├─ pandas                 (Data processing)               │    │
│  ├─ openpyxl               (Excel reading)                 │    │
│  ├─ smtplib                (Email sending - stdlib)        │    │
│  └─ hashlib                (Password hashing - stdlib)     │    │
│  └─ json                   (Data storage - stdlib)         │    │
│  └─ threading              (Background tasks - stdlib)     │    │
│  └─ datetime               (Timestamps - stdlib)           │    │
│                                                              │    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ API Endpoints (Routes)                                  │    │
│  ├─ POST /login            → HttpBasic auth               │    │
│  ├─ GET  /job-codes        → Load from master JSON        │    │
│  ├─ POST /update-request   → Save to update_requests.json│    │
│  ├─ POST /approve-request  → Update requests (admin only) │    │
│  ├─ GET  /export           → Generate CSV (admin only)    │    │
│  ├─ GET  /user-profile     → Get current user             │    │
│  ├─ POST /register         → Create new user              │    │
│  └─ POST /send-email       → Queue email notification    │    │
│                                                              │    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Core Functions                                          │    │
│  ├─ load_users()           → Read users.json              │    │
│  ├─ load_job_codes()       → Read job_codes_master.json   │    │
│  ├─ load_teaming_data()    → Read TMS Excel file          │    │
│  ├─ load_polaris_data()    → Read polaris_job_codes.csv   │    │
│  ├─ merge_job_codes()      → Combine sources              │    │
│  ├─ process_request()      → Handle user submissions      │    │
│  ├─ export_requests()      → Generate TMS format CSV      │    │
│  └─ send_email_async()     → Background email threading   │    │
│                                                              │    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Authentication & Session                                │    │
│  ├─ HTTPBasic security scheme                              │    │
│  ├─ Password verification (SHA256 hash)                    │    │
│  └─ Session token generation                               │    │
│                                                              │    │
└──────────────────────────┬───────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┬──────────────────┐
           │ Read/Write    │               │                  │
           │               │               │                  │
      ┌────▼───┐      ┌────▼──────┐  ┌────▼──────┐      ┌────▼────┐
      │ Input  │      │ JSON Data │  │ External  │      │  SMTP   │
      │ Files  │      │ Storage   │  │ Systems   │      │ Gateway │
      │        │      │           │  │           │      │         │
      │ Sources│      │ (data/)   │  │ Integrations
      │  ──    │      │  ──────   │  │  ────────  │      │  ────   │
      │        │      │           │  │           │      │         │
      ├──────┤       ├─────────┤  ├─────────┤  ├────────┤
      │ *.xlsx │       │users.json│  │BigQuery │  │Walmart  │
      │        │       │          │  │  (via   │  │ SMTP    │
      │ *.csv  │       │sessions  │  │  CSV   │  │         │
      │        │       │ .json    │  │ export) │  │smtp-gw1 │
      │ Data...│       │          │  │         │  │.homeoffe│
      │        │       │update_   │  │ (polaris│  │ice.wal- │
      │Sources │       │requests  │  │_job_    │  │mart.com │
      │        │       │ .json    │  │codes.   │  │ :25     │
      │  ─┬─   │       │          │  │csv)     │  │         │
      │   │    │       │job_code_ │  │         │  │→ Email  │
      │   ├─ TMS│       │requests  │  │ Python  │  │ Notifi- │
      │   │ Data       │ .json    │  │ Pandas  │  │cation   │
      │   │ (3).       │          │  │ query   │  │         │
      │   │   xlsx     │job_codes │  │ library │  │to:      │
      │   │            │_master   │  │         │  │ATCTEAM  │
      │   │ ┌────────┐ │ .json    │  │         │  │SUPPORT  │
      │   ├─►│Teaming│  │          │  │         │  │@walmart │
      │   │  │Data   │  │email_    │  │         │  │.com     │
      │   │  │(3).   │  │queue.json│  │         │  │         │
      │   │  │xlsx   │  │          │  │         │  │         │
      │   │  └────────┘ │email_    │  │         │  │         │
      │   │            │config    │  │         │  │         │
      │   ├─ Polaris   │ .json    │  │         │  │         │
      │   │ Job Codes  │          │  │         │  │         │
      │   │ (from      │rejection │  │         │  │         │
      │   │ BigQuery)  │_history  │  │         │  │         │
      │   │            │ .json    │  │         │  │         │
      │   │ ┌────────┐ │          │  │         │  │         │
      │   └─►│polaris│  └─────────┘  │         │  │         │
      │      │_job_  │                │         │  │         │
      │      │codes  │                │         │  │         │
      │      │.csv   │                │         │  │         │
      │      └────────┘                │         │  │         │
      │                               │         │  │         │
      │ ┌────────────────┐            │         │  │         │
      │ │polaris_user_   │            │         │  │         │
      │ │counts.csv      │            │         │  │         │
      │ └────────────────┘            │         │  │         │
      │                                │         │  │         │
      └────────────────────────────────┴─────────┴──┴─────────┘
```

---

## Data Flow Dependencies

```
┌─ STARTUP INITIALIZATION ─────────────────────────┐
│                                                   │
│  1. main.py starts                              │
│     ├─► Loads users.json (if exists)            │
│     ├─► Loads TMS Data (3).xlsx                 │
│     ├─► Loads polaris_job_codes.csv             │
│     ├─► Loads polaris_user_counts.csv (optional)│
│     └─► Merges into job_codes_master.json       │
│                                                   │
│  2. Uvicorn server binds to 0.0.0.0:8080       │
│     └─► Serves frontend/index.html              │
│                                                   │
└───────────────────────────────────────────────────┘
                        │
                        ▼
┌─ USER LOGIN FLOW ─────────────────────────────────┐
│                                                   │
│  Browser → POST /login                           │
│  ├─► Backend: Verify credentials vs users.json   │
│  ├─► Generate session token                      │
│  ├─► Store in sessions.json                      │
│  └─► Return token to browser                     │
│                                                   │
└───────────────────────────────────────────────────┘
                        │
                        ▼
┌─ VIEW JOB CODES FLOW ─────────────────────────────┐
│                                                   │
│  Browser → GET /job-codes                        │
│  ├─► Backend: Load job_codes_master.json         │
│  ├─► Apply role-based filtering                  │
│  ├─► Filter: Remove already-assigned codes      │
│  └─► Return JSON to browser for display          │
│                                                   │
└───────────────────────────────────────────────────┘
                        │
                        ▼
┌─ SUBMIT TEAMING REQUEST FLOW ─────────────────────┐
│                                                   │
│  Browser: User selects job code + team           │
│  ├─► POST /update-request                        │
│  ├─► Backend: Validate request data              │
│  ├─► Append to update_requests.json              │
│  ├─► Queue email in email_queue.json             │
│  ├─► Background thread sends email via SMTP      │
│  │   └─► ATCTEAMSUPPORT@walmart.com              │
│  └─► Return confirmation JSON                    │
│                                                   │
└───────────────────────────────────────────────────┘
                        │
                        ▼
┌─ ADMIN APPROVAL FLOW ─────────────────────────────┐
│                                                   │
│  Admin: Reviews requests dashboard                │
│  ├─► GET /requests (admin only)                  │
│  │   ├─► Load update_requests.json               │
│  │   └─► Show pending approvals                   │
│  ├─► POST /approve-request (admin only)          │
│  │   ├─► Update request status in JSON           │
│  │   ├─► Remove job code from "missing" list    │
│  │   └─► Update job_codes_master.json            │
│  └─► POST /export (admin only)                   │
│      ├─► Generate CSV format                      │
│      ├─► Include job code + team mapping          │
│      └─► Download to user's computer              │
│                                                   │
└───────────────────────────────────────────────────┘
```

---

## File Dependencies Matrix

### Dependency Table: What Reads What

| Component | Reads From | Writes To | Purpose |
|-----------|-----------|-----------|---------|
| **main.py startup** | TMS Data (3).xlsx | job_codes_master.json | Initialize job code list |
| | polaris_job_codes.csv | | |
| **Authentication** | users.json | sessions.json | User login & session tracking |
| **Job Code Display** | job_codes_master.json | (none) | Show available codes |
| **Request Processing** | job_codes_master.json | update_requests.json | Store user submissions |
| | (validates against) | email_queue.json | |
| **Admin Approval** | update_requests.json | update_requests.json | Approve/reject requests |
| | users.json | job_codes_master.json | Update status |
| **Email System** | email_queue.json | email_config.json | Track notifications sent |
| **User Management** | users.json | users.json | Add/edit/delete users |
| **Export** | update_requests.json | (download to user) | Generate TMS format |

---

## External System Dependencies

```
┌─────────────────────────────────────────┐
│      External Systems Integration       │
└─────────────────────────────────────────┘
           │          │          │
           │          │          │
    ┌──────▼┐  ┌──────▼┐  ┌──────▼─────┐
    │Teaming│  │Polaris│  │  Walmart   │
    │(TMS)  │  │(HRIS) │  │  SMTP      │
    │       │  │       │  │  Gateway   │
    │Data   │  │BigQuery  │            │
    │Source │  │Export │  │ Email      │
    │       │  │       │  │ Service    │
    │*.xlsx │  │*.csv  │  │            │
    │file   │  │file   │  │            │
    └──────┬┘  └──────┬┘  └──────┬─────┘
           │          │          │
         Input      Input     Output
           │          │          │
    ┌──────▼──────────▼──────────▼─────┐
    │      FastAPI Backend              │
    │      (main.py)                    │
    └───────────────────────────────────┘
           │          │
           │          ├─ Frontend (Static)
           │          └─ index.html
           │
        Browser
     (User Access)
```

---

## Python Package Dependencies

### Direct Dependencies (in main.py)

```
fastapi              → Web framework
  └─ depends on:
     ├─ starlette
     ├─ pydantic
     └─ typing

uvicorn              → ASGI server
  └─ depends on:
     ├─ asgiref
     └─ click

pandas               → Data manipulation
  └─ depends on:
     ├─ numpy
     ├─ python-dateutil
     └─ pytz

openpyxl             → Excel file reading
  └─ depends on:
     ├─ et-xmlfile
     └─ lxml (optional)

smtplib              → Built-in (Python stdlib)
                       Email protocol

hashlib              → Built-in (Python stdlib)
                       Cryptographic hashing

json                 → Built-in (Python stdlib)
                       JSON encoding/decoding

threading            → Built-in (Python stdlib)
                       Background tasks

datetime             → Built-in (Python stdlib)
                       Date/time handling
```

---

## Request/Response Dependencies

### API Endpoint Chain

```
GET /job-codes
├─ Requires: Valid session token
├─ Reads: job_codes_master.json
├─ Filters: By user role (Admin/User)
└─ Returns: JSON array of job code objects

POST /update-request
├─ Requires: User authentication
├─ Reads: job_codes_master.json (validation)
├─ Writes: update_requests.json (append)
├─ Triggers: Background email thread
│   └─ Sends to: ATCTEAMSUPPORT@walmart.com
└─ Returns: {"status": "submitted", "id": "..."}

POST /approve-request
├─ Requires: Admin authentication
├─ Reads: update_requests.json
├─ Modifies: update_requests.json
├─ Depends on: job_codes_master.json
└─ Returns: {"status": "approved", "jobCode": "..."}

GET /export
├─ Requires: Admin authentication
├─ Reads: update_requests.json
├─ Formats: CSV (TMS-compatible)
└─ Returns: File download (binary)
```

---

## Initialization Sequence

**Correct startup order:**

1. **Python environment**: `.code-puppy-venv` must be activated
2. **Working directory**: `dashboard/` folder
3. **Backend dependencies**: Packages installed (fastapi, uvicorn, pandas, openpyxl)
4. **Data files exist**: 
   - `../TMS Data (3).xlsx` ✓
   - `../polaris_job_codes.csv` ✓
5. **Data directory**: `data/` folder exists (auto-created if missing)
6. **main.py starts**: Loads all data sources into JSON
7. **Uvicorn runs**: Server listens on 0.0.0.0:8080
8. **Frontend served**: index.html available at /static/
9. **Browser access**: http://LEUS62315243171.homeoffice.wal-mart.com:8080/static/index.html

---

## Circular Dependencies & Considerations

⚠️ **Potential Issues:**

| Issue | Cause | Prevention |
|-------|-------|-----------|
| Stale job code data | Excel file not updated | Schedule refresh or manual reload |
| Email failures | SMTP server unreachable | Test SMTP connection independently |
| Duplicate requests | Concurrent submissions | Backend validates timestamps |
| Session expiration | Long-running operations | Session timeout after N minutes |
| File locking | Multiple processes access JSON | Use file-based locking or DB |

---

## Summary

### Critical Dependencies
1. Backend depends on: **Python + FastAPI + Uvicorn**
2. Data depends on: **TMS Excel + Polaris CSV files**
3. Network depends on: **Firewall rule + VPN access**
4. Email depends on: **SMTP gateway + Walmart VPN**

### Data Ownership
- **Teaming data** → Source: TMS system (external)
- **Job codes** → Source: Polaris/BigQuery (external)
- **User data** → Managed locally (users.json)
- **Requests** → Managed locally (update_requests.json)
