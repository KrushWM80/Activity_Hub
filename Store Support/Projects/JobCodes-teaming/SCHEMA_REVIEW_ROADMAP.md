# JobCodes Dashboard - Data Join Strategy
## Updated April 9, 2026

---

## SCHEMA ANALYZED - KEY FINDINGS

### 1. POLARIS: `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`

**✅ CONFIRMED:** Single field `job_code` (SMART format)
- Format: `1-995-710`, `1-990-7410`, etc.
- NOT decomposed into div/dept/code
- Job name EMBEDS code: "Maint Assoc ON 1-995-710"
- Pattern: `{Title} {code}`

**Key Columns (from Sample Data):**
- `job_code` - Authority source (271 codes)
- `job_nm` - Embedded format
- `worker_id` - Numeric (e.g., 506448534)
- `worker_payment_type` - H (Hourly) / P (Part-time)
- `location_id`, `location_nm` - Store assignment
- `shift_id` - Shift details

---

### 2. COREHR: `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`

**✅ CONFIRMED:** Nested JSON structure
- `jobCode` is in `employmentInfo.positionInfoHistory[]` array
- **CRITICAL:** Uses Workday format, NOT SMART format
  - Example: `US-01-0990-007410` (NOT `1-990-7410`)
  - This is a MISMATCH with Polaris codes!
- Multiple positions per employee (employment history)
- Requires JSON unnesting

**Key Fields (from nested positionInfoHistory):**
- `jobCode` - Workday format (⚠️ Different from Polaris SMART)
- `jobFamilyID` - e.g., "Global_JF_Operations_Management"
- `managementLevelID` - e.g., "IND_CONTR", "SI_CONTR"
- `positionTitle` - Job title text
- `storeName`, `storeNumber` - Location
- `jobEffectiveDate`, `jobEndDate` - Employment period

**User Identification:**
- `userID` - Workday user ID (format: e.g., "e0c0l5x.s03935", alphanumeric)
- `employeeID` - Employee number

---

### 3. TMS DATA: `TMS Data (3).xlsx` (Already Examined)

**✅ CONFIRMED:** Single field `jobCode` (SMART format, matches Polaris)
- Format: Matches Polaris `job_code`
- 492 records
- 21 columns

**TMS-Only Data (use as-is):**
```
✓ teamName, teamId           ← Teaming data
✓ baseDivisionCode, bannerCode
✓ merchDeptNumbers
✓ tlJobCode, tlJobTitle, tlDeptNumber, tlDivNumber  ← Team Lead info
✓ slJobCode, slDeptNumber, slDivNumber, slJobTitle  ← Store Lead info
```

---

## CRITICAL ISSUE: CODE FORMAT MISMATCH

**Problem:** CoreHR stores Workday codes, but Polaris uses SMART codes

| System | Format | Example |
|--------|--------|---------|
| **Polaris** | SMART | `1-990-7410` |
| **CoreHR** | Workday | `US-01-0990-007410` |
| **Excel** | BOTH | Has both columns for mapping |
| **TMS** | SMART | `1-990-7410` |

**Solution:** Excel master file has both formats as bridge
- Use Excel mapping: SMART ↔ Workday if CoreHR linkage needed
- For now: Focus on Polaris + Excel + TMS (skip CoreHR code join)
- Option: Query CoreHR for user/role data separately if needed

---

## CREATED: BigQuery Extraction Scripts

### File 1: `query_polaris_jobcodes.py`
**Execute to extract Polaris data:**
```python
# Queries: vw_polaris_current_schedule
# Returns: 271 distinct job codes with worker/location context
# Output: polaris_job_codes_extracted.csv
```

### File 2: `query_corehr_jobcodes.py`
**Execute to extract CoreHR data:**
```python
# Queries: UNIFIED_PROFILE_SENSITIVE_VW with JSON unnesting
# Handles: Nested positionInfoHistory arrays
# Note: Uses Workday codes (US-01-XXXX-XXXXXX format)
# Output: corehr_job_codes_extracted.csv
```

### File 3: `join_engine.py`
**Orchestrates complete join pipeline:**
```python
# Step 1: Load Polaris (authority - 271 codes)
# Step 2: LEFT JOIN Excel enrichment (864 records)
# Step 3: LEFT JOIN TMS organizational data (492 records)
# Output: enriched_job_codes.csv + SQLite database table
```

---

## DATA JOIN STRATEGY (IMPLEMENTED)

