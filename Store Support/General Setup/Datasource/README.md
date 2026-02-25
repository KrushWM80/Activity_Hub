# 📊 Activity Hub - Datasource Documentation

## Overview
This folder documents all data sources integrated into the Activity Hub system. It includes descriptions of each datasource, their purpose, current usage, and which folders/projects depend on them.

---

## 🗂️ Folder Structure

```
Datasource/
├── README.md                    # This file - Main index
├── DATASOURCE-MATRIX.md         # Cross-reference matrix showing data flows
│
├── BigQuery/                    # Cloud data warehouse sources
│   ├── README.md                # BigQuery overview
│   ├── Polaris.md               # Polaris scheduling system
│   ├── Asset-Protection.md      # Asset Protection & Intake Hub data
│   ├── Store-Refresh.md         # Store refresh touring data
│   ├── Pricing.md               # Pricing operations data
│   └── templates/
│       └── bigquery-query-template.sql
│
├── APIs/                        # External API integrations
│   ├── README.md                # API sources overview
│   ├── Workday.md               # Workday HR system
│   ├── Active-Directory.md      # Microsoft Active Directory
│   ├── MS-Graph.md              # Microsoft Graph (Teams, Outlook, SharePoint)
│   ├── Sparky-AI.md             # Sparky AI Assistant
│   └── templates/
│       └── api-connection-template.md
│
├── File-Based/                  # File uploads & imports
│   ├── README.md                # File-based sources overview
│   ├── CSV-Excel-Imports.md     # CSV and Excel file uploads
│   ├── JSON-Config.md           # JSON configuration files
│   └── templates/
│       └── file-import-template.md
│
├── Databases/                   # Internal database connections
│   ├── README.md                # Database sources overview
│   ├── PostgreSQL.md            # PostgreSQL databases
│   └── templates/
│       └── db-connection-template.md
│
└── SYNC-GUIDE.md                # Data synchronization schedule & procedures
```

---

## 📌 Quick Reference: Datasources at a Glance

| **Data Source** | **Type** | **Purpose** | **Primary Users** | **Sync Frequency** |
|---|---|---|---|---|
| **Polaris** | BigQuery | Store scheduling, labor planning | JobCodes-teaming, AMP | Daily |
| **Asset Protection** | BigQuery | Projects, store assignments | Intake Hub, Projects | Daily |
| **Store Refresh Data** | BigQuery | Store touring information | Refresh Guide, Store Support | Daily |
| **Pricing** | BigQuery | Pricing operations & COOP | Pricing Project | As needed |
| **Workday** | API | Employee HR data, job codes | Distribution Lists, General Setup | Daily |
| **Active Directory** | API | User authentication, groups | Admin, Access Control | Real-time |
| **Microsoft Graph** | API | Teams, Outlook, SharePoint | Notifications, Teams, Calendar | Real-time |
| **Sparky AI** | API | AI queries and processing | Sparky AI Assistant | Real-time |
| **CSV/Excel Files** | File Upload | Manual data imports | Projects, Intake Hub | On-demand |
| **PostgreSQL** | Database | Local project storage | Projects Dashboard | Real-time |

---

## 🎯 How to Use This Documentation

