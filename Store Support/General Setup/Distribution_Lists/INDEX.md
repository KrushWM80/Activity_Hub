# Distribution Lists - Folder Organization

**Last Updated:** January 16, 2026

---

## 📋 Quick Reference

### Active Files (Root)
These are the primary working files for HNMeeting2 distribution list management:

| File | Purpose | Records |
|------|---------|---------|
| **HN_MEMBERS_WITH_CATEGORIES.csv** | Master categorization of all 1,236 HN members | 1,236 |
| **SECONDARY_AUDIENCES_WITH_JOB_CODES.csv** | Secondary audience members ready for DL creation | 785 |
| **CRYSTAL_CLEAR_SUMMARY.md** | Executive summary with complete breakdown | — |
| **NOT_ON_COMMS_DL_COMPLETE_LIST.md** | Detailed list of 804 members not on Comms DL | 804 |
| **EMAIL_SUMMARY_HNMEETING2_ANALYSIS.md** | Email template for stakeholder communication | — |

---

## 📁 Folder Structure

### `00_ACTIVE_LISTS/` 
**Status:** Ready for implementation
- Primary and secondary audience distribution lists
- Prepared member lists for each role/level

### `01_ANALYSIS_REPORTS/`
**Status:** Reference & reporting
- Executive briefs and audience analysis
- Comparison tables and detailed breakdowns
- Final status reports

### `02_SCRIPTS_AND_TOOLS/`
**Status:** Supporting utilities
- PowerShell scripts for AD operations
- Python extraction and analysis tools
- API connectors and data processors

### `03_SOURCE_DATA/`
**Status:** Reference data
- Azure AD Comms DL extracts (6 files)
- Workday HR extracts with hierarchy
- Latest snapshots of source systems

### `04_REFERENCE_DOCS/`
**Status:** Documentation & guides
- Architecture diagrams
- Setup guides and implementation notes
- Integration documentation

### `archive/`
**Status:** Historical & old versions
- `archive/` — Current archive
- `archive/OLD_ANALYSIS/` — Previous analysis versions and duplicates

---

## 📊 Summary Statistics

**HNMeeting2 Total:** 1,236 members
- **On Comms DL List:** 432 (35%)
  - Market Managers: 402
  - Regional Gen Managers: 30
- **NOT On Comms DL List:** 804 (65%)
  - With Job Codes (ready for Phase 1): 785
  - Without Job Codes (need investigation): 19

---

## 🚀 Implementation Phases

### Phase 1: Create Secondary Audience Distribution Lists
**Members:** 785 with complete job code data
**Files Needed:** `SECONDARY_AUDIENCES_WITH_JOB_CODES.csv`
**Status:** ✅ Ready to execute

### Phase 2: Create Exceptions DL
**Members:** 3 special members on existing DLs
**Files Needed:** `NOT_ON_COMMS_DL_COMPLETE_LIST.md` (Section: Without Job Codes)
**Status:** ⏳ After Phase 1

### Phase 3: Verify Missing Job Codes
**Members:** 16 requiring Workday verification
**Status:** 🔍 Concurrent with Phase 2

---

## 📄 File Reference Guide

### Categorization & Analysis
- `CRYSTAL_CLEAR_SUMMARY.md` — Best starting point for understanding the breakdown
- `AUDIENCE_COMPARISON_TABLE.md` — Side-by-side comparison of on/off DL members
- `EXECUTIVE_BRIEF.md` — Formal executive summary

### Member Lists
- `SECONDARY_AUDIENCES_WITH_JOB_CODES.csv` — Ready for bulk import (785 members)
- `NOT_ON_COMMS_DL_COMPLETE_LIST.md` — Complete list with details (804 members)
- `SECONDARY_AUDIENCES_DETAILED_BY_JOBCODE.md` — Organized by 394 unique job codes

### Communication
- `EMAIL_SUMMARY_HNMEETING2_ANALYSIS.md` — Ready-to-send email template

### Source Data
- `HNMeeting2_With_Hierarchy_20251219_115704.csv` — Latest Workday HR snapshot
- `U.S. Comm - All MMs.csv` — Market Managers from AD (402 members)
- `U.S. Comm - All RGM.csv` — Regional Gen Managers from AD (30 members)
- `All US Stores AP MAPMs.csv` — Secondary DL source
- `All US Stores AP RAPDs.csv` — Secondary DL source
- `WMUS_Store_MarketPeoplePartners.csv` — Secondary DL source
- `WMUS_Store_RegionalPeoplePartners.csv` — Secondary DL source

---

## ⚙️ Tools & Scripts

Located in `02_SCRIPTS_AND_TOOLS/`:
- PowerShell scripts for AD group member extraction
- Python utilities for data analysis and transformation
- BigQuery integration and data upload tools

---

## 🔄 Workflow

```
1. Review CRYSTAL_CLEAR_SUMMARY.md → Understand the breakdown
2. Send EMAIL_SUMMARY_HNMEETING2_ANALYSIS.md → Stakeholder communication
3. Execute Phase 1 → Use SECONDARY_AUDIENCES_WITH_JOB_CODES.csv
4. Execute Phase 2 → Use NOT_ON_COMMS_DL_COMPLETE_LIST.md
5. Execute Phase 3 → Verify 16 missing members
```

---

## 📞 Next Steps

1. **Review:** Start with `CRYSTAL_CLEAR_SUMMARY.md`
2. **Communicate:** Send `EMAIL_SUMMARY_HNMEETING2_ANALYSIS.md` to stakeholders
3. **Implement:** Follow phases in `NOT_ON_COMMS_DL_COMPLETE_LIST.md`
4. **Reference:** Use `SECONDARY_AUDIENCES_DETAILED_BY_JOBCODE.md` for job code details

---

**Status:** ✅ Cleaned and organized January 16, 2026
