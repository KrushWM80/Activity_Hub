# Workday Access Guide - Step-by-Step
## How to Connect and Export Job Master Data

**Date:** December 15, 2025  
**Purpose:** Get job descriptions for distribution list tool

---

## Step 1: Access Workday

### Option A: Walmart Workday Portal (Primary)

1. **Open your browser** (Chrome or Edge recommended)

2. **Navigate to Walmart Workday:**
   - URL: https://www.myworkday.com/walmart
   - Or search "Walmart Workday" in your browser
   - Or go through OneWalmart → Resources → Workday

3. **Login with your credentials:**
   - Username: Your Walmart username (same as Windows login)
   - Password: Your Walmart password
   - May require 2FA/MFA authentication

### Option B: Direct Workday Link

- Try: https://wd5.myworkday.com/walmart
- Or: https://walmart.workday.com

### Option C: Through OneWalmart

1. Go to https://one.walmart.com
2. Click on **Me** (top right)
3. Select **Workday** from dropdown
4. You'll be automatically logged in

---

## Step 2: Find Job Master Report

Once logged into Workday:

### Method 1: Search Bar (Fastest)

1. **Click the search bar** at the top of the page
2. **Type one of these:**
   - "Job Master"
   - "Jobs Report"
   - "Job Profiles"
   - "Job Data"

3. **Look for reports named:**
   - "Job Master Report"
   - "Job Data Export"
   - "Jobs Listing"
   - "Job Profiles Report"

4. **Click on the report** that appears in search results

### Method 2: Navigation Menu

1. **Click the menu icon** (☰ hamburger menu, top left)

2. **Navigate to:**
   ```
   Menu → Reports → Human Resources → Jobs
   ```
   Or:
   ```
   Menu → View → Human Resources → Jobs → Job Master
   ```

3. **Select:** "Job Master Report" or "Jobs Report"

### Method 3: Ask for Help

If you can't find it:

1. **Contact Workday Support:**
   - In Workday, search for "Help"
   - Or click your profile → Get Help
   - Ask: "How do I access the Job Master Report?"

2. **Or contact your HR Business Partner:**
   - They can send you the direct link
   - Or run the report for you

---

## Step 3: Configure the Report

Once you open the Job Master Report:

### Required Fields to Include:

1. **Essential Fields:**
   - ☑️ Job Code (or Job ID)
   - ☑️ Job Title / Job Name
   - ☑️ Job Description

2. **Optional But Helpful:**
   - ☑️ Job Family
   - ☑️ Job Level
   - ☑️ Grade
   - ☑️ Job Profile ID
   - ☑️ Active Status

### How to Add/Remove Columns:

1. Look for **"Columns"** or **"Edit Columns"** button
2. Click to open column selector
3. Check the boxes for fields you want
4. Uncheck fields you don't need
5. Click **"OK"** or **"Apply"**

### Filters to Apply:

**Important:** Filter to active jobs only

1. Find **"Filters"** or **"Prompts"** section
2. Add filter:
   - **Field:** "Active Status" or "Job Status"
   - **Value:** "Active" or "Current"
   - **Operator:** "Equals"

3. *(Optional)* Filter by specific job codes:
   - **Field:** "Job Code"
   - **Value:** Paste your job codes (from CSV)
   - **Operator:** "In" or "One of"

---

## Step 4: Export the Report

### Export to CSV (Recommended)

1. **Click the export button** (usually looks like ⬇️ or has "Export" text)

2. **Select format:**
   - Choose **"Excel"** or **"CSV"**
   - CSV is preferred for our merge script

3. **Download the file:**
   - File will download to your Downloads folder
   - Name will be something like: `Job_Master_Report_20251215.csv`

4. **Save with a better name:**
   - Rename to: `workday_jobs.csv`
   - Move to: `C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\`

### Export Options

**If export button has options:**
- Format: CSV or Excel
- Include headers: Yes
- Include filters: No
- Delimiter: Comma (not tab)

---

## Step 5: Verify the Export

### Check the CSV Format

Open the file in Excel or Notepad and verify:

**Good Format:**
```csv
job_code,job_title,job_description,job_family,job_level,grade
800469,Director - Market Operations,Director responsible for market H&W operations,Management,Director,GR45
814450,Market Manager,Manages market-level store operations,Field Operations,Manager,GR40
808250,Market Manager - Supercenter,Supercenter market manager,Field Operations,Manager,GR40
```

**Column Names May Vary:**
- "Job Code" or "Job_Code" or "JobCode" (any is fine)
- "Job Title" or "Job_Title" or "JobName"
- Headers should be in first row
- No blank rows at top

### Required Columns

Minimum you need:
1. Job code column
2. Job title/description column
3. (Optional) Job number/ID column

### Clean Up if Needed

If the CSV has extra info at top:
1. Open in Excel
2. Delete any rows above the header row
3. Save as CSV again

---

## Step 6: Use the Data

Now you're ready to merge!

```powershell
# Navigate to the folder
cd "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists"

