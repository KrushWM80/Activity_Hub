"""
CORRECTED ARCHITECTURE: Why We Don't Need Excel Bridge

User's Insight: Job code formats are transformable!
SMART: 1-202-2104      (Div-Dept-Code)
Workday: US-01-0202-002104   (US-0{Div}-{Dept:04d}-{Code:06d})

The transformation is MATHEMATICAL - we can do it in SQL!
"""

# ============================================================================
# PROBLEM WITH ORIGINAL APPROACH (Using Excel Bridge)
# ============================================================================

Original Plan:
  Polaris (SMART codes) 
    → Excel enrichment (has both SMART and Workday codes)
    → TMS data

Issues:
  ✗ We DON'T need Excel just to transform codes
  ✗ Excel isn't the right tool for code format conversion
  ✗ Excel adds complexity: requires loading 864 records just for mapping
  ✗ Excel limits to records that exist in Excel (some Polaris codes might not match)

# ============================================================================
# CORRECTED APPROACH: Direct Transform in BigQuery
# ============================================================================

Architecture:
  
  Polaris (271 SMART codes) [Authority]
    │
    ├─ Contains: job_code, job_nm, worker_id, location, etc.
    │
    └─ CREATE derived field: Workday format from SMART
         SMART: 1-202-2104 → Workday: US-01-0202-002104
    
    ↓ JOIN CoreHR on Workday code
    
  CoreHR (Employment data) [Job Family, Management Level, etc.]
    │
    ├─ Contains: Workday job code, employment history, user info
    │
    └─ JOIN to Polaris on transformed code
    
    ↓ JOIN TMS
    
  TMS Data (Organizational) [Teams, Workgroups]
    │
    └─ Contains: teamName, teamId, organizational hierarchy
  
  ↓
  
  FINAL: Enriched Job Codes = Polaris + CoreHR + TMS
  (No Excel needed!)

# ============================================================================
# WHY THE EXCEL BRIDGE WAS WRONG
# ============================================================================

Assumption 1: "We can't directly join Polaris to CoreHR"
Reality:     We CAN - just transform the code field!

Assumption 2: "Job code formats are incompatible"
Reality:     They're not - one is derived mathematically from the other

Assumption 3: "Excel has the mapping"
Reality:     The mapping IS THE FORMULA. We don't need Excel to store it.

Example:
  WRONG: Extract Excel codes, use them to bridge Polaris and CoreHR
  RIGHT: Transform Polaris SMART → Workday in SQL, join directly
  
  Result: 
    - Keep ALL data in BigQuery (faster, scalable)
    - No Excel dependencies
    - No data loss from unmatched Excel records
    - Direct SQL join logic

# ============================================================================
# SQL TRANSFORMATION FUNCTION
# ============================================================================

-- Convert SMART format to Workday format
-- Input:  SMART code like "1-202-2104"
-- Output: Workday code like "US-01-0202-002104"

CREATE TEMPORARY FUNCTION smart_to_workday(smart_code STRING)
RETURNS STRING
LANGUAGE js
AS """
  // Extract components from SMART: "1-202-2104"
  const parts = smart_code.split('-');
  if (parts.length !== 3) return null;
  
  const div = parseInt(parts[0]);
  const dept = parseInt(parts[1]);
  const code = parseInt(parts[2]);
  
  // Build Workday: "US-01-0202-002104"
  return 'US-' + 
         String(div).padStart(2, '0') + '-' +
         String(dept).padStart(4, '0') + '-' +
         String(code).padStart(6, '0');
""";

-- Test:
SELECT
  smart_code,
  smart_to_workday(smart_code) as workday_code
FROM (
  SELECT '1-202-2104' as smart_code  UNION ALL
  SELECT '1-0-812673'  UNION ALL
  SELECT '1-995-710'
);

-- Result:
-- 1-202-2104     → US-01-0202-002104
-- 1-0-812673     → US-01-0000-812673
-- 1-995-710      → US-01-0995-000710

# ============================================================================
# CORRECTED JOIN QUERIES
# ============================================================================

-- Query 1: Extract Polaris with Workday format
SELECT
  job_code as smart_code,
  smart_to_workday(job_code) as workday_code,  -- ← Derived field!
  job_nm,
  worker_id,
  location_nm,
  worker_payment_type,
  COUNT(DISTINCT worker_id) as worker_count
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code IS NOT NULL AND deleted = 'N'
GROUP BY smart_code, workday_code, job_nm, worker_id, location_nm, worker_payment_type;


-- Query 2: Extract CoreHR with Workday codes (already stored)
SELECT
  JSON_EXTRACT_SCALAR(emp, '$.jobCode') as workday_code,  -- ← Already Workday!
  JSON_EXTRACT_SCALAR(emp, '$.jobFamilyID') as job_family_id,
  JSON_EXTRACT_SCALAR(emp, '$.managementLevelID') as management_level,
  userID,
  employeeID
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`,
UNNEST(JSON_EXTRACT_ARRAY(employmentInfo, '$.positionInfoHistory')) as emp;


-- Query 3: JOIN on Workday codes (no Excel needed!)
WITH polaris_with_workday AS (
  SELECT
    job_code,
    smart_to_workday(job_code) as workday_code,
    job_nm,
    worker_id,
    location_nm,
    worker_payment_type,
    COUNT(DISTINCT worker_id) as worker_count
  FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
  WHERE job_code IS NOT NULL AND deleted = 'N'
  GROUP BY 1, 2, 3, 4, 5, 6
),
corehr_positions AS (
  SELECT
    JSON_EXTRACT_SCALAR(emp, '$.jobCode') as workday_code,
    JSON_EXTRACT_SCALAR(emp, '$.jobFamilyID') as job_family_id,
    JSON_EXTRACT_SCALAR(emp, '$.managementLevelID') as management_level,
    userID,
    employeeID
  FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`,
  UNNEST(JSON_EXTRACT_ARRAY(employmentInfo, '$.positionInfoHistory')) as emp
)
SELECT
  p.job_code,
  p.workday_code,
  p.job_nm,
  c.job_family_id,
  c.management_level,
  p.worker_count,
  c.userID,
  c.employeeID
FROM polaris_with_workday p
LEFT JOIN corehr_positions c 
  ON p.workday_code = c.workday_code  -- ← Direct join on transformed code!
ORDER BY p.job_code;

# ============================================================================
# BENEFITS OF CORRECTED APPROACH
# ============================================================================

✓ No Excel dependency
✓ All 271 Polaris codes preserved (no matching required)
✓ Can enrich with CoreHR directly (no intermediate steps)
✓ JOINs are 100% reversible (no data loss)
✓ TMS can still be added as optional third JOIN
✓ SQL-based transformation is faster than file matching
✓ Single source of truth (BigQuery data only)

# ============================================================================
# REVISED PIPELINE (Simpler!)
# ============================================================================

Query 1: Polaris with derived Workday codes
  ↓
Query 2: CoreHR with Workday codes  
  ↓
Query 3: LEFT JOIN on Workday code (direct!)
  ↓
Query 4: (Optional) LEFT JOIN TMS on SMART code
  ↓
Result: Complete enriched dataset

No Excel loading, no intermediate files, pure SQL logic

# ============================================================================
