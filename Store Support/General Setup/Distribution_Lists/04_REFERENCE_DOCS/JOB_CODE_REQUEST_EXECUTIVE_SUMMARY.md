# JOB CODE REQUEST EXECUTIVE SUMMARY

**Date:** January 16, 2026  
**Status:** READY FOR HANDOFF TO DATA TEAM  
**Action:** Extract job codes for 801 secondary audience members

---

## THE GAP: What We Know vs. What We Need

### COMPLETE ✅

```
MARKET MANAGERS (402 members)
├─ Job Code: US-100015099 ✅
├─ Job Title: Market Manager ✅
├─ On New DL: U.S. Comm - All MMs ✅
└─ Status: COMPLETE - Ready to add 68 new members

SENIOR DIRECTORS (30 members on HN)
├─ Primary Job Codes Known: 6 ✅
│  ├─ US-100017446 (Merchandising)
│  ├─ US-100019721 (Merchandising Operations)
│  ├─ US-100020695 (Operations)
│  ├─ US-100019946 (Supply Chain)
│  ├─ US-100022540 (Product Management)
│  └─ US-100022319 (Data Science)
├─ On New DL: U.S. Comm - All RGM ✅
└─ Status: PARTIAL - 30 found, 7 pending, 317 missing
```

---

### INCOMPLETE ❌

```
SECONDARY AUDIENCES (801 members NOT on new DLs)

1. GROUP DIRECTORS (~163)
   ├─ Job Code: ❌ UNKNOWN
   ├─ Job Codes Expected: ~10-15 unique codes
   └─ Status: AWAITING DATA

2. VICE PRESIDENTS (~296)
   ├─ Levels: VP, SVP, EVP
   ├─ Job Codes Expected: ~20+ unique codes
   └─ Status: AWAITING DATA

3. REGIONAL/FUNCTIONAL DIRECTORS (~163)
   ├─ Job Code: ❌ UNKNOWN
   ├─ Job Codes Expected: ~25-30 unique codes
   └─ Status: AWAITING DATA

4. OTHER MANAGERS & SPECIALISTS (~44)
   ├─ Job Code: ❌ UNKNOWN
   ├─ Job Codes Expected: ~10-15 unique codes
   └─ Status: AWAITING DATA

5. UNCLASSIFIED (~175)
   ├─ Job Title: ❌ UNKNOWN
   ├─ Job Code: ❌ UNKNOWN
   ├─ Department: ❌ UNKNOWN
   └─ Status: REQUIRES FULL INVESTIGATION
```

---

## WHAT WE NEED TO REQUEST

**To:** HR/People Analytics/Workday Team  
**From:** Distribution List Analysis  
**Date Needed:** ASAP (critical for DL strategy)

### THE REQUEST

**Extract from Workday for these 801 employees (emails listed in HN_MEMBERS_WITH_CATEGORIES.csv):**

```
Columns Needed:
├─ Email ✓
├─ Job Code ❌ NEED THIS
├─ Job Title ❌ NEED THIS
├─ Department ❌ NEED THIS
├─ Management Level ❌ NEED THIS
├─ Function/Division ❌ NEED THIS
└─ Current Manager ← Nice to have
```

---

## DISTRIBUTION BY MISSING JOB CODES

### What Job Codes Don't Exist for These People:

**Group Directors - Expected Job Codes:**
```
❓ Group Director, Supply Chain Management (14 people)
❓ Group Director, Operations (11 people)
❓ Group Director, Product Management (9 people)
❓ Group Director, Data Science (?)
❓ Group Director, Technology (?)
❓ Group Director, Automation (?)
❓ Group Director, [Other roles] (?)
```

**Vice Presidents - Expected Job Codes:**
```
❓ Vice President, Supply Chain (?)
❓ Vice President, Store Operations (?)
❓ Vice President, Merchandising (?)
❓ Vice President, Technology (?)
❓ Vice President, Finance (?)
❓ Vice President, Strategy (?)
❓ Vice President, Human Resources (?)
❓ Divisional Vice President, Supply Chain (?)
❓ Divisional Vice President, Operations (?)
❓ Senior Vice President, [Function] (?)
❓ Executive Vice President, [Function] (?)
```

**Regional/Functional Directors - Expected Job Codes:**
```
❓ Director, Regional Asset Protection (10 people)
❓ Emerging Market Manager (7 people)
❓ Director, Store Planning (?)
❓ Director, Real Estate (?)
❓ Director, Supply Chain Planning (?)
❓ Director, Regional Store Operations (?)
❓ Director, Distribution Center Operations (?)
❓ Director, Loss Prevention (?)
❓ [Many other director roles...]
```

**Other Managers - Expected Job Codes:**
```
❓ Manager, Store Operations
❓ Manager, Regional Operations
❓ Manager, Supply Chain
❓ Operations Coordinator
❓ [Other manager roles...]
```

