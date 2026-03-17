# Available Data Sources for Employee/Contact Lookups
**Inventory Date:** March 17, 2026  
**Purpose:** Alternative data sources for store contacts, employee rosters, and associate information instead of failed Polaris queries

---

## 📊 **BIGQUERY TABLES** (Project: `wmt-assetprotection-prod`)

### Primary Tables in `Store_Support_Dev` Dataset

#### 1. **`Store Roster Contacts`** ⭐ PRIMARY ROSTER
- **Full Path:** `wmt-assetprotection-prod.Store_Support_Dev.`Store Roster Contacts``
- **Purpose:** Store contact roster with employee information
- **Key Fields:** Store, Name, (and other contact fields - schema available)
- **Status:** ✅ Accessible and tested
- **Used By:** [check_roster_schema.py](check_roster_schema.py)
- **Query Example:**
  ```sql
  SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.`Store Roster Contacts``
  WHERE Store = 30 AND (Name LIKE '%Kathleen%' OR Name LIKE '%Reed%')
  ```
- **Note:** Uses backticks due to spaces in table name

#### 2. **`Workforce Data`** ⭐ WORKFORCE TABLE
- **Full Path:** `wmt-assetprotection-prod.Store_Support_Dev.`Workforce Data``
- **Purpose:** Employee/associate workforce information
- **Key Fields:** Include first_name, last_name, store_number, job_code, job_nm
- **Status:** ✅ Accessible
- **Used By:** [search_by_workforce.py](search_by_workforce.py), [search_workforce_simple.py](search_workforce_simple.py)
- **Query Example:**
  ```sql
  SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.`Workforce Data``
  WHERE store_number = 30 AND (first_name LIKE '%Kathleen%' OR last_name LIKE '%Reed%')
  ```
- **Note:** May NOT include user_id field - primary use is name/store/job_code lookups

#### 3. **`Store Cur Data`** 
- **Full Path:** `wmt-assetprotection-prod.Store_Support_Dev.Store Cur Data`
- **Purpose:** Current store information/data
- **Status:** ✅ Referenced in infrastructure docs
- **Used By:** Setup requirements, configuration

#### 4. **`Output- TDA Report`**
- **Full Path:** `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
- **Purpose:** TDA (Trend Data Analysis) reporting output
- **Related Fields:** TDA_Ownership, store identifiers
- **Status:** ✅ Actively used
- **Used By:** [_query_ownership.py](Store%20Support/Projects/TDA%20Insights/_query_ownership.py), [analyze_data_diff.py](Store%20Support/Projects/TDA%20Insights/analyze_data_diff.py)

#### 5. **`Output- AMP ALL 2`**
- **Full Path:** `wmt-assetprotection-prod.Store_Support_Dev.Output- AMP ALL 2`
- **Purpose:** AMP (Activity Management Platform) comprehensive output
- **Status:** ✅ Accessible for AMP data queries

#### 6. **`IH_Intake_Data`**
- **Full Path:** `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
- **Purpose:** Intake Hub project data
- **Status:** ✅ Referenced in admin dashboard

#### 7. **Additional Tables (View/Views/Procedures)**
- `AMP_Events_Change_Detection` - View for change detection
- `Calendar_Change_Detection` - Calendar-based change detection
- `Store_Change_Detection` - Store-level changes
- `AMP_Data_Update_Log` - Logging table for AMP updates
- Various stored procedures for sync operations

---

## 📁 **LOCAL CSV DATA FILES** (Pre-extracted Employee Data)

### JobCodes-teaming Project
**Location:** [Store Support/Projects/JobCodes-teaming/Teaming/](Store%20Support/Projects/JobCodes-teaming/Teaming/)

#### 1. **`Worker_Names_Stores_JobCodes.csv`**
- **Purpose:** Store-based worker names mapped to store numbers and job codes
- **Columns:** `first_name, last_name, store_number, job_code, job_nm`
- **Sample Data:** Yes (9+ records showing how structure works)
- **Size:** Contains multiple workers across various stores
- **Use Case:** Direct name → store → job code lookup without database query
- **Format:** Simple CSV for direct import/search

