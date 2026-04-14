# AMP AutoFeed Validation - Install Guide (Off VPN)

## Quick Install (Copy & Paste)

Once you're OFF the corporate VPN, open a PowerShell terminal and run these commands:

```powershell
# Install Python packages
py -m pip install beautifulsoup4 pywin32 -q

# Verify installation
py -c "import bs4; import win32com; print('All packages installed successfully!')"
```

That's it! Should take 30-60 seconds.

---

## Then Create Scheduled Tasks (As Admin)

After packages are installed, open PowerShell as Administrator and run:

```powershell
# Daily validation at 7:00 AM
schtasks /create /tn "AMP-AutoFeed-DailyValidation" /tr "py 'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_orchestrator.py' daily --log-dir 'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_validation_logs'" /sc daily /st 07:00 /ru SYSTEM /f

# Weekly CSV reports on Monday at 6:00 AM
schtasks /create /tn "AMP-AutoFeed-WeeklyReport" /tr "py 'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_orchestrator.py' csv-report --days 90 --log-dir 'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_validation_logs'" /sc weekly /d MON /st 06:00 /ru SYSTEM /f
```

---

## Verify Installation

After both steps above, verify it worked:

```powershell
# Check packages
py -c "import bs4; import win32com; print('Packages OK')"

# Check scheduled tasks
schtasks /query /tn "AMP-AutoFeed-*" /v
```

Should show both tasks with status "Ready".

---

## Test the System

Finally, test that everything works:

```powershell
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
py .\amp_autofeed_orchestrator.py daily
```

Expected output:
```
Validation Status: PASS
Data match verified
```

---

## If Something Goes Wrong

**Error: "Module not found"**
- Make sure you're OFF VPN
- Try again: `py -m pip install beautifulsoup4 pywin32`

**Error: "Access denied" on scheduled tasks**
- Must run PowerShell as Administrator
- Right-click PowerShell, select "Run as administrator"

**Error: "Python not found"**
- Make sure `py` works: `py --version`
- If not, you may need to install Python from python.org

---

## Summary

1. **Off VPN**: `py -m pip install beautifulsoup4 pywin32 -q`
2. **Admin PowerShell**: Run the two `schtasks` commands above
3. **Verify**: `schtasks /query /tn "AMP-AutoFeed-*"`
4. **Test**: `py .\amp_autofeed_orchestrator.py daily`

That's it! System will then run automatically daily at 7:00 AM.
