# BigQuery Connection Setup for Projects in Stores Dashboard

## Quick Setup (Using gcloud CLI)

The easiest way to connect to BigQuery is using Google Cloud CLI authentication.

### Step 1: Install Google Cloud SDK

If not already installed, run:
```powershell
# Download and install from: https://cloud.google.com/sdk/docs/install
# Or use the automated script from BigQuery Project folder
C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\BigQueryProject\02-Authentication\install_gcloud.ps1
```

### Step 2: Authenticate with gcloud

```powershell
# Login to Google Cloud
gcloud auth login

# Set the project
gcloud config set project wmt-assetprotection-prod

# Create application default credentials
gcloud auth application-default login
```

### Step 3: Update .env File

Create `backend/.env` file with:
```env
# BigQuery Connection
GCP_PROJECT_ID=wmt-assetprotection-prod
GOOGLE_APPLICATION_CREDENTIALS=  # Leave empty to use gcloud credentials

# Database Details
BIGQUERY_DATASET=Store_Support_Dev
BIGQUERY_TABLE=IH_Intake_Data

# OpenAI (Optional - for AI assistant)
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4
```

### Step 4: Test Connection

```powershell
cd backend
python -c "from google.cloud import bigquery; client = bigquery.Client(project='wmt-assetprotection-prod'); print('✅ Connection successful!')"
```

## Alternative Setup (Using Service Account)

### Step 1: Get Service Account Key

1. Contact your GCP admin or Allen (peer)
2. Request access to `wmt-assetprotection-prod`
3. Download service account JSON key file

### Step 2: Configure .env

```env
GCP_PROJECT_ID=wmt-assetprotection-prod
GOOGLE_APPLICATION_CREDENTIALS=C:/path/to/service-account-key.json
BIGQUERY_DATASET=Store_Support_Dev
BIGQUERY_TABLE=IH_Intake_Data
```

## Database Schema

### Table: `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`

Expected columns:
- `project_id` (STRING)
- `project_source` (STRING) - "Intake Hub" or "Realty"
- `title` (STRING)
- `division` (STRING)
- `region` (STRING)
- `market` (STRING)
- `store` (STRING)
- `store_area` (STRING)
- `business_area` (STRING)
- `phase` (STRING)
- `tribe` (STRING)
- `wm_week` (STRING)
- `status` (STRING) - "Active", "Archived", or "Pending"
- `store_count` (INTEGER)
- `created_date` (TIMESTAMP)
- `last_updated` (TIMESTAMP)
- `description` (STRING)

## Verification

### Test with bq Command

```powershell
bq query --use_legacy_sql=false "
SELECT COUNT(*) as total_projects
FROM \`wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data\`
WHERE status = 'Active'
"
```

### Test with Python

```python
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')
query = """
SELECT COUNT(*) as count 
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE status = 'Active'
"""
result = list(client.query(query).result())[0]
print(f"Active projects: {result.count}")
```

## Troubleshooting

### Error: "Could not automatically determine credentials"

**Solution:** Run `gcloud auth application-default login`

### Error: "Permission denied"

**Solution:** 
1. Verify you're authenticated: `gcloud auth list`
2. Check project access: Contact GCP admin
3. Request BigQuery Data Viewer role

### Error: "Table not found"

**Solution:**
1. Verify table name: `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
2. Check dataset permissions
3. Confirm table exists in BigQuery console

## Cost Management

- BigQuery queries are billed based on data scanned
- First 1 TB per month is free
- Dashboard queries typically scan < 100 MB per request
- Estimated cost: < $5/month for typical usage

## Best Practices

1. **Use gcloud CLI** - Simplest authentication method
2. **Cache filter options** - Reduces query frequency
3. **Limit query results** - Use LIMIT clause
4. **Test with mock data first** - Verify dashboard works before connecting

## Reference Files

Your existing BigQuery setup files:
- Connection script: `C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\BigQueryProject\03-Data-Access\connect_bigquery.py`
- Authentication setup: `C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\BigQueryProject\02-Authentication\setup_gcloud_auth.ps1`
- Complete docs: `C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\BigQueryProject\README.md`

## Quick Start Commands

```powershell
# 1. Authenticate
gcloud auth application-default login

# 2. Set project
gcloud config set project wmt-assetprotection-prod

# 3. Create .env file (backend/.env)
@"
GCP_PROJECT_ID=wmt-assetprotection-prod
BIGQUERY_DATASET=Store_Support_Dev
BIGQUERY_TABLE=IH_Intake_Data
"@ | Out-File -FilePath .env -Encoding UTF8

# 4. Start dashboard
python main.py
```

Your dashboard will automatically detect gcloud credentials and connect to BigQuery!
