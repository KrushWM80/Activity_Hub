# 📊 Weekly Report System - Setup & Instructions

**Last Updated:** January 23, 2026  
**Report Frequency:** Every Friday  
**Execution Time:** ~15-20 minutes

---

## 🎯 How It Works

### **Weekly Workflow:**

#### **Tuesday/Wednesday - Capture Outside Work**
- Update `WEEKLY_CAPTURE_LOG.md` with work not in tracked systems
- Log meetings, calls, alignment discussions, dashboard work
- Takes ~5 minutes when done as you go

#### **Thursday Evening - Pre-Report Checklist**
- Run `PRE_REPORT_CHECKLIST.md` to identify missing items
- Verify all projects accounted for
- Get notified of items needing input

#### **Friday Morning - Generate Report**
- Run `GENERATE_WEEKLY_REPORT.ps1` PowerShell script
- Automatically:
  - Scans all project folders
  - Pulls latest documentation
  - Incorporates captured work items
  - Generates comprehensive report with time estimates
  - Creates PDF/HTML version
  - Saves timestamped copy

---

## 📁 System Structure

```
WEEKLY_REPORT_SYSTEM/
├── README.md                          ← YOU ARE HERE
├── WEEKLY_CAPTURE_LOG.md             ← Log work as it happens
├── PRE_REPORT_CHECKLIST.md           ← Run Thursday to verify
├── GENERATE_WEEKLY_REPORT.ps1        ← Run Friday morning
├── REPORT_TEMPLATE.md                ← Master template
├── FOLDER_SCAN_CONFIG.json           ← Configure what to scan
├── reports/                          ← Archive of all reports
│   ├── WEEKLY_REPORT_2026-01-17.md
│   ├── WEEKLY_REPORT_2026-01-24.md
│   └── [future reports...]
├── captured_work/                    ← Backup of weekly capture logs
│   ├── WEEK_2026-01-17.md
│   ├── WEEK_2026-01-24.md
│   └── [future captures...]
└── scripts/                          ← Supporting scripts
    ├── scan_folders.ps1
    ├── extract_metrics.ps1
    ├── time_estimator.ps1
    └── generate_pdf.ps1
```

---

## 🚀 Quick Start (This Friday)

### **Step 1: Review Current Work (5 minutes)**
Open: `WEEKLY_CAPTURE_LOG.md`

Add any work from this week NOT in the scanned projects:
- Calls and meetings
- Dashboard work
- Alignment discussions
- Approvals received
- Items needing Friday review

### **Step 2: Run Pre-Report Checklist (5 minutes)**
Open: `PRE_REPORT_CHECKLIST.md`

This will prompt you:
- ❓ Any additional projects to review?
- ❓ Meetings to include?
- ❓ Alignment work to add?
- ❓ Approvals/decisions this week?
- ❓ Anything else?

### **Step 3: Generate Report (5 minutes)**
Run in PowerShell:
```powershell
cd c:\Users\krush\Documents\VSCode\WEEKLY_REPORT_SYSTEM
.\GENERATE_WEEKLY_REPORT.ps1
```

**Output:**
- Comprehensive markdown report
- Time allocation breakdown
- Project status summary
- PDF version saved
- Previous report archived
- Timestamped file saved

---

## 📋 Weekly Capture Log

**Use:** `WEEKLY_CAPTURE_LOG.md` - Update as work happens

### **Each Day (2 minutes):**
1. Open the file
2. Add to appropriate section:
   - **Meetings/Calls** - Title, duration, outcome
   - **Alignment Work** - Team, status, decision
   - **Dashboards** - Project name, progress
   - **Approvals** - What was approved, by whom
   - **Other** - Anything else tracked

### **Example Entry:**

```markdown
## Wednesday 1/22/26

### Meetings & Calls
- **AMP Platform Call** (45 min)
  - Status: Performance review
  - Outcome: Issues logged for Auto Feeds
  - Attendees: 6 people

### Alignment Work
- **Fashion Team Meeting** (30 min)
  - Status: Tour Guides alignment finalized
  - Decision: APPROVED - Ready for MyWm Exp
  - Next: Begin integration phase

### Dashboard Work
- **Projects in Stores Dashboard** (2 hours)
  - Activity: AI tuning finalization
  - Status: Production-ready awaiting final review
```

---

## ✅ Pre-Report Checklist

**Use:** `PRE_REPORT_CHECKLIST.md` - Run Thursday evening

This file contains:
- ❓ Checklist of all known projects
- ❓ Prompts for work outside tracked systems
- ❓ Questions to verify coverage
- ⚠️ Warnings for missing data

**Run through it to:**
1. Confirm all tracked projects have latest data
2. Identify any work not yet captured
3. Get a checklist of items for Friday reporting

---

## 🤖 Automated Report Generation

**Use:** `GENERATE_WEEKLY_REPORT.ps1` - Run Friday morning

This PowerShell script automatically:

### **Scanning**
- Searches all configured project folders
- Reads latest documentation
- Extracts metadata and timestamps
- Identifies recent changes

### **Processing**
- Incorporates captured work items
- Calculates time spent estimates
- Categorizes by project/area
- Assesses status and progress

