# Workday Job Data Integration Guide

## Overview

Your extracted AD user data now includes `job_code` for each user. To add Workday job descriptions and job numbers, you need to map these job codes to Workday data.

## Current Data Status

✅ **Extracted from AD:**
- Job Code (wm-jobcode) - e.g., `800469`, `814450`, `808250`
- Position Code (wm-positioncode)
- Employee Number (wm-employeenumber)
- Business Unit Number
- Business Unit Type

⏳ **Still Needed from Workday:**
- Job Number (Workday identifier)
- Job Description (human-readable title)
- Job Family (optional, for grouping)
- Job Level (optional, for hierarchy)
- Grade (optional, for compensation)

## How to Get Workday Data

### Option 1: Request from HR/Workday Team (RECOMMENDED)

Contact your HR or Workday administrator and request:

**Email Template:**
```
Subject: Request for Job Master Data Export

Hi [HR/Workday Team],

We're building a distribution list tool and need to map job codes to job 
descriptions and job numbers. 

Can you please export the Workday Job Master with the following fields:
  • Job Code (Walmart ID: wm-jobcode)
  • Workday Job ID / Job Number
  • Job Title / Job Description
  • Job Family (optional)
  • Job Level (optional)
  • Grade (optional)

We have identified these job codes in our system:
  • 800469 (Director roles)
  • 814450 (Manager roles)
  • 808250 (Market Manager roles)
  • [etc.]

Please export as CSV with the job codes we're using.

Thanks!
```

**Expected output format:**
```csv
job_code,job_number,job_description,job_family,job_level,grade
800469,WD12345,Director of Market Operations,Management,Director,GR45
814450,WD12346,Market Manager,Field Operations,Manager,GR40
808250,WD12347,Market Manager Supercenter,Field Operations,Manager,GR40
```

### Option 2: Workday Portal Access

If you have Workday access:

1. **Login to Workday**
   - Go to https://wd3.myworkday.com (or your Workday instance)
   - Use your credentials

2. **Access Job Master Report**
   - Search for: "Job Master Report" or "Jobs Listing"
   - Or navigate: Menu → Workforce → Talent Management → Jobs

3. **Create Custom Report**
   - Add columns: Job Code, Job ID, Job Title, Job Family, Level
   - Filter by: Current jobs only
   - Export as CSV

4. **Save as CSV**
   - Export file and save as `workday_jobs.csv`

### Option 3: Workday API (Advanced)

If your organization has Workday API access:

```python
from workday_job_lookup import WorkdayAPILookup

# Configure API connection
lookup = WorkdayAPILookup(
    api_url="https://api.workday.com/v2",
    api_key="your_api_key_here"
)

# Connect and query
if lookup.connect():
    job = lookup.lookup_from_api("800469")
    print(f"Job: {job.job_description}")
```

Note: Requires Workday API setup and credentials from your IT team.

## Using the Merger Script

Once you have the Workday CSV:

### Step 1: Organize Files

```
C:\Users\krush\Documents\n├── ad_groups_20251215_154559.csv        (Your AD extraction)
├── workday_jobs.csv                     (Your Workday export)
├── merge_workday_data.py                (The script)
└── workday_job_lookup.py                (Helper module)
```

### Step 2: Run the Merger

```bash
cd C:\Users\krush\Documents
py merge_workday_data.py --ad-csv ad_groups_20251215_154559.csv --workday-csv workday_jobs.csv --output final_users_with_jobs.csv
```

Output:
```
+ Loaded 2684 users from ad_groups_20251215_154559.csv
+ Loaded 245 job codes from workday_jobs.csv
Merging 2684 users with Workday job data...
  Progress: 0/2684
  Progress: 200/2684
  Progress: 400/2684
  ...

+ Job matches found: 2650
+ Job codes not found in lookup: 34
+ Users without job code: 0

+ Exported 2684 merged users to final_users_with_jobs.csv
```

### Step 3: Review Results

Open `final_users_with_jobs.csv` in Excel:

| username | email | job_code | workday_job_number | workday_job_description |
|----------|-------|----------|-------------------|------------------------|
| mclary   | matthew.clary@walmart.com | 800469 | WD12345 | Director, Market H&W |
| a0a028b  | alland.anderson@walmart.com | 808250 | WD12347 | Market Manager |

## Troubleshooting

### Job codes not found

If you see "NOT_FOUND" in workday_job_number:

1. Check the job code format (should match exactly)
2. Verify Workday export includes all active job codes
3. Ensure CSV doesn't have trailing spaces
4. Some older job codes may be inactive in Workday

**Fix:**
```bash
# Clean up spaces in CSV
py -c "import csv; 
from pathlib import Path
with open('workday_jobs.csv') as f:
    r = csv.DictReader(f)
    rows = [{k.strip(): str(v).strip() for k,v in row.items()} for row in r]
with open('workday_jobs_clean.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
"
```

### Missing Workday data

If your organization doesn't have Workday Job Master export:

**Alternative: Use AD Title field**
```python
# Instead of job_description, use the title field
# Users will have: job_code + job_title (from AD)
# This is less detailed but still useful for distribution lists
```

## Next Steps After Merge

Once you have merged data:

1. **Update Distribution Lists**
   ```bash
   # Create DLs grouped by Job Description
   python create_distribution_list.ps1 --filter-by-job "Director" 
   ```

2. **Build Dashboard**
   - Show users grouped by job description
   - Filter by job family/level
   - Create DLs by job role

3. **Reporting**
   - Headcount by job level
   - Distribution by job family
   - Manager reports by job code

## Quick Reference

### Job Mapping CSV Format

**Minimum required columns:**
```csv
job_code,job_number,job_description
```

**Optional columns:**
```csv
job_code,job_number,job_description,job_family,job_level,grade
```

### Job Code Examples from Your Data

These are some of the job codes in your groups:
- **800469** - Director level roles
- **814450** - Asset Protection Manager roles
- **808250** - Market Manager Supercenter roles
- **814732** - Market Fulfillment Lead roles

These should be in your Workday export.

## Getting Help

- **Question about Workday access?** → Contact your HR IT team
- **Issue running the merge script?** → Check the error message and verify file format
- **Need to add more fields?** → Edit `workday_job_lookup.py` to add custom columns

---

**Status:** Awaiting Workday Job Master export
**Action Item:** Request from HR/Workday team
**Timeline:** Once you get the CSV, merge takes ~1 minute