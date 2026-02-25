# 📊 Weekly Dashboard Update Process - Refresh Guide

**Last Updated**: February 24, 2026  
**Document**: Weekly data extraction & dashboard generation SOP  
**Project**: Store Refresh - 7-Week Comparison Dashboard  
**Status**: Production Ready

---

## 🎯 Overview

This document outlines the standardized process for extracting weekly BigQuery data and updating the Code Puppy Pages 7-week comparison dashboard. The process is designed to support recurring weekly updates through Week 8 and beyond.

### Current Dashboard State
- **File**: `business-overview-comparison-dashboard-2-23-26.html` (61.31 KB)
- **Data Range**: Week 1 (1/19/26) → Week 7 (2/16-2/23/26)
- **Update Frequency**: Weekly (Fridays)
- **Next Update**: Week 8 (2/23-2/28/26)

---

## 📅 Weekly Timeline

| Week | Date Range | Status | Completion % | Notes |
|------|-----------|--------|--------------|-------|
| Week 1 | 1/19/26 | ✅ Complete | 45.9% | Baseline week |
| Week 2 | 1/26/26 | ✅ Complete | 60.9% | +15.0% gain |
| Week 3 | 2/1/26 | ✅ Complete | 65.5% | +4.6% gain |
| Week 4 | 2/2/26 | ✅ Complete | 70.4% | +4.9% gain |
| Week 5 | 2/9/26 | ✅ Complete | 75.4% | +5.0% gain (peak) |
| Week 6 | 2/16/26 | ✅ Complete | 77.1% | +1.7% gain |
| Week 7 | 2/16-2/23/26 | ✅ Complete | 44.2% | -32.9% (new cycle) |
| Week 8 | 2/23-2/28/26 | ⏳ Pending | — | Ready to add |

---

## 🔄 Weekly Update Process

### Phase 1: Data Extraction (Start of Week)

**1a. Query BigQuery for Raw Metrics**

```bash
# Extract from: athena-gateway-prod.store_refresh.store_refresh_data
# Key metrics to collect:
- Total stores with assignments
- Total possible items (max questions)
- Total assigned items
- Total completed items
- Overall completion percentage
- Division-level stats (7 divisions)
- Format stats (SC, NHM, DIV1)
- Area performance (8 store areas)
- User engagement metrics
```

**Metric Structure Template:**
```json
{
  "week": 8,
  "date": "2/23/26",
  "label": "Week 8",
  "summary": {
    "totalStores": 4595,
    "storesWithAssignments": [VALUE],
    "totalPossibleStores": 4595,
    "totalPossibleItems": [VALUE],
    "totalAssignedItems": [VALUE],
    "totalCompletedItems": [VALUE],
    "overallCompletionOfMax": "[PCT]"
  },
  "divisionStats": [
    {
      "divisionId": "SOUTHEAST BU",
      "storeCount": 778,
      "assignedCount": [VALUE],
      "completedCount": [VALUE],
      "maxPossibleCount": [VALUE],
      "completionPercentage": [PCT],
      "averageMaxQuestions": 328
    }
    // ... 6 more divisions
  ],
  "formatStats": [
    {
      "format": "SC",
      "storeCount": 3555,
      "assignedCount": [VALUE],
      "completedCount": [VALUE],
      "maxPossibleCount": 1166040,
      "completionPercentage": [PCT]
    }
    // ... NHM, DIV1
  ],
  "areaStats": [
    {
      "area": "ACC",
      "assigned": [VALUE],
      "completed": [VALUE],
      "maxPossible": 215655,
      "completionPercentage": "[PCT]"
    }
    // ... 7 more areas
  ],
  "userEngagement": {
    "workers": [VALUE],
    "managers": [VALUE],
    "totalUsers": [VALUE],
    "assignments": [VALUE],
    "completions": [VALUE],
    "totalActions": [VALUE],
    "actionsPerUser": [VALUE]
  }
}
```

**Scripts Available:**
- `extract_week7_data.py` - Python extraction template
- `query_bigquery.py` - Direct BigQuery query tool

### Phase 2: Dashboard Code Update (Mid-Week)

