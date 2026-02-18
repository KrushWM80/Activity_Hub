# ELM Manager Change Detection - Deployment Guide

**Version:** 2.0  
**Last Updated:** January 13, 2026  
**For:** Windows deployment with Outlook COM automation

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Required Access](#required-access)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Production Deployment](#production-deployment)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

### **Software Requirements:**

1. **Windows 10/11** (or Windows Server 2016+)
2. **Python 3.8+**
   - Install from: https://www.python.org/downloads/
   - ✅ Add Python to PATH during installation
   
3. **Microsoft Outlook** (Desktop version)
   - Must be installed and configured
   - Office 365 or Outlook 2016+
   
4. **Git** (optional, for version control)
   - Install from: https://git-scm.com/

### **Python Packages:**

The following packages will be installed:
```
pandas
openpyxl
requests
playwright
pywin32
lxml
html5lib
```

---

## 🔑 Required Access

### **1. VPN Access**
- ✅ Walmart VPN (required for SDL access)
- Must be connected to access internal systems

### **2. SDL (Store Directory Lookup)**
- URL: https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/
- **Access Required:** Read access to SDL
- **Purpose:** Export manager data
- **Test:** Can you access SDL in a browser while on VPN?

### **3. LAS API (DC Alignment)**
- URL: http://dcalignment.telocmdm.prod.us.walmart.com/
- **Access Required:** Read access to DC alignment API
- **Purpose:** Get DC-to-store mappings
- **Test:** Can you access the API endpoint?

### **4. Shared Mailbox**
- **Required:** "Send As" permissions for shared mailbox
- **Example:** supplychainops@email.wal-mart.com
- **Purpose:** Send automated emails
- **How to get:** Request from mailbox owner or IT

**To add shared mailbox to Outlook:**
1. Open Outlook
2. File → Account Settings → Account Settings
3. Select your account → Change
4. More Settings → Advanced
5. Click "Add" under "Open these additional mailboxes"
6. Enter shared mailbox email
7. Click OK, OK, Next, Finish

### **5. Optional: BigQuery Access**

**Not currently required** - The system uses SDL exports, not BigQuery.

If you want to enhance with BigQuery:
- Project: `wmt-edw-prod`
- Dataset: `WW_CORE_DIM_DL_VM`
- Table: `DL_BU`
- **Access Required:** BigQuery Data Viewer role

---

## 📦 Installation

### **Step 1: Extract Files**

1. Extract `elm-manager-change-detection.zip` to a permanent location
2. Recommended: `C:\Users\<username>\elm\`
3. Do NOT use a network drive or temporary location

### **Step 2: Install Python Dependencies**

Open Command Prompt or PowerShell in the extracted folder:

```bash
cd C:\Users\<username>\elm

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium
```

### **Step 3: Run Setup Wizard**

```bash
python SETUP_WIZARD.py
```

The wizard will prompt you for:
- Your email address
- Shared mailbox email
- Test mode preference (recommended: YES)
- Location filters
- VPN retry configuration

---

## ⚙️ Configuration

### **Option 1: Use Setup Wizard (Recommended)**

Run `python SETUP_WIZARD.py` and follow the prompts.

### **Option 2: Manual Configuration**

Edit `config.py` directly:

```python
# Your email for test mode
TEST_EMAIL = "your.email@walmart.com"

# Shared mailbox
SHARED_MAILBOX_EMAIL = "your-shared-mailbox@email.wal-mart.com"
SHARED_MAILBOX_NAME = "Your Shared Mailbox Name"

# Test mode (keep TRUE until ready for production)
TEST_MODE = True

# VPN retry (recommended: 7 days)
VPN_MAX_RETRY_DAYS = 7
```

### **DC Email Configuration**

Edit `dc_email_config.py` to configure DC leadership emails.

**For test mode:** Leave as-is (all emails go to TEST_EMAIL)

**For production:** Update `get_dc_emails()` function with real DC GM/AGM emails

---

## 🧪 Testing

### **Test 1: VPN Connectivity**

```bash
python vpn_checker.py
```

**Expected:** `CONNECTED` (if on VPN) or `NOT CONNECTED`

### **Test 2: Create Initial Snapshot**

```bash
python create_snapshot.py
```

**Expected:**
- Downloads SDL export
- Applies filters
- Creates snapshot in `snapshots_local/`
- Shows ~4,900-5,000 managers

### **Test 3: Manual Daily Check**

```bash
python daily_check.py
```

**Expected:**
- Checks VPN
- Compares snapshots
- Reports changes (or no changes)
- Sends test email to your address

### **Test 4: Check Email**

Verify you received the test email:
- **From:** Your shared mailbox
- **To:** Your email
- **Subject:** Varies (changes detected or no changes)

---

## 🚀 Production Deployment

### **Step 1: Set Up Task Scheduler**

Run as **Administrator**:

```bash
setup_hourly_task_auto.bat
```

This creates a task that:
- Runs every hour starting at 2:00 AM
- Checks VPN connectivity
- Retries for up to 7 days
- Only processes each day once

### **Step 2: Verify Task**

1. Open Task Scheduler
2. Find "ManagerChangeDetection" task
3. Right-click → Run (test it manually)
4. Check for errors

### **Step 3: Monitor First Few Runs**

Check logs in the project folder:
```bash
type daily_run_log_YYYYMMDD.txt
```

Expect to see:
- VPN check results
- Snapshot creation
- Email sending confirmations

### **Step 4: Enable Production Mode** (When Ready)

Edit `config.py`:
```python
TEST_MODE = False  # Emails now go to DC distribution lists
```

**⚠️ WARNING:** Test thoroughly before disabling test mode!

---

## 🐛 Troubleshooting

### **Issue: "VPN not detected"**

**Solution:**
1. Connect to Walmart VPN
2. Test: `python vpn_checker.py`
3. Verify you can access SDL in browser

### **Issue: "Shared mailbox not found"**

**Solution:**
1. Add shared mailbox to Outlook (see [Required Access](#required-access))
2. Restart Outlook
3. Test: `python check_outlook_accounts.py`

### **Issue: "SDL scraping failed"**

**Solution:**
1. Check VPN connection
2. Try accessing SDL manually in browser
3. Check if Playwright is installed: `python -m playwright install chromium`

### **Issue: "Task Scheduler not running"**

**Solution:**
1. Open Task Scheduler
2. Check task status (should be "Ready" or "Running")
3. Check last run result (should be 0 for success)
4. View history for detailed errors

### **Issue: "No emails received"**

**Solution:**
1. Check `config.py` - is `EMAIL_ENABLED = True`?
2. Check `TEST_EMAIL` is your correct email
3. Check spam/junk folder
4. Check Outlook Sent Items for shared mailbox
5. Run manual test: `python test_no_changes_email.py`

---

## 📞 Support

**For issues or questions:**

1. Check logs: `daily_run_log_*.txt`
2. Review documentation in `/docs` folder
3. Contact: Original system deployer

---

## 📝 File Structure

```
elm/
├── config.py                 # Main configuration
├── dc_email_config.py        # DC leadership emails
├── daily_check.py            # Main automation script
├── daily_check_smart.py      # Smart wrapper with VPN retry
├── create_snapshot.py        # Snapshot creation
├── compare_snapshots.py      # Change detection
├── email_helper.py           # Email sending logic
├── vpn_checker.py            # VPN detection
├── scrape_sdl_playwright.py  # SDL scraping
├── dc_alignment_refresh.py   # DC alignment refresh
├── setup_hourly_task_auto.bat # Task Scheduler setup
├── SETUP_WIZARD.py           # Interactive setup
├── requirements.txt          # Python dependencies
├── snapshots_local/          # Local snapshots
├── data_input/               # SDL exports
├── emails_pending/           # Pending emails
└── logs/                     # Log files
```

---

## 🔒 Security Notes

- ✅ Runs under your Windows account
- ✅ Uses Outlook COM (no credentials stored)
- ✅ VPN required for all operations
- ✅ Shared mailbox requires "Send As" permission
- ✅ No data stored outside of local machine/OneDrive
- ✅ Test mode prevents accidental production emails

---

## 📊 What Gets Tracked

**Default Configuration:**
- ~5,200 locations
- Walmart Supercenters (3,568)
- Neighborhood Markets (684)
- Discount Stores (346)
- Sam's Clubs (610)

**Roles Tracked:**
- Store Manager / Club Manager
- Market Manager
- Regional General Manager
- DC General Manager
- DC Assistant General Manager

**Changes Detected:**
- Manager name changes
- New manager assignments
- TBD to named manager

---

## ✨ Features

✅ **Automated SDL Export** - No manual downloads  
✅ **VPN Retry Logic** - Retries for 7 days if off VPN  
✅ **DC-Segmented Emails** - Emails grouped by DC territory  
✅ **Shared Mailbox Support** - Sends from team mailbox  
✅ **Test Mode** - Safe testing before production  
✅ **Location Filters** - Focus on retail stores only  
✅ **Incomplete Alignment Alerts** - Flags stores missing DC assignments  
✅ **Smart Deduplication** - Never processes same day twice  

---

**Ready to deploy!** 🚀
