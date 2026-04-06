# Activity Hub Logic Rules Engine

## Overview

The Logic Rules Engine is the central orchestration system for Activity Hub that manages composite "Logic Requests" containing notification, task, and next-step components.

**Key Capabilities:**
- Admins create Logic Requests that may include one or more components (Notification, Task, Next Steps)
- Single approval flow for entire request, but child rules can be edited independently after approval
- Central Scheduler Service monitors for trigger events and executes matched rules automatically
- Audit trail for all approvals and executions

## System Architecture

```
Admin Dashboard (Interface/Admin/admin-dashboard.html)
  └─ Logic Tab → Notification Alerts sub-tab
       ├─ Create Logic Request form
       └─ Pending Approvals dashboard

Scheduler Service (Interface/Admin/Logic/Scheduler/main.py) - Port 5011
  ├─ TriggerDetector: Monitors projects table for new projects
  ├─ RuleEvaluator: Finds matching active rules
  └─ RuleExecutor: Executes notification, task, and next-step components
       ├─ Notification delivery (Email, In-App, Teams, Slack)
       ├─ Task creation (Phase 2)
       └─ Next Steps (Phase 2)

BigQuery Tables (wmt-assetprotection-prod.Store_Support_Dev)
  ├─ logic_requests - Parent requests
  ├─ notification_logic_rules - Notification child rules
  ├─ scheduler_execution_log - Execution audit trail
  ├─ notification_deliveries -  Final sent notifications
  ├─ notification_user_preferences - User settings
  └─ logic_request_approvals - Approval history
```

## Component Status

| Component | Status | Phase |
|-----------|--------|-------|
| Logic Request CRUD | ✅ Implemented (UI + schema) | 1 |
| Single Approval Workflow | ✅ Designed | 1 |
| Scheduler Service | ✅ Implemented | 1 |
| Notification Execution | ✅ Implemented (email + in-app) | 1 |
| BigQuery Tables | ✅ Schema created | 1 |
| Admin Dashboard Integration | ✅ Form added | 1 |
| User Preferences | ⚠️ Schema only | 1-2 |
| Task Logic Component | ⚠️ Placeholder | 2 |
| Next Steps Component | ⚠️ Placeholder | 2 |

## Custom Trigger Workflow

### Problem
Admins may need to create Logic Requests based on triggers that don't yet exist in the system (e.g., "project hasn't had a note in 30 days"). These require backend implementation to detect.

### Solution: 3-Step Validation Process

```
Step 1: Admin Submits Logic Request
┌─────────────────────────────────┐
│ Form: Trigger Type = "Custom..." │
│ Input: "Project no note > 30d"   │
└─────────────────────────────────┘
         ↓
Step 2: Admin Reviews & Approves (Pending Implementation)
┌──────────────────────────────────────────┐
│ Status: PENDING_APPROVAL                 │
│ Flag: ⚠️ Custom Trigger (Requires Impl)  │
│ Trigger: "Project no note > 30d"         │
│ Action: Approve (confirms requirement) OR Reject
└──────────────────────────────────────────┘
         ↓
Step 3: Backend Developer Implements & Converts to Standard
┌────────────────────────────────────────────┐
│ File: TriggerDetector.detect() method      │
│ Task: Write SQL query for "no note > 30d"  │
│ Result: Trigger becomes standard option    │
│ Next Requests: Dropdown shows new option   │
└────────────────────────────────────────────┘
```

### Custom Trigger Requirements for Approval

When Admin sees a Logic Request with a **Custom Trigger**, approval means:

1. ✅ **Admin confirms** the trigger requirement is valid and useful
2. ⚠️ **Implementation pending** - Backend must add detection SQL
3. 📋 **Trigger label captured** - Custom trigger text stored for developer reference
4. 🔄 **Conversion plan** - Once implemented, trigger becomes standard option

### Backend Implementation Checklist

When implementing a custom trigger in the approval queue:

- [ ] **Locate trigger** in `Interface/Admin/Logic/Scheduler/main.py`, class `TriggerDetector`
- [ ] **Add SQL query** to detect the condition (use Polaris BigQuery tables)
- [ ] **Add trigger option** to trigger dropdown in `admin-dashboard.html`
- [ ] **Test** trigger detection with sample data
- [ ] **Update** any Logic Request using this custom trigger to reference standard option instead
- [ ] **Mark complete** in approval notes

**Example Implementation:**

```python
# In TriggerDetector.detect()
elif trigger_type == 'project_no_note_30d':
    # Query: Projects without note in 30+ days
    query = """
    SELECT p.project_id FROM projects p
    LEFT JOIN project_notes n ON p.project_id = n.project_id
        AND n.created_at > CURRENT_TIMESTAMP() - INTERVAL 30 DAY
    WHERE n.project_id IS NULL
    """
```

Then add to dropdown:
```html
<option value="project_no_note_30d">Project Has No Note (30+ Days)</option>
```
| Teams Integration | ⚠️ Placeholder | 2 |
| Slack Integration | ⚠️ Placeholder | 2 |

## Folder Structure

