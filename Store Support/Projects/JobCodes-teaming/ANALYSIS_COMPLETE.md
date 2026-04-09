# SCHEMA ANALYSIS COMPLETE
## Status: Ready for BigQuery Queries

**Date:** April 9, 2026  
**Session Focus:** Analyzed Polaris and CoreHR schemas using user-provided sample data

---

## KEY FINDINGS

### ✅ Polaris Schema (Job Code Authority)
```
Source: polaris-analytics-prod.us_walmart.vw_polaris_current_schedule
Format: Single field job_code (SMART format: 1-XXX-XXX)
Total Codes: 271 distinct
Key Fields:
  - job_code: Authority source (1-995-710)
  - job_nm: Embeds code ("Maint Assoc ON 1-995-710")
  - worker_id: Numeric identifier
  - worker_payment_type: H (Hourly) / P (Part-time)
  - location_id, location_nm: Store assignment
  - shift_id: Scheduling context
```

### ✅ CoreHR Schema (Employment Data)
```
Source: wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW
Structure: NESTED JSON with employment history
Challenge: jobCode uses Workday format (US-01-0990-007410), NOT SMART format
Location: employmentInfo.positionInfoHistory[] array
Key Fields:
  - userID: Workday user identifier (alphanumeric)
  - employeeID: Employee number
  - jobCode: Workday format (different from Polaris!)
  - jobFamilyID: Career classification
  - managementLevelID: Level code
  - Position History: Multiple records per employee
```

### ⚠️ CRITICAL ISSUE IDENTIFIED
**Code Format Mismatch:**
- Polaris stores SMART codes: `1-990-7410`
- CoreHR stores Workday codes: `US-01-0990-007410`
- **Cannot join directly without mapping**
- **Solution:** Excel master file bridges both formats

---

## WHAT WAS CREATED

### 1. Query Scripts (Ready to Execute)

**`query_polaris_jobcodes.py`**
- Extracts 271 distinct job codes from Polaris
- Includes worker counts, locations, payment types
- Output: CSV ready for joining

**`query_corehr_jobcodes.py`**
- Handles nested JSON unnesting from positionInfoHistory
- Extracts employment context (family, level, position)
- Note: Uses Workday codes (different from Polaris)
- Output: CSV for separate analysis or user/role lookup

### 2. Join Engine (`join_engine.py`)

**Three-Stage Pipeline:**
```
Stage 1: Load Polaris (271 SMART codes) - AUTHORITY
          ↓ LEFT JOIN
Stage 2: Load Excel enrichment (864 records, 50+ columns)
          ↓ LEFT JOIN
Stage 3: Load TMS organizational data (492 records)
          ↓
Output: Enriched dataset with all fields preserved for unmatched codes
```

**Features:**
- Normalizes job codes for matching
- Preserves all Polaris codes (LEFT JOIN strategy)
- Handles missing Excel entries (will be NULL)
- Handles missing TMS entries (will be NULL)
- Saves to SQLite database + CSV

### 3. Updated Documentation

**`SCHEMA_REVIEW_ROADMAP.md`** - Updated with:
- Actual column structure from samples
- Format differences identified
- Code mismatch documented
- Solution strategy provided

**`EXECUTION_PLAN.md`** - Created with:
- Step-by-step execution guide
- Prerequisites and dependencies
- Troubleshooting tips
- Success indicators

---

## DATA ARCHITECTURE CONFIRMED

```
                    Polaris (Authority)
                         ↓
                    271 Job Codes (SMART)
                         ↓ LEFT JOIN
                    Excel Enrichment
                  (864 records, 50 columns)
                    - Category
                    - Job Family
                    - PG Level
                    - [50 other fields]
                         ↓ LEFT JOIN
                    TMS Organizational Data
                    (492 records, teaming)
                    - Team Name
                    - Team ID
                    - Division/Banner
                    - Role Hierarchy
                         ↓
                  Enriched Job Code Master
                  (271 records, 100+ columns)
                         ↓
                  SQLite Database
                  (For backend consumption)
                         ↓
              Dashboard API Updates
              (/api/job-codes-master endpoint)
```

---

## NEXT STEPS (IN ORDER)

### 1️⃣ Execute Polaris Query
```bash
cd JobCodes-teaming
python query_polaris_jobcodes.py
# Output: polaris_job_codes_extracted.csv
```

### 2️⃣ Execute Join Engine
```bash
python join_engine.py
# Output: 
#   - enriched_job_codes.csv
#   - Updated jobcodes_cache.db SQLite database
```

### 3️⃣ Update Backend (main.py)
- Modify database sync to load from `enriched_job_codes` table
- Update API response to include new enrichment fields
- Test endpoint with enriched data

### 4️⃣ CoreHR Query (Optional)
- Execute if you need user/role data separate from job codes
- Creates separate user/role mapping dataset
- Can be used for personnel org chart if needed

---

## VALIDATION CHECKLIST

- [✓] Polaris schema analyzed (single job_code field confirmed)
- [✓] CoreHR schema analyzed (nested JSON identified)
- [✓] Code format mismatch documented (SMART vs Workday)
- [✓] Excel bridge identified (has both formats)
- [✓] TMS data confirmed (single jobCode field matches Polaris)
- [✓] Join strategy validated (LEFT JOIN preserves all Polaris codes)
- [✓] Query scripts created and ready
- [✓] Join engine created and ready
- [✓] Documentation updated with findings
- [ ] Polaris query executed
- [ ] Join engine executed
- [ ] Backend updated with enriched data
- [ ] Dashboard tested with new enrichment fields

---

## IMPORTANT NOTES

1. **Polaris is Authority:** All 271 codes MUST appear in output (never discarded)
2. **Excel Format:** Use SMART format `job_code` column for joining with Polaris
3. **CoreHR Timing:** Workday codes can be queried separately if user/role enrichment needed
4. **NULL Handling:** Unmatched enrichment fields will be NULL (expected for ~20-40% of codes)
5. **TMS Coverage:** Expect 60-70% match rate; some job codes not in team structure

---

## FILES CREATED THIS SESSION

```
✓ query_polaris_jobcodes.py      - Polaris extraction query
✓ query_corehr_jobcodes.py       - CoreHR extraction query  
✓ join_engine.py                 - Join orchestration engine
✓ SCHEMA_REVIEW_ROADMAP.md       - Updated with findings
✓ EXECUTION_PLAN.md              - Step-by-step guide
✓ ANALYSIS_COMPLETE.md           - This file
```

---

## AUTHENTICATION REQUIRED

Before executing queries, ensure BigQuery access:
```bash
# Verify authentication
gcloud auth list

# If needed, set credentials
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Test connection
bq query --use_legacy_sql=False 'SELECT 1'
```

---

**Status: READY FOR EXECUTION** ✅

All preparation complete. Ready to run BigQuery extractions and join pipeline.
