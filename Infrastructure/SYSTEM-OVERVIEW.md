# 📊 Activity Hub - System Overview & Visual Guide

**Purpose**: High-level visual summary of the entire system architecture and key concepts  
**Last Updated**: February 17, 2026  
**Best For**: Quick understanding, presentations, onboarding

---

##  🎯 System at a Glance

```
╔════════════════════════════════════════════════════════════════════╗
║              WALMART ENTERPRISE ACTIVITY HUB                       ║
║                   50,000+ Employee Platform                        ║
╚════════════════════════════════════════════════════════════════════╝

Business Objective: Increase productivity, collaboration, and 
decision-making speed across enterprise

Target Users:    C-Level Execs → VPs → Directors → Managers → Teams
Expected ROI:    694% first-year return on $3.4M investment
Time Savings:    4-6 hours per user per week
User Base:       50,000+ Walmart Enterprise employees
```

---

## 👥 User Tiers (Role Hierarchy)

```
┌──────────────────────────────────────────────────────────────┐
│                    Role Hierarchy                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Level 1: C-Level Executive           ← 12 users           │
│  ├─ CEO, CFO, CTO                                           │
│  ├─ Permission: enterprise.view.all                         │
│  └─ Access: All data, reports, strategic decisions          │
│                                                              │
│  Level 2: Vice President              ← 28 users           │
│  ├─ BU VPs, Function VPs                                    │
│  ├─ Permission: business_unit.view.all                      │
│  └─ Access: Business unit data, reports                     │
│                                                              │
│  Level 3: Senior Director             ← 67 users           │
│  ├─ Department heads, Senior leads                          │
│  ├─ Permission: department.view.multiple                    │
│  └─ Access: Multiple departments, teams                     │
│                                                              │
│  Level 4: Director                    ← 156 users          │
│  ├─ Department managers                                     │
│  ├─ Permission: department.view.all                         │
│  └─ Access: Own department, teams                           │
│                                                              │
│  Level 5: Senior Manager               ← ??? users         │
│  Level 6: Manager                      ← ??? users         │
│  Level 7: Specialist                   ← ??? users         │
│  Level 8: Team Member                  ← ??? users         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎨 Core Components

### **1. User Interface Layer (What Users See)**

```
┌─────────────────────────────────────────────────────────┐
│                LANDING PAGE (Main Entry)                │
│  ┌────────────────────────────────────────────────┐    │
│  │ • Personalized dashboard (role-based)          │    │
│  │ • Quick links & navigation                     │    │
│  │ • Recent activities & notifications            │    │
│  │ • AI assistant widget (Sparky)                 │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
         ↓           ↓            ↓           ↓
    ┌─────────┬─────────────┬──────────┬─────────────┐
    │         │             │          │             │
    ↓         ↓             ↓          ↓             ↓
┌─────────┐ ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌────────┐
│ ADMIN   │ │ MY WORK │ │ PROJECTS │ │ REPORTS │ │SETTINGS│
│DASHBOARD│ │         │ │          │ │         │ │        │
└─────────┘ └─────────┘ └──────────┘ └─────────┘ └────────┘

 ↑ Admins  Staff    Teams    Analysis   Preferences
```

### **2. Application Services (Backend Logic)**

```
┌────────────────────────────────────────────────────────┐
│              APPLICATION SERVICES LAYER                │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────────────────┐                         │
│  │  Role & Access Services  │                         │
│  │  ├─ Role Manager         │ ← Read role config    │
│  │  ├─ Access Control       │                         │
│  │  └─ Permission Engine    │ ← Check every request  │
│  └──────────────────────────┘                         │
│                                                        │
│  ┌──────────────────────────┐                         │
│  │  Data Services           │                         │
│  │  ├─ Data-Bridge          │ ← Transform data      │
│  │  ├─ Validators           │ ← Check schemas       │
│  │  └─ Transformers         │ ← Map fields           │
│  └──────────────────────────┘                         │
│                                                        │
│  ┌──────────────────────────┐                         │
│  │  Intelligence Layer      │                         │
│  │  ├─ Sparky AI            │ ← Answer questions    │
│  │  ├─ Recommendation Engine │                        │
│  │  └─ Analytics            │                         │
│  └──────────────────────────┘                         │
│                                                        │
│  ┌──────────────────────────┐                         │
│  │  Notification System     │                         │
│  │  ├─ Event Processing     │                         │
│  │  ├─ Delivery Pipeline    │                         │
│  │  └─ User Preferences     │                         │
│  └──────────────────────────┘                         │
│                                                        │
└────────────────────────────────────────────────────────┘
         ↑                                ↑
         └────────────────────────────────┘
              (Uses Config Files)
