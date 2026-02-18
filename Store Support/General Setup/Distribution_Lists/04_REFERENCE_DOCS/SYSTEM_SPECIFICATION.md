# Distribution List Management System - Project Specification

## Vision
Self-service distribution list management platform where Business Owners can create, configure, and manage DLs based on dynamic job code parameters with automatic daily synchronization to Microsoft 365.

---

## Core Features

### 0. DL Selector & Email Composer Tool (Priority)
**Purpose:** Allow users to browse all DLs and compose emails to selected lists

**Features:**
- Searchable catalog of all 134,900+ distribution lists
- Filter by:
  - Name/keyword
  - Category (Operations, Market, Region, Support, Management, Team)
  - Size (Small <50, Medium 50-499, Large 500+)
  - Owner
- Multi-select DLs (checkbox interface)
- Preview DL details (member count, description, owner)
- "Compose Email" button → Opens Outlook/M365 with selected DLs in To/CC/BCC
- Save favorite DL combinations
- Recent selections history

**Technology:**
- Frontend: React with DataTables or AG-Grid for large list handling
- Backend: FastAPI serving DL catalog from database
- Search: Elasticsearch or PostgreSQL full-text search
- Data source: extract_all_dls_optimized.py output

**User Flow:**
1. User opens DL Selector tool
2. Searches/filters DLs (e.g., "market operations")
3. Selects multiple DLs via checkboxes
4. Clicks "Compose Email"
5. System generates mailto: link or opens Outlook Web with DLs pre-populated
6. User writes email and sends

### 1. Business Owner Web Interface
**Purpose:** Central portal for DL creation and management

**Features:**
- View all DLs owned by the user
- Search/browse existing DLs across organization
- Create new distribution lists
- Configure job code parameters and criteria
- Set geographical filters (Region, Market, Business Unit)
- Manage approval workflows
- View and manage exceptions
- Set permission levels per DL
- Publish/unpublish DLs to M365

**Technology Stack:**
- Frontend: React or Vue.js
- Backend: Flask/FastAPI (Python)
- Database: PostgreSQL or SQL Server
- Authentication: Windows AD/Azure AD SSO

---

### 2. Job Code Parameter System
**Purpose:** Define dynamic membership rules

**Parameters:**
- Job Codes (single or multiple)
- Job Families
- Job Levels (Director, Manager, Associate, etc.)
- Geographical filters:
  - Region(s)
  - Market(s)
  - Business Unit(s)
  - Store/Facility numbers
- Employment Status (Active only, Include contractors, etc.)
- Custom AD attributes

**Logic:**
- AND/OR conditions between parameters
- Inclusion/Exclusion rules
- Parameter templates for common patterns

---

### 3. Daily Automatic Update Engine
**Purpose:** Keep DLs synchronized with current workforce

**Process:**
1. **Scheduled Job** (runs daily, configurable time)
2. **Query Active Directory** for users matching parameters
3. **Apply job code filters** using Workday data
4. **Apply geographical filters** from AD attributes
5. **Check exception list** (add approved exceptions, remove denied)
6. **Calculate delta** (new adds, removes)
7. **Update M365 DL** via Graph API
8. **Send notification** to DL owner with changes summary
9. **Log all actions** to audit trail

**Components:**
- Python scheduler service (runs as Windows Service or cron job)
- AD query engine (uses existing ad_group_extractor.py logic)
- Workday integration (merge_workday_data.py)
- M365 Graph API client
- Email notification system
- Audit logging database

---

### 4. User Request & Approval Workflow
**Purpose:** Allow users to request DL access even if they don't meet criteria

**Flow:**

```
User submits request
    ↓
System checks parameters
    ↓
Does user meet criteria?
    ↓ No
Email sent to DL Owner
    - User details (name, job code, reason)
    - Approve/Deny links (secure tokens)
    ↓
Owner clicks Approve
    ↓
User added to exception list
    ↓
User added to DL immediately
    ↓
Confirmation email to user
    ↓
User remains until owner manually removes
```

**If Denied:**
- User receives notification
- Includes DL owner contact information
- Option to resubmit with additional justification

**Database Tables:**
- `requests` (id, user_email, dl_id, reason, status, requested_date)
- `exceptions` (id, user_email, dl_id, approved_by, approved_date, notes)
- `audit_log` (id, action, dl_id, user_email, timestamp, performed_by)

---

### 5. DL Creation & Publishing Interface
**Purpose:** Streamlined DL lifecycle management

**Workflow:**
1. **Create New DL**
   - DL Name (validated for uniqueness)
   - Display Name
   - Description
   - Owner(s) assignment
   - Status: Draft/Published

2. **Configure Parameters**
   - Add job code criteria
   - Set geographical filters
   - Define permission rules
   - Preview membership (shows count + sample users)

3. **Publish**
   - Validation checks (no conflicts, valid parameters)
   - Creates DL in M365 via Graph API
   - Populates initial membership
   - Schedules for daily updates
   - Publishes to Global Address List

