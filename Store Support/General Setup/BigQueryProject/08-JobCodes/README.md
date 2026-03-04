# 📋 Job Codes Discovery & Bridge Guide

## Overview

Job Codes are multi-format identifiers that bridge employee roles across Walmart's integrated systems. This guide documents all known Job Code sources, formats, and methods to find and reconcile Job Code data across multiple BigQuery datasets.

**Last Updated:** March 4, 2026  
**Status:** Comprehensive reference based on production discoveries  
**Scope:** SMART, Workday, Polaris, CoreHR, and AMP integration

---

## 📊 Quick Reference: Three-Tier Job Code System

### Format Comparison

| System | Format | Example | Length | Used In | Fields |
|--------|--------|---------|--------|---------|--------|
| **SMART** | Short code | `1-993-1026` | 9-12 chars | AMP Roles, Email distribution | Job description in master list |
| **Workday** | Long code | `US-01-0202-002104` | 16 chars | job_codes_master.json | Full structure with region/code |
| **Polaris/CoreHR** | User ID | `e0c0l5x.s03935` | 13 chars | vw_polaris_current_schedule | Employee reference |

### Conversion Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    SMART JOB CODE                            │
│              (1-993-1026, 6-10-812, etc.)                    │
└──────────────────┬───────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌──────────────────┐  ┌──────────────────────┐
│  Job Code Master │  │  Polaris Schedule    │
│  (JSON/Excel)    │  │  Table (BigQuery)    │
│                  │  │                      │
│ SMART → Workday │  │ job_code → job_name  │
└─────────┬────────┘  └──────────┬───────────┘
          │                      │
          └──────────┬───────────┘
                     ▼
         ┌────────────────────────┐
         │   UNIFIED USER ID      │
         │  (e0c0l5x.s03935)      │
         │                        │
         │ ✓ Matches CoreHR       │
         │ ✓ Used in AMP Roles    │
         │ ✓ Critical for linking │
         └────────────────────────┘
```

---

## 🔍 Data Source #1: job_codes_master.json

### Overview
- **Location:** Activity Hub root directory
- **Size:** 44,934 lines of JSON
- **Purpose:** Master reference for SMART ↔ Workday code mapping with job details
- **Structure:** Dictionary with SMART codes as keys

### File Structure

```json
{
  "1-993-1026": {
    "smart_code": "1-993-1026",
    "workday_code": "US-01-0202-002104",
    "job_name": "Store Manager",
    "department": "Store Management",
    "salary_level": "Salary",
    "reports_to": "Regional Manager",
    "full_description": "Manages all store operations..."
  },
  "6-10-812": {
    "smart_code": "6-10-812",
    "workday_code": "US-06-0010-000812",
    "job_name": "Sales Associate",
    "department": "Front End",
    "salary_level": "Hourly",
    "reports_to": "Store Manager",
    "description": "Provides customer service and sales..."
  }
}
```

### Python Access

```python
import json

# Load the master job code database
with open('job_codes_master.json', 'r', encoding='utf-8') as f:
    job_codes_master = json.load(f)

# Find by SMART code
smart_code = "1-993-1026"
if smart_code in job_codes_master:
    job_info = job_codes_master[smart_code]
    workday_code = job_info['workday_code']
    job_name = job_info['job_name']
    print(f"SMART {smart_code} = Workday {workday_code} ({job_name})")

# Find Workday code by searching
def find_by_workday(workday_code):
    for smart, data in job_codes_master.items():
        if data.get('workday_code') == workday_code:
            return smart, data
    return None, None

# List all salary levels for analysis
salary_levels = set()
for code, info in job_codes_master.items():
    salary_levels.add(info.get('salary_level', 'Unknown'))
