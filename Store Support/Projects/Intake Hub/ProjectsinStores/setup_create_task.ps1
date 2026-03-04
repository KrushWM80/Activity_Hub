################################################################################
# Create Windows Task Scheduler Job - Projects in Stores 24/7 Server
# 
# PURPOSE:
#   Register the backend server to run automatically on system startup
#   with automatic restart on crashes
#
# REQUIREMENTS:
#   - Must run as Administrator (this script will check and exit if not)
#   - Windows Task Scheduler must be available
#
# USAGE:
#   Right-click this file → "Run with PowerShell" or
#   Open PowerShell as Administrator, then: .\setup_create_task.ps1
#
# WHAT THIS DOES:
#   1. Checks for Administrator privileges
#   2. Removes any existing task with same name
#   3. Creates new scheduled task with properties:
#      - Trigger: System startup
#      - Action: Run start_server_24_7.bat
#      - Run with highest privileges
#      - Auto-restart on failure
################################################################################

# Color codes for output
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Cyan"

Write-Host "`n================================" -ForegroundColor $InfoColor
Write-Host "  Projects in Stores 24/7 Setup" -ForegroundColor $InfoColor
Write-Host "================================`n" -ForegroundColor $InfoColor

# ============================================================================
# STEP 1: Check for Administrator Privileges
# ============================================================================

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "❌ ERROR: This script requires Administrator privileges!" -ForegroundColor $ErrorColor
    Write-Host "`nTo run as Administrator:" -ForegroundColor $InfoColor
    Write-Host "  1. Right-click this script file (.ps1)"
    Write-Host "  2. Select 'Run with PowerShell'"
    Write-Host "  3. Click 'Yes' when prompted"
    Write-Host "`nAlternatively, open PowerShell as Administrator first, then run this script.`n"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Running with Administrator privileges`n" -ForegroundColor $SuccessColor

# ============================================================================
# STEP 2: Define Task Parameters
# ============================================================================

$TaskName = "Projects in Stores Server 24/7"
$TaskPath = "\Activity Hub\"
$FullTaskName = "$TaskPath$TaskName"
$ScriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\start_server_24_7.bat"
$WorkingDirectory = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

Write-Host "Task Configuration:" -ForegroundColor $InfoColor
Write-Host "  Task Name: $TaskName"
Write-Host "  Task Path: $TaskPath"
Write-Host "  Script: $ScriptPath"
Write-Host ""

# ============================================================================
# STEP 3: Remove Existing Task (if present)
# ============================================================================

Write-Host "Checking for existing task..." -ForegroundColor $InfoColor

$existingTask = Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskPath -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Found existing task. Removing..." -ForegroundColor $InfoColor
    try {
        Unregister-ScheduledTask -TaskName $TaskName -TaskPath $TaskPath -Confirm:$false -ErrorAction Stop
        Write-Host "✅ Existing task removed`n" -ForegroundColor $SuccessColor
    } catch {
        Write-Host "⚠️  Warning: Could not remove existing task: $_" -ForegroundColor "Yellow"
        Write-Host "Attempting to continue...`n" -ForegroundColor "Yellow"
    }
} else {
    Write-Host "No existing task found. Proceeding with creation...`n" -ForegroundColor $InfoColor
}

# ============================================================================
# STEP 4: Create New Scheduled Task
# ============================================================================

Write-Host "Creating scheduled task..." -ForegroundColor $InfoColor

try {
    # Create trigger (At Startup)
    $trigger = New-ScheduledTaskTrigger -AtStartup -ErrorAction Stop
    
    # Create action (Run the batch file)
    $action = New-ScheduledTaskAction `
        -Execute "cmd.exe" `
        -Argument "/c `"$ScriptPath`"" `
        -WorkingDirectory $WorkingDirectory `
        -ErrorAction Stop
    
    # Create settings with reliability options
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable:$false `
        -Compatibility Win8 `
        -ErrorAction Stop
    
    # Create principal (run with highest privileges)
    $principal = New-ScheduledTaskPrincipal `
        -UserId "SYSTEM" `
        -LogonType ServiceAccount `
        -RunLevel Highest `
        -ErrorAction Stop
    
    # Register the task
    $task = Register-ScheduledTask `
        -TaskName $TaskName `
        -TaskPath $TaskPath `
        -Trigger $trigger `
        -Action $action `
        -Settings $settings `
        -Principal $principal `
        -Force `
        -ErrorAction Stop
    
    Write-Host "✅ Task created successfully!`n" -ForegroundColor $SuccessColor
    
} catch {
    Write-Host "❌ ERROR creating task: $_`n" -ForegroundColor $ErrorColor
    Read-Host "Press Enter to exit"
    exit 1
}

# ============================================================================
# STEP 5: Verify Task Was Created
# ============================================================================

Write-Host "Verifying task..." -ForegroundColor $InfoColor

$verifyTask = Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskPath -ErrorAction SilentlyContinue

if ($verifyTask) {
    Write-Host "✅ Task verification SUCCESSFUL`n" -ForegroundColor $SuccessColor
    Write-Host "Task Details:" -ForegroundColor $InfoColor
    Write-Host "  Name:      $($verifyTask.TaskName)"
    Write-Host "  Path:      $($verifyTask.TaskPath)"
    Write-Host "  State:     $($verifyTask.State)"
    Write-Host "  Enabled:   $($verifyTask.Settings.Enabled)"
    Write-Host ""
} else {
    Write-Host "⚠️  Could not verify task. It may not have been created.`n" -ForegroundColor "Yellow"
}

# ============================================================================
# STEP 6: Test Task (Optional)
# ============================================================================

Write-Host "Next Steps:" -ForegroundColor $InfoColor
Write-Host "  1. Restart your computer to verify auto-start works"
Write-Host "  2. Check status with: .\check_status.ps1"
Write-Host "  3. Server will be running at: http://localhost:8001"
Write-Host "`n"

Write-Host "To verify the task now, run:" -ForegroundColor $InfoColor
Write-Host "  .\check_status.ps1`n"

Write-Host "================================" -ForegroundColor $InfoColor
Write-Host "Setup Complete!" -ForegroundColor $InfoColor
Write-Host "================================`n" -ForegroundColor $InfoColor

Read-Host "Press Enter to exit"
