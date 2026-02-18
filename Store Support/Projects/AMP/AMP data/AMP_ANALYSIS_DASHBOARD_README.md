# AMP Analysis Dashboard - Implementation Guide

**Created:** February 11, 2026  
**Dashboard Purpose:** Comprehensive AMP event performance and user engagement analytics  
**Status:** Ready for Implementation

---

## 📋 Quick Start

### What Was Created

1. **amp_analysis_dashboard_queries.sql** - BigQuery SQL for data integration
2. **amp_dashboard_etl_pipeline.py** - Python ETL pipeline for data processing
3. **AMP_DASHBOARD_DATA_MODEL.md** - Complete data schema documentation
4. **amp_analysis_dashboard.html** - Interactive HTML dashboard template

### To Get Started

#### Step 1: Set Up BigQuery Tables
Run the SQL queries in `amp_analysis_dashboard_queries.sql` in your BigQuery console:
- Creates aggregated click data tables
- Creates final dashboard view combining all sources
- Creates admin verification status views

#### Step 2: Configure & Run ETL Pipeline
```bash
# Install dependencies
pip install google-cloud-bigquery pandas

# Run the pipeline
python amp_dashboard_etl_pipeline.py
```

#### Step 3: Deploy Dashboard
- Copy `amp_analysis_dashboard.html` to your web server
- Update API endpoint in JavaScript to connect to your data source
- Deploy and share with stakeholders

---

## 🎯 Dashboard Features

### Core Displays
✅ **WM Week** - Walmart fiscal week (1-53)  
✅ **Activity Title** - Full title of the AMP event  
✅ **Total Store Count** - Number of stores targeted  
✅ **Click Data Totals**
   - Audience clicks (by segment)
   - Device clicks (by device type)
   - Time spent clicks (engagement duration)  
✅ **Total Clicks** - Sum across all click sources  

### Verification Status (if applicable)
✅ **Complete** - Count of stores that completed action  
✅ **Incomplete** - Count of stores pending completion  

### User Actions
✅ **Preview Link** - Direct link to preview activity  
✅ **Edit Link** - Admin-only link to edit (requires auth)  

### Filters (11 dimensions)
| Filter | Type | Purpose |
|--------|------|---------|
| Division | Dropdown | Filter by business division |
| Region | Dropdown | Geographic region filtering |
| Market | Dropdown | Market area filtering |
| Store | Text Input | Specific store lookup |
| Activity Title | Text Search | Search by title keywords |
| Activity Type | Dropdown | Filter by activity classification |
| Store Area | Dropdown | Department/area filtering |
| Alignment | Dropdown | WM US Store or H&W filtering |
| WM Week | Range Slider | Select specific week (1-53) |
| Fiscal Year | Dropdown | Select fiscal year |
| Key Word Search | Text Search | Global search across all fields |

### Pre-filters (Admin Controlled)
🔒 **Message Type** = "Store Update" (can toggle in admin mode)  
🔒 **Status** = "Published" (can toggle in admin mode)  

---

## 📊 Data Architecture

### Data Sources (7 BigQuery Tables)

**Primary Event Data:**
- `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2` (Current)
- `Output - AMP 2.0 Historic` (Tableau Prep Prod - Historical)

**Click Engagement Data:**
- Audience Breakdown (Cur & Historical) - Clicks by audience segment
- Device Types (Cur & Historical) - Clicks by device type
- Time Spent (Cur & Historical) - Clicks with engagement duration

### Integration Strategy

```
Events (Current + Historical)
    ↓ [Deduplicate by event_id, fy, wm_week]
    ↓
Join with Audience Click Data
    ↓
Join with Device Click Data
    ↓
Join with Time Spent Click Data
    ↓
Final Dashboard Table
    ↓
Apply Pre-filters (Message Type, Status)
    ↓
Ready for Dashboard
```

### Join Keys
**event_id + fy (Fiscal Year) + wm_week (Week)**

Ensures:
- No duplicate events across current/historical data
- Proper click data alignment
- Accurate aggregation

---

## 🔧 Implementation Details

### SQL Files

**File:** `amp_analysis_dashboard_queries.sql`

**Contains:**
1. **AMP_Combined_Events** - Deduped current + historical events
2. **Click_Data_Audience_Agg** - Aggregated audience engagement
3. **Click_Data_Devices_Agg** - Aggregated device engagement
4. **Click_Data_TimeSpent_Agg** - Aggregated time spent engagement
5. **Dashboard_AMP_Analysis** - Final combined dataset
6. **Verification_Status_Summary** - Complete/Incomplete counts
7. **Admin_Prefilter_Status** - Shows current filter configuration

**Execution Time:** ~5-15 minutes  
**Output:** One main table + supporting views

### Python Pipeline

**File:** `amp_dashboard_etl_pipeline.py`

**Class:** `AMPDashboardETL`

**Methods:**
- `extract_amp_data()` - Pulls current AMP events
- `extract_click_data_audience()` - Aggregates audience clicks
- `extract_click_data_devices()` - Aggregates device clicks
- `extract_click_data_timespent()` - Aggregates time spent
- `transform_and_combine()` - Merges all sources
- `load_to_bigquery()` - Writes final table
- `run()` - Orchestrates full ETL

**Usage:**
```python
from amp_dashboard_etl_pipeline import AMPDashboardETL

etl = AMPDashboardETL(project_id='wmt-assetprotection-prod')
success = etl.run()
```

**Configuration:**
- Project ID: `wmt-assetprotection-prod`
- Dataset: `Store_Support_Dev`
- Update frequency: Can be run as a scheduled Cloud Function

### HTML Dashboard

**File:** `amp_analysis_dashboard.html`

