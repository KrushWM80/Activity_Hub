# Activity Hub - File Reorganization Quick Start Guide

**Status:** Ready to execute file reorganization  
**Created:** March 5, 2026  
**Purpose:** Safely move ~80 scattered files from root Activity Hub folder to appropriate project directories

---

## 📋 What This Does

This guide walks you through reorganizing the Activity Hub workspace:
- **80 scattered Python/PowerShell files** currently in the root folder
- **Move them to 3 projects:** Zorro (25 files), JobCodes-teaming (15 files), TDA Insights (15 files)
- **Keep core operations** in root (17 files: scripts, docs, batch files)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Review the Plan (Optional but Recommended)
```powershell
# Read the detailed organization plan
Get-Content "FILE_ORGANIZATION_PLAN.md" | less
```

### Step 2: Run Dry-Run Test (Safe)
```powershell
# This shows what WILL happen WITHOUT making changes
.\MOVE_FILES.ps1 -DryRun -Confirm:$false
```
**Expected output:** List of directories to create and files to move

### Step 3: Execute the Reorganization
```powershell
# Actually move the files
.\MOVE_FILES.ps1 -Confirm:$false

# Or with manual confirmations (slower):
.\MOVE_FILES.ps1
```

---

## 🔍 Verify Success

After running MOVE_FILES.ps1:

### Check Health Status
```powershell
.\HEALTH_CHECK.ps1
```
Should show:
- ✓ Port 5000 (TDA Insights)
- ✓ Port 8001 (Projects in Stores)  
- ✓ Google Cloud Credentials
- ✓ Python environments

### Count Remaining Files
```powershell
Get-ChildItem -Filter "*.py" | Measure-Object
Get-ChildItem -Filter "*.ps1" | Where-Object Name -NotMatch "(HEALTH_CHECK|MOVE_FILES)" | Measure-Object
```
Should be ~17-20 files (core operations only)

### Test Both Flask Servers
```powershell
# Terminal 1: TDA Insights
cd "Store Support\Projects\TDA Insights"
python backend_simple.py

# Terminal 2: Projects in Stores  
cd "Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend"
python main.py

# Then test connectivity
Test-NetConnection localhost -Port 5000 -InformationLevel Quiet  # Should be True
Test-NetConnection localhost -Port 8001 -InformationLevel Quiet  # Should be True
```

---

## 📊 File Distribution After Reorganization

```
Activity_Hub (Root)
├── README.md                        ← Main documentation
├── OPERATIONS_DASHBOARD.md          ← Service info & startup guide
├── FILE_ORGANIZATION_PLAN.md        ← This reorganization plan
├── HEALTH_CHECK.ps1                 ← Run to verify services status
├── .gitignore                       ← Git ignore rules
│
└─ Store Support/Projects/
    │
    ├─ AMP/Zorro/
    │   └─ Audio/Scripts/            ← 25 voice/audio files moved here
    │       ├─ voice_management/
    │       ├─ generation/podcasts/
    │       ├─ conversion/
    │       └─ engines/
    │
    ├─ JobCodes-teaming/
    │   └─ Job Codes/scripts/        ← 15 job code analysis files moved here
    │       ├─ analysis/
    │       ├─ creation/
    │       ├─ extraction/
    │       ├─ queries/
    │       ├─ transformation/
    │       └─ verification/
    │
    └─ TDA Insights/
        └─ scripts/                  ← 15 BigQuery/Polaris files moved here
            ├─ schema/
            ├─ queries/
            └─ search/
```

---

## ⚠️ Troubleshooting

**Problem:** "Access Denied" when moving files
- **Solution:** Close any open files in VS Code or PowerShell terminals first
- **Solution:** Run PowerShell as Administrator

**Problem:** Script shows "Not found" for files
- **Solution:** Some files may already exist in destination directories
- **Solution:** Review FILE_ORGANIZATION_PLAN.md to check if this is expected

**Problem:** Flask servers won't start after move
- **Solution:** Check if Python paths need updating (see below)
- **Solution:** Run: `pip install -r requirements.txt` in the project directory
- **Solution:** Check HEALTH_CHECK.ps1 output for details