4. **Update Published DL**
   - Modify parameters (takes effect next daily run)
   - Immediate update option (runs sync now)
   - Change history tracking

5. **Unpublish/Archive**
   - Removes from M365 (optional)
   - Retains configuration for re-activation
   - Maintains audit history

---

### 6. Permission Management System
**Purpose:** Control who can use/see each DL

**Permission Levels:**
- **All Users** - Anyone can send to DL (default)
- **Restricted** - Only specific job codes can send
- **Internal Only** - No external recipients
- **Owner Only** - Only DL owners can send
- **Hidden from GAL** - Not visible in address book search

**Job Code-Based Access:**
- Define which job codes can send to DL
- Inherit from organizational hierarchy
- Override with specific user exceptions

**Implementation:**
- M365 "SendAs" and "SendOnBehalfOf" permissions
- "HiddenFromAddressListsEnabled" property
- "RequireSenderAuthenticationEnabled" setting

---

## System Architecture

### Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     Business Owner Web UI                        │
│         (React/Vue - Create, Configure, Manage DLs)             │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────────┐
│                   REST API Backend (FastAPI)                     │
│  - DL CRUD operations                                            │
│  - Parameter management                                          │
│  - User request handling                                         │
│  - Approval workflow                                             │
└───┬────────────┬────────────┬────────────┬───────────────────────┘
    │            │            │            │
    ↓            ↓            ↓            ↓
┌───────┐   ┌───────┐   ┌─────────┐   ┌──────────┐
│ SQL   │   │ AD    │   │ Workday │   │ M365     │
│ DB    │   │ Query │   │ API     │   │ Graph    │
│       │   │ Engine│   │         │   │ API      │
└───────┘   └───────┘   └─────────┘   └──────────┘
                   ↑
                   │
┌──────────────────┴──────────────────────────────────────────────┐
│              Daily Update Scheduler Service                      │
│  - Runs daily (configurable schedule)                           │
│  - Queries AD for users matching DL parameters                  │
│  - Merges with Workday job data                                 │
│  - Calculates membership changes                                │
│  - Updates M365 DLs via Graph API                               │
│  - Sends notification emails                                    │
│  - Logs all changes to audit trail                              │
└─────────────────────────────────────────────────────────────────┘
```

### Data Model

**Core Tables:**

```sql
-- Distribution Lists
CREATE TABLE distribution_lists (
    id INT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    description TEXT,
    owner_email VARCHAR(255),
    status VARCHAR(20), -- Draft, Published, Archived
    created_date DATETIME,
    published_date DATETIME,
    last_updated DATETIME,
    m365_group_id VARCHAR(255)
);

-- DL Parameters (job code rules)
CREATE TABLE dl_parameters (
    id INT PRIMARY KEY,
    dl_id INT REFERENCES distribution_lists(id),
    parameter_type VARCHAR(50), -- JobCode, JobFamily, JobLevel, Region, Market, BU
    parameter_value VARCHAR(255),
    operator VARCHAR(10), -- Equals, Contains, In, NotIn
    logic VARCHAR(5) -- AND, OR
);

-- Exceptions (manual adds)
CREATE TABLE dl_exceptions (
    id INT PRIMARY KEY,
    dl_id INT REFERENCES distribution_lists(id),
    user_email VARCHAR(255),
    approved_by VARCHAR(255),
    approved_date DATETIME,
    reason TEXT,
    status VARCHAR(20) -- Active, Removed
);

-- Access Requests
CREATE TABLE access_requests (
    id INT PRIMARY KEY,
    dl_id INT REFERENCES distribution_lists(id),
    user_email VARCHAR(255),
    requested_date DATETIME,
    reason TEXT,
    status VARCHAR(20), -- Pending, Approved, Denied
    reviewed_by VARCHAR(255),
    reviewed_date DATETIME,
    approval_token VARCHAR(255)
);

-- Permission Rules
CREATE TABLE dl_permissions (
    id INT PRIMARY KEY,
    dl_id INT REFERENCES distribution_lists(id),
    permission_type VARCHAR(50), -- SendAs, ViewOnly, Restricted
    job_code VARCHAR(20),
    allow_deny VARCHAR(10) -- Allow, Deny
);

-- Audit Log
CREATE TABLE audit_log (
    id INT PRIMARY KEY,
    dl_id INT REFERENCES distribution_lists(id),
    action VARCHAR(50), -- Created, Updated, MemberAdded, MemberRemoved, Published
    user_email VARCHAR(255),
    performed_by VARCHAR(255),
    timestamp DATETIME,
    details TEXT
);

