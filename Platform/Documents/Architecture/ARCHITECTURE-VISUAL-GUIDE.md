# Activity Hub: Visual Architecture & Component Interactions

## 1. SYSTEM ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ACTIVITY HUB PLATFORM                              │
│                   Centralized Data Aggregation & Orchestration               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┐  ┌──────────────────┐  ┌─────────────────────────┐
│   EXTERNAL SYSTEMS      │  │  DATA STANDARDS  │  │   INTERNAL SERVICES     │
├─────────────────────────┤  ├──────────────────┤  ├─────────────────────────┤
│ • Intake Hub (BigQuery) │  │ • Projects       │  │ • Notification Engine   │
│ • AMP Platform          │  │ • Project Status │  │ • Org Sync Service      │
│ • HR System             │  │ • Impact Scope   │  │ • Analytics Service     │
│ • Future Platforms      │  │ • Work Items     │  │ • Reporting Service     │
└─────────────────────────┘  │ • Assignments    │  │ • Access Service        │
                             │ • Timelines      │  │ • Audit Service         │
         API ↕               │ • Dependencies   │  └─────────────────────────┘
                             └──────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│              PLATFORM BRIDGE (Column Mapping & Validation)                  │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────────┐ │
│  │ Input: Raw  │  →   │ Registry &  │  →   │ Output: Standardized        │ │
│  │ Data from   │      │ Validation  │      │ Projects Table              │ │
│  │ Platforms   │      │             │      │                             │ │
│  └─────────────┘      └─────────────┘      └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
         ↓ (Standardized Data)
┌─────────────────────────────────────────────────────────────────────────────┐
│                   ACTIVITY HUB DATABASE (PostgreSQL)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Projects │ Tasks │ Notifications │ Org Units │ Users │ Rules │ Audit Logs  │
└─────────────────────────────────────────────────────────────────────────────┘
         ↓ (Project Data Changes)
┌─────────────────────────────────────────────────────────────────────────────┐
│              NOTIFICATION ENGINE (Event Driven, Rule Based)                 │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────────┐ │
│  │ Event:      │  →   │ Evaluate    │  →   │ Execute Actions:            │ │
│  │ Project     │      │ Rules       │      │ • Send Notifications        │ │
│  │ Changed     │      │ (AND/OR)    │      │ • Create Tasks              │ │
│  │             │      │             │      │ • Update Metrics            │ │
│  │             │      │             │      │ • Schedule Reminders        │ │
│  └─────────────┘      └─────────────┘      └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
         ↓ (User Actions)
┌─────────────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                                      │
│ ├─ Dashboard (Project Overview)                                             │
│ ├─ Admin Panel (Rule Management)                                            │
│ ├─ Notifications UI (Alerts & Tasks)                                        │
│ ├─ Reporting (Metrics & KPIs)                                               │
│ └─ Mobile/Native Apps                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. DATA FLOW: END-TO-END PROJECT LIFECYCLE

