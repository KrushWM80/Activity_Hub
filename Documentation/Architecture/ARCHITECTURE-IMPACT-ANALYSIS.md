# Activity Hub Architecture Impact Analysis
**Date:** January 14, 2026  
**Status:** DESIGN REVIEW - PRE-IMPLEMENTATION  
**Prepared for:** Review & Approval Before Changes

---

## Executive Summary

Your proposed Activity Hub architecture fundamentally transforms it from a simple activity tracking system into a **centralized data aggregation and orchestration platform**. This requires significant architectural changes across:

1. **Data Integration Layer** - Multi-source API connectivity
2. **Data Model** - Dynamic column mapping and standardization
3. **Notification Engine** - Rule-based, admin-configurable system
4. **Access Control** - Org hierarchy alignment with HR data
5. **Platform Bridge** - Dynamic schema validation and mapping

**Key Risk Areas:** Data standardization complexity, real-time org sync, notification rule management

---

## Part 1: ARCHITECTURAL IMPACT

### Current State (Today)
```
Activity Hub (Monolithic)
├─ Single data model (Activity, Store, User, Communication)
├─ Basic CRUD operations
├─ WebSocket for real-time updates
└─ Pre-determined schema (no flexibility)
```

### Proposed State (Target)
```
Activity Hub (Data Orchestration Platform)
├─ Project Management (Core Entity)
├─ Platform Bridge (Data Mapping)
├─ Multi-Source Integration (Intake Hub, AMP, Future Platforms)
├─ Notification Engine (Admin-Configurable Rules)
├─ Org Hierarchy Sync (HR Data)
└─ Unified Data Model (Standardized Columns)
```

### Why This Matters
- **Complexity:** From 5 core models → 12-15 core models + bridge patterns
- **Dependencies:** From internal only → 4-5 external data sources
- **Real-time:** Current WebSocket is point-to-point → needs pub/sub architecture
- **State Management:** Static schema → dynamic schema validation

---

## Part 2: CORE COMPONENTS & DATA FLOW

### 2.1 PROJECT (Central Entity)
This becomes your canonical data model that everything else aligns to.

**Current State:** No Project table exists
**Needed Addition:** Project table with standardized columns

**Project Data Model Should Contain:**
```
From Intake Hub BigQuery Analysis Needed:
├─ Project Metadata
│  ├─ Project ID (unique identifier)
│  ├─ Project Name
│  ├─ Project Description
│  ├─ Project Owner
│  ├─ Project Status (POC, POT, Implementation, Live, Closed)
│  ├─ Created Date
│  ├─ Start Date
│  └─ End Date
│
├─ Impact Scope
│  ├─ Impact Type (Stores, Home Office, Both)
│  ├─ Store Numbers Affected
│  ├─ Geographic Region
│  ├─ Department
│  └─ Division
│
├─ Work Organization
│  ├─ Project Type (Initiative, Pilot, Rollout, etc.)
│  ├─ Priority Level
│  ├─ Budget Allocation
│  └─ Timeline
│
└─ Cross-Platform References
   ├─ AMP Communication Activity IDs
   ├─ Source Platform (Intake Hub, etc.)
   ├─ Source Platform Project ID
   └─ Associated Tasks/Work Items
```

**CRITICAL DECISION:** You need to examine `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` to determine what columns Intake Hub currently has, so we can design the standardized Project columns that all platforms will map TO.

---

### 2.2 PLATFORM BRIDGE (The Mapper)
**Purpose:** Connect different project management platforms to Activity Hub's standardized Project model

**Concept:**
```
┌─────────────────┐
│ Intake Hub      │
│ (Raw Data)      │
└────────┬────────┘
         │
    [Column Mapping]
         │
┌────────▼────────┐
│ Platform Bridge │◄──── Maps Intake Hub columns to Activity Hub Project columns
│ Registry        │      Validates unknown columns
│ (Active Mapper) │      Stores mapping rules
└────────┬────────┘
         │
    [Standardized Data]
         │
┌────────▼────────────────────┐
│ Activity Hub Project Model  │
│ (Canonical Data Model)      │
└────────┬────────────────────┘
         │
    [Used by:]
    ├─ Notifications
    ├─ Reporting
    ├─ Metrics
    ├─ Scheduling
    └─ Other Platforms
```

