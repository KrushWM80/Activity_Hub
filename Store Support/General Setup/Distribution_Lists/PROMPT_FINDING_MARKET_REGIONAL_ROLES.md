# Prompt for Finding Position Data by Role Type

## Workspace Structure

**Base Directory:** `C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists`

**Folder Organization:**
- `02_SCRIPTS_AND_TOOLS/` - Python and PowerShell extraction/analysis scripts
- `03_SOURCE_DATA/` - Raw data files (AD CSV extracts, BigQuery exports)
- `01_ANALYSIS_REPORTS/` - Analysis results and summary documents
- `04_REFERENCE_DOCS/` - Documentation and reference guides
- Root directory - Current/working data files (e.g., `ad_groups_*.csv`)

## Task Overview
This is a **general-purpose methodology** for finding job codes and extracting user data for ANY role type in the organization. The example below focuses on Home Office or Market Level positions (regional and market fulfillment/digital operations leadership roles), but the same approach works for:

- **Any department** (Finance, HR, IT, Merchandising, etc.)
- **Any level** (Individual Contributor, Manager, Director, VP, SVP, etc.)
- **Any role type** (Store Manager, Coach, Asset Protection, People Lead, etc.)

Simply modify the search patterns and job title keywords to match your target roles.

## Data Sources

### **IMPORTANT: Source of Truth Hierarchy**

1. **PRIMARY SOURCE (Source of Truth for Job Codes):**
   - `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` - HR/Employee master data
   - `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule` - Store scheduling/assignments
   
   **These BigQuery tables are the authoritative source for:**
   - Job Codes (accurate, up-to-date)
   - Position details
   - Employment status
   - Organizational hierarchy

2. **SECONDARY SOURCE (For Group Membership & Quick Lookups):**
   - **Location:** Root directory or `03_SOURCE_DATA/`
   - **Filename Pattern:** `ad_groups_YYYYMMDD_HHMMSS.csv` (extracted from Active Directory)
   - **Extraction Script:** `02_SCRIPTS_AND_TOOLS/ad_group_extractor.py`
   
   **AD Groups are useful for:**
   - Finding who belongs to which security/distribution groups
   - Quick initial queries
   - Windows authentication integration
   
   **⚠️ LIMITATION:** AD data may not have complete or current job codes. Always validate job codes against BigQuery tables.

### **Scripts for Data Access:**
- **BigQuery Queries:** `02_SCRIPTS_AND_TOOLS/query_hnmeeting2_bigquery.py`, `check_polaris_schema.py`, `check_unified_profile_structure.py`
- **AD Extraction:** `02_SCRIPTS_AND_TOOLS/ad_group_extractor.py`
- **Data Validation:** `02_SCRIPTS_AND_TOOLS/merge_workday_data.py`, `find_email_win_mapping.py`

### CSV Structure (from AD extraction)
The CSV file contains the following columns (may not have headers):
- Group
- UserID
- Email
- Name
- JobTitle
- Department
- CostCenter1
- **JobCode** ⚠️ (may be incomplete - verify with BigQuery)
- EmployeeID
- Field10
- Location
- Status
- Field13
- Field14

## Step 1: Identify Relevant Job Codes (Using BigQuery - Source of Truth)

**RECOMMENDED: Query BigQuery directly for accurate job codes**

```sql
-- Get all unique job codes for Market/Regional leadership roles
SELECT DISTINCT
    employmentInfo.positionInfo[0].jobCode AS JobCode,
    employmentInfo.positionInfo[0].jobTitle AS JobTitle,
    employmentInfo.positionInfo[0].businessUnitType AS LocationType,
    COUNT(*) AS EmployeeCount
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
WHERE employmentInfo.isActive = true
    AND (
        employmentInfo.positionInfo[0].jobTitle LIKE '%Market%Lead%'
        OR employmentInfo.positionInfo[0].jobTitle LIKE '%Regional%Lead%'
        OR employmentInfo.positionInfo[0].jobTitle LIKE '%Digital%Lead%'
        OR employmentInfo.positionInfo[0].jobTitle LIKE '%Fulfillment%Lead%'
        OR employmentInfo.positionInfo[0].jobTitle LIKE '%Director%Regional%'
    )
GROUP BY JobCode, JobTitle, LocationType
ORDER BY JobCode
```

**ALTERNATIVE: Quick lookup from AD CSV (may be incomplete)**

