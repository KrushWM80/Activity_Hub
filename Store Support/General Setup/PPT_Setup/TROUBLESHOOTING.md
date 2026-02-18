# python-pptx Troubleshooting Guide

## Quick Reference

| Error | Cause | Quick Fix |
|-------|-------|-----------|
| getaddrinfo failed (11001) | Not on VPN or proxy not set | Connect to VPN, set proxy variables |
| 403 MediaTypeBlocked | Network blocks .whl files | Try Artifactory or manual install |
| ProxyError 10054 | Proxy connection issues | Verify VPN, try alternate proxy |
| SSL Certificate errors | Certificate validation failed | Use `--trusted-host` flags |
| Module not found | Package not installed | Run installation command again |

---

## Detailed Troubleshooting

### 1. Network Connection Issues

#### Symptom: DNS Resolution Failed
```
WARNING: Retrying (Retry(total=4...
Failed to establish a new connection: [Errno 11001] getaddrinfo failed
ERROR: Could not find a version that satisfies the requirement python-pptx
```

**Diagnostic Steps:**
1. Check VPN connection:
```powershell
Test-Connection proxy.wal-mart.com
```

2. Verify proxy environment variables:
```powershell
Get-ChildItem Env: | Where-Object { $_.Name -like '*PROXY*' }
```

3. Test internet connectivity:
```powershell
Test-NetConnection pypi.org -Port 443
```

**Solutions:**
- **Connect to Walmart VPN** if not already connected
- **Set proxy variables:**
```powershell
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"
```
- **Restart PowerShell** after setting variables
- **Try alternate proxy:** `http://proxyout.wal-mart.com:8080`

---

### 2. MediaTypeBlocked Error (403)

#### Symptom: Files Blocked by Network Security
```
ERROR: 403 Client Error: MediaTypeBlocked for url: https://files.pythonhosted.org/packages/.../python_pptx-1.0.2-py3-none-any.whl
```

**Root Cause:** Walmart's network security policy blocks certain file types (.whl files) from external sources for security reasons.

**Solution A: Use Walmart Artifactory**
```powershell
# Set proxy
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"

# Install from Artifactory
python -m pip install python-pptx \
    --index-url https://artifacts.walmart.com/artifactory/api/pypi/python-virtual/simple \
    --trusted-host artifacts.walmart.com
```

**Solution B: Manual Download and Transfer**

1. **On personal device/network**, download from PyPI:
   - Visit: https://pypi.org/project/python-pptx/#files
   - Download: `python_pptx-1.0.2-py3-none-any.whl`

2. **Download dependencies** (also from PyPI):
   - Pillow (e.g., `pillow-12.0.0-cp314-cp314-win_amd64.whl`)
   - XlsxWriter (e.g., `xlsxwriter-3.2.9-py3-none-any.whl`)
   - lxml (e.g., `lxml-6.0.2-cp314-cp314-win_amd64.whl`)
   - typing-extensions (e.g., `typing_extensions-4.15.0-py3-none-any.whl`)

3. **Transfer files** to Walmart machine (USB, email, file share)

4. **Install locally:**
```powershell
cd path\to\downloaded\files
python -m pip install typing_extensions-4.15.0-py3-none-any.whl
python -m pip install pillow-12.0.0-cp314-cp314-win_amd64.whl
python -m pip install xlsxwriter-3.2.9-py3-none-any.whl
python -m pip install lxml-6.0.2-cp314-cp314-win_amd64.whl
python -m pip install python_pptx-1.0.2-py3-none-any.whl
```

**Solution C: Request IT Access**
- Submit ServiceNow ticket
- Category: Network Access / Firewall Exception
- Request: Whitelist PyPI (pypi.org, files.pythonhosted.org) for Python development
- Justification: Required for automated reporting and presentation generation
- Business Impact: Development productivity, automation capabilities

---

### 3. Proxy Connection Errors

#### Symptom: Connection Reset by Proxy
```
ProxyError('Cannot connect to proxy.', ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host'))
```

**Diagnostic Steps:**
1. Test proxy connectivity:
```powershell
Test-NetConnection proxy.wal-mart.com -Port 8080
```

2. Check if proxy is responding:
```powershell
Invoke-WebRequest -Uri "http://proxy.wal-mart.com:8080" -UseBasicParsing
```

**Solutions:**
- **Restart VPN connection**
- **Try alternate proxy server:**
```powershell
$env:HTTP_PROXY = "http://proxyout.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxyout.wal-mart.com:8080"
```
- **Clear proxy settings and retry:**
```powershell
Remove-Item Env:HTTP_PROXY
Remove-Item Env:HTTPS_PROXY
# Reconnect VPN, then reset proxy
```
- **Contact IT:** If proxy is consistently unresponsive

---

### 4. SSL Certificate Verification Errors

#### Symptom: Certificate Validation Failed
```
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**Cause:** Corporate SSL inspection or outdated certificates

**Solution:**
```powershell
python -m pip install python-pptx \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org
```

**For persistent SSL issues:**
```powershell
# Disable SSL verification (USE WITH CAUTION)
python -m pip install python-pptx --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

---

### 5. Python Version Compatibility Issues

#### Symptom: No Matching Distribution
```
ERROR: Could not find a version that satisfies the requirement python-pptx
ERROR: No matching distribution found for python-pptx
```

**Check Python version:**
```powershell
python --version
```

**Requirements:** Python 3.8 or higher

**Solution:**
- Upgrade Python if version < 3.8
- Or download version-specific wheel file

---

### 6. Virtual Environment Issues

