# BigQuery REST API Connection Setup

## Quick Setup Guide

### Step 1: Start the BigQuery Service
```bash
python bigquery_rest_service.py
```

### Step 2: Configure Google OAuth (One-time setup)

1. **Go to Google Cloud Console:**
   - https://console.cloud.google.com/apis/credentials
   - Select project: `wmt-assetprotection-prod`

2. **Create OAuth 2.0 Client:**
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Application type: "Web application"
   - Name: "AMP Dashboard BigQuery Connection"
   
3. **Add Redirect URI:**
   - Authorized redirect URIs: `http://localhost:8081/api/bigquery/callback`

4. **Get Credentials:**
   - Copy the Client ID and Client Secret
   - Update `bigquery_rest_service.py`:
     ```python
     client_id = 'YOUR_ACTUAL_CLIENT_ID_HERE'
     client_secret = 'YOUR_ACTUAL_CLIENT_SECRET_HERE'
     ```

### Step 3: Authenticate and Connect

1. **Start the service** (if not already running)
2. **Visit:** http://localhost:8081/api/bigquery/auth-url
3. **Follow the OAuth flow** to authenticate
4. **Refresh your dashboard** - it will now show live BigQuery data!

## Service Endpoints

- **Status:** http://localhost:8081/api/status
- **Authentication:** http://localhost:8081/api/bigquery/auth-url  
- **Data:** http://localhost:8081/api/bigquery/data

## What You Get

✅ **Direct connection** to `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep`
✅ **Real-time data** - No manual exports
✅ **OAuth security** - Industry standard authentication
✅ **All Week 39 published activities** with working GUID preview links
✅ **Automatic dashboard integration**

## Troubleshooting

### Service Won't Start
- Check if port 8081 is available
- Ensure Python is working: `python --version`

### Authentication Fails
- Verify OAuth credentials are correct
- Check redirect URI matches exactly: `http://localhost:8081/api/bigquery/callback`
- Ensure BigQuery API is enabled in Google Cloud Console

### No Data Returned  
- Verify permissions to `wmt-assetprotection-prod` project
- Check BigQuery API access
- Confirm table exists: `Store_Support_Dev.AMP_Data_Prep`

### Dashboard Not Connecting
- Ensure BigQuery service is running on port 8081
- Check browser console for connection errors
- Verify dashboard is looking at localhost:8081

## Next Steps

Once setup is complete:
1. Your dashboard will automatically connect to live BigQuery data
2. All preview links will be real GUID links that work
3. Data refreshes automatically when you reload the dashboard
4. No more manual exports needed!