#### 2. **`User_Details_JobCodes.csv`**
- **Purpose:** Detailed user/worker schedule and shift information
- **Columns:** Multiple schedule/shift fields including:
  - `worker_id` - UNIQUE WORKER IDENTIFIER
  - `win_nbr` - Windows identifier
  - `location_id` - Store ID
  - `location_nm` - Store name
  - `job_code, job_nm` - Job information
  - `first_name, last_name`
  - `hire_date, worker_type_code, empl_type_code`
  - Shift/schedule data
- **Sample Data:** Yes (9+ shift records)
- **Status:** ✅ Contains actual US store data
- **Key Value:** Includes `worker_id` field for identity tracking

#### 3. **`EXTRACTED_USER_IDS_WITH_USERID_FORMAT.csv`**
- **Purpose:** Extracted user IDs in standard Walmart format (kar008t.s00030)
- **Format:** `[username].[store_code]` format
- **Use Case:** Email/authentication format lookups
- **Status:** ✅ Pre-processed and ready

#### 4. **`EXTRACTED_USER_IDS_BY_JOB_CODE_20260223_080251.csv`**
- **Purpose:** User IDs organized by job code
- **Use Case:** Find associates by role/job code
- **Status:** ✅ Pre-processed

#### 5. **`polaris_user_counts.csv`**
- **Purpose:** User count data from Polaris system analysis
- **Use Case:** Validation/cross-reference data

#### 6. **`polaris_job_codes.csv`**
- **Purpose:** Job codes from Polaris system
- **Use Case:** Job code validation and mapping

### Other CSV Files in Teaming Folder
- `Teaming_Not_In_Polaris.csv` - Gap analysis data
- `Teaming_JobCodes_Not_In_HR.csv` - Data discrepancies
- `Missing_JobCodes_From_Teaming.csv` - Missing data indicators
- `Missing_From_Teaming_POLARIS.csv` - Cross-system gaps

---

## 📋 **EXCEL/DATA FILES**

### DC to Store Change Management Project
**Location:** [Store Support/Projects/DC to Store Change Management Emails/data_input/](Store%20Support/Projects/DC%20to%20Store%20Change%20Management%20Emails/data_input/)

#### 1. **`managers_export.xlsx`**
- **Purpose:** Manager roster export from Store Directory Lookup (SDL)
- **Content:** DC managers, store managers, regional managers
- **Status:** ✅ Recent data available (3 versions found)
- **Versions:**
  - `managers_export.xlsx` - Current
  - `managers_export_20260306_123108_html.xlsx` - Dated export
  - `managers_export_20260306_130122_html.xlsx` - Dated export
- **Use Case:** Store manager and DC leadership lookups

### Evaluation System
**Location:** [Store Support/Projects/Evaluation-System/](Store%20Support/Projects/Evaluation-System/)

#### 2. **`Kendalls Task and Work.xlsx`**
- **Purpose:** Work evaluation data for performance analysis
- **Status:** ✅ Available

#### 3. **`SAMPLE_DATA.csv`**
- **Purpose:** Sample evaluation system data
- **Status:** ✅ Available for reference

### TrackIT Project
**Location:** [Store Support/Projects/TrackIT/](Store%20Support/Projects/TrackIT/)

#### 4. **`Core Work Project Tasks Tracker.csv`**
- **Purpose:** Task tracking and work assignment data
- **Status:** ✅ Available

---

## 🔗 **JSON CONFIGURATION FILES** (Manager/Contact Lists)

### DC to Store Configuration
**Location:** [Store Support/Projects/DC to Store Change Management Emails/](Store%20Support/Projects/DC%20to%20Store%20Change%20Management%20Emails/)

#### 1. **`dc_contacts_template.json`** ⭐ TEMPLATE FOR EXPANSION
- **Purpose:** DC regional contact directory template
- **Structure:**
  ```json
  {
    "dcs": {
      "region_name": {
        "dc_name": "Distribution Center Name",
        "region": "Region",
        "contacts": [
          {
            "name": "Manager Name",
            "email": "email@walmart.com",
            "title": "Title",
            "role": "Role Type",
            "active": true
          }
        ]
      }
    }
  }
  ```
