# Deployment Guide - Logic Rules Engine Scheduler Service

## Prerequisites

- Python 3.10+ installed
- Google Cloud BigQuery access (service account credentials)
- Activity Hub environment variable for `GOOGLE_APPLICATION_CREDENTIALS`

## Local Development Setup

### Step 1: Install Dependencies

```powershell
cd "Interface\Admin\Logic\Scheduler"
pip install -r requirements.txt
```

### Step 2: Set BigQuery Credentials

```powershell
# Set the environment variable for this session
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"

# Or permanently (in user environment)
[Environment]::SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS", "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json", "User")
```

### Step 3: Create BigQuery Tables

Before running the service, create the required tables in BigQuery:

```bash
# Copy query from Schemas/bigquery_tables.sql
# Paste into BigQuery Console
# Target dataset: wmt-assetprotection-prod.Store_Support_Dev
```

### Step 4: Run Scheduler Service

```powershell
# From Interface\Admin\Logic\Scheduler directory
python main.py
```

**Expected output:**
```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:5011 (Press CTRL+C to quit)
Scheduler loop started (interval: 300s)
```

### Step 5: Verify Service is Running

```powershell
# In another terminal
Invoke-WebRequest http://localhost:5011/health | ConvertTo-Json
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "Logic Rules Engine - Scheduler",
  "instance_id": "abc12345",
  "timestamp": "2026-04-06T12:34:56.789"
}
```

## Automated Startup (Windows Task Scheduler)

### Create Startup Task

1. **Open Task Scheduler**
   - Press `Win+R`, type `taskschd.msc`, press Enter

2. **Create New Task**
   - Right-click "Task Scheduler (Local)" → "Create Task..."
   - Name: `Activity_Hub_LogicScheduler_AutoStart`
   - Check: "Run with highest privileges"

3. **Set Trigger**
   - Triggers tab → New...
   - Begin the task: "At startup"
   - OK

4. **Set Action**
   - Actions tab → New...
   - Action: "Start a program"
   - Program/script: `python.exe` (or full path to python)
   - Arguments:
   ```
   -u "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\Admin\Logic\Scheduler\main.py"
   ```
   - Start in: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\Admin\Logic\Scheduler`
   - OK

5. **Set Environment**
   - General tab
   - Check: "Run whether user is logged in or not"
   - User account: `SYSTEM` (or your account)

6. **Save and Test**
   - OK to create task
   - Right-click task → Run
   - Verify service starts at `http://localhost:5011/health`

### Startup Script (Alternative)

Create `Interface\Admin\Logic\Scheduler\deploy_scheduler.ps1`:

```powershell
# Deploy and start Scheduler Service
$SchedulerPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\Admin\Logic\Scheduler"
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
cd $SchedulerPath
pip install -r requirements.txt

# Start service in background
Write-Host "Starting Scheduler Service on port 5011..." -ForegroundColor Green
Start-Process python main.py -NoNewWindow

# Wait and verify
Start-Sleep -Seconds 3
$health = Invoke-WebRequest http://localhost:5011/health | ConvertFrom-Json
Write-Host "✓ Scheduler Service healthy: $($health.status)" -ForegroundColor Green
```

Run it:
```powershell
& "Interface\Admin\Logic\Scheduler\deploy_scheduler.ps1"
```

## Remote Deployment

### On Remote Server (10.97.114.181)

1. **Copy files to remote**
   ```powershell
   # From local machine
   Copy-Item -Path "Interface\Admin\Logic\Scheduler" `
             -Destination "\\10.97.114.181\c$\Activity_Hub\Interface\Admin\Logic\Scheduler" `
             -Recurse -Force
   ```

2. **Setup on remote**
   ```powershell
   # Remote in as admin
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\gcloud\application_default_credentials.json"
   pip install -r requirements.txt
   ```

3. **Create remote scheduled task** (same as above but adjust paths)

4. **Verify remote service**
   ```powershell
   Invoke-WebRequest http://10.97.114.181:5011/health
   ```

## Configuration

Edit `Interface\Admin\Logic\Scheduler\main.py` to customize:

| Setting | Location | Default | Purpose |
|---------|----------|---------|---------|
| Port | Line 23 | 5011 | Service port |
| Trigger interval | Line 24 | 300 | Check for triggers every 5 min |
| Project ID | Line 31 | wmt-assetprotection-prod | BigQuery project |
| Dataset ID | Line 32 | Store_Support_Dev | BigQuery dataset |
| Debug mode | Line 26 | True | Verbose logging |

## Monitoring

### View Service Logs

```powershell
# If running in terminal
# Logs display in real-time

# If running as scheduled task
# Check Windows Event Viewer → Windows Logs → Application
```

### Check Scheduler Status

```powershell
Invoke-WebRequest http://localhost:5011/api/v1/scheduler/status | ConvertFrom-Json
```

**Output example:**
```json
{
  "status": "running",
  "instance_id": "abc12345",
  "check_interval_seconds": 300,
  "last_24_hours": {
    "total_executions": 42,
    "successful": 40,
    "failed": 2,
    "last_execution": "2026-04-06T12:30:00Z"
  }
}
```

### Query Execution Log (BigQuery)

```sql
SELECT 
    execution_id,
    trigger_timestamp,
    status,
    delivery_status,
    executed_at
FROM `wmt-assetprotection-prod.Store_Support_Dev.scheduler_execution_log`
WHERE DATE(executed_at) = CURRENT_DATE()
ORDER BY executed_at DESC
LIMIT 50
```

## Troubleshooting

### Problem: Service fails to start
```
Error: Failed to initialize BigQuery client
```

**Solution:** Check `GOOGLE_APPLICATION_CREDENTIALS` environment variable
```powershell
Get-Item env:GOOGLE_APPLICATION_CREDENTIALS
# Should show path to credentials file
```

### Problem: No projects detected
```
INFO: Detected 0 new projects since 2026-04-06 10:00:00
```

**Solution:** Check that projects table exists and has data
```sql
SELECT COUNT(*) FROM `wmt-assetprotection-prod.Store_Support_Dev.projects`
WHERE created_at > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
```

### Problem: Notifications not sent
```
WARN: No recipients resolved for rule abc-123
```

**Solution:** Check recipient_rule in notification_logic_rules table
```sql
SELECT rule_id, recipient_rule FROM notification_logic_rules
WHERE rule_id = 'abc-123'
```

### Problem: Service crashes on startup
```
ModuleNotFoundError: No module named 'google.cloud'
```

**Solution:** Reinstall dependencies
```powershell
pip uninstall google-cloud-bigquery -y
pip install -r requirements.txt
```

## Performance Notes

- Scheduler checks for triggers every **5 minutes** (configurable)
- Each project table scan limited to **100 records** to avoid timeout
- Notification delivery is **asynchronous** (doesn't block scheduler loop)
- **BigQuery partitioning** by DATE optimizes query performance

## Next Steps

1. Create BigQuery tables (see Step 3 above)
2. Start Scheduler Service locally
3. Test with sample Logic Request in Admin Dashboard
4. Set up scheduled task for automatic startup
5. Deploy to remote server when stable

## Rollback

If issues occur, stop the service and revert:

```powershell
# Stop service
Stop-Process -Name "python" -Force  # Or close terminal

# Revert code
git checkout Interface/Admin/Logic/Scheduler/

# Delete BigQuery tables if needed
# (in BigQuery Console)
```
