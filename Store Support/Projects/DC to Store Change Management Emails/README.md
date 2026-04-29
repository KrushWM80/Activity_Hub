# DC Manager Change Detection System

**Production system for automated manager change tracking and DC leadership notification (PayCycle FY27)**

---

## 🚀 Production Status

**LAUNCHED:** April 17, 2026 (PC-06 ✅)  
**Distribution:** 21 PayCycles scheduled (PC-06 through PC-26)  
**Email Method:** Walmart SMTP Gateway (proven, reliable)  
**Next Execution:** PC-07 on May 1, 2026 @ 06:00 AM

---

## ⚠️ Data Source Information

**CURRENT STATUS (April 29):**
- Using **SYNTHETIC TEST DATA** from `create_synthetic_snapshots.py`
- Fake stores, fake managers for testing email pipeline only
- **NOT production data**

**MAY 1, 2026:**
- Real data from `sdl_scraper.py` (automated Playwright browser automation)
- Connects to Walmart SDL (Store Directory Lookup) system
- Exports real manager data and store information
- **THEN production email with real data**

**See:** `DATA_SOURCE_CLARIFICATION.md` for full details

---

## 📚 Core Documentation

- **EMAIL_SYSTEM_STANDARDS.md** - Standard email delivery method (SMTP gateway)
- **dc_email_config.py** - Configuration and settings
- **paycycle_tracking.json** - Execution history and timestamps
- **send_pc06_production_email.py** - Production email sender

---

## ✅ System Requirements

- Windows Server 2016+ (Task Scheduler)
- Python 3.8+ with venv
- pywin32 (for task scheduling)
- smtplib (built-in, SMTP email delivery)
- Internal network access to `smtp-gw1.homeoffice.wal-mart.com:25`

**NOTE:** No Outlook desktop required (uses SMTP gateway instead)

---

## 🛠️ What It Does

1. **Detects** manager changes from backend change management data
2. **Identifies** affected distribution centers using smart DC routing
3. **Targets** only DC leaders (GMs/AGMs) of affected DCs
4. **Sends emails** via Walmart internal SMTP gateway (reliable, proven method)
5. **Tracks** all executions with timestamps and recipient counts
6. **Monitors** via BCC recipients for internal team oversight

---

## 📧 Email Recipients

**Primary (TO):**
- DC General Managers (GM)
- DC Assistant General Managers (AGM)
- Only for DCs affected by manager changes (smart targeting)

**BCC (Internal Monitoring):**
- Kristine Torres (kristine.torres@walmart.com)
- Matthew Farnworth (matthew.farnworth@walmart.com)
- Kendall Rush (kendall.rush@walmart.com)

---

## 🔧 Email Settings

- **Subject:** Manager Change Report - PayCycle XX (Date)
- **From:** supplychainops@email.wal-mart.com
- **Content:** HTML formatted with greeting line
- **Greeting:** "Please make time to meet them and introduce yourself and the team at the DC."
- **Method:** SMTP Gateway (`smtp-gw1.homeoffice.wal-mart.com:25`)

---

## 📅 PayCycle Schedule (FY27)
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