- **Status:** Ready-to-populate template
- **Fields:** Name, Email, Title, Role, Active status

#### 2. **`dc_to_stores_lookup.json`** ⭐ DC-TO-STORE MAPPING
- **Purpose:** Maps DC distribution centers to store numbers
- **Structure:** DC number → array of store numbers
- **Example Data:** DC 6094 → stores [1, 2, 4, 6, 10, 12, ...]
- **Use Case:** Find all stores for a DC or vice versa
- **Status:** ✅ Contains actual Walmart DC/store mappings

#### 3. **`email_recipients.json`**
- **Purpose:** Email recipient configuration
- **Status:** ✅ DC manager email list

#### 4. **Manager Snapshots** (snapshots_local folder)
- **Files:**
  - `manager_snapshot_2026-03-06.json`
  - `manager_snapshot_2026-03-05.json`
- **Purpose:** Point-in-time snapshots of manager organizational structure
- **Content:** Manager names, locations, titles, organizational hierarchy
- **Status:** ✅ Recent daily snapshots available

#### 5. **`paycycle_tracking.json`**
- **Purpose:** PayCycle automation tracking
- **Status:** ✅ Available for scheduling coordination

#### 6. **`alignment_type_mapping.json`**
- **Purpose:** Data alignment mappings
- **Status:** ✅ Available

---

## 🐍 **PYTHON SCRIPTS** (Pre-written Query Tools)

### Store Roster Queries
1. **[check_roster_schema.py](check_roster_schema.py)**
   - Query: Store Roster Contacts table schema and sample data
   - Command: `python check_roster_schema.py`

2. **[check_accessible_data.py](check_accessible_data.py)**
   - Query: Scans Store_Support_Dev for contact/roster/employee tables
   - Command: `python check_accessible_data.py`
   - Output: Lists all accessible user/contact/roster related tables

### Workforce Queries
3. **[search_by_workforce.py](search_by_workforce.py)**
   - Query: Workforce Data table for employee lookups
   - Command: `python search_by_workforce.py`

4. **[search_workforce_simple.py](search_workforce_simple.py)**
   - Simple query: Workforce Data with cleaner output

5. **[search_workforce_kathleen.py](search_workforce_kathleen.py)**
   - Find workforce table dynamically and query

### Polaris Reference (for comparison)
6. **[find_kathleen_reed.py](find_kathleen_reed.py)**
   - Proven Polaris schedule query (references: `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`)
   - Note: Can be adapted if Polaris access is restored

---

## 📊 **DATA COMPARISON/ANALYSIS**

### BigQuery Integration Framework
**Location:** [Store Support/General Setup/BigQueryProject/](Store%20Support/General%20Setup/BigQueryProject/)

1. **`tableau_schema_extracted.json`**
   - Complete field mapping from Tableau AMP Data schema
   - 311 unique fields analyzed and categorized
   - Useful for understanding available data structures

2. **Supporting Scripts:**
   - `csv_bigquery_comparison.py` - Compares CSV vs BigQuery outputs
   - `tableau_schema_extractor.py` - Field definition extraction
   - Multiple integration generator scripts

---

## 🎯 **RECOMMENDED APPROACH FOR EMPLOYEE LOOKUP**

### **Immediate Solution (No Polaris Needed)**
```
1. Use: `Store Roster Contacts` BigQuery table
   Query: SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.`Store Roster Contacts``
          WHERE Store = [store_num] AND Name LIKE '%[name]%'

2. Fallback: `Workforce Data` BigQuery table
   Query: SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.`Workforce Data``
          WHERE store_number = [store_num] AND (first_name OR last_name LIKE '%[name]%')

3. For manager lookups: Use manager_snapshot_2026-03-*.json files
   Or: managers_export.xlsx from data_input folder

4. For DC-to-store mapping: Use dc_to_stores_lookup.json
```