```powershell
# Navigate to workspace if needed
cd "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists"

# Search for specific role types in job titles
# Use the most recent ad_groups CSV file in root or 03_SOURCE_DATA/
$data = Import-Csv "ad_groups_YYYYMMDD_HHMMSS.csv" -Header @("Group","UserID","Email","Name","JobTitle","Department","CostCenter1","JobCode","EmployeeID","Field10","Location","Status","Field13","Field14")

# Find unique job codes - NOTE: These should be validated against BigQuery
$data | Where-Object { $_.JobTitle -match 'Market.*Lead|Regional.*Lead|Digital.*Lead|Fulfillment.*Lead|Director.*Regional' } | Select-Object JobCode, JobTitle -Unique | Sort-Object JobCode
```

### Example: Common Job Codes for Market/Regional Leadership:
- **814451** - Digital Operations Lead / Market Fulfillment Lead
- **814732** - Market Fulfillment Lead - Neighborhood Markets  
- **890097** - Director, Regional Fulfillment
### **Option A: Query BigQuery Directly (RECOMMENDED - Most Accurate)**

```sql
-- Extract all users with specific job codes from source of truth
SELECT
    personalInfo.legalName.firstName AS FirstName,
    personalInfo.legalName.lastName AS LastName,
    contactInfo.emailInfo[0].emailAddress AS Email,
    employmentInfo.positionInfo[0].jobCode AS JobCode,
    employmentInfo.positionInfo[0].jobTitle AS JobTitle,
    employmentInfo.positionInfo[0].businessUnitName AS Department,
    employmentInfo.positionInfo[0].businessUnitType AS LocationType,
    employmentInfo.positionInfo[0].employmentStatus AS Status
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
WHERE emploValidate Job Codes (If Using AD Data)

If you started with AD CSV data, validate the job codes against BigQuery:

```python
# Python script to validate and enrich AD data with BigQuery
# Save this in 02_SCRIPTS_AND_TOOLS/ or run from workspace root
import os
os.chdir(r'C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists')

from google.cloud import bigquery
import pandas as pd

client = bigquery.Client(project='wmt-assetprotection-prod')

# Read AD CSV from root directory
ad_data = pd.read_csv('ad_groups_YYYYMMDD_HHMMSS.csv')

# Get employee numbers or emails to match
emails = ad_data['email'].tolist()

