# Scheduled Automation System

A template for creating background tasks that run on a schedule (hourly, daily, etc.) using Windows Task Scheduler.

## When to Use This Method

✅ **Good For:**
- Automated email reports
- Data synchronization between systems
- Change detection and notifications
- Periodic file processing
- Scheduled data exports
- Monitoring and alerting

❌ **Not Good For:**
- Web dashboards users access via URL
- APIs that need to respond to requests
- Real-time data displays
- Interactive web applications

---

## How It Works

```
┌─────────────────────┐
│   Task Scheduler    │ ← Triggers task (hourly/daily)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Your Script       │ ← Runs automation logic
│   (main.py)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Output            │ ← Sends emails, saves files
│   (email/file/API)  │
└─────────────────────┘
           │
           ▼
     Script EXITS
     (no resources used until next run)
```

---

## Template Files

### 1. `main_script.py` - Your Automation Logic

```python
"""
Scheduled Automation Script Template
Runs via Windows Task Scheduler
"""

import os
import sys
from datetime import datetime
import logging

# ============================================================
# CONFIGURATION
# ============================================================

LOG_FILE = "automation_log.txt"
DATA_FILE = "data_cache.json"

# ============================================================
# LOGGING SETUP
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# MAIN LOGIC
# ============================================================

def check_prerequisites():
    """Check if system is ready to run (VPN, network, etc.)"""
    # Add your checks here
    # Example: Check if VPN is connected
    # Example: Check if required files exist
    return True

def fetch_data():
    """Fetch data from source system"""
    logger.info("Fetching data...")
    # Add your data fetching logic
    # Example: Scrape website, call API, read database
    return {"sample": "data"}

def process_data(data):
    """Process the fetched data"""
    logger.info("Processing data...")
    # Add your processing logic
    # Example: Compare with previous data, detect changes
    return {"changes": []}

def send_notification(results):
    """Send notification with results"""
    logger.info("Sending notification...")
    # Add your notification logic
    # Example: Send email, post to Teams, save report
    pass

def main():
    """Main automation workflow"""
    logger.info("=" * 60)
    logger.info(f"Starting automation run at {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        # Step 1: Check prerequisites
        if not check_prerequisites():
            logger.warning("Prerequisites not met. Exiting...")
            return
        
        # Step 2: Fetch data
        data = fetch_data()
        
        # Step 3: Process data
        results = process_data(data)
        
        # Step 4: Send notification if needed
        if results.get("changes"):
            send_notification(results)
            logger.info(f"Notification sent for {len(results['changes'])} changes")
        else:
            logger.info("No changes detected")
        
        logger.info("Automation run completed successfully")
        
    except Exception as e:
        logger.error(f"Automation failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
```

### 2. `setup_scheduled_task.bat` - Task Scheduler Setup

```batch
@echo off
REM ============================================================
REM SCHEDULED TASK SETUP SCRIPT
REM ============================================================
REM
REM Customize these variables for your project:
REM   TASK_NAME    - Name shown in Task Scheduler
REM   PROJECT_PATH - Full path to your project folder
REM   SCRIPT_NAME  - Your main Python script
REM   SCHEDULE     - HOURLY, DAILY, WEEKLY, etc.
REM   START_TIME   - When to start (HH:MM)
REM
REM ============================================================

SET TASK_NAME=MyAutomationTask
SET PROJECT_PATH=C:\Users\krush\Documents\VSCode\YourProject
SET SCRIPT_NAME=main_script.py
SET SCHEDULE=HOURLY
SET START_TIME=06:00

echo.
echo ============================================================
echo SETTING UP SCHEDULED TASK
echo ============================================================
echo.
echo Task Name:    %TASK_NAME%
echo Project:      %PROJECT_PATH%
echo Script:       %SCRIPT_NAME%
echo Schedule:     %SCHEDULE% starting at %START_TIME%
echo.
echo Press CTRL+C to cancel, or
pause

REM Delete existing task if it exists
schtasks /Delete /TN "%TASK_NAME%" /F 2>nul

echo.
echo Creating scheduled task...

REM Create the scheduled task
schtasks /Create ^
    /TN "%TASK_NAME%" ^
    /TR "cmd /c cd /d %PROJECT_PATH% && python %SCRIPT_NAME% >> logs\run_%%date:~10,4%%%%date:~4,2%%%%date:~7,2%%.txt 2>&1" ^
    /SC %SCHEDULE% ^
    /ST %START_TIME% ^
    /RU "%USERNAME%" ^
    /RL HIGHEST ^
    /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo SUCCESS!
    echo ============================================================
    echo.
    echo Task created: %TASK_NAME%
    echo Schedule: %SCHEDULE% starting at %START_TIME%
    echo.
    echo To view: Open Task Scheduler and look for "%TASK_NAME%"
    echo To run now: Right-click task ^> Run
    echo To remove: schtasks /Delete /TN "%TASK_NAME%" /F
    echo.
) else (
    echo.
    echo ERROR: Failed to create scheduled task
    echo Make sure you have administrator privileges
    echo.
)

pause
```

### 3. `setup_scheduled_task.ps1` - PowerShell Alternative

