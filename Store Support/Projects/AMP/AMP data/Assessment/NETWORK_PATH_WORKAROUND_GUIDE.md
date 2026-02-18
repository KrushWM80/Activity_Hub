# AMP BigQuery Integration - Network/PATH Issue Workaround Guide

**Date**: October 28, 2025  
**Status**: Software Installed - Network/PATH Issues Detected

## 🚨 **CURRENT ISSUES IDENTIFIED**

### 1. Network Connectivity Issue
- **Problem**: Corporate firewall/proxy blocking pip package downloads
- **Error**: `getaddrinfo failed` - DNS/network resolution issue
- **Impact**: Cannot install Python packages from PyPI

### 2. PATH Configuration Issue  
- **Problem**: Git and Google Cloud SDK not in system PATH
- **Status**: Software installed but not accessible via command line
- **Impact**: Cannot use `git` or `gcloud` commands directly

## 🔧 **IMMEDIATE WORKAROUND SOLUTIONS**

### Solution 1: Use Full Paths for Git and Google Cloud SDK

Since the software is installed, you can use full paths:

```powershell
# Git commands (use full path)
& "$env:USERPROFILE\AppData\Local\Programs\Git\bin\git.exe" --version

# Google Cloud SDK commands (use full path)  
& "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" version
& "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\bq.cmd" version
```

### Solution 2: Create PowerShell Aliases

Add these to your PowerShell profile for easier access:

```powershell
# Create aliases for this session
Set-Alias git "$env:USERPROFILE\AppData\Local\Programs\Git\bin\git.exe"
Set-Alias gcloud "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
Set-Alias bq "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\bq.cmd"

# Test the aliases
git --version
gcloud version
bq version
```

### Solution 3: Network-Independent Package Installation

Since network is restricted, here are alternative approaches:

#### Option A: Use Corporate Package Repository
```powershell
# If your organization has an internal PyPI mirror
pip install google-cloud-bigquery --index-url=http://your-corporate-pypi-mirror
```

#### Option B: Download Wheels Manually (Advanced)
1. Download `.whl` files on a machine with internet access
2. Transfer to your work machine
3. Install offline: `pip install path/to/downloaded.whl`

#### Option C: Use Conda (if available)
```powershell
conda install -c conda-forge google-cloud-bigquery pandas numpy matplotlib
```

## 🚀 **PRODUCTION-READY DEPLOYMENT OPTIONS**

### Option 1: Cloud-Based Deployment (Recommended)

Since local network is restricted, deploy directly to Google Cloud:

```powershell
# Authenticate using full path
& "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" auth login

# Set project
& "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" config set project wmt-assetprotection-prod

# Deploy Cloud Function directly (dependencies will be installed in cloud)
& "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" functions deploy enhanced-amp-sync-trigger-http --source=. --entry-point=enhanced_amp_sync_trigger_http --runtime=python39 --trigger=http
```

### Option 2: Use Pre-built Deployment Scripts

I can modify the deployment scripts to handle the PATH issues:

```powershell
# Modified deployment script that uses full paths
$gcloud = "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
$bq = "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\bq.cmd"

# Deploy BigQuery SQL directly
& $bq query --use_legacy_sql=false < amp_bigquery_enhanced_multisource_system_20251028_080418.sql
```

## 📋 **UPDATED ACTION PLAN**

### Immediate Actions (Network Independent):

1. **Test Cloud Tools with Full Paths**:
   ```powershell
   & "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" auth login
   & "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" config set project wmt-assetprotection-prod
   ```

2. **Deploy BigQuery Components**:
   ```powershell
   # Deploy the SQL trigger system directly
   & "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\bq.cmd" query --use_legacy_sql=false < amp_bigquery_enhanced_multisource_system_20251028_080418.sql
   ```

3. **Setup Authentication**:
   ```powershell
   # Enable required APIs
   & "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" services enable bigquery.googleapis.com cloudfunctions.googleapis.com cloudscheduler.googleapis.com
   ```

### Long-term Solutions:

1. **Contact IT for Network Access**: Request PyPI access or internal mirror
2. **PATH Fix**: Restart computer or manually add to system PATH
3. **Alternative Python Environment**: Use Anaconda/Miniconda if available

## 🎯 **WHAT WE CAN DO RIGHT NOW**

Despite the network and PATH issues, we can still:

✅ **Deploy the BigQuery trigger system** using full paths to gcloud/bq  
✅ **Set up authentication** for Google Cloud access  
✅ **Create the BigQuery tables and procedures** using the generated SQL  
✅ **Test the system** using BigQuery console or command line tools  

## 📞 **NEXT STEPS RECOMMENDATION**

Would you like me to:

1. **Create modified deployment scripts** that use full paths to bypass PATH issues?
2. **Guide you through BigQuery deployment** using the cloud console?
3. **Set up authentication** using the installed Google Cloud SDK?
4. **Create a network-independent deployment approach**?

Choose the option that works best for your corporate environment!