```
STEP 1: DATA INGESTION
═════════════════════════════════════════════════════════════════════

  Intake Hub          AMP              HR System          Future
  (BigQuery)        (Platform)        (Daily Sync)        Platforms
    │                  │                  │                  │
    └──────────────────┴──────────────────┴──────────────────┘
                        │
                   API Endpoint
                  /platforms/{name}
                        │
                        ↓
            ┌─────────────────────────┐
            │ API Request Handler     │
            │ - Validate API Key      │
            │ - Parse Payload         │
            │ - Rate Limit Check      │
            └─────────────────────────┘
                        │
                        ↓


STEP 2: PLATFORM BRIDGE (Column Mapping)
═════════════════════════════════════════════════════════════════════

            Raw Data Received
            (Unknown Schema)
                        │
                        ↓
        ┌────────────────────────────────┐
        │ Check Column Registry:         │
        │ "Does this column exist        │
        │  in our mapping?"              │
        └────────────────────────────────┘
                        │
                ┌───────┴───────┐
                │               │
           YES  │               │  NO
                ↓               ↓
        ┌─────────────┐  ┌───────────────┐
        │ Apply       │  │ Column Not    │
        │ Mapping     │  │ Recognized    │
        │ Rules       │  │               │
        └─────────────┘  │ Options:      │
                │        │ 1. Create new │
                │        │ 2. Map to     │
                │        │    existing   │
                │        │ 3. Ignore     │
                │        │ 4. Admin      │
                │        │    review     │
                │        └───────────────┘
                │               │
                └───────────────┘
                        │
                        ↓
        ┌────────────────────────────────┐
        │ Validate Against Project       │
        │ Schema:                        │
        │ - Required fields present?     │
        │ - Data types correct?          │
        │ - Foreign keys valid?          │
        └────────────────────────────────┘
                        │
                ┌───────┴───────┐
                │               │
             VALID          INVALID
                │               │
                ↓               ↓
        ┌─────────────┐  ┌──────────────┐
        │ Proceed     │  │ Log Error    │
        │             │  │ Notify Admin │
        │             │  │ Add to       │
        │             │  │ Failed Queue │
        └─────────────┘  └──────────────┘
                │
                ↓


STEP 3: DATA PERSISTENCE
═════════════════════════════════════════════════════════════════════

        ┌────────────────────────────────┐
        │ Insert/Update Project in DB    │
        │ - INSERT if new project        │
        │ - UPDATE if exists             │
        │ - Log change in audit table    │
        └────────────────────────────────┘
                        │
                        ↓
        ┌────────────────────────────────┐
        │ Create/Update Relationships:   │
        │ - Link to stores affected      │
        │ - Link to project owner        │
        │ - Create notifications field   │
        │ - Schedule meetings/tasks      │
        └────────────────────────────────┘
                        │
                        ↓
        ┌────────────────────────────────┐
        │ Publish Event:                 │
        │ PROJECT_CREATED or             │
        │ PROJECT_UPDATED               │
        │ → Redis Pub/Sub                │
        │ (Notification Engine listens)  │
        └────────────────────────────────┘
                        │
                        ↓


STEP 4: RULE EVALUATION (Notification Engine)
═════════════════════════════════════════════════════════════════════

        ┌────────────────────────────────┐
        │ Notification Engine Receives   │
        │ Event: PROJECT_UPDATED         │
        │ Project: {id, status, ...}     │
        └────────────────────────────────┘
                        │
                        ↓
        ┌────────────────────────────────┐
        │ Load All Active Rules from DB  │
        │ - Filter by trigger type       │
        │ - Load conditions              │
        │ - Load actions                 │
        └────────────────────────────────┘
                        │
                        ↓
        ┌────────────────────────────────┐
        │ For Each Rule, Evaluate:       │
        │                                │
        │ IF project.status == 'POC'     │
        │    AND project.impact == 'Stores'
        │    AND project.created < 7days │
        │ THEN {                         │
        │    Send notification           │
        │    Create task                 │
        │    Schedule reminder           │
        │ }                              │
        └────────────────────────────────┘
                        │
                ┌───────┴───────┐
                │               │
           MATCH            NO MATCH
                │               │
                ↓               ↓
        ┌─────────────┐  ┌────────────┐
        │ Collect     │  │ Continue   │
        │ Actions     │  │ to next    │
        │ to Execute  │  │ rule       │
        └─────────────┘  └────────────┘
                │               │
                └───────────────┘
                        │
                        ↓


STEP 5: ACTION EXECUTION
═════════════════════════════════════════════════════════════════════

        ┌────────────────────────────────┐
        │ Action Queue:                  │
        │ - Send Email Notification      │
        │ - Send In-App Alert            │
        │ - Create Slack Message         │
        │ - Create Task (AMP Integration)│
        │ - Set Reminder (3 days)        │
        │ - Update Project Status        │
        └────────────────────────────────┘
                        │
        ┌───────┬───────┼───────┬───────┐
        │       │       │       │       │
        ↓       ↓       ↓       ↓       ↓
    EMAIL   IN-APP  SLACK   TASK   REMINDER
        │       │       │       │       │
        └───────┴───────┼───────┴───────┘
                        │
                        ↓
        ┌────────────────────────────────┐
        │ Log Execution:                 │
        │ - rule_id: 42                  │
        │ - project_id: 123              │
        │ - executed_at: timestamp       │
        │ - status: success/failed       │
        │ - recipient_count: 15          │
        │ - error_msg: (if any)          │
        └────────────────────────────────┘
                        │
                        ↓


STEP 6: USER INTERACTION
═════════════════════════════════════════════════════════════════════

  Email      In-App         Slack
  Alert      Notification   Message
    │            │            │
    └────────────┴────────────┘
               │
               ↓
    User sees notification
    and takes action
               │
        ┌──────┴──────┐
        │             │
     CLICK         SNOOZE
        │             │
        ↓             ↓
    Navigate     Reschedule
    to Project   Reminder
        │             │
        └──────┬──────┘
               │
               ↓
    Activity Hub Dashboard
    Shows Project Details
    & Related Tasks


STEP 7: AUDIT & TRACKING
═════════════════════════════════════════════════════════════════════

        All Actions Logged:
        ┌────────────────────────────────┐
        │ Data Sync Audit Log:           │
        │ - Source: Intake Hub            │
        │ - Synced Projects: 45           │
        │ - Errors: 0                     │
        │ - Timestamp: 2026-01-14 10:00  │
        └────────────────────────────────┘

        ┌────────────────────────────────┐
        │ Rule Execution Audit Log:      │
        │ - Rule: POC/POT Notification   │
        │ - Triggered: Yes                │
        │ - Recipients: 15                │
        │ - Status: Delivered             │
        │ - Timestamp: 2026-01-14 10:15  │
        └────────────────────────────────┘

        ┌────────────────────────────────┐
        │ Access Log:                    │
        │ - User: john.doe@walmart.com   │
        │ - Action: Viewed Project       │
        │ - Resource: project_123        │
        │ - Timestamp: 2026-01-14 10:20  │
        │ - Result: Allowed (RBAC check) │
        └────────────────────────────────┘
```