```powershell
# ============================================================
# SCHEDULED TASK SETUP SCRIPT (PowerShell)
# ============================================================
# Run as Administrator for best results

# CUSTOMIZE THESE VALUES
$TaskName = "MyAutomationTask"
$ProjectPath = "C:\Users\krush\Documents\VSCode\YourProject"
$ScriptName = "main_script.py"
$Schedule = "Hourly"  # Hourly, Daily, Weekly
$StartTime = "06:00"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SETTING UP SCHEDULED TASK" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Task Name:  $TaskName"
Write-Host "Project:    $ProjectPath"
Write-Host "Script:     $ScriptName"
Write-Host "Schedule:   $Schedule starting at $StartTime"
Write-Host ""

# Remove existing task if exists
$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create trigger based on schedule type
switch ($Schedule) {
    "Hourly" { 
        # For hourly, we need to use repetition
        $trigger = New-ScheduledTaskTrigger -Once -At $StartTime -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 365)
    }
    "Daily" { 
        $trigger = New-ScheduledTaskTrigger -Daily -At $StartTime
    }
    "Weekly" { 
        $trigger = New-ScheduledTaskTrigger -Weekly -At $StartTime -DaysOfWeek Monday
    }
}

# Create action
$action = New-ScheduledTaskAction `
    -Execute "python" `
    -Argument "$ScriptName" `
    -WorkingDirectory $ProjectPath

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

try {
    # Register the task
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Trigger $trigger `
        -Action $action `
        -Settings $settings `
        -Description "Automated task for $ScriptName" `
        -Force

    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task created: $TaskName"
    Write-Host ""
    Write-Host "To view: Open Task Scheduler and look for '$TaskName'"
    Write-Host "To run now: Right-click task > Run"
    Write-Host "To remove: Unregister-ScheduledTask -TaskName '$TaskName'"
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "ERROR: $_" -ForegroundColor Red
    Write-Host "Make sure you're running as Administrator" -ForegroundColor Yellow
}
```

### 4. `requirements.txt` - Dependencies

```text
# Common dependencies for automation scripts

# HTTP requests
requests>=2.28.0

# Data processing
pandas>=1.5.0

# Email sending
# (uses built-in smtplib, email libraries)

# Environment variables
python-dotenv>=1.0.0

# Logging (built-in, but useful extras)
colorlog>=6.7.0

# Scheduling (alternative to Task Scheduler)
# schedule>=1.2.0

# Add your project-specific dependencies below:
```

---

## Project Structure

```
your-scheduled-project/
├── main_script.py              # Main automation logic
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── setup_scheduled_task.bat    # Windows batch setup
├── setup_scheduled_task.ps1    # PowerShell setup (alternative)
├── remove_scheduled_task.bat   # Remove the task
├── README.md                   # Project documentation
├── logs/                       # Execution logs
│   └── .gitkeep
└── data/                       # Data files
    └── .gitkeep
```

---

## Setup Instructions

### Step 1: Create Your Project
1. Copy this template to your project folder
2. Customize `main_script.py` with your automation logic
3. Update `requirements.txt` with your dependencies

### Step 2: Install Dependencies
```cmd
cd your-project-folder
pip install -r requirements.txt
```

### Step 3: Test Manually
```cmd
python main_script.py
```

### Step 4: Create Scheduled Task
Run as Administrator:
```cmd
setup_scheduled_task.bat
```
Or use PowerShell:
```powershell
.\setup_scheduled_task.ps1
```

### Step 5: Verify
1. Open Task Scheduler (`taskschd.msc`)
2. Find your task in the list
3. Right-click → Run to test

---

## Best Practices

### 1. Always Log Everything
```python
logging.info(f"Processing started at {datetime.now()}")
logging.info(f"Found {len(items)} items to process")
logging.info(f"Completed successfully")
```

### 2. Handle VPN/Network Issues
```python
def check_vpn():
    """Check if VPN is connected before proceeding"""
    try:
        response = requests.get("http://internal-server", timeout=5)
        return response.status_code == 200
    except:
        return False

if not check_vpn():
    logging.warning("VPN not connected - will retry next hour")
    return  # Exit and let Task Scheduler run again later
```

### 3. Track What's Already Processed
```python
def already_processed_today():
    """Check if we've already run successfully today"""
    marker = f"processed_{datetime.now().strftime('%Y%m%d')}.flag"
    return os.path.exists(marker)

def mark_processed():
    """Create marker file to prevent duplicate runs"""
    marker = f"processed_{datetime.now().strftime('%Y%m%d')}.flag"
    with open(marker, 'w') as f:
        f.write(datetime.now().isoformat())
```

### 4. Send Meaningful Notifications
```python
def send_summary_email(changes):
    """Send email only when there's something to report"""
    if not changes:
        logging.info("No changes - skipping email")
        return
    
    # Send email with actual changes
```

---

## Troubleshooting

### Task Not Running
1. Check Task Scheduler history for errors
2. Verify Python is in PATH
3. Test script manually first
4. Check log files in `logs/` folder

### Script Fails Silently
1. Add more logging statements
2. Check the log file output
3. Run manually to see errors

### VPN Issues
1. Add VPN check at script start
2. Log VPN status
3. Exit gracefully if VPN unavailable

---

## Real-World Example

See the working implementation at:
`C:\Users\krush\Documents\VSCode\Store Support\Projects\DC to Store Change Management Emails`

This project:
- Runs hourly via Task Scheduler
- Checks VPN connectivity
- Scrapes data from internal site
- Detects manager changes
- Sends email notifications
- Maintains 7-day retry window
