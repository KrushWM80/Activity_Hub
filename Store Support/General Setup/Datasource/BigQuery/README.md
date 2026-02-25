# 🗄️ BigQuery Datasources

## Overview

Activity Hub uses **Google BigQuery** as its primary cloud data warehouse. BigQuery provides scalable, SQL-based access to multiple Walmart business datasets across different projects.

---

## BigQuery Projects & Datasets

### 1. **polaris-analytics-prod** - Polaris Scheduling System
**Purpose**: Store labor scheduling, shift assignments, and employee scheduling data

| Dataset | Table | Purpose | Used By |
|---|---|---|---|
| `us_walmart` | `vw_polaris_current_schedule` | Current employee schedules | JobCodes-teaming, AMP Dashboard |
| `us_walmart` | `vw_polaris_associate_details` | Employee details from Polaris | JobCodes-teaming, Teaming module |
| `us_walmart` | `vw_polaris_locations` | Store/facility location data | Search By Location tools |

**Key Columns**:
- `associate_id`, `employee_name`, `employee_email`
- `store_number`, `store_name`, `location_area`
- `job_code`, `job_title`, `scheduled_hours`
- `shift_date`, `start_time`, `end_time`

**Sync Frequency**: Daily (overnight)

**Files Using This**:
```
- final_polaris_search.py
- search_by_location.py
- query_polaris_correct_columns.py
- explore_polaris_locations.py
```

**Query Example**:
```sql
SELECT 
    associate_id,
    employee_name,
    job_code,
    store_number,
    scheduled_hours
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE store_number = @store_id
LIMIT 100
```

---

### 2. **wmt-assetprotection-prod** - Asset Protection & Projects
**Purpose**: Manage Asset Protection, Projects in Stores, and Distribution Lists data

#### Dataset A: `Store_Support_Dev`

| Table | Purpose | Used By |
|---|---|---|
| `projects_intake_data` | Intake Hub project listings | Intake Hub Dashboard, Projects |
| `projects_stores_mapping` | Store assignments for projects | Projects in Stores Dashboard |
| `dl_catalog` | Email distribution lists | Distribution Lists module |
| `AMP_Data_Prep` | Asset Management Plan data | AMP Dashboard |
| `Store_Cur_Data` | Current store data | Store Support modules |

**Key Columns** (Projects):
- `project_id`, `project_title`, `project_status`
- `store_number`, `store_name`, `market`, `region`
- `start_date`, `end_date`, `owner_email`
- `budget`, `priority_level`

**Key Columns** (Distribution Lists):
- `email`, `name`, `display_name`
- `description`, `member_count`, `category`

**Sync Frequency**: 
- Projects: Daily
- Distribution Lists: Daily
- AMP Data: Real-time

**Files Using This**:
```
- database.py (Projects Dashboard backend)
- api_distribution_lists.js (Distribution Lists API)
- amp_backend_server_lite.py (AMP Dashboard)
```

**Query Example (Projects)**:
```sql
SELECT 
    project_id,
    project_title,
    store_number,
    start_date,
    end_date,
    owner_email
FROM `wmt-assetprotection-prod.Store_Support_Dev.projects_intake_data`
WHERE project_status = 'Active'
ORDER BY store_number
```

---

### 3. **athena-gateway-prod** - Store Refresh Touring
**Purpose**: Store refreshing and touring guide data

| Dataset | Table | Purpose | Used By |
|---|---|---|---|
| `store_refresh` | `store_refresh_data` | Store refresh event details | Refresh Guide Project |

**Key Columns**:
- `store_number`, `store_name`, `region`
- `refresh_type`, `phase`, `start_date`, `completion_date`
- `responsible_team`, `contact_email`, `status`

**Sync Frequency**: Daily

**Files Using This**:
```
- generate-embedded-data-bigquery-pr.js (Refresh Guide backend)
```

**Query Example**:
```sql
SELECT 
    store_number,
    phase,
    start_date,
    status
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE store_number IN (1497, 1502, 1505)
```

---

### 4. **wmt-pricingops-analytics** - Pricing Operations
**Purpose**: Pricing data, COOP details, and pricing analytics

| Dataset | Table | Purpose | Used By |
|---|---|---|---|
| `Ad_Hoc_Copp_Tables` | `mixed_base` | Mixed pricing and COOP data | Pricing Project |
| `Ad_Hoc_Copp_Tables` | `vendor_pricing` | Vendor pricing details | Pricing analysis tools |

**Key Columns**:
- `vendor_id`, `vendor_name`, `item_id`, `item_description`
- `cost`, `retail_price`, `margin`
- `coop_amount`, `coop_type`, `effective_date`

**Sync Frequency**: Daily/Weekly (depends on source)

**Files Using This**:
```
- Store Support/Projects/Pricing/fetch_data.py
```

**Query Example**:
```python
query = """
SELECT 
    vendor_id,
    item_id,
    cost,
    retail_price,
    coop_amount
FROM `wmt-pricingops-analytics.Ad_Hoc_Copp_Tables.mixed_base`
LIMIT 1000
"""
```

