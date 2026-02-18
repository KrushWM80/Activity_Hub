# Comprehensive HNMeeting2 Audience Summary

**Created:** January 16, 2026  
**Total HN Members:** 1,236  
**Analysis Date:** Based on latest data refresh

---

## EXECUTIVE SUMMARY

### Overall Status
- **Total HNMeeting2 Members:** 1,236
- **On Comms DL List:** 432 (35%)
- **NOT on Comms DL List:** 804 (65%)
  - With Job Codes Found: 785 (97.6%)
  - Missing (Need Investigation): 19 (2.4%)

### Categorization
| Category | Count | Status |
|----------|-------|--------|
| On Comms DL List | 432 | ✅ Complete |
| Not on Comms DL List | 801 | ✅ 785 with Job Codes |
| On Specialized DLs Only | 3 | ℹ️ Separate handling |

---

## PRIMARY AUDIENCES (ON COMMS DL LIST) - 432 Members

### Market Managers (MMs)
- **DL Source:** U.S. Comm - All MMs.csv
- **Count:** 470 members on list
- **HN Members:** ~402 overlap with HNMeeting2
- **Status:** ✅ ON Comms DL List

### Regional General Managers (RGMs)
- **DL Source:** U.S. Comm - All RGM.csv
- **Count:** 37 members on list
- **HN Members:** ~30 overlap with HNMeeting2
- **Status:** ✅ ON Comms DL List

### Other Comms DL Members
- **Additional Members:** ~30 (Area Market People Partners, Store People Partners, etc.)
- **Status:** ✅ ON Comms DL List

**Primary Audience Total: 432 members**

---

## SECONDARY AUDIENCES (NOT ON COMMS DL LIST) - 801+ Members

These are employees in HNMeeting2 who are NOT on any Comms DL List but need communication access.

### By Management Level

| Level | Title | Count | Status |
|-------|-------|-------|--------|
| VP | Vice President | ~50 | ✅ Job Codes Found |
| C | Group Director | ~160 | ✅ Job Codes Found |
| D | Senior Director | ~130 | ✅ Job Codes Found |
| E | Field Level/Manager | ~350 | ✅ Job Codes Found |
| B | Director | ~65 | ✅ Job Codes Found |
| F | Other Specialists | ~30 | ✅ Job Codes Found |

### By Primary Role (Top 15)

| Job Title | Count | Job Code Examples |
|-----------|-------|-------------------|
| Senior Director, Merchandising Operations | 27 | US-100019721 |
| Senior Director, Merchandising | 26 | US-100017446 |
| Senior Director, Supply Chain Management | 16 | US-100019946 |
| Senior Director, Technology Operations | 14 | (Various) |
| Senior Director, Operations | 13 | US-100020695 |
| Senior Director, Product Management | 13 | US-100022540 |
| Group Director, Supply Chain Management | 13 | US-100019949 |
| Senior Director, Advanced Analytics | 12 | US-100022602 |
| Senior Director, Real Estate | 12 | (Various) |
| Senior Director, Product Development | 10 | (Various) |
| Senior Director, Data Science | 9 | US-100022319 |
| Senior Director, Operations | 9 | (Various) |
| Director, Regional Asset Protection | 9 | US-100024103 |
| Senior Director, Data Science (USA) | 9 | (Various) |
| Senior Director, Business Strategy | 7 | US-100020346 |

**Secondary Audience Total: 785 members with job codes + 16 missing**

---

## THREE-PART BREAKDOWN SUMMARY

### 1. PRIMARY AUDIENCES (ON COMMS DL LIST)
✅ **432 Members** - Complete, no action needed

**These are:**
- Market Managers (402)
- Regional General Managers (30)

**Located in:**
- U.S. Comm - All MMs.csv
- U.S. Comm - All RGM.csv
- All US Stores AP MAPMs.csv
- All US Stores AP RAPDs.csv
- WMUS_Store_MarketPeoplePartners.csv
- WMUS_Store_RegionalPeoplePartners.csv

---

### 2. SECONDARY AUDIENCES (NOT ON COMMS DL LIST - WITH JOB CODES)
✅ **785 Members** - Ready for DL creation

**These are:**
- Vice Presidents (~50)
- Group Directors (~160)
- Senior Directors (~130)
- Directors (~65)
- Field Managers/Specialists (~380)

