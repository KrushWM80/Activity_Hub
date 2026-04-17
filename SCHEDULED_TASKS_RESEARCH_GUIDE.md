# Activity Hub Scheduled Tasks Creation & Management Guide
**Last Updated:** April 8, 2026  
**Maintainer:** Kendall Rush  
**Status:** Research & Best Practices Documentation

---

## Executive Summary

This document provides a comprehensive guide to creating, managing, and troubleshooting scheduled tasks in the Activity Hub ecosystem. The Activity Hub uses **Windows Task Scheduler** as the primary scheduling mechanism, wrapper scripts for process isolation, and PowerShell/Python for complex logic execution.

**Current Infrastructure:**
- 31+ scheduled tasks across all services
- 4 core auto-starting services (Projects, Job Codes, Daily Reports, AMP AutoFeed)
- 26 biweekly PayCycle automation tasks
- 100% uptime requirement for customer-facing dashboards

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Scheduling Mechanisms](#core-scheduling-mechanisms)
3. [Step-by-Step Task Creation Process](#step-by-step-task-creation-process)
4. [Task Types & Examples](#task-types--examples)
5. [Best Practices & Patterns](#best-practices--patterns)
6. [Service Integration Guide](#service-integration-guide)
7. [Troubleshooting & Monitoring](#troubleshooting--monitoring)
8. [Template Repository](#template-repository)

---

## Architecture Overview

### Why Windows Task Scheduler?

The Activity Hub chose Windows Task Scheduler for these reasons:

| Advantage | Why It Matters | Risk Mitigation |
|-----------|-----------------|-----------------|
| **Native Service** | No external dependencies; runs on Windows, not within Python/Node | .bat wrapper + SYSTEM account for reliability |
| **Persistent Execution** | Tasks survive terminal crashes, process kills, network interruptions | Scheduled tasks not affected by development activity |
| **SYSTEM-Level Access** | Runs with elevated privileges for file operations, registry access | Properly scoped account permissions |
| **Built-in Retry Logic** | Native retry on failure, configurable intervals | Exponential backoff for email failures |
| **Historical Data** | Full audit trail of runs, exit codes, output in Event Viewer | Enables root cause analysis for failures |

### Layered Architecture (Recommended)

```
┌─────────────────────────────────────────────────────┐
│         WINDOWS TASK SCHEDULER (Layer 1)            │
│  • Timing logic (daily, weekly, specific dates)     │
│  • Retry framework (native)                         │
│  • Execution audit trail                            │
│  • Runs when system/user not logged in              │
└──────────────────┬──────────────────────────────────┘
                   │ Triggers at scheduled time
                   ▼
┌─────────────────────────────────────────────────────┐
│    WRAPPER SCRIPT (Layer 2) — .bat or .ps1          │
│  • Environment variable setup (PATH, credentials)   │
│  • Process isolation (prevents terminal conflicts)  │
│  • Error handling & logging                         │
│  • CD to correct directory                          │
└──────────────────┬──────────────────────────────────┘
                   │ Invokes actual task
                   ▼
┌─────────────────────────────────────────────────────┐
│   BUSINESS LOGIC (Layer 3) — Python, PowerShell     │
│  • Data processing                                  │
│  • API calls                                        │
│  • Email generation                                 │
│  • Database updates                                 │
└─────────────────────────────────────────────────────┘
```

### Current Service Ports & Auto-Start Configuration

| Service | Port | Type | Auto-Start | Wrapper | Restart Trigger |
|---------|------|------|-----------|---------|-----------------|
| Projects in Stores | 8001 | FastAPI | ✅ Yes | `start_server_24_7.bat` | System startup + 30s delay |
| Job Codes Teaming | 8080 | FastAPI | ✅ Yes | `start_jobcodes_server_24_7.bat` | System logon |
| Job Codes Daily Sync | 8080† | Python | N/A | `start_jobcodes_server_24_7.bat` | Daily 2:00 AM |
| DC PayCycle Emails | N/A | Python | N/A | `.bat` wrapper (26 tasks) | Every 2 weeks @ 6:00 AM |
| Daily Status Reports | N/A | PowerShell | ✅ Yes | `MONITOR_AND_REPORT.ps1` | Daily 6:00 AM + startup |
| AMP AutoFeed | N/A | Python | ✅ Yes | `amp_run_daily.bat` | Daily 5:00 AM |
| V.E.T. Dashboard | 5001 | Flask | ❌ Manual | N/A | Manual start only |
| Scheduler Service | 5011 | FastAPI | ❌ Manual | N/A | Manual start (Logic Rules Engine) |

†Job Codes daily sync runs on same service as main API

---

## Core Scheduling Mechanisms

### Mechanism 1: Direct Service Auto-Start

**Used For:** Long-running services that must be available 24/7 (FastAPI/Flask backends)

**How It Works:**
1. Scheduled task runs `.bat` wrapper on system startup
2. Wrapper activates virtualenv, sets environment, executes main.py
3. Main.py binds to port and stays alive
4. Task Scheduler monitors process; can be set to restart if crashed

**Example Task Configuration:**

```powershell
# PowerShell: Create or verify auto-start task
$taskName = "ActivityHubServer"
$taskPath = "\Activity_Hub\"
$principal = New-ScheduledTaskPrincipal -UserID "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount -RunLevel Highest

$trigger = New-ScheduledTaskTrigger -AtStartup
$trigger.Delay = "PT30S"  # 30-second delay for system stability

$action = New-ScheduledTaskAction `
    -Execute "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_server_24_7.bat"

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName $taskName -TaskPath $taskPath -Principal $principal `
    -Trigger $trigger -Action $action -Settings $settings -Force
```

**Failure Modes & Recovery:**

| Failure | Symptom | Recovery |
|---------|---------|----------|
| Port already in use | Task exits immediately | Other process using port; check `netstat -ano \| Select-String ":8001"` |
| Python virtualenv missing | Import errors | Recreate `.venv` with `python -m venv .venv` |
| Network unavailable on startup | Connection refused | Task configured with `StartWhenAvailable` |
| File permissions | Access denied on startup | Run as SYSTEM with `RunLevel Highest` |

---

### Mechanism 2: Scheduled One-Time Execution

**Used For:** Scripts that should run at specific times (emails, reports, data syncs)

**How It Works:**
1. Task runs at scheduled time (e.g., 6:00 AM on specific dates)
2. Wrapper script executes business logic
3. Task completes and exits
4. Task Scheduler logs result in Windows Event Viewer

**Example: PayCycle Email Task**

```powershell
# Create single PayCycle task (repeat pattern for each date)
$taskName = "DC-EMAIL-PC-06"
$taskPath = "\Activity_Hub\PayCycle\"
$payPeriodDate = "2026-05-01"  # Start of PC-06

$trigger = New-ScheduledTaskTrigger -At "06:00:00" -Once -RepetitionInterval (New-TimeSpan -Days 0) | `
    Get-ScheduledTask -TaskName $taskName | Get-ScheduledTaskInfo

$runAsUser = "krush"
$principal = New-ScheduledTaskPrincipal -UserID "WAL-MART\$runAsUser" -LogonType Interactive -RunLevel Highest

$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c python platform\daily_check_smart.py send-paycycle --payperiod PC-06"

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable -StopIfGoingOffBatteries

Register-ScheduledTask -TaskName $taskName -TaskPath $taskPath -Principal $principal `
    -Trigger $trigger -Action $action -Settings $settings -Force
```

**Key Configuration Points:**

- **Once vs. Recurring:** Use `-Once` with specific date; use `-Recurring` with `-RepetitionInterval` for ongoing
- **User Context:** PayCycle tasks run as `WAL-MART\krush` (user account); system services run as `SYSTEM`
- **Failure Handling:** Native retry with exponential backoff (30s, 1m, 5m intervals configurable)

---

### Mechanism 3: Daily/Weekly Recurring Tasks

**Used For:** Reports, reconciliation, health checks that repeat indefinitely

**How It Works:**
1. Trigger set to recur daily/weekly at specified time
2. First run on specified date; then repeats forever
3. Can be paused/disabled without deletion
4. Long-term tracking via Event Viewer

**Example: Daily Status Report**

```powershell
$taskName = "ActivityHub-DailyStatus-6AM"

# Recurring daily at 6:00 AM, repeat every 1 day
$dailyTrigger = New-ScheduledTaskTrigger -Daily -At "06:00:00"

# Add repeat interval (repeat task every 24 hours after start time)
$dailyTrigger.Repetition.Interval = "PT24H"
$dailyTrigger.Repetition.StopAtDurationEnd = $false  # No stop time

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File MONITOR_AND_REPORT.ps1"

# Run as SYSTEM with highest privileges
$principal = New-ScheduledTaskPrincipal `
    -UserID "NT AUTHORITY\SYSTEM" `
    -LogonType ServiceAccount `
    -RunLevel Highest

Register-ScheduledTask -TaskName $taskName -Principal $principal -Trigger $dailyTrigger -Action $action -Force
```

---

## Step-by-Step Task Creation Process

### Before You Start: Pre-Flight Checklist

```checklist
☐ Task name follows naming convention (see Naming Patterns section)
☐ Script (Python/PowerShell/Batch) exists and runs manually without errors
☐ Script has error handling (try-catch, exit codes, logging)
☐ Output directory exists (for logs, reports)
☐ Required environment variables documented (PATH, Python version, etc.)
☐ Credentials locked down (no plaintext passwords in scripts)
☐ Decision made: SYSTEM account vs. user account (see Security section)
☐ Tested script with correct working directory
☐ Identified failure scenarios and recovery steps
```

### Phase 1: Create & Test the Execution Script

#### For Python Tasks

**Template: `my_scheduled_task.py`**

```python
#!/usr/bin/env python3
"""
Scheduled task template for Activity Hub.
Follows Activity Hub error handling patterns.
"""

import sys
import logging
from datetime import datetime
from pathlib import Path

# Setup logging (always first)
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main task execution."""
    try:
        logger.info("Task started")
        
        # ===== YOUR BUSINESS LOGIC HERE =====
        # 1. Load configuration
        # 2. Connect to services (BigQuery, APIs, etc.)
        # 3. Process data
        # 4. Handle results
        
        logger.info("Task completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Task failed: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
```

**How to Test:**

```powershell
# Activate virtualenv
& ".\.venv\Scripts\Activate.ps1"

# Run script directly
python my_scheduled_task.py

# Check exit code
echo $LASTEXITCODE
# Should print 0 for success, 1 for failure

# Verify log file created
Get-ChildItem logs/ -Newest 1
```

#### For PowerShell Tasks

**Template: `my_scheduled_task.ps1`**

```powershell
<#
.SYNOPSIS
Scheduled task template for Activity Hub.

.DESCRIPTION
Follows Activity Hub error handling and logging patterns.
Must be called with -ExecutionPolicy Bypass when scheduled.

.PARAMETER Action
Action to perform: send-email, sync-data, health-check, etc.

.EXAMPLE
.\my_scheduled_task.ps1 -Action 'send-email'
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('send-email', 'sync-data', 'health-check')]
    [string]$Action
)

# Error handling
$ErrorActionPreference = "Stop"

# Setup logging
$logDir = Join-Path $PSScriptRoot "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$logFile = Join-Path $logDir "task_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    Add-Content -Path $logFile -Value $logMessage
    Write-Host $logMessage
}

try {
    Write-Log "Task started with action: $Action"
    
    # ===== YOUR BUSINESS LOGIC HERE =====
    
    switch ($Action) {
        'send-email' { 
            # Email logic 
        }
        'sync-data' { 
            # Data sync logic 
        }
        'health-check' { 
            # Health check logic 
        }
    }
    
    Write-Log "Task completed successfully"
    exit 0
    
} catch {
    Write-Log "Task failed: $_" "ERROR"
    Write-Log $_.ScriptStackTrace "ERROR"
    exit 1
}
```

**How to Test:**

```powershell
# Test directly
& ".\my_scheduled_task.ps1" -Action "sync-data"

# Check exit code
$LASTEXITCODE
# Should print 0 for success

# View logs
Get-Content logs\task_*.log -Tail 20
```

#### For Batch File Wrapper

**Template: `wrapper_my_task.bat`**

```batch
@echo off
REM Batch wrapper for Activity Hub scheduled task
REM Sets environment and invokes Python script

setlocal enabledelayedexpansion

REM Get current directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Setup logs directory
if not exist "logs" mkdir "logs"

REM Get timestamp for logging
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set datestamp=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set timestamp=%%a%%b)

set "LOG_FILE=logs\task_%datestamp%_%timestamp%.log"

REM Activate Python virtualenv
call .venv\Scripts\activate.bat

REM Run Python script and log output
python my_scheduled_task.py >> "%LOG_FILE%" 2>&1

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

REM Deactivate virtualenv
call deactivate

REM Exit with same code
exit /b %EXIT_CODE%
```

**How to Test:**

```powershell
# Run wrapper directly
cmd /c wrapper_my_task.bat

# Check exit code
echo $LASTEXITCODE

# View logs
Get-Content logs\task_*.log -Tail 20
```

---

### Phase 2: Create the Wrapper Script (if needed)

**When to use Wrapper:**
- ✅ Python task running in virtualenv (need activation)
- ✅ Task needs environment variable setup
- ✅ Task needs directory change before execution
- ❌ Simple PowerShell script (call directly in Task Scheduler)
- ❌ Already using virtualenv activation in .bat

**Example: `Automation/start_paycycle_email.bat`**

```batch
@echo off
REM Activity Hub - DC PayCycle Email Sender
REM Scheduled by: DC-EMAIL-PC-* tasks
REM Run as: WAL-MART\krush

cd /d "%~dp0.."
cd "Platform\DC to Store Change Management Emails"

REM Setup Python environment
call .venv\Scripts\activate.bat

REM Setup logging
if not exist "logs" mkdir "logs"
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set datestamp=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set timestamp=%%a%%b)
set "LOG_FILE=logs\paycycle_%datestamp%_%timestamp%.log"

REM Run with optional pay cycle argument
python daily_check_smart.py send-paycycle --payperiod %1 >> "%LOG_FILE%" 2>&1

REM Exit with Python exit code
exit /b %ERRORLEVEL%
```

---

### Phase 3: Register the Scheduled Task

#### Option A: Interactive Setup (UI)

1. **Open Task Scheduler:**
   ```powershell
   taskschd.msc
   ```

2. **Create folder hierarchy:**
   - Right-click "Task Scheduler Library"
   - Select "New Folder"
   - Name: `Activity_Hub` (or `ActivityHub`, match existing convention)

3. **Create new task:**
   - Right-click your folder → "Create Task..."
   - **General tab:**
     - Name: `DC-EMAIL-PC-06` (follow naming convention)
     - Description: "Send DC manager weekly email for pay cycle 06"
     - User: `NT AUTHORITY\SYSTEM` (for system services) or `WAL-MART\krush` (for scheduled jobs)
     - ✅ Check: "Run with highest privileges"
     - ✅ Check: "Run whether user is logged in or not"

   - **Triggers tab:**
     - Click "New..."
     - Begin the task: "On a schedule"
     - Daily / Weekly / One-time (your choice)
     - Date/Time: Your schedule
     - ✅ Check: "Enabled"
     - Advanced: Set repeat interval if recurring

   - **Actions tab:**
     - Click "New..."
     - Action: "Start a program"
     - Program/script: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\wrapper_my_task.bat`
     - OR for PowerShell: `powershell.exe`
     - Add arguments: `-NoProfile -ExecutionPolicy Bypass -File my_script.ps1`
     - Start in: (blank - uses script directory)

   - **Conditions tab:**
     - ✅ Check: "Start the task only if the computer is on AC power"
     - ✅ Check: "Start the task only if the following network connection is available" → Any
     - ❌ Uncheck: "Stop if device switches to battery power"

   - **Settings tab:**
     - ✅ Check: "Allow task to be run on demand"
     - ✅ Check: "Stop the task if it runs longer than: 1 hour"
     - ✅ Check: "If the task fails, restart every: 5 minutes"
     - Max retry: 3 attempts
     - ✅ Check: "If the task finishes with a return code of 0, treat as successful"

4. **Click OK** and authenticate

#### Option B: PowerShell Automation

**Script: `Automation/register_scheduled_task.ps1`**

```powershell
<#
.SYNOPSIS
Register new scheduled task for Activity Hub

.PARAMETER TaskName
Name of the scheduled task (e.g., "DC-EMAIL-PC-06")

.PARAMETER TaskDescription
What the task does

.PARAMETER ScheduleType
"Once", "Daily", "Weekly", custom

.PARAMETER ExecutionTime
Time to run (e.g., "06:00:00")

.PARAMETER ExecutionDate
Date to run (e.g., "2026-05-01")

.PARAMETER ScriptPath
Path to .bat wrapper or .ps1 script

.EXAMPLE
.\register_scheduled_task.ps1 `
  -TaskName "DC-EMAIL-PC-06" `
  -TaskDescription "Send weekly DC manager email" `
  -ScheduleType "Once" `
  -ExecutionDate "2026-05-01" `
  -ExecutionTime "06:00:00" `
  -ScriptPath "Automation\start_paycycle_email.bat"
#>

param(
    [Parameter(Mandatory=$true)] [string]$TaskName,
    [Parameter(Mandatory=$true)] [string]$TaskDescription,
    [Parameter(Mandatory=$true)] [string]$ScheduleType,
    [Parameter(Mandatory=$true)] [string]$ExecutionTime,
    [string]$ExecutionDate,
    [Parameter(Mandatory=$true)] [string]$ScriptPath,
    [string]$TaskArguments = ""
)

# Validate inputs
if (-not (Test-Path $ScriptPath)) {
    Write-Error "Script not found: $ScriptPath"
    exit 1
}

# Resolve script path to absolute
$ScriptPath = (Resolve-Path $ScriptPath).Path

# Determine principal (who runs task)
$principal = New-ScheduledTaskPrincipal `
    -UserID "NT AUTHORITY\SYSTEM" `
    -LogonType ServiceAccount `
    -RunLevel Highest

# Create trigger based on schedule type
$trigger = switch ($ScheduleType) {
    "Once" {
        [datetime]$runTime = "$ExecutionDate $ExecutionTime"
        New-ScheduledTaskTrigger -At $runTime -Once
    }
    "Daily" {
        [datetime]$runTime = $ExecutionTime
        New-ScheduledTaskTrigger -Daily -At $runTime
    }
    "Weekly" {
        New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -WeeksInterval 2 -At $ExecutionTime
    }
    default { throw "Unknown schedule type: $_" }
}

# Create action (what to execute)
if ($ScriptPath -like "*.bat") {
    $action = New-ScheduledTaskAction `
        -Execute $ScriptPath `
        -Argument $TaskArguments
} else {
    $action = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`" $TaskArguments"
}

# Configure settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5) `
    -StopIfGoingOffBatteries:$false

# Register task
Write-Host "Registering task: $TaskName"
try {
    $task = Register-ScheduledTask `
        -TaskName $TaskName `
        -TaskPath "\Activity_Hub\" `
        -Principal $principal `
        -Trigger $trigger `
        -Action $action `
        -Settings $settings `
        -Description $TaskDescription `
        -Force

    Write-Host "✓ Task registered successfully"
    Write-Host "  Task name: $($task.TaskName)"
    Write-Host "  Triggers: $(($task.Triggers | Measure-Object).Count)"
    
} catch {
    Write-Error "Failed to register task: $_"
    exit 1
}
```

**How to Use:**

```powershell
# Register single PayCycle task
.\register_scheduled_task.ps1 `
    -TaskName "DC-EMAIL-PC-06" `
    -TaskDescription "Send DC manager email for PC-06" `
    -ScheduleType "Once" `
    -ExecutionDate "2026-05-01" `
    -ExecutionTime "06:00:00" `
    -ScriptPath "Automation\start_paycycle_email.bat"

# Register recurring daily task
.\register_scheduled_task.ps1 `
    -TaskName "JobCodes-Daily-Reconciliation" `
    -TaskDescription "Reconcile job codes daily" `
    -ScheduleType "Daily" `
    -ExecutionTime "02:00:00" `
    -ScriptPath "Store Support\Projects\JobCodes-teaming\Teaming\dashboard\reconcile.py"
```

---

### Phase 4: Verify & Monitor

#### Immediate Verification (Before Task Triggers)

```powershell
# List task
Get-ScheduledTask -TaskName "DC-EMAIL-PC-06" | Format-List *

# Run manually to test
Get-ScheduledTask -TaskName "DC-EMAIL-PC-06" | Start-ScheduledTask

# Monitor execution
Get-ScheduledTaskInfo -TaskName "DC-EMAIL-PC-06"

# Check logs
Get-WinEvent -LogName "Microsoft-Windows-TaskScheduler/Operational" `
    -FilterXPath "*[System[Computer='COMPUTER_NAME' and EventID=201]]" `
    -Newest 5 -ErrorAction SilentlyContinue
```

#### Ongoing Monitoring

```powershell
# Setup periodic monitoring (every hour)
$task = Get-ScheduledTask -TaskName "DC-EMAIL-PC-06"
$info = $task | Get-ScheduledTaskInfo

Write-Host "Last Run Time: $($info.LastRunTime)"
Write-Host "Last Task Result: $($info.LastTaskResult)"  # 0 = success
Write-Host "NextRunTime: $($info.NextRunTime)"

# Setup for failure alerts
if ($info.LastTaskResult -ne 0) {
    Write-Warning "Task failed with exit code: $($info.LastTaskResult)"
    # Send email alert here
}
```

---

## Task Types & Examples

### Type 1: Background Service (Always-On)

**Purpose:** Long-running API/web server  
**Frequency:** Runs continuously after startup  
**Restart on Failure:** Yes (automatic)  
**Log Output:** Console + Windows Event Viewer  

**Example: Projects in Stores API**

```powershell
# Wrapper: start_server_24_7.bat
@echo off
cd /d "%~dp0.."
cd "Store Support\Projects\Platform"

call .venv\Scripts\activate.bat

python main.py
REM Server stays running; never exits normally
```

```powershell
# Task Scheduler Config
$trigger = New-ScheduledTaskTrigger -AtStartup
$trigger.Delay = "PT30S"  # Wait 30 seconds for system stability

$action = New-ScheduledTaskAction `
    -Execute "C:\...Automation\start_server_24_7.bat"

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew

$principal = New-ScheduledTaskPrincipal -UserID "NT AUTHORITY\SYSTEM" -RunLevel Highest

Register-ScheduledTask -TaskName "ActivityHubServer" -Principal $principal `
    -Trigger $trigger -Action $action -Settings $settings -Force
```

**Troubleshooting Checklist:**

```
❌ Port already in use?
  → netstat -ano | Select-String ":8001"
  → Kill occupying process, restart

❌ Process started but won't bind?
  → Check logs for startup errors
  → Verify virtualenv activation: .venv\Scripts\activate.bat

❌ Task disappears after reboot?
  → Check SYSTEM user permissions
  → Verify Run Level = Highest
  → Check: "Run whether user is logged in or not"
```

---

### Type 2: Scheduled Report/Email (One-Time or Recurring)

**Purpose:** Generate reports, send emails at scheduled times  
**Frequency:** Daily, weekly, or specific dates  
**Restart on Failure:** Yes (with retry intervals)  
**Log Output:** Script log files + exit code tracking  

**Example: DC PayCycle Email**

**Python Script: `daily_check_smart.py`**

```python
import click
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--payperiod', required=True, help='Pay period code (e.g., PC-06)')
def send_paycycle(payperiod):
    """Send DC manager email for specified pay period."""
    try:
        logger.info(f"Sending PayCycle email for {payperiod}")
        
        # 1. Generate report data
        report_content = generate_report(payperiod)
        
        # 2. Send email
        send_email(
            recipients=['ATCTeamsupport@walmart.com', 'kendall.rush@walmart.com'],
            subject=f"DC Activity Hub - {payperiod} Weekly Report",
            body=report_content
        )
        
        logger.info(f"✓ Email sent for {payperiod}")
        return 0
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    exit_code = cli()
    sys.exit(exit_code if exit_code else 0)
```

**Wrapper: `start_paycycle_email.bat`**

```batch
@echo off
cd /d "%~dp0.."
cd "Platform\DC to Store Change Management Emails"

call .venv\Scripts\activate.bat

for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set datestamp=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set timestamp=%%a%%b)
set "LOG_FILE=logs\paycycle_%datestamp%_%timestamp%.log"

python daily_check_smart.py send-paycycle --payperiod %1 >> "%LOG_FILE%" 2>&1
exit /b %ERRORLEVEL%
```

**Registration: 26x PayCycle Tasks**

```powershell
# Define all 26 pay cycle dates for FY27
$PayCycles = @(
    @{ Code = "PC-06"; Date = "2026-05-01" },
    @{ Code = "PC-07"; Date = "2026-05-15" },
    # ... continue for all 26
)

# Register each task
foreach ($pc in $PayCycles) {
    $taskName = "DC-EMAIL-$($pc.Code)"
    
    $scriptPath = Resolve-Path "Automation\start_paycycle_email.bat"
    
    $trigger = New-ScheduledTaskTrigger `
        -At "06:00:00" `
        -Once `
        -RepetitionInterval (New-TimeSpan -Days 0)
    
    # Set actual date (need separate setup for date parameter)
    $trigger.StartBoundary = "$($pc.Date)T06:00:00"
    
    $action = New-ScheduledTaskAction `
        -Execute $scriptPath `
        -Argument $pc.Code
    
    Register-ScheduledTask -TaskName $taskName `
        -TaskPath "\Activity_Hub\PayCycle\" `
        -Trigger $trigger `
        -Action $action `
        -Principal (New-ScheduledTaskPrincipal -UserID "WAL-MART\krush" -RunLevel Highest) `
        -Force
    
    Write-Host "✓ Registered $taskName for $($pc.Date)"
}
```

**Monitoring:**

```powershell
# Check last execution
Get-ScheduledTaskInfo -TaskName "DC-EMAIL-PC-06" |
    Select-Object -Property TaskName, LastRunTime, LastTaskResult

# Review logs
Get-ChildItem "Platform\DC to Store Change Management Emails\logs\" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 3 |
    ForEach-Object { Get-Content $_.FullName | Write-Host }
```

---

### Type 3: Health Check / Monitoring Task

**Purpose:** Verify services are running, send alerts if issues  
**Frequency:** Daily at startup or at regular intervals  
**Restart on Failure:** Yes  
**Log Output:** Event log + email notifications  

**Example: Daily Status Report**

**PowerShell Script: `MONITOR_AND_REPORT.ps1`**

```powershell
<#
.SYNOPSIS
Monitor Activity Hub services and send daily status report
#>

param(
    [switch]$QuietMode  # Suppress console output
)

$services = @{
    "ProjectsInStores" = @{ Port = 8001; Service = "FastAPI" }
    "JobCodesDashboard" = @{ Port = 8080; Service = "FastAPI" }
    "AMP_AutoFeed" = @{ Service = "Scheduled"; LastRun = "5:00 AM" }
}

$healthReport = @()

# Check port availability
foreach ($name in $services.Keys) {
    $service = $services[$name]
    
    if ($service.Port) {
        $portCheck = Test-NetConnection -ComputerName "localhost" `
            -Port $service.Port -ErrorAction SilentlyContinue
        
        $status = if ($portCheck.TcpTestSucceeded) { "✓ UP" } else { "❌ DOWN" }
        
        $healthReport += [PSCustomObject]@{
            Service = $name
            Status = $status
            LastChecked = Get-Date
        }
    }
}

# Check scheduled task status
$tasks = @(
    "DC-EMAIL-PC-*",
    "JobCodes-Daily-Reconciliation",
    "ActivityHub-DailyStatus-6AM"
)

foreach ($taskPattern in $tasks) {
    $tasks_found = Get-ScheduledTask -TaskName $taskPattern -ErrorAction SilentlyContinue
    
    foreach ($task in $tasks_found) {
        $info = Get-ScheduledTaskInfo -TaskName $task.TaskName
        $status = if ($info.LastTaskResult -eq 0) { "✓ Success" } else { "⚠ Failed ($($info.LastTaskResult))" }
        
        $healthReport += [PSCustomObject]@{
            Service = "Task: $($task.TaskName)"
            Status = $status
            LastRun = $info.LastRunTime
        }
    }
}

# Generate email report
$htmlBody = @"
<html>
<body>
<h2>Activity Hub Daily Status Report</h2>
<p>Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')</p>

<table border="1" style="border-collapse: collapse;">
<tr style="background-color: #f0f0f0;">
    <th>Service</th>
    <th>Status</th>
    <th>Last Checked</th>
</tr>
"@

foreach ($report in $healthReport) {
    $htmlBody += @"
<tr>
    <td>$($report.Service)</td>
    <td>$($report.Status)</td>
    <td>$($report.LastChecked)</td>
</tr>
"@
}

$htmlBody += "</table></body></html>"

# Send email
$emailParams = @{
    To = @('ATCTeamsupport@walmart.com', 'kendall.rush@walmart.com')
    Subject = "Activity Hub Daily Status - $(Get-Date -Format 'yyyy-MM-dd')"
    Body = $htmlBody
    BodyAsHtml = $true
    SmtpServer = "relay.walmart.com"
    From = "ActivityHub@walmart.com"
}

Send-MailMessage @emailParams -ErrorAction Continue

if (-not $QuietMode) {
    Write-Host $($healthReport | Format-Table | Out-String)
}
```

**Registration:**

```powershell
# Daily at 6:00 AM
$trigger = New-ScheduledTaskTrigger -Daily -At "06:00:00"

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File MONITOR_AND_REPORT.ps1"

Register-ScheduledTask -TaskName "ActivityHub-DailyStatus-6AM" `
    -Path "\Activity_Hub\" `
    -Principal (New-ScheduledTaskPrincipal -UserID "NT AUTHORITY\SYSTEM" -RunLevel Highest) `
    -Trigger $trigger `
    -Action $action `
    -Force

# Also on system startup (send immediate report)
$trigger2 = New-ScheduledTaskTrigger -AtStartup
$trigger2.Delay = "PT2M"  # Wait 2 minutes for services to start

Register-ScheduledTask -TaskName "ActivityHub-Startup-Report" `
    -Path "\Activity_Hub\" `
    -Principal (New-ScheduledTaskPrincipal -UserID "NT AUTHORITY\SYSTEM" -RunLevel Highest) `
    -Trigger $trigger2 `
    -Action $action `
    -Force
```

---

## Best Practices & Patterns

### 1. Naming Conventions

**Consistent naming prevents confusion and enables pattern matching for bulk operations.**

```
Pattern: {SYSTEM}-{TYPE}-{IDENTIFIER}
Examples:
  ✓ ActivityHub-Server-Main
  ✓ DC-EMAIL-PC-06
  ✓ JobCodes-Daily-Reconciliation
  ✓ AMP-AutoFeed-Daily

Service Prefixes:
  ActivityHub, DC (District Manager), JobCodes, AMP (AutoFeed)

Type Indicators:
  -Server, -Email, -Reconciliation, -Report, -AutoFeed, -Cleanup

Date Suffixes (for one-time tasks):
  -2026-05-01, or embedded in name -PC-06
```

### 2. Error Handling & Exit Codes

**Critical: Always use exit codes for task success/failure determination.**

**Python:**

```python
def main():
    try:
        # Business logic
        return 0  # Success
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1  # Failure

sys.exit(main())
```

**PowerShell:**

```powershell
try {
    # Business logic
    exit 0
} catch {
    Write-Error $_
    exit 1
}
```

**Batch:**

```batch
REM Do work
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

exit /b 0
```

**Task Scheduler Setting:**

```powershell
# Task must return exit code 0 to be considered successful
-Settings (New-ScheduledTaskSettingsSet -IfTaskFailsReboot $false)
```

### 3. Logging Best Practices

**Every task MUST have structured logging.**

```python
# Python logging template
import logging
from datetime import datetime
from pathlib import Path

log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

handler = logging.FileHandler(
    log_dir / f"task_{datetime.now().strftime('%Y%m%d')}.log"
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Usage
logger.info("Task started")
logger.warning("This might fail")
logger.error("Something went wrong", exc_info=True)
```

**Log Location Standard:**

```
Task Scripts:
  script.py

Logs:
  logs/
    task_20260408.log
    task_20260409.log
    error.log (consolidated)

Retention:
  Keep 30 days (auto-cleanup)
  Archive older logs monthly
```

### 4. Credential Management

**NEVER hardcode credentials. Use these approaches:**

```python
# Option 1: Environment variables (for development)
import os
api_key = os.environ.get('MY_API_KEY')

# Option 2: Google Application Credentials (for BigQuery)
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\path\to\creds.json'
from google.cloud import bigquery
client = bigquery.Client()

# Option 3: Windows Credential Manager (for Windows auth)
# Map network drive with credentials stored in Credential Manager
# Batch script: net use Z: \\server\share /persistent:yes

# Option 4: Service account JSON (OAuth)
# Store in restricted folder: C:\Users\krush\AppData\Roaming\gcloud\
# Reference via env var
```

**Credential File Permissions:**

```powershell
# For JSON credential files, restrict to current user only
$filePath = "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"

# Get current ACL
$acl = Get-Acl $filePath

# Remove inherited permissions
$acl.SetAccessRuleProtection($true, $false)

# Remove all existing rules
$acl.Access | ForEach-Object { $acl.RemoveAccessRule($_) }

# Add permission only for current user
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "$($env:USERDOMAIN)\$($env:USERNAME)",
    "FullControl",
    "Allow"
)
$acl.AddAccessRule($rule)

Set-Acl $filePath $acl

Write-Host "✓ Permissions restricted to current user only"
```

### 5. Retry & Backoff Strategy

**Automatic retry for transient failures.**

```powershell
# Task Scheduler settings
$settings = New-ScheduledTaskSettingsSet `
    -RestartCount 3 `                   # Retry up to 3 times
    -RestartInterval (New-TimeSpan -Minutes 5) `  # After 5 min, then 10, then 15
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)   # Max 1 hour per run

Register-ScheduledTask ... -Settings $settings
```

**For API calls within script:**

```python
import time
import random

def retry_with_backoff(func, max_attempts=3):
    """Retry function with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time:.1f}s")
            time.sleep(wait_time)

# Usage
result = retry_with_backoff(lambda: api.get_data())
```

### 6. Resource Cleanup

**Ensure tasks don't accumulate resources over time.**

```python
# Task cleanup template
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

log_dir = Path("logs")
retention_days = 30

# Cleanup old logs
for log_file in log_dir.glob("task_*.log"):
    file_age = datetime.now() - datetime.fromtimestamp(log_file.stat().st_mtime)
    if file_age > timedelta(days=retention_days):
        log_file.unlink()
        logger.info(f"Deleted old log: {log_file.name}")

# Cleanup temporary files
temp_dir = Path("temp")
for temp_file in temp_dir.glob("*"):
    if temp_file.is_file():
        temp_file.unlink()
```

---

## Service Integration Guide

### Integrating with Existing Services

#### 1. BigQuery Integration

**For Analysis & Data Sync Tasks:**

```python
from google.cloud import bigquery
import os

# Uses GOOGLE_APPLICATION_CREDENTIALS env var
client = bigquery.Client(project='wmt-assetprotection-prod')

# Typically query from polaris-analytics-prod dataset
query = """
SELECT 
    worker_id,
    job_code,
    first_name,
    last_name
FROM polaris-analytics-prod.us_walmart.vw_polaris_current_schedule
WHERE job_code = '30-49-855'
"""

results = client.query(query).result()
for row in results:
    print(f"{row.first_name} {row.last_name} - Job: {row.job_code}")
```

**Environment Setup:**

```batch
REM Set credentials before running
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json
python my_task.py
```

#### 2. Email Integration

**Using Walmart SMTP Relay:**

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_addresses, subject, html_body):
    """Send email via Walmart relay."""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'ActivityHub@walmart.com'
    msg['To'] = ', '.join(to_addresses)
    
    msg.attach(MIMEText(html_body, 'html'))
    
    with smtplib.SMTP('relay.walmart.com', 587) as server:
        server.sendmail('ActivityHub@walmart.com', to_addresses, msg.as_string())

# Usage
send_email(
    ['kendall.rush@walmart.com'],
    'Weekly Report',
    '<h1>Activity Hub Status</h1><p>All systems operational</p>'
)
```

#### 3. API Endpoint Integration

**For Tasks That Call Activity Hub APIs:**

```python
import requests
from requests.auth import HTTPBasicAuth

# Job Codes Lookup API
response = requests.post(
    'http://localhost:8080/api/job-codes/lookup',
    json={
        'job_code': '30-49-855',
        'pay_types': ['H', 'S']
    },
    auth=HTTPBasicAuth('admin', 'password'),
    timeout=30
)

if response.status_code == 200:
    results = response.json()
    print(f"Found {len(results['workers'])} employees")
else:
    raise Exception(f"API error: {response.status_code}")
```

---

## Troubleshooting & Monitoring

### Common Failure Scenarios

#### Scenario 1: Task Runs But Doesn't Do Anything

**Symptoms:**
- Task shows Last Task Result = 0 (success)
- But no output files, emails, or database changes
- Script runs when manually executed

**Diagnosis:**

```powershell
# Check working directory
Get-ScheduledTaskInfo -TaskName "TaskName"
# Note: Working directory in Task Scheduler action defaults to SYSTEM32

# Test script manually with SYSTEM context
# Run as SYSTEM using PsExec64
PsExec64.exe -s cmd /c "python script.py"
```

**Common Causes:**

| Cause | Solution |
|-------|----------|
| Working directory not set | Add `Start in: C:\path\to\script\dir` in action |
| File paths relative | Use absolute paths in script |
| Output written to SYSTEM temp | Use absolute path for logs |
| Environment variables not inherited | Set in script or wrapper, not globally |
| Network paths unavailable to SYSTEM | Use mapped drives (`net use` with credentials) |

#### Scenario 2: Scheduled Task Disappears

**Symptoms:**
- Task registered successfully
- Does not appear in Task Scheduler
- Not in Get-ScheduledTask output

**Root Causes & Fixes:**

| Cause | Symptoms | Fix |
|-------|----------|-----|
| Run with SYSTEM, but user logged out | Task runs at 2 AM, but system locked | Add "Run whether user logged in or not" |
| Registry corruption | Task was there, now gone after reboot | Recreate via PowerShell (don't use UI) |
| Task Scheduler corruption | Multiple tasks disappearing | Restart Task Scheduler service: `Restart-Service Schedule` |
| Permission issue | User can't see but SYSTEM can | Elevated PowerShell required for registration |

**Recovery:**

```powershell
# Restart Task Scheduler service
Stop-Service -Name Schedule -Force
Start-Service -Name Schedule

# Verify service running
Get-Service Schedule

# If still missing, recreate task
# (Use PowerShell script from Phase 3)
```

#### Scenario 3: Task Runs Twice

**Symptoms:**
- Email sent twice
- Database record inserted twice
- Task appears to run multiple times

**Causes:**

| Cause | Symptom | Fix |
|-------|--------|-----|
| Multiple triggers on same task | Check task triggers | Remove duplicate triggers |
| Pattern matching multiple tasks | Task like "PC-*" matches too many | Use full exact name |
| Startup + recurring both enabled | Task inherited startup + daily | Disable startup trigger if not needed |
| Repeat interval too short | Daily task with 12-hour repeat interval | Set interval to 24 hours or higher |

**Fix:**

```powershell
# List all triggers for task
Get-ScheduledTask -TaskName "YourTask" | Select-Object -ExpandProperty Triggers

# Remove task and recreate with single trigger
Unregister-ScheduledTask -TaskName "YourTask" -Confirm:$false

# Recreate with single, correct trigger
# (Use registration script from Phase 3)
```

#### Scenario 4: Memory Leak / Process Hangs

**Symptoms:**
- Memory usage grows over time
- Task appears to hang at 11:59 PM and never completes
- CPU usage stays at 100%

**Diagnosis:**

```powershell
# Monitor process memory
$process = Get-Process python | Sort-Object WorkingSet | Select-Object -Last 1
$memMB = $process.WorkingSet / 1MB
if ($memMB -gt 500) { Write-Warning "High memory: $memMB MB" }

# Check for stuck processes
Get-Process python | Where-Object { $_.StartTime -lt (Get-Date).AddHours(-2) }

# Kill stuck process
Stop-Process -ID $process.Id -Force
```

**Prevention:**

```python
# In your task script
import gc
import resource

# Periodic garbage collection
gc.collect()

# Set memory limit (e.g., 500 MB)
resource.setrlimit(resource.RLIMIT_AS, (500*1024*1024, 500*1024*1024))

# Add this to main loop if processing large datasets
if memory_used > threshold:
    logger.warning("High memory, exiting early")
    sys.exit(0)
```

### Monitoring Dashboard

**Create monitoring script to track all Activity Hub tasks:**

```powershell
function Get-ActivityHubTaskStatus {
    $tasks = Get-ScheduledTask -Path "\Activity_Hub\*" -Recurse
    $report = @()
    
    foreach ($task in $tasks) {
        $info = Get-ScheduledTaskInfo -InputObject $task
        $lastTrigger = $task.Triggers | Select-Object -Last 1
        
        $report += [PSCustomObject]@{
            TaskName = $task.TaskName
            Status = $task.State
            LastResult = if ($info.LastTaskResult -eq 0) { "✓" } else { "✗ ($($info.LastTaskResult))" }
            LastRunTime = $info.LastRunTime
            NextRunTime = $info.NextRunTime
            TriggerType = $lastTrigger.CimClass.CimClassName -replace 'MSFT_', ''
            CpuTime = [math]::Round(($info.RunDuration | Measure-Object -Sum).Sum / 1000, 1)
        }
    }
    
    return $report | Sort-Object -Property NextRunTime
}

# Usage
Get-ActivityHubTaskStatus | Format-Table -AutoSize

# Export to CSV for trending
Get-ActivityHubTaskStatus | Export-Csv "activity_hub_status_$(Get-Date -Format 'yyyyMMdd').csv"
```

---

## Template Repository

### Quick Reference: Copy-Paste Templates

#### Template 1: Minimal Scheduled Task (Python)

```python
#!/usr/bin/env python3
import sys
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Task started")
        # YOUR CODE HERE
        logger.info("Task completed")
        return 0
    except Exception as e:
        logger.error(f"Task failed: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

#### Template 2: Minimal Wrapper (.bat)

```batch
@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python task.py
exit /b %ERRORLEVEL%
```

#### Template 3: Minimal Task Registration (PowerShell)

```powershell
$trigger = New-ScheduledTaskTrigger -At "06:00:00" -Daily
$action = New-ScheduledTaskAction -Execute "C:\path\to\wrapper.bat"
$principal = New-ScheduledTaskPrincipal -UserID "NT AUTHORITY\SYSTEM" -RunLevel Highest
Register-ScheduledTask -TaskName "MyTask" -Trigger $trigger -Action $action -Principal $principal -Force
```

---

## Appendix: Frequently Asked Questions

### Q: Can I run multiple services on the same port?
**A:** No. Each service must have a unique port. See [Service Ports table](#current-service-ports--auto-start-configuration) for allocation.

### Q: How do I debug a task that only fails when scheduled?
**A:** Run with `PsExec64.exe -s` to execute as SYSTEM account: `PsExec64.exe -s python task.py`

### Q: What's the Windows Task Scheduler file location?
**A:** `C:\Windows\System32\Tasks\Activity_Hub\` (one XML file per task)

### Q: Can I schedule a task from a remote server?
**A:** Yes, use `schtasks.exe` or PowerShell remoting, but test locally first.

### Q: How do I prevent a task from running while another is still executing?
**A:** In task settings, set "Multiple Instances" to "IgnoreNew" or "Queue New"

### Q: Can I see the full output of a scheduled task?
**A:** Yes, via Windows Event Viewer: `eventvwr.msc` → Windows Logs → System/Application

---

## Version History

| Date | Author | Changes |
|------|--------|---------|
| Apr 8, 2026 | Kendall Rush | Initial comprehensive guide created |
| | | Documented 4 core services, 31+ existing tasks |
| | | Added troubleshooting section and examples |

---

**Document Classification:** Internal Research Guide  
**Last Reviewed:** April 8, 2026  
**Next Review:** May 8, 2026
