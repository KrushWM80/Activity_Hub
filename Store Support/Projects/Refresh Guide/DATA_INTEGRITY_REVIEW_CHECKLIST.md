# 📋 Data Integrity Review Checklist for Dashboard Updates

**Date Created**: February 24, 2026  
**Review Scope**: Week-by-week data validation protocol  
**Status**: ⏳ PENDING TOMORROW'S REVIEW

---

## 🎯 Core Data Integrity Principle

> **NO NUMBER SHOULD EVER DECREASE WEEK-OVER-WEEK**
> 
> All metrics follow a monotonic non-decreasing pattern:
> - Completed items: Week N ≥ Week N-1
> - Max Possible items: Week N ≥ Week N-1
> - Engagement metrics: Week N ≥ Week N-1

If ANY metric decreases, investigate immediately—it indicates a data issue.

---

## ✅ Metrics That Cannot Decrease

### 1. Overall Metrics
- [ ] `totalCompletedItems` - Must be ≥ previous week
- [ ] `totalPossibleItems` - Must be ≥ previous week (same as `maxPossibleCount`)
- [ ] `totalAssignedItems` - Must be ≥ previous week
- [ ] `overallCompletionOfMax` % - Must be ≥ previous week

### 2. Division-Level Metrics (7 divisions)
For each division:
- [ ] `completedCount` - Never decreases
- [ ] `maxPossibleCount` - Never decreases
- [ ] `completionPercentage` - Never decreases (calculated: completedCount / maxPossibleCount)

### 3. Format-Level Metrics (SC, DIV1, NHM)
For each format:
- [ ] `completedCount` - Never decreases
- [ ] `maxPossibleCount` - Never decreases
- [ ] `completionPercentage` - Never decreases (calculated: completedCount / maxPossibleCount)

### 4. Area-Level Metrics (8 store areas)
For each area:
- [ ] `completed` - Never decreases
- [ ] `maxPossible` - Never decreases
- [ ] `completionPercentage` - Never decreases (calculated: completed / maxPossible)

### 5. User Engagement Metrics
For each week:
- [ ] `workers` - Never decreases
- [ ] `managers` - Never decreases
- [ ] `totalUsers` - Never decreases
- [ ] `assignments` - Never decreases
- [ ] `completions` - Never decreases
- [ ] `totalActions` - Never decreases
- [ ] `actionsPerUser` - Never decreases

---

## 🔍 Investigation Protocol

### IF a metric decreases:

**Rule**: "If Completed can't go down AND Max Possible can't go down, then one of these changed"

#### Step 1: Identify What Changed
- [ ] Check if `totalCompletedItems` decreased
  - If YES: Data extraction error or store reset (verify with stakeholder)
- [ ] Check if `totalPossibleItems` or `maxPossibleCount` changed
  - If YES: This could explain percentage anomalies
- [ ] Check if engagement metrics changed
  - If YES: Verify if this aligns with completion trend

#### Step 2: Root Cause Determination

**Scenario A: Completed Items Decreased**
- Indicates: Data extraction error OR new cycle with reset
- Action: Re-run extraction query, verify Week N-1 vs Week N
- Validation: Run `extract_week7_final.py` pattern against Week N

**Scenario B: Max Possible Changed**
- Indicates: New stores added/removed OR baselines corrected
- Action: Document the change, recalculate all dependent percentages
- Impact: Must recalculate ALL division/format/area percentages
- Example: If maxPossibleCount goes from 1,426,588 → 1,677,600
  - Then ALL previous weeks need percentage recalculation
  - New % = completed / 1,677,600 (not old baseline)

**Scenario C: Engagement Metrics Changed Direction**
- Indicates: Data entry issue or new tracking methodology
- Action: Verify engagement data source independently
- Expected: Should mirror completion trend (more users → more completions)

#### Step 3: Percentage Recalculation

If you discover Max Possible changed, recalculate all percentages:

**For each week:**
```
Division Completion % = division_completedCount / division_maxPossibleCount
Format Completion % = format_completedCount / format_maxPossibleCount
Area Completion % = area_completed / area_maxPossible
Overall % = totalCompletedItems / totalPossibleItems
```

**Key**: Each percentage is SCOPED to its category's max possible, not global max.

---

## 📊 Data Relationships Required

### Clarification: Max Possible = Total Possible

```
totalPossibleItems  ← Global maximum across all stores/formats/areas
    ↓
    Equals the sum of:
    - All division maxPossibleCount values
    - All format maxPossibleCount values
    - All area maxPossible values
```

### Completeness Check

For Week N, verify:
```
Sum of all division completedCount = totalCompletedItems? ✓ or ✗
Sum of all format completedCount = totalCompletedItems? ✓ or ✗
Sum of all area completed = totalCompletedItems? ✓ or ✗
```

If ANY of these don't match: **Data integrity issue detected**

---

## 🧮 Mathematical Validations

### Sanity Checks (Must Pass)

For each week:
- [ ] `totalCompletedItems` ≤ `totalPossibleItems`
  - If violated: Impossible state, extraction error
- [ ] `totalCompletedItems` ≥ Week(N-1).`totalCompletedItems`
  - If violated: Data anomaly
- [ ] `overallCompletionOfMax` % = round(`totalCompletedItems` / `totalPossibleItems` * 100, 1)
  - If not equal: Calculation error
