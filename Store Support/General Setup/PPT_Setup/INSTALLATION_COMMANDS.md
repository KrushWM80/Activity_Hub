# python-pptx Installation Commands

## Quick Installation (If Network is Working)

```powershell
# With Walmart proxy
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"
python -m pip install python-pptx
```

---

## Complete Installation Steps

### Step 1: Set Proxy Environment Variables
```powershell
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"
```

### Step 2: Install Package
```powershell
python -m pip install python-pptx
```

### Step 3: Verify Installation
```powershell
python -c "import pptx; print(pptx.__version__)"
```

---

## Alternative Installation Methods

### Method 1: Using Walmart Artifactory
```powershell
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"
python -m pip install python-pptx --index-url https://artifacts.walmart.com/artifactory/api/pypi/python-virtual/simple --trusted-host artifacts.walmart.com
```

### Method 2: With Trusted Hosts (SSL Issues)
```powershell
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"
python -m pip install python-pptx --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

### Method 3: From Local Wheel Files
```powershell
# Install dependencies first
python -m pip install typing_extensions-4.15.0-py3-none-any.whl
python -m pip install pillow-12.0.0-cp314-cp314-win_amd64.whl
python -m pip install xlsxwriter-3.2.9-py3-none-any.whl
python -m pip install lxml-6.0.2-cp314-cp314-win_amd64.whl

# Then install python-pptx
python -m pip install python_pptx-1.0.2-py3-none-any.whl
```

### Method 4: User Installation (No Admin Rights)
```powershell
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"
python -m pip install --user python-pptx
```

### Method 5: Virtual Environment Installation
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Set proxy
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"

# Install package
pip install python-pptx
```

---

## Verification Commands

### Check if Package is Installed
```powershell
python -m pip show python-pptx
```

### Check Package Version
```powershell
python -c "import pptx; print(pptx.__version__)"
```

### List All Installed Packages
```powershell
python -m pip list
```

### Test Basic Functionality
```powershell
python -c "from pptx import Presentation; prs = Presentation(); prs.save('test.pptx'); print('Success!')"
```

---

## Update/Upgrade Commands

### Upgrade python-pptx
```powershell
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"
python -m pip install --upgrade python-pptx
```

### Upgrade pip
```powershell
python -m pip install --upgrade pip
```

### Reinstall Package
```powershell
python -m pip uninstall python-pptx
python -m pip install python-pptx
```

---

## Uninstallation Commands

### Uninstall python-pptx Only
```powershell
python -m pip uninstall python-pptx
```

### Uninstall with Dependencies
```powershell
python -m pip uninstall python-pptx Pillow XlsxWriter lxml typing-extensions
```

---

## Troubleshooting Commands

### Check Python Version
```powershell
python --version
```

### Check Python Executable Path
```powershell
python -c "import sys; print(sys.executable)"
```

### Check pip Version
```powershell
python -m pip --version
```

### Test Network Connection
```powershell
Test-Connection proxy.wal-mart.com
Test-NetConnection pypi.org -Port 443
```

### Check Proxy Settings
```powershell
Get-ChildItem Env: | Where-Object { $_.Name -like '*PROXY*' }
```

### Clear Proxy Settings
```powershell
Remove-Item Env:HTTP_PROXY
Remove-Item Env:HTTPS_PROXY
```

### Check Available Python Environments
```powershell
py --list
```

---

## Dependencies Installation Commands

If you need to install dependencies separately:

### Install All Dependencies
```powershell
python -m pip install Pillow XlsxWriter lxml typing-extensions
```

### Install Individual Dependencies
```powershell
python -m pip install Pillow>=3.3.2
python -m pip install XlsxWriter>=0.5.7
python -m pip install lxml>=3.1.0
python -m pip install typing-extensions>=4.9.0
```

---

## Permanent Proxy Configuration