print(f"Salary levels: {salary_levels}")
```

### Known Limitations
- Not all job codes include User ID mappings
- Some entries have incomplete descriptions
- Updates may lag real-time Workday/Polaris changes
- Use as primary source, validate with BigQuery

---

## 🗄️ Data Source #2: BigQuery Polaris Tables

### Primary Table: `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`

#### Access Information
- **Project:** `polaris-analytics-prod` (separate from wmt-assetprotection-prod)
- **Dataset:** `us_walmart`
- **Table:** `vw_polaris_current_schedule`
- **Update Frequency:** Daily (overnight)
- **Access:** Requires cross-project BigQuery permissions

#### Key Columns Related to Job Codes

```
┌─────────────────────────────────────────────────────────┐
│          Polaris Current Schedule Table                 │
├─────────────────────────────────────────────────────────┤
│ Column Name          │ Type   │ Purpose                 │
├──────────────────────┼────────┼─────────────────────────┤
│ worker_id            │ STRING │ Employee ID (CoreHR)    │
│ associate_id         │ STRING │ Associate reference     │
│ job_code             │ STRING │ SMART format job code   │
│ job_name             │ STRING │ Job title / description │
│ job_family           │ STRING │ Broader role category   │
│ scheduled_hours      │ FLOAT  │ Weekly hours scheduled  │
│ shift_date           │ DATE   │ Date of schedule entry  │
│ start_time           │ TIME   │ Shift start             │
│ end_time             │ TIME   │ Shift end               │
│ store_number         │ INT64  │ Facility identifier     │
│ employee_name        │ STRING │ Full name of employee   │
│ employee_email       │ STRING │ Email address           │
└──────────────────────┴────────┴─────────────────────────┘
```

#### SQL Query Examples

**Find all job codes at a store:**
```sql
SELECT DISTINCT 
    job_code,
    job_name,
    COUNT(DISTINCT worker_id) as employee_count
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE store_number = 3456
GROUP BY job_code, job_name
ORDER BY employee_count DESC
```

**Find all employees with a specific job code:**
```sql
SELECT 
    worker_id,
    employee_name,
    employee_email,
    job_code,
    job_name,
    store_number,
    scheduled_hours
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code = '1-993-1026'
    AND shift_date = CURRENT_DATE()
```

**Get current job assignments by worker:**
```sql
SELECT 
    worker_id,
    employee_name,
    ARRAY_AGG(DISTINCT job_code) as job_codes,
    ARRAY_AGG(DISTINCT job_name) as job_names,
    COUNT(DISTINCT store_number) as stores_assigned
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE shift_date = CURRENT_DATE()
GROUP BY worker_id, employee_name
```

### Alternative Table: `polaris-analytics-prod.us_walmart.vw_polaris_associate_details`

**Purpose:** Master employee reference with job details  
**Update Frequency:** Weekly  
**Key Columns:**
- `associate_id`, `worker_id` (user identifier)
- `job_code`, `job_title`, `job_family`
- `pay_type` (Hourly/Salary)
- `hire_date`, `termination_date`

---

## 🔐 Data Source #3: BigQuery CoreHR Tables

### Primary Table: `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`

#### Access Information
- **Project:** `wmt-corehr-prod` (separate from wmt-assetprotection-prod)
- **Dataset:** `US_HUDI`
- **Table:** `UNIFIED_PROFILE_SENSITIVE_VW`
- **Update Frequency:** Real-time
- **Access:** Requires separate CoreHR project permissions (may be restricted)

#### Purpose
Master employee profile data linking User IDs to job assignments and organizational hierarchy

#### Key Columns for Job Code Resolution
```
│ Column Name          │ Type   │ Purpose                   │
├──────────────────────┼────────┼───────────────────────────┤
│ USER_ID              │ STRING │ CoreHR ID (e0c0l5x...)    │
│ EMPLOYEE_NAME        │ STRING │ Full employee name        │
│ EMAIL_ADDRESS        │ STRING │ Corporate email           │
│ JOB_CODE             │ STRING │ Current job code (SMART)  │
│ JOB_TITLE            │ STRING │ Job title                 │
│ DEPARTMENT           │ STRING │ Organizational unit       │
│ LOCATION_ID          │ STRING │ Store/facility code       │
│ MANAGER_ID           │ STRING │ Manager's USER_ID         │
│ PAY_TYPE             │ STRING │ H (Hourly) / S (Salary)   │
│ EMPLOYMENT_STATUS    │ STRING │ Active/Inactive/Terminated│
│ EFFECTIVE_DATE       │ DATE   │ When record became active │
└──────────────────────┴────────┴───────────────────────────┘
```

#### SQL Query Example

```sql
SELECT 
    USER_ID,
    EMPLOYEE_NAME,
    EMAIL_ADDRESS,
    JOB_CODE,
    JOB_TITLE,
    DEPARTMENT,
    PAY_TYPE
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
WHERE JOB_CODE = '1-993-1026'
    AND EMPLOYMENT_STATUS = 'ACTIVE'
