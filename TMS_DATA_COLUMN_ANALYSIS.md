# TMS Data (3).xlsx Column Analysis Report
# Based on: Current file structure vs. Backend requirements

## ACTUAL COLUMNS IN TMS DATA (3).xlsx
- jobCode
- deptNumber  
- divNumber

**Total: 3 columns**

---

## COLUMNS BACKEND CODE EXPECTS
From main.py lines 200-212 (load_job_code_data function):

### For groupby.agg() operation:
- jobCode ✓
- deptNumber ✓
- divNumber ✓
- jobCodeTitle ✗ MISSING
- teamName ✗ MISSING
- teamId ✗ MISSING
- workgroupName ✗ MISSING
- workgroupId ✗ MISSING

**Expected: 8 columns | Actual: 3 columns | Coverage: 37.5%**

---

## IMPACT ANALYSIS

### What Works ✓
- Composite key creation: divNumber + deptNumber + jobCode → "1-0-40407"
- Merge with polaris_job_codes.csv (uses composite_job_code as key)

### What Breaks ✗
Line 205-212 in main.py crashes when trying to aggregate missing columns:

```python
teaming_summary = teaming_df.groupby('composite_job_code').agg({
    'jobCodeTitle': 'first',                          # KeyError
    'teamName': lambda x: list(x.unique()),           # KeyError
    'teamId': lambda x: list(x.unique()),             # KeyError
    'workgroupName': lambda x: list(x.unique()),      # KeyError
    'workgroupId': lambda x: list(x.unique()),        # KeyError
})
```

Result: HTTP 500 error on `/api/job-codes` and `/api/teams` endpoints

---

## SOLUTION OPTIONS

### Option A: Add Missing Columns to TMS Data (3).xlsx
Add 5 columns with teaming assignment data:
1. **jobCodeTitle** - Job code description (e.g., "Overnight Coach")
2. **teamName** - Team assignment (e.g., "Overnight Coaches")
3. **teamId** - Team identifier  
4. **workgroupName** - Workgroup name (e.g., "Store Management")
5. **workgroupId** - Workgroup identifier

**Effort**: Moderate (need to populate these fields)
**Result**: Dashboard works with full teaming data

### Option B: Simplify Backend to Work with Existing Columns
Modify main.py to skip missing columns:
- Remove team/workgroup aggregation
- Focus on: job_code, job_name, division, department, user_count
- API returns simplified response

**Effort**: Low (code changes only)
**Result**: Basic dashboard works, teams/workgroups not available

### Option C: Replace TMS Data with Complete Source
Find/create a new teaming data source that has all 8 columns.

**Effort**: Depends on data availability
**Result**: Full feature set

---

## RECOMMENDATION

To get your dashboard working quickly while maintaining features:
**Option B is fastest**: Modify the backend to handle the current 3-column structure gracefully, then collect the team/workgroup data later if needed.

Want me to implement Option B (simplify the backend)?
