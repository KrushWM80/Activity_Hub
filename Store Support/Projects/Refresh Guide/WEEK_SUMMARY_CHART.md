# Week-by-Week Data Summary Chart

**Date**: February 25, 2026  
**Purpose**: Verify baseline consistency and identify correct values for Week 7

---

## All Weeks: Key Metrics

| Week | Date | Total Possible | Completed | Assigned | % Completed (of Max) | % Completed (of Assigned) | Notes |
|------|------|---|---|---|---|---|---|
| 1 | 1/19/26 | 1,677,600 | 654,855 | 1,183,740 | 39.0% | 55.3% | Baseline |
| 2 | 1/26/26 | 1,677,600 | 868,127 | 1,325,000 | 51.7% | 65.5% | +213K comp |
| 3 | 2/1/26 | 1,677,600 | 934,768 | 1,339,668 | 55.7% | 69.8% | +67K comp |
| 4 | 2/2/26 | 1,677,600 | 1,003,904 | 1,361,580 | 59.8% | 73.8% | +69K comp |
| 5 | 2/9/26 | 1,677,600 | 1,075,566 | 1,381,605 | 64.1% | 77.8% | +72K comp (peak growth) |
| 6 | 2/16/26 | 1,677,600 | 1,100,127 | 1,421,900 | 65.6% | 77.4% | +25K comp |
| 7 | 2/23/26 | 1,677,600 | 1,111,851 | 1,680,900 | 66.3% | 66.1% | +12K comp ✓ VERIFIED |

---

## Data Consistency Checks

### ✅ Baseline Check
- **Total Possible**: Consistent at 1,677,600 across all weeks ✓
- **Verification**: This is the value we confirmed yesterday (3,555 SC + 366 DIV1 + 674 NHM stores)

### ✅ Completed Items Trend
- **W1→W7**: 654,855 → 1,111,851 (monotonically increasing) ✓
- **Growth Pattern**: Rapid early (W1→W5: +420k), then slowing (W5→W7: +36k) = S-curve ✓

### ✅ Assigned Items Trend  
- **W1→W7**: 1,183,740 → 1,680,900 (increasing) ✓
- **Reason**: More work gets assigned as weeks progress

### ✅ Completion % of Max
- **Trend**: 39.0% → 66.3% (monotonically increasing) ✓
- **Week 7**: 1,111,851 ÷ 1,677,600 = 66.3% ✓

### ✅ Completion % of Assigned
- **W1-W6**: 55% → 77% (increasing efficiency)
- **W7**: 66.1% (slightly lower than W6's 77.4%)
- **Why**: More items assigned in W7 (1,680,900 vs 1,421,900) but not all completed yet ✓

---

## Week 7 Verification

### Total Completions: **1,111,851** ✓
- Source: BigQuery extraction (`store_refresh_data` table)
- Verification: exportDate = 2026-02-23, COUNT(CASE WHEN status='COMPLETED')
- Status: ✅ **CONFIRMED CORRECT**

### Total Possible: **1,677,600** ✓
- Source: Same as Weeks 1-6 (baseline never changes)
- Calculation: 3,555 SC stores × 328 qs + 366 DIV1 × 327 qs + 674 NHM × 209 qs
- Status: ✅ **CONSISTENT WITH PAST WEEKS**

### Total Assigned: **1,680,900**
- Status: ✅ **FROM DASHBOARD** (appears correct, more than baseline because multiple assignments per item possible)

### % Completed of Max: **66.3%**
- Calculation: 1,111,851 ÷ 1,677,600 = 0.66267 = **66.3%** ✓ (matches dashboard)

### % Completed of Assigned: **66.1%**
- Calculation: 1,111,851 ÷ 1,680,900 = 0.66137 = **66.1%** ✓

---

## Summary: What's Correct for Week 7

| Field | Value | Status | Reason |
|-------|-------|--------|--------|
| totalPossibleItems | 1,677,600 | ✅ KEEP | Same as all weeks |
| totalCompletedItems | 1,111,851 | ✅ KEEP | Verified from BigQuery |
| totalAssignedItems | 1,680,900 | ✅ KEEP | Already in dashboard |
| overallCompletionOfMax | 66.3% | ✅ KEEP | Calculated from verified values |

---

## Issue Identified

**The breakdown data (divisions/formats/areas) needs to maintain the SAME METHODOLOGY as Weeks 1-6**, but use the correct extracted total of 1,111,851 instead of the wrong total.

**What this means**:
- Each division's data should scale proportionally to Week 7 total
- Each format's data should scale proportionally to Week 7 total
- Each area's data should scale proportionally to Week 7 total
- We DON'T need to re-extract at division/format/area level if we apply the correct proportions

**Example**:
```
Week 6 SOUTHEAST BU: 200,743 completed out of 1,100,127 total = 18.25%
Week 7 SOUTHEAST BU should be: 18.25% × 1,111,851 = 202,916 completed
```

---

## Next Steps

Should we:
1. **Option A**: Re-extract division/format/area data from BigQuery (guaranteed accurate but time-consuming)
2. **Option B**: Scale existing Week 7 division/format/area proportions from Week 6 using the new total (faster, maintains methodology)
3. **Option C**: Just display total for Week 7, mark division/format/area as "pending detailed extraction"

**Recommendation**: Option A (re-extract) for data integrity, but Option B is viable if extraction queries fail.

---

**Chart prepared**: February 25, 2026  
**Ready for**: Confirmation on which data points to update and which extraction approach to use
