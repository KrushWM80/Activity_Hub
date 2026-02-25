# 📊 Activity Hub - Datasource Usage Matrix

## Overview
This document provides a complete cross-reference showing which Activity Hub folders and projects use each datasource, including data flow patterns, dependencies, and update frequencies.

---

## 🗺️ Complete Datasource-to-Folder Mapping

### BIGQUERY DATASOURCES

#### 1️⃣ Polaris - `polaris-analytics-prod.us_walmart`

**Dataset**: `us_walmart`
**Tables**: `vw_polaris_current_schedule`, `vw_polaris_associate_details`, `vw_polaris_locations`

| Folder/Project | Purpose | Usage Pattern | Update Frequency | Type |
|---|---|---|---|---|
| **Projects/JobCodes-teaming/** | Teaming module uses Polaris for scheduling lookup | Query associate schedules by store | Daily | Read-only |
| **Projects/AMP/Store Updates Dashboard/** | Asset Management Plan queries associate schedules | Pull labor data for compliance | Daily | Read-only |
| **Root/final_polaris_search.py** | Test/utility script for Polaris queries | Test data access | On-demand | Read-only |
| **Root/search_by_location.py** | Search facility data by location | Lookup store info | On-demand | Read-only |
| **Root/explore_polaris_locations.py** | Explore Polaris location hierarchy | Data discovery | On-demand | Read-only |
| **Root/query_polaris_correct_columns.py** | Query Polaris with specific columns | Column verification | On-demand | Read-only |

**Data Flow**:
```
Polaris System (External)
    ↓ (Daily sync via ETL)
BigQuery polaris-analytics-prod
    ↓ (SQL queries)
Activity Hub Project Modules
    ↓ (Display schedules, assignments)
User Dashboards
```

**Key Data Elements**:
- Associate ID, Name, Email
- Job Code, Title, Department
- Store Number, Location, Area
- Scheduled hours, Shift times

---

#### 2️⃣ Asset Protection - `wmt-assetprotection-prod.Store_Support_Dev`

**Dataset**: `Store_Support_Dev`
**Tables**: `projects_intake_data`, `projects_stores_mapping`, `dl_catalog`, `AMP_Data_Prep`, `Store_Cur_Data`

| Folder/Project | Table Used | Purpose | Type |
|---|---|---|---|
| **Projects/Intake Hub/ProjectsinStores/** | `projects_intake_data` | Intake Hub dashboard data | Read/Write |
| **Projects/Intake Hub/ProjectsinStores/** | `projects_stores_mapping` | Store assignment visualization | Read-only |
| **General Setup/Distribution_Lists/** | `dl_catalog` | Email distribution list catalog | Read-only |
| **Projects/AMP/Store Updates Dashboard/** | `AMP_Data_Prep` | AMP compliance data | Read/Write |
| **Projects/RefreshGuide/** | `Store_Cur_Data` | Store information | Read-only |
| **Interface/Admin/Admin Dashboard/** | `projects_intake_data` | Project administration | Read/Write |

**Data Flow**:
```
External Systems (Workday, HR, Manual)
    ↓ (Daily ETL)
Asset Protection Database
    ↓ (Export to BigQuery)
wmt-assetprotection-prod.Store_Support_Dev
    ↓ (API queries from Activity Hub)
Dashboard Modules
```

**Key Tables**:

**projects_intake_data**:
```
project_id, project_title, project_status, owner_email,
start_date, end_date, store_number, budget, priority,
description, region, market, area_manager
```

**dl_catalog**:
```
email, name, display_name, description,
member_count, category, department, created_date
```

---

#### 3️⃣ Store Refresh - `athena-gateway-prod.store_refresh`

**Dataset**: `store_refresh`
**Tables**: `store_refresh_data`

| Folder/Project | Purpose | Usage Pattern | Frequency |
|---|---|---|---|
| **Projects/Refresh Guide/** | Refresh touring schedule and status | Display store refresh phases | Daily |
| **General Setup/Production_Path/** | Store refresh status tracking | Monitor completion rates | Daily |

**Data Flow**:
```
Store Leadership System → athena-gateway-prod
    ↓ (Daily sync)
Refresh Guide Dashboard
    ↓ (Real-time display)
Store Support Teams
```

---

#### 4️⃣ Pricing - `wmt-pricingops-analytics.Ad_Hoc_Copp_Tables`

**Dataset**: `Ad_Hoc_Copp_Tables`
**Tables**: `mixed_base`, `vendor_pricing`

| Folder/Project | Purpose | Style |
|---|---|---|
| **Projects/Pricing/** | Pricing operations data and COOP analysis | Query & visualization |

**Python File**:
```
Store Support/Projects/Pricing/fetch_data.py
```

**Usage**:
```python
# Query example
SELECT vendor_id, item_id, cost, retail_price, coop_amount
FROM `wmt-pricingops-analytics.Ad_Hoc_Copp_Tables.mixed_base`
```

---

### API DATASOURCES

#### 1️⃣ Workday HR System

| Module | Purpose | Endpoint | Update |
|---|---|---|---|
| **Distribution_Lists/** | Job code mappings | `/jobs/{job_code}` | Daily |
| **Distribution_Lists/** | Employee lookup | `/employees/{id}` | Daily |
| **General Setup/Admin** | HR data sync | `/departments`, `/locations` | Daily |

**Files**:
```
- Distribution_Lists/02_SCRIPTS_AND_TOOLS/workday_job_lookup.py
- Distribution_Lists/02_SCRIPTS_AND_TOOLS/workday_api_integration.py
```

**Key Operations**:
- Lookup employee by ID
- Get job title by code
- Verify department mappings
- Validate location assignments

---

#### 2️⃣ Active Directory / Microsoft Graph

| Module | Purpose | Scope | Type |
|---|---|---|---|
| **Interface/Admin/** | User & group management | Authentication, authorization | Real-time |
| **Interface/Settings/** | User preferences & roles | Profile data | Real-time |
| **All Modules** | Access control | Group membership verification | Real-time |

**Key Groups**:
```
activity-hub-admins
activity-hub-managers  
activity-hub-project-leads
activity-hub-store-support
store-refresh-team
```

**API Endpoints**:
```
/me - Current user
/me/memberOf - User's groups
/groups/{id}/members - Group members
```

---

#### 3️⃣ Microsoft 365 Integration (MS Graph)

| Service | Purpose | Modules | Type |
|---|---|---|---|
| **Teams** | Notifications, messaging | Notifications, Projects | Real-time |
| **Outlook Calendar** | Calendar events | Calendar, Events | Real-time |
| **SharePoint** | Document storage | Document management | On-demand |
| **OneDrive** | File storage | Projects, Uploads | On-demand |

**API Endpoints**:
```
/teams/{id}/channels/{id}/messages - Post message
/me/events - Calendar events
/me/sendMail - Send email
/drives/{id}/items - File access
```

---

#### 4️⃣ Sparky AI Assistant API

| Module | Purpose | Type |
|---|---|---|
| **Platform/Sparky AI/** | Query processing, AI responses | Real-time |
| **Interface/Projects/** | AI-powered features | Real-time |
| **Dashboards** | Smart recommendations | Real-time |

**Endpoints**:
```
POST /api/v1/assistant/query - Natural language query
POST /api/v1/assistant/chat - Conversation
GET  /api/v1/assistant/capabilities - Features
```

---

### FILE-BASED DATASOURCES

#### CSV Imports

| Source Folder | Purpose | Format |
|---|---|---|
| **Interface/Projects/Upload Projects/** | Project bulk imports | CSV file |
| **Intake Hub** | Store assignment uploads | CSV file |
| **General Setup/** | Employee/associate data | CSV file |

**Typical Fields**:
```
project_id, project_title, status, owner_email,
store_number, start_date, end_date, budget, priority
```

#### Excel Imports

| Source Folder | Purpose | Features |
|---|---|---|
| **Interface/Projects/Upload Projects/** | Multi-sheet project data | Validation formulas |
| **Store Support Projects/** | Complex data uploads | Linked sheets |

**Supported Sheets**:
- Projects
- Store Assignments
- Timeline/Phases
- Budget/Resources

#### JSON Configurations

| File | Purpose | Used By |
|---|---|---|
| `Interface/Admin/role-configuration.json` | Role definitions | Admin system |
| `Interface/Admin/access-groups.json` | AD group mappings | Access control |
| `Interface/Admin/dynamic-links.json` | Navigation links | UI rendering |

---

### DATABASE DATASOURCES

#### PostgreSQL

| Table | Purpose | Modules | Type |
|---|---|---|---|
| `projects` | Project records | All project modules | R/W |
| `users` | User profiles | Admin, Settings | R/W |
| `project_activities` | Activity log | Dashboards | R/W |
| `user_preferences` | UI preferences | Settings | R/W |
| `audit_logs` | Change tracking | Admin, Compliance | R |

#### Redis Cache

| Cache Type | Purpose | TTL |
|---|---|---|
| `session:*` | User sessions | 8 hours |
| `projects:*` | Project lists | 1 hour |
| `stores:*` | Store data | 24 hours |
| `filter_options:*` | Filter values | 6 hours |

---

## 🔄 Data Flow Diagrams

### Primary Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    EXTERNAL DATA SOURCES                    │
├──────────────────────────────────────────────────────────────┤
│ Polaris | HR Systems | Asset Protection | Pricing Ops       │
└────────────────┬─────────────────────────┬──────────────────┘
                 │                         │
                 ▼                         ▼
┌──────────────────────────────────────────────────────────┐
│            ETL PIPELINE / DATA WAREHOUSE                 │
├──────────────────────────────────────────────────────────┤
│ BigQuery Projects:                                       │
│  • polaris-analytics-prod                               │
│  • wmt-assetprotection-prod                             │
│  • athena-gateway-prod                                  │
│  • wmt-pricingops-analytics                             │
└────────────┬─────────────────────────────┬──────────────┘
             │                             │
             ▼                             ▼
┌──────────────────────┐    ┌──────────────────────┐
│  Activity Hub APIs   │    │  REST Integrations   │
│  (Query engines)     │    │  (Workday, AD, etc)  │
└────────────┬─────────┘    └──────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────────┐
│         APPLICATION LAYER (Backend Services)             │
├──────────────────────────────────────────────────────────┤
│ • FastAPI backend (Projects, AMP, etc)                   │
│ • Node.js services (Refresh Guide, etc)                  │
│ • AI Agent (Sparky)                                      │
└────────────┬──────────────────────────────┬─────────────┘
             │                              │
   ┌─────────▼────────────┐    ┌───────────▼─────────────┐
   │ PostgreSQL Database  │    │ Redis Cache Layer       │
   │ • Projects           │    │ • Sessions              │
   │ • Users              │    │ • Cached queries        │
   │ • Audit logs         │    │ • Real-time updates     │
   └──────────────────────┘    └────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────────┐
│                  USER INTERFACE LAYER                    │
├──────────────────────────────────────────────────────────┤
│ • Admin Dashboard      • Projects Dashboard              │
│ • Intake Hub          • Reports & Analytics              │
│ • AMP Dashboard       • Store Refresh Guide              │
│ • Distribution Lists  • User Notifications               │
└──────────────────────────────────────────────────────────┘
```

---

## 📊 Data Dependency Map

```
Initiative Requirements
    ├─ Admin Dashboard
    │  ├─ PostgreSQL (users, projects)
    │  ├─ Active Directory (groups, members)
    │  └─ Audit Logs (audit trail)
    │
    ├─ Projects Module
    │  ├─ BigQuery Asset Protection Data
    │  ├─ PostgreSQL (projects table)
    │  ├─ File Uploads (CSV, Excel)
    │  └─ Redis Cache (project lists)
    │
    ├─ JobCodes-Teaming
    │  ├─ BigQuery Polaris Data
    │  ├─ Workday API (job mappings)
    │  └─ PostgreSQL (assignments)
    │
    ├─ Intake Hub
    │  ├─ BigQuery Asset Protection
    │  ├─ File Uploads
    │  ├─ PostgreSQL (local storage)
    │  └─ Sparky AI (queries)
    │
    ├─ Refresh Guide
    │  ├─ BigQuery Store Refresh Data
    │  ├─ BigQuery Asset Protection
    │  └─ PostgreSQL (progress tracking)
    │
    └─ Pricing Projects
       ├─ BigQuery Pricing Data
       └─ File Uploads (Excel)
```

---

## 🔐 Data Security & Classification

### Sensitivity Levels by Datasource

| Datasource | Classification | Encryption | Access |
|---|---|---|---|
| Polaris | Internal Use | Standard | Department managers |
| Asset Protection | Internal Use | Standard | Project teams |
| Workday (HR data) | Confidential | Strong | HR staff, admins |
| Active Directory | Internal Use | Standard | System admins |
| PostgreSQL | Internal Use | Standard | App services |
| Redis Cache | Internal Use | Standard | Backend only |

---

## ⚠️ Critical Dependencies

### Must-Have Services
1. **BigQuery** - 95% uptime SLA
2. **PostgreSQL** - Database primary
3. **Redis** - Cache layer
4. **Active Directory** - Authentication

### Impact of Outage

| Service | Duration | Impact |
|---|---|---|
| BigQuery (1hr) | Minor - use cache | Read-only mode |
| PostgreSQL (30min) | Critical | Write-only blocked |
| Redis (full) | Moderate | Performance degraded |
| Active Directory (1hr) | Major | No new logins |

---

## 🛠️ Sync Verification

### Check Data Integrity

```bash
# BigQuery - Are datasets current?
SELECT MAX(last_modified) FROM projects_intake_data

# PostgreSQL - Are updates reflected?
SELECT COUNT(*) FROM projects WHERE updated_at > NOW() - INTERVAL 1 HOUR

# Redis - Is cache populated?
redis-cli INFO stats
```

### Verification Checklist
- [ ] BigQuery datasets synchronized (last 24h)
- [ ] PostgreSQL replication lag < 1 second
- [ ] Redis cache hit rate > 80%
- [ ] API response times < 500ms (p95)
- [ ] File upload processing lag < 5 minutes

---

## 📈 Usage Statistics

### Current Data Volumes

| Source | Records | Size | Update Freq |
|---|---|---|---|
| Polaris Schedules | 2.5M | 450 MB | Daily |
| Projects | 196 | 5 MB | Daily |
| Distribution Lists | 450 | 25 MB | Daily |
| Store Data | 4,200+ | 150 MB | Daily |
| Pricing | 50K+ | 100 MB | Daily/Weekly |
| User Profiles | 50K+ | 50 MB | Real-time |

### Query Load

| Source | Queries/Hour | Peak QPS | P95 latency |
|---|---|---|---|
| BigQuery | 5,000+ | 50 | 500ms |
| PostgreSQL | 10,000+ | 100 | 50ms |
| APIs | 2,000+ | 20 | 200ms |
| Redis | 50,000+ | 500 | 5ms |

---

## 🔗 Related Documents

- [README.md](./README.md) - Main datasource overview
- [BigQuery/README.md](./BigQuery/README.md) - BigQuery details
- [APIs/README.md](./APIs/README.md) - API integration guide
- [File-Based/README.md](./File-Based/README.md) - File import guide
- [Databases/README.md](./Databases/README.md) - Database details
- [SYNC-GUIDE.md](./SYNC-GUIDE.md) - Sync schedules & procedures

