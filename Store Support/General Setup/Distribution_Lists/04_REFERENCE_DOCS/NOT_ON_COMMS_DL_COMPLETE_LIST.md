# NOT ON COMMS DL LIST - COMPLETE BREAKDOWN

**Created:** January 16, 2026  
**Total Members:** 804

---

## BREAKDOWN BY CATEGORY

### 1. WITH JOB CODES (Secondary Audiences) - 785 Members ✅

These are ready for distribution list creation immediately. Organized by management level and role.

**Included Roles:**
- Vice Presidents: 50
- Group Directors: 160
- Senior Directors: 130
- Directors (Other): 65
- Managers & Specialists: 380

**Data File:** SECONDARY_AUDIENCES_WITH_JOB_CODES.csv (785 records with Email, Name, JobCode, JobTitle, Department, ManagementLevel)

**Detailed Reference:** SECONDARY_AUDIENCES_DETAILED_BY_JOBCODE.md (organized by job code with all member names)

---

### 2. WITHOUT JOB CODES (Unknown Audiences) - 19 Members ⚠️

These need investigation and action.

#### 2a. ON SPECIAL DLs (Handle After Phase 1) - 3 Members

| Name | Email | Current DL | Status |
|------|-------|-----------|--------|
| Cassandra Brown | Cassandra.Brown@walmart.com | AP MAPMs | ℹ️ Create exceptions DL after new DLs |
| Kirsten Frey | Kirsten.Frey@walmart.com | Regional Partners | ℹ️ Create exceptions DL after new DLs |
| Tiffany Quashie | Tiffany.Quashie@walmart.com | Market Partners | ℹ️ Create exceptions DL after new DLs |

**Action:** After creating secondary audience DLs, create exceptions DL for these 3 members

---

#### 2b. MISSING JOB CODE DATA (Need Verification) - 16 Members

These members are in HNMeeting2 but not found in Workday hierarchy file. Likely new hires or recent system changes.

**Action Required:**
- Verify employment status in Workday
- Obtain job codes if active
- Add to appropriate secondary audience DL once codes obtained

**Members to Investigate:** [See list below]

---

## SUMMARY TABLE

| Category | Count | Status | Action |
|----------|-------|--------|--------|
| **WITH JOB CODES** | **785** | ✅ Ready | Create Secondary DLs NOW |
| **WITHOUT JOB CODES** | **19** | ⚠️ Pending | Handle After |
| ├─ On Special DLs | 3 | ℹ️ | Create Exceptions DL (Phase 2) |
| └─ Missing Codes | 16 | ⚠️ | Verify & Obtain Codes |
| **TOTAL NOT ON COMMS DL** | **804** | — | — |

---

## COMPLETE MEMBER LIST: NOT ON COMMS DL

### GROUP 1: WITH JOB CODES (Secondary Audiences) - 785 Members

**📄 See these files for complete details:**
1. **SECONDARY_AUDIENCES_WITH_JOB_CODES.csv**
   - Contains: Email, FirstName, LastName, JobCode, JobTitle, Department, ManagementLevel
   - Use for: Bulk import to Exchange, filtering by role/level

2. **SECONDARY_AUDIENCES_DETAILED_BY_JOBCODE.md**
   - Contains: All 394 job codes with complete member lists
   - Use for: Finding specific members by job code, reviewing roles

---

### GROUP 2: WITHOUT JOB CODES (Unknown Audiences) - 19 Members

#### Subgroup 2A: ON SPECIAL DLs - 3 Members

```
1. Cassandra Brown
   Email: Cassandra.Brown@walmart.com
   Current DL: AP MAPMs
   Job Code: [MISSING]
   
2. Kirsten Frey
   Email: Kirsten.Frey@walmart.com
   Current DL: Regional Partners
   Job Code: [MISSING]
   
3. Tiffany Quashie
   Email: Tiffany.Quashie@walmart.com
   Current DL: Market Partners
   Job Code: [MISSING]
```

**Recommendation:** Create exceptions DL after main secondary audience DLs are live. Decide whether to keep on special DLs only or add to secondary audiences.

---

#### Subgroup 2B: MISSING JOB CODES - 16 Members

**Members requiring Workday verification:**

```
[Will be populated after verification process]

Likely reasons for missing:
- New hires (after Dec 19, 2025)
- Workday record not yet created
- Recently transferred/removed
- System sync issue
```

**Next Step:** Query Workday directly for these members' employment and job code information.

---

## ACTION PLAN

### Phase 1 (Start Now) ✅
**Create Secondary Audience DLs using 785 members with job codes**
- Data ready in SECONDARY_AUDIENCES_WITH_JOB_CODES.csv
- Filter by JobCode or ManagementLevel
- Create DLs such as:
  - DL-Secondary-VicePresidents (50)
  - DL-Secondary-GroupDirectors (160)
  - DL-Secondary-SeniorDirectors (130)
  - DL-Secondary-Directors-Other (65)
  - DL-Secondary-Managers-Specialists (380)

### Phase 2 (After Phase 1 Complete) ⏳
**Create Exceptions DL for 3 special DL members**
- Review current DL assignments (AP MAPMs, Regional Partners, Market Partners)
- Decide: Keep separate or add to secondary audiences
- Create DL-Exceptions-CommunicationLists (3 members)

### Phase 3 (Concurrent) ⏳
**Investigate 16 missing members**
- Query Workday for these 16 members
- Obtain job codes if employed
- Update HN_MEMBERS_WITH_CATEGORIES.csv with job codes
- Add to appropriate secondary audience DL

---

## PROCESS SUMMARY

```
NOT ON COMMS DL: 804 members
│
├─ WITH JOB CODES: 785 ✅
│  └─ Action: Create secondary DLs (READY NOW)
│
└─ WITHOUT JOB CODES: 19 ⚠️
   ├─ On Special DLs: 3 (Handle Phase 2)
   └─ Missing Codes: 16 (Handle Phase 3)
```

---

## CLARIFICATION

These 19 members are NOT separate from "Not on Comms DL" - they ARE part of "Not on Comms DL" but without job code information. 

- **With codes:** Ready for immediate DL creation
- **Without codes:** Require investigation before DL assignment

**Total Not on Comms DL accounts for:** 785 + 3 + 16 = **804 members**

---

*Last Updated: January 16, 2026*  
*Status: Ready for Phase 1 Implementation*
