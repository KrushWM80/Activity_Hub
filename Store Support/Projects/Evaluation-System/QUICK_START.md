# Quick Start Guide - Evaluation System

## 🚀 Get Started in 5 Minutes

### Step 1: Install & Run

```bash
# Navigate to the Evaluation System directory
cd C:\Users\krush\Documents\VSCode\Evaluation-System

# Install dependencies (first time only)
npm install

# Start the server
npm start
```

**Expected Output:**
```
╔════════════════════════════════════════╗
║   Evaluation System Server Running     ║
╠════════════════════════════════════════╣
║   URL: http://localhost:3001           ║
║   API: http://localhost:3001/api       ║
║   Upload: POST /api/upload             ║
║   Evaluate: POST /api/evaluate         ║
║   Download: POST /api/download-html    ║
╚════════════════════════════════════════╝
```

### Step 2: Open in Browser

Navigate to: **http://localhost:3001**

### Step 3: Enter Your Information

1. Enter your name
2. Enter your title (optional but recommended)
3. Select evaluation period (Quarterly, Mid-Year, Fiscal Year, or Custom)
4. Click "Next: Input Data"

### Step 4: Upload or Enter Project Data

**Option A: Upload CSV/Excel File**
- Click the upload area or drag & drop your file
- File must include columns for projects
- System will show preview of first 5 rows

**Option B: Manual Entry**
- Click "Enter Projects Manually"
- You'll add projects one at a time in the next step

### Step 5: Map Your Columns

For each column in your file:
1. Select what that column represents (Project Name, Status, Description, etc.)
2. Hover over the "i" icon to see field description
3. Required fields (with *): Project Name, Description, Accomplishment
4. Click "Next: Generate Evaluation"

### Step 6: Generate Evaluation

Click "Generate Now" button
- System analyzes your data
- Calculates performance score (0-100)
- Generates professional narrative
- Maps to 4 leadership competencies

### Step 7: Review & Download

1. Review the generated evaluation
2. View or edit the HTML code if needed
3. Click "📥 Download as HTML" to save file
4. File will be named: `Evaluation_YourName_YYYY-MM-DD.html`

## 📊 Using Sample Data

We've provided sample project data in `SAMPLE_DATA.csv`:

```bash
# Option 1: Copy to your working directory
cp SAMPLE_DATA.csv MyProjects.csv

# Option 2: Upload directly through the web interface
# Go to Step 2 and upload SAMPLE_DATA.csv
```

**Sample includes 8 projects:**
- Refresh Guide (In Production)
- Activity-Hub Platform (Active)
- Spark Playground (In Production)
- Activity Hub Projects (Active)
- AMP Operations (Active)
- Intake Hub (Active)
- Pricing Dashboard (Active)
- EOC Systems (Active)

## 📋 Prepare Your Own Data

### Create a CSV File

**Minimum columns needed:**
```csv
Project,Description,Accomplishment,Impact,Hours
My Project,What it does,What was delivered,Business value,40
```

**Recommended columns:**
```csv
Project,Status,Description,Accomplishment,Impact,Users,Hours,Departments,Start,End
Project A,In Production,Modernized platform,Deployed successfully,27M value,50000,400,Eng|Ops,2025-01-01,2025-09-30
Project B,Active,New dashboard,Built analytics engine,Productivity +15%,100,200,Data|Prod,2025-03-01,2026-06-30
```

### Create an Excel File

Same structure as CSV:
- Column A: Project Name
- Column B: Status
- Column C: Description
- Column D: Accomplishment
- Column E: Impact/Business Value
- etc.

**Note:** First sheet will be used. Make sure headers are in row 1.

## ✅ Validation Checklist

Before uploading your data:

- [ ] File is CSV or Excel format
- [ ] File has headers in first row
- [ ] Each row is one project
- [ ] At least 1 project listed
- [ ] "Project" column present (or will map to Project Name)
- [ ] "Description" column present
- [ ] "Accomplishment" column present

## 🎯 Field Mapping Tips