```

### **3. Configuration Layer (System Settings)**

```
┌────────────────────────────────────────────────────────┐
│           CONFIGURATION & RULES (JSON Files)           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  role-configuration.json                             │
│  ├─ All 8 user roles defined                         │
│  ├─ Permissions for each role                        │
│  └─ Role hierarchy & inheritance                     │
│     Loaded by: Role Manager Service                  │
│                                                        │
│  access-groups.json                                  │
│  ├─ AD group to role mapping                         │
│  ├─ Automated provisioning rules                     │
│  └─ Group hierarchies                                │
│     Loaded by: Access Control Service                │
│                                                        │
│  dynamic-links.json                                  │
│  ├─ Navigation links & buttons                       │
│  ├─ Role-based visibility                           │
│  └─ External resource URLs                           │
│     Loaded by: Navigation System                     │
│                                                        │
│  Data Schemas (projects-schema.json, etc.)           │
│  ├─ Data structure definitions                       │
│  ├─ Field types & constraints                        │
│  └─ Validation rules                                 │
│     Loaded by: Validators                            │
│                                                        │
│  Data Mappings (intake-hub-mapping.json, etc.)       │
│  ├─ External → Internal field mapping                │
│  ├─ Transformation rules                             │
│  └─ Data enrichment steps                            │
│     Loaded by: Transformers                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### **4. Database Layer (Data Storage)**

```
┌──────────────────────────────────────────────────┐
│         PERSISTENCE & DATA LAYER                  │
├──────────────────────────────────────────────────┤
│                                                  │
│  PostgreSQL (Primary Database)                  │
│  ├─ users table                                 │
│  ├─ projects table                              │
│  ├─ tasks table                                 │
│  ├─ roles table                                 │
│  ├─ permissions table                           │
│  ├─ notifications table                         │
│  └─ audit_logs table                            │
│  Access: All read/write operations              │
│                                                  │
│  Redis (Cache & Sessions)                       │
│  ├─ User sessions (with TTL)                    │
│  ├─ Role cache (hot data)                       │
│  ├─ Permission cache                            │
│  └─ Temporary data                              │
│  Access: Fast lookup, expires automatically     │
│                                                  │
│  Elasticsearch (Search Index)                   │
│  ├─ projects_index (searchable)                 │
│  ├─ tasks_index                                 │
│  ├─ knowledge_index (docs, help)                │
│  └─ audit_index                                 │
│  Access: Full-text search                       │
│                                                  │
│  Cloud File Storage (AWS S3 / Azure Blob)       │
│  ├─ User uploads                                │
│  ├─ Project imports                             │
│  ├─ Report exports                              │
│  └─ System backups                              │
│  Access: File operations                        │
│                                                  │
│  Active Directory (External)                    │
│  ├─ User authentication                         │
│  ├─ Group membership                            │
│  └─ User profiles                               │
│  Access: Sync daily, use locally cached         │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 🔄 Key Data Flows

### **Flow 1: User Login → Access Dashboard**

```
USER BROWSER
    │
    │ [Login Request]
    ↓
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
Authentication Service
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    │
    │ [Verify AD Credentials]
    ↓
Active Directory
    │
    │ [User ID + Groups]
    ↓
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
Role Manager Service
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    │ [Reads: role-configuration.json]
    │ [Reads: access-groups.json]
    ↓ [Determines: Role tier 1-8]
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
Session Service
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    │ [Store session in Redis with TTL]
    ↓ [Generate auth token]
USER SEES: Landing Page (personalized by role)
```

### **Flow 2: Project Upload → Processing → Display**

```
USER BROWSER (Upload Page)
    │
    │ [Select file + submit]
    ↓
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
API: POST /api/projects/upload
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    │
    │ [Check user permissions]
    ↓
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
Access Control Service
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    │ [Can user upload projects?]
    ↓ [Yes → Continue]
