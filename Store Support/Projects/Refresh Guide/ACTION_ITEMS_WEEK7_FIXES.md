# 📋 ACTION ITEMS: Week 7 Data Integrity Fixes

**Date**: February 25, 2026  
**Status**: 🔴 **REQUIRES IMMEDIATE ACTION**  
**Priority**: CRITICAL (Must fix before Week 8 begins)

---

## Executive Summary

**Week 7 Audit Results:**
- ✅ Total completed items (1,111,851) - **VERIFIED CORRECT**
- ❌ Division/Format/Area breakdowns - **COMPLETELY WRONG**
- ❌ User engagement metrics - **INCONSISTENT WITH TREND**

**Root Cause**: Only the TOTAL was extracted from BigQuery. Division/Format/Area/Engagement data was either:
1. Not extracted at all, or
2. Extracted from wrong date/query, or
3. Manually fabricated

**Impact**: Dashboard shows nonsensical data where every division/format/area DECREASED despite total INCREASING.

---

## Critical Issues Summary

| Issue | Severity | Impact | Fix |
|-------|----------|--------|-----|
| Division completed counts DOWN (all 7 divisions) | 🔴 CRITICAL | 418,204 items missing from division breakdown | Re-extract by division |
| Format completed counts DOWN (all 3 formats) | 🔴 CRITICAL | 410,949 items missing from format breakdown | Re-extract by format |
| Area completed counts DOWN (all 8 areas) | 🔴 CRITICAL | 399,574 items missing from area breakdown | Re-extract by area |
| User count dropped 41.9% (185,500 → 107,850) | 🔴 CRITICAL | Illogical trend (users down but completions up) | Verify engagement data source |
| Total actions dropped 10.5% (2,660,127 → 2,380,450) | 🔴 CRITICAL | Contradicts business logic | Re-extract activity metrics |
| Cross-validation FAILED | 🔴 CRITICAL | Dashboard data not trustworthy | Complete re-extraction required |

---

## Action Items (In Order of Execution)

### Phase 1: Data Extraction (Est. 2-3 hours)

#### ✅ Task 1.1: Extract Division Breakdown
**Status**: Ready to execute  
**Script**: `extract_week7_breakdown.py`  
**Expected Output**: 7 divisions with correct completed counts summing to 1,111,851

```bash
python extract_week7_breakdown.py
# Output will show:
#   - SOUTHEAST BU: [X] completed
#   - NORTH BU: [Y] completed
#   - ... (5 more divisions)
```

**Acceptance Criteria**:
- [ ] Sum of 7 divisions = 1,111,851
- [ ] Each division has completedCount ≥ Week 6 value
- [ ] All percentages recalculate correctly

---

#### ✅ Task 1.2: Extract Format Breakdown
**Status**: Ready to execute (same script above)  
**Expected Output**: SC, DIV1, NHM with correct counts

```
SC: [X] completed
DIV1: [Y] completed  
NHM: [Z] completed
Sum: 1,111,851
```

**Acceptance Criteria**:
- [ ] SC completed ≥ Week 6 (891,505)
- [ ] DIV1 completed ≥ Week 6 (87,422)
- [ ] NHM completed ≥ Week 6 (121,200)
- [ ] Sum = 1,111,851

---

#### ✅ Task 1.3: Extract Area Breakdown
**Status**: Ready to execute (same script above)  
**Expected Output**: 8 areas with correct counts

```
ACC: [X] completed
Asset Protection: [Y] completed
Backroom: [Z] completed
... (5 more areas)
Sum: 1,111,851
```

**Acceptance Criteria**:
- [ ] All 8 areas have values ≥ Week 6
- [ ] Sum = 1,111,851

---

#### ✅ Task 1.4: Verify User Engagement Data
**Status**: Needs investigation  
**Questions to Answer**:
- [ ] Where did "107,850 total users" come from?
- [ ] Should this be from a different table? (activity_logs vs store_refresh_data?)
- [ ] Why did it drop 41.9% if completions increased?
- [ ] Is this an extraction error or real data?

**Investigation Steps**:
1. Check data source documentation
2. Query activity_logs table for Week 7
3. Compare with Week 6 engagement data
4. Determine if 107,850 or 185,500 is correct baseline

---

### Phase 2: Dashboard Updates (Est. 30-45 min)