```
┌──────────────────────────────────────────────────────────────────┐
│ STEP 1: Query ALL Polaris Job Codes (271 records)                │
│ Source: polaris-analytics-prod.us_walmart.vw_polaris_...         │
│ Columns: job_code, job_title, user_id, role, role_type,          │
│          workgroup_id, workgroup_name, div, dept, access_level   │
└──────────────────────────────────────────────────────────────────┘
                              ⬇
┌──────────────────────────────────────────────────────────────────┐
│ STEP 2: LEFT JOIN Job_Code_Master_Table.xlsx                     │
│ Match Key: Polaris job_code = Excel SMART Job Code               │
│ Add: Category, Job Family, PG Level, Team, Workgroup, Supervisor │
│      Reports To, etc. (50 columns available)                     │
│ If no match: Leave columns BLANK                                 │
└──────────────────────────────────────────────────────────────────┘
                              ⬇
┌──────────────────────────────────────────────────────────────────┐
│ STEP 3: LEFT JOIN TMS_Data (3).xlsx                              │
│ Match Key: Polaris job_code = TMS jobCode                        │
│ Add: teamName, teamId, baseDivisionCode, bannerCode,             │
│      merchDeptNumbers, tlJobCode, tlJobTitle,                    │
│      slJobCode, slDeptNumber, slDivNumber, slJobTitle            │
│ If no match: Leave columns BLANK → Mark as "Missing Teaming"    │
└──────────────────────────────────────────────────────────────────┘
                              ⬇
┌──────────────────────────────────────────────────────────────────┐
│ STEP 4: (OPTIONAL) LEFT JOIN CoreHR if needed                    │
│ Match Key: Polaris user_id = CoreHR user_id (if available)       │
│ Add: Additional role/role_type data if CoreHR has better data    │
│ Leave BLANK if CoreHR doesn't enhance Polaris                    │
└──────────────────────────────────────────────────────────────────┘
                              ⬇
┌──────────────────────────────────────────────────────────────────┐
│ RESULT: Complete JobCodes Master Dataset                         │
│ ✓ 271 Polaris codes (all of them)                                │
│ ✓ Enrichment data (where available in Excel)                     │
│ ✓ Teaming data (where available in TMS)                          │
│ ✓ BLANK columns for team to review & update                      │
│ ✓ "Missing Teaming Data" flagged for manual addition             │
└──────────────────────────────────────────────────────────────────┘
```

---

## WHAT WE KNOW vs WHAT WE NEED

### ✅ Already Confirmed:
- Job codes in Polaris: 271 SMART codes
- Job_Code_Master_Table.xlsx: 864 records, 50 columns (enrichment)
- TMS_Data(3).xlsx: 492 rows, 21 columns (teaming)
- TMS has specific team/teaming data we need
- TMS breaks job codes into div/dept/code

### ❓ Need to Confirm (Schema Review):
- Polaris job code field structure (format of "1-202-2104")
- Does Polaris break into div/dept/code or store as single field?
- Polaris columns: user_id, role, role_type, workgroup fields
- CoreHR linkage to job codes (if any)
- CoreHR columns: user_id, role, role_type

---

## ACTION ITEMS FOR YOU

**Priority 1: Confirm Schema**
- [ ] Provide sample Polaris data (5-10 rows showing all columns)
- [ ] Provide sample CoreHR data (5-10 rows showing format)
- [ ] Confirm job code format/structure
- [ ] Fill in schema template below

**Priority 2: Provide Access**
- [ ] Can I query Polaris directly, or do you need to export data?
- [ ] Same for CoreHR?
- [ ] BigQuery credentials available?

**Priority 3: Implementation**
- [ ] Once schema confirmed, I'll write Python scripts to:
  - Query Polaris
  - Query CoreHR (if needed)
  - Load Excel and TMS data
  - Execute full joins
  - Generate final enriched dataset
  - Mark blanks as "Review Needed"

---

## SCHEMA CONFIRMATION TEMPLATE

**Fill this in once you review the schemas:**

```
POLARIS STRUCTURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Job Code Representation:
  ☐ Single field: [column name] = "1-202-2104"
  ☐ Three fields: div=[col], dept=[col], code=[col]
  
Key Columns:
  Job Code: ________________
  Job Title: ________________
  User ID: ________________
  Role: ________________
  Role Type: ________________
  Workgroup ID: ________________
  Workgroup Name: ________________
  Access Level/Pay Type: ________________
  Other key columns: ________________

COREHR STRUCTURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  User ID: ________________
  Role: ________________
  Role Type: ________________
  Job Code Link: ________________ (if exists)
  Other relevant: ________________
  
Notes: ________________

CONFIRMATION:
  Does Polaris job_code match TMS jobCode format? ☐ Yes ☐ No ☐ Partial
  Need special logic to join div/dept/code? ☐ Yes ☐ No
  Ready to write queries? ☐ Yes, I have access ☐ Export data first
```

