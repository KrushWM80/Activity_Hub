# 🤖 Generate Weekly Report Script

**Purpose:** Automatically generate comprehensive weekly report  
**Platform:** PowerShell (Windows)  
**Run Time:** ~5-10 minutes  
**Frequency:** Every Friday morning

---

## 📋 Quick Start

```powershell
cd c:\Users\krush\Documents\VSCode\WEEKLY_REPORT_SYSTEM
.\GENERATE_WEEKLY_REPORT.ps1
```

**Output:**
- `WEEKLY_REPORT_[DATE].md` - Main report
- `reports/WEEKLY_REPORT_[DATE].md` - Archived copy

---

## 📝 What Happens When You Run This

1. ✅ Scans configured project folders
2. ✅ Reads latest documentation
3. ✅ Extracts timestamps and status
4. ✅ Loads captured work items from log
5. ✅ Prompts for time estimates (if not provided)
6. ✅ Generates comprehensive report
7. ✅ Saves timestamped copies
8. ✅ Archives capture log

---

## ⚙️ Configuration

### **Projects to Scan**
Edit these paths in `FOLDER_SCAN_CONFIG.json`:

```json
{
  "scan_paths": [
    "Refresh Guide",
    "Evaluation-System", 
    "Activity-Hub",
    "Spark-Playground",
    "Intake Hub/ProjectsinStores",
    "Store Support/Projects"
  ]
}
```

### **Files to Read**
```json
{
  "file_patterns": [
    "README.md",
    "*_SUMMARY.md",
    "*_STATUS.md",
    "DELIVERY_SUMMARY.txt",
    "BUILD_SUMMARY.md"
  ]
}
```

### **How Far Back to Look**
```json
{
  "look_back_days": 7
}
```

---

## 🔧 Installation

### **Step 1: Create System Folder**
```powershell
mkdir "c:\Users\krush\Documents\VSCode\WEEKLY_REPORT_SYSTEM"
cd "c:\Users\krush\Documents\VSCode\WEEKLY_REPORT_SYSTEM"
mkdir reports
mkdir captured_work
mkdir scripts
```

### **Step 2: Copy Scripts**
All scripts are already created in this folder.

### **Step 3: Set Execution Policy** (One time only)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🏃 Running the Script

### **Friday Morning:**

```powershell
# Navigate to system folder
cd c:\Users\krush\Documents\VSCode\WEEKLY_REPORT_SYSTEM

# Run the script
.\GENERATE_WEEKLY_REPORT.ps1

# Follow prompts:
# 1. Any additional projects?
# 2. Time estimates
# 3. Special notes
# 4. Confirm generation
```

### **Output Files:**

```
WEEKLY_REPORT_2026-01-24.md          ← This week's main report
reports/WEEKLY_REPORT_2026-01-24.md  ← Archived copy
reports/WEEKLY_REPORT_2026-01-17.md  ← Last week
reports/WEEKLY_REPORT_2026-01-10.md  ← Historical
```

---

## 📊 Report Contents

The generated report includes:

### **1. Executive Summary**
- Overall assessment
- Key metrics
- Total hours worked
- Major achievements

### **2. Project Breakdowns**
For each scanned project:
- What was accomplished
- Time spent (from your estimates)
- Deliverables created
- Current status
- Next week focus

### **3. Captured Work**
From your WEEKLY_CAPTURE_LOG.md:
- Meetings and calls
- Alignment discussions
- Dashboard work
- Approvals and decisions

### **4. Time Analysis**
- Hours by project
- Percentage allocation
- Productivity metrics
- Estimated completion dates

### **5. Next Week Preview**
- Upcoming priorities
- Scheduled reviews
- Key deadlines
- Focus areas

---

## 💬 Interactive Prompts

When you run the script, you'll see:

### **Prompt 1: Additional Projects**
```
Any additional projects to include? (Y/N)
> [Type Y or N]
If Y: Enter project name and time spent
```

### **Prompt 2: Time Estimates**
```
Enter time spent on [Project Name] this week (hours):
> [Type number]
```

### **Prompt 3: Breakdown (Optional)**
```
Provide breakdown for [Project] (optional):
- Activity 1: __ hours
- Activity 2: __ hours
- Activity 3: __ hours
[Or leave blank for auto-estimate]
```

### **Prompt 4: Special Notes**
```
Any special notes for this week's report? (Y/N)
> [Type Y or N]
If Y: Enter notes (achievements, blockers, etc.)
```

### **Prompt 5: Confirm**
```
Generate report? (Y/N)
> [Type Y]
```

---