Cloud File Storage
    │ [Store uploaded file]
    ↓
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
Data-Bridge Service
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    │
    ├─ Validator [uses: projects-schema.json]
    │  └─ Extract & validate fields
    │
    ├─ Transformer [uses: intake-hub-mapping.json]
    │  └─ Map external fields to internal format
    │
    └─ Enricher
       └─ Add metadata, timestamps
    ↓
PostgreSQL
    │ [INSERT project record]
    ↓
Elasticsearch
    │ [INDEX: projects_index]
    ↓
USER BROWSER
    └─ "Project uploaded successfully!"
    └─ [Projects page shows new project]
```

### **Flow 3: Admin Changes Role Permissions**

```
ADMIN BROWSER
    │
    │ [Admin Dashboard: Modify role-configuration.json]
    │ [Example: Add "reports.export" permission to Manager]
    ↓
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
File System / Backend Storage
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    │
    │ [Persistence layer saves changes]
    ↓
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
Config Validation Service
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    │ [Validate JSON structure]
    │ [Check permission names]
    │ [Verify no conflicts]
    ↓ [Valid]
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
Role Manager Service
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    │ [Re-read role-configuration.json]
    ↓
Redis Cache
    │ [Invalidate old role cache]
    │ [Load new roles]
    ↓
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
Active User Sessions
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    │ (Continue as-is)
    │ (Next request: Check new permissions)
    ↓
ALL MANAGERS
    └─ Can now export reports (automatically!)
    └─ Zero downtime deployment
```

---

## 📊 Component Relationship Matrix

```
            Admin  Landing  Projects Reports Settings
            Dash   Page     Mgmt
────────────────────────────────────────────────────
Design      ✓      ✓        ✓       ✓       ✓
System

Role        ✓      ✓        ✓       ✓       ✓
Manager

Access      ✓      ✓        ✓       ✓       ✓
Control

Data-       ✓      ○        ✓       ✓       ○
Bridge

Sparky      ○      ✓        ○       ○       ○
AI

Notifi-     ○      ✓        ○       ○       ○
cation

PostgreSQL  ✓      ✓        ✓       ✓       ✓

Redis       ✓      ○        ○       ✓       ✓

Elastic     ✓      ✓        ✓       ✓       ○

Legend: ✓ = Critical  |  ○ = Optional  |  - = Not used
```

---

## 🔑 Key Concepts

### **Permission Model**

```
┌─────────────────────────────────────────────┐
│         Permission Hierarchy                │
├─────────────────────────────────────────────┤
│                                             │
│  ROLE (e.g., "Manager")                    │
│      ↓                                      │
│  PERMISSIONS (e.g., "project.view.all")    │
│      ↓                                      │
│  RESOURCES (e.g., "Project X")             │
│      ↓                                      │
│  ACTIONS (e.g., "view", "edit", "delete")  │
│                                             │
│  Result: Allow or Deny                     │
│                                             │
└─────────────────────────────────────────────┘

Example:
  Manager has "project.view.all" permission
  → Can view all projects
  → "project.edit.own" permission
  → Can edit only their own projects
  → No "project.delete" permission
  → Cannot delete any projects
```

### **Role-Based Access Control (RBAC)**

```
User → [Active Directory] → Group Memberships
           ↓
       [access-groups.json] → Role Assignment
           ↓
       [role-configuration.json] → Permission Set
           ↓
       [Permission Engine] → Can access resource?
           ↓
       ALLOW or DENY
