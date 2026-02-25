# 📚 Refresh Guide - Knowledge Base Reference

**Last Updated**: February 24, 2026  
**Purpose**: Index of institutional knowledge and system mapping for Refresh Guide project  
**Status**: Active Reference

---

## 🔗 Enterprise Knowledge Base

The Walmart Enterprise Activity Hub maintains comprehensive documentation about system architecture, dependencies, and institutional knowledge. This document indexes the relevant sections for the Refresh Guide project.

### **Primary Knowledge Documents** (Root Level)

| Document | Purpose | Key Sections |
|----------|---------|--------------|
| [KNOWLEDGE_HUB.md](/../../KNOWLEDGE_HUB.md) | Main system architecture & institutional knowledge | System overview, configuration, design system, Refresh Guide dashboard section |
| [DEPENDENCIES-MAP.md](/../../DEPENDENCIES-MAP.md) | Component relationships & data flows | Layer dependencies, data flows, Refresh Guide workflow, critical paths |
| [NAVIGATION-INDEX.md](/../../NAVIGATION-INDEX.md) | Workspace navigation & file discovery | Directory structure, quick links |
| [DATA-CLASSIFICATION-ASSESSMENT.md](/../../DATA-CLASSIFICATION-ASSESSMENT.md) | Data security & compliance | Classification levels, handling requirements |

---

## 📊 Refresh Guide Dashboard Documentation

### **Dashboard Files**

**1. Business Overview Comparison Dashboard** (PRODUCTION READY ✅)
- **File**: `business-overview-comparison-dashboard-2-23-26.html`
- **Size**: 61.31 KB
- **Data Range**: Week 1 (1/19/26) → Week 7 (2/23/26)
- **Status**: ✅ Production-ready for Code Puppy Pages
- **Updates**: Weekly (Fridays)

**2. Weekly Update Process**
- **Document**: [WEEKLY_DASHBOARD_UPDATE_PROCESS.md](./WEEKLY_DASHBOARD_UPDATE_PROCESS.md)
- **Purpose**: Complete SOP for data extraction → dashboard update → validation
- **Covers**: 4-phase process, templates, checklist, troubleshooting

**3. Supporting Files**
- `extract_week7_data.py` - BigQuery extraction script
- `query_bigquery.py` - Direct BigQuery query utility
- Data output: `data/v3-user-engagement-data.json`

---

## 🔍 Quick Reference Links

### **System Architecture**
- [System Overview](../../SYSTEM-OVERVIEW.md) - High-level project understanding
- [Architecture docs](../../Platform/Documents/Architecture/) - Detailed system design

### **Configuration & Administration**
- [Role Management](../../Interface/Admin/ROLE_MANAGEMENT.md) - Permission structure
- [Access Control](../../Interface/Admin/ACCESS_CONTROL.md) - Authentication & authorization
- [Link Management](../../Interface/Admin/LINK_MANAGEMENT.md) - Dynamic navigation

### **Design & Branding**
- [Design System](../../Platform/Design/DESIGN_SYSTEM.md) - Colors, typography, components
- [Brand Specifications](../../Platform/Design/OFFICIAL_COLOR_PALETTE.md)

### **Data & Compliance**
- [Data Classification](../../DATA-CLASSIFICATION-ASSESSMENT.md) - Security levels
- [Compliance Documentation](../../Platform/Documents/Compliance/)

### **Backend & APIs**
- [Backend API Documentation](../../Platform/Sparky%20AI/BACKEND_API.md) - REST endpoints
- [Sparky AI Integration](../../Platform/Sparky%20AI/INTEGRATION_GUIDE.md)

---

## 🎯 Refresh Guide Specific Resources

### **Weekly Dashboard Update Workflow**

