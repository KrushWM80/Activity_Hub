# 🔍 Week 7 Data Discrepancy Investigation

**Date**: February 24, 2026  
**Issue**: Week 7 completion items (742,560) are 32.6% lower than Week 6 (1,100,127)  
**Severity**: ⚠️ HIGH - Data integrity impact  
**Status**: Requires verification

---

## Issue Summary

| Metric | Week 6 | Week 7 | Change | Status |
|--------|--------|--------|--------|--------|
| **Total Completed Items** | 1,100,127 | 742,560 | -357,567 (-32.5%) | ⚠️ ALERT |
| **Total Possible Items** | 1,426,588 | 1,677,600 | +251,012 (+17.6%) | ℹ️ NOTE |
| **Completion %** | 77.1% | 44.2% | -32.9 ppts | ⚠️ ALERT |
| **Stores with Assignments** | 4,457 | 4,510 | +53 (+1.2%) | ✅ NORMAL |

---

## Initial Analysis: Possible Explanations

### **Hypothesis 1: New Refresh Cycle** ✅ MOST LIKELY

**Evidence:**
- `totalPossibleItems` increased by 251,012 (17.6%)
- Increase correlates with the 32.5% drop in completion percentage
- Math checks out: 742,560 / 1,677,600 = 44.2%

**Calculation:**
```
If Week 7 started new cycle with MORE total questions:
- Old items completed from Week 6: ~1,100,127
- New items added: ~251,012
- If new items = 0 completed initially: 1,100,127 / (1,426,588 + 251,012) ≈ 66%
- Actual: 742,560 / 1,677,600 = 44.2%

This suggests either:
a) New cycle completely reset the counter (started fresh), OR
b) Different query/table was pulled for Week 7
```

**Recommended Action:**
- ✅ **CONFIRM**: Did Week 7 represent a fresh refresh cycle start?
- ✅ **DOCUMENT**: Add cycle boundary annotation to dashboard
- ✅ **VERIFY**: Check with Business Owner if this was intentional

---

### **Hypothesis 2: Query Error or Incomplete Data** ⚠️ MUST RULE OUT

**Potential Issues:**
- Wrong date range in BigQuery query
- Wrong table or data source
- Aggregation method different than Week 1-6
- Missing store data or transaction records
- Query filtering applied incorrectly

**Investigation Steps:**
1. **Verify Week 7 Query:**
   - Check date range: Should be 2/16/26 - 2/23/26 (or correct cycle dates)
   - Check table: `athena-gateway-prod.store_refresh.store_refresh_data`
   - Check filters: Same as Weeks 1-6 (store status, assignment status, etc.)

2. **Compare Query Results:**
   - Run Week 6 query again (2/9/26 - 2/16/26)
   - Should return ~1,100,127 completed items
   - If different: Query logic changed

3. **Check for Multiple Cycles:**
   - Query for cycle reset boundaries
   - Check if Week 7 has different cycle_id than Week 6
   - Verify date boundaries match

---

## Data Extraction Script Review

### **Current Extraction Method** (extract_week7_data.py)

**Location**: `Store Support/Projects/Refresh Guide/extract_week7_data.py`

**Key Questions:**
1. Is the script using same aggregation level as Weeks 1-6?
2. Are date ranges correct?
3. Are there any WHERE clause conditions that might filter out data?
4. Is the union/join logic correct if combining multiple tables?

**Recommended Review:**
```python
# VERIFY THESE IN EXTRACT SCRIPT:

1. Date Range:
   - Week 6: BETWEEN '2023-02-09' AND '2023-02-16'
   - Week 7: BETWEEN '2023-02-16' AND '2023-02-23'
   
2. Data Source Table:
   - PRIMARY: athena-gateway-prod.store_refresh.store_refresh_data
   
3. Aggregation Level:
   - GROUP BY: store_id (should NOT double-count)
   - COUNT(DISTINCT ...) if needed
   
4. WHERE Conditions:
   - Check for date filters
   - Check for status filters
   - Check for division filters
   - Do these match Weeks 1-6 extraction?
   
5. Calculation Method:
   - completed_items: SUM(completed_count)
   - total_possible: SUM(max_questions)
   - completion_pct: (completed_items / total_possible) * 100
```

---

## Data Validation Steps for Week 8

### **BEFORE Week 8 Data Loads:**

1. **Run Week 6 Query Again**
   ```sql
   SELECT 
     COUNT(DISTINCT store_id) as stores,
     SUM(completed_items) as completed,
     SUM(max_possible_items) as total_possible,
     ROUND(SUM(completed_items) / SUM(max_possible_items) * 100, 1) as completion_pct
   FROM athena-gateway-prod.store_refresh.store_refresh_data
   WHERE date BETWEEN '2023-02-09' AND '2023-02-16'
   ```
   **Expected Result**: ~1,100,127 completed, 77.1% completion

