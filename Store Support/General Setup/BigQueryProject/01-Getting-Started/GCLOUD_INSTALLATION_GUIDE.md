# Google Cloud CLI Installation Guide for Windows

## Download and Install

1. **Download Google Cloud CLI:**
   - Go to: https://cloud.google.com/sdk/docs/install-sdk
   - Click "Windows" tab
   - Download the installer (GoogleCloudSDKInstaller.exe)

2. **Run the installer:**
   - Run GoogleCloudSDKInstaller.exe as administrator
   - Follow the installation prompts
   - Choose "Install for all users" if prompted

3. **Verify installation:**
   - Open a NEW PowerShell window
   - Run: `gcloud --version`
   - You should see version information

## Quick Installation Commands

If you prefer command-line installation:

```powershell
# Download using PowerShell (if you prefer)
Invoke-WebRequest -Uri "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe" -OutFile "GoogleCloudSDKInstaller.exe"

# Run installer
.\GoogleCloudSDKInstaller.exe
```

## Post-Installation Steps

1. **Open NEW PowerShell window** (important - to refresh PATH)
2. **Verify gcloud works:**
   ```powershell
   gcloud --version
   ```

3. **Initialize gcloud:**
   ```powershell
   gcloud init
   ```

4. **Authenticate:**
   ```powershell
   gcloud auth login
   ```

5. **Set project:**
   ```powershell
   gcloud config set project wmt-assetprotection-prod
   ```

6. **Test BigQuery access:**
   ```powershell
   bq ls
   ```

## If Installation Fails

### Alternative: Manual Installation
1. Download the zip file from the Google Cloud SDK page
2. Extract to `C:\google-cloud-sdk`
3. Add `C:\google-cloud-sdk\bin` to your PATH environment variable
4. Restart PowerShell and run `gcloud init`

### Troubleshooting
- **Path issues:** Restart PowerShell after installation
- **Permissions:** Run as administrator if needed
- **Corporate firewall:** May need IT assistance for download

## Ready to Continue?

Once gcloud is installed and `gcloud --version` works:
1. We'll authenticate you with your enterprise credentials
2. Set the project to wmt-assetprotection-prod
3. Fetch real BigQuery data directly
4. Your dashboard will show all 75+ real activities!

Let me know when gcloud is installed and working!