---

## 🔗 BigQuery Connection Details

### Authentication
- **Method**: Google Cloud Service Account
- **Credentials File**: `GOOGLE_APPLICATION_CREDENTIALS` environment variable
- **Permissions**: Minimal read access (BigQuery Data Viewer role)

### Python Client Usage
```python
from google.cloud import bigquery

# Initialize client
client = bigquery.Client(project='polaris-analytics-prod')

# Execute query
query = """
SELECT * 
FROM `project.dataset.table`
LIMIT 10
"""
results = client.query(query)

# Process results
for row in results:
    print(row)
```

### JavaScript/Node.js Usage
```javascript
const { BigQuery } = require('@google-cloud/bigquery');
const bigquery = new BigQuery({
    projectId: 'wmt-assetprotection-prod'
});

const query = `SELECT * FROM project.dataset.table LIMIT 10`;
const [rows] = await bigquery.query({ query });
```

---

## 📊 Data Schema & Column Types

For each BigQuery table, documentation is located in:

```
BigQuery/
├── Polaris.md          # Detailed schema
├── Asset-Protection.md # Detailed schema  
├── Store-Refresh.md    # Detailed schema
├── Pricing.md          # Detailed schema
```

---

## ⚙️ Query Best Practices

### 1. **Use Views for Complex Queries**
```sql
-- Good: Use existing views
SELECT * FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`

-- Prefer views over raw tables when available
```

### 2. **Filter Early**
```sql
-- Good: Filter at query time
SELECT * 
FROM table
WHERE store_number = 1497 AND year = 2026

-- Avoid: SELECT * without filters (expensive!)
```

### 3. **Use Partitioning**
```sql
-- Good: Leverage date partitions
WHERE DATE(event_date) >= '2026-01-01'
AND DATE(event_date) <= '2026-02-25'
```

### 4. **Limit Results**
```sql
-- Good: Use LIMIT for testing
SELECT * FROM table LIMIT 1000

-- Production: Aggregate or summarize large datasets
```

---

## 🔄 Data Refresh Schedule

| Project | Dataset | Table | Frequency | Time | Owner |
|---|---|---|---|---|---|
| polaris-analytics-prod | us_walmart | vw_polaris_current_schedule | Daily | 2:00 AM | Walmart Workforce |
| wmt-assetprotection-prod | Store_Support_Dev | projects_intake_data | Daily | 3:00 AM | Asset Protection |
| wmt-assetprotection-prod | Store_Support_Dev | dl_catalog | Daily | 2:30 AM | Security/Admin |
| athena-gateway-prod | store_refresh | store_refresh_data | Daily | 1:30 AM | Store Leadership |
| wmt-pricingops-analytics | Ad_Hoc_Copp_Tables | mixed_base | Daily/Weekly | Varies | Pricing Operations |

---

## ❌ Common Issues & Solutions

### Issue 1: "Table not found" Error
**Cause**: Project ID or dataset name incorrect
```
Solution: 
1. Verify project ID matches credentials
2. Check dataset name spelling (case-sensitive)
3. Confirm table exists: SELECT * FROM INFORMATION_SCHEMA.TABLES
```

### Issue 2: "Permission denied" Error
**Cause**: Service account lacks BigQuery Data Viewer role
```
Solution:
1. Add role to service account in IAM
2. Verify GOOGLE_APPLICATION_CREDENTIALS path
3. Check credentials JSON validity
```

### Issue 3: Query Timeout
**Cause**: Large dataset without proper filters
```
Solution:
1. Add time/date filters
2. Reduce SELECT scope (list specific columns)
3. Use LIMIT to test before full query
```

### Issue 4: High Query Cost
**Cause**: Scanning unnecessary data
```
Solution:
1. Use existing materialized views
2. Partition queries by time period
3. Avoid SELECT * - list specific columns
```

---

## 🛠️ Templates & Examples

### Template 1: Basic Query
See [bigquery-query-template.sql](./templates/bigquery-query-template.sql)

### Template 2: Filter by Date Range
```sql
SELECT 
    associate_id,
    employee_name,
    scheduled_hours
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE DATE(shift_date) BETWEEN @start_date AND @end_date
LIMIT 1000
```

### Template 3: Aggregation
```sql
SELECT 
    store_number,
    job_code,
    SUM(scheduled_hours) as total_hours,
    COUNT(DISTINCT associate_id) as employee_count
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
GROUP BY store_number, job_code
ORDER BY total_hours DESC
```

---

## 📞 Support

- **Error Codes**: Check [BigQuery Error Messages](https://cloud.google.com/bigquery/docs/troubleshoot)
- **Quota Issues**: Review usage in [BigQuery Admin Dashboard](https://console.cloud.google.com/bigquery)
- **Schema Help**: Query INFORMATION_SCHEMA for table details
- **Contact**: Walmart Cloud Data Engineering team