```
Interface/Admin/Logic/
├── Notification-Alerts/          # Notification component module
│   └── backend/                   # Notification-specific services
├── Task-Logic/                    # Task component module (TBD)
├── Next-Steps/                    # Next Steps component module (TBD)
├── Scheduler/                     # Central Scheduler Service
│   ├── main.py                    # Scheduler FastAPI server
│   ├── requirements.txt           # Python dependencies
│   └── modules/                   # Scheduler modules
│       ├── trigger_detector.py    # (embedded in main.py currently)
│       ├── rule_evaluator.py      # (embedded in main.py currently)
│       └── rule_executor.py       # (embedded in main.py currently)
├── Config/                        # Configuration files
├── Schemas/                       # Database schemas
│   ├── bigquery_tables.sql        # Table definitions
│   └── SCHEMA_DOCUMENTATION.md    # Detailed schema docs
├── README.md                      # This file
├── DEPLOYMENT.md                  # Deployment guide
└── LOGIC_REQUEST_GUIDE.md         # Admin usage guide
```

## Quick Start

### 1. Create BigQuery Tables

Run the SQL in [Schemas/bigquery_tables.sql](Schemas/bigquery_tables.sql) in BigQuery Console:

```sql
-- Copy and paste from Schemas/bigquery_tables.sql
-- Target: wmt-assetprotection-prod.Store_Support_Dev
```

### 2. Start Scheduler Service

```powershell
# Navigate to scheduler folder
cd "Interface\Admin\Logic\Scheduler"

# Install dependencies
pip install -r requirements.txt

# Set BigQuery credentials
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\application_default_credentials.json"

# Run scheduler
python main.py
```

Service will start on `http://localhost:5011`

Health check: `http://localhost:5011/health`

### 3. Access Admin Dashboard

Navigate to Admin Dashboard → Logic tab → Notification Alerts sub-tab

- **Create Logic Request**: Fill form and click "Submit for Approval"
- **View Pending**: See pending approvals with pending count badge
- **Approve**: Click "Approve" on pending request
- **View Active Rules**: See all active rules and their execution metrics

## How It Works

### Scenario: SIF Meeting Notification for New Projects

**1. Admin Creates Logic Request**
```
Name: "SIF Meeting Notification for New Projects"
Trigger: When new project created
Components:
  ☐ Notification ← Selected
  ☐ Task
  ☐ Next Steps
```

**2. Admin Configures Notification Component**
```
Category: PROJECT_LIFECYCLE
Title: "Action Required: Submit SIF Meeting for {project_name}"
Message: "Please submit your SIF meeting request by clicking the link below"
Recipients: Project Owner
Channels: Email, In-App
Schedule: Immediate
```

**3. Admin Submits for Approval**
- Request saved to `logic_requests` table with status = "pending_approval"
- System generates approval notification to admins (itself!)
- Admin receives email/in-app notification with approval link

**4. Admin Approves**
- Status changes to "approved" → "active"
- Child rule created in `notification_logic_rules` table
- Approval recorded in `logic_request_approvals` table

**5. Scheduler Detects Trigger**
- Every 5 minutes, Scheduler queries projects table
- Detects: New project created 2 minutes ago
- Finds: "SIF Meeting Notification" rule matches trigger

**6. Scheduler Executes**
- Loads notification rule
- Renders templates: "SIF Meeting Required: Project Alpha"
- Looks up owner: john.doe@walmart.com
- Checks user preferences: Wants email + in-app
- Delivers:
  - Email sent via Walmart SMTP
  - In-app notification created in `notification_deliveries`
- Logs execution in `scheduler_execution_log`

**7. Owner Receives**
- Email with clickable link to SIF form
- In-app notification in For You page bell
- Clicks link → goes to SIF form portal

## API Endpoints

### Scheduler Service (Port 5011)

#### Health & Status
- `GET /health` - Health check
- `GET /api/v1/scheduler/status` - Scheduler metrics (last 24h)

#### Logic Requests
- `GET /api/v1/logic-requests?status=approved&limit=50` - List active requests
- `POST /api/v1/notifications/ingest` - (Phase 2) Platforms submit notifications

#### Audit & Logs
- `GET /api/v1/execution-log?limit=100` - Recent executions

### Admin Dashboard (Port 8001)

#### Logic Tab Integration
- Form submission → Saves to BigQuery `logic_requests` table
- Approval button → Updates status + creates child rules
- Real-time updates from Scheduler Service → Dashboard refreshes

## Next Steps (Phase 2)

1. **Task Logic Component**
   - Design task creation rules
   - Implement task executor
   - Test end-to-end with Notification

2. **Next Steps Component**
   - Design next steps generation
   - Implement next steps executor

3. **Multi-Platform Triggers**
   - Expand from Projects to Tour Guide, Roster
   - Add trigger event registration API

4. **Teams & Slack Integration**
   - Implement Teams messaging
   - Implement Slack webhooks

5. **Advanced Features**
   - Approval chain (multiple approvers)
   - Conditional logic in rules
   - Custom template variables
   - Throttling & deduplication

## Files

- [DEPLOYMENT.md](DEPLOYMENT.md) - How to deploy Scheduler Service
- [SCHEMA_DOCUMENTATION.md](Schemas/SCHEMA_DOCUMENTATION.md) - Detailed database schema
- [LOGIC_REQUEST_GUIDE.md](LOGIC_REQUEST_GUIDE.md) - Admin user guide (TBD)

## Support

For issues or questions:
1. Check `Interface/Admin/Logic/Scheduler/` logs
2. Query `Scheduler_execution_log` table in BigQuery
3. Review pending approvals in Admin Dashboard
