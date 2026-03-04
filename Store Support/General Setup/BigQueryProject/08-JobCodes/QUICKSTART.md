# ⚡ Job Codes - Quick Start Guide

## What Are Job Codes?

Job codes are **unique identifiers for positions** at Walmart. They exist in multiple formats across different systems:

| Format | Example | System |
|--------|---------|--------|
| **SMART** | `1-993-1026` | AMP, Email, HR systems |
| **Workday** | `US-01-0202-002104` | Financial, planning systems |
| **User ID** | `e0c0l5x.s03935` | BigQuery, CoreHR, Polaris |

---

## 5-Minute Lookup: Find User IDs for a Job Code

### What You Need
- Job code (SMART format, like `1-993-1026`)
- Google BigQuery access
- Python installed with google-cloud-bigquery

### Quick Python Script

```python
from google.cloud import bigquery

# Setup
client = bigquery.Client(project='polaris-analytics-prod')
job_code = "1-993-1026"  # ← CHANGE THIS

# Query current employees with this job code
query = f"""
SELECT 
    worker_id,
    employee_name,
    job_name,
    store_number,
    COUNT(*) as scheduled_shifts
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code = '{job_code}'
    AND shift_date >= CURRENT_DATE() - 7
GROUP BY worker_id, employee_name, job_name, store_number
ORDER BY store_number
"""

results = client.query(query)
for row in results:
    print(f"{row.worker_id} | {row.employee_name} | {row.job_name} | Store {row.store_number}")
```

### What You Get
- **worker_id** ← Use this as the User ID in AMP Roles
- **employee_name** ← For verification
- **job_name** ← Human-readable description
- **store_number** ← Where they work

---

## Finding Job Codes by Role Name

### Example: Find all "Store Manager" job codes

```python
import json

# Load master database
with open('job_codes_master.json', 'r') as f:
    master = json.load(f)

# Find all matching codes
search_term = "Store Manager"
matches = [(code, info) for code, info in master.items() 
           if search_term.lower() in info.get('job_name', '').lower()]

for code, info in matches:
    print(f"{code}: {info['job_name']}")
```

---

## Get All Job Codes at a Store

```python
from google.cloud import bigquery

client = bigquery.Client(project='polaris-analytics-prod')
store_number = 3456  # ← YOUR STORE NUMBER

query = f"""
SELECT DISTINCT
    job_code,
    job_name,
    COUNT(DISTINCT worker_id) as num_employees
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE store_number = {store_number}
    AND shift_date = CURRENT_DATE()
GROUP BY job_code, job_name
ORDER BY num_employees DESC
"""

for row in client.query(query):
    print(f"{row.job_code} | {row.job_name} | {row.num_employees} employees")
```

---

## Validate a Mapping: SMART → Workday → User ID

```python
import json
from google.cloud import bigquery

def validate_job_code(smart_code):
    # Load master
    with open('job_codes_master.json', 'r') as f:
        master = json.load(f)
    
    if smart_code not in master:
        print(f"❌ {smart_code} not found in master database")
        return
    
    info = master[smart_code]
    workday_code = info.get('workday_code')
    job_name = info.get('job_name')
    
    print(f"✓ SMART:    {smart_code}")
    print(f"✓ Workday:  {workday_code}")
    print(f"✓ Role:     {job_name}")
    
    # Query Polaris for current assignments
    client = bigquery.Client(project='polaris-analytics-prod')
    query = f"""
    SELECT COUNT(DISTINCT worker_id) as count
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE job_code = '{smart_code}'
    """
    
    result = list(client.query(query))[0]
    print(f"✓ Active:   {result.count} employees")

# Usage
validate_job_code("1-993-1026")
```

---

## Common Job Codes by Department

### Store Management
- `1-993-1026` - Store Manager
- `1-993-1014` - Assistant Store Manager  
- `1-993-1074` - Department Manager
- `6-10-812` - Sales Associate

### Support Services
- `1-993-3001` - Loss Prevention Manager
- `1-993-2015` - Facilities Manager
- `1-993-2014` - Pharmacy Manager

**For complete list:** See [job_codes_master.json](../../../../job_codes_master.json)

---

## Troubleshooting

### "Job Code Not Found in Polaris"
This means no one is currently scheduled with that job code. Try:
```python
# Check if it exists in master
if code in job_codes_master:
    print("Code is valid but no one assigned today")
else:
    print("Code doesn't exist - check spelling")
```

### "I want the actual User ID, not a representative"
Query Polaris to get real worker_ids:
```python
query = """
SELECT DISTINCT worker_id
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code = '1-993-1026'
LIMIT 1  -- Get first one
"""
```

### "Access Denied to Polaris Project"
You may need cross-project permissions. Ask your GCP admin for:
- `roles/bigquery.dataViewer` in `polaris-analytics-prod`

---

## Key Formulas for Spreadsheets

### Excel VLOOKUP for Job Code Names
```excel
=VLOOKUP(A2, IMPORTJSON("https://..."), 2, FALSE)
```

### Google Sheets: Import from Master
Use Google Apps Script to load job_codes_master.json and create lookup functions.

---

## Files & Resources

| File | Purpose |
|------|---------|
| [job_codes_master.json](../../../../job_codes_master.json) | Master lookup (44,934 lines) |
| [Complete Guide](./README.md) | Full technical documentation |
| [AMP Integration](../04-AMP-Specific/) | How we use job codes in AMP |
| [Datasource Reference](../../Datasource/BigQuery/README.md) | All available tables |

---

## Still Need Help?

**Check the complete guide:** [Job Codes Discovery & Bridge Guide](./README.md)

Or see related Quick-Start guides:
- [BigQuery Getting Started](../01-Getting-Started/)
- [Authentication Setup](../02-Authentication/)
