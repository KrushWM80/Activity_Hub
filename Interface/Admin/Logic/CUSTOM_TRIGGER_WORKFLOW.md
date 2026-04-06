# Custom Trigger Validation Workflow

**Document Date:** April 6, 2026  
**Owner:** Kendall Rush  
**Status:** ✅ Implemented in UI (April 6, 2026)

## Executive Summary

Custom Triggers enable admins to request Logic Request functionality that doesn't yet exist in the system. A **3-step validation workflow** ensures that:
1. Admin can express new trigger requirements as custom triggers
2. Requirements remain visible to admin/backend until implemented
3. Once implemented, triggers become standard dropdown options
4. System prevents incomplete custom triggers from silently failing

## Problem Statement

### Before Custom Triggers
- Admin needs: "Send notification when project hasn't had a note in 30 days"
- System limitation: Only predefined triggers available (new_project, status_changed, etc.)
- Result: Requirement goes unfulfilled; admin has no way to express need through UI

### With Custom Triggers
- Admin can describe ANY trigger condition they need
- Request captures the requirement for backend review
- Backend implements detection SQL and converts to standard option
- Future admins see it as standard dropdown choice (no custom flag)

## Design: 3-Step Validation

### Phase 1: Admin Submits Logic Request with Custom Trigger

**UI Location:** Logic → Notification Alerts → "Create New Logic Request" button → Modal Form

**Form Field:**
```
Trigger Type: [Dropdown]
  - New Project Created
  - Project Status Changed
  - Task Assigned
  - Task Overdue
  - Custom Trigger... (Requires Implementation)  ← User selects this
```

**Additional Input When "Custom..." Selected:**
```
Custom Trigger Description *
[Text Input]
Default: "Project has not had a note in more than 30 days"

⚠️ Requires Implementation: Your custom trigger will be 
reviewed for approval, but full activation requires backend 
implementation. Validation steps:
  1. Admin approves Logic Request
  2. Backend developer implements trigger detection SQL
  3. Trigger becomes standard option in dropdown
  4. Logic Request fully activates with standard trigger
```

**JS Behavior:**
- Custom section hidden by default
- `.onchange="toggleCustomTrigger(this.value)"` shows/hides on selection
- Custom text input marked `required` when custom trigger selected
- Form submission includes custom trigger text in payload

**Payload sent to Scheduler Service:**
```json
{
  "name": "SIF Meeting for Idle Projects",
  "trigger_type": "custom",
  "custom_trigger_text": "Project has not had a note in more than 30 days",
  "has_notification_component": true,
  "notification_rule": { ... },
  ...
}
```

### Phase 2: Admin Reviews Pending Approval (Validation Gate)

**UI Location:** Logic → Notification Alerts → "Pending Logic Request Approvals"

**Custom Trigger Alert Box** (always visible at top):
```
⚠️ Custom Trigger Workflow: Requests with custom triggers 
require validation. Admin approval confirms the trigger 
requirement; backend implementation adds it to the data 
layer; trigger then becomes a standard option in future 
requests. [Learn more]
```

**Approval Card for Custom Trigger Request:**
```
┌─────────────────────────────────────────────────┐
│ ⚠️ SIF Meeting for Idle Projects                │
│ Suggested next meetings for projects...          │
│ 🔧 custom                    April 6, 2026       │
│                                                  │
│ ⚠️ Custom Trigger (Requires Implementation):    │
│    "Project has not had a note in more than     │
│     30 days"                                     │
│    Backend developer must implement trigger      │
│     detection SQL                                │
│                                    [Approve] [Reject]
└─────────────────────────────────────────────────┘
```

**Admin Actions:**

1. **✅ Approve** - Confirms trigger requirement is valid
   - Status → PENDING_IMPLEMENTATION
   - Notification to backend (via monitoring/Slack): "New custom trigger approved, needs implementation"
   - Custom trigger text available for developer reference

2. **❌ Reject** - Requires reason
   - Status → REJECTED
   - Reason stored in approval_notes
   - Request not visible to end users

**Admin's Mental Model:**
- "I'm approving that this trigger is *needed*, not that it works yet"
- "Backend will get notified and implement the SQL"
- "When they implement it, this request will activate and it becomes a standard trigger"

### Phase 3: Backend Implements & Trigger Becomes Standard

**Files Touched:**