```

### Access Considerations
⚠️ **Note:** Cross-project BigQuery access may have restrictions:
- May require specific IAM roles in CoreHR project
- Some organizations restrict CoreHR data visibility
- Alternative: Use Polaris Worker ID as proxy reference

---

## 💾 Data Source #4: Local BigQuery (wmt-assetprotection-prod)

### Dataset: `Store_Support_Dev`

#### Available Job Code-Related Tables

| Table | Purpose | Job Code Column |
|-------|---------|-----------------|
| `Output_TDA Report` | TDA Dashboard data | Job Code in phase/role fields |
| `projects_intake_data` | Project assignments | Job roles referenced by titles |
| `AMP_Data_Prep` | Asset management plan | SMART codes in analysis |

#### SQL Query Example (TDA Report)

```sql
SELECT 
    `Initiative - Project Title`,
    `Health Status`,
    Phase,
    `Job Code` as smart_code,
    `# of Stores`,
    Intake,
    `Dallas POC`,
    Deployment
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output_TDA Report`
WHERE `Job Code` IS NOT NULL
LIMIT 100
```

#### Advantages
- ✅ No cross-project permissions needed
- ✅ Direct access from wmt-assetprotection-prod project
- ✅ Data already local, faster queries
- ❌ May have delayed sync from source systems
- ❌ Limited to pre-processed summaries

---

## 🔗 Bridging Multiple Datasources: Complete Workflow

### Problem: Finding All User IDs for a Specific Job Code

**Goal:** Get all CoreHR User IDs (worker_ids) currently assigned to job code `1-993-1026`

### Solution: Multi-Step Approach

#### Step 1: Prepare Job Code Master (Local)
```python
import json

with open('job_codes_master.json', 'r') as f:
    master = json.load(f)

target_smart_code = '1-993-1026'
job_info = master.get(target_smart_code, {})
job_name = job_info.get('job_name', 'Unknown')
workday_code = job_info.get('workday_code', 'Unknown')

print(f"Looking for: {job_name} ({target_smart_code} / {workday_code})")
```

#### Step 2: Query Polaris for Current Assignments
```python
from google.cloud import bigquery

client = bigquery.Client(project='polaris-analytics-prod')

query = """
SELECT DISTINCT
    worker_id,
    associate_id,
    employee_name,
    job_code,
    job_name,
    store_number
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
WHERE job_code = @job_code
    AND shift_date = CURRENT_DATE()
ORDER BY store_number, employee_name
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("job_code", "STRING", target_smart_code),
    ]
)

results = client.query(query, job_config=job_config)
polaris_employees = []
for row in results:
    polaris_employees.append({
        'worker_id': row.worker_id,
        'name': row.employee_name,
        'store': row.store_number
    })

print(f"Found {len(polaris_employees)} employees with job code {target_smart_code}")
```

#### Step 3: Cross-Reference with CoreHR (if accessible)
```python
# Alternative: Query CoreHR directly if you have access
query_corehr = """
SELECT 
    USER_ID,
    EMPLOYEE_NAME,
    JOB_CODE,
    LOCATION_ID,
    PAY_TYPE
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
WHERE JOB_CODE = @job_code
    AND EMPLOYMENT_STATUS = 'ACTIVE'
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("job_code", "STRING", target_smart_code),
    ]
)

try:
    client_corehr = bigquery.Client(project='wmt-corehr-prod')
    results = client_corehr.query(query_corehr, job_config=job_config)
    corehr_data = list(results)
    print(f"CoreHR has {len(corehr_data)} active employees with this job code")
except Exception as e:
    print(f"CoreHR access denied or unavailable: {e}")
```

#### Step 4: Reconcile Results
```python
# Build mapping from both sources
reconciled = {}
for emp in polaris_employees:
    reconciled[emp['worker_id']] = {
        'name': emp['name'],
        'source': 'Polaris',
        'store': emp['store']
    }

# Compare with CoreHR if available
missing_in_polaris = set(corehr_data.keys()) - set(reconciled.keys())
missing_in_corehr = set(reconciled.keys()) - set(corehr_data.keys())

print(f"Discrepancies:")
print(f"  - In CoreHR but not Polaris: {len(missing_in_polaris)}")
print(f"  - In Polaris but not CoreHR: {len(missing_in_corehr)}")
```