**What Platform Bridge Needs:**
1. **Column Registry Table**
   ```
   - Source Platform (Intake Hub, AMP, Future)
   - Source Column Name (raw field)
   - Activity Hub Project Column (standardized)
   - Data Type
   - Transformation Rules
   - Last Updated
   - Created By
   ```

2. **Mapping Validation Engine**
   ```
   When new data arrives:
   - IF column exists in registry → map automatically
   - IF column unknown → flag for admin review
   - Admin decides: ignore, create new column, or map to existing
   - Once decided, update registry for next time
   ```

3. **Data Sync Process**
   ```
   Poll/API Call → Intake Hub raw data
   ↓
   Apply column mappings
   ↓
   Validate against Project schema
   ↓
   IF valid → upsert to Activity Hub Project table
   IF invalid → log error + notify admin
   ```

**IMPACT ON BACKEND:**
- New tables: `platform_bridge_registry`, `platform_bridge_mappings`, `data_sync_logs`
- New services: `platform_bridge_service`, `data_mapping_service`
- New API endpoints: `/api/v1/admin/platform-mappings/*`

---

### 2.3 DATA INTEGRATION (Multi-Source API)

**Current State:** 
- No external data sources connected
- `intake_hub_service.py` exists but likely basic

**Proposed State:**
```
Activity Hub API Layer:
├─ Incoming Data Endpoints (Platforms push data TO Hub)
│  ├─ POST /api/v1/platforms/intake-hub/projects
│  ├─ POST /api/v1/platforms/amp/activities
│  ├─ POST /api/v1/platforms/{platform-name}/{entity-type}
│  └─ Authentication: Platform API key + IP whitelist
│
├─ Outgoing Data Endpoints (Hub provides data TO Platforms)
│  ├─ GET /api/v1/projects (filtered by platform needs)
│  ├─ GET /api/v1/projects/{id}/notifications
│  ├─ GET /api/v1/projects/{id}/metrics
│  └─ Authentication: OAuth2 + rate limiting
│
└─ Data Sync Status Endpoints
   ├─ GET /api/v1/admin/sync-status
   ├─ GET /api/v1/admin/sync-logs/{platform}
   └─ POST /api/v1/admin/manual-sync/{platform}
```

**IMPACT ON BACKEND:**
- New API router: `api/v1/platforms/`
- New services: `intake_hub_service` (expanded), `amp_service`, `platform_connector_service`
- New models: `DataSyncLog`, `PlatformConfig`, `APIKey`
- New middleware: API key validation, rate limiting, request logging

---

### 2.4 NOTIFICATION ENGINE (Rule-Based Admin Configuration)

**Purpose:** Admin-created notifications based on Project data + cross-platform conditions

**Example Notification Rule:**
```
{
  "name": "POC/POT Communication Setup",
  "description": "When project enters POC/POT, notify relevant teams to set up AMP Communication Activity",
  "trigger": {
    "event_type": "project_status_change",
    "condition": "status IN ('POC', 'POT')",
    "platform_data": "project.status"
  },
  "actions": [
    {
      "type": "notification",
      "channels": ["email", "in-app"],
      "template": "poc_pot_kickoff",
      "recipients": {
        "project_owner": true,
        "project_owner_direct_reports": true,
        "amp_coordinator": true
      },
      "parameters": {
        "project_id": "{{project.id}}",
        "store_list": "{{project.stores_affected}}",
        "phase": "{{project.status}}"
      }
    },
    {
      "type": "task_creation",
      "task_template": "create_amp_communication_activity",
      "assigned_to": "project_owner_direct_reports",
      "due_date": "+3 days"
    },
    {
      "type": "reminder",
      "schedule": "weekly",
      "duration": "until_task_complete"
    }
  ],
  "ownership": {
    "created_by": "user_id_123",
    "created_by_org_unit": "Store Support",
    "escalation_to": "{{created_by.direct_manager}}"
  },
  "maintenance": {
    "review_date": "2026-04-14",
    "review_reminder": "2026-03-14",
    "auto_disable_after_inactivity": "90 days"
  }
}
```

