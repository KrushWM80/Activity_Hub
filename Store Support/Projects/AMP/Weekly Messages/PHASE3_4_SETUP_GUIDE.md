# Phase 3 & 4 Implementation Guide
# Adobe Analytics to BigQuery Pipeline - Tableau Prep & Task Scheduler Setup

---

## PHASE 3: TABLEAU PREP INTEGRATION

### Objective
Verify BigQuery tables can feed Tableau Prep with auto-refresh scheduling.

### Prerequisites
- Tableau Prep installed (version 2023.2+)
- GCP credentials available (same as loader script)
- BigQuery tables populated with data (from Phase 2)

### Step 1: Test BigQuery Connection

1. **Open Tableau Prep**
   ```
   Start → Programs → Tableau Prep
   ```

2. **Create New Flow**
   - Click "Create a new flow" button

3. **Add Input Source**
   - Click "Add Connection" or "+" button
   - Select **BigQuery**

4. **Configure Connection**
   - **Project ID**: `wmt-assetprotection-prod`
   - **Billing Project**: `wmt-assetprotection-prod` (or leave blank)
   - **Authentication**: 
     - Option 1: "Use Google Single Sign-On" (recommended)
     - Option 2: "Enter credentials manually"
   - Click **Connect**

5. **Select Tables**
   - Project: `wmt-assetprotection-prod`
   - Dataset: `Weekly_Message_FY27`
   - Table: `bq_weekly_messages_metrics` (start with this)
   - Click **Create**

6. **Preview Data**
   - View preview pane on right
   - Verify row counts and columns match expectations
   - Example: Should see ~1,500 rows with columns: report_date, category, page_name, page_views, unique_users, average_time_on_site, visits, extracted_date

### Step 2: Create Test Workflow

This is optional but recommended to validate the full pipeline.

1. **Create Multi-Input Workflow**
   - Add Input 1: `Weekly_Message_FY27.bq_weekly_messages_metrics`
   - Add Input 2: `Playbook_Hub_Data.bq_playbook_hub_metrics`

2. **Add Transforms** (optional)
   - Clean steps: Filter out invalid rows
   - Aggregate: Group by category, sum page views
   - Custom calculations if needed

3. **Add Output**
   - Can write back to BigQuery for validation
   - Or leave for existing Tableau Prep use case

4. **Save Workflow**
   ```
   File → Save
   Name: adobe_test_workflow
   Location: Store Support\Projects\AMP\Weekly Messages\tests\adobe_test_workflow.tflx
   ```

### Step 3: Verify Data Consistency

Compare row counts between BigQuery and Tableau Prep:

**In Tableau Prep**:
- Run flow
- Check output row count

**In BigQuery Console**:
```sql
SELECT COUNT(*) as row_count
FROM `wmt-assetprotection-prod.Weekly_Message_FY27.bq_weekly_messages_metrics`
WHERE DATE(extracted_date) = CURRENT_DATE();
```

Numbers should match!

### Step 4: Set Up Auto-Refresh Scheduling

**In Tableau Prep**:

1. **Save to Tableau Prep Server** (if using server deployments)
   - File → Publish to Tableau Prep Server
   - Or File → Save to cloud

2. **Configure Schedule** (Tableau Prep Server)
   - Right-click workflow
   - "Schedule"
   - **Frequency**: Weekly
   - **Day**: Monday
   - **Time**: 08:00 AM (loader runs Sunday 6 AM)
   - **Email notifications**: Enable if desired

3. **Test Manual Refresh**
   - Right-click workflow
   - "Run on Tableau Prep Server"
   - Check that it completes successfully

**Alternative: Blend with Existing Tableau Workflows**

If you have existing Tableau workflows:
1. Replace Excel input with BigQuery input
2. Point to `Weekly_Message_FY27` or `Playbook_Hub_Data` tables
3. Keep existing transforms/logic
4. Republish and test

### Troubleshooting Phase 3

| Issue | Solution |
|-------|----------|
| Connection fails | Check GCP credentials (`gcloud auth list`), verify project ID `wmt-assetprotection-prod` |
| "Table not found" | Verify BigQuery tables exist (see Phase 1 verification) |
| Row count mismatch | Check extracted_date filter, verify MERGE completed successfully in Phase 2 logs |
| Scheduling doesn't work | Ensure Tableau Prep Server is configured, or use Windows Task Scheduler instead |
| Permission denied | Verify user has BigQuery Dataset Editor role in IAM |

---

## PHASE 4: WINDOWS TASK SCHEDULER AUTOMATION

### Objective
Schedule Python loader to run every Sunday 6:00 AM automatically.

### Prerequisites
- Phase 2 (Python loader) fully tested and working
- Administrator access to Windows
- PowerShell 5.1+ (Windows 10/11 standard)

### Step 1: Create Scheduled Task

**Option A: Using PowerShell (Recommended)**

Open PowerShell **as Administrator**:

