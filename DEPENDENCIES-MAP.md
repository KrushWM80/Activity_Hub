# 🔗 Dependencies Map - Activity Hub System

**Purpose**: Detailed mapping of component relationships, data flows, and architectural dependencies  
**Last Updated**: February 17, 2026  
**Status**: Active Reference Document

---

## 📋 Table of Contents

1. [System Architecture](#-system-architecture)
2. [Layer Dependencies](#-layer-dependencies)
3. [Component Relationships](#-component-relationships)
4. [Data Flow Diagrams](#-data-flow-diagrams)
5. [File Dependencies](#-file-dependencies)
6. [Configuration Dependencies](#-configuration-dependencies)
7. [External Integrations](#-external-integrations)
8. [Dependency Matrix](#-dependency-matrix)

---

## 🏗️ System Architecture

### **Three-Tier Architecture Overview**

```
┌────────────────────────────────────────────────────────────────────┐
│ PRESENTATION TIER (User Interface)                                  │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐               │
│  │ Landing     │  │   Admin     │  │   Projects   │  ...          │
│  │ Page        │  │ Dashboard   │  │ Management   │               │
│  └─────────────┘  └─────────────┘  └──────────────┘               │
│                                                                      │
│  Dependencies: Design System, Role Manager, Notification System    │
└────────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────────┐
│ APPLICATION TIER (Business Logic & Services)                        │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Role       │  │   Access     │  │  Permission  │             │
│  │   Manager    │  │  Controller  │  │   Engine     │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Data-Bridge  │  │ Sparky AI    │  │  Notification│             │
│  │ (Transform)  │  │  Assistant   │  │   Engine     │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  Dependencies: PostgreSQL, Redis, Elasticsearch, Authentication    │
└────────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────────┐
│ DATA TIER (Persistence & External Systems)                          │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ PostgreSQL   │  │    Redis     │  │ Elasticsearch│             │
│  │ Transaction  │  │  Caching &   │  │  Full-Text   │             │
│  │    Data      │  │   Sessions   │  │   Search     │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐                               │
│  │ File Storage │  │ AD Directory │                               │
│  │  (Projects)  │  │ (Auth)       │                               │
│  └──────────────┘  └──────────────┘                               │
│                                                                      │
│  External: AWS/Azure Cloud, Sparky API, OpenAI                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Layer Dependencies

### **Layer 1: Presentation (User Interface)**

**Components:**
- Landing Page (For You)
- Admin Dashboard
- Projects Interface
- My Work, Notifications, Settings, Teams
- Reporting Views

**Direct Dependencies:**
```
Landing Page
├── Design System (styles, colors, typography)
├── Role Manager (personalization per user role)
├── Navigation Links (dynamic-links.json)
├── Notification System (announcements, alerts)
└── Authentication (user identity verification)

Admin Dashboard
├── Role Configuration (role-configuration.json)
├── Access Groups (access-groups.json)
├── Dynamic Links (dynamic-links.json)
├── Data Schemas (validation rules)
├── Data Mappings (field transformations)
└── Backend API (CRUD operations)

Projects Interface
├── Design System
├── Data-Bridge (transformations)
├── Project Schema (validation)
├── File Upload System
├── Backend API (project CRUD)
└── Progress Tracking System
```

**Reverse Dependencies (What depends on these):**
- All features depend on consistent UI
- Navigation depends on dynamic-links.json
- All protected pages depend on authentication

---

### **Layer 2: Application (Business Logic)**

**Core Services:**

#### **Role Manager Service**
```
Role Manager
├── Input: User identity from AD/SSO
├── Lookup: role-configuration.json
├── Process: Permission evaluation
├── Output: Role tier (1-8), associated permissions
└── Consumed By: Access Control, Admin Dashboard, All Interfaces
```

**Dependencies:**
- role-configuration.json (configuration)
- Active Directory (user identity)
- Access Control Service (enforcement)

**Dependents:**
- Access Control Engine
- All UI components (for personalization)
- Permission Engine

---

#### **Access Control Service**
```
Access Control
├── Input: User, requested resource, action
├── Lookup: access-groups.json + role-configuration.json
├── Verify: AD group membership
├── Evaluate: Permission rules
├── Output: Allow/Deny decision
└── Consumed By: All API endpoints, UI access checks
```

**Dependencies:**
- access-groups.json (group mappings)
- role-configuration.json (permission matrices)
- Active Directory (group verification)
- Role Manager Service (role lookup)

**Dependents:**
- Admin API endpoints
- Protected UI pages
- Data API endpoints
- File upload service

---

#### **Permission Engine**
```
Permission Engine
├── Role + Resource → Permission Rules
├── Handles: granular permission checks
├── Examples: enterprise.view.all, department.view.multiple
├── Output: boolean (permitted/denied)
└── Consumed By: All authorization-required endpoints
```

**Dependencies:**
- role-configuration.json (permission definitions)
- Access Control Service (role + group info)

---

#### **Data-Bridge (Transformation Service)**
```
Data-Bridge
├── Transformations (transformations.js)
│   ├── Field mapping (external → internal schema)
│   ├── Data type conversion
│   ├── Value transformation
│   └── Aggregation/filtering logic
│
├── Validators (validators.js)
│   ├── Schema validation (projects-schema.json)
│   ├── Data quality checks
│   ├── Business rule validation
│   └── Output: validation errors or clean data
│
└── Flows:
    File Input → Validator → Schema Check → Transformer → Storage
```

**Dependencies:**
- Data Schemas (projects-schema.json, etc.)
- Data Mappings (intake-hub-mapping.json, etc.)
- File Upload System
- PostgreSQL (output data store)

**Dependents:**
- Projects Management (project data)
- Reporting (data aggregation)
- Analytics (data for analysis)

---

#### **Sparky AI Assistant Service**
```
Sparky AI Service
├── Query Processing (POST /api/v1/assistant/query)
├── Context Awareness (page, user, visible data)
├── NLP Processing (intent, entities)
├── Response Generation
├── Suggestion Engine
└── Action Recommendations
```

**Dependencies:**
- Node.js + Express API
- Python + FastAPI (ML processing)
- PostgreSQL (conversation history)
- Redis (session cache)
- Elasticsearch (knowledge search)
- Sparky API (Walmart AI service)
- OpenAI API (backup NLP)

**Dependents:**
- Landing Page (assistant widget)
- Admin Dashboard (help system)
- All UI pages (contextual help)

---

#### **Notification System**
```
Notification Engine
├── Trigger Types: System events, user actions, alerts
├── Processing: Route → Filter → Prioritize
├── Storage: Temporal notification queue
├── Delivery: Real-time, batch, scheduled
└── Display: Bell icon, in-app, email, SMS
```

**Dependencies:**
- Event stream (system events)
- User preferences (notification settings)
- Role-based rules (notification routing)
- Content templates
- PostgreSQL (history)
- Redis (queue)

**Dependents:**
- Landing Page (notifications bell)
- All UI pages (system alerts)
- Admin Dashboard (alerts)

---

### **Layer 3: Data (Persistence & Storage)**

**Databases:**

#### **PostgreSQL (Transactional Data)**
```
PostgreSQL Database
├── Tables:
│   ├── users (identity, profile, roles)
│   ├── projects (project master data)
│   ├── tasks (work items)
│   ├── teams (team definitions)
│   ├── roles (role definitions, mirrored from role-configuration.json)
│   ├── permissions (permission assignments)
│   ├── access_groups (mirrored from access-groups.json)
│   ├── notifications (notification history)
│   ├── conversation_logs (Sparky AI history)
│   ├── audit_logs (system audit trail)
│   └── ... (operational tables)
│
└── Used By: All backend services
```

**Dependencies:**
- Initial seed data from configuration files
- Input from Data-Bridge transformations
- Input from file uploads

**Dependents:**
- Role Manager (user lookup)
- Access Control (permission checks)
- All API endpoints (data access)
- Reporting (aggregations)

---

#### **Redis (Caching & Session Store)**
```
Redis Cache
├── Session Data: user sessions, auth tokens
├── Cache: frequently accessed data (roles, permissions)
├── Temporary: pending uploads, processing queues
├── TTL: expire sessions, cache entries
│
└── Used By: All services requiring fast access
```

**Dependencies:**
- PostgreSQL (source of truth)
- Session management service

**Dependents:**
- Authentication (session lookup)
- Role Manager (cache roles)
- Access Control (cache permissions)
- Sparky AI (session context)

---

#### **Elasticsearch (Full-Text Search)**
```
Elasticsearch Cluster
├── Indexes:
│   ├── projects_index (project name, description)
│   ├── tasks_index (task titles, descriptions)
│   ├── knowledge_index (documentation, help, FAQs)
│   ├── audit_index (system audit events)
│   └── ... (searchable content)
│
└── Used By: Search features, analytics, reporting
```

**Dependencies:**
- PostgreSQL (source documents)
- Document indexing pipeline

**Dependents:**
- Search feature (projects, tasks, docs)
- Analytics (trend analysis)
- Sparky AI (knowledge search)

---

**File Storage (AWS S3 / Azure Blob):**
```
Cloud File Store
├── Project uploads directory
├── Report storage
├── User documents
├── System backups
│
└── Used By: File upload/download services
```

**Dependencies:**
- Cloud provider account/credentials
- Upload service

**Dependents:**
- Projects Management (project files)
- Reporting (export storage)
- Data-Bridge (file input)

---

**Active Directory / SSO:**
```
AD Integration
├── User authentication (login)
├── Group membership verification
├── User profile attributes
├── MFA integration (optional)
│
└── Used By: Authentication system
```

**Dependencies:**
- Walmart enterprise AD infrastructure
- SSO configuration

**Dependents:**
- All UI pages (authentication required)
- Role Manager (group lookups)
- Access Control (group verification)

---

## 🔄 Component Relationships

### **Interface → Configuration Files**

```
┌─────────────────────────────┐
│  Admin Dashboard (HTML)      │
└─────────────────────────────┘
          ↓
┌─────────────────────────────┐
│ Reads/Updates Configuration │
└─────────────────────────────┘
          ↓
┌────────────────┬─────────────────────────┬────────────────┐
│                │                         │                │
↓                ↓                         ↓                ↓
role-            access-              dynamic-         data-
configuration    groups.json          links.json       schemas
.json
```

### **Configuration → Services → UI**

```
Role Config (JSON)
    ↓
Role Manager Service
    ↓
    ├→ Landing Page (personalization)
    ├→ Admin Dashboard (role listing)
    └→ Access Control (permission checks)

Access Groups (JSON)
    ↓
Access Control Service
    ↓
    └→ All Protected Pages (access checks)

Dynamic Links (JSON)
    ↓
Navigation System
    ↓
    ├→ Landing Page (link display)
    ├→ Admin Dashboard (link management)
    └→ All Pages (navigation menu)
```

### **Data Schema → Validation → Storage**

```
Project Schema (JSON)
    ↓
Validators (validators.js)
    ↓
    ├→ UI Form Validation
    ├→ File Upload Validation
    └→ API Request Validation
           ↓
        PostgreSQL (valid data stored)
           ↓
        Elasticsearch (indexed for search)
```

### **Design System → All Interfaces**

```
Design System (DESIGN_SYSTEM.md)
    ├→ walmart-brand-variables.css
    │   ├→ Landing Page
    │   ├→ Admin Dashboard
    │   ├→ Projects Interface
    │   ├→ All UI Components
    │   └→ Responsive Layouts
    │
    └→ WIDGET_SPECIFICATIONS.md
        ├→ Component Library
        ├→ Button Styles
        ├→ Card Components
        └→ Form Elements
```

---

## 📊 Data Flow Diagrams

### **User Login & Authorization Flow**

```
User Browser
    ↓ (Login Request)
├─────────────────────────────────────────
│ Authentication Service                   │
├─────────────────────────────────────────
    ↓ (Verify Credentials)
Active Directory / SSO
    ↓ (User ID + Group Membership)
├─────────────────────────────────────────
│ Role Manager Service                     │
├─────────────────────────────────────────
    ↓ (Lookup role-configuration.json)
    ↓ (Determine role tier 1-8)
    ↓ (Load permissions)
├─────────────────────────────────────────
│ Session Service (Redis)                  │
├─────────────────────────────────────────
    ↓ (Store session + auth token)
├─────────────────────────────────────────
│ Landing Page Rendering                   │
├─────────────────────────────────────────
    ↓ (Personalize based on role)
User Dashboard
```

### **Project Upload & Processing Flow**

```
User Browser (Projects Upload Page)
    ↓ (Select file + metadata)
├─────────────────────────────────────────
│ API: POST /api/projects/upload           │
├─────────────────────────────────────────
    ↓
├─────────────────────────────────────────
│ Access Control Check                     │
│ (Does user have upload permission?)      │
├─────────────────────────────────────────
    ↓ (Verified)
├─────────────────────────────────────────
│ File Upload Service                      │
├─────────────────────────────────────────
    ↓ (Save to Cloud Storage)
    ↓
├─────────────────────────────────────────
│ Data-Bridge Processing                   │
├─────────────────────────────────────────
    ↓ (Read file)
    ├→ Validator (validate against projects-schema.json)
    │   └→ Extract fields
    ├→ Transformer (apply intake-hub-mapping.json)
    │   └→ Convert to internal format
    └→ Enrich (add metadata, timestamps)
        ↓
├─────────────────────────────────────────
│ PostgreSQL                               │
├─────────────────────────────────────────
    ↓ (Insert project record)
    ↓
├─────────────────────────────────────────
│ Elasticsearch Indexing                   │
├─────────────────────────────────────────
    ↓ (Index for search)
    ↓
├─────────────────────────────────────────
│ Response to UI                           │
├─────────────────────────────────────────
User Sees: "Project uploaded successfully"
```

### **Admin Dashboard Configuration Update Flow**

```
Admin User (Admin Dashboard)
    ↓ (Modify role permissions)
    ├→ Update role-configuration.json (adds permission)
    ├→ Save to repository/backend
    │
    ↓ (Trigger deployment)
│
├─────────────────────────────────────────
│ Configuration Validation Service         │
├─────────────────────────────────────────
    ↓ (Verify JSON structure)
    ├→ Check permission names exist
    ├→ Validate role hierarchy
    └→ Confirm no conflicts
        ↓
├─────────────────────────────────────────
│ Role Manager Cache Update                │
├─────────────────────────────────────────
    ↓ (Invalidate Redis cache)
    ↓ (Reload role-configuration.json)
        ↓
├─────────────────────────────────────────
│ Active Sessions Update                   │
├─────────────────────────────────────────
    ↓ (Next request: user gets new permissions)
        ↓
All affected users automatically get new permissions
```

### **Sparky AI Assistant Query Flow**

```
User (On any page) Types: "Why is Project X delayed?"
    ↓
├─────────────────────────────────────────
│ Sparky AI Service (POST /api/assistant) │
├─────────────────────────────────────────
    ↓
├─────────────────────────────────────────
│ Context Gathering                        │
├─────────────────────────────────────────
    ├→ Page context (current URL/data)
    ├→ User context (role, department)
    ├→ Session data (recent actions)
    └→ Visible data (projects on dashboard)
        ↓
├─────────────────────────────────────────
│ NLP Processing (Python/FastAPI)          │
├─────────────────────────────────────────
    ├→ Intent detection (query type)
    ├→ Entity extraction (Project X)
    └→ Context matching
        ↓
├─────────────────────────────────────────
│ Data Search & Retrieval                  │
├─────────────────────────────────────────
    ├→ Elasticsearch (search docs)
    ├→ PostgreSQL (project data)
    ├→ Knowledge base lookup
    └→ Historical data analysis
        ↓
├─────────────────────────────────────────
│ Response Generation                      │
├─────────────────────────────────────────
    ├→ Sparky API (natural response text)
    ├→ Suggestions (related questions)
    └→ Actions (highlight, links, navigation)
        ↓
├─────────────────────────────────────────
│ Logging & Analytics                      │
├─────────────────────────────────────────
    ├→ PostgreSQL (save conversation)
    ├→ Elasticsearch (index for analytics)
    └→ Redis (session cache)
        ↓
User Sees: "Project X is delayed due to [reason]. Would you like to [action]?"
```

---

## 📁 File Dependencies

### **Configuration Files**

#### **role-configuration.json**
```
Location: Interface/Admin/role-configuration.json
Type: Master configuration (source of truth for roles)

Depends On:
├── (None - foundational file)

Used By:
├── Role Manager Service (primary)
├── Access Control Service (permission lookup)
├── Admin Dashboard (display/edit)
├── Report generator (role-based reports)
├── All API endpoints (permission checks)
└── All UI pages (personalization)

Impact of Changes:
├── Immediate: Cache invalidation needed
├── Sessions: Next request applies new permissions
├── Admin: Ability to adjust role tiers
└── Users: Automatic permission updates
```

#### **access-groups.json**
```
Location: Interface/Admin/access-groups.json
Type: AD integration configuration

Depends On:
├── Active Directory schema
└── Role configuration (role IDs referenced)

Used By:
├── Access Control Service (primary)
├── Authentication (group verification)
├── Admin Dashboard (AD group management)
└── Permission evaluation (group membership)

Example Structure:
{
  "groups": [
    {
      "ad_group": "Walmart-Operations-Managers",
      "roles": ["manager"],
      "permissions": ["department.view.all"]
    }
  ]
}

Sync Method: Changes in AD automatically affect user permissions
```

#### **dynamic-links.json**
```
Location: Interface/Admin/dynamic-links.json
Type: Navigation and link configuration

Depends On:
├── Design System (link styles)
└── (Optional) External URLs

Used By:
├── Landing Page (navigation)
├── Admin Dashboard (link management UI)
├── All pages (header/footer navigation)
└── Navigation service

Link Categories:
├── Main navigation
├── Department-specific
├── Role-based visibility
├── External resources
└── Admin tools
```

#### **Data Schemas**
```
Location: Interface/Admin/Data-Bridge/Schemas/
Type: Data validation definitions

Files:
├── projects-schema.json (project data structure)
├── _schema-template.json (template for new schemas)

Depends On:
├── (None - foundational)

Used By:
├── Validators (validation rules)
├── Data-Bridge (transformation rules)
├── API (request validation)
├── UI forms (field validation)
└── PostgreSQL (column definitions)

Example:
{
  "project": {
    "name": { "type": "string", "required": true },
    "status": { "type": "enum", "values": ["active", "closed"] },
    "dueDate": { "type": "date" }
  }
}
```

#### **Data Mappings**
```
Location: Interface/Admin/Data-Bridge/Mappings/
Type: External data transformation definitions

Files:
├── Projects/intake-hub-mapping.json
├── _mapping-template.json

Depends On:
├── Data Schemas (target schema)
├── External data sources (source schema)

Used By:
├── Data-Bridge Transformer (primary)
├── File upload validation
└── External data integration

Example:
{
  "mappings": [
    {
      "source": "ext_project_name",
      "target": "name",
      "transformation": "trim | capitalize"
    }
  ]
}
```

### **Code Files**

#### **transformations.js**
```
Location: Platform/Data-Bridge/Transformations/transformations.js
Type: Transformation logic implementation

Imports/Requires:
├── Data Mappings (configuration)
└── Schema definitions (validation rules)

Exports:
├── transformField(source, mapping)
├── validateData(data, schema)
├── transformProject(externalData)
└── transformAndValidate(data, schema, mapping)

Used By:
├── Data-Bridge Service (primary)
├── File upload processor
├── External data import
└── API data normalizers

Common Operations:
├── Field type conversion
├── Field name mapping
├── Data enrichment (add metadata)
├── Aggregation (combine fields)
└── Filtering (remove unwanted data)
```

#### **validators.js**
```
Location: Platform/Data-Bridge/Transformations/validators.js
Type: Data validation logic

Imports/Requires:
├── Data Schemas (validation rules)
└── transformations.js (transform helpers)

Exports:
├── validateAgainstSchema(data, schema)
├── validateProject(projectData)
├── validateFieldType(field, expectedType)
├── getValidationErrors(data, schema)
└── isValid(data, schema)

Used By:
├── Data-Bridge Service (primary)
├── API middleware (request validation)
├── UI form validation
└── File upload validation

Validation Types:
├── Type checking (string, number, date)
├── Required fields
├── Enum values
├── Min/max constraints
├── Pattern matching (regex)
└── Custom rules
```

---

## ⚙️ Configuration Dependencies

### **Role Hierarchy Dependencies**

```
Parent-Child Relationships:

C-Level Executive (Level 1)
    └─ Can override or delegate to:
        └─ Vice President (Level 2)
            └─ Can manage:
                └─ Senior Director (Level 3)
                    └─ Can manage:
                        └─ Director (Level 4)
                            └─ Can manage:
                                └─ Senior Manager (Level 5)
                                    └─ Can manage:
                                        └─ Manager (Level 6)
                                            └─ Can manage:
                                                ├─ Specialist (Level 7)
                                                └─ Team Member (Level 8)

Permission Inheritance:
├─ Higher levels inherit permissions from lower (on demand)
├─ Restricted permissions must be explicitly granted
└─ Department customizations allowed within constraints
```

### **Permission Dependency Map**

```
enterprise.view.all (C-Level Executive)
    ├─ Requires: Level 1 role
    ├─ Enables: business_unit.view.all
    ├─ Enables: dashboard.executive.access
    └─ Blocks: Cannot be removed from C-Level

department.view.multiple (Senior Director)
    ├─ Requires: Level 3 role
    ├─ Enables: Multiple department dashboards
    ├─ Enables: dashboard.management.access
    └─ Can delegate to: Directors in same department

resource.allocation.enterprise (C-Level Executive)
    ├─ Requires: Level 1 role
    ├─ Enables: Budget override authority
    └─ Cannot be inherited: Must be explicitly assigned
```

---

## 🔗 External Integrations

### **Active Directory Integration**

```
┌────────────────────────────────────────┐
│ Walmart Enterprise AD                   │
│ (External System)                       │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ AD Sync Service                         │
│ (Runs periodically)                     │
└────────────────────────────────────────┘
                    ↓
        ┌───────────────────┐
        │ Sync Operations   │
        ├───────────────────┤
        ├─ User profiles    │
        ├─ Group membership │
        ├─ Manager hierarchy
        ├─ Department info  │
        └─ Deactivations    │
                    ↓
┌────────────────────────────────────────┐
│ PostgreSQL (Local Cache)                │
├────────────────────────────────────────┤
│ users | groups | group_members|managers│
└────────────────────────────────────────┘
                    ↓
        Role Manager & Access Control
```

**Sync Frequency**: Daily (configurable)  
**Failure Handling**: Retry with fallback to last-known state  
**Impact**: Role assignments, access control decisions

### **Sparky AI Integration**

```
┌────────────────────────────────────────┐
│ Walmart Sparky AI Platform              │
│ (External Service)                      │
└────────────────────────────────────────┘
                    ↑
        ┌───────────────────────┐
        │ API Calls             │
        ├───────────────────────┤
        ├─ NLP processing       │
        ├─ Intent detection     │
        ├─ Entity extraction    │
        └─ Response generation  │
                    ↑
┌────────────────────────────────────────┐
│ Sparky AI Service                       │
│ (Backup: OpenAI)                        │
│ Local fallback available                │
└────────────────────────────────────────┘
                    ↑
    Chatbot ← Landing Page, All Pages
    Query
```

**Primary**: Sparky API (Walmart)  
**Secondary**: OpenAI GPT (cloud backup)  
**Tertiary**: Local NLP models (fallback)  
**Rate Limiting**: Per-user rate limits applied  

### **Notification Service Integration**

```
┌────────────────────────────────────────┐
│ Event Stream (Internal)                 │
│ ├─ User actions                         │
│ ├─ System events                        │
│ ├─ Project status changes               │
│ └─ Task updates                         │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ Notification Service                    │
│ ├─ Process events                       │
│ ├─ Apply filters                        │
│ ├─ Apply user preferences               │
│ └─ Queue messages                       │
└────────────────────────────────────────┘
                    ↓
        ┌───────────────┬───────────────┬───────────────┐
        │               │               │               │
        ↓               ↓               ↓               ↓
    In-App         Email         SMS (opt-in)      Webhook
    Real-time      Queue         Gateway            External
    WebSocket      Service       (Twilio)           Systems
```

---

## 🔀 Dependency Matrix

### **Component × Dependency Cross-Reference**

| Component | Depends On | Used By | Impact Level |
|-----------|-----------|---------|--------------|
| **Role Manager** | role-configuration.json, AD | Access Control, UI | CRITICAL |
| **Access Control** | Role Manager, access-groups.json, AD | All APIs, UI pages | CRITICAL |
| **Permission Engine** | role-configuration.json | All endpoints | CRITICAL |
| **Data-Bridge** | Schemas, Mappings, Files | Projects, Reports | HIGH |
| **Validators** | Schemas | Data-Bridge, APIs | HIGH |
| **Transformations** | Mappings, Validators | Data-Bridge | HIGH |
| **Design System** | (foundational) | All UI pages | HIGH |
| **Sparky AI** | Backend APIs, DBs, Sparky Service | Landing Page, Help | MEDIUM |
| **Notifications** | Event Stream, PostgreSQL | All pages | MEDIUM |
| **Landing Page** | Design System, Role Manager, Notification | Users | CRITICAL |
| **Admin Dashboard** | Role Manager, Access Control, Configs | Admins | HIGH |
| **Projects Interface** | Data-Bridge, Schemas, Design System | Project teams | HIGH |
| **PostgreSQL** | (foundational) | All services | CRITICAL |
| **Redis** | PostgreSQL (for cache source) | Session/Auth, Role Cache | HIGH |
| **Elasticsearch** | PostgreSQL (source) | Search, Analytics | MEDIUM |

---

## 🔄 Circular Dependencies (None Detected)

This architecture avoids circular dependencies through proper layering:
- Configuration files (foundational, no dependencies)
- Services layer (depends on config only)
- UI layer (depends on services and config)
- Infrastructure layer (provides services)

**Pattern Used**: Dependency Inversion Principle
- High-level modules don't depend on low-level modules
- Both depend on abstractions (configuration files, interfaces)

---

## 🚀 Deployment Dependencies

### **Order of Service Startup**

```
1. Infrastructure
   ├─ PostgreSQL (database)
   ├─ Redis (cache)
   └─ Elasticsearch (search)

2. Configuration Layer
   ├─ Load role-configuration.json
   ├─ Load access-groups.json
   ├─ Load dynamic-links.json
   ├─ Load data schemas
   └─ Load data mappings

3. Core Services
   ├─ Role Manager Service
   ├─ Access Control Service
   ├─ (depends on config from step 2)
   └─ Permission Engine

4. Business Logic
   ├─ Data-Bridge Service
   ├─ Sparky AI Service
   ├─ Notification Service
   └─ API Gateway

5. UI Layer
   ├─ Frontend (HTML/CSS/JS)
   ├─ (depends on APIs from step 4)
   └─ (depends on design system)

Total startup time: ~2-3 minutes for full system
```

### **Configuration Hot-Reload Capability**

```
role-configuration.json [UPDATED]
        ↓ (File watch detected)
        ↓ (Validate JSON)
        ↓ (If valid)
    Role Manager
        ↓ (Re-load from file)
    Redis Cache
        ↓ (Invalidate role cache)
Active Sessions
        ↓ (Next request: apply new permissions)

Zero downtime - sessions continue, permissions updated on next check
```

---

## 📈 Scalability Considerations

### **Scaling Pattern**

```
Single User
        ↓ (Load increases)
        ↓
Session Cache (Redis)
        ↓ (Horizontal scale: multiple Redis instances)
        ↓
Role Cache Distribution
        ↓ (Broadcast config changes to all instances)
        ↓
Database Connection Pool
        ↓ (Horizontal scale: read replicas)
        ↓
API Service Instances
        ↓ (Load balancer: distribute requests)
        ↓
10,000+ Concurrent Users (Expected capacity)
```

**Bottleneck Analysis:**
- Role lookups: Cache (< 1ms)
- Permission checks: Cache + Redis (< 10ms)
- Data queries: Read replicas (< 100ms)
- External APIs: Async processing (varies)

---

## 🔒 Security Dependencies

### **Authentication & Authorization Chain**

```
HTTPS Connection
    ↓ [encrypted]
SSO / AD Login
    ↓ [verified]
Session Token
    ↓ [stored in Redis with TTL]
Role Lookup
    ↓ [from cache]
Permission Check
    ↓ [required for each API call]
Resource Access
    ↓ [granted or denied]
Audit Log
    ↓ [recorded in PostgreSQL]
```

### **Data Protection Dependencies**

```
Encryption at Rest:
├─ PostgreSQL: AES-256
├─ File Storage: Cloud provider encryption
└─ Backups: Encrypted before transfer

Encryption in Transit:
├─ HTTPS/TLS (all connections)
├─ JWT tokens (signed and encrypted)
└─ Database connections: SSL/TLS

Access Control:
├─ Role-based access control
├─ Field-level security (HIPAA if needed)
└─ Audit logging (all data access)
```

---

## 🎯 Critical Path Analysis

**Most Critical Dependencies** (system fails without these):

1. **PostgreSQL Database** - 99.99% uptime required
   - Contains all operational data
   - User permissions, projects, tasks
   - Recovery time: < 15 minutes

2. **Active Directory** - 99.9% uptime
   - User authentication
   - Group membership
   - Fallback: Use last-known AD state

3. **Role Configuration (role-configuration.json)** - Must be valid
   - Defines all permissions
   - Loaded on startup
   - Validation required before deployment

4. **Access Control Service** - Blocks unauthorized access
   - Prevents privilege escalation
   - Critical for data security
   - Single point of enforcement

---

**Document Version**: 1.0  
**Status**: Active Reference  
**Last Updated**: February 17, 2026  
**Maintained By**: Knowledge Hub Team
