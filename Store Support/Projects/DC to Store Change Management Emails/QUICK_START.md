# Quick Start Guide

**ELM Manager Change Detection System - 5 Minute Setup**

---

## Step 1: Extract Files (1 min)

1. Extract `elm-manager-change-detection-v2.0-YYYYMMDD.zip`
2. Choose a permanent location (e.g., `C:\Users\<you>\elm`)
3. **DO NOT** use a network drive or temporary folder

---

## Step 2: Install Python (2 min)

If you don't have Python 3.8+:

1. Download from: https://www.python.org/downloads/
2. Run installer
3. ✅ **Check "Add Python to PATH"**
4. Click "Install Now"

---

## Step 3: Install Dependencies (1 min)

Open Command Prompt in the extracted folder:

```bash
cd C:\Users\<you>\elm
pip install -r requirements.txt
python -m playwright install chromium
```

---

## Step 4: Run Setup Wizard (1 min)

```bash
python SETUP_WIZARD.py
```

**You'll be asked for:**
- Your email address
- Shared mailbox email (e.g., yourteam@email.wal-mart.com)
- Test mode preference (say YES)

The wizard creates `config.py` for you.

---

## Step 5: Add Shared Mailbox to Outlook (2 min)

1. Open Outlook
2. File → Account Settings → Account Settings
3. Select account → Change → More Settings → Advanced
4. Click "Add" under "Open these additional mailboxes"
5. Enter your shared mailbox email
6. Click OK, OK, Next, Finish
7. Restart Outlook

---

## Step 6: Test It (2 min)

### Test VPN:
```bash
python vpn_checker.py
```
**Should say:** `CONNECTED`

### Create first snapshot:
```bash
python create_snapshot.py
```
**Should create:** `snapshots_local/manager_snapshot_YYYY-MM-DD.json`

### Send test email:
```bash
python test_no_changes_email.py
```
**Check your inbox** - you should get an email from your shared mailbox!

---

## Step 7: Set Up Automation (1 min)

Run **as Administrator**:

```bash
setup_hourly_task_auto.bat
```

This creates a Task Scheduler task that runs hourly.

---

## ✅ You're Done!

The system will now:
- Check every hour for VPN
- Run daily check when VPN available
- Send emails from your shared mailbox
- Retry for 7 days if off VPN

---

## 📝 Logs

Check `daily_run_log_YYYYMMDD.txt` to see what happened.

---

## 🔧 Configuration

Edit `config.py` to customize:
- Test mode (keep `True` until ready)
- VPN retry days
- Location filters

---

## 🚀 Production Mode

When ready to go live:

1. Edit `config.py`
2. Change `TEST_MODE = False`
3. Update `dc_email_config.py` with real DC emails
4. Test one more time
5. Let it run!

---

## ❓ Need Help?

See **DEPLOYMENT_GUIDE.md** for detailed troubleshooting.

---

**That's it!** You're ready to track manager changes automatically. 🎉
