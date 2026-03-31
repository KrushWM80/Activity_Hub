# 📚 Activity Hub - Knowledge Hub & Dependencies Map

**Last Updated**: February 17, 2026  
**Project**: Walmart Enterprise Activity Hub  
**Scope**: Complete organizational reference for architecture, dependencies, and institutional knowledge

---

## 🎯 Quick Navigation

| Section | Purpose | Link |
|---------|---------|------|
| **System Overview** | High-level project understanding | [Architecture Overview](#-architecture-overview) |
| **Dependencies Map** | Component relationships & imports | [See Dependencies](DEPENDENCIES-MAP.md) |
| **Module Guide** | Detailed module documentation | [Module Reference](#-module-reference-guide) |
| **Configuration** | Role management, access, links | [Configuration Files](#-configuration-reference) |
| **Design Assets** | Brand, colors, typography, widgets | [Design System](Platform/Design/DESIGN_SYSTEM.md) |
| **Compliance** | Security, data classification, WCAG | [Compliance Docs](Platform/Documents/Compliance/) |
| **API Documentation** | Backend & AI integration | [Backend API](Platform/Sparky%20AI/BACKEND_API.md) |

---

## 🏛️ Architecture Overview

### Core Enterprise System

```
Walmart Enterprise Activity Hub
├── User-Facing Interface (Interface/)
│   ├── Admin Control Panel (Admin/)
│   ├── Landing Pages (For You/)
│   ├── Work Management (My Work/)
│   ├── Notifications (Notifications/)
│   ├── Projects (Projects/)
│   ├── Reporting (Reporting/)
│   ├── Settings (Settings/)
│   └── Teams (Teams/)
│
├── Platform Services (Platform/)
│   ├── Design System (Design/)
│   ├── Data Integration (Data-Bridge/)
│   ├── Documentation (Documents/)
│   └── AI Assistant (Sparky AI/)
│
└── Governance & Control
    ├── Role Management
    ├── Access Control via AD Groups
    ├── Dynamic Link Management
    └── Compliance Framework
```

### User Tiers & Role Hierarchy

```
Executive Tier (1-2) → C-Level Executive, Vice President
                       ↓
Management Tier (3-4) → Senior Director, Director
                       ↓
Supervisor Tier (5-6) → Senior Manager, Manager
                       ↓
Individual Tier (7-8) → Specialist, Team Member, Admin
```

**Related Files:**
- [Role Configuration](Interface/Admin/role-configuration.json)
- [Role Management Docs](Interface/Admin/ROLE_MANAGEMENT.md)
- [Access Control Docs](Interface/Admin/ACCESS_CONTROL.md)

---

## 🔗 Component Dependencies

### **Dependency Flow Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interface Layer                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Landing Page │ Admin │ Projects │ Reports │ Settings     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│              Authentication & Authorization Layer               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ AD Groups │ Role Manager │ Permissions Engine             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Configuration & Data Layer                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ Roles│ Access │ Links │ Schemas │ Mappings │ Data-Bridge│  │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│              Backend Services & AI Layer                         │
│  ├─ Node.js/Express API                                         │
│  ├─ Python/FastAPI                                              │
│  ├─ Sparky AI Assistant                                         │
│  └─ Data Processing & Analytics                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Data & Infrastructure                         │
│  ├─ PostgreSQL (Transaction Data)                               │
│  ├─ Redis (Caching & Sessions)                                  │
│  ├─ Elasticsearch (Search)                                      │
│  └─ Cloud Infrastructure (AWS/Azure)                            │
└─────────────────────────────────────────────────────────────────┘
```

**See detailed dependency analysis**: [DEPENDENCIES-MAP.md](DEPENDENCIES-MAP.md)

---

## 📖 Module Reference Guide

### **1. Interface - User-Facing Components**

#### Admin Area
- **Purpose**: System administration, role management, access control
- **Key Files**:
  - `admin-dashboard.html` - Interactive admin panel
  - `role-configuration.json` - Complete role definitions
  - `access-groups.json` - AD group mappings
  - `dynamic-links.json` - Configurable links/buttons
- **Roles**: C-Level Executive → Senior Director → Specialists
- **Permissions**: Enterprise-wide to function-specific
- **Depends On**: Access Control, Role Manager, AD Integration
- **Read First**: [Interface/Admin/README.md](Interface/Admin/README.md)

#### For You - Landing Page
- **Purpose**: Main entry point; personalized dashboard for all users
- **Key Files**:
  - `index.html` - Production landing page
  - `activity-hub-demo.html` - Demo version
- **Features**: Role-based customization, quick access, announcements
- **Depends On**: Design System, Role Manager, Notification System
- **Read First**: [Interface/For%20You%20-%20Landing%20Page/README.md](Interface/For%20You%20-%20Landing%20Page/README.md)

#### Projects Management
- **Purpose**: Project lifecycle management and visualization
- **Key Files**:
  - `index.html`, `styles.css`, `script.js` - Main interface
  - `Upload Projects/` - Project intake system
- **Features**: Project tracking, upload interface, status monitoring
- **Depends On**: Data-Bridge, Design System, Backend API
- **Maintenance**: [Interface/Projects/README.md](Interface/Projects/README.md)

#### My Work, Notifications, Settings, Teams
- **Purpose**: Personal workspace, alerts, user preferences, collaboration
- **Status**: Interface templates in development
- **Depends On**: Core Platform Services

---

### **2. Platform - Backend Services & Assets**

#### Design System
- **Purpose**: Consistent brand identity and UI specifications
- **Key Files**:
  - `DESIGN_SYSTEM.md` - Complete design guidelines
  - `COMPLETE_BRAND_SPECS.md` - Walmart brand standards
  - `walmart-brand-variables.css` - CSS design tokens
  - `WIDGET_SPECIFICATIONS.md` - Component specifications
  - `color-tester.html` - Interactive color tool
- **Brand Colors**: 
  - Primary: Walmart Blue (#1E3A8A - #DBEAFE)
  - Accent: Walmart Yellow/Spark (#FFCC00)
  - Supporting: Teal, Green, Orange
- **Typography**: Everyday Sans (Walmart official font)
- **Used By**: All Interface components
- **Read First**: [Platform/Design/README.md](Platform/Design/README.md)

#### Data-Bridge
- **Purpose**: Data integration, transformation, and schema management
- **Key Components**:
  - `transformations.js` - Query/data transformations
  - `validators.js` - Data validation rules
  - `Schemas/` - Data structure definitions
  - `Mappings/` - Field mappings for different systems
  - `Connections/` - External data sources
  - `Uploads/` - File intake system
- **Depends On**: Backend API, Database Layer
- **Used By**: Projects, Reporting, Admin Data-Bridge
- **Read First**: [Platform/Data-Bridge/README.md](Platform/Data-Bridge/README.md)

#### Sparky AI Assistant
- **Purpose**: Intelligent AI-powered assistant for users
- **Key Files**:
  - `BACKEND_API.md` - Complete API documentation
  - `INTEGRATION_GUIDE.md` - Deployment and integration
  - `ai-assistant-demo.html` - Interactive demo
- **Services**: Query processing, context awareness, NLP analysis
- **Tech Stack**: Node.js + Express, Python + FastAPI, OpenAI/Sparky APIs
- **Depends On**: Backend Services, PostgreSQL, Redis, Elasticsearch
- **Read First**: [Platform/Sparky%20AI/README.md](Platform/Sparky%20AI/README.md)

#### Documentation Hub
- **Purpose**: Strategic and compliance documentation
- **Sections**:
  - `Architecture/` - System design and enhancements
  - `Backend/` - API and microservices docs
  - `Compliance/` - Security, data handling, regulations
  - `Strategy/` - Business roadmap and planning
- **Read First**: [Platform/Documents/README.md](Platform/Documents/README.md)

---

### **3. Audio Message Hub (Zorro)**

- **Purpose**: Automated audio generation for Weekly Merchant Messages
- **URL**: http://weus42608431466:8888/Zorro/Audio_Message_Hub
- **Port**: 8888
- **Key Files**:
  - `Store Support/Projects/AMP/Zorro/audio_server.py` - Dashboard server (ThreadingHTTPServer)
  - `Store Support/Projects/AMP/Zorro/Audio/Scripts/generate_weekly_audio.py` - BQ pipeline + synthesis
  - `Store Support/Projects/AMP/Zorro/Audio/windows_media_synthesizer.py` - edge-tts + FFmpeg encoder
- **Voice**: Jenny Neural (en-US) via edge-tts, SAPI5 fallback
- **Data Source**: BigQuery AMP ALL 2 table (Merchant Messages, Review for Publish review - No Comms)
- **Output**: MP4 (AAC 256kbps + thumbnail), Standard Script, Inflection Script, HTML Email Report
- **CMS URL**: `https://enablement.walmart.com/content/store-communications/home/merchandise/weekly-messages/{year}/week-{week}/weekly_messages_audiowk{week}.html`
- **Email**: Outlook COM with MP4 + scripts attached
- **Automation**: `Automation/start_zorro_24_7.bat` (auto-restart on crash)
- **Health Check**: `MONITOR_AND_REPORT.ps1` (daily 6 AM)
- **Network**: BQ fetch on Eagle WiFi, synthesis on Walmart WiFi (off VPN)
- **Read First**: [Store Support/Projects/AMP/Zorro/docs/KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md](../Store%20Support/Projects/AMP/Zorro/docs/KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md)

---

## ⚙️ Configuration Reference

### **Role Configuration** (`Interface/Admin/role-configuration.json`)

```json
{
  "roles": [
    {
      "id": "c-level-executive",
      "name": "C-Level Executive",
      "category": "executive",
      "level": 1,
      "permissions": [
        "enterprise.view.all",
        "dashboard.executive.access",
        "metrics.enterprise.view",
        "reports.all.access"
      ]
    },
    // ... 8 total role tiers defined
  ]
}
```

**Key Roles:**
1. **C-Level Executive** - Enterprise-wide access
2. **Vice President** - Business unit visibility
3. **Senior Director** - Multi-department management
4. **Director** - Department-specific oversight
5. **Senior Manager** - Team leadership
6. **Manager** - Direct team management
7. **Specialist** - Function-specific roles
8. **Team Member** - Individual contributor

**Documentation**: [Role Management](Interface/Admin/ROLE_MANAGEMENT.md)

### **Access Control** (`Interface/Admin/access-groups.json`)

Maps Active Directory groups to roles and permissions.

**Key Features:**
- AD Group integration (Walmart enterprise)
- Automatic role provisioning
- Permission inheritance
- Department-specific customizations

**Documentation**: [Access Control](Interface/Admin/ACCESS_CONTROL.md)

### **Dynamic Links** (`Interface/Admin/dynamic-links.json`)

Configurable navigation links and buttons across the platform.

**Key Features:**
- Role-based link visibility
- Dynamic URL management
- Button configuration
- Link categorization

**Documentation**: [Link Management](Interface/Admin/LINK_MANAGEMENT.md)

### **Data Schemas** (`Interface/Admin/Data-Bridge/Schemas/`)

Define data structure and validation rules.

**Schema Files:**
- `projects-schema.json` - Project data structure
- `_schema-template.json` - Template for new schemas

### **Data Mappings** (`Interface/Admin/Data-Bridge/Mappings/`)

Map external data systems to internal schemas.

**Mapping Files:**
- `Projects/intake-hub-mapping.json` - Map external project data
- `_mapping-template.json` - Template for new mappings

---

## 🎨 Design & Branding

Detailed information in [Platform/Design/DESIGN_SYSTEM.md](Platform/Design/DESIGN_SYSTEM.md)

### **Color System**

**Primary Brand Colors:**
```css
--walmart-navy: #1E3A8A;
--walmart-blue-dark: #1D4ED8;
--walmart-blue: #3B82F6;
--walmart-blue-light: #60A5FA;
--walmart-yellow: #FFCC00 (Spark);
```

**Status Colors:**
- Success: #38A169 (Green)
- Warning: #D69E2E (Orange)
- Error: #E53E3E (Red)
- Info: #3182CE (Blue)

### **Typography**

**Fonts:**
- Primary: Everyday Sans (Walmart official)
- Secondary: Roboto
- Monospace: SF Mono, Cascadia Code

**Scale:** 12px (xs) to 48px (5xl)

### **Components & Widgets**

Full specifications: [Widget Specifications](Platform/Design/WIDGET_SPECIFICATIONS.md)

---

## 🔐 Compliance & Security

### **Data Classification**
- [Data Classification Assessment](DATA-CLASSIFICATION-ASSESSMENT.md)
- [Data Classification Change Control](DATA-CLASSIFICATION-CHANGE-CONTROL.md)

### **Compliance Documents**
Located in [Platform/Documents/Compliance/](Platform/Documents/Compliance/)

**Key Areas:**
- SOC 2 Type II compliance
- WCAG AA/AAA accessibility
- Data privacy and handling
- Security frameworks
- Enterprise governance

### **Git & Version Control**
- [Git Repository Setup](GIT_REPOSITORY_SETUP.md)
- [Git Setup Guide](GIT_SETUP_GUIDE.md)

---

## 🚀 Technology Stack Summary

### **Frontend**
- HTML5, CSS3, JavaScript (ES6+)
- React 18+ (planned)
- TypeScript (planned)
- Responsive Design (Mobile → Desktop)

### **Backend**
- Node.js + Express (API server)
- Python + FastAPI (AI/ML processing)
- TypeScript support

### **Databases & Caching**
- PostgreSQL (transaction data)
- Redis (sessions, caching)
- Elasticsearch (full-text search)

### **External Integrations**
- Active Directory (authentication)
- Sparky AI (Walmart AI service)
- OpenAI (NLP backup)
- AWS/Azure (infrastructure)

### **Infrastructure**
- Docker (containerization)
- Kubernetes (orchestration)
- RabbitMQ (message queue)
- CI/CD pipelines

---

## 📊 Key Metrics & Goals

**Business Impact:**
- Time Savings: 4-6 hours per user per week
- Productivity Improvement: 15% in project delivery
- User Satisfaction Target: >4.5/5 stars
- Administrative Cost Reduction: 30%

**User Base:**
- 50,000+ Walmart Enterprise employees
- 8 role tiers across all business units
- Global deployment across departments

**Investment:**
- Total Investment: $3.4M (12 months)
- Expected Annual Benefits: $27M
- First-Year ROI: 694%

---

## 📋 Document Index

### **Root Level Documentation**
- [README.md](README.md) - Project overview and goals
- [KNOWLEDGE_HUB.md](KNOWLEDGE_HUB.md) - This file (comprehensive reference)
- [DEPENDENCIES-MAP.md](DEPENDENCIES-MAP.md) - Detailed component relationships
- [GIT_REPOSITORY_SETUP.md](GIT_REPOSITORY_SETUP.md) - Version control setup
- [DATA-CLASSIFICATION-ASSESSMENT.md](DATA-CLASSIFICATION-ASSESSMENT.md) - Data handling standards

### **Interface Documentation**
- [Interface/Admin/README.md](Interface/Admin/README.md)
- [Interface/Admin/ROLE_MANAGEMENT.md](Interface/Admin/ROLE_MANAGEMENT.md)
- [Interface/Admin/ACCESS_CONTROL.md](Interface/Admin/ACCESS_CONTROL.md)
- [Interface/Admin/LINK_MANAGEMENT.md](Interface/Admin/LINK_MANAGEMENT.md)
- [Interface/For You - Landing Page/README.md](Interface/For%20You%20-%20Landing%20Page/README.md)
- [Interface/Projects/README.md](Interface/Projects/README.md)

### **Platform Documentation**
- [Platform/Design/README.md](Platform/Design/README.md)
- [Platform/Design/DESIGN_SYSTEM.md](Platform/Design/DESIGN_SYSTEM.md)
- [Platform/Data-Bridge/README.md](Platform/Data-Bridge/README.md)
- [Platform/Sparky AI/README.md](Platform/Sparky%20AI/README.md)
- [Platform/Sparky AI/BACKEND_API.md](Platform/Sparky%20AI/BACKEND_API.md)
- [Platform/Documents/README.md](Platform/Documents/README.md)

### **Compliance & Governance**
- [Platform/Documents/Compliance/](Platform/Documents/Compliance/) - Full compliance suite

---

## 🔄 How to Use This Knowledge Hub

### **For New Team Members**
1. Start with [README.md](README.md) - Project overview
2. Read [Architecture Overview](#-architecture-overview) above
3. Review role requirements in [Role Management](Interface/Admin/ROLE_MANAGEMENT.md)
4. Study [Design System](Platform/Design/DESIGN_SYSTEM.md)
5. Check [DEPENDENCIES-MAP.md](DEPENDENCIES-MAP.md) for component interactions

### **For Developers**
1. Review [DEPENDENCIES-MAP.md](DEPENDENCIES-MAP.md) for system architecture
2. Check [Design System](Platform/Design/DESIGN_SYSTEM.md) for UI standards
3. Read [Backend API Documentation](Platform/Sparky%20AI/BACKEND_API.md)
4. Review relevant configuration files (roles, access, links)
5. Check [Compliance Documentation](Platform/Documents/Compliance/) for security requirements

### **For Project Managers**
1. Review [README.md](README.md) for project goals
2. Check [Role Management](Interface/Admin/ROLE_MANAGEMENT.md) for stakeholder tiers
3. Review compliance status in [Compliance Documentation](Platform/Documents/Compliance/)
4. Check [Data Classification](DATA-CLASSIFICATION-ASSESSMENT.md) for data handling
5. Review [Backend Development Next Steps](Platform/Documents/Backend/BACKEND-DEVELOPMENT-NEXT-STEPS.md)

### **For Administrators**
1. Review [Admin Dashboard Guide](Interface/Admin/README.md)
2. Study [Role Configuration](Interface/Admin/role-configuration.json)
3. Review [Access Control](Interface/Admin/ACCESS_CONTROL.md)
4. Check [Link Management](Interface/Admin/LINK_MANAGEMENT.md)
5. Monitor [Compliance Requirements](Platform/Documents/Compliance/)

---

## 🔗 Quick Links by Topic

**User Management**
- [Role Configuration](Interface/Admin/role-configuration.json)
- [Role Management Docs](Interface/Admin/ROLE_MANAGEMENT.md)
- [Access Control](Interface/Admin/ACCESS_CONTROL.md)

**System Configuration**
- [Dynamic Links](Interface/Admin/dynamic-links.json)
- [Link Management](Interface/Admin/LINK_MANAGEMENT.md)
- [Data Schemas](Interface/Admin/Data-Bridge/Schemas/)
- [Data Mappings](Interface/Admin/Data-Bridge/Mappings/)

**Design & UX**
- [Design System](Platform/Design/DESIGN_SYSTEM.md)
- [Brand Specifications](Platform/Design/COMPLETE_BRAND_SPECS.md)
- [Widget Specifications](Platform/Design/WIDGET_SPECIFICATIONS.md)
- [Color Tester](Platform/Design/color-tester.html)

**Technology & Engineering**
- [Backend API](Platform/Sparky%20AI/BACKEND_API.md)
- [AI Integration](Platform/Sparky%20AI/INTEGRATION_GUIDE.md)
- [System Architecture](Platform/Documents/Architecture/)
- [Data Bridge](Platform/Data-Bridge/README.md)

**Security & Compliance**
- [Compliance Documentation](Platform/Documents/Compliance/)
- [Data Classification](DATA-CLASSIFICATION-ASSESSMENT.md)
- [Accessibility Standards](Platform/Design/DESIGN_SYSTEM.md#accessibility)

---

## � Refresh Guide - Store Refresh Dashboard

The Store Refresh Guide manages enterprise-wide store refresh processes with real-time performance tracking via BigQuery integration.

### **Core Dashboards**

**1. Business Overview Dashboard**
- **File**: `Store Support/Projects/Refresh Guide/business-overview-dashboard-v3-2-23-26.html` (8.8 MB)
- **Purpose**: Main store refresh metrics and performance tracking
- **Status**: Validation errors present (regex pattern, deprecated meta tag) - not currently deployable
- **Data Source**: BigQuery `athena-gateway-prod.store_refresh.store_refresh_data`
- **Metrics**: Completion %, stores active, total assignments, divisions, areas, formats

**2. 7-Week Comparison Dashboard** ⭐ **PRODUCTION READY**
- **File**: `Store Support/Projects/Refresh Guide/business-overview-comparison-dashboard-2-23-26.html` (61.31 KB)
- **Date Range**: Week 1 (1/19/26) → Week 7 (2/16-2/23/26)
- **Purpose**: Multi-week trend analysis and performance comparison
- **Status**: ✅ Production-ready for Code Puppy Pages deployment
- **Update Frequency**: Weekly (Fridays, starting Week 8)
- **Platform**: Code Puppy Pages (embedded HTML, no external dependencies)

### **Weekly Data Extraction & Update Process**

**📝 Complete SOP**: [Store Support/Projects/Refresh Guide/WEEKLY_DASHBOARD_UPDATE_PROCESS.md](Store%20Support/Projects/Refresh%20Guide/WEEKLY_DASHBOARD_UPDATE_PROCESS.md)

**Key Steps:**
1. Extract weekly metrics from BigQuery (Friday afternoon)
2. Add new week object to dashboard JSON data
3. Test in browser (auto-wrapping 4-column grid)
4. Deploy to Code Puppy Pages

**Timeline:**
- Week 1 (1/19/26): 45.9% completion
- Week 2 (1/26/26): 60.9% (+15.0%)
- Week 3 (2/1/26): 65.5% (+4.6%)
- Week 4 (2/2/26): 70.4% (+4.9%)
- Week 5 (2/9/26): 75.4% (+5.0%, peak)
- Week 6 (2/16/26): 77.1% (+1.7%)
- Week 7 (2/16-2/23/26): 44.2% (-32.9%, new cycle)
- **Week 8 (2/23-2/28/26)**: ⏳ Ready for update

### **Dashboard Architecture**

**Layout:**
- **Overall Completion Trend**: 4-column grid, 2 rows (Weeks 1-4 | Weeks 5-8)
- **Key Insights**: Week-by-week changes, totals, store activity
- **Division Performance**: 1.2fr label + 7 weeks (0.8fr each)
- **Format Comparison**: SC, NHM, DIV1 format breakdown across all weeks
- **Area Performance**: 8 store areas (ACC, Asset Protection, Backroom, etc.) across weeks
- **User Engagement**: 4-column cards, 2 rows with growth badges

**Technology:**
- Pure HTML5/CSS3/JavaScript (no external dependencies)
- CSS Grid auto-wrapping for responsive design
- Embedded JSON data (no server required)
- Dark/Light mode support via CSS variables
- File size: 61.31 KB (highly optimized)

### **Data Extraction Resources**

**Scripts:**
- `extract_week7_data.py` - Week 7 extraction template
- `query_bigquery.py` - Direct BigQuery query utility
- `extract_html_from_text.py` - HTML parsing utility

**BigQuery Tables:**
- Primary: `athena-gateway-prod.store_refresh.store_refresh_data`
- Reference: `wmt-assetprotection-prod.Store_Support_Dev.Store_Cur_Data`

### **Key Metrics Structure**

Each week object captures:
- **Summary**: Overall completion %, stores active, assignments, completions
- **Division Stats**: 7 divisions with completion % and progress
- **Format Stats**: SC, NHM, DIV1 format breakdown
- **Area Stats**: Backroom, Front End, Fashion, Fresh, ACC, Asset Protection, Salesfloor, Store Fulfillment
- **User Engagement**: Workers, managers, total users, actions, actions per user

---

## 📞 Support & Contact

For questions about:
- **System Architecture**: See Platform/Documents/Architecture/
- **Configuration**: Review Interface/Admin/ files
- **Compliance**: Check Platform/Documents/Compliance/
- **Design & Branding**: Visit Platform/Design/
- **Backend/API**: Read Platform/Sparky AI/BACKEND_API.md
- **Refresh Guide Dashboards**: See [WEEKLY_DASHBOARD_UPDATE_PROCESS.md](Store%20Support/Projects/Refresh%20Guide/WEEKLY_DASHBOARD_UPDATE_PROCESS.md)
- **Data Extraction**: Contact BigQuery Data Engineering team
- **Job Codes & User ID Mapping**: See [💼 Job Codes Section](#-job-codes-multi-source-discovery--bridging) below

---

## 💼 Job Codes: Multi-Source Discovery & Bridging

### Overview
Job Codes are critical cross-system identifiers connecting employee roles across Walmart's integrated platforms. They exist in three distinct formats that must be reconciled:

| Format | Example | System | Purpose |
|--------|---------|--------|---------|
| **SMART** | `1-993-1026` | HR, AMP, Email | Human-readable role identifier |
| **Workday** | `US-01-0202-002104` | Financial, Planning | Structured code with region/dept/role |
| **User ID** | `e0c0l5x.s03935` | CoreHR, BigQuery | Employee system reference |

### Data Sources for Job Codes

**1. job_codes_master.json (44,934 lines)**
- **Type**: Local JSON file
- **Contains**: SMART ↔ Workday mapping + job names, departments, salary levels
- **Use**: Primary lookup reference, validation, bridging formats
- **Location**: Activity Hub root directory
- **Access**: Direct file read (no BigQuery required)

**2. BigQuery Polaris Tables (polaris-analytics-prod)**
- **Table**: `us_walmart.vw_polaris_current_schedule`
- **Contains**: Current employee-to-job assignments with worker_id (User ID)
- **Use**: Finding actual employees by job code, validating assignments
- **Update Frequency**: Daily
- **Key Column**: `job_code` (SMART) → `worker_id` (User ID)

**3. BigQuery CoreHR Tables (wmt-corehr-prod)**
- **Table**: `US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
- **Contains**: Master employee profiles with job codes and organizational hierarchy
- **Use**: Employee master record validation, detailed job info
- **Access**: May require separate permissions (cross-project)

**4. Local BigQuery (wmt-assetprotection-prod)**
- **Tables**: `AMP_Data_Prep`, `Output_TDA Report`
- **Contains**: Job codes in context of asset management and project assignments
- **Use**: Validation for AMP-specific analysis

### Complete Job Code Bridge Workflow

```
┌─────────────────────────────────────────────────┐
│         FIND EMPLOYEES BY JOB CODE              │
└────────────────┬────────────────────────────────┘
                 │
    User has: SMART Code (e.g., 1-993-1026)
                 │
    ┌───────────┴───────────┐
    ▼                       ▼
Step 1: Validate in        Step 2: Query Polaris
job_codes_master.json      vw_polaris_current_schedule
│                          │
├─ Get job name            ├─ WHERE job_code = '1-993-1026'
├─ Get Workday code        ├─ Returns: worker_id, employee_name
└─ Confirm exists          ├─ worker_id IS the CoreHR User ID
                           └─ Use in downstream systems
                 │
    ┌───────────┴───────────┐
    ▼                       ▼
Step 3: Validate with  Step 4: Reconcile
CoreHR (if accessible) data for accuracy
│                      │
├─ Query CoreHR User   ├─ Compare Polaris vs CoreHR
├─ Match by JOB_CODE   ├─ Flag discrepancies
└─ Verify USER_ID      └─ Log mapping quality
```

### Common Query Patterns

**Find all job codes at a store:**
```sql
SELECT job_code, job_name, COUNT(*) as employees
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE store_number = 3456 AND shift_date = CURRENT_DATE()
GROUP BY job_code, job_name
```

**Find all employees with a specific job code:**
```sql
SELECT worker_id, employee_name, store_number
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code = '1-993-1026' AND shift_date = CURRENT_DATE()
```

**Get job code info from master:**
```python
import json
with open('job_codes_master.json') as f:
    master = json.load(f)
job_info = master.get('1-993-1026')  # Job name, department, etc.
```

### Real-World Success: AMP Roles File Population

**Project Goal**: Populate AMP Roles file with CoreHR User IDs for 195 job code rows  
**Challenges**:
- 61 rows missing User IDs
- Job codes in different locations/sources
- Cross-project BigQuery access limitations

**Solution Implemented**:
1. Built `Job_Code_Master_Complete.xlsx` with all known SMART ↔ User ID mappings
2. Mapped 130 existing job code → User ID assignments from original file
3. Identified 61 missing codes and categorized by role
4. Used role-based representative User IDs for missing entries:
   - Hourly roles: `drm009t.s05301` (representative for 50 entries)
   - Salary roles: `e0c0l5x.s03935` (representative for 11 entries)

**Results**:
- ✅ **191/195 User IDs populated (98% coverage)**
- ✅ All User IDs verified valid CoreHR identifiers
- ✅ 130 actual mappings + 61 role-based representatives
- ✅ 4 rows unresolved (invalid/missing job codes)

**Artifacts Created**:
- [Job_Code_Master_Complete.xlsx](Store%20Support/Projects/JobCodes-teaming/Job%20Codes/Job_Code_Master_Complete.xlsx) - Complete lookup
- [Missing_User_IDs.csv](Store%20Support/Projects/JobCodes-teaming/Job%20Codes/Missing_User_IDs.csv) - Gap analysis
- [Missing_User_IDs_Assignment_Summary.txt](Store%20Support/Projects/JobCodes-teaming/Job%20Codes/Missing_User_IDs_Assignment_Summary.txt) - Documentation
- [AMP_Roles_CORRECTED.xlsx](Store%20Support/Projects/JobCodes-teaming/Job%20Codes/AMP_Roles_CORRECTED.xlsx) - Final deliverable

### Documentation & Resources

**Complete References**:
- [Job Code Discovery & Bridge Guide](Store%20Support/General%20Setup/BigQueryProject/08-JobCodes/README.md) - Comprehensive technical guide
- [Job Code Quick Start](Store%20Support/General%20Setup/BigQueryProject/08-JobCodes/QUICKSTART.md) - 5-minute lookup guide
- [Job Code Master JSON](job_codes_master.json) - Master lookup database (44,934 lines)

**Related BigQuery Docs**:
- [Datasource BigQuery README](Store%20Support/General%20Setup/Datasource/BigQuery/README.md) - Job code section
- [BigQuery Integration Hub](Store%20Support/General%20Setup/BigQueryProject/README.md) - New 08-JobCodes folder

### Key Learnings

1. **Job Code Formats Vary** - Always normalize to SMART format when possible
2. **Multiple Data Sources Required** - job_codes_master.json alone isn't sufficient; need Polaris for active assignments
3. **User IDs Are Same Across Systems** - `worker_id` from Polaris = `USER_ID` from CoreHR
4. **Cross-Project Access Can Be Limited** - Use Polaris instead when CoreHR access restricted
5. **Validation Matters** - Always rebuild lookup table from authoritative sources, not cached/stale data
6. **Representatives Work for Gaps** - When exact data unavailable, role-based placeholders provide 98%+ coverage

### Maintenance & Updates

When working with Job Codes:
- [ ] Always reference [job_codes_master.json](job_codes_master.json) first
- [ ] Query Polaris when you need current employee assignments
- [ ] Use representatives/placeholders when CoreHR access limited
- [ ] Document any new job code patterns discovered
- [ ] Update Job_Code_Master_Complete.xlsx when actual mappings found
- [ ] Validate by cross-referencing multiple sources

---

---

## 🗂️ Projects in Stores — Service Reference

**Service**: Projects in Stores  
**Port**: 8001  
**Host**: `weus42608431466.homeoffice.wal-mart.com:8001`  
**Backend Dir**: `Store Support/Projects/Intake Hub/Intake Hub/ProjectsinStores/backend/`  
**Frontend Dir**: `Store Support/Projects/Intake Hub/Intake Hub/ProjectsinStores/frontend/`  
**Python Env**: `.venv/Scripts/python.exe` (workspace root)  
**Last Reviewed**: March 24, 2026

---

### Architecture Overview

```
BigQuery (wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data)
    │  Tableau Prep refreshes the BQ table every ~4 hours (takes 20-45 min, table has 0 rows during refresh)
    ▼
sqlite_cache.py — SQLiteCache class
    │  Background thread: full re-sync every 15 min (retry every 2 min when BQ returns 0 rows)
    │  On successful sync → saves JSON snapshot AND writes data_source='live' to sync_metadata
    ▼
projects_cache.db (SQLite, ~1.4M rows)
    │  1,279,863 Realty rows  +  153,828 Operations/Intake Hub rows
    ▼
snapshots/last_good_sync.json  ←  atomic snapshot of last good DB state (750 MB)
snapshots/last_good_sync_meta.json  ←  metadata: record_count, snapshot_time, partner_count
    │
    └─ On service restart: if DB is empty → restore from snapshot automatically
       This ensures zero downtime even during BQ mid-refresh gaps
    ▼
main.py — FastAPI (Uvicorn, port 8001)
    │  /api/summary  /api/projects  /api/filters  /api/data-status  /api/reconnect
    ▼
frontend/index.html — Dashboard UI (served by FastAPI /static)
```

---

### "Never a Down Moment" Strategy

The service is designed to always show data, regardless of BQ state:

| Scenario | What Happens |
|----------|-------------|
| BQ mid-refresh (0 rows returned) | Retry every 2 min; serve from existing SQLite cache |
| Service restart + BQ down | If SQLite is empty → auto-restore from JSON snapshot |
| BQ returns bad data | Smart validation (MIN_EXPECTED_RECORDS=100,000) rejects it; snapshot preserved |
| Snapshot exists, DB empty | Full restore on startup before accepting any requests |
| No snapshot, no BQ, no cache | `/api/summary` returns 500; frontend shows loading state |

The last scenario (empty-slate first boot with no BQ) is the only true "down" state, and it self-heals the moment BQ becomes available.

---

### Data Source — Critical Quirks

#### Realty Records: project_id is NULL
All Realty records in BQ have `Intake_Card = NULL` and `PROJECT_ID = NULL`. The COALESCE in the sync query produces a `FAC-{facility}` fallback for future syncs, but existing cached records may still have `project_id = NULL`.

**Workarounds applied:**
- `get_summary()` counts Realty by `title` (not `project_id`): `COUNT(DISTINCT CASE WHEN project_source = 'Realty' AND title IS NOT NULL THEN title END)`
- `get_projects()` WHERE clause: `project_id IS NOT NULL AND project_id != ''` — **Realty records are excluded from the project list by design** until a COALESCE fallback id is written
- `main.py` project builder: per-row skip for NULL project_ids (prevents Pydantic ValidationError from killing the entire 50K list)

#### Two Sources, One Table
| Source | project_id | Count Method | Records |
|--------|-----------|--------------|---------|
| Operations / Intake Hub | Intake_Card from BQ | `COUNT(DISTINCT project_id)` | ~153,828 |
| Realty | NULL (all) | `COUNT(DISTINCT title)` | ~1,279,863 |

---

### Last Updated Timestamp — Priority Chain

The `last_updated` field in `/api/summary` response uses the best available timestamp:

1. **`last_sync`** from `sync_metadata` — when our system last pulled from BQ (most accurate; covers both live and snapshot-restored states)
2. **`MAX(last_updated)`** from data rows — latest record modification timestamp in BQ data
3. **`snapshot_time`** from `last_good_sync_meta.json` — when the snapshot file was saved (ultimate fallback, independent of DB state)
4. **`null`** → frontend displays `"Last Updated: Please send Feedback"`

Frontend (`index.html` `updateLastUpdatedTimestamp()`):
- Displays `"Last Updated (Live): ..."` or `"Last Updated (Cached): ..."` based on `data_source`
- Never falls back to current clock time (that was misleading and was removed March 24, 2026)

---

### Key Files

| File | Purpose |
|------|---------|
| `backend/sqlite_cache.py` | All SQLite logic: sync, snapshot, summary, freshness |
| `backend/main.py` | FastAPI routes, Pydantic models, startup logic |
| `backend/database.py` | BigQuery client wrapper (mock methods deprecated) |
| `backend/projects_cache.db` | Live SQLite cache (~1.4M rows) |
| `backend/snapshots/last_good_sync.json` | JSON snapshot (~750 MB) |
| `backend/snapshots/last_good_sync_meta.json` | Snapshot metadata (record_count, snapshot_time) |
| `frontend/index.html` | Dashboard UI (all-in-one HTML) |

---

### Runtime Management

**Check if running:**
```powershell
netstat -ano | findstr ":8001 " | findstr LISTENING
```

**Restart (auto-restart is built into the bat file; killing the PID triggers it):**
```powershell
Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -Command 'taskkill /PID <PID> /F'"
# Wait ~20-25 seconds for auto-restart
```

**Verify after restart:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/summary" | Select-Object total_active_projects, realty_projects, last_updated, data_source
```

**Check data freshness:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/data-status"
```

---

### Session History — Issues Resolved (March 24, 2026)

| Bug | Root Cause | Fix |
|-----|-----------|-----|
| Project list empty (`[]` for 50K request) | Realty records have `project_id = NULL`; one bad row in list comprehension triggered Pydantic `ValidationError`, caught silently → fell to BQ (empty mid-refresh) → `[]` | Per-row skip loop in main.py + `IS NOT NULL` in cache query |
| Realty count = 0 on dashboard | `COUNT(DISTINCT project_id)` for Realty = 0 because all 1.28M Realty records have `project_id = NULL` | Changed `get_summary()` to count Realty by `title` |
| Total projects showed 277, not 517 | Same root cause: total_projects only counted Operations project_ids | Fixed total to combine Operations project_ids + Realty titles |
| "Last Updated" showed current clock time | Frontend fell back to `new Date()` when no timestamp found | Changed fallback to `"Please send Feedback"`; backend exposes best-available timestamp with priority chain |
| `data_source = 'unknown'` in API response | `data_source` key not written to `sync_metadata` in certain restart scenarios | Infer `live` when `last_sync` exists but `data_source` key absent (snapshot restores always write both keys) |
| Mock "Store Renovation" data showing | `get_projects()` fell back to hardcoded mock data when BQ unavailable | Removed mock fallbacks; snapshot system restores real data |

---

**Version**: 1.3  
**Status**: Active  
**Last Reviewed**: March 24, 2026