```
1. Data Extraction (Friday Start)
   ↓
   [WEEKLY_DASHBOARD_UPDATE_PROCESS.md → Phase 1]
   ↓
2. Data Transformation (Mid-Week)
   ↓
   [WEEKLY_DASHBOARD_UPDATE_PROCESS.md → Phase 2]
   ↓
3. Dashboard Update (End of Week)
   ↓
   [WEEKLY_DASHBOARD_UPDATE_PROCESS.md → Phase 3]
   ↓
4. Validation & Deployment (Friday)
   ↓
   [WEEKLY_DASHBOARD_UPDATE_PROCESS.md → Phase 4]
   ↓
Code Puppy Pages Deployment ✅
```

### **Data Extraction Template Access**

- **Phase 1 - Raw Metrics Extraction**: See [WEEKLY_DASHBOARD_UPDATE_PROCESS.md - Phase 1](./WEEKLY_DASHBOARD_UPDATE_PROCESS.md#phase-1-data-extraction-start-of-week)
- **BigQuery Tables**: `athena-gateway-prod.store_refresh.store_refresh_data`
- **Backup Source**: `wmt-assetprotection-prod.Store_Support_Dev.Store_Cur_Data`

### **Weekly Metrics Structure**

See [WEEKLY_DASHBOARD_UPDATE_PROCESS.md - Metric Structure](./WEEKLY_DASHBOARD_UPDATE_PROCESS.md#1a-query-bigquery-for-raw-metrics)

**Key Fields to Verify:**
- `totalPossibleItems` - Has this changed (new cycle)?
- `totalCompletedItems` - Should never decrease from previous week
- Division stats (7 divisions)
- Format stats (SC, NHM, DIV1)
- Area stats (8 areas)
- User engagement metrics

---

## ⚠️ Data Validation Checklist

### **For Each Weekly Update:**

- [ ] Total Completed Items ≥ Previous Week (never decreases)
- [ ] Total Possible Items constant OR intentional increase (new cycle)
- [ ] Division completion % should trend upward or plateau (not decrease)
- [ ] Format stats sum to overall completion %
- [ ] Area stats align with store counts
- [ ] User counts trending upward (workers, managers)
- [ ] All 7 divisions present and calculating
- [ ] Completion percentages between 0-100%

### **Data Integrity Alerts:**

| Scenario | Cause | Action |
|----------|-------|--------|
| Completed items decrease | Data incomplete or wrong cycle | Re-query BigQuery, verify date range |
| Completion % increases but items flat | Division reassignments | Verify with Business Owner |
| New divisions appear | System change | Update dashboard rendering, document change |
| Total possible items increase 10%+ | New refresh cycle | Confirm with stakeholders, document cycle boundary |
| User counts drop | System change or query error | Re-verify query filters |

---

## 🔄 Week 8 Preparation (2/23-2/28/26)

**Status**: ⏳ Pending
**Extraction Date**: Friday 2/28/26

### **Specific Validation for Week 8:**

1. **Cycle Confirmation**: Verify if Week 8 continues Week 7 cycle or starts new cycle
   - If continuing: Total completed items should be ≥ 742,560
   - If new cycle: New total possible items expected

2. **Data Quality Check**:
   - Verify completion percentages are reasonable (target 44-77% range based on history)
   - Check all 7 divisions reporting
   - Confirm no data gaps or missing metrics

3. **Dashboard Update**:
   - Add Week 8 JSON object to `COMPARISON_DATA.weeks` array
   - Week 8 will auto-display in 4-column grid position 8
   - Update header date range: "1/19 through 2/28/26"

---

## 📞 Support & Resources

### **Getting Help**

**For Dashboard Layout Issues:**
- Refer: [WEEKLY_DASHBOARD_UPDATE_PROCESS.md](./WEEKLY_DASHBOARD_UPDATE_PROCESS.md) - Troubleshooting section

**For Data Extraction Questions:**
- Refer: [DEPENDENCIES-MAP.md - Refresh Guide Dashboard Workflow](../../DEPENDENCIES-MAP.md#-refresh-guide-dashboard-workflow)
- Contact: BigQuery Data Engineering

**For System Architecture Questions:**
- Refer: [KNOWLEDGE_HUB.md - Refresh Guide Dashboard Section](../../KNOWLEDGE_HUB.md#-refresh-guide---store-refresh-dashboard)

**For Code Puppy Pages Deployment:**
- Contact: Platform Team

### **Related Documentation by Topic**

**Data & BigQuery:**
- [WEEKLY_DASHBOARD_UPDATE_PROCESS.md - Data Sources](./WEEKLY_DASHBOARD_UPDATE_PROCESS.md#-data-sources)
- [DEPENDENCIES-MAP.md - File Dependencies](../../DEPENDENCIES-MAP.md#-refresh-guide-dashboard-workflow)

**Dashboard Rendering:**
- [WEEKLY_DASHBOARD_UPDATE_PROCESS.md - Technical Details](./WEEKLY_DASHBOARD_UPDATE_PROCESS.md#-technical-details)
- [business-overview-comparison-dashboard-2-23-26.html](./business-overview-comparison-dashboard-2-23-26.html)

**Process & Procedures:**
- [WEEKLY_DASHBOARD_UPDATE_PROCESS.md - Complete SOP](./WEEKLY_DASHBOARD_UPDATE_PROCESS.md)
- [DEPENDENCIES-MAP.md - Process Timeline](../../DEPENDENCIES-MAP.md#-refresh-guide-dashboard-workflow)

---

## 🗂️ Refresh Guide Project Structure

```
Store Support/Projects/Refresh Guide/
├── 📘 REFRESH_GUIDE_KNOWLEDGE_BASE.md ← YOU ARE HERE
├── 📘 WEEKLY_DASHBOARD_UPDATE_PROCESS.md
├── 📊 business-overview-comparison-dashboard-2-23-26.html (PRODUCTION)
├── 📊 business-overview-dashboard-v3-2-23-26.html (Main dashboard - blocked)
├── 🐍 extract_week7_data.py
├── 🐍 query_bigquery.py
├── 📄 WEEKLY_USER_ENGAGEMENT_ANALYSIS.md
├── 📄 README.md
└── 📁 data/ (output files)
    └── v3-user-engagement-data.json

✅ = Production Ready | ⏳ = Pending | ⚠️ = Needs Review
```

---

## 📋 Index of Key Concepts

### **Metrics & Calculations**

- **Completion %**: (totalCompletedItems / totalPossibleItems) × 100
- **Week-to-Week Change**: Current Week % - Previous Week %
- **Growth Badge**: Shows % change, colored by direction
- **Per-Division Stats**: Division completed / Division max possible

### **Data Hierarchy**

```
COMPARISON_DATA
├── weeks[] (array of 7 week objects)
│   ├── week (1-7)
│   ├── date (MM/DD/YY)
│   ├── label (Week X)
│   ├── summary (overall metrics)
│   ├── divisionStats[] (7 divisions)
│   ├── formatStats[] (SC, NHM, DIV1)
│   ├── areaStats[] (8 areas)
│   └── userEngagement (user metrics)
```

### **Grid Layout**

- **Trend Chart**: 4-column grid (auto-wrap, 2 rows for 8 weeks)
- **User Engagement**: 4-column grid (auto-wrap, 2 rows for 8 weeks)
- **Division Comparison**: 1 label column + 7 week columns (stays on single row)
- **Area Comparison**: 1 label column + 7 week columns (stays on single row)

---

## 🔐 Data Security & Compliance

**Data Classification**: Business Sensitive  
**Location**: Embedded in HTML file  
**Access**: Code Puppy Pages (requires platform authentication)  
**Retention**: Keep current + 12 weeks historical  
**Backup**: GitHub repository (versioned)

For complete compliance info, see [DATA-CLASSIFICATION-ASSESSMENT.md](../../DATA-CLASSIFICATION-ASSESSMENT.md)

---

**Version**: 1.0  
**Last Updated**: February 24, 2026  
**Next Review**: March 3, 2026 (Post-Week 8 Update)
