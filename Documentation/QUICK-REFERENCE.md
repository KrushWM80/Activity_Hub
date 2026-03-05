# 📊 Activity Hub - Architecture & Dependencies Quick Reference

**Purpose**: Visual quick reference for system components, relationships, and navigation  
**Last Updated**: February 17, 2026

---

## 🗺️ System at a Glance

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ACTIVITY HUB SYSTEM ARCHITECTURE                     │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │                    PRESENTATION TIER                            │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │   │
│  │  │ Landing  │ │  Admin   │ │ Projects │ │ Reports  │ ...     │   │
│  │  │  Page    │ │Dashboard │ │Management │ │         │          │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                  ↑                                      │
│                    (Design System, Authentication)                      │
│                                  ↓                                      │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │                  APPLICATION TIER (Services)                   │   │
│  │  ┌──────────┐ ┌─────────────┐ ┌──────────────┐                │   │
│  │  │   Role   │ │   Access    │ │ Permission   │                │   │
│  │  │ Manager  │ │ Control     │ │ Engine       │                │   │
│  │  └──────────┘ └─────────────┘ └──────────────┘                │   │
│  │     ↑              ↑                  ↑                         │   │
│  │     │  (Configuration)               │                         │   │
│  │  ┌──────────┐ ┌─────────────┐ ┌──────────────┐                │   │
│  │  │ Data-    │ │  Sparky AI  │ │Notifications │                │   │
│  │  │ Bridge   │ │ Assistant   │ │ System       │                │   │
│  │  └──────────┘ └─────────────┘ └──────────────┘                │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                  ↑                                      │
│        (PostgreSQL, Redis, Elasticsearch, Cloud Storage, AD)            │
│                                  ↓                                      │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │                     DATA TIER (Databases)                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────┐     │   │
│  │  │PostgreSQL│ │  Redis   │ │Elasticsearch │ │  Cloud   │     │   │
│  │  │Database  │ │  Cache   │ │   Search     │ │ Storage  │     │   │
│  │  └──────────┘ └──────────┘ └──────────────┘ └──────────┘     │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                  ↑                                      │
│   (Active Directory, Sparky API, OpenAI, Cloud Provider)                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Folder Structure with Dependencies

```
Activity-Hub/
│
├─ Interface/                          ← User-Facing Components
│  ├─ Admin/
│  │  ├─ admin-dashboard.html         [Uses: Roles, Groups, Links config]
│  │  ├─ role-configuration.json ────┐ [Master config - foundation]
│  │  ├─ access-groups.json ─────────┤ [AD mapping - foundational]
│  │  ├─ dynamic-links.json ─────────┤ [Navigation config]
│  │  ├─ Data-Bridge/               │ [Data transformation]
│  │  │  ├─ Schemas/                 [Project data structure]
│  │  │  ├─ Mappings/                [External data mapping]
│  │  │  ├─ Connections/              [Data sources]
│  │  │  └─ Uploads/                  [File intake]
│  │  └─ README.md                 ◄──┤ [Guides]
│  │
│  ├─ For You - Landing Page/
│  │  ├─ index.html                   [Uses: Design, Roles, Notifications]
│  │  ├─ activity-hub-demo.html
│  │  └─ README.md
│  │
│  ├─ Projects/
│  │  ├─ index.html
│  │  ├─ styles.css                   [Uses: Design System variables]
│  │  ├─ script.js                    [Uses: Backend API, Data-Bridge]
│  │  └─ Upload Projects/ ────────────┐ [Depends on Data-Bridge]
│  │                                  │
│  └─ [Other sections: My Work, Notifications, Settings, Teams]
│                                     │
├─ Platform/                          │
│  │                                   │
│  ├─ Design/                          ← Shared Design Assets
│  │  ├─ DESIGN_SYSTEM.md ◄───────────┤ [Master design reference]
│  │  ├─ walmart-brand-variables.css ─┤ [CSS design tokens]
│  │  ├─ COMPLETE_BRAND_SPECS.md ────┤ [Brand guidelines]
│  │  ├─ WIDGET_SPECIFICATIONS.md ────┤ [Component specs]
│  │  └─ color-tester.html
│  │
│  ├─ Data-Bridge/
│  │  ├─ transformations.js           [Uses: Schemas, Mappings]
│  │  ├─ validators.js                [Uses: Schemas]
│  │  ├─ transformations/ ────────────┐ [Transformation logic]
│  │  ├─ Schemas/                     │
│  │  ├─ Mappings/                    │
│  │  └─ README.md                 ◄──┤
│  │
│  ├─ Sparky AI/
│  │  ├─ BACKEND_API.md ◄─────────────┐ [API specification]
│  │  ├─ INTEGRATION_GUIDE.md ────────┤ [Integration guide]
│  │  ├─ ai-assistant-demo.html ─────┤ [Demo interface]
│  │  └─ README.md
│  │
│  └─ Documents/
│  │  ├─ Architecture/                [System design docs]
│  │  ├─ Backend/                     [API & services docs]
│  │  ├─ Compliance/                  [Security & governance]
│  │  └─ Strategy/                    [Business planning]
│  │
│
├─ KNOWLEDGE_HUB.md ◄────────────────┐ [Main reference document]
├─ DEPENDENCIES-MAP.md ────────────────┤ [Detailed dependencies]
├─ README.md ─────────────────────────┤ [Project overview]
├─ DATA-CLASSIFICATION-ASSESSMENT.md ─┤ [Data handling policy]
└─ GIT_REPOSITORY_SETUP.md ───────────┘ [Version control]
```