### Set System-Wide Environment Variables (Requires Admin)
```powershell
[System.Environment]::SetEnvironmentVariable("HTTP_PROXY", "http://proxy.wal-mart.com:8080", "Machine")
[System.Environment]::SetEnvironmentVariable("HTTPS_PROXY", "http://proxy.wal-mart.com:8080", "Machine")
```

### Set User-Level Environment Variables
```powershell
[System.Environment]::SetEnvironmentVariable("HTTP_PROXY", "http://proxy.wal-mart.com:8080", "User")
[System.Environment]::SetEnvironmentVariable("HTTPS_PROXY", "http://proxy.wal-mart.com:8080", "User")
```

### Configure pip to Always Use Proxy
```powershell
python -m pip config set global.proxy http://proxy.wal-mart.com:8080
```

### View pip Configuration
```powershell
python -m pip config list
```

---

## Batch Installation Script

Save this as `install_pptx.ps1`:

```powershell
# install_pptx.ps1
# Installation script for python-pptx at Walmart

Write-Host "Setting up Walmart proxy..." -ForegroundColor Green
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"

Write-Host "Installing python-pptx..." -ForegroundColor Green
python -m pip install python-pptx

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nInstallation successful!" -ForegroundColor Green
    Write-Host "Verifying installation..." -ForegroundColor Green
    python -c "import pptx; print('python-pptx version:', pptx.__version__)"
} else {
    Write-Host "`nInstallation failed. Try alternative methods:" -ForegroundColor Red
    Write-Host "1. Check VPN connection" -ForegroundColor Yellow
    Write-Host "2. Try Artifactory: python -m pip install python-pptx --index-url https://artifacts.walmart.com/artifactory/api/pypi/python-virtual/simple --trusted-host artifacts.walmart.com" -ForegroundColor Yellow
    Write-Host "3. See TROUBLESHOOTING.md for more options" -ForegroundColor Yellow
}
```

Run with:
```powershell
.\install_pptx.ps1
```

---

## Download Links (For Manual Installation)

### PyPI Package Pages
- **python-pptx:** https://pypi.org/project/python-pptx/#files
- **Pillow:** https://pypi.org/project/Pillow/#files
- **XlsxWriter:** https://pypi.org/project/XlsxWriter/#files
- **lxml:** https://pypi.org/project/lxml/#files
- **typing-extensions:** https://pypi.org/project/typing-extensions/#files

### Current Versions (as of Dec 2025)
- python-pptx: 1.0.2
- Pillow: 12.0.0
- XlsxWriter: 3.2.9
- lxml: 6.0.2
- typing-extensions: 4.15.0

---

## Requirements.txt Format

Create a `requirements.txt` file for reproducible installations:

```text
python-pptx==1.0.2
Pillow>=3.3.2
XlsxWriter>=0.5.7
lxml>=3.1.0
typing-extensions>=4.9.0
```

Install from requirements.txt:
```powershell
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"
python -m pip install -r requirements.txt
```

---

## Virtual Environment Best Practices

### Create and Setup Virtual Environment
```powershell
# Create virtual environment
python -m venv pptx_env

# Activate it
.\pptx_env\Scripts\Activate.ps1

# Verify you're in the environment (prompt should show (pptx_env))
python -c "import sys; print(sys.prefix)"

# Install python-pptx
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"
pip install python-pptx

# Deactivate when done
deactivate
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│         python-pptx Quick Install Reference            │
├─────────────────────────────────────────────────────────┤
│ 1. Set Proxy:                                          │
│    $env:HTTP_PROXY = "http://proxy.wal-mart.com:8080" │
│    $env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"│
│                                                         │
│ 2. Install:                                            │
│    python -m pip install python-pptx                   │
│                                                         │
│ 3. Verify:                                             │
│    python -c "import pptx; print(pptx.__version__)"   │
│                                                         │
│ Troubleshooting:                                       │
│    - Check VPN connection                              │
│    - Try Artifactory (see TROUBLESHOOTING.md)         │
│    - Manual install from wheel files                   │
│    - ServiceNow ticket for network access              │
└─────────────────────────────────────────────────────────┘
```