1. **`Interface/Admin/Logic/Scheduler/main.py`** - TriggerDetector class
   
   ```python
   class TriggerDetector:
       def detect(self, trigger_type):
           if trigger_type == 'new_project':
               # existing code
           elif trigger_type == 'project_no_note_30d':  # NEW TRIGGER
               query = """
               SELECT p.project_id FROM projects p
               LEFT JOIN project_notes n ON p.project_id = n.project_id
                   AND n.created_at > CURRENT_TIMESTAMP() - INTERVAL 30 DAY
               WHERE n.project_id IS NULL
               """
               # Execute query, return matching projects
   ```

2. **`Interface/Admin/admin-dashboard.html`** - Modal form trigger dropdown

   ```html
   <select id="trigger-type" name="trigger_type" required>
       <option value="new_project">New Project Created</option>
       <option value="project_status_changed">Project Status Changed</option>
       <option value="task_assigned">Task Assigned</option>
       <option value="task_overdue">Task Overdue</option>
       <!-- NEW: Add as standard option -->
       <option value="project_no_note_30d">Project Has No Note (30+ Days)</option>
       <option value="custom">Custom Trigger... (Requires Implementation)</option>
   </select>
   ```
   Note: "Custom..." moved to END so users see standard options first

3. **`Interface/Admin/Logic\IMPLEMENTATION_CHECKLIST.md`** - Add entry

   ```markdown
   - [x] Custom trigger: "Project no note > 30 days"
     - PR: [Link to GitHub]
     - Trigger Type: `project_no_note_30d`
     - SQL Tested: Yes, 47 matching projects
     - Approved Requests: 1 (automatically converts to standard trigger)
   ```

**Validation Checklist Before Implementing:**

- [ ] Original custom trigger requirement in approval queue is identified
- [ ] SQL query tested against production-like dataset
- [ ] Trigger type name is descriptive and follows naming convention (snake_case)
- [ ] Added to TriggerDetector.detect() method
- [ ] Added to dropdown in admin-dashboard.html form
- [ ] Unit tests written for new detection logic
- [ ] Any pending Logic Requests using this custom trigger manually updated to reference standard option
- [ ] Documentation updated with new trigger option
- [ ] Backend restarted (Scheduler Service port 5011)

**After Implementation:**

- Original Logic Request with custom trigger: Status changes to PENDING_APPROVAL again (or manually resets)
- Admin re-approves using standard trigger option instead of custom
- Request now activates without "requires implementation" flag
- Future admins see trigger as standard option (no orange warning)

## Status Tracking

### Approval Status Values

```
DRAFT              - Unsaved in form
PENDING_APPROVAL   - Submitted, awaiting admin review
PENDING_IMPL*      - Custom trigger approved, awaiting backend implementation
APPROVED           - Ready to activate
ACTIVE             - Rules executing
PAUSED             - Temporarily disabled
ARCHIVED           - No longer needed
REJECTED           - Did not meet approval criteria
```

**\* PENDING_IMPL** is custom trigger state only. Non-custom triggers go directly from PENDING_APPROVAL → APPROVED.

### Database Tracking

**Table:** `logic_requests`

```sql
CREATE OR REPLACE FIELD TYPE logic_request_status AS STRUCT<
  status STRING,                    -- DRAFT, PENDING_APPROVAL, PENDING_IMPL, etc.
  approval_date TIMESTAMP,          -- When approved
  approval_by STRING,               -- Admin email
  custom_trigger_flag BOOL,         -- True if trigger_type = 'custom'
  custom_trigger_text STRING,       -- User's custom trigger description
  implementation_status STRING,     -- AWAITING, IN_PROGRESS, COMPLETED, BLOCKED
  implementation_notes STRING       -- Backend developer notes
>;
```

## UI/UX Patterns

### Form Level (Create Request)

**Trigger Dropdown:**
- Standard triggers highlighted at top (new_project, etc.)
- Custom option at bottom (clearly marked with "Requires Implementation")
- Selecting "Custom" reveals text input for requirement

**Custom Text Input:**
- Placeholder: Good example of actual requirement
- Required when custom selected
- Supports multi-line (textarea acceptable)
- No validation (capture intent, not syntax)

### Approval Level (Pending Approvals)

**Visual Indicators:**
- 🔧 Icon for custom triggers (wrench = needs implementation)
- ⚠️ Orange box with implementation checklist steps
- Clear statement: "Backend developer must implement trigger detection SQL"

**Action Buttons:**
- [Approve] - Green, normal-weight (common action)
- [Reject] - Red, normal-weight (less common but important)
- No "Modify" button (request goes back to submitter, not admin)