---

## 🔄 Core Dependencies Simplified

### **Configuration Dependencies**
```
role-configuration.json ──────────┐
                                  ├─→ Role Manager Service
access-groups.json ───────────────┤
                                  └─→ Access Control Service
dynamic-links.json ───────────────→ Navigation/Link Service

                All of above ─────→ Permission Checks (all endpoints)
```

### **Data Processing Dependencies**
```
Data File (Upload)
        ↓
Validator (uses: Schemas)
        ↓ (valid)
Transformer (uses: Mappings)
        ↓
PostgreSQL (storage)
        ↓
Elasticsearch (indexing)
```

### **UI Rendering Dependencies**
```
Design System (colors, fonts, spacing)
        ↓
Component Library
        ↓
Page Templates
        ↓
Role Manager (personalization)
        ↓
Rendered HTML (user sees)
```

---

## 📍 Key Configuration Files Quick Lookup

| File | Location | Purpose | Edited By | Impact |
|------|----------|---------|-----------|--------|
| **role-configuration.json** | Interface/Admin/ | Define role tiers 1-8 | Admins | User permissions |
| **access-groups.json** | Interface/Admin/ | Map AD groups to roles | Admins | Access control |
| **dynamic-links.json** | Interface/Admin/ | Configure navigation links | Admins | User navigation |
| **projects-schema.json** | Interface/Admin/Data-Bridge/Schemas/ | Define project data structure | Developers | Data validation |
| **intake-hub-mapping.json** | Interface/Admin/Data-Bridge/Mappings/ | Map external project data | Developers | Data transformation |
| **DESIGN_SYSTEM.md** | Platform/Design/ | Brand colors, typography | UX/Design | Visual consistency |
| **walmart-brand-variables.css** | Platform/Design/ | CSS design tokens | Developers | UI styling |

---

## 🔗 Dependency Chains (Critical Paths)

### **Path 1: User Authentication → Authorization → Page Access**
```
1. User Login
   ↓ [AD authentication]
2. Session Created (Redis)
   ↓
3. Role Lookup (role-configuration.json)
   ↓
4. Permission Matrix Built (access-groups.json)
   ↓
5. Landing Page Rendered (personalized by role)
   ↓
6. User sees appropriate content based on permissions
```

### **Path 2: Admin Configuration Change → System-Wide Effect**
```
1. Admin modifies role-configuration.json
   ↓ [via Admin Dashboard]
2. File validated
   ↓
3. Role Manager Service reloaded
   ↓
4. Redis cache invalidated
   ↓
5. Active users get updated permissions on next action
   ↓ (Zero downtime deployment pattern)
6. All UI pages show updated features/options
```

### **Path 3: File Upload → Data Processing → Display**
```
1. User uploads project file
   ↓
2. Access Control validates permission
   ↓
3. File stored in Cloud Storage
   ↓
4. Data-Bridge Validator (uses: schema)
   ↓ [validates structure]
5. Data-Bridge Transformer (uses: mapping)
   ↓ [converts to internal format]
6. PostgreSQL insertion
   ↓
7. Elasticsearch indexing
   ↓
8. Projects page displays new project
   ↓ [searchable, filtered by user role]
9. Notifications sent to stakeholders
```

---

## 📊 Component Relationship Matrix

```
                    Role Mgr  Access Ctrl  Data-Bridge  Design  Sparky  DB
Landing Page          ✓          ✓            ✓         ✓       ✓      ✓
Admin Dashboard       ✓          ✓            ✓         ✓       -      ✓
Projects Page        ✓          ✓            ✓         ✓       ✓      ✓
Reports              ✓          ✓            ✓         ✓       ✓      ✓
Settings Page        ✓          ✓            -         ✓       -      ✓

Role Manager         -          -            -         -       -      ✓
Access Control       ✓          -            -         -       -      -
Data-Bridge          -          ✓            -         -       -      ✓
Permissions          ✓          ✓            -         -       -      -
Sparky AI            ✓          ✓            -         -       -      ✓

Legend: ✓ = Depends on  |  - = Independent
```