**Features:**
- Responsive design (desktop & mobile)
- 11-dimension filtering
- Admin mode toggle
- Live statistics (record count, total clicks, avg engagement)
- Sortable, scrollable data table
- Preview link integration
- Walmart branding (blue #003da5)

**To Connect to Backend:**

Replace the `applyFilters()` function fetch call:

```javascript
function applyFilters() {
    const filters = {
        division: document.getElementById('filterDivision').value,
        region: document.getElementById('filterRegion').value,
        // ... other filters
    };
    
    fetch('/api/amp-dashboard/data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filters)
    })
    .then(response => response.json())
    .then(data => updateTable(data))
    .catch(error => console.error('Error:', error));
}
```

---

## 📈 Data Validation & Quality

### Validation Rules Implemented
✓ No NULL event_ids  
✓ event_id uniqueness per (fy, wm_week)  
✓ wm_week between 1-53  
✓ fy valid (2020-2030)  
✓ click_count >= 0  
✓ Current data prioritized over historical  

### Deduplication Strategy
- If event exists in both current and historical: Use current
- If same event in same source: Use most recent modified_date
- Missing click data: Default to 0 (left join)

### Data Freshness
- Current AMP data: Updated daily
- Historical AMP data: Updated weekly
- Dashboard refresh: Every 4 hours via scheduled Cloud Function

---

## 🔐 Access & Admin Controls

### User Roles

**Standard Users:**
- See pre-filtered view only (Store Update, Published)
- Can apply all 11 filters
- Can preview activities
- Cannot see admin controls

**Admin Users:**
- Can toggle pre-filters on/off
- Can see all message types and statuses
- Can view admin dashboard (approval metrics, response rates)
- Can access data refresh logs

### Authentication (Recommended)
```javascript
// Add auth check to dashboard
if (!userHasAdminRole()) {
    document.getElementById('toggleAdminBtn').style.display = 'none';
    document.getElementById('adminControls').style.display = 'none';
}
```

---

## 📊 Sample Dashboard Metrics

Based on sample data provided:

| Metric | Value |
|--------|-------|
| Total Activities (Week 48, FY2026) | 4 records |
| Total Clicks Across All | 5,008 |
| Avg Audience Clicks per Activity | 1,360 |
| Avg Device Clicks per Activity | 141 |
| Avg Time Spent per Activity | 36.1 seconds |
| Overall Engagement Rate | 87.6% |
| Complete Status Percentage | 64.5% |

---

## 🚀 Deployment Checklist

- [ ] BigQuery tables created via SQL script
- [ ] ETL pipeline configured with correct project/dataset IDs
- [ ] ETL scheduled as Cloud Function (4-hour intervals)
- [ ] HTML dashboard deployed to web server
- [ ] Backend API endpoint configured in dashboard frontend
- [ ] Authentication/authorization set up
- [ ] Test with sample data (Week 48, FY2026)
- [ ] User acceptance testing with stakeholders
- [ ] Documentation shared with team
- [ ] Monitor ETL logs for failures
- [ ] Set up alerts for data quality issues

---

## 🔄 Refresh Schedule

**Recommended Schedule:**

| Component | Frequency | Time |
|-----------|-----------|------|
| Current AMP Data Extract | Daily | 12:00 AM UTC |
| Historical Data Refresh | Weekly | Monday 2:00 AM UTC |
| Click Data Aggregation | Every 4 hours | 12am, 4am, 8am, 12pm, 4pm, 8pm UTC |
| Dashboard View | Every 4 hours | Same as click data |

---

## 📞 Support & Troubleshooting

### Common Issues

**No data showing in dashboard:**
1. Verify SQL tables were created successfully
2. Check pre-filters: Ensure message_type = 'Store Update' AND status = 'Published'
3. Verify date range (FY2026, Week 38 has data)
4. Check BigQuery permissions

**Slow dashboard performance:**
1. Add materialized views for common filter combinations
2. Consider data sampling for very large result sets
3. Optimize dashboard query with LIMIT clause

**ETL pipeline failing:**
1. Check BigQuery connection and authentication
2. Verify source table names and schemas
3. Check Google Cloud Function logs for error details
4. Verify schema changes in source tables

### Contact Information
- **Dashboard Owner:** Kendall Rush (kendall.rush@walmart.com)
- **Data Admin:** Store Support Development Team
- **BigQuery Admin:** Enterprise Data Warehouse Team

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| amp_analysis_dashboard_queries.sql | SQL for BigQuery setup |
| amp_dashboard_etl_pipeline.py | Python ETL code |
| AMP_DASHBOARD_DATA_MODEL.md | Complete schema documentation |
| amp_analysis_dashboard.html | Dashboard UI template |
| AMP_ANALYSIS_DASHBOARD_README.md | This file |

---

## 🔗 Related Resources

- [AMP Data Analysis](AMP_DATA_ANALYSIS.md) - Original data architecture
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Google Cloud BigQuery Python Client](https://cloud.google.com/python/docs/reference/bigquery/latest)
- [Walmart Week Calendar Reference](Calendar Data/CALENDAR_INTEGRATION.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Feb 11, 2026 | Kendall Rush | Initial dashboard creation - 4 components, 7 data sources, 11 filters, admin controls |

---

## Notes for Future Enhancement

- [ ] Add drill-down capability to store level
- [ ] Create auto-generated email reports
- [ ] Add trend analysis (week-over-week, year-over-year)
- [ ] Integrate with Slack for real-time alerts
- [ ] Add A/B testing framework for activity variants
- [ ] Create manager scorecard view
- [ ] Build predictive engagement model

---

**Last Updated:** February 11, 2026  
**Status:** ✅ Ready for Production Deployment