**Database Schema Needed:**
```
Tables:
├─ notification_rules
│  ├─ rule_id (PK)
│  ├─ rule_name
│  ├─ description
│  ├─ trigger_conditions (JSON)
│  ├─ actions (JSON)
│  ├─ ownership (creator, org_unit, escalation)
│  ├─ created_at
│  ├─ updated_at
│  ├─ review_due_date
│  ├─ is_active
│  └─ metadata (JSON)
│
├─ notification_executions
│  ├─ execution_id (PK)
│  ├─ rule_id (FK)
│  ├─ trigger_event_id
│  ├─ triggered_at
│  ├─ project_id (FK)
│  ├─ status (pending, sent, failed)
│  ├─ recipients (JSON)
│  └─ error_message
│
├─ notification_templates
│  ├─ template_id (PK)
│  ├─ template_name
│  ├─ channel (email, in_app, slack)
│  ├─ subject
│  ├─ body (with {{placeholders}})
│  ├─ created_by
│  └─ updated_at
│
├─ notification_audit
│  ├─ audit_id (PK)
│  ├─ rule_id (FK)
│  ├─ change_type (created, updated, disabled)
│  ├─ changed_by
│  ├─ changed_at
│  ├─ old_value (JSON)
│  └─ new_value (JSON)
│
└─ rule_maintenance_schedule
   ├─ maintenance_id (PK)
   ├─ rule_id (FK)
   ├─ review_date
   ├─ review_reminder_sent_date
   ├─ last_reviewed_by
   └─ next_review_due
```

**UI/Admin Components Needed:**
```
Admin Dashboard → Notification Rules
├─ Rule Builder (visual or JSON)
│  ├─ Trigger selection (project status, date, metric threshold)
│  ├─ Condition builder (AND/OR logic)
│  ├─ Action selection (notify, create task, schedule)
│  ├─ Template selection/creation
│  └─ Recipient selection (by role, org unit, direct reports)
│
├─ Rule Management
│  ├─ List of active rules with last execution
│  ├─ Enable/disable toggles
│  ├─ Edit/duplicate/delete
│  ├─ Test rule (run against sample data)
│  └─ View execution history
│
├─ Template Management
│  ├─ Create email/in-app/Slack templates
│  ├─ Template variables ({{placeholders}})
│  └─ Preview
│
└─ Maintenance Schedule
   ├─ Rules needing review
   ├─ Review reminders
   ├─ Ownership tracking when creator changes
   └─ Auto-disable for stale rules
```

**IMPACT ON BACKEND:**
- New tables: 6 tables (rules, executions, templates, audit, schedule, + logging)
- New services: `notification_engine_service`, `rule_execution_service`, `template_service`
- New API endpoints: `/api/v1/admin/notifications/*`
- New workers: Background job runner for rule triggers + reminders
- New dependencies: Job queue (Celery/Redis), Template engine (Jinja2)

---

### 2.5 HIERARCHY & ORG SYNC (HR Data Integration)

**Purpose:** Align user access, project ownership, and notification routing with org structure

**Current State:**
```
Users table has:
- id, email, full_name, role (single role)
- No org hierarchy
- No manager relationships
- No team associations
```

**Proposed State:**
```
Need to add:
├─ Organizational Unit (Department, Store, Region, District)
├─ Manager Relationships (who reports to whom)
├─ Team Membership
├─ Role History (for SOX compliance)
├─ Position Information
└─ HR Data Sync Status
```