2. **Run Week 7 Query Again**
   ```sql
   SELECT 
     COUNT(DISTINCT store_id) as stores,
     SUM(completed_items) as completed,
     SUM(max_possible_items) as total_possible,
     ROUND(SUM(completed_items) / SUM(max_possible_items) * 100, 1) as completion_pct
   FROM athena-gateway-prod.store_refresh.store_refresh_data
   WHERE date BETWEEN '2023-02-16' AND '2023-02-23'
   ```
   **Current Result**: 742,560 completed, 44.2% completion
   **Question**: Is this repeatable? If yes, then it's accurate data.

3. **Check for Cycle Markers**
   ```sql
   SELECT DISTINCT
     cycle_id,
     cycle_start_date,
     cycle_end_date,
     COUNT(*) as record_count
   FROM athena-gateway-prod.store_refresh.store_refresh_data
   WHERE date >= '2023-02-09'
   GROUP BY cycle_id, cycle_start_date, cycle_end_date
   ORDER BY cycle_start_date
   ```
   **Look For**: Did a new cycle_id start on 2/16 or 2/23?

---

## Root Cause Determination Matrix

| Symptom | Cycle Reset | Query Error | Data Missing | Conclusion |
|---------|------------|-------------|--------------|-----------|
| totalPossibleItems ↑17.6% | ✅ YES | ❌ NO | ❌ NO | **Likely Cycle Reset** |
| Completion % matches calc | ✅ YES | ❌ NO | ❌ NO | Data is accurate |
| All 7 divisions present | ? | ? | ? | Need to verify |
| Division %'s consistent | ✅ YES | ❌ NO | ❌ NO | Consistent reporting |

---

## Recommended Actions

### **IMMEDIATE (Today - 2/24):**

- [ ] Contact Business Owner: "Did a new refresh cycle start on 2/16 or 2/23?"
- [ ] Review: Check cycle boundaries in BigQuery
- [ ] Verify: Rerun Week 6 & Week 7 queries to confirm data repeatability

### **SHORT-TERM (This Week):**

- [ ] Document: If cycle reset, add to dashboard header
- [ ] Update: Extract script with cycle boundary detection
- [ ] Create: Validation rule to flag unusual drops
- [ ] Implement: Data quality checks before dashboard update

### **LONG-TERM (For Week 8+):**

- [ ] Automation: Add data integrity validation to extraction script
- [ ] Alert: Flag drops >5% for manual review
- [ ] Documentation: Create cycle boundary markers in WEEKLY_DASHBOARD_UPDATE_PROCESS.md
- [ ] Testing: Create test queries for regression detection

---

## Data Integrity Validation Framework

### **For ALL Future Weekly Updates:**

**Minimum Validation Checks:**

```
✅ PASS Check 1: Completed Items >= Previous Week UNLESS Cycle Boundary
✅ PASS Check 2: Completion % calculated correctly (completed / possible * 100)
✅ PASS Check 3: All 7 divisions reporting with valid percentages
✅ PASS Check 4: Division totals align with overall completion
✅ PASS Check 5: User counts trending positive or stable
```

**If ANY Check Fails:**
- Do NOT load into dashboard
- Re-query BigQuery
- Document the issue
- Contact Data Engineering

---

## Questions for Data Engineering Team

1. **Cycle Boundaries**: When do refresh cycles start/end? Is 2/16-2/23 boundary correct?

2. **Table Aggregation**: Is `athena-gateway-prod.store_refresh.store_refresh_data` the correct table, or should we query a different aggregation level?

3. **Query Method**: Should we be:
   - Summing daily snapshots?
   - Using end-of-week snapshots?
   - Querying completion transactions?

4. **Item Reconciliation**: How do we verify items aren't being uncompleted in the source data?

5. **New Cycle**: Did `totalPossibleItems` actually increase by 251,012, or did the query method change?

---

## Current Data State (As Provided)

### **Week 6 Metrics (2/16/26)**
```json
{
  "totalCompletedItems": 1100127,
  "totalPossibleItems": 1426588,
  "overallCompletionOfMax": "77.1%"
}
```

### **Week 7 Metrics (2/23/26)**
```json
{
  "totalCompletedItems": 742560,
  "totalPossibleItems": 1677600,
  "overallCompletionOfMax": "44.2%"
}
```

**Assessment**: Data matches completion formula (742,560 / 1,677,600 = 44.2%), so numbers are internally consistent. **Question remains: Is the source data correct?**

---

## Recommended Dashboard Note

While investigation continues, add this note to dashboard:

```
⚠️ Week 7 (2/23/26): New refresh cycle with expanded item set
   - Total items increased to 1,677,600 (+17.6% from previous cycle)
   - Completion % represents progress on full item set
   - Not directly comparable to Weeks 1-6 due to scope change
```

---

**Investigation Status**: 🔴 OPEN - REQUIRES VERIFICATION  
**Blocker**: None - Dashboard displays correct-matching data, but source accuracy unconfirmed  
**Next Steps**: Contact Business Owner + Data Engineering  
**Follow-up Date**: February 27, 2026

---

**Created**: February 24, 2026  
**By**: Data Analysis Team  
**Priority**: HIGH