---

## 🎯 Information Lookup Guide

**"I need to know about..."** → **Go to:**

```
├─ User Roles & Permissions
│  └─→ Interface/Admin/ROLE_MANAGEMENT.md
│      (Then: role-configuration.json, access-groups.json)
│
├─ Design & Branding
│  └─→ Platform/Design/DESIGN_SYSTEM.md
│      (Then: walmart-brand-variables.css, WIDGET_SPECIFICATIONS.md)
│
├─ Access Control & Security
│  └─→ Interface/Admin/ACCESS_CONTROL.md
│      (Then: Platform/Documents/Compliance/)
│
├─ System Architecture
│  └─→ DEPENDENCIES-MAP.md (this document)
│      (Then: Platform/Documents/Architecture/)
│
├─ Data Integration
│  └─→ Platform/Data-Bridge/README.md
│      (Then: transformations.js, validators.js, Schemas/, Mappings/)
│
├─ API Documentation
│  └─→ Platform/Sparky AI/BACKEND_API.md
│      (Then: INTEGRATION_GUIDE.md)
│
├─ Project Management
│  └─→ Interface/Projects/README.md
│      (Then: index.html, styles.css, script.js)
│
├─ Administrative Tasks
│  └─→ Interface/Admin/README.md
│      (Then: admin-dashboard.html, LINK_MANAGEMENT.md)
│
└─ Compliance & Governance
   └─→ Platform/Documents/Compliance/
       (Then: DATA-CLASSIFICATION-ASSESSMENT.md)
```

---

## ⚡ Dependency Impact Analysis

**If this fails... these are affected:**

| Component | Failure Impact | Recovery Time | Workaround |
|-----------|---|---|---|
| **PostgreSQL** | Complete system outage | 15-30 min | Failover to replica |
| **Redis** | Slow auth (no cache) | < 1 min | Continue with DB queries |
| **Elasticsearch** | No search, analytics down | < 5 min | Fallback search |
| **AD/SSO** | Users can't log in | ~30 min | Use fallback auth |
| **Sparky AI** | Assistant offline | ~15 min | Use local NLP models |
| **Config files** | Invalid config crash | Immediate | Revert to known-good version |
| **Design System** | Unstyled pages | < 1 min | Fallback CSS |
| **File Storage** | Uploads fail | ~10 min | Switch to backup storage |

---

## 🚀 Service Startup Sequence

```
Minute 0:00 - Infrastructure Layer
│   ├─ PostgreSQL (3-5 min)
│   ├─ Redis (1-2 min)
│   └─ Elasticsearch (2-3 min)
│
Minute 0:05 - Configuration Layer
│   ├─ Load role-configuration.json
│   ├─ Load access-groups.json
│   ├─ Load dynamic-links.json
│   ├─ Load schemas
│   └─ Load mappings
│
Minute 0:10 - Core Services
│   ├─ Role Manager
│   ├─ Access Control
│   ├─ Permission Engine
│   ├─ Data-Bridge
│   ├─ Sparky AI
│   └─ Notification System
│
Minute 0:15 - Frontend APIs
│   ├─ API Gateway
│   ├─ Load balancer
│   └─ API instances
│
Minute 0:20 - Frontend
│   ├─ Landing page (ready)
│   ├─ Admin dashboard (ready)
│   ├─ Projects (ready)
│   └─ Other pages (ready)
│
✓ System Ready! (Total: ~2-3 minutes)
```

---

## 🔐 Security Dependency Chain

```
HTTPS Connection (encrypted)
    ↓
Login (AD verification)
    ↓
Session Token (Redis stored, with TTL)
    ↓
Role Lookup (from role-configuration.json)
    ↓
Permission Check (every request)
    ↓
Resource Access (granted or denied)
    ↓
Audit Log (PostgreSQL, records all access)
    ↓
Data Encryption (at rest + in transit)
```

---

## 📈 Scalability Per Component

| Component | Single Instance? | Scaling Strategy | Bottleneck Prevention |
|-----------|---|---|---|
| **Role Manager** | Yes | In-memory cache | Redis distributes cache |
| **Access Control** | Yes (for logic) | Stateless (replicate service) | Cache permission checks |
| **Data-Bridge** | Maybe | Queue-based processing | Async jobs, RabbitMQ |
| **Sparky AI** | No | Multiple API instances | Load balancer distributes |
| **PostgreSQL** | No | Read replicas | Connection pooling |
| **Redis** | Maybe | Cluster mode | Replication, failover |
| **Elasticsearch** | No | Sharded indices | Bulk indexing, snapshots |
| **API Gateway** | No | Multiple instances | Load balancer |

