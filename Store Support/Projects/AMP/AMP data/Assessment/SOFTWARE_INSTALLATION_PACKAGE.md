# AMP BigQuery Trigger System - Complete Software Package

## 🎯 Current Status Assessment

Based on your system analysis:

### ✅ Already Installed:
- **Python 3.8+**: Available in your virtual environment
- **VS Code**: Currently in use  
- **curl**: Available for HTTP testing
- **PowerShell**: Available for script execution

### ❌ Missing Essential Software:
- **Google Cloud CLI (gcloud)**: Required for BigQuery and Cloud Functions
- **Git for Windows**: Required for Git Bash terminal and version control

### ❌ Missing Python Packages:
- google-cloud-bigquery
- google-cloud-functions-framework  
- google-auth
- pandas
- requests

## 📥 Direct Download Links

### 1. Google Cloud CLI (ESSENTIAL)
**Direct Download**: https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe

**Installation Steps**:
1. Download the installer from the link above
2. Run as Administrator
3. Follow the installation wizard
4. When complete, open a new PowerShell window
5. Run: `gcloud init` to configure

**Alternative - Manual Installation**:
```powershell
# Download and install via PowerShell
$url = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
$output = "$env:TEMP\GoogleCloudSDKInstaller.exe"
Invoke-WebRequest -Uri $url -OutFile $output
Start-Process -FilePath $output -Wait
```

### 2. Git for Windows (ESSENTIAL - includes Git Bash)
**Direct Download**: https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe

**Installation Steps**:
1. Download the installer from the link above
2. Run the installer
3. **IMPORTANT**: During installation, select "Git Bash Here" option
4. Keep all other default settings
5. After installation, you'll have Git Bash available

**Alternative - Latest Version**:
- Go to: https://git-scm.com/download/windows
- Download the 64-bit version

## 🐍 Python Package Installation

After installing the essential software above, install required Python packages:

```bash
# In your current virtual environment
C:/Users/krush/Documents/VSCode/Spark-Playground/.venv-1/Scripts/python.exe -m pip install google-cloud-bigquery google-cloud-functions-framework google-auth pandas requests
```

## 🚀 Quick Installation Script

**Option 1: Manual Installation (Recommended)**
1. Download Google Cloud CLI from the direct link above
2. Download Git for Windows from the direct link above  
3. Install both programs
4. Run the Python package installation command

**Option 2: Automated PowerShell Script**
Run this in PowerShell as Administrator:

```powershell
# Quick install script - save as install_software.ps1
Write-Host "Installing AMP BigQuery dependencies..." -ForegroundColor Green

# Install Chocolatey (package manager)
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    refreshenv
}

# Install Git
choco install git -y

# Install Google Cloud CLI  
choco install gcloudsdk -y

Write-Host "Installation complete! Please restart your terminal." -ForegroundColor Green
```

## 🔧 Post-Installation Configuration

### 1. Configure Google Cloud CLI
```bash
# Authenticate with Google Cloud
gcloud auth login

# Set your project (you'll need to verify this project ID)
gcloud config set project wmt-assetprotection-prod

# Verify authentication
gcloud auth list
```

### 2. Install Python Packages
```bash
# Navigate to your project directory
cd C:/Users/krush/Documents/VSCode/Spark-Playground

# Activate your virtual environment (if not already active)
.venv-1/Scripts/activate

# Install required packages
pip install google-cloud-bigquery google-cloud-functions-framework google-auth pandas requests
```

### 3. Verify Installation
```bash
# Test gcloud
gcloud version

# Test git
git --version

# Test BigQuery CLI (comes with gcloud)
bq version

# Test Python packages
python -c "import google.cloud.bigquery; print('BigQuery client installed successfully')"
```

## 📋 Installation Checklist

- [ ] Download and install Google Cloud CLI
- [ ] Download and install Git for Windows  
- [ ] Install Python packages in virtual environment
- [ ] Configure Google Cloud authentication
- [ ] Verify all installations work
- [ ] Run BigQuery trigger system setup

## 🎯 Ready for Deployment

Once you complete the installation checklist above, you'll be ready to:

1. **Deploy BigQuery Tables**: Run the generated SQL scripts
2. **Deploy Cloud Functions**: Use the deployment script
3. **Set up Monitoring**: Configure the trigger system
4. **Test the Pipeline**: Verify end-to-end functionality

## 🆘 Troubleshooting

### Common Issues and Solutions:

**"gcloud not found after installation"**
- Restart your terminal/PowerShell
- Add to PATH: `C:\Users\[username]\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin`

**"Permission denied" errors**
- Run PowerShell as Administrator
- Check Windows Defender/Antivirus settings

**Python package installation fails** 
- Ensure virtual environment is activated
- Update pip: `python -m pip install --upgrade pip`
- Try installing packages one at a time

**Git Bash not available**
- During Git installation, ensure "Git Bash Here" is selected
- Restart Windows Explorer after installation

## 📞 Support Resources

- **Google Cloud Documentation**: https://cloud.google.com/docs
- **Git for Windows**: https://gitforwindows.org/
- **BigQuery Documentation**: https://cloud.google.com/bigquery/docs
- **Cloud Functions Documentation**: https://cloud.google.com/functions/docs

---

**Next Steps**: Once software is installed, proceed with running the BigQuery trigger system deployment!