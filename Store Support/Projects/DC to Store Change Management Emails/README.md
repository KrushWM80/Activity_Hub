# ELM Manager Change Detection System

**Automated manager change tracking and notification system for Walmart retail locations.**

---

## 🎯 Quick Start

1. **Extract** this ZIP file to a permanent location
2. **Run** `python SETUP_WIZARD.py`
3. **Follow** the prompts to configure
4. **Test** with `python create_snapshot.py`
5. **Deploy** with `setup_hourly_task_auto.bat` (as admin)

**Full instructions:** See `DEPLOYMENT_GUIDE.md`

---

## 📚 Documentation

- **DEPLOYMENT_GUIDE.md** - Complete setup and deployment instructions
- **7_DAY_VPN_RETRY_SUMMARY.md** - VPN retry logic explained
- **VPN_RETRY_LOGIC.md** - Technical details on VPN detection

---

## ✅ Prerequisites

- Windows 10/11
- Python 3.8+
- Microsoft Outlook (desktop)
- Walmart VPN access
- Shared mailbox with "Send As" permissions

---

## 🛠️ What It Does

1. **Automatically downloads** manager data from SDL (hourly)
2. **Detects changes** by comparing daily snapshots
3. **Groups changes** by DC territory
4. **Sends emails** from your shared mailbox
5. **Retries for 7 days** if VPN unavailable

---

## 📧 Email Features

- **DC-Segmented:** Emails grouped by distribution center
- **Test Mode:** All emails go to you (safe for testing)
- **Shared Mailbox:** Sends from team mailbox (not personal)
- **HTML Format:** Professional, branded emails
- **Smart Alerts:** Incomplete DC alignment warnings

---

## 📊 What Gets Tracked

**~5,200 locations:**
- Walmart Supercenters (3,568)
- Neighborhood Markets (684)
- Discount Stores (346)
- Sam's Clubs (610)

**Roles:**
- Store/Club Manager
- Market Manager
- Regional GM
- DC GM/AGM

---

## 🔒 Security

- Runs under your Windows account
- No credentials stored
- VPN required for all operations
- Uses Outlook COM (Windows integrated auth)
- Data stays local or in your OneDrive

---

## 💡 Key Features

✅ **7-Day VPN Retry** - Keeps trying if laptop is off VPN  
✅ **Smart Deduplication** - Never processes same day twice  
✅ **Automated SDL Export** - No manual downloads  
✅ **Location Filters** - Focus on retail stores only  
✅ **Test Mode** - Safe testing before production  

---

## 🚀 Quick Commands

```bash
# Initial setup
python SETUP_WIZARD.py

# Test VPN
python vpn_checker.py

# Create first snapshot
python create_snapshot.py

# Manual daily check
python daily_check.py

# Set up automation (as admin)
setup_hourly_task_auto.bat
```

---

## 📞 Need Help?

1. Check `DEPLOYMENT_GUIDE.md` for detailed instructions
2. Review logs in `daily_run_log_*.txt`
3. Test each component individually
4. Contact your IT support or original deployer

---

## 📁 Version

**Version:** 2.0  
**Release Date:** January 2026  
**Python:** 3.8+  
**Platform:** Windows 10/11

---

**Ready to deploy!** See `DEPLOYMENT_GUIDE.md` for step-by-step instructions.
