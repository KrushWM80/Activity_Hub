# Code Puppy Pages - Development Guide

## Platform Overview

**Code Puppy Pages** is Walmart''s internal static content deployment platform.

- **URL**: https://puppy.walmart.com
- **Deployment**: Single-file HTML with embedded data
- **Use Cases**: Dashboards, reports, data visualizations

## Key Requirements

### Single-File Architecture
- All HTML, CSS, and JavaScript in one file
- No external dependencies or API calls
- Embed all data as JavaScript objects
- File size tested up to 2.7 MB successfully

### File Structure Pattern
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Your Dashboard</title>
    <style>/* Inline CSS */</style>
</head>
<body>
    <!-- HTML content -->
    <script>
        window.EMBEDDED_DATA = {/* Your data */};
        // Your JavaScript
    </script>
</body>
</html>
```

## Data Architecture Best Practices

### Pre-Calculate Aggregations
Store pre-calculated statistics to avoid recalculation overhead:

```javascript
window.EMBEDDED_DATA = {
    summary: {
        totalStores: 4577,
        totalAssigned: 547528,
        totalMaxPossible: 1401720
    },
    divisionStats: [
        {
            divisionId: "NHM BU",
            assignedCount: 58054,
            maxPossibleCount: 137820,
            completedCount: 15679
        }
    ],
    stores: [/* Individual store records */]
};
```

### Filtering Pattern
When filtering data, use pre-calculated stats instead of recalculating from stores:

```javascript
// WRONG - calculates wrong values
const totalAssigned = stores.reduce((sum, s) => sum + (s.maxQuestions || 0), 0);

// RIGHT - uses pre-calculated division stats
const divisionIds = [...new Set(stores.map(s => s.divisionId))];
const totalAssigned = divisionStats
    .filter(d => divisionIds.includes(d.divisionId))
    .reduce((sum, d) => sum + d.assignedCount, 0);
```

### Why This Matters
- Store-level data may not have all aggregated fields
- Backend calculations are authoritative
- Ensures data consistency across all views
- Prevents showing incorrect totals (e.g., maxPossible instead of assigned)

## Percentage Calculation Strategy

### Global vs Filtered Context
When applying filters, maintain global context for percentages:

```javascript
function recalculateMetrics(stores, globalMaxPossible) {
    const filteredMaxPossible = stores.reduce((sum, s) => sum + (s.maxQuestions || 0), 0);
    
    // Use global max for system-wide percentage
    const totalMaxPossible = globalMaxPossible || filteredMaxPossible;
    const assignedPct = (totalAssigned / totalMaxPossible) * 100;
}

// Call with global context
const globalMax = allStores.reduce((sum, s) => sum + (s.maxQuestions || 0), 0);
recalculateMetrics(filteredStores, globalMax);
```

Without passing globalMaxPossible, filtering to one division would show 100% assigned.

