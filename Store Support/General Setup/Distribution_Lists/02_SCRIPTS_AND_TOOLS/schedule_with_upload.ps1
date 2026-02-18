# Enhanced Daily DL Update with Code Puppy Pages Upload
# Extracts DLs at 5 AM and uploads to Code Puppy Pages automatically

Write-Host "================================================================================"
Write-Host "Setting Up Daily DL Update with Code Puppy Upload"
Write-Host "================================================================================"
Write-Host ""

# Configuration
$scriptPath = $PSScriptRoot
$pythonScript = Join-Path $scriptPath "extract_all_dls_optimized.py"
$codePuppyUrl = "YOUR_CODE_PUPPY_API_ENDPOINT_HERE"  # Update with actual Code Puppy API
$logPath = Join-Path $scriptPath "logs"

# Create logs directory if it doesn't exist
if (!(Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath | Out-Null
}

# Task configuration
$taskName = "DL_Catalog_Daily_Update_With_Upload"
$taskDescription = "Extracts all distribution lists daily at 5:00 AM and uploads to Code Puppy Pages"

# Create the PowerShell script that will run daily
$dailyScriptContent = @"
# Daily DL Extraction and Upload Script
`$ErrorActionPreference = 'Continue'
`$logFile = "$logPath\dl_update_`$(Get-Date -Format 'yyyyMMdd').log"

function Write-Log {
    param([string]`$Message)
    `$timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    `$logMessage = "[`$timestamp] `$Message"
    Write-Host `$logMessage
    Add-Content -Path `$logFile -Value `$logMessage
}

Write-Log "=========================================="
Write-Log "Starting Daily DL Update Process"
Write-Log "=========================================="

# Step 1: Extract DLs from Active Directory
Write-Log "Step 1: Extracting distribution lists from AD..."
try {
    Set-Location '$scriptPath'
    `$pythonExe = 'python'
    `$extractOutput = & `$pythonExe '$pythonScript' 2>&1
    Write-Log "Extraction completed successfully"
    Write-Log `$extractOutput
} catch {
    Write-Log "ERROR: Extraction failed - `$(`$_.Exception.Message)"
    exit 1
}

# Step 2: Find the latest CSV file
Write-Log "Step 2: Locating latest CSV file..."
`$csvPattern = Join-Path '$scriptPath' 'all_distribution_lists_*.csv'
`$latestCsv = Get-ChildItem `$csvPattern | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (`$latestCsv) {
    Write-Log "Found latest CSV: `$(`$latestCsv.Name)"
    Write-Log "File size: `$([math]::Round(`$latestCsv.Length / 1MB, 2)) MB"
    Write-Log "Record count: `$(( Get-Content `$latestCsv.FullName | Measure-Object -Line ).Lines)"
    
    # Copy to standard name for Code Puppy
    `$standardCsv = Join-Path '$scriptPath' 'all_distribution_lists.csv'
    Copy-Item `$latestCsv.FullName `$standardCsv -Force
    Write-Log "Copied to standard filename: all_distribution_lists.csv"
} else {
    Write-Log "ERROR: No CSV file found after extraction"
    exit 1
}

# Step 3: Upload to Code Puppy Pages
Write-Log "Step 3: Uploading to Code Puppy Pages..."

# METHOD A: If Code Puppy has API endpoint
# Uncomment and configure if Code Puppy provides an API:
# try {
#     `$uploadUrl = '$codePuppyUrl'
#     `$headers = @{
#         'Authorization' = 'Bearer YOUR_TOKEN_HERE'
#         'Content-Type' = 'multipart/form-data'
#     }
#     `$response = Invoke-RestMethod -Uri `$uploadUrl -Method Post -Headers `$headers -InFile `$standardCsv
#     Write-Log "Upload successful via API"
# } catch {
#     Write-Log "ERROR: Upload failed - `$(`$_.Exception.Message)"
# }

# METHOD B: If Code Puppy uses file share/network location
# Uncomment and configure if Code Puppy uses a network share:
# try {
#     `$codePuppyPath = '\\codepuppy-server\shared\dl-selector\all_distribution_lists.csv'
#     Copy-Item `$standardCsv `$codePuppyPath -Force
#     Write-Log "Upload successful via network share"
# } catch {
#     Write-Log "ERROR: Upload failed - `$(`$_.Exception.Message)"
# }

# METHOD C: Manual notification (default until you configure A or B)
Write-Log "NOTICE: Automatic upload not configured"
Write-Log "Please manually upload: `$standardCsv"
Write-Log "To Code Puppy Pages application"

# Step 4: Cleanup old CSV files (keep last 7 days)
Write-Log "Step 4: Cleaning up old CSV files..."
`$cutoffDate = (Get-Date).AddDays(-7)
Get-ChildItem `$csvPattern | Where-Object { `$_.LastWriteTime -lt `$cutoffDate } | ForEach-Object {
    Write-Log "Deleting old file: `$(`$_.Name)"
    Remove-Item `$_.FullName -Force
}

# Step 5: Cleanup old log files (keep last 30 days)
Write-Log "Step 5: Cleaning up old log files..."
`$logCutoff = (Get-Date).AddDays(-30)
Get-ChildItem '$logPath\dl_update_*.log' | Where-Object { `$_.LastWriteTime -lt `$logCutoff } | ForEach-Object {
    Write-Log "Deleting old log: `$(`$_.Name)"
    Remove-Item `$_.FullName -Force
}

Write-Log "=========================================="
Write-Log "Daily DL Update Process Completed"
Write-Log "=========================================="
"@

# Save the daily script
$dailyScriptPath = Join-Path $scriptPath "daily_dl_update.ps1"
$dailyScriptContent | Out-File -FilePath $dailyScriptPath -Encoding UTF8 -Force
Write-Host "✓ Created daily update script: daily_dl_update.ps1" -ForegroundColor Green

# Create the scheduled task
Write-Host ""
Write-Host "Creating Windows Scheduled Task..." -ForegroundColor Cyan

$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$dailyScriptPath`""
$trigger = New-ScheduledTaskTrigger -Daily -At "05:00AM"
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    # Remove existing task if present
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    
    # Register new task
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description $taskDescription | Out-Null
    
    Write-Host "✓ Scheduled task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Yellow
    Write-Host "  Name: $taskName"
    Write-Host "  Schedule: Daily at 5:00 AM"
    Write-Host "  Script: $dailyScriptPath"
    Write-Host "  Logs: $logPath"
    
} catch {
    Write-Host "✗ Failed to create scheduled task: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "You may need to run this script as Administrator" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "================================================================================"
Write-Host "IMPORTANT: Configure Code Puppy Upload Method"
Write-Host "================================================================================"
Write-Host ""
Write-Host "The scheduled task is created, but automatic upload is NOT configured yet." -ForegroundColor Yellow
Write-Host ""
Write-Host "To enable automatic upload to Code Puppy Pages, edit:" -ForegroundColor Cyan
Write-Host "  $dailyScriptPath" -ForegroundColor White
Write-Host ""
Write-Host "Choose ONE of these methods:" -ForegroundColor Cyan
Write-Host ""
Write-Host "METHOD A: API Upload (if Code Puppy has API)" -ForegroundColor Green
Write-Host "  - Uncomment the API section in daily_dl_update.ps1"
Write-Host "  - Add your Code Puppy API endpoint and authentication token"
Write-Host ""
Write-Host "METHOD B: Network Share (if Code Puppy uses file share)" -ForegroundColor Green
Write-Host "  - Uncomment the network share section"
Write-Host "  - Update the path to your Code Puppy file location"
Write-Host ""
Write-Host "METHOD C: Manual Upload (current default)" -ForegroundColor Yellow
Write-Host "  - Task extracts CSV at 5 AM"
Write-Host "  - You manually upload to Code Puppy Pages when convenient"
Write-Host ""
Write-Host "================================================================================"
Write-Host "Next Steps:"
Write-Host "================================================================================"
Write-Host "1. Test the extraction manually:" -ForegroundColor Cyan
Write-Host "   .\daily_dl_update.ps1" -ForegroundColor White
Write-Host ""
Write-Host "2. Check the log file:" -ForegroundColor Cyan
Write-Host "   Get-Content '$logPath\dl_update_`$(Get-Date -Format 'yyyyMMdd').log'" -ForegroundColor White
Write-Host ""
Write-Host "3. Test the scheduled task:" -ForegroundColor Cyan
Write-Host "   Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
Write-Host ""
Write-Host "4. Configure Code Puppy upload method (see above)" -ForegroundColor Cyan
Write-Host ""
Write-Host "================================================================================"
