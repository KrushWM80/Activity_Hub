# Project Update Date Structure Analysis

## Summary
The Activity Hub database stores project update timestamps in the BigQuery table `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`. This document analyzes the available fields and their purposes.

## Current Database Fields

### Timestamp Fields
| Field Name | Type | Source | Purpose |
|------------|------|--------|---------|
| `created_date` | TIMESTAMP | BigQuery | When the project record was first created in the system |
| `last_updated` | TIMESTAMP | BigQuery | When the project record was last modified (system-managed) |
| `project_update` | STRING | User Input | The actual project update/note content (text field, NOT a timestamp) |

### Current Implementation
- **`created_date`**: Auto-set to CURRENT_TIMESTAMP() when a new project is inserted
- **`last_updated`**: Auto-set to CURRENT_TIMESTAMP() for any CREATE or UPDATE operation
- **`project_update`**: User-provided text content describing the current project status/update

## Key Finding
There is **NO separate `Project_Update_Date` column** in the database. The system uses:
1. **`last_updated`** (TIMESTAMP) - when the update was recorded
2. **`project_update`** (STRING) - what the update says

## Proposed Enhancement Option 1: Add Explicit Field
To explicitly track when a project update text was created separately from system modifications:

```sql
ALTER TABLE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
ADD COLUMN project_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP() 
```

Benefits:
- Separates user update timing from system metadata changes
- Users can timestamp when they actually worked on the project vs. when they edited the record

## Proposed Enhancement Option 2: Current Structure (Recommended)
Keep using `last_updated` as the project change timestamp because:
- Simple to maintain (one timestamp field)
- Accurate reflection of when information changed
- Aligns with standard database practices

## Current WM Week Calculation
```python
fiscal_year_start = datetime(today.year if today.month >= 2 else today.year - 1, 2, 1)
days_since_fy = (today - fiscal_year_start).days
current_wm_week = (days_since_fy // 7) + 1
```
- Fiscal year starts February 1st
- Weeks are calculated as 7-day intervals from FY start
- Currently used for filtering "Updated This Week" logic

## Data Architecture
```
Activity Hub Projects Table
├── project_id (STRING) - Unique identifier
├── title (STRING) - Project name
├── business_organization (STRING) - Business area
├── owner (STRING) - Project owner name
├── owner_id (STRING) - Owner ID
├── health (STRING) - Project health status
├── status (STRING) - Project status
├── project_source (STRING) - Intake Hub | Manual Entry | Data-Bridge
├── created_date (TIMESTAMP) - When record was created
├── last_updated (TIMESTAMP) ← Project change timestamp
└── project_update (STRING) - Update content/notes
```

## Recommendations

### Issue #1: Missing Project_Update_Date
**Current Solution**: `last_updated` serves as the project update date
- This is the timestamp of the latest update to the project
- Accurate for determining "updated this week" calculations

### Issue #2: Potential Enhancement
If you want to track when a user actually made an update vs. system modifications:
- Option A: Add a new `project_update_date` column (breaking change)
- Option B: Store update timestamp in `project_update` text (current approach)
- Option C: Keep current structure and derive dates from `last_updated` (simplest)

### Issue #3: WM Week Tracking
Current implementation:
- ✅ Calculates correctly based on Walmart fiscal calendar
- ✅ Identifies "updated this week" for filtering
- ✅ Can be extended to show "WK 12" format in UI if needed

## Conclusion
**No additional database changes needed.** The current structure uses `last_updated` (TIMESTAMP) as the effective "Project Update Date." This field:
- Accurately tracks when project information was last changed
- Powers the WM week calculations
- Is suitable for all current and proposed filtering needs

If you need to display the project update date/time on the dashboard for transparency, use the `last_updated` field and format as needed (e.g., "Apr 20, 2026").