#### Symptom: Package Installed but Import Fails
```python
>>> import pptx
ModuleNotFoundError: No module named 'pptx'
```

**Cause:** Package installed in wrong environment

**Solution:**
1. Verify which Python is running:
```powershell
python -c "import sys; print(sys.executable)"
```

2. Verify which pip is installing:
```powershell
python -m pip --version
```

3. Ensure they match, then reinstall:
```powershell
python -m pip install python-pptx
```

4. If using virtual environment:
```powershell
# Activate first
.\.venv\Scripts\Activate.ps1

# Then install
pip install python-pptx
```

---

### 7. Permission Errors

#### Symptom: Access Denied
```
ERROR: Could not install packages due to an OSError: [WinError 5] Access is denied
```

**Solutions:**
- **Install with user flag:**
```powershell
python -m pip install --user python-pptx
```

- **Run as Administrator** (if necessary):
```powershell
# Right-click PowerShell, select "Run as Administrator"
python -m pip install python-pptx
```

---

### 8. Dependency Conflicts

#### Symptom: Dependency Resolution Failed
```
ERROR: Cannot install python-pptx because these package versions have conflicting dependencies.
```

**Solution:**
1. Check existing packages:
```powershell
python -m pip list
```

2. Try installing with `--no-deps` first:
```powershell
python -m pip install --no-deps python-pptx
```

3. Then install missing dependencies individually:
```powershell
python -m pip install Pillow XlsxWriter lxml typing-extensions
```

---

### 9. Import Errors After Installation

#### Symptom: Package Installed but Import Fails
```python
>>> import pptx
ImportError: DLL load failed while importing _imaging: The specified module could not be found.
```

**Cause:** Missing Visual C++ Redistributables (for Pillow dependency)

**Solution:**
1. Download and install [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. Restart Python
3. Try import again

---

### 10. File Permission Issues When Saving

#### Symptom: Permission Error When Saving .pptx
```python
PermissionError: [Errno 13] Permission denied: 'presentation.pptx'
```

**Causes:**
- File is open in PowerPoint
- No write permissions to directory
- File is locked by another process

**Solutions:**
- Close the file in PowerPoint
- Check file/folder permissions
- Save to a different location
- Use a different filename

---

## Verification Steps

After troubleshooting, verify installation:

```powershell
# Test 1: Check installation
python -m pip show python-pptx

# Test 2: Import package
python -c "import pptx; print('Success! Version:', pptx.__version__)"

# Test 3: Create test presentation
python -c "from pptx import Presentation; prs = Presentation(); prs.save('test.pptx'); print('Created test.pptx')"
```

**Expected outputs:**
- Test 1: Shows package information
- Test 2: Prints version number (e.g., "Success! Version: 1.0.2")
- Test 3: Creates test.pptx file

---

## Getting Help

### Internal Resources
1. **ServiceNow:** Submit IT support ticket
   - Category: Software Installation
   - Priority: Based on business need
   - Include: Error messages, steps taken, Python version

2. **Walmart Developer Community:**
   - Slack channels for Python developers
   - Internal wiki/documentation
   - Ask colleagues who have installed successfully

### External Resources
1. **python-pptx GitHub:** https://github.com/scanny/python-pptx/issues
2. **Stack Overflow:** Tag questions with `python-pptx`
3. **Official Docs:** https://python-pptx.readthedocs.io/

---

## Escalation Path

If unable to resolve:

1. **Level 1:** Retry with different proxy/network
2. **Level 2:** Try manual installation with downloaded wheels
3. **Level 3:** Submit ServiceNow ticket for network access
4. **Level 4:** Contact Python development team lead
5. **Level 5:** Request exception from IT security team

---

## Prevention Tips

- **Document your setup:** Save your working configuration
- **Use requirements.txt:** Track all dependencies
- **Keep Python updated:** Use recent stable versions
- **Test in dev environment:** Before production use
- **Maintain proxy settings:** Save as permanent environment variables
- **Keep offline packages:** Save wheel files for future use

---

## Common Walmart-Specific Issues

### Issue: Artifactory Authentication Required
```
401 Unauthorized: Authentication required for https://artifacts.walmart.com/
```

**Solution:**
```powershell
# Configure pip with Artifactory credentials
python -m pip config set global.index-url https://USERNAME:PASSWORD@artifacts.walmart.com/artifactory/api/pypi/python-virtual/simple
```

### Issue: Corporate Certificate Chain
```
SSLError: certificate verify failed: unable to get local issuer certificate
```

**Solution:**
Export Walmart CA certificates and configure pip:
```powershell
python -m pip config set global.cert "C:\path\to\walmart-ca-bundle.crt"
```

---

## Emergency Workaround

If all else fails and you need PowerPoint generation immediately:

### Alternative 1: Use Different Library
- **openpyxl:** Export to Excel, then convert to PowerPoint manually
- **reportlab:** Generate PDF, then import into PowerPoint

### Alternative 2: Generate XML
- PowerPoint uses Office Open XML format
- Can be manipulated with standard XML libraries
- More complex but doesn't require python-pptx

### Alternative 3: Use Online Services
- Some internal Walmart services may offer PowerPoint generation APIs
- Check with enterprise architecture team

---

## Contact Information

**For urgent issues:**
- IT Helpdesk: 1-800-XXX-XXXX
- Email: IT.Support@walmart.com
- ServiceNow: https://walmart.service-now.com/

**For package-specific questions:**
- GitHub Issues: https://github.com/scanny/python-pptx/issues
- Documentation: https://python-pptx.readthedocs.io/