### **For Email Format / User ID Lookup**
```
1. Use: `User_Details_JobCodes.csv` (contains worker_id field)
2. Use: `EXTRACTED_USER_IDS_WITH_USERID_FORMAT.csv` (contains kar008t.s00030 format)
3. Pattern: [username].[store_code]
```

### **For Job Code / Role Based Lookup**
```
1. Use: `Worker_Names_Stores_JobCodes.csv`
   Columns: first_name, last_name, store_number, job_code, job_nm
2. Use: `EXTRACTED_USER_IDS_BY_JOB_CODE_*.csv`
```

---

## 🔍 **HOW TO USE THESE SOURCES**

### Python Script Execution (BigQuery)
```bash
# List all available tables with contact/roster keywords
python check_accessible_data.py

# Query Store Roster Contacts directly
python check_roster_schema.py

# Search Workforce Data
python search_by_workforce.py
python search_workforce_simple.py
```

### Direct CSV Import
```python
import pandas as pd

# Worker names by store
df_workers = pd.read_csv('Store Support/Projects/JobCodes-teaming/Teaming/Worker_Names_Stores_JobCodes.csv')
store_30_workers = df_workers[df_workers['store_number'] == 30]

# User IDs with format
df_user_ids = pd.read_csv('Store Support/Projects/JobCodes-teaming/Teaming/EXTRACTED_USER_IDS_WITH_USERID_FORMAT.csv')
```

### JSON Lookups
```python
import json

# DC to store mapping
with open('Store Support/Projects/DC to Store Change Management Emails/dc_to_stores_lookup.json') as f:
    dc_stores = json.load(f)
    stores_in_dc = dc_stores['6094']  # Get stores for DC 6094

# Manager snapshots
with open('Store Support/Projects/DC to Store Change Management Emails/snapshots_local/manager_snapshot_2026-03-06.json') as f:
    managers = json.load(f)
```

---

## ✅ **SUMMARY: WHAT'S AVAILABLE**

| Data Type | Source | Format | Status | Key Use |
|-----------|--------|--------|--------|---------|
| **Store Roster** | Store Roster Contacts (BQ) | BigQuery Table | ✅ Active | Primary contact lookup |
| **Workforce Data** | Workforce Data (BQ) | BigQuery Table | ✅ Active | Employee/associate lookup |
| **Worker Names** | Worker_Names_Stores_JobCodes | CSV | ✅ Available | Store-based name searches |
| **Worker Details** | User_Details_JobCodes | CSV | ✅ Available | Includes worker_id field |
| **User IDs** | EXTRACTED_USER_IDS_* | CSV | ✅ Available | Email format (kar008t.s00030) |
| **Manager Directory** | managers_export.xlsx | Excel | ✅ Recent | Store/DC manager lookups |
| **Manager Snaps** | manager_snapshot_*.json | JSON | ✅ Daily | Current org structure |
| **DC-to-Store Map** | dc_to_stores_lookup.json | JSON | ✅ Available | Find stores by DC |
| **Job Codes** | Multiple CSV/BQ tables | CSV/BQ | ✅ Available | Role-based search |
| **TDA Data** | Output- TDA Report | BigQuery Table | ✅ Active | TDA ownership lookups |
| **AMP Data** | Output- AMP ALL 2 | BigQuery Table | ✅ Active | AMP reporting |

---

## ⚠️ **NOTES**

1. **No Polaris Required:** All primary lookups possible via Store Roster Contacts or Workforce Data tables
2. **User ID Format:** Format is `[username].[store_code]` (e.g., kar008t.s00030)
3. **Store Numbers:** Used consistently across CSV and BigQuery tables
4. **Manager Data:** Most current via manager_snapshot JSON files (updated daily)
5. **DC Mapping:** Static mapping available in dc_to_stores_lookup.json
6. **Backtick Syntax:** BigQuery table names with spaces require backticks: \`Store Roster Contacts\`
7. **BigQuery Project:** All tables in `wmt-assetprotection-prod` project, `Store_Support_Dev` dataset

---

**Last Updated:** March 17, 2026  
**Status:** Complete Inventory  
**Alternative to:** Failed Polaris queries