**New Tables:**
```
├─ organizational_units
│  ├─ unit_id (PK)
│  ├─ unit_name
│  ├─ unit_type (Department, Store, Region, District, Area, Division)
│  ├─ parent_unit_id (FK - for hierarchy)
│  ├─ manager_id (FK - who manages this unit)
│  ├─ created_at
│  └─ hr_system_id (sync point with HR system)
│
├─ user_org_assignments
│  ├─ assignment_id (PK)
│  ├─ user_id (FK)
│  ├─ org_unit_id (FK)
│  ├─ position_title
│  ├─ assignment_date
│  ├─ end_date (nullable - if transferred)
│  ├─ is_current (boolean)
│  └─ hr_system_position_id
│
├─ user_manager_relationships
│  ├─ relationship_id (PK)
│  ├─ employee_id (FK - User)
│  ├─ manager_id (FK - User who manages)
│  ├─ relationship_start_date
│  ├─ relationship_end_date (nullable - if changed)
│  ├─ is_current (boolean)
│  └─ direct_report_order (rank for multi-manager scenarios)
│
├─ user_roles_history (SOX Compliance)
│  ├─ history_id (PK)
│  ├─ user_id (FK)
│  ├─ role (admin, manager, viewer, etc.)
│  ├─ role_assigned_date
│  ├─ role_removed_date
│  ├─ assigned_by
│  ├─ reason
│  └─ approval_id (if required)
│
├─ hr_sync_status
│  ├─ sync_id (PK)
│  ├─ last_sync_timestamp
│  ├─ next_scheduled_sync
│  ├─ status (success, partial_failure, failed)
│  ├─ records_processed
│  ├─ records_failed
│  ├─ error_log
│  └─ synced_by (system/user)
│
└─ user_team_memberships
   ├─ membership_id (PK)
   ├─ user_id (FK)
   ├─ team_id (FK)
   ├─ role_in_team
   ├─ joined_date
   └─ left_date (nullable)
```

**HR Sync Process:**
```
Schedule: Daily at 2 AM
1. Connect to HR system API/database
2. Get all user/org changes
3. Compare with current state
4. For changes:
   - Update org assignments
   - Update manager relationships
   - Create role history records
   - Log all changes for audit
5. Identify cascading changes:
   - If user changed managers → update notification ownerships
   - If user moved orgs → update access groups
   - If user left → reassign projects/notifications
6. Send change notification to admins
7. Log sync status + success metrics
```

**IMPACT ON BACKEND:**
- New tables: 6 tables
- New services: `hr_sync_service`, `org_hierarchy_service`, `access_sync_service`
- New API endpoints: `/api/v1/admin/org-sync/*`, `/api/v1/admin/hierarchy/*`
- New workers: Scheduled HR sync job (daily)
- New dependencies: HR system integration (API/database driver)

---

## Part 3: INTEGRATION ARCHITECTURE

### 3.1 Data Flow Diagram
```
┌──────────────────────────────────────────────────────────────────┐
│                         ACTIVITY HUB                              │
└──────────────────────────────────────────────────────────────────┘

External Data Sources:
├─ INTAKE HUB (BigQuery)
│  └─ Project management data
│     └─ API → Activity Hub
│        └─ Platform Bridge → Standardize
│           └─ Project Table
│
├─ AMP (Communications Platform)
│  └─ Communication activities
│     └─ API → Activity Hub
│        └─ Linked to Projects
│
├─ HR SYSTEM (daily sync)
│  └─ Org hierarchy + user info
│     └─ Scheduled sync → Activity Hub
│        └─ User, OrgUnit, Manager tables
│
└─ Future Platforms
   └─ TBD

Internal Processing:
├─ NOTIFICATION ENGINE
│  ├─ Monitors Project data
│  ├─ Evaluates rules
│  ├─ Executes actions
│  └─ Creates notifications + tasks
│
├─ REPORTING & METRICS
│  ├─ Aggregates project data
│  ├─ Calculates KPIs
│  └─ Generates dashboards
│
└─ ACCESS CONTROL
   ├─ Uses org hierarchy
   ├─ Enforces RBAC
   └─ Manages permissions
```

### 3.2 Key Dependencies Between Components
```
1. Platform Bridge depends on:
   - Project table schema (must be defined first)
   - Intake Hub BigQuery analysis (need to understand existing columns)

2. Notification Engine depends on:
   - Project table (what to trigger on)
   - User + Org tables (who to notify)
   - Notification templates (what to send)

3. Org Hierarchy depends on:
   - HR system connectivity (external dependency)
   - User roles history (SOX compliance)

4. All depends on:
   - Robust API authentication (platform-to-platform)
   - Error handling + retry logic
   - Audit logging for compliance
```