# Test the merge (dry run)
python merge_workday_data.py `
    --ad-csv ad_groups_20251215_154559.csv `
    --workday-csv workday_jobs.csv `
    --output users_with_jobs.csv `
    --dry-run

# If looks good, run for real
python merge_workday_data.py `
    --ad-csv ad_groups_20251215_154559.csv `
    --workday-csv workday_jobs.csv `
    --output users_with_jobs.csv
```

---

## Troubleshooting

### "I can't find Workday"

**Solution:**
1. Go to https://one.walmart.com
2. Search for "Workday" in the search bar
3. Or ask your manager for the Workday link

### "I don't have access to Workday"

**Solution:**
1. You might need to request access
2. Contact your HR Business Partner
3. Or submit an access request through:
   - OneWalmart → IT Help
   - Or call IT Help Desk

### "I can't find Job Master Report"

**Solutions:**

**Option 1:** Use a different report name
- Try searching: "Jobs", "Job Profiles", "Position Data"
- Any report with job codes and titles will work

**Option 2:** Request from HR
- Email your HR team with this template:

```
Subject: Request for Job Master Data Export

Hi [HR Team],

I need a Workday export for a distribution list project.

Can you please export:
- Report: Job Master or Jobs Report
- Format: CSV
- Fields needed:
  * Job Code
  * Job Title/Description
  * Job Family (optional)
  * Job Level (optional)

Filter to: Active jobs only

I have about 150 unique job codes from our OPS Support groups.
Sample codes: 800469, 814450, 808250

Timeline: Needed this week if possible

Thanks!
```

**Option 3:** Use alternative data source
- Ask if there's a shared drive with job code mappings
- Check if your team has a job code reference document
- Some departments maintain their own job code lists

### "The export format doesn't match"

**Solution:**
The merge script is flexible. As long as you have:
1. A column with job codes
2. A column with job titles/descriptions

The column names don't need to match exactly. The script will try to find them.

### "Some job codes aren't in Workday"

**Explanation:**
- Some job codes may be:
  - Inactive/deprecated
  - Contractor codes (not in job master)
  - Position codes (different from job codes)

**Solution:**
- That's okay! The merge script handles this
- Missing codes will show as "NOT_FOUND"
- You'll still get 90-95% match rate
- Can manually look up the remaining codes

### "I get an error downloading the CSV"

**Solutions:**
1. Try Excel format instead (.xlsx)
   - You can convert to CSV later in Excel
   - File → Save As → CSV

2. Check file size
   - If too large, add more filters
   - Filter by specific business units
   - Or job codes you actually need

3. Try different browser
   - Chrome and Edge work best
   - Clear cache if issues

---

## Alternative: Request from HR (If Self-Service Doesn't Work)

If you can't access the report yourself:

### Email Template

```
To: [Your HR Business Partner]
Subject: Request for Workday Job Master Export

Hi [Name],

I'm working on a distribution list management tool for OPS Support 
and need to map job codes to job descriptions.

REQUEST:
Export from Workday with these fields:
  • Job Code
  • Job Title/Description  
  • Job Family (optional)
  • Job Level (optional)
  • Grade (optional)

FORMAT: CSV file

FILTERS:
  • Active jobs only
  • Include all job codes (we have ~150 unique codes)
  • Or specifically: 800469, 814450, 808250, 807245, 800474, etc.

PURPOSE: 
Creating accurate distribution lists for Store Support team 
communications. We have 2,684 users and need to organize by 
job description.

TIMELINE: 
Needed by end of week if possible (for December deliverable)

I can provide the full list of 150 job codes if that helps 
narrow the export.

Let me know if you need any additional information!

Thanks,
[Your Name]
```

### Who to Contact

**Primary contacts:**
- Your HR Business Partner
- Workday Support Team (search "Workday Help" in OneWalmart)
- Your manager (they may have access)

**Response time:**
- Usually 1-3 business days
- May be faster if you provide the specific job codes needed

---

## Quick Reference

### Workday URLs to Try
1. https://www.myworkday.com/walmart
2. https://wd5.myworkday.com/walmart
3. https://one.walmart.com → Workday link

### Search Terms in Workday
- "Job Master"
- "Jobs Report"
- "Job Profiles"
- "Job Data"

### Required Export Fields
- Job Code (minimum)
- Job Title/Description (minimum)
- Everything else is optional

### File Location
Save as: `C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\workday_jobs.csv`

---

## Next Steps After Getting CSV

1. **Verify file format** (open in Excel, check headers)
2. **Run dry-run merge** (test without writing output)
3. **Review match statistics** (should be 90-95%)
4. **Run actual merge** (create final CSV)
5. **Create distribution lists** (using merged data)

---

**Need Help?**
- Check the CODE_REVIEW_AND_IMPROVEMENTS.md file
- Review WORKDAY_INTEGRATION_GUIDE.md
- Or just ask - I can help troubleshoot!

**Status:** Ready to connect to Workday
**Action:** Try accessing Workday now using the steps above
**Timeline:** Should take 15-30 minutes total
