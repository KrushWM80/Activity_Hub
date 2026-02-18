# AMP Analysis Dashboard - Data Model & Schema Documentation

## Overview

The AMP Analysis Dashboard integrates Activity Management Plan (AMP) event data with user engagement click data to provide comprehensive visibility into store communications effectiveness and audience interaction patterns.

**Last Updated:** February 11, 2026  
**Dashboard Type:** Analysis & Reporting  
**Primary Use Case:** Monitor activity performance, engagement metrics, and completion status across all store levels

---

## Data Sources & Integration Architecture

### Primary Event Data Sources

#### 1. Current AMP Data
- **Source Table:** `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
- **Data Type:** Real-time/Current period AMP events
- **Update Frequency:** Daily
- **Key Identifier:** `event_id`, `fy` (Fiscal Year), `wm_week` (Week)
- **Record Count:** ~500-2,000 monthly records
- **Purpose:** Current activity messages and communications

#### 2. Historical AMP Data
- **Source Table:** `Output - AMP 2.0 Historic` (Tableau Prep Production)
- **Location:** https://tableau-prep-prod.homeoffice.wal-mart.com/
- **Data Type:** Historical AMP events (archive)
- **Update Frequency:** Monthly
- **Key Identifier:** `event_id`, `fy`, `wm_week`
- **Purpose:** Trend analysis and historical comparison

### Click Engagement Data Sources

#### 3. Audience Breakdown Data
- **Current Source:** `wmt-assetprotection-prod.Store_Support_Dev.Audience Breakdown Cur`
- **Historical Source:** `wmt-assetprotection-prod.Store_Support_Dev.Audience Breakdown Historical`
- **Data Type:** User engagement by audience segment (e.g., Store Managers, Associates, etc.)
- **Key Metric:** `click_count`, `view_count` per audience segment
- **Key Identifier:** `event_id`, `fy`, `wm_week`
- **Purpose:** Understand which audience segments engage with activities

#### 4. Device Types Data
- **Current Source:** `wmt-assetprotection-prod.Store_Support_Dev.Device Types Cur`
- **Historical Source:** `wmt-assetprotection-prod.Store_Support_Dev.Device Types Historical`
- **Data Type:** User engagement by device type (Mobile, Desktop, Tablet, etc.)
- **Key Metric:** `click_count`, `view_count` per device type
- **Key Identifier:** `event_id`, `fy`, `wm_week`
- **Purpose:** Analyze device preference and mobile-first trends

#### 5. Time Spent Data
- **Current Source:** `wmt-assetprotection-prod.Store_Support_Dev.Time Spent Cur`
- **Historical Source:** `wmt-assetprotection-prod.Store_Support_Dev.Time Spent Historical`
- **Data Type:** Engagement duration metrics
- **Key Metrics:** `duration_seconds`, `click_count`, `view_count`
- **Key Identifier:** `event_id`, `fy`, `wm_week`
- **Purpose:** Measure engagement depth and time commitment per activity

---

## Output Dataset Schema

### Main Dashboard Table
**Table Name:** `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_Analysis`

#### Event Identifiers
| Field | Type | Description |
|-------|------|-------------|
| event_id | STRING (PRIMARY KEY) | Unique identifier for the AMP event |
| fy | INTEGER | Fiscal Year (e.g., 2026) |
| wm_week | INTEGER | Walmart Week number (1-53) |

#### Event Core Information
| Field | Type | Description |
|-------|------|-------------|
| activity_title | STRING | Title/name of the activity (e.g., "Weekly Store Operations Update") |
| message_type | STRING | Type of message (PREFILTERED: "Store Update") |
| activity_type | STRING | Activity classification (e.g., "Action Required", "Information Only", "Autofeeds") |
| message_status | STRING | Publication status (PREFILTERED: "Published") |
| status | STRING | Verification status (e.g., "Complete", "Incomplete", "In Progress") |

#### Location & Business Hierarchy
| Field | Type | Description |
|-------|------|-------------|
| division | STRING | Walmart Division (e.g., "SAM", "General Merchandise") |
| region | STRING | Geographic region code (e.g., "R05" = Southeast) |
| market | STRING | Market area (e.g., "M142" = Atlanta) |
| store | STRING/ARRAY | Target store number(s) for the activity |
| store_area | STRING | Specific store department/area (e.g., "Produce", "Electronics") |
| audience | STRING | Target audience (e.g., "Store Associates", "Department Managers") |
| business_area | STRING | Business function area (e.g., "Store Operations", "Inventory Management") |
| total_store_count | INTEGER | Total number of stores targeted by this event |

#### Click Engagement Metrics - Audience
| Field | Type | Description |
|-------|------|-------------|
| total_audience_clicks | INTEGER | Total clicks by all audience segments |
| total_audience_views | INTEGER | Total views by all audience segments |
| audience_segment_count | INTEGER | Number of distinct audience segments that engaged |

#### Click Engagement Metrics - Devices
| Field | Type | Description |
|-------|------|-------------|
| total_device_clicks | INTEGER | Total clicks across all device types |
| total_device_views | INTEGER | Total views across all device types |
| device_type_count | INTEGER | Number of distinct device types used |
| device_types | STRING | Comma-separated list of device types (e.g., "Mobile, Desktop, Tablet") |

#### Click Engagement Metrics - Time Spent
| Field | Type | Description |
|-------|------|-------------|
| total_time_clicks | INTEGER | Total clicks during engagement sessions |
| total_time_views | INTEGER | Total views during engagement sessions |
| avg_duration_seconds | FLOAT | Average time spent per engagement (in seconds) |
| max_duration_seconds | INTEGER | Maximum time spent in a single session (in seconds) |

#### Aggregate Metrics
| Field | Type | Description |
|-------|------|-------------|
| total_clicks | INTEGER | Sum of all clicks (audience + device + time sources) |

#### Operational Links
| Field | Type | Description |
|-------|------|-------------|
| edit_link | STRING | URL to edit the activity (admin-only) |
| preview_link | STRING | URL to preview the activity for end users |

#### Metadata
| Field | Type | Description |
|-------|------|-------------|
| created_date | TIMESTAMP | When the activity was created |
| modified_date | TIMESTAMP | When the activity was last updated |
| data_source | STRING | Origin ("Current" or "Historical") |
| dashboard_refresh_timestamp | TIMESTAMP | When this record was loaded to the dashboard |

---

## Data Join Logic

### Join Keys
All joins use the composite key: **EVENT_ID + FY + WM_WEEK**

This ensures:
- No duplicate events across current and historical data
- Proper alignment of click data to specific activities
- Accurate aggregation across all engagement sources

### Join Types
```
AMP Events (Current + Historical) 
    ↓ [LEFT JOIN on event_id, fy, wm_week] ↓
