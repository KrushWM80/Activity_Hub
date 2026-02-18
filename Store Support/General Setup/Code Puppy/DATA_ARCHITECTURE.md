# Data Architecture Patterns

## Overview

This guide documents best practices for structuring data in Code Puppy Pages applications, particularly for dashboards with filtering capabilities.

## Dual-Granularity Data Pattern

### Concept
Store both pre-aggregated statistics and raw granular data:

```javascript
window.EMBEDDED_DATA = {
    // Pre-calculated aggregations (from backend)
    summary: {
        data: {
            divisionStats: [...],  // Division-level totals
            regionStats: [...],    // Region-level totals
            formatStats: [...]     // Format-level totals
        }
    },
    
    // Raw individual records
    stores: {
        data: [...]  // Individual store records
    }
};
```

### Why Both?
- **Aggregations**: Fast filtering, matches backend calculations
- **Raw data**: Enables drill-down, custom filtering
- **Consistency**: Pre-calculated stats are authoritative

## Critical Lesson: Store Data Limitations

### The Problem
Store-level records may not contain all aggregated fields needed for metrics.

**Example from Business Overview Dashboard:**
```javascript
// Store record has:
{
    storeNumber: "1",
    maxQuestions: 324,      // Max possible items
    completedItems: 66,     // Completed items
    divisionId: "NHM BU"
    // BUT: No assignedItems field!
}

// Division stats has:
{
    divisionId: "NHM BU",
    assignedCount: 58054,       //  Has assigned count
    maxPossibleCount: 137820,   // Sum of all store maxQuestions
    completedCount: 15679
}
```

### The Bug This Causes
```javascript
// WRONG - sums maxQuestions thinking it''s assigned
const totalAssigned = stores.reduce((sum, s) => 
    sum + (s.maxQuestions || 0), 0
);
// For NHM: Shows 137,820 (max possible) instead of 58,054 (actual assigned)
```

### The Fix
```javascript
// RIGHT - uses pre-calculated division stats
const divisionIds = [...new Set(stores.map(s => s.divisionId))];
const totalAssigned = divisionStats
    .filter(div => divisionIds.includes(div.divisionId))
    .reduce((sum, div) => sum + (div.assignedCount || 0), 0);
// For NHM: Correctly shows 58,054
```

## Filtering Architecture

### Filter-First Pattern
1. Filter stores by selected criteria
2. Extract affected division/region/market IDs
3. Filter pre-calculated stats
4. Sum filtered stats (don''t recalculate)

```javascript
function applyFilters(selectedFilters) {
    // 1. Filter stores
    const filteredStores = allStores.filter(store => {
        if (selectedFilters.division.length > 0 && 
            !selectedFilters.division.includes(store.divisionId)) {
            return false;
        }
        if (selectedFilters.format.length > 0 && 
            !selectedFilters.format.includes(store.format)) {
            return false;
        }
        return true;
    });
    
    // 2. Get affected division IDs
    const divisionIds = [...new Set(filteredStores.map(s => s.divisionId))];
    
    // 3. Filter pre-calculated stats
    const filteredDivisionStats = allDivisionStats.filter(div => 
        divisionIds.includes(div.divisionId)
    );
    
    // 4. Sum stats
    const totalAssigned = filteredDivisionStats.reduce(
        (sum, div) => sum + div.assignedCount, 0
    );
    const totalMaxPossible = filteredDivisionStats.reduce(
        (sum, div) => sum + div.maxPossibleCount, 0
    );
    
    // 5. Update UI
    updateMetrics({ totalAssigned, totalMaxPossible });
}
```

## Division Card Filtering

### Requirement
When filtering by division:
- Show only selected division cards
- Maintain original percentages (don''t recalculate)

```javascript
// Get all division stats
const allDivisionStats = EMBEDDED_DATA.summary.data.divisionStats;

// Filter to selected divisions
const filteredDivisionStats = selectedFilters.division.length > 0 
    ? allDivisionStats.filter(div => 
        selectedFilters.division.includes(div.divisionId))
    : allDivisionStats;

// Render filtered cards (keeps original %)
updateDivisionCards(filteredDivisionStats);
```

### Why Not Recalculate?
Division stats contain backend-calculated values:
- `completionPercentage`: Completed / Max Possible
- `assignedCount`: Backend knows which items are assigned
- Recalculating from stores would be inaccurate

## Percentage Calculations

### Global vs Filtered Context

**Two types of percentages:**
1. **System-wide**: Relative to all stores
2. **Filtered**: Relative to filtered subset

**Example metrics that need global context:**
- "X% of all possible items assigned"
- "Store coverage rate"

```javascript
function recalculateMetrics(stores, globalMaxPossible) {
    const filteredMaxPossible = stores.reduce(
        (sum, s) => sum + (s.maxQuestions || 0), 0
    );
    
    // Use global for system-wide percentages
    const totalMaxPossible = globalMaxPossible || filteredMaxPossible;
    const assignedPct = (totalAssigned / totalMaxPossible) * 100;
    
    // Use filtered for subset-specific percentages
    const completionRate = (totalCompleted / totalAssigned) * 100;
}
```

### Calling Pattern
```javascript
// Calculate global max once
const globalMaxPossible = allStores.reduce(
    (sum, s) => sum + (s.maxQuestions || 0), 0
);

// Pass to recalculate function
function handleFilterChange() {
    const filteredStores = applyStoreFilters(allStores);
    recalculateMetrics(filteredStores, globalMaxPossible);
}
```

## Common Pitfalls

### Pitfall 1: Assuming Store Has All Fields
 **Wrong**: `store.assignedItems` (field doesn''t exist)
 **Right**: Get from division stats

### Pitfall 2: Recalculating What''s Pre-Calculated
 **Wrong**: Sum store data for metrics
 **Right**: Filter and sum division stats

### Pitfall 3: Losing Global Context
 **Wrong**: Calculate % from filtered data only
 **Right**: Pass globalMaxPossible parameter

### Pitfall 4: Recalculating Division Percentages
 **Wrong**: Recalculate division completion %
 **Right**: Use pre-calculated `completionPercentage`

## Data Validation Checklist

Before deployment, verify:
- [ ] Division stats sum equals system totals
- [ ] Store count matches backend
- [ ] Max possible = sum of all store maxQuestions
- [ ] Assigned count from backend, not calculated
- [ ] Completion percentages match backend
- [ ] Filtered metrics use correct denominator

## Testing Scenarios

### Test 1: No Filters
- Should show all system data
- Metrics match summary totals
- All divisions visible

### Test 2: Single Division Filter
- Shows only that division
- Assigned count matches divisionStats
- Percentages relative to global max

### Test 3: Multiple Division Filter
- Shows selected divisions
- Metrics sum correctly
- Division cards filter appropriately

### Test 4: Combined Filters
- Division + Format
- Division + Region
- All three combined

**Last Updated**: January 13, 2026