---

## THE DATA COLLECTION PROCESS

### Step 1: Provide to Data Team
```
📄 Files to Send:
├─ HN_MEMBERS_WITH_CATEGORIES.csv (contains 801 emails)
├─ JOB_CODE_REQUEST_SECONDARY_AUDIENCES.md (explains what's needed)
└─ JOB_CODE_COLLECTION_TEMPLATE.csv (expected output format)
```

### Step 2: They Extract Data
```
🔍 From Workday System:
├─ Filter: Email IN [801_emails_from_HN]
├─ Extract: JobCode, JobTitle, Department, Management Level
└─ Export: CSV with template format
```

### Step 3: Validation
```
✓ Verify all 801 records returned
✓ Check job codes are valid Workday codes
✓ Ensure no duplicates
✓ Match emails to HN list
```

### Step 4: Analysis
```
📊 Categorize:
├─ By Job Code (identify unique codes)
├─ By Management Level (VP/C/B/A)
├─ By Function (Supply Chain, Ops, etc.)
└─ By Division (Global Tech, Stores, etc.)
```

### Step 5: DL Creation
```
📋 Create New DLs:
├─ Group Directors DL (163)
├─ Vice Presidents DL (296)
├─ Regional Directors DL (163)
├─ Managers & Specialists DL (44)
└─ [Classified members]
```

---

## URGENCY & IMPACT

### Why This Matters
- 801 members (65% of HN) are NOT on new distribution lists
- No job code information means we can't properly categorize them
- Can't create targeted DLs without knowing roles
- Can't make governance decisions without role clarity

### Impact if Data NOT Provided
- ❌ Can't add new members to HNMeeting2
- ❌ Can't create secondary audience DLs
- ❌ Can't align organizational structure
- ❌ Can't ensure proper communications routing

### Impact if Data IS Provided
- ✅ Complete HN membership categorization
- ✅ Clear governance by job code and level
- ✅ Ability to create targeted DLs
- ✅ Organizational alignment verified
- ✅ Ready for distribution list updates

---

## HANDOFF CHECKLIST

**Send to Data Team:**
- [ ] HN_MEMBERS_WITH_CATEGORIES.csv (contains 801 emails in "Not on Any New DL" category)
- [ ] JOB_CODE_REQUEST_SECONDARY_AUDIENCES.md (full details)
- [ ] JOB_CODE_SUMMARY_MISSING.md (what's missing)
- [ ] JOB_CODE_COLLECTION_TEMPLATE.csv (expected format)
- [ ] This document (executive summary)

**Request Timeline:**
- [ ] Submission: This week
- [ ] Expected Return: Within 5 business days
- [ ] Validation: 2 business days
- [ ] Analysis: Following week
- [ ] DL Creation: Within 2 weeks

---

## CURRENT STATUS BY AUDIENCE

| Audience | Members | HN Count | New DL | Job Codes | Status |
|----------|---------|----------|--------|-----------|--------|
| Market Managers | 402 | 402 | YES | ✅ Complete | READY |
| Senior Directors | 30 | 30 | YES | ✅ Partial | READY |
| Group Directors | 163 | ~163 | NO | ❌ Missing | ⏳ HOLD |
| Vice Presidents | 296 | ~296 | NO | ❌ Missing | ⏳ HOLD |
| Regional Directors | 163 | ~163 | NO | ❌ Missing | ⏳ HOLD |
| Managers/Specialists | 44 | ~44 | NO | ❌ Missing | ⏳ HOLD |
| Unclassified | 175 | ~175 | NO | ❌ Unknown | ⏳ HOLD |
| **TOTAL** | **1,236** | | | | |

---

## IMMEDIATE ACTIONS

### ✅ Ready Now (No data needed)
1. Add 68 new Market Managers (NEW_68_MEMBERS_TO_ADD.csv ready)
2. Validate existing 402 Market Managers ✓
3. Review existing 30 Senior Directors ✓

### ⏳ Waiting on Data
4. Categorize 163 Group Directors (need job codes)
5. Categorize 296 Vice Presidents (need job codes)
6. Categorize 163 Regional Directors (need job codes)
7. Categorize 44 Managers/Specialists (need job codes)
8. Classify 175 Unclassified members (need full data)

### After Data Received
9. Create new DL strategy documents
10. Create/update distribution lists
11. Add members to appropriate lists
12. Test and validate

---

## SUMMARY

**Total Members Needing Job Codes:** 801  
**Total Job Codes to Identify:** ~75-100+ unique codes  
**Data Status:** AWAITING EXTRACTION FROM WORKDAY  
**Estimated Timeline to Complete:** 3-4 weeks once data is provided  
**Next Step:** Provide files to HR/Workday team with data extraction request