-- User Cache (from AD + Workday merge)
CREATE TABLE user_cache (
    email VARCHAR(255) PRIMARY KEY,
    username VARCHAR(100),
    display_name VARCHAR(255),
    job_code VARCHAR(20),
    job_description VARCHAR(255),
    job_level VARCHAR(50),
    region VARCHAR(100),
    market VARCHAR(100),
    business_unit VARCHAR(100),
    employment_status VARCHAR(50),
    last_updated DATETIME
);
```

---

## Technology Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI (high performance, async)
- **Database:** PostgreSQL 14+ or SQL Server
- **ORM:** SQLAlchemy
- **Task Scheduler:** APScheduler or Celery
- **API Client:** Microsoft Graph SDK for Python

### Frontend
- **Framework:** React 18 with TypeScript
- **UI Library:** Material-UI or Ant Design
- **State Management:** Redux Toolkit or Zustand
- **Forms:** React Hook Form
- **HTTP Client:** Axios

### Infrastructure
- **Authentication:** Azure AD / Windows AD SSO
- **Hosting:** Windows Server or Linux (Docker containers)
- **Email:** Exchange Web Services or SMTP
- **Logging:** Python logging + ELK stack
- **Monitoring:** Prometheus + Grafana

---

## Implementation Phases

### Phase 1: Foundation (Weeks 1-3)
- [ ] Set up database schema
- [ ] Build REST API for DL CRUD operations
- [ ] Create parameter management endpoints
- [ ] Implement AD query engine (extend existing scripts)
- [ ] Set up Workday data merge pipeline

### Phase 2: Web Interface (Weeks 4-6)
- [ ] Design UI mockups
- [ ] Build React frontend framework
- [ ] Implement DL creation wizard
- [ ] Build parameter configuration UI
- [ ] Add preview/validation features

### Phase 3: Daily Update Engine (Weeks 7-9)
- [ ] Build scheduled service
- [ ] Implement membership calculation logic
- [ ] Integrate M365 Graph API
- [ ] Add exception handling
- [ ] Create email notification system

### Phase 4: Approval Workflow (Weeks 10-11)
- [ ] Build request submission UI
- [ ] Create approval email templates
- [ ] Implement secure token system
- [ ] Build exception management
- [ ] Add owner notification system

### Phase 5: Permissions & Publishing (Weeks 12-13)
- [ ] Implement permission rules engine
- [ ] Build M365 DL creation via Graph API
- [ ] Add publish/unpublish functionality
- [ ] Implement permission sync to M365

### Phase 6: Testing & Deployment (Weeks 14-16)
- [ ] Comprehensive testing (unit, integration, E2E)
- [ ] Performance testing with production data size
- [ ] Security audit
- [ ] Staging environment deployment
- [ ] Production deployment
- [ ] User training and documentation

---

## API Endpoints

### Distribution Lists
```
GET    /api/dls                  - List all DLs (filtered by owner)
GET    /api/dls/{id}             - Get DL details
POST   /api/dls                  - Create new DL
PUT    /api/dls/{id}             - Update DL
DELETE /api/dls/{id}             - Archive DL
POST   /api/dls/{id}/publish     - Publish DL to M365
POST   /api/dls/{id}/unpublish   - Unpublish DL
GET    /api/dls/{id}/preview     - Preview membership
POST   /api/dls/{id}/sync-now    - Trigger immediate sync
```

### Parameters
```
GET    /api/dls/{id}/parameters  - Get DL parameters
POST   /api/dls/{id}/parameters  - Add parameter
PUT    /api/parameters/{id}      - Update parameter
DELETE /api/parameters/{id}      - Remove parameter
```

### Requests
```
POST   /api/requests             - Submit access request
GET    /api/requests/{id}        - Get request details
POST   /api/requests/{id}/approve - Approve request (with token)
POST   /api/requests/{id}/deny   - Deny request (with token)
GET    /api/dls/{id}/requests    - List requests for DL
```

### Exceptions
```
GET    /api/dls/{id}/exceptions  - List exceptions
POST   /api/dls/{id}/exceptions  - Add manual exception
DELETE /api/exceptions/{id}      - Remove exception
```

### Users
```
GET    /api/users/search         - Search users by name/email
GET    /api/users/{email}        - Get user details (job code, etc.)
```

---

## Security Considerations

1. **Authentication:** Azure AD SSO for all users
2. **Authorization:** Only DL owners can modify their DLs
3. **API Security:** JWT tokens, rate limiting
4. **Approval Tokens:** Time-limited, single-use tokens for email approvals
5. **Audit Trail:** Log all changes with timestamp and user
6. **Data Privacy:** Only expose necessary user information
7. **M365 Permissions:** Use service account with minimum required Graph API permissions

---

## Success Metrics

- **Time to create DL:** < 5 minutes
- **Daily sync completion:** < 30 minutes
- **System uptime:** 99.5%
- **Request approval time:** < 24 hours average
- **User satisfaction:** > 4/5 rating

---

## Future Enhancements

- Mobile app for approvals
- Slack/Teams bot integration
- Advanced analytics dashboard
- AI-suggested parameters based on patterns
- Bulk DL operations
- DL templates/cloning
- Integration with other HR systems
- Self-service troubleshooting tools

---

**Document Version:** 1.0  
**Date:** December 16, 2025  
**Status:** Planning Phase