---

## 3. DATABASE RELATIONSHIP DIAGRAM

```
┌──────────────────┐
│   USERS          │
├──────────────────┤
│ id (PK)          │
│ email            │
│ full_name        │
│ role             │◄───────────┐
│ current_org_id   │            │
│ manager_id       │ ┌──────────┤
│ last_login       │ │          │
│ created_at       │ │          │
└──────────────────┘ │          │
        │ 1          │          │
        │            │ 1        │
        │ N          │          │
        │            │          │
┌──────────────────────────────┐│
│ USER_ORG_ASSIGNMENTS │
├──────────────────────────────┤│
│ id (PK)              ││
│ user_id (FK) ────────┘│
│ org_unit_id (FK) ──────┐
│ position_title   ││
│ assignment_date  ││
│ is_current       ││
└──────────────────────────────┘│
        │ N                      │
        │                        │
        │ 1                      │
        │                    ┌──────────────────┐
        └────────────────────┤ORG_UNITS         │
                             ├──────────────────┤
                             │ id (PK)          │
                             │ unit_name        │
                             │ unit_type        │
                             │ parent_unit_id◄──┤─ Self-referencing
                             │ manager_id (FK) ──┐ for hierarchy
                             │ hr_system_id     │
                             └──────────────────┘
                                     ▲
                                     │
                ┌────────────────────┘
                │
        ┌───────┴─────────┐
        │                 │
    REGION          DISTRICT
    │                 │
    ├─ Division      ├─ Area
    ├─ Department    ├─ Store
    │                 └─ (1:4700 stores)
    └─ (national)


┌──────────────────────────────────┐
│ USER_MANAGER_RELATIONSHIPS       │ ◄─── WHO REPORTS TO WHOM
├──────────────────────────────────┤
│ id (PK)                          │
│ employee_id (FK) → USERS         │
│ manager_id (FK) → USERS          │
│ relationship_start_date          │
│ relationship_end_date (nullable) │
│ is_current                       │
└──────────────────────────────────┘
        │ N (employee can have 1 manager, 
        │    manager can have N employees)


┌──────────────────────────────────┐
│ PROJECTS (NEW - CENTRAL)         │
├──────────────────────────────────┤
│ id (PK)                          │
│ project_name                     │
│ description                      │
│ status (POC/POT/Implementation)  │
│ priority                         │
│ project_owner_id (FK) → USERS    │
│ impact_scope (Stores/HO/Both)    │
│ created_at                       │
│ start_date                       │
│ end_date                         │
│ source_platform_id               │
│ source_system_project_id         │
└──────────────────────────────────┘
        │ 1
        │
        │ N
        │
┌──────────────────────────────────┐
│ PROJECT_STORE_MAPPING            │ ◄─── WHICH STORES AFFECTED
├──────────────────────────────────┤
│ id (PK)                          │
│ project_id (FK)                  │
│ store_id (FK) → STORES           │
│ assigned_date                    │
└──────────────────────────────────┘


┌──────────────────────────────────┐
│ PROJECTS (cont')                 │
├──────────────────────────────────┤
│ id (PK)                          │
│ ... (see above)                  │
└──────────────────────────────────┘
        │ 1
        │
        │ N
        │
┌──────────────────────────────────┐
│ NOTIFICATION_RULES               │ ◄─── ADMIN-CONFIGURED RULES
├──────────────────────────────────┤
│ id (PK)                          │
│ rule_name                        │
│ description                      │
│ trigger_conditions (JSON)        │
│ actions (JSON)                   │
│ created_by (FK) → USERS          │
│ created_by_org_unit_id (FK)      │
│ escalation_to (FK) → USERS       │
│ review_due_date                  │
│ is_active                        │
└──────────────────────────────────┘
        │ 1
        │
        │ N
        │
┌──────────────────────────────────┐
│ NOTIFICATION_EXECUTIONS          │ ◄─── AUDIT TRAIL
├──────────────────────────────────┤
│ id (PK)                          │
│ rule_id (FK)                     │
│ project_id (FK)                  │
│ triggered_at                     │
│ recipients (JSON)                │
│ status (pending/sent/failed)     │
│ error_message                    │
└──────────────────────────────────┘


┌──────────────────────────────────┐
│ PLATFORM_BRIDGE_REGISTRY         │ ◄─── COLUMN MAPPING
├──────────────────────────────────┤
│ id (PK)                          │
│ source_platform (Intake Hub)     │
│ source_column_name (raw field)   │
│ target_column_name (Activity Hub)│
│ data_type                        │
│ transformation_rules (JSON)      │
│ created_at                       │
│ updated_at                       │
└──────────────────────────────────┘


┌──────────────────────────────────┐
│ DATA_SYNC_LOGS                   │ ◄─── SYNC HISTORY
├──────────────────────────────────┤
│ id (PK)                          │
│ source_platform                  │
│ sync_started_at                  │
│ sync_completed_at                │
│ records_processed                │
│ records_failed                   │
│ error_log (JSON)                 │
│ synced_by (system/user)          │
└──────────────────────────────────┘


┌──────────────────────────────────┐
│ HR_SYNC_STATUS                   │ ◄─── OPERATIONAL STATUS
├──────────────────────────────────┤
│ id (PK)                          │
│ last_sync_timestamp              │
│ next_scheduled_sync              │
│ status (success/failure)         │
│ records_processed                │
│ error_log                        │
└──────────────────────────────────┘
```