Audience Click Data (aggregated)
    ↓ [LEFT JOIN on event_id, fy, wm_week] ↓
Device Click Data (aggregated)
    ↓ [LEFT JOIN on event_id, fy, wm_week] ↓
Time Spent Click Data (aggregated)
    ↓
Final Dashboard Table
```

### Deduplication Strategy
- **Current vs Historical:** If an event exists in both tables, prioritize Current data
- **Same data source:** Use most recent `modified_date`
- **No matches in click tables:** Use NULL (converted to 0 for numeric fields)

---

## Pre-filters (Admin Controlled)

### Standard Dashboard Pre-filters
```sql
WHERE message_type = 'Store Update'
  AND message_status = 'Published'
```

**Rationale:**
- Excludes draft/unpublished content
- Focuses on primary communication channel (Store Updates)
- Provides clean, production-ready view

### Admin Controls (Proposed)
- Ability to toggle `message_type` filter
- Ability to toggle `message_status` filter
- Default filters apply to all non-admin users
- Admin panel to modify pre-filter logic

---

## Available Filters (Dashboard Level)

Users can drill down by any of these dimensions:

| Filter | Type | Source | Example Values |
|--------|------|--------|-----------------|
| **Division** | Dropdown | AMP Data | "SAM", "General Merchandise", "Grocery" |
| **Region** | Dropdown | AMP Data | "R05", "R02", "R08" |
| **Market** | Dropdown | AMP Data | "M142", "M027", "M098" |
| **Store** | Dropdown/Multi-select | AMP Data | "1001", "1234", "5678" |
| **WM Week** | Slider/Dropdown | Calendar | 1-53 |
| **FY** | Dropdown | Calendar | 2024, 2025, 2026 |
| **Activity Type** | Dropdown | AMP Data | "Action Required", "Information Only", "Autofeeds" |
| **Store Area** | Dropdown | AMP Data | "Produce", "Electronics", "Grocery" |
| **Alignment** | Dropdown | AMP Data | "WM US Store", "H&W" (Health & Wellness) |
| **Key Word Search** | Text Input | AMP Data.activity_title | Free-text search across all titles |

---

## Aggregation & Calculations

### Total Clicks Formula
```
Total Clicks = Total Audience Clicks + Total Device Clicks + Total Time Clicks
```

### Engagement Rate (Proposed Additional Metric)
```
Engagement Rate (%) = (Total Clicks / Total Store Count) × 100
```

### Completion Percentage (if Status field applies)
```
Completion % = (Complete Count / Total Status Records) × 100
```

---

## Data Quality & Freshness

### Refresh Schedule
- **Current Data:** Daily (overnight)
- **Historical Data:** Weekly (Monday morning)
- **Dashboard Refresh:** Every 4 hours

### Data Validation Rules
- `event_id` is NOT NULL and UNIQUE per (fy, wm_week)
- `total_clicks` must be >= 0
- `wm_week` must be between 1-53
- `fy` must be valid fiscal year (2020-2030)
- Click counts cannot exceed total view counts

### Known Data Limitations
1. Historical data may have gaps for events prior to 2024
2. Click data reflects MyWalmart platform usage only (excludes other channels)
3. Time spent data rounded to seconds (not sub-second granularity)
4. Audience/Device/Time click data is additive (same click may be counted in multiple dimensions)

---

## Access & Permissions

### View Access
- **Standard Users:** Pre-filtered view (Store Update, Published only)
- **Managers:** Division-, Region-, or Market-level view
- **Directors:** Enterprise-wide view

### Edit Access
- **Activity Owners:** Can edit `edit_link` destinations
- **Data Admins:** Can modify pre-filters and update historical records

### Admin Access
- Full access to all fields and data
- Ability to modify pre-filters
- Access to raw data and load logs

---

## ETL Pipeline Details

### Extract Phase
- Extracts from 7 BigQuery source tables
- Applies pre-filters during extraction
- ~2-10 minutes depending on data volume

### Transform Phase
- Deduplicates events (current vs historical)
- Aggregates click data by event
- Handles NULL values (converts to 0)
- Calculates derived metrics

### Load Phase
- Writes to `Dashboard_AMP_Analysis` table
- Uses WRITE_TRUNCATE (full table refresh)
- Applies schema validation
- Stores refresh timestamp

**Execution Time:** ~5-15 minutes total  
**Failure Recovery:** Automatic retry with exponential backoff (max 3 retries)

---

## Support & Troubleshooting

### Common Issues

**No data showing for a specific week:**
- Verify events were published (check `message_status`)
- Verify events are classified as "Store Update" type
- Check if week falls within data collection period

**Click counts seem low:**
- Confirm click data tables have recent data
- Check if click data is filtered by time period
- Verify audience/device/time data alignment

**Dashboard loading slowly:**
- May indicate large query volume across all filters
- Check BigQuery query costs in Cloud Console
- Consider adding materialized views for common filter combinations

### Contact
- **Dashboard Owners:** Kendall Rush (kendall.rush@walmart.com)
- **Data Admin:** Store Support Development Team
- **BigQuery Admin:** Enterprise Data Warehouse Team

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 11, 2026 | Initial dashboard data model, 7 source tables, click engagement integration |