```powershell
# Configuration
$TaskName = "Adobe_Weekly_to_BigQuery_Loader"
$ScriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Weekly Messages\deploy_adobe_pipeline.ps1"
$TriggerDay = [System.DayOfWeek]::Sunday
$TriggerTime = "06:00:00"

# Step 1: Create weekly trigger (Sunday 6:00 AM)
Write-Host "Creating scheduled trigger..." -ForegroundColor Cyan
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $TriggerDay -At $TriggerTime

# Step 2: Create action (run PowerShell script)
Write-Host "Creating task action..." -ForegroundColor Cyan
$Action = New-ScheduledTaskAction `
  -Execute "powershell.exe" `
  -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""

# Step 3: Create task settings
Write-Host "Creating task settings..." -ForegroundColor Cyan
$Settings = New-ScheduledTaskSettingsSet `
  -StartWhenAvailable `
  -RunOnlyIfNetworkAvailable `
  -RunOnlyIfIdle:$false `
  -MultipleInstances IgnoreNew

# Step 4: Add retry (restart on failure)
$Settings.RestartCount = 2
$Settings.RestartInterval = (New-TimeSpan -Minutes 15)

# Step 5: Register task
Write-Host "Registering task..." -ForegroundColor Cyan
@"
Registering Scheduled Task:
  Name: $TaskName
  Trigger: Every $TriggerDay at $TriggerTime
  Script: $ScriptPath
  Run Level: HIGHEST (admin)
  Restart on Failure: Yes (max 2 retries, 15 min intervals)
"@

Register-ScheduledTask -TaskName $TaskName `
  -Trigger $Trigger `
  -Action $Action `
  -Settings $Settings `
  -RunLevel Highest `
  -Force

Write-Host "✓ Task created successfully!" -ForegroundColor Green
```

**Option B: Using Task Scheduler GUI**

1. **Open Task Scheduler**
   - Press `Win+R` → Type `taskschd.msc` → Enter

2. **Create Basic Task**
   - Right-click "Task Scheduler Library" → New → New Task

3. **General Tab**
   - Name: `Adobe_Weekly_to_BigQuery_Loader`
   - Description: "Weekly load of Adobe Analytics to BigQuery"
   - Security: Check "Run with highest privileges"

4. **Triggers Tab**
   - New Trigger
   - Begin the task: On a Schedule
   - Recurrence: Weekly
   - Repeat every: 1 week
   - Day: Sunday
   - Time: 06:00:00
   - Click OK

5. **Actions Tab**
   - New Action
   - Program/script: `powershell.exe`
   - Arguments: 
     ```
     -NoProfile -ExecutionPolicy Bypass -File "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Weekly Messages\deploy_adobe_pipeline.ps1"
     ```
   - Start in: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Weekly Messages`
   - Click OK

6. **Conditions Tab** (Optional)
   - ☑ Start the task only if the computer is on AC power
   - ☐ Stop if the computer switches to battery power
   - ☑ Wake the computer to run this task (optional)

7. **Settings Tab** (Optional)
   - ☑ Allow task to be run on demand
   - ☑ Run task as soon as possible if a scheduled run is missed
   - ☑ If the task fails, restart every: 15 minutes

8. **Finish & Save**

### Step 2: Verify Task is Registered

```powershell
# List the task
Write-Host "Checking if task exists..." -ForegroundColor Cyan
Get-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader" -ErrorAction Stop

# Get task details
Write-Host "`nTask Details:" -ForegroundColor Cyan
Get-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader" | Select-Object TaskName, @{Name='NextRunTime'; Expression={$_.Triggers.StartBoundary}}
```

### Step 3: Test Task Manually

```powershell
# IMPORTANT: Test before relying on automatic schedule

Write-Host "Testing task manually..." -ForegroundColor Yellow
Start-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader"

# Wait for execution
Start-Sleep -Seconds 5

# Check if task is running
Write-Host "Checking task status..." -ForegroundColor Cyan
Get-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader" | Select-Object State, @{Name='LastRunTime'; Expression={$_.LastRunTime}}

# Check logs
Write-Host "`nLast 30 lines of log:" -ForegroundColor Cyan
Get-Content "Store Support\Projects\AMP\Weekly Messages\logs\adobe_loader.log" -Tail 30
```

**Expected Output**:
- Task State: "Ready"
- Last Runtime: Should show very recent timestamp
- Log file should show:
  ```
  Adobe Analytics to BigQuery Loader - START
  [PHASE 1] Parsing Excel files...
  [PHASE 2] Loading to BigQuery...
  ...
  Adobe Analytics to BigQuery Loader - SUCCESS
  ```

### Step 4: Check Task History

```powershell
# View last 10 executions
Write-Host "Task Execution History:" -ForegroundColor Cyan
Get-ScheduledTaskInfo -TaskName "Adobe_Weekly_to_BigQuery_Loader" | Format-List