---

## 4. NOTIFICATION ENGINE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    NOTIFICATION ENGINE (Event-Driven)                   │
└─────────────────────────────────────────────────────────────────────────┘

EVENT SOURCE: Project State Changes
═════════════════════════════════════

    Database Trigger / Application Event
              │
              ↓
    ┌──────────────────────────────────┐
    │ EVENT: PROJECT_STATUS_CHANGED    │
    │ - project_id: 123                │
    │ - old_status: PENDING            │
    │ - new_status: POC                │
    │ - timestamp: 2026-01-14 10:15    │
    └──────────────────────────────────┘
              │
              ↓
    ┌──────────────────────────────────┐
    │ Publish to Redis Pub/Sub:        │
    │ Channel: "project:status:change" │
    │ Message: event_json              │
    └──────────────────────────────────┘


RULE EVALUATION LAYER
═════════════════════════════════════

    ┌─────────────────────────────────────────────────┐
    │ Notification Rule Subscriber                    │
    │ (Listening to Redis pub/sub channels)           │
    └─────────────────────────────────────────────────┘
              │
              ↓
    ┌─────────────────────────────────────────────────┐
    │ Load Triggering Rule:                           │
    │ {                                               │
    │   "rule_id": 42,                                │
    │   "name": "POC/POT Communication Setup",         │
    │   "triggers": [                                 │
    │     {                                           │
    │       "event_type": "project_status_change",    │
    │       "conditions": [                           │
    │         "new_status IN ('POC', 'POT')",         │
    │         "impact_scope IN ('Stores', 'Both')"    │
    │       ],                                        │
    │       "join": "AND"                             │
    │     }                                           │
    │   ]                                             │
    │ }                                               │
    └─────────────────────────────────────────────────┘
              │
              ↓
    ┌─────────────────────────────────────────────────┐
    │ EVALUATE CONDITIONS                             │
    │                                                 │
    │ Check: new_status == 'POC'? ✓ YES              │
    │ Check: impact_scope == 'Stores'? ✓ YES         │
    │ → ALL CONDITIONS MET → EXECUTE ACTIONS          │
    └─────────────────────────────────────────────────┘
              │
              ↓


ACTION EXECUTION LAYER
═════════════════════════════════════

    ┌─────────────────────────────────────────────────┐
    │ ACTIONS to execute:                             │
    │ [                                               │
    │   { type: "notify", channels: ["email", "in-app"]},
    │   { type: "create_task", template: "..." },     │
    │   { type: "schedule_reminder", days: 3 }       │
    │ ]                                               │
    └─────────────────────────────────────────────────┘
              │
        ┌─────┴─────┬─────────┬─────────┐
        │           │         │         │
        ↓           ↓         ↓         ↓
    NOTIFY      CREATE      SCHEDULE  (Future
    ACTION      TASK        REMINDER  Actions)
        │           │         │
        ↓           ↓         ↓