### **Reporting**
- Generates comprehensive markdown
- Creates executive summary
- Lists all deliverables
- Calculates time allocation
- Estimates remaining work

### **Output**
- `WEEKLY_REPORT_[DATE].md` - Main report
- `WEEKLY_REPORT_[DATE].pdf` - PDF version
- `WEEKLY_REPORT_[DATE].html` - HTML version
- Automatic backup to `reports/` folder
- Archive of capture log to `captured_work/` folder

---

## 🎯 What Gets Reported

Each Friday report includes:

### **1. Executive Summary**
- Overall week assessment (EXCEPTIONAL, GOOD, ON TRACK, etc.)
- Key metrics and achievements
- Time spent total

### **2. Project-by-Project Breakdown**
For each tracked project:
- ✅ What was accomplished
- ⏱️ Time spent (estimated)
- 📊 Deliverables created
- 📈 Status and progress
- 🎯 Next week focus

### **3. Additional Work**
- 📞 Calls and meetings
- 🤝 Alignment discussions
- 💼 Approvals/decisions
- 📋 Other activities

### **4. Metrics & Analysis**
- Time allocation by project
- Percentage completion by area
- Velocity and productivity
- Resource utilization

### **5. Next Week Preview**
- Upcoming meetings
- Scheduled decisions
- Planned deliverables
- Focus areas

---

## 📂 Configuration

### **FOLDER_SCAN_CONFIG.json**
Defines which folders/projects to scan:

```json
{
  "scan_paths": [
    "Refresh Guide",
    "Evaluation-System",
    "Activity-Hub",
    "Spark-Playground",
    "Intake Hub/ProjectsinStores",
    "Store Support/Projects"
  ],
  "file_patterns": [
    "*.md",
    "README.md",
    "*_SUMMARY.md",
    "*_STATUS.md"
  ],
  "look_back_days": 7
}
```

**Edit this to:**
- Add/remove project folders
- Change file patterns to scan
- Adjust how far back to look

---

## ⏱️ Time Estimates

The system will ask you to provide:
- **Actual time** if you tracked it
- **Estimate** if you didn't

For each project/area, you can input:
```
Project: Refresh Guide
Time: 30 hours
Break down:
  - Dashboard work: 12 hours
  - Analysis & reporting: 8 hours
  - Documentation: 5 hours
  - Data validation: 5 hours
```

Or just: `"30 hours"` and let system estimate breakdown

---

## 🔄 Running Each Week

### **Every Friday at 9:00 AM:**

```powershell
# Open PowerShell
cd c:\Users\krush\Documents\VSCode\WEEKLY_REPORT_SYSTEM

# Check capture log for completeness
notepad WEEKLY_CAPTURE_LOG.md

# Run report generation
.\GENERATE_WEEKLY_REPORT.ps1

# Follow prompts for:
# 1. Any additional work items?
# 2. Time estimates for projects
# 3. Special notes or achievements
```

**Output:** Report ready in ~5 minutes

---

## 📊 Report Archive

All weekly reports saved to `reports/` with timestamps:
- `WEEKLY_REPORT_2026-01-17.md`
- `WEEKLY_REPORT_2026-01-24.md`
- etc.

**Access anytime to:**
- Review historical progress
- Compare week-to-week metrics
- Track project evolution
- Analyze time allocation trends

---

## 💡 Tips for Success

### **Keep Capture Log Updated**
- Takes 2 minutes per day if done daily
- Much easier than trying to remember Friday
- Ensures nothing gets missed

### **Use Realistic Time Estimates**
- If unsure, estimate high
- System will average estimates over time
- Track actual when possible

### **Review Report Before Sharing**
- Check for accuracy
- Add context in "Notes" section
- Verify all projects represented
- Update status descriptions if needed

### **Make It a Friday Ritual**
- Same time each Friday
- ~15-20 minutes total
- Set calendar reminder
- Share report with stakeholders

---

## 🔧 Troubleshooting

### **Report won't generate?**
1. Verify PowerShell execution policy:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
2. Check `FOLDER_SCAN_CONFIG.json` syntax
3. Verify all paths exist

### **Missing project data?**
1. Check `FOLDER_SCAN_CONFIG.json` includes path
2. Verify README.md or *_STATUS.md exists in folder
3. Add manual entry to WEEKLY_CAPTURE_LOG.md

### **Time estimates seem off?**
1. Edit in `WEEKLY_CAPTURE_LOG.md` before running report
2. Use "actual" time instead of estimates
3. System learns from repeated estimates

---

## 🚀 Next Steps

1. **Copy `WEEKLY_CAPTURE_LOG.md` template** (already provided)
2. **Review `PRE_REPORT_CHECKLIST.md`** (already provided)
3. **Read `GENERATE_WEEKLY_REPORT.ps1`** (already provided)
4. **This Friday:** Run through the process
5. **Adjust** based on what works/doesn't

---

## 📞 Support

**Questions about:**
- **Capture Log format** → See WEEKLY_CAPTURE_LOG.md examples
- **Report generation** → See GENERATE_WEEKLY_REPORT.ps1 comments
- **Configuration** → Edit FOLDER_SCAN_CONFIG.json
- **Archived reports** → Check `reports/` folder

---

**Report System Ready to Use** ✅  
Run this Friday and adjust as needed!