- [ ] For each division: `completionPercentage` = round(`completedCount` / `maxPossibleCount` * 100, 1)
  - If not equal: Calculation error
- [ ] For each format: `completionPercentage` = round(`completedCount` / `maxPossibleCount` * 100, 1)
  - If not equal: Calculation error
- [ ] For each area: `completionPercentage` = round(`completed` / `maxPossible` * 100, 1)
  - If not equal: Calculation error

### Trend Validation (Should Show S-Curve)

Plot `totalCompletedItems` across all weeks:
- [ ] Should increase or stay flat (never decrease)
- [ ] Should show slowing growth as approaching 100% (S-curve pattern)
- [ ] Percentage increases should be largest early, smallest near completion

If trend is jagged or has dips: **Investigate each anomaly**

---

## 📋 Tomorrow's Review Agenda

### 1. Division/Format/Area Data Audit
- [ ] Check all division maxPossibleCount values (shouldn't change)
- [ ] Check all format maxPossibleCount values (shouldn't change)
- [ ] Check all area maxPossible values (shouldn't change)
- [ ] If any changed: Document the change and recalculate affected percentages

### 2. Cross-Verification
- [ ] Sum of division completed = total completed? (Match or explain)
- [ ] Sum of format completed = total completed? (Match or explain)
- [ ] Sum of area completed = total completed? (Match or explain)

### 3. Engagement Metrics Check
- [ ] Do engagement metrics trend the same direction as completions?
- [ ] Are any engagement metrics lower than previous week? (Flag if YES)
- [ ] Does the ratio of completions to users make sense?

### 4. Percentage Recalculation Step
If any max possible values changed:
- [ ] Identify which weeks are affected
- [ ] Create recalculation impact document (like WEEK 1-6 update)
- [ ] Apply all changes systematically
- [ ] Re-validate using this checklist

### 5. Final Sign-Off
- [ ] All metrics pass monotonic non-decreasing check
- [ ] All percentages recalculated correctly
- [ ] Cross-verification math all matches
- [ ] Dashboard numbers match BigQuery extraction
- [ ] Engagement metrics align with completion trends

---

## 🚨 Red Flags (Investigate Immediately)

| Red Flag | Investigation | Action |
|----------|---|--------|
| Any completed count < previous week | Data extraction error | Re-run extraction, verify with BigQuery |
| Any max possible < previous week | Baseline changed or stores removed | Document change, recalculate all % |
| Completion % < previous week | Likely max possible reduced | Check baseline change immediately |
| Engagement down significantly | Data entry error or new methodology | Verify engagement source independently |
| Division totals ≠ overall total | Data inconsistency | Audit each division's numbers |
| Format totals ≠ overall total | Data inconsistency | Audit each format's numbers |
| Area totals ≠ overall total | Data inconsistency | Audit each area's numbers |
| Division % > overall % | Calculation error | Verify percentage formulas |
| Max possible increased | Could be data correction or new stores | Document and note in change log |

---

## 📝 Example: Week 1-6 Baseline Change

This is what happened previously—use as reference:

**Discovery**: Week 1-6 had wrong baseline
- Old: `totalPossibleItems = 1,426,588`
- Correct: `totalPossibleItems = 1,677,600`

**Impact**: ALL percentages needed recalculation
- Week 1: 45.9% → 39.0% (down because denominator increased)
- Week 2: 60.9% → 51.7%
- ...etc...

**Lesson**: When max possible changes, **all dependent %s recalculate automatically**

---

## 🎯 Review Sign-Off Template

Once all checks pass, document:

```
✅ DATA INTEGRITY REVIEW - [WEEK N]

Date Reviewed: [DATE]
Reviewer: [NAME]

Completed Items: [N] (vs Week [N-1]: [TREND])
Max Possible: [N] (vs Week [N-1]: [TREND])
Overall %: [PCT] (vs Week [N-1]: [TREND])

Division Data: ✅ VERIFIED (all non-decreasing)
Format Data: ✅ VERIFIED (all non-decreasing)
Area Data: ✅ VERIFIED (all non-decreasing)
Engagement Data: ✅ VERIFIED (all non-decreasing)

Cross-Check: ✅ PASSED (division/format/area sums match total)

Red Flags: [NONE / LIST ANY ISSUES]

Status: [APPROVED / NEEDS CORRECTION]
```

---

## 📚 Related Documents

- [WEEK7_EXTRACTION_CORRECTION_REPORT.md](./WEEK7_EXTRACTION_CORRECTION_REPORT.md) - Week 7 fix example
- [DATA_RECALCULATION_IMPACT.md](./DATA_RECALCULATION_IMPACT.md) - Week 1-6 baseline change documentation
- [STORE_FORMAT_QUESTION_MATRIX.md](./STORE_FORMAT_QUESTION_MATRIX.md) - Store format baseline validation
- [WEEKLY_DASHBOARD_UPDATE_PROCESS.md](./WEEKLY_DASHBOARD_UPDATE_PROCESS.md) - Standard update procedure

---

## 🔧 Scripts & Tools

**For Data Extraction:**
- `extract_week7_final.py` - Template for week-by-week extraction with validation

**For Validation:**
- Run comparison: Week N vs Week N-1 for all metrics
- Manual verification: Sum division/format/area totals against overall

---

**Document Version**: 1.0  
**Created**: February 24, 2026  
**Review Scheduled**: February 25, 2026  
**Next Review**: Weekly or when new week data added