```

---

## 💾 Data Classification

```
┌────────────────────────────────────────┐
│        Data Security Levels             │
├────────────────────────────────────────┤
│                                        │
│  PUBLIC                                │
│  ├─ Help documentation                 │
│  ├─ Product announcements             │
│  └─ General company info               │
│                                        │
│  INTERNAL                              │
│  ├─ Project data                       │
│  ├─ Team information                   │
│  ├─ Non-sensitive reports              │
│  └─ Operational metrics                │
│                                        │
│  CONFIDENTIAL                          │
│  ├─ Financial data                     │
│  ├─ Strategic plans                    │
│  ├─ Employee performance data          │
│  └─ Contract information               │
│                                        │
│  RESTRICTED                            │
│  ├─ Executive-only data                │
│  ├─ HR sensitive info                  │
│  ├─ Security credentials               │
│  └─ Audit information                  │
│                                        │
│  Control: Role-based access,           │
│           Encryption at rest & transit │
│                                        │
└────────────────────────────────────────┘
```

---

## 🔐 Security Architecture

```
┌────────────────────────────────────────────────────────┐
│                SECURITY LAYERS                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Layer 1: Network Security                            │
│  ├─ HTTPS / TLS Encryption                            │
│  ├─ API Gateway                                       │
│  └─ DDoS Protection                                   │
│                                                        │
│  Layer 2: Authentication                              │
│  ├─ AD / SSO Integration                              │
│  ├─ MFA (Multi-Factor Auth)                           │
│  └─ Session Management                                │
│                                                        │
│  Layer 3: Authorization                               │
│  ├─ Role-Based Access Control                         │
│  ├─ Permission Checks (every request)                 │
│  └─ Field-Level Security (where applicable)           │
│                                                        │
│  Layer 4: Data Protection                             │
│  ├─ Encryption at Rest (AES-256)                      │
│  ├─ Encryption in Transit (TLS)                       │
│  └─ Key Management                                    │
│                                                        │
│  Layer 5: Audit & Monitoring                          │
│  ├─ All Access Logged                                 │
│  ├─ Security Events Monitored                         │
│  └─ Compliance Reports Generated                      │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 📈 System Scaling

```
┌─────────────────────────────────────────────┐
│         Scalability Strategy                │
├─────────────────────────────────────────────┤
│                                             │
│  Current: Single Instance Services          │
│  ├─ Role Manager                            │
│  ├─ Access Control                          │
│  └─ Notification handler                    │
│                                             │
│  Bottleneck: Service falls → All down       │
│  Solution: Stateless (horizontally scale)   │
│                                             │
│  Current: Single Database                   │
│  ├─ PostgreSQL main instance                │
│  └─ Redis single instance                   │
│                                             │
│  Bottleneck: DB connection pool max         │
│  Solution: Read replicas, connection pool   │
│                                             │
│  Current: Single File Storage               │
│  ├─ AWS S3 bucket                           │
│  └─ Regional replication available          │
│                                             │
│  Expected Capacity: 10,000+ concurrent     │
│  Load Testing: In progress                  │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🚀 Technology Stack Summary

```
┌──────────────────────────────────┐
│      Frontend (User Facing)       │
├──────────────────────────────────┤
│ HTML5 / CSS3 / JavaScript (ES6+) │
│ React 18+ (planned migration)     │
│ TypeScript (planned)              │
│ Responsive Design                 │
│ WCAG AA/AAA Accessibility         │
└──────────────────────────────────┘
           ↓
┌──────────────────────────────────┐
│    APIs & Backend Services       │
├──────────────────────────────────┤
│ Node.js + Express (API server)    │
│ Python + FastAPI (AI/ML)          │
│ TypeScript support                │
│ Microservices architecture        │
└──────────────────────────────────┘
           ↓
┌──────────────────────────────────┐
│     Data & Infrastructure         │
├──────────────────────────────────┤
│ PostgreSQL (primary)              │
│ Redis (cache/sessions)            │
│ Elasticsearch (search)            │
│ AWS / Azure cloud                 │
│ Docker + Kubernetes               │
└──────────────────────────────────┘
           ↓
┌──────────────────────────────────┐
│    External Integrations          │
├──────────────────────────────────┤
│ Active Directory (auth)           │
│ Sparky AI (Walmart AI)            │
│ OpenAI (NLP backup)               │
│ Cloud Provider APIs               │
└──────────────────────────────────┘
```

---

## 📊 Key Metrics & Success Factors

```
╔════════════════════════════════════╗
║   BUSINESS METRICS                 ║
╠════════════════════════════════════╣
║                                    ║
║  Time Savings:        4-6 hrs/week ║
║  Productivity Gain:   15% increase  ║
║  User Satisfaction:   >4.5/5 stars  ║
║  Adoption Rate:       Target: 100%  ║
║                                    ║
║  Investment:          $3.4M        ║
║  Expected Benefits:   $27M/year     ║
║  First-Year ROI:      694%          ║
║                                    ║
╚════════════════════════════════════╝

