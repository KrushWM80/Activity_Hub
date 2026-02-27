# Dashboard Data Analysis - Week 7 (2026-02-15 to 2026-02-21)

## Issue Found
The embedded data in `business-overview-dashboard-v3-2-23-26.html` does not match the Week 7 BigQuery data extracted.

## Current Embedded Data (In HTML File)
```
totalStores: 4595
storesWithAssignments: 4457
totalAssignedItems: 1384080
totalCompletedItems: 1100127
overallCompletionOfMax: 77.1%

User Engagement:
- workers: (not shown in summary)
- managers: (not shown in summary)
- totalUsers: (not shown in summary)
```

## Correct Week 7 Data (From BigQuery - Comparison Dashboard)
```
Week 7 (2026-02-15 to 2026-02-21):

Summary Data:
totalStores: 4595
storesWithAssignments: 4510
totalPossibleStores: 4595
totalPossibleItems: 1677600
totalAssignedItems: 1680900
totalCompletedItems: 1111851
overallCompletionOfMax: 66.3%

User Engagement:
- workers: 105378
- managers: 65399
- totalUsers: 170777
- assignments: 1680900
- completions: 1111851
- totalActions: 7445862
- actionsPerUser: 43.6
```

## Action Required
Update the embedded data in `business-overview-dashboard-v3-2-23-26.html` to use Week 7 BigQuery metrics:
1. Replace summary data section (starting around line 6485-6490)
2. Replace divisionStats with Week 7 values
3. Replace formatStats with Week 7 values
4. Replace areaStats with Week 7 values
5. Update the data date reference from 2026-02-16 to 2026-02-15 to 2026-02-21

## Data Source Files
- Business Overview Comparison Dashboard: business-overview-comparison-dashboard-2-23-26.html (Week 7 data at lines 1500-1700)
- Business Overview Single Week Dashboard: business-overview-dashboard-v3-2-23-26.html (needs update)
