# Adobe Analytics Raw Data Pipeline

## Overview

Two separate BigQuery data pipelines now exist:

### ✅ Normalized Pipeline (Original)
**Files:** `adobe_to_bigquery_loader.py`

Extracts and normalizes data from Excel files into separate, structured tables:
- `bq_weekly_messages_devices` - Device-level metrics (11 rows)
- `bq_weekly_messages_metrics` - Aggregated metrics (11 rows)  
- `bq_playbook_hub_metrics` - Playbook data (46 rows, normalized)

**Purpose:** Tableau Prep and dashboards that need clean, structured data

**Run:** `python adobe_to_bigquery_loader.py`

---

### ✅ Raw Data Pipeline (NEW)
**Files:** `adobe_raw_data_loader.py`

Extracts and stores raw Excel data exactly as-is, preserving all metadata rows:
- `bq_playbook_hub_raw` - All 69 rows from Playbook Excel (columns: F1-F4)
- `bq_weekly_messages_raw` - All 669 rows from Weekly Messages Excel (columns: F1-F6)

**Purpose:** Audit trail, compliance, exact replication of Adobe reports

**Run:** `python adobe_raw_data_loader.py`

---

## Table Structure

### Playbook Hub Raw (`bq_playbook_hub_raw`)
```
F1 (STRING)  - Column A from Excel (page names, metadata)
F2 (STRING)  - Column B from Excel (Page Views)
F3 (STRING)  - Column C from Excel (Store Salary Associates)
F4 (STRING)  - Column D from Excel (Store Hourly Associates)
extracted_date (TIMESTAMP) - When data was loaded
```

**Sample Data:**
```
Row 1: '#================================================================', '', '', ''
Row 2: '# Playbook Hub - FY27', '', '', ''
...
Row 30: 'Page Name (v9)', '40636.0', '0.0', '0.0'
Row 31: '2026 Valentine\'s Merchandising Guide', '40494.0', '0.0', '0.0'
```

---

### Weekly Messages Raw (`bq_weekly_messages_raw`)
```
F1 (STRING)  - Column A from Excel (page names, metadata)
F2 (STRING)  - Column B from Excel (Tablets Excluding Store Devices)
F3 (STRING)  - Column C from Excel (Desktop)
F4 (STRING)  - Column D from Excel (Store Devices)
F5 (STRING)  - Column E from Excel (Mobile Phones Excluding Store)
F6 (STRING)  - Column F from Excel (XCover Devices)
extracted_date (TIMESTAMP) - When data was loaded
```

**Sample Data:**
```
Row 1: '#================================================================', '', '', '', '', ''
Row 2: '# Weekly Messages - Fashion', '', '', '', '', ''
...
Row 14: 'Page Name (v9)', '156.0', '20847.0', '', '11547.0', '7.0'
Row 15: 'store-communications:home:merc...', '21.0', '3377.0', '', '2018.0', ''
```

---

## Data Lineage

```
Excel Files (AGE Team - Documents)
    ↓
Playbook Hub and Active Playbooks - Weekly Report.xlsx
Weekly Messages Area Reports - Tables FY27.xlsx
    
    ↓ (adobe_to_bigquery_loader.py)
    ├→ Normalized Tables (Structured)
    │   ├→ bq_weekly_messages_devices
    │   ├→ bq_weekly_messages_metrics
    │   └→ bq_playbook_hub_metrics
    │
    ↓ (adobe_raw_data_loader.py)
    └→ Raw Tables (Exact Excel Copy)
        ├→ bq_playbook_hub_raw
        └→ bq_weekly_messages_raw
```

---

## Usage

Both loaders are independent and can be run separately or together:

```powershell
# Run both loaders
cd "Store Support\Projects\AMP\Weekly Messages"

# Option 1: Load normalized data (for dashboards/BI)
python adobe_to_bigquery_loader.py

# Option 2: Load raw data (for compliance/audit)
python adobe_raw_data_loader.py

# Option 3: Load both (full pipeline)
python adobe_to_bigquery_loader.py && python adobe_raw_data_loader.py
```

---

## Schedule Integration

Both loaders can be scheduled independently via Windows Task Scheduler:

### Normalized Pipeline
**When:** Sundays 6 AM (after email arrives Saturday midnight)
**Task:** `adobe_analytics_weekly_load_normalized`
**Command:** `python adobe_to_bigquery_loader.py`

### Raw Data Pipeline  
**When:** Sundays 7 AM (after normalized pipeline)
**Task:** `adobe_analytics_weekly_load_raw`
**Command:** `python adobe_raw_data_loader.py`

---

## Configuration

Both loaders use the same `adobe_config.yaml` configuration file:

```yaml
source_files:
  playbook_hub_path: "C:\Users\krush\OneDrive - Walmart Inc\AGE Team - Documents\..."
  weekly_messages_excel_path: "C:\Users\krush\OneDrive - Walmart Inc\AGE Team - Documents\..."
  weekly_messages_folder: "C:\Users\krush\Documents\VSCode\AMP\Weekly Messages\Docs\"

gcp:
  project_id: "wmt-assetprotection-prod"
  location: "US"

bigquery:
  dataset_id: "Store_Support_Dev"
  tables:
    weekly_devices: "bq_weekly_messages_devices"
    weekly_metrics: "bq_weekly_messages_metrics"
    playbook: "bq_playbook_hub_metrics"
```

---

## FAQ

**Q: Why two separate pipelines?**
A: The normalized pipeline is optimized for Tableau/BI with clean, denormalized data. The raw pipeline preserves the exact Excel format for compliance, audit trails, and accuracy verification.

**Q: Can I run both simultaneously?**
A: Yes, they operate on completely separate tables and do not interfere.

**Q: What if the Excel file structure changes?**
A: The normalized pipeline may need schema updates. The raw pipeline will still load successfully since it treats all columns as STRING.

**Q: Are the tables partitioned?**
A: Yes, both are partitioned by `extracted_date` for cost-efficient querying.

---

## Logs

Both loaders create logs in: `logs/adobe_loader.log` and `logs/adobe_raw_loader.log`

Check logs for detailed execution information, errors, and timing.