---

## Part 4: DATABASE SCHEMA IMPACT

### Current Database
```
Tables: ~6
├─ users
├─ stores
├─ activities
├─ communications
├─ kpis
└─ analytics_summaries
```

### Proposed Database (Phase 1)
```
Tables: ~18-20
│
├─ Core Projects
│  └─ projects (NEW - CENTRAL)
│
├─ Data Integration
│  ├─ platform_bridge_registry (NEW)
│  ├─ platform_bridge_mappings (NEW)
│  ├─ data_sync_logs (NEW)
│  └─ platform_configs (NEW)
│
├─ Notifications
│  ├─ notification_rules (NEW)
│  ├─ notification_executions (NEW)
│  ├─ notification_templates (NEW)
│  ├─ notification_audit (NEW)
│  └─ rule_maintenance_schedule (NEW)
│
├─ Organization
│  ├─ organizational_units (NEW)
│  ├─ user_org_assignments (NEW)
│  ├─ user_manager_relationships (NEW)
│  ├─ user_roles_history (NEW)
│  ├─ user_team_memberships (NEW)
│  └─ hr_sync_status (NEW)
│
└─ Existing (Enhanced)
   ├─ users (add manager_id, current_org_unit_id, last_sync)
   ├─ stores
   ├─ activities
   ├─ communications
   ├─ kpis
   └─ analytics_summaries
```

**Impact:** 3x increase in table count, significant increase in foreign key relationships

---

## Part 5: API EXPANSION

### Current API Endpoints
```
~12-15 endpoints focused on:
- Activities CRUD
- Stores CRUD
- Basic reporting
- WebSocket connections
```

### Proposed API Additions
```
New endpoint groups (~40+ endpoints):

1. Admin - Platform Management
   POST /api/v1/admin/platform-mappings/
   GET /api/v1/admin/platform-mappings/{platform}
   PUT /api/v1/admin/platform-mappings/{mapping_id}
   POST /api/v1/admin/sync/{platform}

2. Admin - Notification Rules
   GET /api/v1/admin/notifications/rules
   POST /api/v1/admin/notifications/rules
   PUT /api/v1/admin/notifications/rules/{rule_id}
   DELETE /api/v1/admin/notifications/rules/{rule_id}
   POST /api/v1/admin/notifications/rules/{rule_id}/test
   GET /api/v1/admin/notifications/rules/{rule_id}/executions

3. Admin - Notification Templates
   GET /api/v1/admin/notifications/templates
   POST /api/v1/admin/notifications/templates
   PUT /api/v1/admin/notifications/templates/{template_id}

4. Admin - Organization Sync
   GET /api/v1/admin/org-sync/status
   POST /api/v1/admin/org-sync/manual
   GET /api/v1/admin/org-sync/logs

5. Admin - Organization Hierarchy
   GET /api/v1/admin/hierarchy
   GET /api/v1/admin/hierarchy/{unit_id}/tree
   PUT /api/v1/admin/users/{user_id}/org-assignment

6. Platforms - Data Intake
   POST /api/v1/platforms/intake-hub/projects
   POST /api/v1/platforms/{platform}/sync

7. Projects
   GET /api/v1/projects
   GET /api/v1/projects/{id}
   POST /api/v1/projects
   PUT /api/v1/projects/{id}
```

**Impact:** API complexity increased by 3-4x, additional rate limiting/authentication needed

---

## Part 6: DEPENDENCY & TECHNOLOGY STACK IMPACT