#### ✅ Task 2.1: Update Division Stats
**File**: `business-overview-comparison-dashboard-2-23-26.html`  
**Location**: Week 7 data (~line 1626-1742)

For each of 7 divisions:
- [ ] Replace `completedCount` with extracted value
- [ ] Recalculate `completionPercentage` = (completedCount / maxPossibleCount) * 100, round to 1 decimal
- [ ] Verify value ≥ Week 6

**Example**:
```javascript
// OLD (WRONG)
{
  "divisionId": "SOUTHEAST BU",
  "completedCount": 124180,
  "maxPossibleCount": 255162,
  "completionPercentage": 48.7
}

// NEW (CORRECT) - Replace with extracted values
{
  "divisionId": "SOUTHEAST BU",
  "completedCount": [EXTRACTED],
  "maxPossibleCount": 255162,
  "completionPercentage": [RECALCULATE]
}
```

---

#### ✅ Task 2.2: Update Format Stats
**File**: `business-overview-comparison-dashboard-2-23-26.html`  
**Location**: Week 7 formatStats (~line 1605-1625)

For each of 3 formats (SC, DIV1, NHM):
- [ ] Replace `completedCount` with extracted value
- [ ] Recalculate `completionPercentage` = (completedCount / maxPossibleCount) * 100
- [ ] Verify value ≥ Week 6

---

#### ✅ Task 2.3: Update Area Stats
**File**: `business-overview-comparison-dashboard-2-23-26.html`  
**Location**: Week 7 areaStats (~line 1742-1850)

For each of 8 areas:
- [ ] Replace `completed` value with extracted value
- [ ] Recalculate `completionPercentage` = round((completed / maxPossible) * 100, 1)
- [ ] Verify value ≥ Week 6

---

#### ✅ Task 2.4: Update User Engagement (If Verified)
**File**: `business-overview-comparison-dashboard-2-23-26.html`  
**Location**: Week 7 userEngagement (~line 1850)

Only if Task 1.4 investigation confirms the values:
- [ ] Update `workers`: [VERIFIED_VALUE]
- [ ] Update `managers`: [VERIFIED_VALUE]
- [ ] Update `totalUsers`: [VERIFIED_VALUE]
- [ ] Update `totalActions`: [VERIFIED_VALUE]
- [ ] Recalculate `actionsPerUser` = round(totalActions / totalUsers, 1)

---

### Phase 3: Validation (Est. 30 min)

#### ✅ Task 3.1: Cross-Verification
- [ ] Sum of 7 divisions = 1,111,851
- [ ] Sum of 3 formats = 1,111,851
- [ ] Sum of 8 areas = 1,111,851
- [ ] Overall total still = 1,111,851 (verify line 1524)

**Script to validate**:
```javascript
// In browser console, after loading updated dashboard
const week7 = COMPARISON_DATA.weeks[6];
const divSum = week7.divisionStats.reduce((a,b) => a + b.completedCount, 0);
const fmtSum = week7.formatStats.reduce((a,b) => a + b.completedCount, 0);
const areaSum = week7.areaStats.reduce((a,b) => a + parseInt(b.completed), 0);
console.log(`Division Sum: ${divSum} (expect 1111851)`);
console.log(`Format Sum: ${fmtSum} (expect 1111851)`);
console.log(`Area Sum: ${areaSum} (expect 1111851)`);
console.log(`Total: ${week7.summary.totalCompletedItems}`);
```

---

#### ✅ Task 3.2: Monotonic Increase Check
- [ ] Week 1: 654,855
- [ ] Week 2: 868,127 (up 213,272) ✓
- [ ] Week 3: 934,768 (up 66,641) ✓
- [ ] Week 4: 1,003,904 (up 69,136) ✓
- [ ] Week 5: 1,075,566 (up 71,662) ✓
- [ ] Week 6: 1,100,127 (up 24,561) ✓
- [ ] Week 7: 1,111,851 (up 11,724) ✓ **SHOULD BE:**
  - Division increases (all 7)
  - Format increases (all 3)
  - Area increases (all 8)

**Check**: Open dashboard in browser and verify trend chart shows continuous upward line.

---

#### ✅ Task 3.3: Percentage Validations
- [ ] Each division % ≥ Week 6
- [ ] Each format % ≥ Week 6
- [ ] Each area % ≥ Week 6
- [ ] Overall completion % = 66.3% ✓ (already correct)

---