**2a. Locate Dashboard File**
```
Store Support/Projects/Refresh Guide/business-overview-comparison-dashboard-2-23-26.html
```

**2b. Update Embedded Data (Line ~1660)**

Find the `COMPARISON_DATA` object and add new week object:
```javascript
const COMPARISON_DATA = {
  weeks: [
    // ... existing weeks 1-7
    {
      "week": 8,
      "date": "2/23/26",
      "label": "Week 8",
      // ... add extracted metrics here
    }
  ]
};
```

**2c. Verify Grid Layout**

Grid automatically adapts to any number of weeks:
- **trendChart**: `grid-template-columns: repeat(4, 1fr)` → wraps 4 columns per row
- **userEngagement**: `grid-template-columns: repeat(4, 1fr)` → same wrapping
- **divisionComparison**: `grid-template-columns: 1.2fr repeat(7, 0.8fr)` → all 7 weeks on single row

No code changes needed for grid layout—just add data.

**2d. Update Key Insights Function**

The `renderInsights()` function automatically calculates:
- Week-by-week percentage changes
- Items completed since Week 1
- Current status vs. total possible
- Active stores percentage

**No manual changes required** if using all weeks.

**2e. Update Responsive Breakpoints** (if needed)

```css
@media (max-width: 1600px) {
    #trendChart { grid-template-columns: repeat(7, 1fr); }
}
@media (max-width: 1200px) {
    #trendChart { grid-template-columns: repeat(4, 1fr); }
}
@media (max-width: 768px) {
    #trendChart { grid-template-columns: repeat(2, 1fr); }
}
```

---

### Phase 3: Validation & Testing (End of Week)

**3a. Browser Testing**
- Open HTML file in Chrome/Edge
- Verify all 8 weeks display (Row 1: Weeks 1-4, Row 2: Weeks 5-8)
- Check trends are accurate
- Verify user engagement metrics display correctly
- Test responsive breakpoints (resize browser)

**3b. Visual Validation**
- ✅ Overall Completion Trend: Shows progression and trend
- ✅ Key Insights: Week-by-week changes calculated correctly
- ✅ Division Performance: All 7 divisions visible on single row
- ✅ Format Comparison: SC/NHM/DIV1 cards display all weeks
- ✅ Area Performance: All 8 areas visible on single row
- ✅ User Engagement: Shows all metrics with growth badges

**3c. Data Accuracy Check**
- Verify latest week shows in position 8 (Week 8 placeholder becomes data)
- Confirm completion percentages match source data
- Check division totals sum to overall completion
- Validate user growth metrics are positive/realistic

**3d. File Size Check**
```bash
# Target: Keep under 100 KB
# Current: 61.31 KB (comfortable margin)
```

---

## 🎨 Layout Structure (Current)

### Trend Charts (4-Column Grid, 2 Rows)
```
Row 1: Week 1 | Week 2 | Week 3 | Week 4
Row 2: Week 5 | Week 6 | Week 7 | Week 8
```

### User Engagement (4-Column Grid, 2 Rows)
```
Row 1: Week 1 Card | Week 2 Card | Week 3 Card | Week 4 Card
Row 2: Week 5 Card | Week 6 Card | Week 7 Card | Week 8 Card
```

### Department Grids (7-Column)
```
Division Name | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 | Week 6 | Week 7
```

---

## 📝 Week 8 Specific Instructions (2/23-2/28/26)

### Metrics to Extract (Friday 2/28)
- Query final Week 8 data from BigQuery
- Calculate completion percentage (should show progression or plateau)
- Gather all 7 divisions' Week 8 stats
- Collect SC/NHM/DIV1 format breakdown
- Compile all 8 store areas data
- Gather user engagement numbers (workers, managers, actions)

### Dashboard Update Steps
1. Open `business-overview-comparison-dashboard-2-23-26.html`
2. Locate Week 7 object in COMPARISON_DATA (around line 1828)
3. Add Week 8 object immediately after Week 7
4. Update file date in header to "2/23-2/28/26"
5. Save and test in browser
6. Verify GitHub commit with message: "Week 8 data: [completion_pct]% (Week 8/2023-2028)"