### Auto-Detection
If your columns match these names, system auto-maps:
- `project` or `name` → Project Name
- `status` → Project Status
- `description` or `desc` → Description
- `accomplishment` or `achievement` → Accomplishment
- `value` or `impact` → Metric Value

### Manual Mapping
If auto-detection doesn't work:
1. Select matching column header
2. Choose system field from dropdown
3. Hover "i" for field description
4. Repeat for each column

### Example Mapping

Your File → System Field
- `Project` → project_name
- `Current Status` → project_status
- `What It Does` → description
- `Key Result` → accomplishment
- `Annual Value` → business_value
- `Team Members` → team_size
- `Who Was Involved` → team_departments

## 🎨 Understanding the Output

### Score Meanings
- **80-100: Exceeds Expectations** ⭐
  - Strong metrics, good collaboration, production delivered
- **70-79: Meets Expectations** ✓
  - Solid work across competencies
- **Below 70: Developing** 📈
  - Starting point for growth

### Sections in Generated Evaluation

1. **Executive Summary** - Overview of your work and impact
2. **Leadership Competencies** - Evidence for all 4 competencies
3. **Project Portfolio** - Detailed breakdown of each project
4. **Statistics** - Key metrics and team data

### What Gets Calculated

- Total projects, status breakdown
- Team members coordinated across projects
- Hours invested
- Departments involved
- Business value delivered
- Metric achievements
- Competency coverage score

## 🆘 Troubleshooting

### File Won't Upload
- Check file format (CSV or Excel only)
- Verify file can open in Excel/Sheets
- Try uploading a smaller file first
- Check file size (max 50MB)

### Can't Map Columns
- Make sure file has headers in first row
- Check that column names appear in preview
- Try renaming columns to match field names
- System requires: Project Name, Description, Accomplishment

### Evaluation Won't Generate
- Verify all required fields are mapped
- Check that each project row has values in required columns
- Empty cells in required fields will cause errors
- Re-upload file and re-map if needed

### Low Score After Generation
- Add more metrics to your projects
- Include team size and departments
- Add more competency information
- Ensure projects have clear business value

## 💡 Pro Tips

1. **Include Competency Evidence**
   - Add columns for how each project demonstrates leadership
   - Maps directly to promotion conversations

2. **Quantify Impact**
   - Users served, revenue generated, efficiency gains
   - Concrete numbers are more powerful

3. **Document Collaboration**
   - Team size and departments involved
   - Shows coordination ability

4. **Track Challenges**
   - What problems you solved
   - Demonstrates problem-solving ability

5. **Multiple Evaluations**
   - Generate quarterly to track progress
   - Show growth trends over time

## 📞 Getting Help

### Common Questions

**Q: Can I use this for multiple employees?**
A: Yes! Each person enters their own data and generates their evaluation.

**Q: Can I edit the HTML after downloading?**
A: Yes! Right-click the HTML file → Open with Editor to modify.

**Q: How do I update an evaluation?**
A: Upload the same data again with updated information and regenerate.

**Q: Can I add more projects later?**
A: Yes! Upload again with additional projects - just add new rows to your file.

**Q: What if my column names don't match?**
A: Use the manual mapping interface to match your columns to system fields.

## 🔄 Workflow Examples

### Quarterly Review
1. Copy previous period's data
2. Add new projects from the quarter
3. Update status and metrics
4. Upload and generate
5. Compare to previous quarter's evaluation

### Promotion Preparation
1. Collect all major projects from past year
2. Add competency evidence for each
3. Include quantified impact
4. Generate professional evaluation
5. Use in promotion/calibration conversations

### Team Manager Review
1. Request project lists from team members via spreadsheet template
2. Collect all responses
3. Generate standardized evaluations for each team member
4. Compare across team for calibration

## 🎓 Learning Resources

- Check `README.md` for full documentation
- Review field descriptions with "i" icons
- Look at `SAMPLE_DATA.csv` for examples
- Use help text in each form field

---

**Ready to generate your evaluation?**

```bash
npm start
# Then open http://localhost:3001 in your browser
```

**Questions or need help?** Check README.md or contact your administrator.

---

**Version:** 1.0.0  
**Last Updated:** January 2026