# Query BigQuery for authoritative job codes
query = f"""
SELECT
    contactInfo.emailInfo[0].emailAddress AS Email,
    employmentInfo.positionInfo[0].jobCode AS JobCode,
    employmentInfo.positionInfo[0].jobTitle AS JobTitle
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
WHERE contactInfo.emailInfo[0].emailAddress IN UNNEST(@emails)
    AND employmentInfo.isActive = true
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ArrayQueryParameter("emails", "STRING", emails)
    ]
)

bq_data = client.query(query, job_config=job_config).to_dataframe()

# Merge and compare
merged = pd.merge(ad_data, bq_data, on='Email', suffixes=('_AD', '_BQ'))
merged['JobCodeMatch'] = merged['JobCode_AD'] == merged['JobCode_BQ']

# Show discrepancies
discrepancies = merged[merged['JobCodeMatch'] == False]
print(f"Found {len(discrepancies)} job code mismatches between AD and BigQuery")
```

## Step 4: ymentInfo.isActive = true
    AND employmentInfo.positionInfo[0].jobCode IN ('814451', '814732', '890097')
    AND employmentInfo.positionInfo[0].businessUnitType = 'HO'  -- Home Office roles only
ORDER BY JobCode, LastName
```

### **Option B: Use AD CSV (Quick Lookup - Validate Job Codes)**

```powershell
# Navigate to workspace
cd "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists"

# Import CSV with proper headers (file typically in root or 03_SOURCE_DATA/)
$data = Import-Csv "ad_groups_YYYYMMDD_HHMMSS.csv" -Header @("Group","UserID","Email","Name","JobTitle","Department","CostCenter1","JobCode","EmployeeID","Field10","Location","Status","Field13","Field14")

# Filter for target job codes and roles
$filtered = $data | Where-Object { 
    $_.JobCode -in @('814451', '814732', '890097') -and 
    ($_.JobTitle -match 'Regional|Market|Digital|Fulfillment Lead|Director')
}

# Display results
$filtered | Select-Object Name, Email, JobCode, JobTitle, Department | Format-Table -AutoSize | Out-String -Width 300
```

**⚠️ IMPORTANT:** If using Option B (AD CSV), cross-reference results with BigQuery to ensure job codes are current.
# Example: Finance roles
$data | Where-Object { $_.JobTitle -match 'Finance|Controller|Accounting' } | Select-Object JobCode, JobTitle -Unique

# Example: IT/Technology roles
$data | Where-Object { $_.JobTitle -match 'Engineer|Developer|Architect|Technology' } | Select-Object JobCode, JobTitle -Unique
```

## Step 2: Extract User Data for These Roles

```powershell
# Import CSV with proper headers
$data = Import-Csv "ad_groups_YYYYMMDD_HHMMSS.csv" -Header @("Group","UserID","Email","Name","JobTitle","Department","CostCenter1","JobCode","EmployeeID","Field10","Location","Status","Field13","Field14")

# Filter for target job codes and roles
$filtered = $data | Where-Object { 
    $_.JobCode -in @('814451', '814732', '890097') -and 
    ($_.JobTitle -match 'Regional|Market|Digital|Fulfillment Lead|Director')
}

# Display results
$filtered | Select-Object Name, Email, JobCode, JobTitle, Department | Format-Table -AutoSize | Out-String -Width 300
```

## Step 3: Export Results (Optional)

```powershell
# Export to 01_ANALYSIS_REPORTS/ folder
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$outputPath = "01_ANALYSIS_REPORTS\Market_Regional_Leaders_$timestamp.csv"

$filtered | Select-Object Name, Email, JobCode, JobTitle, Department | Export-Csv $outputPath -NoTypeInformation

Write-Host "Results exported to: $outputPath"

# Or count by job code
$filtered | Group-Object JobCode | Select-Object Name, Count
```

## Role Categories for Any Role Type

Use these regex patterns as templates - **replace the keywords with your target role:**

### Example: Market/Regional Operations Roles
```regex
Market.*Lead|Regional.*Lead|Digital.*Lead|Fulfillment.*Lead
Director.*Regional|Regional.*Director
VP.*Regional|Regional.*VP
```

### Example: Store Operations Roles
```regex
Store Manager|Store Lead|Coach|Assistant.*Manager
Complex.*Manager|Supercenter.*Manager
```

### Example: Corporate/HO Roles by Level
```regex
# C-Level
Chief.*Officer|CEO|CFO|COO|CMO

# SVP Level
Senior Vice President|SVP

# VP Level
Vice President|VP|Divisional VP|DVP

# Director Level
Director|Senior Director|Group Director

# Manager Level
Manager|Senior Manager|Lead
```

### General Pattern Structure
```regex
[Role Title]|[Alternate Title]|[Level].*[Function]ad
- Regional Vice President
- VP, Regional General Manager

### Distinguishing Home Office vs Store Roles:

**Location Field (Field10 in CSV):**
- **HO** = Home Office - Field-based leadership roles (Market/Regional leads, Directors, etc.) that report to corporate
- **ST** = Store - Store-based positions (Store Managers, Department Managers, Associates, etc.)

**Job Code Ranges (general patterns):**
- **814xxx** - Market/Regional Operations roles (Market Fulfillment Lead, Digital Ops Lead, etc.)
- **890xxx** - Regional Director level roles
- **808xxx** - Market Managers (Supercenter/Neighborhood Market)
- **814454** - Market People Partners
- **800469** - Market Health & Wellness Directors

### How to Filter by Location Type:

```powershell
# Home Office roles ONLY
$hoRoles = $data | Where-Object { $_.Location -eq 'HO' }

# Store roles ONLY
$storeRoles = $data | Where-Object { $_.Location -eq 'ST' }

# Both HO and Store
$allRoles = $data | Where-Object { $_.Location -in @('HO', 'ST') }
```

### Other Identifying Characteristics:
- Status usually "A" (Active), "P" (Part-time), or "L" (Leave)
- HO roles often have broader geographic scope in Department field (Region, Market, Division)
- Store roles typically reference specific store numbers or locations

## Search Patterns

Use these regex patterns to find similar roles:

```regex
Market.*Lead|Regional.*Lead|Digital.*Lead|Fulfillment.*Lead
Director.*Regional|Regional.*Director
VP.*Regional|Regional.*VP
Market.*Fulfillment|Regional.*Fulfillment
Digital.*Operations.*Lead
```

## Quick Lookup Query

For ad-hoc searches by specific criteria:

```powershell
# Find all users with specific job code
$data | Where-Object { $_.JobCode -eq '814451' } | Select-Object Name, Email, JobTitle

# Find by job title pattern
$data | Where-Object { $_.JobTitle -like '*Digital Operations Lead*' } | Select-Object Name, Email, JobCode, Department

# Find by region/market in department
$data | Where-Object { $_.Department -match 'Region \d+|Market \d+' } | Select-Object Name, Email, JobTitle, Department
```

## Output Format

Standard output should include:
- Name
- Email
- Job Code
- Job Title
- Department/Region

This provides sufficient context to identify the role level and area of responsibility.