**Data File:** SECONDARY_AUDIENCES_WITH_JOB_CODES.csv

**What We Have:**
- Email
- First Name / Last Name
- Job Code (Workday)
- Job Title (Workday)
- Department
- Cost Center
- Management Level

---

### 3. UNIDENTIFIED MEMBERS (NEED INVESTIGATION)
❌ **19 Members** - Missing Job Codes

These are HNMeeting2 members NOT on Comms DL List AND not found in job code source file.

**Likely Reasons:**
- New hires (after Dec 19, 2025)
- Recently removed/transferred
- Workday record issues

**Action Required:**
- Verify employment status
- Check if still needed for HNMeeting2
- Obtain job codes if active

---

## DATA QUALITY & SOURCING

### Primary Data Sources
1. **HNMeeting2_With_Hierarchy_20251219_115704.csv**
   - Source: Workday HR system
   - Records: 1,246 employees
   - Lookup Size: 1,219 valid entries
   - Contains: Job codes, titles, departments, management levels

2. **Comms DL List (6 CSV Files)**
   - Source: Azure AD
   - Total Members: 1,061 unique emails across all 6 files
   - Contains: Email addresses only (no job codes)

3. **HN_MEMBERS_WITH_CATEGORIES.csv**
   - Records: 1,236 HNMeeting2 members
   - Categories: On DL / Not on DL / Exception DLs

### Data Matching Results
- **Total Secondary Audience Members:** 801 (after excluding 3 on specialized DLs)
- **Matched:** 785 (98.1%)
- **Missing:** 16 (1.9%)

**Match Method:** Email address cross-reference between HNMeeting2 and Workday hierarchy file

---

## NEXT STEPS

### Phase 1: Distribution List Creation (Ready Now)
Create new DLs for secondary audiences using SECONDARY_AUDIENCES_WITH_JOB_CODES.csv

**Example DL Structure:**
- DL-Secondary-VicePresidents (50 members)
- DL-Secondary-GroupDirectors (160 members)
- DL-Secondary-SeniorDirectors (130 members)
- DL-Secondary-Directors-Other (65 members)
- DL-Secondary-Managers-Specialists (380 members)

### Phase 2: Identify Missing 19 Members
- Review employment records
- Check Workday for updates
- Obtain missing job codes if still active

### Phase 3: Automate Maintenance
- Create job code-based inclusion criteria
- Set up monthly refresh to catch new hires
- Establish governance for DL membership

---

## KEY METRICS

| Metric | Value |
|--------|-------|
| **Total HN Members** | 1,236 |
| **On Comms DL** | 432 (35%) |
| **Not on Comms DL** | 804 (65%) |
| **With Job Codes** | 785 (97.6% of secondary) |
| **Missing Job Codes** | 19 (2.4% of secondary) |
| **Unique Job Codes** | 394 |
| **Management Levels** | 11 types |
| **Time to Complete** | 2 hours vs 2 weeks |

---

## FILE LOCATIONS

**Analysis Files:**
- COMPREHENSIVE_AUDIENCE_SUMMARY.md (this file)
- SECONDARY_AUDIENCES_WITH_JOB_CODES.csv
- SOLUTION_SUMMARY_JOB_CODES_FOUND.md

**Source Files:**
- HN_MEMBERS_WITH_CATEGORIES.csv
- HNMeeting2_With_Hierarchy_20251219_115704.csv

**Comms DL List Files:**
- U.S. Comm - All MMs.csv
- U.S. Comm - All RGM.csv
- All US Stores AP MAPMs.csv
- All US Stores AP RAPDs.csv
- WMUS_Store_MarketPeoplePartners.csv
- WMUS_Store_RegionalPeoplePartners.csv

---

## QUICK REFERENCE: WHO IS WHO

### If they're in HNMeeting2 AND on a Comms DL List
✅ **Status:** Primary audience - already communicated to  
**Action:** None needed

### If they're in HNMeeting2 but NOT on any Comms DL List AND we have their job code
✅ **Status:** Secondary audience - need new DL  
**Action:** Add to appropriate secondary DL based on job code/role  
**Resources:** SECONDARY_AUDIENCES_WITH_JOB_CODES.csv

### If they're in HNMeeting2 but NOT on any Comms DL List AND we DON'T have their job code
❌ **Status:** Unidentified - need investigation  
**Action:** Verify employment and obtain job code  
**Resources:** Check Workday for recent changes