1. NOTIFICATION ACTION
═════════════════════════════════════
    Load Recipients:
    ├─ Project owner
    ├─ Project owner's direct reports
    └─ AMP Coordinator (by role)

    Load Template:
    ├─ Template ID: "poc_pot_kickoff"
    ├─ Subject: "POC/POT Phase Initiated: {{project.name}}"
    ├─ Body: "A new project has entered..."

    Render Template:
    ├ Replace {{project.name}} with actual name
    ├─ Replace {{store_list}} with store numbers
    └─ Replace {{phase}} with POC/POT

    Send Notifications:
    ├─ Email to recipients
    ├─ In-app notification
    └─ Log delivery status


2. CREATE TASK ACTION
═════════════════════════════════════
    Create Task:
    ├─ title: "Set up AMP Communication Activity"
    ├─ project_id: 123
    ├─ assigned_to: {{project_owner_direct_reports}}
    ├─ due_date: +3 days from now
    └─ status: "pending"

    Link to Project:
    └─ Project 123 now has 1 new task


3. SCHEDULE REMINDER ACTION
═════════════════════════════════════
    Create Scheduled Reminder:
    ├─ reminder_type: "task_due_soon"
    ├─ trigger_date: 2 days from due date
    ├─ recipient: assigned task owner
    ├─ message: "Your task is due in 1 day"
    └─ status: "scheduled"


LOGGING & AUDIT
═════════════════════════════════════

    Insert into NOTIFICATION_EXECUTIONS:
    ├─ rule_id: 42
    ├─ project_id: 123
    ├─ triggered_at: 2026-01-14 10:15:32
    ├─ recipients: ["john@wmt.com", "jane@wmt.com"]
    ├─ status: "sent"
    ├─ task_created: task_id_456
    ├─ reminder_scheduled: reminder_id_789
    ├─ error_message: null
    └─ log_timestamp: 2026-01-14 10:15:35

    Insert into AUDIT_LOG:
    ├─ action: "notification_executed"
    ├─ rule_id: 42
    ├─ project_id: 123
    ├─ user_id: system
    ├─ timestamp: 2026-01-14 10:15:35
    └─ details: {...}
```

---

## 5. ORGANIZATION HIERARCHY & ACCESS PROPAGATION

```
┌─────────────────────────────────────────────────────────────┐
│               ORG HIERARCHY EXAMPLE                          │
└─────────────────────────────────────────────────────────────┘

NATIONAL LEVEL
│
├─ DIVISION: Store Support
│  │  Manager: Sarah Chen (SVP)
│  │
│  ├─ DEPARTMENT: Technology
│  │  │  Manager: Mike Johnson (VP)
│  │  │
│  │  ├─ TEAM: Activity Hub Platform
│  │  │  │  Manager: Lisa Wong (Manager)
│  │  │  │
│  │  │  ├─ John Doe (Engineer)
│  │  │  │
│  │  │  ├─ Jane Smith (Engineer)
│  │  │  │
│  │  │  └─ Bob Wilson (Product Manager)
│  │  │
│  │  └─ TEAM: Integration Services
│  │     └─ (other teams)
│  │
│  └─ DEPARTMENT: Operations
│     │  Manager: David Park (Director)
│     │
│     ├─ REGION: Northeast
│     │  │  Manager: Emily Rodriguez
│     │  │
│     │  ├─ DISTRICT: Boston
│     │  │  │  Manager: Chris Lee
│     │  │  │
│     │  │  ├─ STORE: #1234 Boston Supercenter
│     │  │  │  Store Manager: Amy Johnson
│     │  │  │
│     │  │  └─ STORE: #1235 Boston Neighborhood
│     │  │     Store Manager: Tom Anderson
│     │  │
│     │  └─ DISTRICT: New York
│     │     └─ ...
│     │
│     ├─ REGION: Southeast
│     │  └─ ...
│     │
│     └─ REGION: Midwest
│        └─ ...


DATABASE REPRESENTATION
═════════════════════════════════════

