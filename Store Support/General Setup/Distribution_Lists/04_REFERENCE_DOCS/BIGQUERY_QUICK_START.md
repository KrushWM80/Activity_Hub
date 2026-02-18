# BigQuery Quick Start Guide

## Your Configuration
- **Project**: `wmt-assetprotection-prod`
- **Dataset**: `Store_Support_Dev`
- **Table**: `dl_catalog`
- **Full Path**: `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`

---

## Step 1: Create the Table (One-Time Setup)

### Option A: Using BigQuery Console (Easiest)
1. Go to https://console.cloud.google.com/bigquery
2. Select project: `wmt-assetprotection-prod`
3. Click on dataset: `Store_Support_Dev`
4. Click "CREATE TABLE"
5. Configure:
   - **Source**: Upload → Browse to `all_distribution_lists.csv`
   - **File format**: CSV
   - **Table name**: `dl_catalog`
   - **Schema**: Auto-detect ✓
   - **Header rows to skip**: 1
   - **Write preference**: Overwrite table
6. Click "CREATE TABLE"

### Option B: Using SQL (Console Query)
```sql
CREATE TABLE IF NOT EXISTS `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog` (
    email STRING NOT NULL,
    name STRING NOT NULL,
    display_name STRING,
    description STRING,
    member_count INT64,
    category STRING,
    last_updated TIMESTAMP NOT NULL,
    extraction_date DATE NOT NULL
);
```

Then upload the CSV via Console UI or use gcloud command below.

---

## Step 2: Initial Data Load

### Using gcloud CLI (Recommended)
```powershell
# Make sure you're in the correct directory
cd "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists"

# Upload the CSV to BigQuery
bq load `
  --project_id=wmt-assetprotection-prod `
  --replace `
  --skip_leading_rows=1 `
  --autodetect `
  Store_Support_Dev.dl_catalog `
  all_distribution_lists.csv
```

### Using PowerShell Script
```powershell
.\upload_to_bigquery_simple.ps1
```
(Already configured with your project/dataset values)

---

## Step 3: Verify the Upload

### Check row count:
```sql
SELECT COUNT(*) as total 
FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`;
```
**Expected**: 134,681 rows

### Check categories:
```sql
SELECT category, COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
GROUP BY category
ORDER BY count DESC;
```

### View sample data:
```sql
SELECT email, name, member_count, category
FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
ORDER BY member_count DESC
LIMIT 10;
```

---

## Step 4: Grant Code Puppy Access

If Code Puppy needs to query this table, grant its service account read permission:

```bash
gcloud projects add-iam-policy-binding wmt-assetprotection-prod \
    --member="serviceAccount:YOUR_CODEPUPPY_SERVICE_ACCOUNT@wmt-assetprotection-prod.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"
```

(Ask your Code Puppy admin for the service account email)

---

## Step 5: Query from Code Puppy

### Backend API Endpoint (Node.js example):
```javascript
const { BigQuery } = require('@google-cloud/bigquery');
const bigquery = new BigQuery({ projectId: 'wmt-assetprotection-prod' });

async function getDistributionLists(req, res) {
    const query = `
        SELECT email, name, display_name, description, member_count, category
        FROM \`wmt-assetprotection-prod.Store_Support_Dev.dl_catalog\`
        ORDER BY name
    `;
    
    const [rows] = await bigquery.query(query);
    res.json(rows);
}
```

### Update your index.html:
```javascript
async function loadDistributionLists() {
    try {
        // Replace CSV loading with API call
        const response = await fetch('/api/distribution-lists');
        const data = await response.json();
        
        allDLs = data.map(row => ({
            email: row.email,
            name: row.name,
            displayName: row.display_name,
            description: row.description,
            memberCount: row.member_count,
            category: row.category
        }));
        
        displayDLs();
    } catch (error) {
        console.error('Error loading from BigQuery:', error);
    }
}
```

---

## Daily Updates

### Option 1: Schedule PowerShell Script (Simplest)
Add to your Windows Task Scheduler (daily at 5:10 AM):

```powershell
# Run after DL extraction completes
cd "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists"
.\upload_to_bigquery_simple.ps1
```

### Option 2: Modify Existing Schedule
Update `schedule_with_upload.ps1` to include:

```powershell
Write-Log "Step 3: Uploading to BigQuery..."
try {
    .\upload_to_bigquery_simple.ps1
    Write-Log "BigQuery upload completed successfully"
} catch {
    Write-Log "ERROR: BigQuery upload failed - $($_.Exception.Message)"
}
```

---

## Useful Commands

### Check table info:
```powershell
bq show --format=prettyjson wmt-assetprotection-prod:Store_Support_Dev.dl_catalog
```

### Get row count quickly:
```powershell
bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`'
```

### Export to CSV:
```powershell
bq extract --destination_format=CSV wmt-assetprotection-prod:Store_Support_Dev.dl_catalog gs://your-bucket/export.csv
```

---

## Troubleshooting

### "Table not found"
- Check project name is exactly: `wmt-assetprotection-prod`
- Check dataset name is exactly: `Store_Support_Dev`
- Verify you have access to this project

### "Permission denied"
- Run: `gcloud auth application-default login`
- Or verify your service account has BigQuery Admin/Data Editor role

### "Cannot upload CSV"
- Verify file exists: `Test-Path all_distribution_lists.csv`
- Check file size: `(Get-Item all_distribution_lists.csv).Length / 1MB` MB
- Make sure CSV has headers in first row

---

## Cost Estimate
- **Storage**: 15MB × $0.02/GB/month = **$0.0003/month**
- **Queries**: Full scan × $5/TB = **$0.00007/query**
- **Total monthly**: < **$1.00**

Very affordable! 💰
