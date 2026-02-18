# BigQuery Integration Setup Guide

## Overview
Instead of uploading a 15MB CSV to Code Puppy Pages, we'll store the distribution list data in BigQuery and query it dynamically.

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Daily 5AM Task │────▶│   BigQuery   │◀────│  Code Puppy UI  │
│  (Your Server)  │     │  DL Catalog  │     │  (Browser)      │
└─────────────────┘     └──────────────┘     └─────────────────┘
```

## Benefits

✅ **No file uploads** - Code Puppy queries BigQuery API directly
✅ **Always current** - Users see live data from BigQuery
✅ **Better performance** - Indexed queries, caching
✅ **Scalability** - Can handle millions of rows
✅ **Version history** - Track changes over time
✅ **Multi-access** - Other tools can use same data source

## Setup Steps

### 1. Prerequisites

- Access to Walmart's GCP project
- Service account with BigQuery permissions
- Python packages: `google-cloud-bigquery`

Install required packages:
```powershell
pip install google-cloud-bigquery google-auth
```

### 2. Configure BigQuery

Edit `upload_to_bigquery.py`:
```python
PROJECT_ID = "wmt-assetprotection-prod"  # Your GCP project ID
DATASET_ID = "Store_Support_Dev"          # Dataset name
TABLE_ID = "dl_catalog"                   # Table name
CREDENTIALS_FILE = "bigquery_credentials.json"  # Service account key
```

### 3. Get Service Account Credentials

1. Go to GCP Console → IAM & Admin → Service Accounts
2. Create or use existing service account
3. Grant roles:
   - BigQuery Data Editor
   - BigQuery Job User
4. Download JSON key file
5. Save as `bigquery_credentials.json` in this folder

### 4. Initial Upload

Run the upload script:
```powershell
python upload_to_bigquery.py
```

This will:
- Create dataset `distribution_lists`
- Create table `dl_catalog` with schema
- Load all 134,681 DLs from CSV
- Add timestamps for tracking

Expected output:
```
✓ BigQuery client created successfully
✓ Dataset Store_Support_Dev already exists
✓ Created table dl_catalog
✓ Successfully loaded 134,681 rows into BigQuery
  Table: wmt-assetprotection-prod.Store_Support_Dev.dl_catalog
  Size: 12.45 MB
```

### 5. Update Daily Scheduled Task

Modify `schedule_with_upload.ps1` to use BigQuery instead of CSV upload:

```powershell
# Replace the upload section with:
Write-Log "Step 3: Uploading to BigQuery..."
try {
    $uploadOutput = & python upload_to_bigquery.py 2>&1
    Write-Log $uploadOutput
    Write-Log "Upload to BigQuery completed successfully"
} catch {
    Write-Log "ERROR: BigQuery upload failed - $($_.Exception.Message)"
}
```

### 6. Update Code Puppy Pages HTML

The HTML needs to query BigQuery instead of loading CSV. Two approaches:

#### Option A: Backend Proxy (Recommended)
Create a simple API endpoint in Code Puppy that queries BigQuery server-side:

```javascript
// In Code Puppy's backend (Python/Node.js)
async function getDistributionLists() {
    const query = `
        SELECT email, name, display_name, description, member_count, category
        FROM \`wmt-assetprotection-prod.Store_Support_Dev.dl_catalog\`
        ORDER BY name
    `;
    const [rows] = await bigquery.query(query);
    return rows;
}
```

Then update `index.html`:
```javascript
// Replace loadDistributionLists() function
async function loadDistributionLists() {
    try {
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
        // ... rest of function
    } catch (error) {
        console.error('Error loading from BigQuery:', error);
    }
}
```

#### Option B: Direct Client Query (If Code Puppy allows)
If Code Puppy supports BigQuery client libraries in JavaScript:

```javascript
// Add BigQuery client library
import { BigQuery } from '@google-cloud/bigquery';

async function loadDistributionLists() {
    const bigquery = new BigQuery({
        projectId: 'wmt-assetprotection-prod',
        credentials: CODE_PUPPY_SERVICE_ACCOUNT
    });
    
    const query = `
        SELECT email, name, display_name, description, member_count, category
        FROM \`wmt-assetprotection-prod.Store_Support_Dev.dl_catalog\`
        ORDER BY name
    `;
    
    const [rows] = await bigquery.query(query);
    allDLs = rows;
    // ... rest of function
}
```

### 7. Grant Code Puppy Access

Grant your Code Puppy service account read access:

```bash
gcloud projects add-iam-policy-binding wmt-assetprotection-prod \
    --member="serviceAccount:codepuppy@wmt-assetprotection-prod.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"
```

## BigQuery Schema

```sql
CREATE TABLE `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog` (
    email STRING NOT NULL,
    name STRING NOT NULL,
    display_name STRING,
    description STRING,
    member_count INT64,
    category STRING,
    last_updated TIMESTAMP NOT NULL,
    extraction_date DATE NOT NULL
)
```

## Useful BigQuery Queries

### Total count:
```sql
SELECT COUNT(*) as total 
FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
```

### Category breakdown:
```sql
SELECT category, COUNT(*) as count 
FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog` 
GROUP BY category 
ORDER BY count DESC
```

### Search by keyword:
```sql
SELECT * 
FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
WHERE LOWER(email) LIKE '%ops%'
   OR LOWER(name) LIKE '%ops%'
   OR LOWER(description) LIKE '%ops%'
LIMIT 100
```

### Last update time:
```sql
SELECT MAX(last_updated) as last_update 
FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
```

## Daily Update Flow

1. **5:00 AM** - Scheduled task runs `extract_all_dls_optimized.py`
2. **5:05 AM** - New CSV created with latest DLs
3. **5:06 AM** - `upload_to_bigquery.py` loads data to BigQuery
4. **5:10 AM** - BigQuery table updated (replaces old data)
5. **All Day** - Code Puppy queries live data from BigQuery

## Cost Considerations

BigQuery pricing:
- **Storage**: ~$0.02/GB/month (your 15MB = $0.0003/month)
- **Queries**: $5/TB processed (each query of full table = ~$0.00007)
- **Estimated monthly cost**: < $1

Much cheaper than maintaining servers!

## Monitoring

Check table status:
```powershell
python -c "
from google.cloud import bigquery
client = bigquery.Client()
table = client.get_table('wmt-assetprotection-prod.Store_Support_Dev.dl_catalog')
print(f'Rows: {table.num_rows:,}')
print(f'Size: {table.num_bytes/(1024*1024):.2f} MB')
print(f'Modified: {table.modified}')
"
```

## Troubleshooting

**Error: "Permission denied"**
- Check service account has BigQuery permissions
- Verify credentials file path

**Error: "Dataset not found"**
- Run `upload_to_bigquery.py` to create dataset/table

**Error: "Table already exists"**
- Normal - script will replace data (WRITE_TRUNCATE mode)

**Slow queries**
- Add WHERE clauses to filter data
- Consider partitioning table by category or date

## Next Steps

1. ✅ Run initial upload: `python upload_to_bigquery.py`
2. ⏳ Update scheduled task to use BigQuery
3. ⏳ Configure Code Puppy to query BigQuery
4. ⏳ Test end-to-end flow
5. ⏳ Deploy to production

## Questions for Wibey

When you query Wibey about Code Puppy, ask:
- Does Code Puppy support BigQuery integration?
- Can I create a backend API endpoint in Code Puppy to query BigQuery?
- What's the service account email for Code Puppy applications?
- Are there examples of Code Puppy + BigQuery integrations?