╔════════════════════════════════════╗
║   TECHNICAL METRICS                ║
╠════════════════════════════════════╣
║                                    ║
║  API Response Time:    <100ms       ║
║  Database Query:       <50ms        ║
║  Page Load Time:       <2 seconds   ║
║  Cache Hit Rate:       >80%         ║
║  System Uptime:        99.9%        ║
║  Data Processing:      Real-time    ║
║                                    ║
╚════════════════════════════════════╝
```

---

## 🎯 Implementation Phases

```
Phase 1: Foundation (Completed)
├─ Core architecture
├─ Auth & authorization
├─ Design system
└─ Basic interfaces

Phase 2: Core Features (In Progress)
├─ Dashboard personalization
├─ Project management
├─ Reporting
└─ Data integration (Data-Bridge)

Phase 3: Intelligence (Planned)
├─ Sparky AI integration
├─ Recommendation engine
├─ Analytics & insights
└─ Advanced search

Phase 4: Scale & Optimize (Planned)
├─ Performance optimization
├─ Enterprise features
├─ Advanced security
└─ Global deployment

Total Timeline: 12 months
Current Status: Phase 2 (50% complete)
```

---

## 📋 Quick Status Check

```
┌─────────────────────────────────────────┐
│         Component Status                │
├────────────────────┬────────┬───────────┤
│ Component          │ Status │ Progress  │
├────────────────────┼────────┼───────────┤
│ Core Architecture  │   ✓    │   100%    │
│ UI Components      │   ✓    │    80%    │
│ Authentication     │   ✓    │   100%    │
│ Authorization      │   ✓    │   100%    │
│ Design System      │   ✓    │    95%    │
│ API Framework      │   ✓    │    90%    │
│ Database Layer     │   ✓    │   100%    │
│ Data-Bridge        │   ○    │    60%    │
│ Sparky AI          │   ○    │    40%    │
│ Reporting          │   ○    │    50%    │
│ Compliance         │   ✓    │    95%    │
│ Deployment Ready   │   ○    │    70%    │
└────────────────────┴────────┴───────────┘

Legend: ✓ = Ready / ○ = In Progress / ✗ = Not Started
```

---

## 🔗 Architecture Decision Records (ADRs)

```
Decision: Use PostgreSQL as primary database
├─ Reason: ACID compliance, reliability
├─ Alternative: NoSQL (rejected for transactional needs)
└─ Status: Implemented

Decision: Implement Redis for session management
├─ Reason: Performance, session expiry handling
├─ Alternative: In-memory (rejected for scalability)
└─ Status: Implemented

Decision: Role-based access control (RBAC)
├─ Reason: Enterprise standard, flexible
├─ Alternative: Attribute-based (more complex)
└─ Status: Implemented

Decision: Configuration files (JSON) as config source
├─ Reason: Easy to version, readable, deployable
├─ Alternative: Database config (less flexible)
└─ Status: Implemented

Decision: Microservices architecture
├─ Reason: Scalability, independent deployment
├─ Alternative: Monolithic (less flexible)
└─ Status: Implemented
```

---

## 📚 How to Use This Document

| If you want to... | See section... | Time |
|---|---|---|
| Quick understanding | System at a Glance | 5 min |
| User roles | User Tiers | 5 min |
| Component overview | Core Components | 10 min |
| Data flows | Key Data Flows | 10 min |
| Security approach | Security Architecture | 10 min |
| Technology used | Technology Stack | 5 min |
| Current progress | Quick Status Check | 5 min |
|Full deep dive | Read all sections | 60 min |

---

**Document Type**: Visual Summary & Overview  
**Version**: 1.0  
**Last Updated**: February 17, 2026  
**Audience**: Everyone (non-technical to technical)  
**Related Documents**: 
- [KNOWLEDGE_HUB.md](KNOWLEDGE_HUB.md) - Detailed reference
- [DEPENDENCIES-MAP.md](DEPENDENCIES-MAP.md) - Technical dependencies
- [QUICK-REFERENCE.md](QUICK-REFERENCE.md) - Quick lookup