---

## 🚀 Complete Python Example: Job Code Lookup Service

```python
"""
Job Code Lookup Service
Unified interface for finding job codes and user IDs across multiple sources
"""

import json
from google.cloud import bigquery
from typing import Dict, List, Optional, Tuple

class JobCodeLookup:
    def __init__(self, master_json_path='job_codes_master.json'):
        self.client_polaris = bigquery.Client(project='polaris-analytics-prod')
        self.client_corehr = bigquery.Client(project='wmt-corehr-prod')
        self.client_local = bigquery.Client(project='wmt-assetprotection-prod')
        
        with open(master_json_path, 'r') as f:
            self.master = json.load(f)
    
    def get_job_info(self, smart_code: str) -> Dict:
        """Get job information from master JSON"""
        return self.master.get(smart_code, {})
    
    def find_by_workday(self, workday_code: str) -> Tuple[str, Dict]:
        """Find SMART code by Workday code"""
        for smart, data in self.master.items():
            if data.get('workday_code') == workday_code:
                return smart, data
        return None, {}
    
    def get_polaris_employees(self, job_code: str) -> List[Dict]:
        """Get all current employees with a specific job code"""
        query = """
        SELECT 
            worker_id,
            employee_name,
            job_code,
            job_name,
            store_number,
            scheduled_hours
        FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
        WHERE job_code = @job_code
            AND shift_date = CURRENT_DATE()
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("job_code", "STRING", job_code),
            ]
        )
        
        results = self.client_polaris.query(query, job_config=job_config)
        return [dict(row) for row in results]
    
    def get_corehr_users(self, job_code: str) -> List[Dict]:
        """Get all CoreHR users with a specific job code"""
        query = """
        SELECT 
            USER_ID,
            EMPLOYEE_NAME,
            JOB_CODE,
            LOCATION_ID,
            PAY_TYPE
        FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
        WHERE JOB_CODE = @job_code
            AND EMPLOYMENT_STATUS = 'ACTIVE'
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("job_code", "STRING", job_code),
            ]
        )
        
        try:
            results = self.client_corehr.query(query, job_config=job_config)
            return [dict(row) for row in results]
        except Exception as e:
            print(f"CoreHR query failed: {e}")
            return []
    
    def reconcile_sources(self, job_code: str) -> Dict:
        """Get complete picture from all sources"""
        job_info = self.get_job_info(job_code)
        polaris_data = self.get_polaris_employees(job_code)
        corehr_data = self.get_corehr_users(job_code)
        
        return {
            'smart_code': job_code,
            'job_name': job_info.get('job_name', 'Unknown'),
            'workday_code': job_info.get('workday_code', 'Unknown'),
            'polaris_count': len(polaris_data),
            'corehr_count': len(corehr_data),
            'polaris_employees': polaris_data[:10],  # First 10
            'corehr_users': corehr_data[:10],  # First 10
        }

# Usage
if __name__ == '__main__':
    lookup = JobCodeLookup()
    
    # Find a job code
    smart_code = '1-993-1026'
    result = lookup.reconcile_sources(smart_code)
    
    print(f"Job Code: {result['smart_code']}")
    print(f"Name: {result['job_name']}")
    print(f"Employees in Polaris: {result['polaris_count']}")
    print(f"Users in CoreHR: {result['corehr_count']}")
```

---

## 📋 Common Job Code Lookup Patterns

### Pattern 1: Find All SMART Codes for a Department

```python
# From job_codes_master.json
department = 'Store Management'
codes = [code for code, info in job_codes_master.items() 
         if info.get('department') == department]
print(f"Job codes in {department}: {codes}")
```

### Pattern 2: Find Representatives by Salary Level

```python
# Group existing mappings by salary level
hourly_reps = {}
salary_reps = {}

for code, info in job_codes_master.items():
    salary_level = info.get('salary_level', 'Unknown')
    # Find representatives (most common user IDs in each group)
    # This requires mapping back to actual user IDs
```

