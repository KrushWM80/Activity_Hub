# BigQuery Real Data Connection Setup

This dashboard can connect to real data from `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep`. Follow these steps to enable real data access:

## Option 1: OAuth2 Authentication (Recommended for Development)

### Step 1: Google Cloud Console Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select project: `wmt-assetprotection-prod`
3. Enable the BigQuery API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set Application Type to "Web application"
6. Add your domain to "Authorized JavaScript origins":
   - `http://localhost` (for local development)
   - Your production domain
7. Copy the Client ID

### Step 2: Configure Authentication
1. Open `index.html`
2. Find the line: `const clientId = 'YOUR_OAUTH2_CLIENT_ID';`
3. Replace `'YOUR_OAUTH2_CLIENT_ID'` with your actual Client ID
4. If you have an API key, replace `'YOUR_API_KEY'` as well

### Step 3: Test Connection
1. Open the dashboard
2. Click "Connect to BigQuery" button
3. Complete the OAuth flow
4. Data should now load from the real BigQuery table

## Option 2: Service Account Authentication (For Production)

### Step 1: Service Account Setup
1. Go to Google Cloud Console
2. Go to "IAM & Admin" → "Service Accounts"
3. Create a new service account
4. Grant "BigQuery Data Viewer" role
5. Generate and download JSON key file

### Step 2: Backend Service
Create a backend endpoint that:
1. Uses the service account key to authenticate
2. Executes BigQuery queries
3. Returns data to the frontend

Example backend endpoint (`/api/bigquery-token`):
```javascript
app.post('/api/bigquery-token', async (req, res) => {
  const { BigQuery } = require('@google-cloud/bigquery');
  const bigquery = new BigQuery({
    keyFilename: 'path/to/service-account-key.json',
    projectId: 'wmt-assetprotection-prod'
  });
  
  // Generate access token and return
  const token = await bigquery.authClient.getAccessToken();
  res.json({ access_token: token.token, expires_in: 3600 });
});
```

## Data Source Schema

The dashboard expects the following columns from `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep`:

### Required Columns:
- `week_number` (INTEGER) - Week number for grouping
- `actv_title_home_ofc_nm` (STRING) - Activity title
- `location` (STRING) - Location identifier  
- `total_count` (INTEGER) - Total count of items
- `sc_count` (INTEGER) - Supercenter count
- `nhm_count` (INTEGER) - Neighborhood Market count
- `div1_count` (INTEGER) - Division 1 count
- `fuel_count` (INTEGER) - Fuel center count
- `status` (STRING) - Status (complete/incomplete/inform)
- `division` (STRING) - Division name
- `region` (STRING) - Region identifier
- `market` (STRING) - Market identifier
- `site` (STRING) - Site identifier
- `activity_type` (STRING) - Type (Verification/Inform)
- `store_area` (STRING) - Store area/department
- `published` (BOOLEAN) - Published status
- `alignment` (STRING) - Alignment type
- `create_ts` (TIMESTAMP) - Creation timestamp
- `msg_start_dt` (TIMESTAMP) - Message start date
- `msg_end_dt` (TIMESTAMP) - Message end date

### Optional Columns for Verification Activities:
- `complete_count` (INTEGER) - Count of completed verifications
- `incomplete_count` (INTEGER) - Count of incomplete verifications

## Troubleshooting

### Common Issues:

1. **"Authentication not configured" error**
   - Make sure you've replaced the placeholder Client ID with your actual ID

2. **"Access denied" error**
   - Ensure your Google account has access to the BigQuery dataset
   - Check if BigQuery API is enabled for the project

3. **CORS errors**
   - Make sure your domain is added to authorized origins in Google Cloud Console
   - For local development, use `http://localhost` (not `file://`)

4. **"No data returned" message**
   - Check if the BigQuery table exists and has data
   - Verify the table schema matches the expected columns
   - Check the SQL query in `amp-data-connector.js`

### Fallback Behavior:
If real data connection fails, the dashboard will automatically fall back to using sample data, so the interface remains functional for testing and development.

## Current Status:
- ✅ BigQuery connection code implemented
- ✅ Authentication framework ready
- ✅ Fallback to sample data working
- ⚠️ Requires OAuth2/Service Account configuration
- ⚠️ Requires access permissions to BigQuery dataset

To complete the setup, configure authentication using one of the methods above.