## 📂 File Structure After Running

```
WEEKLY_REPORT_SYSTEM/
├── README.md
├── WEEKLY_CAPTURE_LOG_TEMPLATE.md
├── PRE_REPORT_CHECKLIST.md
├── GENERATE_WEEKLY_REPORT.ps1 ← This script
├── FOLDER_SCAN_CONFIG.json
├── REPORT_TEMPLATE.md
│
├── reports/                        ← Archive
│   ├── WEEKLY_REPORT_2026-01-24.md
│   ├── WEEKLY_REPORT_2026-01-17.md
│   └── [historical reports...]
│
├── captured_work/                  ← Weekly capture logs
│   ├── WEEKLY_CAPTURE_2026-01-24.md
│   ├── WEEKLY_CAPTURE_2026-01-17.md
│   └── [historical captures...]
│
└── WEEKLY_REPORT_2026-01-24.md     ← This week (current)
```

---

## 🔍 Troubleshooting

### **Script won't run?**

**Error: "execution of scripts is disabled"**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Error: "path not found"**
- Verify you're in correct directory:
  ```powershell
  cd c:\Users\krush\Documents\VSCode\WEEKLY_REPORT_SYSTEM
  ```

### **Report is incomplete?**

1. Check `FOLDER_SCAN_CONFIG.json` syntax
2. Verify project paths exist
3. Check that README.md or *_STATUS.md files exist
4. Add missing data to WEEKLY_CAPTURE_LOG.md
5. Run script again

### **Time estimates seem wrong?**

- Edit WEEKLY_CAPTURE_LOG.md before running
- Re-run script with corrected estimates
- Script will use new values

### **Can't find generated report?**

Reports are saved in current directory with timestamp:
```powershell
# List all reports
ls WEEKLY_REPORT*.md

# Open latest
notepad WEEKLY_REPORT_2026-01-24.md
```

---

## 🎨 Customizing Report Output

### **Change Project List:**
Edit `FOLDER_SCAN_CONFIG.json`:
```json
"scan_paths": [
  "My Project 1",
  "My Project 2",
  "etc..."
]
```

### **Change File Patterns:**
Edit `FOLDER_SCAN_CONFIG.json`:
```json
"file_patterns": [
  "README.md",
  "*_STATUS.md",
  "CHANGELOG.md"
]
```

### **Change Look-Back Period:**
Edit `FOLDER_SCAN_CONFIG.json`:
```json
"look_back_days": 7  // Change to 14, 30, etc.
```

---

## 🔄 Making It a Ritual

### **Set a Calendar Reminder:**
- **Day:** Every Friday
- **Time:** 9:00 AM
- **Reminder:** "Generate weekly report"
- **Duration:** 15 minutes

### **Create a Shortcut:**
```powershell
# Create a batch file to launch script
# File: c:\Users\krush\Desktop\GENERATE_REPORT.bat

@echo off
cd c:\Users\krush\Documents\VSCode\WEEKLY_REPORT_SYSTEM
powershell -NoExit -Command ".\GENERATE_WEEKLY_REPORT.ps1"
```

Then: Double-click `GENERATE_REPORT.bat` each Friday

---

## 📊 Using Reports After Generation

### **Share with Stakeholders**
```powershell
# Open report in default markdown viewer
notepad WEEKLY_REPORT_2026-01-24.md

# Or convert to PDF/HTML using external tools
```

### **Track Progress Over Time**
```powershell
# Open reports folder
explorer reports

# Compare week-to-week reports
# Analyze trends
```

### **Extract Metrics**
```powershell
# See all reports
ls reports/ | Sort-Object LastWriteTime

# Get summaries
Get-Content reports/WEEKLY_REPORT_*.md | Select-String "Total Hours"
```

---

## ✨ Pro Tips

1. **Run Monday evening** to test script (no report artifacts)
2. **Update capture log daily** for best results
3. **Use realistic time estimates** - system learns from them
4. **Review report before sharing** - add context if needed
5. **Archive old reports** - keep only 13 weeks (1 quarter)

---

## 🚀 Ready to Use

This script is ready to run immediately.

**First execution:**
```powershell
cd c:\Users\krush\Documents\VSCode\WEEKLY_REPORT_SYSTEM
.\GENERATE_WEEKLY_REPORT.ps1
```

**Then every Friday morning:**
```powershell
.\GENERATE_WEEKLY_REPORT.ps1
```

---

## 📝 Version Info

- **Version:** 1.0
- **Created:** January 23, 2026
- **Last Updated:** January 23, 2026
- **Status:** Ready to use ✅