# View detailed history in Event Viewer
Write-Host "Opening Event Viewer for task logs..." -ForegroundColor Cyan
eventvwr /l "Microsoft-Windows-TaskScheduler/Operational"

# Filter for:
# - Event ID 200 (task started)
# - Event ID 201 (task completed)
# - Task Category: "Adobe_Weekly_to_BigQuery_Loader"
```

### Step 5: Verify BigQuery Data After Scheduled Run

After Sunday 6:00 AM task runs:

```sql
-- Check for today's data in BigQuery
SELECT DATE(extracted_date) as load_date, COUNT(*) as device_rows
FROM `wmt-assetprotection-prod.Weekly_Message_FY27.bq_weekly_messages_devices`
WHERE DATE(extracted_date) = CURRENT_DATE()
GROUP BY load_date;

-- Should show rows loaded on the current date
```

### Troubleshooting Phase 4

| Issue | Solution |
|-------|----------|
| Task fails on Sunday | Check: 1) GCP credentials available, 2) Excel file in correct folder, 3) Logs for error message |
| "Access Denied" error | Run Task Scheduler as Administrator, verify `RunLevel Highest` |
| Task shows "Ready" but never runs | Check trigger time, verify computer is powered on at 6 AM, check Event Viewer |
| Logs show 0 rows loaded | Check if Excel files are in the source folder, verify file names in `adobe_config.yaml` |
| Task runs but take forever | Normal for first run (dependencies install). Subsequent runs should be <2 minutes |
| Task disabled automatically | Check Event Viewer for reasons, re-enable: `Enable-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader"` |

### Maintenance & Monitoring

**Weekly Check**:
```powershell
# Monday morning, verify task ran successfully
Get-Content "Store Support\Projects\AMP\Weekly Messages\logs\adobe_loader.log" -Tail 50

# Verify Tableau Prep refreshed
# (manually check in Tableau Prep Server or your dashboard)
```

**Monthly Review**:
```powershell
# Check task history for failures
Get-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader" | Get-ScheduledTaskInfo

# Review log growth
(Get-Item "Store Support\Projects\AMP\Weekly Messages\logs\adobe_loader.log").Length / 1MB
# If >10 MB, consider archiving old logs
```

**Disable/Re-enable Task**:
```powershell
# Temporarily disable
Disable-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader"

# Re-enable
Enable-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader"
```

**Delete Task**:
```powershell
# Remove task (use with caution)
Unregister-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader" -Confirm:$false
```

---

## PHASE 3 & 4 COMPLETION CHECKLIST

### Phase 3: Tableau Prep
- [ ] Tableau Prep connects to BigQuery without errors
- [ ] Can browse tables in `Weekly_Message_FY27` and `Playbook_Hub_Data` datasets
- [ ] Data preview loads successfully in Tableau Prep
- [ ] Row counts in Tableau match BigQuery counts
- [ ] Test workflow (optional) runs without errors
- [ ] Auto-refresh schedule configured (Monday 8:00 AM recommended)

### Phase 4: Task Scheduler
- [ ] Task "Adobe_Weekly_to_BigQuery_Loader" created
- [ ] Task trigger set to: Sunday 6:00 AM, Weekly
- [ ] Manual test run completed successfully
- [ ] Logs show "SUCCESS" message
- [ ] BigQuery rows loaded after test run
- [ ] BigQuery validation queries confirm row counts
- [ ] Tableau Prep refreshes Monday morning with new data
- [ ] Verified data flows end-to-end: Excel → Python → BigQuery → Tableau Prep

---

## SUMMARY: FULL IMPLEMENTATION TIMELINE

| Phase | Task | Duration | Status |
|-------|------|----------|--------|
| **1** | Create BigQuery datasets & tables | 15 min | ✅ Complete SQL in Phase1_create_bigquery_tables.sql |
| **2** | Build Python loader script | 60 min | ✅ adobe_to_bigquery_loader.py ready |
| **2** | Config + Deployment scripts | 30 min | ✅ adobe_config.yaml + deploy_adobe_pipeline.ps1 ready |
| **2** | Documentation | 30 min | ✅ README.md complete |
| **2** | Test first run | 30 min | ☐ Manual test run (run: deploy_adobe_pipeline.ps1) |
| **3** | Tableau Prep integration | 45 min | ☐ Connect + schedule (see Phase 3 guide above) |
| **4** | Task Scheduler setup | 30 min | ☐ Create weekly task (see Phase 4 guide above) |
| **4** | End-to-end validation | 30 min | ☐ Verify full pipeline works |
| | **TOTAL** | **~6-7 hours** | **Ready for Production** |

---

**Next Steps**:
1. Complete Phase 2 test run (run `deploy_adobe_pipeline.ps1`)
2. Follow Phase 3 guide to set up Tableau Prep
3. Follow Phase 4 guide to schedule task
4. Verify first automatic Sunday 6 AM run

Good luck! 🚀