---

## 📚 Documentation Cross-References

```
KNOWLEDGE_HUB.md (main index)
├─ → README.md (project overview)
├─ → DEPENDENCIES-MAP.md (this doc + more detail)
├─ → Design System files
│   ├─ Platform/Design/DESIGN_SYSTEM.md
│   └─ Platform/Design/COMPLETE_BRAND_SPECS.md
├─ → Configuration files
│   ├─ Interface/Admin/ROLE_MANAGEMENT.md
│   ├─ Interface/Admin/ACCESS_CONTROL.md
│   └─ Interface/Admin/LINK_MANAGEMENT.md
├─ → Backend & API
│   ├─ Platform/Sparky AI/BACKEND_API.md
│   ├─ Platform/Data-Bridge/README.md
│   └─ Platform/Documents/Backend/
├─ → Architecture & Planning
│   ├─ Platform/Documents/Architecture/
│   └─ Platform/Documents/Strategy/
└─ → Compliance & Security
    ├─ Platform/Documents/Compliance/
    ├─ DATA-CLASSIFICATION-ASSESSMENT.md
    └─ COMPLIANCE_COMPLETION_REPORT.md
```

---

## 🎓 Learning Path by Role

### **For New Developers**
1. Read: [README.md](README.md) (5 min)
2. Review: [KNOWLEDGE_HUB.md](KNOWLEDGE_HUB.md#-architecture-overview) (15 min)
3. Study: [DEPENDENCIES-MAP.md](DEPENDENCIES-MAP.md) (30 min)
4. Deep dive: [Platform/Sparky%20AI/BACKEND_API.md](Platform/Sparky%20AI/BACKEND_API.md) (60 min)

### **For Administrators**
1. Read: [Interface/Admin/README.md](Interface/Admin/README.md) (10 min)
2. Review: [ROLE_MANAGEMENT.md](Interface/Admin/ROLE_MANAGEMENT.md) (20 min)
3. Study: [role-configuration.json](Interface/Admin/role-configuration.json) (15 min)
4. Learn: [ACCESS_CONTROL.md](Interface/Admin/ACCESS_CONTROL.md) (20 min)

### **For Project Managers**
1. Read: [README.md](README.md) (5 min)
2. Review: [KNOWLEDGE_HUB.md](KNOWLEDGE_HUB.md) (20 min)
3. Check: [Compliance Documentation](Platform/Documents/Compliance/) (30 min)
4. Monitor: [Backend Development Progress](Platform/Documents/Backend/) (ongoing)

### **For UX/Designers**
1. Study: [DESIGN_SYSTEM.md](Platform/Design/DESIGN_SYSTEM.md) (30 min)
2. Reference: [COMPLETE_BRAND_SPECS.md](Platform/Design/COMPLETE_BRAND_SPECS.md) (20 min)
3. Review: [WIDGET_SPECIFICATIONS.md](Platform/Design/WIDGET_SPECIFICATIONS.md) (20 min)
4. Test: [color-tester.html](Platform/Design/color-tester.html) (hands-on)

---

## 🔍 Quick Troubleshooting

```
Problem: User can't see expected UI elements
├─ Check: role-configuration.json (user has required role?)
├─ Check: access-groups.json (user's AD group mapped?)
└─ Check: WCAG accessibility (contrast, labels)

Problem: Data not appearing in reports
├─ Check: data schema validation (projects-schema.json)
├─ Check: data mapping (intake-hub-mapping.json)
├─ Check: Data-Bridge logs (transformation errors?)
└─ Check: PostgreSQL (data inserted correctly?)

Problem: Styling inconsistent across pages
├─ Check: Design System implementation
├─ Check: walmart-brand-variables.css imported
└─ Check: Component CSS follows DESIGN_SYSTEM.md

Problem: Admin dashboard not loading
├─ Check: Role permission for admin access
├─ Check: Access Control Service running
└─ Check: Configuration files valid (JSON syntax)

Problem: Search results incomplete
├─ Check: Elasticsearch indexing (all docs indexed?)
├─ Check: User permissions (can access search results?)
└─ Check: Database (data present and synced?)
```

---

**Version**: 1.0  
**Type**: Quick Reference & Visual Guide  
**Last Updated**: February 17, 2026  
**Purpose**: Help users navigate the Knowledge Hub and understand system dependencies at a glance