### Success Criteria
- ✅ All 8 weeks visible on dashboard (Row 1: 1-4, Row 2: 5-8)
- ✅ Trend clearly shows progression or change
- ✅ No console errors
- ✅ File size remains under 100 KB
- ✅ All metrics match BigQuery source data

---

## 🔧 Technical Details

### Grid-Based Layout System

**Advantage**: No code changes needed, just add data!

```javascript
// Trend Chart Grid (4 columns, auto-wraps)
#trendChart {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
}
// Weeks 1-4 in row 1
// Weeks 5-8 auto-wrap to row 2
```

### Dynamic Rendering

**Key Functions** (auto-generate from all weeks):
- `renderTrendChart()` - Loops through ALL weeks, creates columns
- `renderUserEngagement()` - Creates engagement cards for all weeks
- `renderInsights()` - Calculates changes for ALL weeks
- `renderDivisionComparison()` - Shows all divisions × all weeks
- `renderAreaComparison()` - Shows all areas × all weeks

**No need to modify rendering code**—functions iterate through `COMPARISON_DATA.weeks` array.

---

## 📊 Data Sources

### BigQuery Tables
```
Primary: athena-gateway-prod.store_refresh.store_refresh_data
Secondary: wmt-assetprotection-prod.Store_Support_Dev.Store_Cur_Data
```

### Key Fields
- `completion_pct` → `overallCompletionOfMax`
- `total_stores` → `totalStores`
- `stores_with_assignments` → `storesWithAssignments`
- `total_possible_items` → `totalPossibleItems`
- `total_completed_items` → `totalCompletedItems`
- Division/format/area breakdowns

---

## 🚀 Future Extensions

### Week 9+ (March 2026)
- Continue using same dashboard structure
- Grid auto-adapts to any number of weeks
- Consider archiving old weeks (e.g., keep last 12 weeks)
- Monitor file size as data grows

### Enhanced Features (Roadmap)
- [ ] Click-to-detail micro-views for each week
- [ ] Export to CSV/PDF functionality
- [ ] Add week-over-week trend analysis
- [ ] Predictive completion modeling
- [ ] Store-level drilldown capability
- [ ] Multi-format comparison view

---

## ⚠️ Troubleshooting

### Issue: Grid not wrapping properly
**Solution**: Check that `grid-template-columns: repeat(4, 1fr)` is applied to `#trendChart`

### Issue: Week 8 data not showing
**Solution**: Verify week object was added to `COMPARISON_DATA.weeks` array (after Week 7)

### Issue: Metrics incorrect
**Solution**: Compare source BigQuery data against embedded JSON values

### Issue: File too large
**Solution**: Check for duplicate data entries or large metadata; target <100 KB

---

## 📞 Support & Contacts

**Dashboard Owner**: [Your Name]  
**BigQuery Access**: Contact Data Engineering  
**Code Puppy Pages**: Contact Platform Team  
**GitHub Repo**: [refresh_guide repository]

**Related Documentation**:
- [KNOWLEDGE_HUB.md](../../KNOWLEDGE_HUB.md) - Overall system architecture
- [DEPENDENCIES-MAP.md](../../DEPENDENCIES-MAP.md) - Component relationships
- [Data Classification](../../DATA-CLASSIFICATION-ASSESSMENT.md) - Data security

---

## 📋 Checklist for Week 8 Update

- [ ] Extract Week 8 data from BigQuery (Friday 2/28)
- [ ] Verify metrics against source queries
- [ ] Open dashboard HTML file
- [ ] Add Week 8 object to COMPARISON_DATA
- [ ] Update page header date range
- [ ] Test in browser (Chrome/Edge)
- [ ] Verify all 8 weeks visible
- [ ] Check responsive layouts (resize browser)
- [ ] Validate trend calculations
- [ ] Confirm no console errors
- [ ] Test on mobile device
- [ ] Commit to GitHub with week message
- [ ] Update this document with Week 8 metrics
- [ ] Archive previous version (if needed)
- [ ] Notify stakeholders of update

---

**Version**: 1.0  
**Last Updated**: February 24, 2026  
**Next Review**: March 3, 2026 (Post-Week 8)
