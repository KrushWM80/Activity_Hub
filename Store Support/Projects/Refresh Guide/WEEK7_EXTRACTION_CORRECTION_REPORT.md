# Week 7 Data Extraction Correction Report

**Date**: February 24, 2026  
**Status**: ✅ CORRECTED AND APPLIED  
**Dashboard Updated**: business-overview-comparison-dashboard-2-23-26.html

---

## 🔴 Problem Identified

Week 7 showed **742,560 completed items** versus Week 6's **1,100,127 completed items**.

This was **mathematically impossible** because:
- Assessment items cannot be "uncompleted"
- All weeks use the same 1,677,600 maximum questions
- Week 7 must have ≥ Week 6's completion count
- This indicated a **data extraction error**

---

## 🔍 Root Cause Analysis

### Failed Extraction Approach

The original extraction script (`extract_week7_data.py`) was:
1. Querying user engagement metrics (workers, managers, actions)
2. **NOT** querying assessment completion metrics
3. Using **hardcoded sample data** (742,560) when BigQuery connection failed

**Key Issue**: The script fell back to this sample data:
```python
def generate_sample_week7_data():
    ...
    "total_completions": 742_560,  # ← This was the problem!
```

### Correct Data Source

The actual data comes from:
- **Table**: `athena-gateway-prod.store_refresh.store_refresh_data`
- **Schema Fields**:
  - `checklistQuestionId`: Unique question identifier
  - `status`: 'COMPLETED' or 'PENDING'
  - `exportDate`: Snapshot date for the data
  - `businessUnitNumber`: Store identifier

---

## ✅ Corrected Extraction Process

### Step 1: Schema Discovery

Discovered the actual table structure through diagnostic queries:
```sql
SELECT * FROM `athena-gateway-prod.store_refresh.store_refresh_data` LIMIT 1
```

This revealed individual checklist record data, not pre-aggregated summary data.

### Step 2: Correct Query

Developed corrected extraction query:
```sql
SELECT
    DATE(exportDate) as export_date,
    COUNT(*) as total_records,
    COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as total_completed_items,
    COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as total_pending_items,
    COUNT(DISTINCT businessUnitNumber) as store_count
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE DATE(exportDate) = '2026-02-23'
GROUP BY DATE(exportDate)
```

### Step 3: Execution

Ran corrected extraction script: `extract_week7_final.py`

---

## 🎯 Results

### Raw Extraction Data
| Metric | Value |
|--------|-------|
| Export Date | 2026-02-23 |
| Total Records | 1,489,306 |
| Total Store Units | 4,459 |
| **Total Completed Items** | **1,111,851** ✨ |
| Total Pending Items | 126,799 |

### Validation

**Compared Against Week 6:**
- Week 6 Completed: 1,100,127
- Week 7 Completed: **1,111,851**
- Difference: **+11,724** items ✅
- Result: **VALID** (maintains monotonic increase)

**Completion Percentage:**
- 1,111,851 ÷ 1,677,600 = **66.3%**
- Week 6 was 65.6%
- **+0.7 percentage point increase** ✅

### Trend Validation

Complete progression now shows:
| Week | Completed Items | % of Max | Week-over-Week Change |
|------|-----------------|----------|----------------------|
| 1 | 654,855 | 39.0% | — |
| 2 | 868,127 | 51.7% | +213,272 |
| 3 | 934,768 | 55.7% | +66,641 |
| 4 | 1,003,904 | 59.8% | +69,136 |
| 5 | 1,075,566 | 64.1% | +71,662 |
| 6 | 1,100,127 | 65.6% | +24,561 |
| 7 | **1,111,851** | **66.3%** | **+11,724** |

✅ **Pattern is valid**: Increases are slowing (S-curve) as approaching maximum

---

## 📊 Dashboard Updates Applied

### File: business-overview-comparison-dashboard-2-23-26.html

**Three data points updated:**

#### Update 1: Summary Section (Line 1523)
```javascript
// BEFORE
"totalCompletedItems": 742560,

// AFTER
"totalCompletedItems": 1111851,
```

#### Update 2: Completion Percentage (Line 1524)
```javascript
// BEFORE
"overallCompletionOfMax": "44.2"

// AFTER
"overallCompletionOfMax": "66.3"
```

#### Update 3: User Engagement Section (Line 1687)
```javascript
// BEFORE
"completions": 742560,

// AFTER
"completions": 1111851,
```

---

## 🔧 Extraction Script Improvements

### Created New Script
**File**: `extract_week7_final.py`

**Improvements**:
1. ✅ Queries correct data source (`store_refresh.store_refresh_data`)
2. ✅ Uses actual schema fields (`status`, `exportDate`)
3. ✅ Counts completed items correctly (`WHERE status = 'COMPLETED'`)
4. ✅ Includes validation logic (Week 6 comparison)
5. ✅ Provides clear feedback on data validity
6. ✅ No hardcoded fallback values

### Usage
```bash
python extract_week7_final.py
```

Output includes validation against Week 6 to ensure data integrity.

---

## 📝 Recommendations for Future Extractions

### For Week 8+

1. **Use `extract_week7_final.py` as template** for subsequent weeks
2. **Change only the `week7_export_date` variable** to target week's end date
3. **Always validate** against previous week (should be ≥ previous completion count)
4. **Store all extraction queries** in `queries/` directory for audit trail

### Suggested Automated Approach

```python
def extract_week_data(export_date):
    """Generic extraction for any week."""
    # Template provided in extract_week7_final.py
    # Already handles all BigQuery connection/query logic
    pass
```

### Script Location for Reuse
- **Path**: `Store Support/Projects/Refresh Guide/extract_week7_final.py`
- **Modify**: Line 18: `week7_export_date = "2026-02-23"` → change date
- **Run**: Same command, gets all metrics automatically

---

## ✨ Final Status

| Component | Status | Details |
|-----------|--------|---------|
| Data Extraction | ✅ CORRECTED | Using proper BigQuery schema and query logic |
| Dashboard Updated | ✅ COMPLETE | All 3 data points updated with correct values |
| Trend Validation | ✅ VALID | Monotonic increase maintained (11,724 more items) |
| Percentage Recalc | ✅ CORRECT | 1,111,851 ÷ 1,677,600 = 66.3% |
| Recovery Script | ✅ CREATED | `extract_week7_final.py` for future extractions |

---

## 📌 Summary

**WEEK 7 CORRECTION COMPLETE**

- ❌ **Removed** incorrect value: 742,560 (hardcoded sample data)
- ✅ **Applied** correct value: **1,111,851** (from BigQuery)
- ✅ **Recalculated** percentage: **66.3%** (was incorrectly 44.2%)
- ✅ **Validated** against Week 6: +11,724 items increase (valid)
- ✅ **Dashboard** now displays accurate data

**Dashboard is now production-ready with corrected Week 7 data.**

---

**Report Generated**: February 24, 2026  
**Extraction Date**: 2026-02-23  
**Total Completed Items (Week 7)**: **1,111,851**
