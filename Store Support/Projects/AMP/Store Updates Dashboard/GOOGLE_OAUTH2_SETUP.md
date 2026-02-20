# Google OAuth2 Setup Guide for AMP Dashboard

## Overview
This guide walks you through configuring Google OAuth2 authentication for the AMP Analysis Dashboard to access live BigQuery data.

---

## Step 1: Access Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Walmart Google account
3. Select the project: **wmt-assetprotection-prod**

---

## Step 2: Create OAuth2 Credentials

1. Navigate to: **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → select **OAuth client ID**
3. If prompted, configure the OAuth consent screen first:
   - **User Type**: Internal (Walmart)
   - **App name**: "AMP Analysis Dashboard"
   - **User support email**: Your email
   - **Scopes required**:
     - `https://www.googleapis.com/auth/bigquery`
     - `https://www.googleapis.com/auth/cloud-platform`
4. For Authorized redirect URIs, add:
   - `http://localhost:8080`
   - `http://localhost:3000`
   - `https://weus42608431466.homeoffice.wal-mart.com:8001` (production)

---

## Step 3: Get Your Client ID

1. After creating credentials, you'll see a dialog with your **Client ID**
2. Copy the **Client ID** value (looks like: `12345-abcde.apps.googleusercontent.com`)

---

## Step 4: Configure the Dashboard

1. Open: `gapi-auth-init.js`
2. Find the line:
   ```javascript
   const GOOGLE_CLIENT_ID = '<YOUR_GOOGLE_CLIENT_ID>';
   ```
3. Replace `<YOUR_GOOGLE_CLIENT_ID>` with your actual Client ID from Step 3
4. Save the file

---

## Step 5: Test the Setup

### Local Testing
1. Start the dashboard server:
   ```powershell
   cd "Store Updates Dashboard"
   python -m http.server 8080
   ```

2. Open browser: `http://localhost:8080`
3. You should see the **"Sign in with Google"** button
4. Click the button and complete the sign-in flow
5. After successful sign-in, the button should show your name
6. The dashboard should now load **live BigQuery data** for the past 90 days

### Verification
- Check browser console (F12) for success messages
- Verify data loads in dashboard tables (not sample data)
- Check console for: *"Successfully obtained BigQuery access token"*

---

## Common Issues & Troubleshooting

### Issue: "Google API not loaded"
- **Cause**: gapi.js script failed to load
- **Solution**: Check internet connection, try refreshing page

### Issue: "Authentication not configured"
- **Cause**: Client ID still has placeholder value
- **Solution**: Complete Step 3-4, reload page

### Issue: "User not signed in"
- **Cause**: Sign-in flow was not completed
- **Solution**: Click sign-in button, complete Google login

### Issue: "Access denied" or 403 error
- **Cause**: Your Google account doesn't have BigQuery access
- **Solution**: Contact GCP admin to grant `roles/bigquery.user` to your email

### Issue: Dashboard still shows sample data
- **Cause**: Authentication succeeded but live query is failing
- **Solution**: Check browser console for BigQuery error details
- **Possible causes**:
  - BigQuery service account not configured
  - Network/firewall blocking BigQuery API calls
  - Table/dataset permissions issue

---

## Production Deployment

For production deployment:

1. Add production URL to OAuth2 redirect URIs in GCP Console:
   ```
   https://weus42608431466.homeoffice.wal-mart.com:8001/
   ```

2. Update `gapi-auth-init.js` to accept environment-specific Client IDs:
   ```javascript
   const GOOGLE_CLIENT_ID = 
       window.location.hostname === 'localhost' 
           ? '<LOCAL_CLIENT_ID>' 
           : '<PROD_CLIENT_ID>';
   ```

3. Ensure dashboard is deployed over HTTPS (required for OAuth2)

---

## Security Notes

✅ **Best Practices:**
- Never commit real Client IDs to Git (only placeholder)
- Use environment variables for Client IDs in production
- Tokens are cached in-memory with 55-minute expiry
- Token is passed securely in Authorization header
- Dashboard never shows token in console (unless debugging)

⚠️ **Never:**
- Use service account JSON keys in frontend code
- Expose BigQuery API keys directly
- Store tokens in localStorage or cookies for production

---

## Next Steps After Configuration

Once OAuth2 is working:

1. ✅ Dashboard will show live AMP data from BigQuery
2. ✅ Data refreshes when filters are applied
3. ✅ Data is cached for 5 minutes per filter combination
4. ✅ Token automatically refreshes when expired

For any issues, check the browser console (F12) for detailed error messages.

---

**Need help?** Check the comments in `gapi-auth-init.js` and `amp-data-connector.js` for additional details.