ORG_UNITS Table:
┌────────────────────────────────────────────────┐
│ id │ name  │ type    │ parent_id │ manager_id │
├────────────────────────────────────────────────┤
│ 1  │National│ CORP   │ NULL      │ NULL       │
├────────────────────────────────────────────────┤
│ 10 │Store  │ DIVISION│ 1         │ user_456   │
│    │Support│         │           │ (Sarah)    │
├────────────────────────────────────────────────┤
│ 20 │Tech   │ DEPT    │ 10        │ user_789   │
│    │       │         │           │ (Mike)     │
├────────────────────────────────────────────────┤
│ 30 │Activity│ TEAM   │ 20        │ user_111   │
│    │Hub    │         │           │ (Lisa)     │
├────────────────────────────────────────────────┤
│ 100│Northeast│ REGION │ 40        │ user_222   │
│    │       │         │           │ (Emily)    │
├────────────────────────────────────────────────┤
│ 110│Boston│ DISTRICT│ 100       │ user_333   │
│    │      │         │           │ (Chris)    │
├────────────────────────────────────────────────┤
│ 111│Store │ STORE   │ 110       │ user_444   │
│    │#1234 │         │           │ (Amy)      │
└────────────────────────────────────────────────┘


ACCESS PROPAGATION EXAMPLE
═════════════════════════════════════

User: John Doe (Engineer)
├─ Current Assignment: Activity Hub Team
├─ Manager: Lisa Wong
├─ Manager's Manager: Mike Johnson
├─ Manager's Manager's Manager: Sarah Chen
├─ Access Scope: Activity Hub Team
└─ Projects Visible:
   └─ Only projects assigned to Activity Hub Team


User: Emily Rodriguez (Regional Manager)
├─ Current Assignment: Northeast Region
├─ Manager: David Park
├─ Teams Under Her: All districts + stores in Northeast
├─ Access Scope: Northeast Region + all subordinate orgs
└─ Projects Visible:
   ├─ All projects assigned to Northeast Region
   ├─ All projects assigned to Boston District
   ├─ All projects assigned to Store #1234
   └─ (recursive down the tree)


ACCESS HIERARCHY LOGIC
═════════════════════════════════════

When user views projects, show projects where:
├─ User assigned to project
├─ User's org unit assigned to project
├─ OR any parent org unit assigned
├─ OR any direct reports assigned
├─ AND user has appropriate role (Viewer, Manager, Admin)
```

---

## 6. NOTIFICATION RULE BUILDER WORKFLOW

```
ADMIN CREATES NEW NOTIFICATION RULE
═════════════════════════════════════════════