### New External Dependencies
```
1. Job Queue System
   └─ Current: None
   └─ Needed: Celery + Redis OR AWS SQS
   └─ Use: Async rule execution, scheduled syncs

2. Template Engine
   └─ Current: None
   └─ Needed: Jinja2
   └─ Use: Notification message customization

3. HR System Integration
   └─ Current: None
   └─ Needed: API client for Walmart HR system
   └─ Use: Daily org hierarchy sync

4. BigQuery Client
   └─ Current: intake_hub_service exists
   └─ Needed: Enhanced BigQuery Python client
   └─ Use: Intake Hub data pull

5. Pub/Sub System
   └─ Current: WebSocket point-to-point
   └─ Needed: Redis Pub/Sub OR AWS SNS
   └─ Use: Broadcasting rule triggers across services
```

### Backend Stack Upgrade
```
Current:
- FastAPI (existing)
- SQLAlchemy (existing)
- Pydantic (existing)
- PostgreSQL (assumed)

Added:
+ Celery (async tasks)
+ Redis (caching, queue, pub/sub)
+ Jinja2 (templates)
+ APScheduler (scheduled jobs)
+ google-cloud-bigquery (BigQuery)
+ Additional auth libraries (OAuth2, API key validation)
```

---

## Part 7: CRITICAL DECISIONS & UNKNOWNS

### Decision 1: Intake Hub Schema Analysis
**Question:** What columns/fields does Intake Hub currently provide?  
**Data Source:** `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`  
**Impact:** Determines Project table structure + Platform Bridge design  
**Action Needed:** Query BigQuery to list all columns and understand data types

### Decision 2: Platform Bridge Implementation
**Options:**
```
A) Code-based mapping
   - Pros: Type-safe, versioned, reviewed
   - Cons: Requires code deploy for new mappings

B) Config-based mapping (JSON/YAML)
   - Pros: Hot-reload, admin UI possible
   - Cons: Less type-safe, needs validation layer

C) Hybrid (defaults in code, overrides in config)
   - Pros: Best of both
   - Cons: More complex
```
**Recommendation:** Start with Hybrid approach
**Action Needed:** Choose before schema design

### Decision 3: Notification Rule Engine
**Options:**
```
A) In-process evaluation
   - Pros: Simple, low latency
   - Cons: Can't scale horizontally

B) Separate service (microservice)
   - Pros: Independent scaling, better reliability
   - Cons: More operational complexity

C) Third-party rules engine
   - Pros: Battle-tested, feature-rich
   - Cons: Vendor lock-in, licensing
```
**Recommendation:** In-process + background workers initially (simpler), migrate to separate service if needed
**Action Needed:** Choose before architecture finalization

### Decision 4: HR System Integration
**Question:** What is the Walmart HR system?  
**Options:** SuccessFactors, Workday, custom system, etc.  
**Impact:** Integration complexity + API/database access method  
**Action Needed:** Determine HR system + access method before Phase 2

### Decision 5: Deployment & Scaling
**Question:** How many concurrent projects? How many users?  
**Impact:** Determines Redis sizing, database sizing, worker count  
**Action Needed:** Define SLA requirements (throughput, latency, availability)

### Decision 6: Audit & Compliance
**Question:** What compliance requirements apply? (SOX, GDPR, HIPAA, etc.)  
**Impact:** Audit logging depth, data retention, access controls  
**Action Needed:** Confirm compliance requirements before implementation

---

## Part 8: IMPLEMENTATION ROADMAP (Proposed)

### Phase 1: Foundation (Weeks 1-3)
```
Week 1:
├─ Finalize Project table schema (based on BigQuery analysis)
├─ Design Platform Bridge architecture
└─ Create database tables (projects, platform_bridge_*)

Week 2:
├─ Implement Intake Hub → Project data pipeline
├─ Create Platform Bridge column registry
├─ Add API endpoints for projects + sync status
└─ Unit tests

Week 3:
├─ Implement data validation + error handling
├─ Add audit logging
└─ Integration tests
```

### Phase 2: Notifications (Weeks 4-6)
```
Week 4:
├─ Design notification rule schema
├─ Create notification tables
└─ Build rule engine (basic triggers)

Week 5:
├─ Implement notification templates
├─ Build admin API endpoints
└─ Add notification execution + audit

Week 6:
├─ Build notification delivery (email, in-app, etc.)
├─ Add rule maintenance scheduler
└─ Testing
```