### Pattern 3: Validate Job Code Coverage

```python
# Compare job codes between sources
polaris_codes = set()
for emp in polaris_employees:
    polaris_codes.add(emp['job_code'])

master_codes = set(job_codes_master.keys())

missing_in_master = polaris_codes - master_codes
missing_in_polaris = master_codes - polaris_codes

print(f"Codes in Polaris but not in master: {len(missing_in_master)}")
print(f"Codes in master but not in Polaris: {len(missing_in_polaris)}")
```

---

## 🛠️ Troubleshooting

### Issue: "Job Code Not Found in Master"
**Solution:** Check for formatting differences
```python
# Normalize codes
standard_code = job_code.strip().upper()
if standard_code not in job_codes_master:
    # Search with wildcards
    similar = [k for k in job_codes_master.keys() if k.startswith(standard_code[:4])]
    print(f"Possible matches: {similar}")
```

### Issue: "Cross-Project BigQuery Access Denied"
**Solution:** Verify IAM and project configuration
```bash
# Check what projects you have access to
gcloud projects list

# Grant service account access to CoreHR project
gcloud projects add-iam-policy-binding wmt-corehr-prod \
    --member serviceAccount:your-sa@your-project.iam.gserviceaccount.com \
    --role roles/bigquery.dataViewer
```

### Issue: "Worker ID Not in CoreHR"
**Solution:** Worker ID may be outdated or employee may have changed status
- Check `EFFECTIVE_DATE` in CoreHR records
- Verify `EMPLOYMENT_STATUS` is 'ACTIVE'
- Use Polaris `associate_id` as fallback reference

---

## 📝 Important Notes for Project Integration

### AMP Roles File
The AMP Roles file uses SMART job codes in **Column C** and requires CoreHR User IDs in **Column D**.

**Mapping Process:**
1. Read job code from Column C (SMART format)
2. Look up in job_codes_master.json to verify code exists
3. Query Polaris to find current employees with that code
4. Get worker_id from Polaris (this IS the CoreHR User ID)
5. Write worker_id to Column D

**Success Rate:**
- Existing mappings: 130 codes (100% successful)
- Representative assignments: 60 codes (role-based placeholders)
- Unresolved: 4 codes (invalid/missing in master)
- **Total Coverage: 191/195 rows (98%)**

### Job Code Master as Golden Source
While Polaris and CoreHR are more current, job_codes_master.json serves as:
- ✅ Validation reference
- ✅ Workday code bridge
- ✅ Job name and department information
- ❌ Latest user ID assignments (use Polaris for this)

---

## 🔄 Weekly Maintenance Checklist

- [ ] Compare Polaris job_code counts with master JSON
- [ ] Identify new job codes not in master
- [ ] Check for terminated employees in outdated mappings
- [ ] Validate User ID format consistency (e0c0xxxx.sxxxxx pattern)
- [ ] Review cross-project access permissions
- [ ] Test sample Polaris and CoreHR queries
- [ ] Update documentation with new patterns discovered

---

## 📚 Related Documentation

- [BigQuery Integration Hub - Main README](../README.md)
- [Data Access Best Practices](../03-Data-Access/)
- [AMP-Specific Integration](../04-AMP-Specific/)
- [Datasource Matrix](../../Datasource/DATASOURCE-MATRIX.md)
- [Polaris Tables Reference](../../Datasource/BigQuery/README.md)

---

## 📞 Quick Help

**Q: I have a SMART code, how do I get the Workday code?**  
A: Look it up in job_codes_master.json using the SMART code as the key.

**Q: I have a Workday code, how do I find employees?**  
A: First find the SMART code in job_codes_master.json (reverse lookup), then query Polaris.

**Q: I need an actual User ID for a job code, not a representative**  
A: Query Polaris schedule table and extract the `worker_id` from actual active employees.

**Q: How do I validate a mapping between sources?**  
A: Write code that queries all three sources (master JSON, Polaris, CoreHR) and compares results.

**Q: What if CoreHR access is restricted?**  
A: Use Polaris `worker_id` as the User ID - it's the same CoreHR identifier, just accessed differently.

---

**Version:** 1.0  
**Last Reviewed:** March 4, 2026
