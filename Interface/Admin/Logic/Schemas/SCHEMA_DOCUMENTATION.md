# BigQuery Schema Documentation - Logic Rules Engine

## Overview
This document describes the database schema for the Activity Hub Logic Rules Engine. All tables are in `wmt-assetprotection-prod.Store_Support_Dev` dataset.

## Table Relationships

```
logic_requests (Parent)
├── notification_logic_rules (Child) - One per request
├── scheduler_execution_log (Execution) - Many per rule
├── logic_request_approvals (Audit) - Approval history
└── notification_deliveries (Results) - Final notifications sent
```

## How Data Flows

### 1. Admin Creates Logic Request
- Admin fills out Logic Request form in Admin Dashboard
- Data saved to `logic_requests` table with status = "draft"
- If Notification component selected, form shows notification rules template

### 2. Admin Submits for Approval
- Status changes to "pending_approval"
- System generates internal notification to admins
- Record inserted in `logic_request_approvals` (action="submitted")

### 3. Admin Approves
- Admin navigates to Admin/Logic/Overview
- Clicks "Approve" on pending request
- Status changes to "approved" → "active"
- Child rule created in `notification_logic_rules`
- Record inserted in `logic_request_approvals` (action="approved")

### 4. Scheduler Detects Trigger
- Scheduler runs every 5 minutes
- Queries `logic_requests` where is_active = TRUE and trigger_type = "new_project"
- Detects new rows in project table since last run
- For each match:
  - Inserts row in `scheduler_execution_log` (status="pending")
  - Calls notification executor

### 5. Notification Executes
- Load notification rule from `notification_logic_rules`
- Render templates with actual data from trigger (project name, owner, etc.)
- Lookup recipient using recipient_rule (e.g., get project owner)
- Check user preferences from `notification_user_preferences`
- Deliver via selected channels (email, in-app, teams, slack)
- Insert row in `notification_deliveries` for each recipient/channel

### 6. Audit Trail
- `scheduler_execution_log` tracks: trigger detected, rule executed, status, errors
- `notification_deliveries` tracks: who received, when, channel, read status
- `logic_request_approvals` tracks: approval history and changes

## Key Fields Explained

### logic_requests

| Field | Type | Description |
|-------|------|-------------|
| `request_id` | STRING | UUID, primary key |
| `name` | STRING | "SIF Meeting Notification for New Projects" |
| `trigger_type` | STRING | "new_project", "project_status_changed", etc. |
| `trigger_table` | STRING | "projects" — which table to monitor |
| `has_notification_component` | BOOL | TRUE if this request includes notifications |
| `status` | STRING | draft → pending_approval → approved → active |
| `approval_status` | STRING | pending → approved or rejected |

### notification_logic_rules

| Field | Type | Description |
|-------|------|-------------|
| `rule_id` | STRING | UUID, primary key |
| `logic_request_id` | STRING | Foreign key to parent request |
| `category` | STRING | PROJECT_LIFECYCLE, TASK_WORK, URGENT, COMPLIANCE, ORG_CHANGE, SYSTEM |
| `title_template` | STRING | "SIF Meeting Required: {project_name}" — uses {placeholders} |
| `message_template` | STRING | HTML email template with {variable} replacements |
| `recipient_rule` | STRING | JSON: `{"type": "owner"}` or `{"type": "users", "emails": [...]}` |
| `channels` | ARRAY<STRING> | ["email", "in_app"] for MVP, ["teams", "slack"] Phase 2 |

### scheduler_execution_log

| Field | Type | Description |
|-------|------|-------------|
| `execution_id` | STRING | UUID, primary key |
| `trigger_timestamp` | TIMESTAMP | When trigger was detected (e.g., project created_at) |
| `trigger_type` | STRING | "new_project" |
| `trigger_source_record_id` | STRING | Project ID that triggered this |
| `status` | STRING | pending → in_progress → success or failed |
| `delivery_status` | JSON | `{"email": "sent", "in_app": "sent"}` |

### notification_deliveries

| Field | Type | Description |
|-------|------|-------------|
| `delivery_id` | STRING | UUID, primary key |
| `recipient_email` | STRING | Who received the notification |
| `channel` | STRING | "email" or "in_app" (MVP) |
| `is_read` | BOOL | Whether user has read it (in-app only) |
| `clicked_at` | TIMESTAMP | When user clicked link in notification |

## Example Data

### Logic Request: SIF Meeting Notification
```json
{
  "request_id": "uuid-123",
  "name": "SIF Meeting Notification for New Projects",
  "description": "When new project arrives, notify owner to submit SIF meeting request",
  "trigger_type": "new_project",
  "trigger_table": "projects",
  "trigger_condition": {"status": "Active", "timeframe": "last_24_hours"},
  "has_notification_component": true,
  "has_task_component": false,
  "has_nextstep_component": false,
  "status": "approved",
  "is_active": true
}
```

### Notification Rule: SIF Email Content
```json
{
  "rule_id": "uuid-456",
  "logic_request_id": "uuid-123",
  "category": "PROJECT_LIFECYCLE",
  "trigger_event": "new_project",
  "title_template": "Action Required: Submit SIF Meeting Request for {project_name}",
  "message_template": "<html>...<a href='http://sif-form.walmart.com?project_id={project_id}'>Submit SIF Request</a>...</html>",
  "recipient_rule": "{\"type\": \"owner\"}",
  "channels": ["email", "in_app"],
  "schedule": "immediate"
}
```

### Execution Log Entry
```json
{
  "execution_id": "uuid-789",
  "trigger_timestamp": "2026-04-06 10:15:32",
  "trigger_type": "new_project",
  "trigger_source_record_id": "proj-999",
  "logic_request_id": "uuid-123",
  "notification_rule_id": "uuid-456",
  "status": "success",
  "recipient_emails": ["john.doe@walmart.com"],
  "delivery_status": {
    "email": "sent",
    "in_app": "created"
  }
}
```

## Querying the Data

### Get all active Logic Requests
```sql
SELECT request_id, name, trigger_type, is_active
FROM `wmt-assetprotection-prod.Store_Support_Dev.logic_requests`
WHERE status = "approved" AND is_active = TRUE
ORDER BY created_at DESC;
```

### Get execution history for a request
```sql
SELECT execution_id, trigger_timestamp, status, delivery_status
FROM `wmt-assetprotection-prod.Store_Support_Dev.scheduler_execution_log`
WHERE logic_request_id = "uuid-123"
ORDER BY trigger_timestamp DESC
LIMIT 20;
```

### Get notifications received by a user (in-app inbox)
```sql
SELECT delivery_id, title, message, action_link, sent_at, is_read, clicked_at
FROM `wmt-assetprotection-prod.Store_Support_Dev.notification_deliveries`
WHERE recipient_email = "john.doe@walmart.com"
  AND channel = "in_app"
  AND NOT is_archived
ORDER BY sent_at DESC;
```

### Get approval audit trail
```sql
SELECT logic_request_id, action, admin_email, action_timestamp, comment
FROM `wmt-assetprotection-prod.Store_Support_Dev.logic_request_approvals`
WHERE logic_request_id = "uuid-123"
ORDER BY action_timestamp ASC;
```

## Notes for Implementation

1. **Partitioning**: All tables are partitioned by DATE to manage query costs and performance.
2. **Indexes**: Created on common filter/join columns (status, is_active, trigger_timestamp, recipient_email).
3. **Foreign Keys**: Declared but not enforced (BigQuery limitation), implement app-level validation.
4. **Credentials**: All services connecting to BQ require `GOOGLE_APPLICATION_CREDENTIALS` environment variable set.