### For Developers
- Check **BigQuery/** for query templates and schema information
- See **APIs/** for authentication and endpoint details
- Review **Databases/** for connection strings and models

### For Project Managers
- Use **DATASOURCE-MATRIX.md** to see data dependencies
- Check **SYNC-GUIDE.md** for synchronization schedules
- Reference this README for high-level overview

### For System Administrators
- Review **Active-Directory.md** and **MS-Graph.md** for access control
- Use **SYNC-GUIDE.md** to monitor data flow
- Check each source's README for troubleshooting

### For Compliance/Security
- Review **DATA-CLASSIFICATION** in project root for security levels
- Check **APIs/** for authentication mechanisms
- Verify credentials management in each source folder

---

## 🔄 Data Flow Overview

```
Activity Hub System
│
├─► Polaris Scheduling (BigQuery)
│   └─ Used by: JobCodes-teaming, AMP Dashboard
│
├─► Asset Protection (BigQuery)
│   ├─ Used by: Intake Hub, Projects Dashboard
│   └─ Updated by: Manual uploads, Field data
│
├─► Store Refresh (BigQuery)
│   └─ Used by: Refresh Guide, Store Support
│
├─► Workday HR Data (API)
│   ├─ Used by: Distribution Lists, User Lookup
│   └─ Sync triggers: Daily, On-demand
│
├─► Active Directory (API)
│   ├─ Used by: Admin Dashboard, Access Control
│   └─ Sync triggers: Real-time
│
├─► Microsoft Graph (API)
│   ├─ Used by: Teams notifications, Calendar events
│   └─ Sync triggers: Real-time, Event-based
│
└─► File Uploads (CSV/Excel)
    └─ Used by: Project imports, Bulk updates
```

---

## 📊 Data Integration Matrix

See [DATASOURCE-MATRIX.md](./DATASOURCE-MATRIX.md) for:
- Complete list of which folders use which datasources
- Data dependencies and relationships
- Update frequency requirements
- Error handling and fallback procedures

---

## 🔐 Security & Authentication

Each datasource has specific authentication requirements:

### BigQuery
- **Method**: Google Cloud service account credentials
- **Location**: Environment variables or config files
- **Scope**: Read-only in most cases, write for specific processes

### APIs (Workday, Active Directory, MS Graph)
- **Method**: OAuth 2.0, API keys, service accounts
- **Credential Storage**: Secure credential manager (Azure Key Vault)
- **Token Refresh**: Automatic

### File-Based
- **Validation**: Schema validation, type checking
- **Restrictions**: File size limits, type restrictions
- **Scanning**: Malware and security scanning on upload

### Databases
- **Connection**: SSL/TLS encryption required
- **Authentication**: Database credentials in secure vault
- **Access**: Role-based database access control

---

## 🚀 Getting Started

### 1. **New to Activity Hub?**
   - Start with [README.md Overview](#overview) above
   - Read the Quick Reference table
   - Browse the relevant datasource folder (BigQuery/, APIs/, etc.)

### 2. **Need to Add a New Data Source?**
   - Follow the structure in the relevant folder
   - Use templates provided in `templates/` subdirectories
   - Update DATASOURCE-MATRIX.md with new flows
   - Update this README with changes

### 3. **Troubleshooting Data Issues?**
   - Check SYNC-GUIDE.md for schedules and status
   - Review error logs in each datasource folder
   - See troubleshooting section in individual source documentation

### 4. **Checking Data Dependencies?**
   - Run a query on DATASOURCE-MATRIX.md
   - Look for circular dependencies or broken chains
   - Verify all nested data updates are synchronized

---

## 📝 Activity Hub Folders Using Each Datasource

### 🗂️ BigQuery Sources
- **Polaris**: JobCodes-teaming/, AMP/
- **Asset Protection**: Intake Hub/, Projects/
- **Store Refresh**: Refresh Guide/, Store Support General/
- **Pricing**: Store Support/Projects/Pricing/

### 🗂️ API Sources
- **Workday**: Distribution Lists/, General Setup/
- **Active Directory**: Admin/, General Setup/
- **MS Graph**: Notifications/, Teams/, Calendar/, Outlook/
- **Sparky AI**: Sparky AI/, Projects/

### 🗂️ File-Based
- **CSV/Excel**: Projects/Upload Projects/, Any import wizard

### 🗂️ Database Sources
- **PostgreSQL**: Projects Dashboard, Various backends

---

## 📞 Support & Contact

For questions about datasources:
- **BigQuery issues**: Check Platform/Documents/Architecture/
- **API issues**: See Platform/INTEGRATION_GUIDE.md
- **Data sync problems**: Check SYNC-GUIDE.md
- **Access issues**: Contact Admin dashboard

---

## 🔄 Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | Feb 2026 | Initial datasource documentation structure |

---

## 📚 Related Documents

- [DATA-CLASSIFICATION-ASSESSMENT.md](../../DATA-CLASSIFICATION-ASSESSMENT.md) - Security classification
- [DEPENDENCIES-MAP.md](../../DEPENDENCIES-MAP.md) - System dependencies  
- [Platform Architecture](../../Platform/Documents/Architecture/) - System design
- [INTEGRATION_GUIDE.md](../../Platform/Sparky%20AI/INTEGRATION_GUIDE.md) - Integration details