Screen 1: Basic Info
┌─────────────────────────────────┐
│ Rule Name:  [________________]  │
│ Description: [_________________│
│ Is Active:  ☑ Yes              │
└─────────────────────────────────┘


Screen 2: Trigger Configuration
┌─────────────────────────────────────────┐
│ Event Type:  [v] Project Status Change  │
│              [  ] Project Date Alert     │
│              [  ] Project Milestone      │
│              [  ] Custom Metric          │
│                                         │
│ Add Condition:                          │
│ [+] New Condition                       │
│                                         │
│ Condition 1:                            │
│ ├─ Field: [v] project.status            │
│ ├─ Operator: [v] is one of              │
│ ├─ Values: [☑] POC [☑] POT [ ] Other    │
│ └─ Delete [x]                           │
│                                         │
│ Condition 2:                            │
│ ├─ Field: [v] project.impact_scope      │
│ ├─ Operator: [v] equals                 │
│ ├─ Value: [v] Stores                    │
│ └─ Delete [x]                           │
│                                         │
│ Join Conditions: [v] ALL (AND)           │
│                  [ ] ANY (OR)            │
└─────────────────────────────────────────┘


Screen 3: Actions Configuration
┌──────────────────────────────────────┐
│ Select Actions to Execute:           │
│                                      │
│ [☑] Send Notification                │
│     ├─ Template: [v] POC Kickoff     │
│     ├─ Channels: ☑Email ☑In-app     │
│     │              ☑Slack            │
│     └─ Recipients: [v] Dynamic       │
│        ├─ [☑] Project Owner          │
│        ├─ [☑] Project Owner's        │
│        │     Direct Reports          │
│        └─ [☑] AMP Coordinator (role) │
│                                      │
│ [☑] Create Task                      │
│     ├─ Template: [v] AMP Setup       │
│     ├─ Assigned To: [v] Dynamic      │
│     │  └─ Project Owner's Reports    │
│     ├─ Due Date: [v] +3 days         │
│     └─ Priority: [v] High            │
│                                      │
│ [☑] Schedule Reminder                │
│     ├─ Type: [v] Task Completion     │
│     ├─ Schedule: [v] Weekly          │
│     └─ Until: [v] Task Complete      │
│                                      │
│ [+] Add Another Action               │
└──────────────────────────────────────┘


Screen 4: Ownership & Maintenance
┌──────────────────────────────────────┐
│ Created By: John Doe                 │
│ Organization: Store Support - Tech   │
│                                      │
│ Escalation:                          │
│ If creator leaves, escalate to:      │
│ [v] Mike Johnson (Direct Manager)    │
│                                      │
│ Maintenance Schedule:                │
│ ├─ First Review Due: 2026-04-14      │
│ ├─ Send Reminder: 2026-03-14         │
│ ├─ Auto-disable if inactive: 90 days │
│ └─ [Edit Schedule]                   │
└──────────────────────────────────────┘


Screen 5: Review & Test
┌──────────────────────────────────────┐
│ Rule Summary:                        │
│ ┌────────────────────────────────┐  │
│ │ Name: POC/POT Kickoff          │  │
│ │ Event: project.status changed  │  │
│ │ If: status IN (POC, POT) AND   │  │
│ │     impact_scope = Stores       │  │
│ │ Then:                          │  │
│ │  - Send email to 3 recipients  │  │
│ │  - Create task (AMP setup)     │  │
│ │  - Schedule weekly reminder    │  │
│ └────────────────────────────────┘  │
│                                      │
│ [Test Rule] [Preview] [Save] [Cancel]│
└──────────────────────────────────────┘


TEST MODE OUTPUT
═════════════════════════════════════

Test Project: #123 "Store Engagement 2026"
Current Status: PENDING → Changed to: POC ✓

Trigger Check:
├─ Trigger Type: project_status_change ✓
├─ Condition 1: status IN (POC, POT) ✓
├─ Condition 2: impact_scope = Stores ✓
├─ Join: AND → ALL conditions met ✓
└─ Rule WILL TRIGGER on this data ✓

Actions (Simulated):
├─ Send Notification:
│  ├─ Template: POC Kickoff ✓
│  ├─ Channels: Email, In-app, Slack ✓
│  └─ Recipients (3):
│     ├─ john.doe@wmt.com (Owner)
│     ├─ jane@wmt.com (Owner's report 1)
│     └─ bob@wmt.com (AMP Coordinator)
│
├─ Create Task:
│  ├─ Title: Set up AMP Communication Activity
│  ├─ Assigned To: jane@wmt.com, bob@wmt.com
│  └─ Due: 2026-01-17
│
└─ Schedule Reminder:
   ├─ Type: Weekly
   ├─ First reminder: 2026-01-16
   └─ Duration: Until task complete

✓ All actions validated successfully
```

---

## 7. HR SYNC PROCESS

```
SCHEDULED: Daily at 2 AM
═════════════════════════════════════════════════════════════════════

2:00 AM - SYNC INITIATION
═════════════════════════

    ┌────────────────────────────────┐
    │ Start Daily HR Sync Job        │
    │ - Log start time               │
    │ - Set status: IN_PROGRESS      │
    │ - Create new sync record       │
    └────────────────────────────────┘


2:01 AM - CONNECT TO HR SYSTEM
═════════════════════════════════════════════

    ┌────────────────────────────────┐
    │ Connect to HR System:          │
    │ - Endpoint: HR API v2.0        │
    │ - Auth: OAuth2 token           │
    │ - Retry: 3 attempts            │
    │ - Timeout: 5 minutes           │
    └────────────────────────────────┘
              │
        ┌─────┴──────┐
        │            │
    SUCCESS       FAILURE
        │            │
        ↓            ↓
   Continue    Report Error


2:03 AM - FETCH NEW/CHANGED DATA
═════════════════════════════════════════════

    Query HR System:
    ├─ All employees (last_modified > last_sync_time)
    ├─ All organization units
    ├─ All manager relationships
    └─ Returns: ~50,000 employee records

    Cache in temporary table:
    ├─ hr_sync_temp_employees
    ├─ hr_sync_temp_org_units
    └─ hr_sync_temp_relationships


2:15 AM - RECONCILE WITH CURRENT STATE
═════════════════════════════════════════════

    ┌─────────────────────────────────┐
    │ For Each Employee in HR Data:   │
    │                                 │
    │ IF NOT in Activity Hub Users:   │
    │ └─ New employee → INSERT        │
    │                                 │
    │ IF in Activity Hub but changed: │
    │ └─ Update: org_unit, manager    │
    │           position, etc.        │
    │                                 │
    │ IF in Activity Hub but removed: │
    │ └─ Mark: is_active = false      │
    │    Record: deactivated_date     │
    │                                 │
    │ Result: 1000 inserts,           │
    │         500 updates,            │
    │         100 deactivations       │
    └─────────────────────────────────┘


2:25 AM - ORGANIZATION HIERARCHY UPDATE
═════════════════════════════════════════════

    Update ORG_UNITS table:
    ├─ Fix parent_unit_id references
    ├─ Update manager_id assignments
    ├─ Move users between orgs (if changed)
    └─ Create any new org units from HR

    Cascade Changes:
    ├─ User moved from Region A → Region B
    │  └─ Update user_org_assignments
    │     └─ Update project visibility
    │        └─ Update access groups
    │
    └─ Manager changed (Lisa left, David promoted)
       ├─ End Lisa's manager relationships
       ├─ Start David's manager relationships
       ├─ Update notification ownership
       │  (Lisa's rules → David's escalation)
       └─ Update project ownership (if needed)


2:35 AM - CREATE AUDIT TRAIL
═════════════════════════════════════════════

    Insert into USER_ROLES_HISTORY:
    ├─ John Doe: role changed VIEWER→MANAGER
    ├─ Jane Smith: org changed Region A→Region B
    └─ Bob Wilson: manager changed Lisa→David

    Insert into HR_SYNC_AUDIT:
    ├─ sync_date: 2026-01-14
    ├─ records_processed: 1600
    ├─ changes_detected: 600
    ├─ errors: 0
    └─ duration: 35 minutes

    Notification to Admins:
    ├─ Email: "HR Sync Complete"
    ├─ Content: "1600 records processed, 600 changes"
    └─ Link: "View sync details"


2:40 AM - CLEANUP & FINALIZATION
═════════════════════════════════════════════

    ┌────────────────────────────────┐
    │ Final Steps:                   │
    │ 1. Drop temp tables            │
    │ 2. Update sync status: SUCCESS │
    │ 3. Set next_sync: tomorrow 2AM │
    │ 4. Log completion              │
    │ 5. Notify on-call admin (email)│
    └────────────────────────────────┘


ERROR HANDLING
═════════════════════════════════════

If HR API Timeout (after 3 retries):
├─ Status: PARTIAL_FAILURE
├─ Fall back to last sync data
├─ Alert admins: "HR Sync failed, using cached data"
├─ Schedule retry: 6 AM (in 4 hours)
└─ Don't apply any changes to avoid data corruption

If Data Conflicts Found:
├─ Log conflict: "John Doe in 2 regions"
├─ Hold conflicting record for manual review
├─ Notify admin: "Conflict detected, requires review"
└─ Apply non-conflicting changes only


IMPACT MONITORING
═════════════════════════════════════

After Sync, Monitor:
├─ Access Control Changes
│  └─ Any users with new access?
│     → Log in access_audit
│
├─ Project Ownership Changes
│  └─ Any projects with new owner?
│     → Log + notify current & new owner
│
├─ Org Hierarchy Changes
│  └─ Any reporting relationships changed?
│     → Update notification escalations
│
└─ Role Changes
   └─ Any new admins/managers?
      → Require re-training confirmation
```

---

## 8. COMPONENT DEPENDENCY MAP

```
CORE DEPENDENCIES (Must Build First)
════════════════════════════════════════════════════════════

TIER 1: Data Models
├─ Projects table (central)
├─ Platform Bridge Registry
└─ Org Units + User assignments


TIER 2: Data Integration
├─ Intake Hub API client
├─ Platform Bridge Mapper
├─ Data validation layer
└─ Sync logging


TIER 3: Orchestration
├─ Notification Engine (uses Project data)
├─ Org Sync Service (uses Org Units)
├─ Access Control Service (uses Org hierarchy)
└─ Notification Router (uses Org Hierarchy)


TIER 4: Admin Interfaces & Features
├─ Rule Builder UI
├─ Template Manager UI
├─ Org Hierarchy Viewer
└─ Sync Status Dashboard


DEPENDENCIES BETWEEN COMPONENTS
════════════════════════════════════════════════════════════

Projects ─────┬─────────────── Notifications
              │                  │
              ├─────────────────┼── Reporting
              │                  │
              └─────────────────┼── Scheduling
                                 │
Org Hierarchy────────────────────┼── Access Control
   │                             │
   └─────────────── Notifications
                          │
Platform Bridge ──────────┼── Projects
                          │
HR System ────────── Org Hierarchy
                          │
                    Access Control


BREAKING CHANGES IF ORDER IS WRONG
════════════════════════════════════════════════════════════

❌ If you build Notifications before Projects:
   └─ No data to trigger notifications on

❌ If you build Org Hierarchy after Notifications:
   └─ Can't route notifications to right people

❌ If you build Platform Bridge without knowing Project schema:
   └─ Mapping rules will be wrong, need rebuild

❌ If you connect HR System before Org structure:
   └─ No place to store org data
```

---

**This visualization file is meant to complement the ARCHITECTURE-IMPACT-ANALYSIS.md document. Reference both when planning implementation.**