#### ✅ Task 3.4: Browser/Visual Testing
- [ ] Open dashboard in Chrome
- [ ] Verify all 7 weeks display (grid: 4 columns × 2 rows)
- [ ] Check trend chart shows smooth upward progression
- [ ] Inspect console for JavaScript errors (press F12)
- [ ] Test on mobile (resize browser)

---

### Phase 4: Documentation (Est. 15 min)

#### ✅ Task 4.1: Document All Changes
Create `WEEK7_CORRECTIONS_APPLIED.md` with:
- [ ] Before/after values for each metric
- [ ] Extraction dates and queries used
- [ ] Cross-validation results
- [ ] Sign-off confirmation

---

#### ✅ Task 4.2: Update Data Integrity Review Checklist
- [ ] Mark Week 7 as complete/approved (once all fixes applied)
- [ ] Document lessons learned
- [ ] Update extraction process for Week 8+

---

## Execution Timeline

| Phase | Task | Est. Time | Owner | Deadline |
|-------|------|-----------|-------|----------|
| 1 | Extract breakdowns | 2-3 hours | Data Eng | Today |
| 2 | Update dashboard | 30-45 min | Dev | Today |
| 3 | Validate | 30 min | QA | Today |
| 4 | Document | 15 min | PM | Today |

**Total**: ~4 hours (If running in parallel: ~2-3 hours)

**Target Completion**: End of business **February 25, 2026**

---

## Rollback Plan (If Needed)

If extraction reveals data problems that can't be resolved:

```bash
# Revert to last known good state (Week 6 + Total Only)
git checkout HEAD~1 -- business-overview-comparison-dashboard-2-23-26.html

# This keeps:
# - Weeks 1-6 with correct data
# - Week 7 total: 1,111,851 (verified correct)

# But removes:
# - Week 7 division breakdown (until correct extraction)
# - Week 7 format breakdown (until correct extraction)
# - Week 7 area breakdown (until correct extraction)
```

---

## Success Criteria

Dashboard will be **APPROVED FOR PRODUCTION** when:

- [x] ✅ Total completions: 1,111,851 (verified from BigQuery)
- [ ] ✅ Division data: All extracted and summing to total
- [ ] ✅ Format data: All extracted and summing to total
- [ ] ✅ Area data: All extracted and summing to total
- [ ] ✅ User engagement: Verified and logically consistent
- [ ] ✅ All percentages: Recalculated and ≥ Week 6 values
- [ ] ✅ Cross-validation: All checks pass
- [ ] ✅ Trend validation: Monotonic non-decreasing
- [ ] ✅ Browser testing: No errors, displays correctly
- [ ] ✅ Documentation: Complete and signed off

---

## Sign-Off Checklist

**For Data Engineering** (Extraction):
- [ ] Division extraction complete
- [ ] Format extraction complete
- [ ] Area extraction complete
- [ ] Engagement data verified
- [ ] All sums equal 1,111,851
- **Who & When**: ________________

**For Development** (Updates):
- [ ] All values replaced in dashboard
- [ ] All percentages recalculated
- [ ] File saved and tested
- **Who & When**: ________________

**For QA** (Validation):
- [ ] Cross-verification passed
- [ ] Monotonic increase verified
- [ ] Browser testing passed
- [ ] No console errors
- **Who & When**: ________________

**For Product** (Approval):
- [ ] Data accuracy verified
- [ ] Business logic confirmed
- [ ] Ready for deployment
- **Who & When**: ________________

---

## Next Steps After Week 7 Fix

### For Week 8 (and all future weeks):

1. **Use proper extraction template** (`extract_week7_breakdown.py`)
2. **Run ALL queries in correct order**:
   - First: Get total (1 query)
   - Then: Get division breakdown (7 queries)
   - Then: Get format breakdown (3 queries)
   - Then: Get area breakdown (8 queries)
   - Then: Get engagement (1 query)
3. **Validate BEFORE updating dashboard**:
   - [ ] SUM CHECK: All breakdowns sum to total
   - [ ] TREND CHECK: All values ≥ previous week
   - [ ] LOGIC CHECK: Engagement aligns with completion trend
4. **Only deploy when ALL checks pass**

---

**Report Prepared By**: Data Audit Team  
**Report Date**: February 25, 2026  
**Status**: 🔴 **REQUIRES IMMEDIATE ACTION**  
**Next Review**: After fixes applied + validation complete
