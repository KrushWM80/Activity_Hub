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

---

**Version**: 1.1  
**Status**: Active  
**Last Reviewed**: February 24, 2026