### Implementation Level (Ticket/GitHub)

**Developer Ticket Template:**

```markdown
## Custom Trigger Implementation

**Approved Requirement:** 
[Link to approval]

**Custom Trigger Text:**
"Project has not had a note in more than 30 days"

**Frontend Option Name:** Need backend to define
(Recommended: `project_no_note_30d`)

**Trigger Type:**  `project_no_note_[days]`

**Detection Query:**
Write SQL that returns matching entities

**Test With:** Sample project IDs from approval notes

**Checklist:**
- [ ] Query tested against production schema
- [ ] Added to TriggerDetector.detect() method
- [ ] Added to admin-dashboard.html dropdown
- [ ] Backend restarted and health check passing
- [ ] Pending Logic Request validated with new trigger option
```

## Backend Integration Points

### 1. API Endpoint: Create Logic Request

**POST** `/api/v1/logic-requests`

**Response includes:**
```json
{
  "status": "success",
  "request_id": "req-uuid-...",
  "trigger_type": "custom",
  "custom_trigger_text": "Project no note > 30d",
  "next_action": "Await admin approval, then backend implementation"
}
```

### 2. Scheduler Service Reaction to Custom Triggers

**Current Behavior:**
```python
def detect(self, trigger_type='custom', custom_text='Project no note > 30d'):
    if trigger_type == 'custom':
        # Don't try to detect; just log
        logger.warning(f'Custom trigger detected, requires implementation: {custom_text}')
        return []  # Empty results until implemented
```

**After Implementation:**
```python
def detect(self, trigger_type='project_no_note_30d'):
    if trigger_type == 'project_no_note_30d':
        # Full detection logic
        query = "SELECT project_id FROM ... WHERE date_diff(...) > 30"
        return client.query(query).result()
```

## Failure Modes & Recovery

### Risk: Admin Approves, Backend Never Implements

**Mitigation:**
- Monitoring dashboard shows "Pending Implementation" count
- Slack notification sent to #engineering on approval
- 30-day reminder email if not implemented
- Auto-archive after 90 days of inactivity

**Current State:** Manual tracking via IMPLEMENTATION_CHECKLIST.md

### Risk: Custom Trigger Text is Ambiguous

**Example:** "Send when we need to"

**Mitigation:**
- Admin review required (approve/reject)
- Suggestion prompts in form (examples given)
- Approval feedback form lets admin comment
- Developer can request clarification in ticket

### Risk: Duplicate Custom Triggers

**Example:** Two admins both request "project no activity X days"

**Mitigation:**
- When submitting custom trigger, show similar approved/implemented triggers
- Suggestion: "Did you mean: Project Has No Note (30+ Days)? This is already available."
- Still allow custom if user confirms

**Current State:** Manual review by admin during approval

## Metrics & Monitoring

### Success Metrics

- **Custom Triggers Submitted:** Count per month
- **Custom to Standard Conversion Rate:** % implemented within 30 days
- **Implementation Time:** Average days from approval to implementation
- **Reuse Rate:** % of custom triggers reused in multiple Logic Requests

### Monitoring Queries

```sql
-- Pending implementations
SELECT COUNT(*) as pending_impl_count
FROM logic_requests
WHERE status = 'PENDING_IMPL'

-- Converts to standard (before/after count)
SELECT custom_trigger_text, COUNT(*) as requests_submitted
FROM logic_requests
WHERE trigger_type = 'custom'
GROUP BY custom_trigger_text
ORDER BY requests_submitted DESC
```

## Summary of Implementation (April 6, 2026)

**✅ Completed:**
- UI form field for custom trigger (required text input, validation message)
- Approval card template showing custom trigger metadata
- Documentation of end-to-end workflow
- Placeholder implementation checklist

**🔄 In Progress:**
- API endpoint validation (POST to Scheduler Service)
- Approval workflow backend

**⏳ Pending:**
- Notification to backend when custom trigger approved
- Implementation tracking system
- Automated status transitions (PENDING_IMPL → APPROVED)
- Dashboard metrics for implementation SLA

## References

- [BigQuery schema](Schemas/bigquery_tables.sql)
- [Scheduler Service API](Scheduler/main.py)
- [Admin Dashboard Form](../../admin-dashboard.html) - Line ~1515 for trigger dropdown
- [Logic Request README](README.md#custom-trigger-workflow)