### Phase 3: Organization (Weeks 7-9)
```
Week 7:
├─ Design org hierarchy tables
├─ Implement HR sync service
└─ Create organization endpoints

Week 8:
├─ Implement manager relationships + access propagation
├─ Update notification routing to use org data
└─ Add role history for compliance

Week 9:
├─ Testing + compliance validation
└─ Documentation
```

### Phase 4: Hardening (Weeks 10+)
```
├─ Performance optimization
├─ Scaling to production volume
├─ Disaster recovery testing
├─ Security hardening
└─ Compliance audit
```

---

## Part 9: RISK ASSESSMENT

### High Risk
```
1. ✗ Intake Hub schema assumptions
   └─ Risk: If schema different than expected, Platform Bridge breaks
   └─ Mitigation: Analyze BigQuery schema FIRST

2. ✗ Real-time org sync from HR
   └─ Risk: If HR system unavailable, access controls could fail
   └─ Mitigation: Implement sync error handling + caching strategy

3. ✗ Notification rule complexity
   └─ Risk: Complex rules could cause performance issues
   └─ Mitigation: Rule execution monitoring + rate limiting

4. ✗ Multi-platform data conflicts
   └─ Risk: Different platforms send conflicting data
   └─ Mitigation: Conflict resolution rules + audit trail
```

### Medium Risk
```
1. Database complexity increase (3x tables)
   └─ Mitigation: Proper indexing, query optimization from start

2. Additional external dependencies
   └─ Mitigation: Implement circuit breakers, fallback logic

3. Admin UI complexity for rule builder
   └─ Mitigation: Start simple, iterate based on usage
```

### Low Risk
```
1. API expansion manageable with FastAPI
2. Existing code base provides good foundation
3. Database migration path clear
```

---

## Part 10: SUMMARY MATRIX

| Component | Complexity | Risk | Timeline | Effort | Dependencies |
|-----------|-----------|------|----------|--------|--------------|
| Project Table | Low | Low | Week 1 | 2 days | BigQuery schema |
| Platform Bridge | High | High | Weeks 1-2 | 4 days | Project schema |
| Intake Hub Integration | Medium | Medium | Weeks 1-3 | 3 days | BigQuery access |
| Notification Engine | High | High | Weeks 4-6 | 8 days | Rule schema |
| Org Hierarchy | Medium | High | Weeks 7-8 | 5 days | HR system access |
| Admin UI | Medium | Low | Weeks 3-10 | 10 days | APIs complete |

---

## NEXT STEPS FOR REVIEW

### Before Implementation Approval, Please Confirm:

- [ ] **BigQuery Analysis:** Examine `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` columns and provide findings
- [ ] **Project Scope:** Confirm Project table core columns (my suggestion in 2.1)
- [ ] **Platform Decision:** Choose Platform Bridge approach (A/B/C from 4.1)
- [ ] **Rule Engine Decision:** Choose notification engine approach (A/B/C from 4.2)
- [ ] **HR System:** Identify Walmart HR system + access method
- [ ] **Compliance:** Confirm audit/compliance requirements
- [ ] **SLAs:** Define performance requirements (throughput, latency, availability)
- [ ] **Timeline:** Confirm 9-week Phase 1-3 timeline is acceptable
- [ ] **Team:** Confirm resource allocation for implementation

---

## Questions for Discussion

1. **Intake Hub Data:** Can you share the BigQuery schema from Intake Hub, or should I help you query it?

2. **Platform Priority:** Is Intake Hub the only source initially, or are there other platforms ready now?

3. **Notification Urgency:** Are notifications critical path for MVP, or can they be Phase 2+?

4. **Admin Users:** Who will create/manage notification rules? Tech team or business users?

5. **Scalability:** Do you have volume projections? (Projects, users, data points/day)

6. **Budget:** Are there budget constraints on external services (BigQuery, HR system integration)?

7. **Timeline Feasibility:** Is 9 weeks realistic given current team capacity?

---

**Status:** AWAITING REVIEW & APPROVAL  
**Next Action:** Discuss this analysis and confirm decisions before proceeding to implementation

