# Distribution List Management Application
**Complete System Specification & Architecture**

## Overview
A comprehensive web application for managing Exchange Distribution Lists with automated synchronization based on configurable parameters, exception handling, and quarterly review workflows.

---

## System Architecture

### Technology Stack
```
Frontend:  HTML5 + JavaScript (Vanilla JS / Vue.js) → Code Puppy Pages
Backend:   Python Flask/FastAPI → Google Cloud Run
Database:  BigQuery (data warehouse) + Cloud SQL (operational)
Scheduler: Google Cloud Scheduler
Auth:      Walmart SSO (OAuth 2.0)
Storage:   Google Cloud Storage (audit logs, exports)
```

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Code Puppy Pages                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ List Manager │  │  Parameters  │  │  Validation  │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│              API Layer (Cloud Run)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │   Auth   │  │   CRUD   │  │ Validate │  │  Sync    │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
└───────┼─────────────┼─────────────┼─────────────┼───────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Cloud SQL   │  │   BigQuery   │  │   Exchange   │      │
│  │  (Config)    │  │  (Analytics) │  │   (DLs)      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
        ▲
        │
┌───────┴──────────────────────────────────────────────────────┐
│              Cloud Scheduler (Daily 5am)                      │
│  Triggers: Sync Job → Validate → Update DLs → Notify Owners  │
└──────────────────────────────────────────────────────────────┘
```

---

## Database Schema

### 1. `dl_lists` - Distribution List Registry
```sql
CREATE TABLE dl_lists (
    list_id VARCHAR(100) PRIMARY KEY,
    list_name VARCHAR(255) NOT NULL,
    list_email VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    department VARCHAR(100),
    business_unit VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    sync_enabled BOOLEAN DEFAULT FALSE,
    last_sync_date TIMESTAMP,
    member_count INT DEFAULT 0,
    naming_convention VARCHAR(255)
);
```

### 2. `dl_parameters` - Inclusion/Exclusion Rules
```sql
CREATE TABLE dl_parameters (
    parameter_id VARCHAR(100) PRIMARY KEY,
    list_id VARCHAR(100) REFERENCES dl_lists(list_id),
    parameter_type VARCHAR(50), -- 'job_code', 'title_pattern', 'department', 'hierarchy', 'custom_sql'
    parameter_tier INT, -- 1=Core, 2=Supporting, 3=Pattern
    condition_type VARCHAR(20), -- 'include', 'exclude'
    condition_operator VARCHAR(20), -- 'equals', 'contains', 'in', 'like', 'regex'
    condition_value TEXT, -- Job code, pattern, SQL WHERE clause
    priority INT DEFAULT 100,
    is_active BOOLEAN DEFAULT TRUE,
    created_by VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by VARCHAR(100),
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_reviewed_date TIMESTAMP,
    review_status VARCHAR(50) -- 'approved', 'pending', 'flagged'
);
```

### 3. `dl_exceptions` - Manual Additions/Removals
```sql
CREATE TABLE dl_exceptions (
    exception_id VARCHAR(100) PRIMARY KEY,
    list_id VARCHAR(100) REFERENCES dl_lists(list_id),
    email VARCHAR(255) NOT NULL,
    win VARCHAR(20),
    exception_type VARCHAR(20), -- 'add', 'remove'
    reason TEXT NOT NULL,
    requested_by VARCHAR(100),
    approved_by VARCHAR(100),
    approval_date TIMESTAMP,
    expiration_date TIMESTAMP, -- NULL = permanent
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_reviewed_date TIMESTAMP,
    review_status VARCHAR(50)
);
```

### 4. `dl_owners` - Access Control
```sql
CREATE TABLE dl_owners (
    owner_id VARCHAR(100) PRIMARY KEY,
    list_id VARCHAR(100) REFERENCES dl_lists(list_id),
    win VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role VARCHAR(50), -- 'owner', 'co-owner', 'admin'
    can_modify_parameters BOOLEAN DEFAULT TRUE,
    can_add_exceptions BOOLEAN DEFAULT TRUE,
    can_approve_exceptions BOOLEAN DEFAULT FALSE,
    notification_enabled BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(list_id, win)
);
```

### 5. `dl_validation_history` - Gap Analysis & Audit
```sql
CREATE TABLE dl_validation_history (
    validation_id VARCHAR(100) PRIMARY KEY,
    list_id VARCHAR(100) REFERENCES dl_lists(list_id),
    validation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    current_member_count INT,
    should_be_member_count INT,
    missing_member_count INT,
    extra_member_count INT,
    missing_members JSON, -- Array of emails
    extra_members JSON, -- Array of emails
    parameter_snapshot JSON, -- Current parameters at time of validation
    validation_status VARCHAR(50), -- 'passed', 'gaps_found', 'error'
    validation_summary TEXT
);
```

### 6. `dl_sync_log` - Daily Sync Audit Trail
```sql
CREATE TABLE dl_sync_log (
    sync_id VARCHAR(100) PRIMARY KEY,
    list_id VARCHAR(100) REFERENCES dl_lists(list_id),
    sync_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sync_type VARCHAR(50), -- 'scheduled', 'manual', 'parameter_change'
    members_added INT DEFAULT 0,
    members_removed INT DEFAULT 0,
    errors_encountered INT DEFAULT 0,
    sync_status VARCHAR(50), -- 'success', 'partial', 'failed'
    sync_duration_seconds INT,
    error_details JSON,
    triggered_by VARCHAR(100)
);
```

### 7. `dl_quarterly_reviews` - Review Workflow
```sql
CREATE TABLE dl_quarterly_reviews (
    review_id VARCHAR(100) PRIMARY KEY,
    list_id VARCHAR(100) REFERENCES dl_lists(list_id),
    review_quarter VARCHAR(10), -- '2025-Q1'
    review_due_date DATE,
    review_status VARCHAR(50), -- 'pending', 'in_progress', 'completed', 'overdue'
    parameters_reviewed BOOLEAN DEFAULT FALSE,
    exceptions_reviewed BOOLEAN DEFAULT FALSE,
    reviewed_by VARCHAR(100),
    reviewed_date TIMESTAMP,
    review_notes TEXT,
    action_items JSON,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## API Endpoints

### Authentication & Authorization
```
POST   /api/v1/auth/login          - SSO login
GET    /api/v1/auth/user           - Get current user info
GET    /api/v1/auth/permissions    - Get user permissions
```

### Distribution Lists
```
GET    /api/v1/lists                    - Get all lists (filtered by user access)
GET    /api/v1/lists/{list_id}          - Get list details
POST   /api/v1/lists                    - Create new list (admin only)
PUT    /api/v1/lists/{list_id}          - Update list metadata
DELETE /api/v1/lists/{list_id}          - Soft delete list (admin only)
GET    /api/v1/lists/{list_id}/members  - Get current members
```

### Parameters
```
GET    /api/v1/lists/{list_id}/parameters         - Get all parameters
POST   /api/v1/lists/{list_id}/parameters         - Create parameter (owner/admin)
PUT    /api/v1/lists/{list_id}/parameters/{id}    - Update parameter
DELETE /api/v1/lists/{list_id}/parameters/{id}    - Delete parameter
POST   /api/v1/lists/{list_id}/parameters/test    - Test parameters (dry run)
```

### Exceptions
```
GET    /api/v1/lists/{list_id}/exceptions         - Get all exceptions
POST   /api/v1/lists/{list_id}/exceptions         - Request exception
PUT    /api/v1/lists/{list_id}/exceptions/{id}    - Update exception
DELETE /api/v1/lists/{list_id}/exceptions/{id}    - Remove exception
POST   /api/v1/lists/{list_id}/exceptions/{id}/approve - Approve exception
```

### Validation & Analysis
```
POST   /api/v1/lists/{list_id}/validate           - Run validation check
GET    /api/v1/lists/{list_id}/validation-history - Get validation history
GET    /api/v1/lists/{list_id}/gaps               - Get current gaps
GET    /api/v1/lists/{list_id}/analysis           - Get analysis report
```

### Synchronization
```
POST   /api/v1/lists/{list_id}/sync               - Trigger immediate sync
GET    /api/v1/lists/{list_id}/sync-history       - Get sync history
GET    /api/v1/sync/schedule                      - Get scheduled syncs
```

### Quarterly Reviews
```
GET    /api/v1/lists/{list_id}/reviews            - Get review history
GET    /api/v1/reviews/pending                    - Get pending reviews (for owner)
POST   /api/v1/reviews/{review_id}/complete       - Complete review
```

### Owners & Access
```
GET    /api/v1/lists/{list_id}/owners             - Get list owners
POST   /api/v1/lists/{list_id}/owners             - Add owner (admin only)
DELETE /api/v1/lists/{list_id}/owners/{owner_id}  - Remove owner
```

### Naming Convention
```
GET    /api/v1/lists/{list_id}/naming             - Get naming convention
PUT    /api/v1/lists/{list_id}/naming             - Update naming convention
POST   /api/v1/lists/{list_id}/naming/apply       - Apply new naming to Exchange
```

---

## Frontend Views (Code Puppy Pages)

### 1. Dashboard (Landing Page)
- **My Lists** - Lists user owns/manages
- **Pending Actions** - Exceptions awaiting approval, reviews due
- **Recent Activity** - Sync logs, validations
- **Quick Stats** - Total members, lists managed, gaps found

### 2. List Management View
- **List Details** - Name, description, member count, last sync
- **Member Browser** - Search/filter current members
- **Quick Actions** - Validate Now, Sync Now, Export Members

### 3. Parameter Editor
- **Tier 1 Parameters** - Job codes (auto-include)
- **Tier 2 Parameters** - Supporting job codes
- **Tier 3 Parameters** - Title patterns, department filters
- **Custom SQL** - Advanced users (admin only)
- **Test Mode** - Preview results without applying
- **Priority Order** - Drag-and-drop to reorder

### 4. Validation Dashboard
- **Gap Analysis** - Missing members vs. Extra members
- **Top Missing Job Codes** - Visualization
- **Historical Trends** - Gap over time
- **Downloadable Reports** - CSV export

### 5. Exception Management
- **Add Exception** - Request form (email, reason, expiration)
- **Pending Exceptions** - Awaiting approval
- **Active Exceptions** - Currently applied
- **Exception History** - Audit trail

### 6. Quarterly Review Interface
- **Review Checklist** - Parameters, Exceptions, Members
- **Side-by-side Comparison** - Current vs. Last Quarter
- **Action Items** - Flagged issues
- **Approve & Submit** - Complete review

### 7. Admin Panel (Admin Only)
- **System Overview** - All lists, users, sync status
- **User Management** - Add/remove owners
- **Sync Schedule** - Configure timing
- **Audit Logs** - Full system activity

---

## Key Features

### 1. Parameter System
```javascript
// Example parameter structure
{
    "tier1": [
        {"type": "job_code", "value": "US-100015099", "name": "Market Manager"}
    ],
    "tier2": [
        {"type": "job_code", "value": "US-100017446", "name": "Senior Director, Merchandising"}
    ],
    "tier3": [
        {
            "type": "title_pattern",
            "pattern": "Senior Director",
            "condition": "AND",
            "additional_filters": [
                {"field": "department", "operator": "equals", "value": "HO"}
            ]
        }
    ]
}
```

### 2. Validation Engine
```python
def validate_list(list_id):
    # 1. Get current members from Exchange
    current_members = get_exchange_members(list_id)
    
    # 2. Query BigQuery with parameters
    should_be_members = query_with_parameters(list_id)
    
    # 3. Apply exceptions
    should_be_members = apply_exceptions(should_be_members, list_id)
    
    # 4. Calculate gaps
    missing = set(should_be_members) - set(current_members)
    extra = set(current_members) - set(should_be_members)
    
    # 5. Store results
    save_validation_results(list_id, missing, extra)
    
    return {
        "current_count": len(current_members),
        "should_be_count": len(should_be_members),
        "missing_count": len(missing),
        "extra_count": len(extra),
        "missing_members": list(missing),
        "extra_members": list(extra)
    }
```

### 3. Daily Sync Process (5am)
```python
# Cloud Scheduler → Cloud Function → Sync Process

def daily_sync_job():
    # 1. Get all lists with sync_enabled=True
    active_lists = get_active_lists()
    
    for list_id in active_lists:
        try:
            # 2. Validate list
            validation = validate_list(list_id)
            
            # 3. If gaps found, sync
            if validation['missing_count'] > 0 or validation['extra_count'] > 0:
                sync_list(list_id, validation)
            
            # 4. Log results
            log_sync_result(list_id, validation)
            
            # 5. Notify owners if significant changes
            if validation['missing_count'] > 50:
                notify_owners(list_id, validation)
                
        except Exception as e:
            log_error(list_id, e)
            notify_admins(list_id, e)
```

### 4. Exception Workflow
```
User Request → Owner Approval → Apply to List → Quarterly Review
```

### 5. Quarterly Review Process
```
Week 1 of Quarter → Generate Review → Notify Owners → 
Owner Reviews → Approve/Reject Changes → Update Parameters → 
Schedule Next Review
```

---

## Security & Compliance

### Authentication
- **Walmart SSO (OAuth 2.0)** - Single sign-on
- **WIN-based authorization** - Role mapping from AD

### Authorization Levels
1. **Viewer** - Can view lists they're a member of
2. **Owner** - Can modify parameters, add exceptions (own lists)
3. **Admin** - Full access to all lists and system settings

### Audit Trail
- All actions logged with WIN, timestamp, action type
- Immutable audit logs stored in BigQuery
- 7-year retention policy

### Data Privacy
- PII data (emails, WINs) encrypted at rest
- API rate limiting per user
- GDPR-compliant data exports

---

## Deployment Strategy

### Phase 1: MVP (4-6 weeks)
- Basic CRUD for lists and parameters
- Manual validation and sync
- Simple UI on Code Puppy Pages

### Phase 2: Automation (2-3 weeks)
- Daily scheduled sync
- Exception management
- Notification system

### Phase 3: Advanced Features (3-4 weeks)
- Quarterly review workflow
- Advanced analytics dashboard
- Naming convention management

### Phase 4: Optimization (2 weeks)
- Performance tuning
- User training
- Documentation

---

## Next Steps

1. **Approval** - Review architecture with stakeholders
2. **Environment Setup** - Create GCP project, databases
3. **Backend Development** - Build API layer
4. **Frontend Development** - Create UI
5. **Testing** - Unit, integration, UAT
6. **Deployment** - Staging → Production
7. **Training** - Owner/Admin training sessions

---

## Files to Create

### Backend (`api/`)
- `main.py` - Flask app entry point
- `models/` - Database models
- `routes/` - API endpoints
- `services/` - Business logic
- `utils/` - Helper functions
- `scheduler.py` - Daily sync job

### Frontend (`frontend/`)
- `index.html` - Landing page
- `list-manager.html` - List management
- `parameter-editor.html` - Parameter UI
- `validation-dashboard.html` - Gap analysis
- `exception-manager.html` - Exception handling
- `quarterly-review.html` - Review interface
- `js/app.js` - Main application logic
- `js/api.js` - API client
- `css/style.css` - Styling

### Database (`database/`)
- `schema.sql` - Table definitions
- `seed.sql` - Initial data
- `migrations/` - Schema changes

### Config
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container definition
- `app.yaml` - Cloud Run config
- `scheduler.yaml` - Cloud Scheduler config

---

*This is a comprehensive system design ready for implementation!*