**Problem:** Imports fail (ModuleNotFoundError)
- **Solution:** Run `.\MOVE_FILES.ps1` again to ensure all files moved
- **Solution:** Check sys.path additions in files that import from moved directories
- **Solution:** May need to update file paths in __init__.py files

---

## 🔧 Post-Move Tasks (If Needed)

### 1. Update Imports (if any fail)
Find files with hardcoded paths:
```powershell
grep -r "from [\.\.]*\/Store Support" --include="*.py" Store\ Support\
```

Update them to use relative paths or environment variables.

### 2. Update sys.path (if needed)
Check if any Python files manually add paths:
```python
# OLD (won't work after move)
sys.path.insert(0, '../../')

# NEW (use relative paths)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

### 3. Verify Flask Servers
```powershell
# Test TDA Insights API
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/data" -ErrorAction SilentlyContinue
if ($response.StatusCode -eq 200) { Write-Host "TDA Insights API OK" }

# Test Projects in Stores API  
$response = Invoke-WebRequest -Uri "http://localhost:8001/api/status" -ErrorAction SilentlyContinue
if ($response.StatusCode -eq 200) { Write-Host "Projects in Stores API OK" }
```

---

## 📝 Final Commit

After successful reorganization:

```powershell
cd C:\Users\krush\OneDrive\ -\ Walmart\ Inc\Documents\VSCode\Activity_Hub

# Review changes
git status

# Stage and commit
git add .
git commit -m "Reorganize scattered files into project-specific directories

- Move 25 voice/audio/TTS files to Zorro/Audio/Scripts/
- Move 15 job code analysis files to JobCodes-teaming/Job Codes/scripts/
- Move 15 BigQuery/Polaris files to TDA Insights/scripts/
- Keep 17 core operations files in root Activity Hub
- Add HEALTH_CHECK.ps1 for service monitoring
- Update OPERATIONS_DASHBOARD.md with new file locations"

# Push to remote
git push
```

---

## 📞 Status Checks

**Monitor Service Status:**
```powershell
.\HEALTH_CHECK.ps1 -Verbose
```

**Track File Organization Progress:**
```powershell
$rootPy = (Get-ChildItem -Filter "*.py" | Measure-Object).Count
$rootPs1 = (Get-ChildItem -Filter "*.ps1" | Where-Object Name -NotMatch "(HEALTH|MOVE)" | Measure-Object).Count
Write-Host "Root .py files: $rootPy (target: ~5-8)"
Write-Host "Root .ps1 files: $rootPs1 (target: ~4-6)"
```

**Check Destination Directories:**
```powershell
(Get-ChildItem "Store Support\Projects\AMP\Zorro\Audio\Scripts" -Recurse -File | Measure-Object).Count
(Get-ChildItem "Store Support\Projects\JobCodes-teaming\Job Codes\scripts" -Recurse -File | Measure-Object).Count
(Get-ChildItem "Store Support\Projects\TDA Insights\scripts" -Recurse -File | Measure-Object).Count
```

---

## 🎯 Success Criteria

✅ All 80 files accounted for (moved or kept in root)  
✅ No errors in MOVE_FILES.ps1 output  
✅ HEALTH_CHECK.ps1 shows both services operational  
✅ Python imports work without errors  
✅ Flask servers start on ports 5000 + 8001  
✅ OPERATIONS_DASHBOARD.md reflects new file structure  
✅ Git commit includes all moved files  

---

## 🔗 Related Documents

- [OPERATIONS_DASHBOARD.md](OPERATIONS_DASHBOARD.md) - Service startup & monitoring guide
- [FILE_ORGANIZATION_PLAN.md](FILE_ORGANIZATION_PLAN.md) - Detailed reorganization manifest
- [HEALTH_CHECK.ps1](HEALTH_CHECK.ps1) - Service health verification script (run after changes)

---

**Ready to proceed?** Run the commands above in order. Start with the dry-run to review changes safely!
