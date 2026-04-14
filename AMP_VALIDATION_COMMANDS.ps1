# AMP AutoFeed Validation Management
# Easy commands for running, checking, and managing the system

# Add these functions to your PowerShell profile or run directly

function Start-AMPValidation {
    <#
    .SYNOPSIS
    Run AMP AutoFeed validation immediately
    
    .EXAMPLE
    Start-AMPValidation
    Start-AMPValidation -SendEmail -Recipient "your.email@walmart.com"
    #>
    param(
        [switch]$SendEmail,
        [string]$Recipient = "Kendall.Rush@walmart.com"
    )
    
    $scriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_orchestrator.py"
    
    if ($SendEmail) {
        Write-Host "Running validation with email report..." -ForegroundColor Cyan
        python $scriptPath daily --send-email --recipient $Recipient
    } else {
        Write-Host "Running validation..." -ForegroundColor Cyan
        python $scriptPath daily
    }
}


function Get-AMPValidationStatus {
    <#
    .SYNOPSIS
    Show recent validation results
    
    .EXAMPLE
    Get-AMPValidationStatus
    #>
    
    $scriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_orchestrator.py"
    
    Write-Host "Getting validation status..." -ForegroundColor Cyan
    python $scriptPath status
}


function Get-AMPScheduledTasks {
    <#
    .SYNOPSIS
    Check if scheduled tasks exist and their status
    
    .EXAMPLE
    Get-AMPScheduledTasks
    #>
    
    Write-Host "`n=== AMP AutoFeed Scheduled Tasks ===" -ForegroundColor Green
    
    $tasks = @(
        "AMP-AutoFeed-DailyValidation",
        "AMP-AutoFeed-WeeklyReport"
    )
    
    foreach ($task in $tasks) {
        $t = Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue
        
        if ($t) {
            $lastRun = $t.LastRunTime
            $lastStatus = $t.LastTaskResult
            
            $statusText = switch ($lastStatus) {
                0 { "✓ Success" }
                1 { "✗ Failed" }
                267009 { "✓ Not yet run" }
                default { "Status: $lastStatus" }
            }
            
            Write-Host "`n$($t.TaskName)" -ForegroundColor Cyan
            Write-Host "  State: $($t.State)" -ForegroundColor Green
            Write-Host "  Last Run: $lastRun"
            Write-Host "  Last Status: $statusText"
        } else {
            Write-Host "`n✗ $task - NOT FOUND" -ForegroundColor Red
        }
    }
    
    Write-Host "`n=== End of Tasks ===" -ForegroundColor Green
}


function Get-AMPAnalyzeEmails {
    <#
    .SYNOPSIS
    Analyze today's emails to see what data is being compared
    
    .EXAMPLE
    Get-AMPAnalyzeEmails
    #>
    
    $scriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\analyze_amp_emails.py"
    
    Write-Host "Analyzing today's emails..." -ForegroundColor Cyan
    python $scriptPath
}


function Open-AMPValidationLogs {
    <#
    .SYNOPSIS
    Open the validation logs folder
    
    .EXAMPLE
    Open-AMPValidationLogs
    #>
    
    $logDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_validation_logs"
    
    if (Test-Path $logDir) {
        explorer $logDir
        Write-Host "Opened: $logDir" -ForegroundColor Green
    } else {
        Write-Host "✗ Logs directory not found: $logDir" -ForegroundColor Red
    }
}


function Get-AMPHistoricalReport {
    <#
    .SYNOPSIS
    Generate historical analysis report
    
    .PARAMETER Days
    Number of days to analyze (default: 90)
    
    .EXAMPLE
    Get-AMPHistoricalReport
    Get-AMPHistoricalReport -Days 30
    #>
    param(
        [int]$Days = 90
    )
    
    $scriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_orchestrator.py"
    
    Write-Host "Generating historical report for last $Days days..." -ForegroundColor Cyan
    python $scriptPath historical --days $Days
}


function Get-AMPCSVReports {
    <#
    .SYNOPSIS
    Generate comprehensive CSV reports for analysis and sharing
    
    .PARAMETER Days
    Number of days to analyze (default: 90)
    
    .EXAMPLE
    Get-AMPCSVReports                # Generate for last 90 days
    Get-AMPCSVReports -Days 30       # Generate for last 30 days
    Get-AMPCSVReports -Days 365      # Generate for last year
    #>
    param(
        [int]$Days = 90
    )
    
    $scriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_orchestrator.py"
    
    Write-Host "Generating CSV reports for last $Days days..." -ForegroundColor Cyan
    python $scriptPath csv-report --days $Days
    
    Write-Host "`nCSV Reports created:" -ForegroundColor Green
    Write-Host "  - daily_summary_*.csv (for daily review)" -ForegroundColor Cyan
    Write-Host "  - discrepancies_*.csv (issues found)" -ForegroundColor Cyan
    Write-Host "  - records_comparison_*.csv (field-by-field)" -ForegroundColor Cyan
    Write-Host "  - trend_statistics_*.csv (metrics)" -ForegroundColor Cyan
    Write-Host "`nLocation: amp_validation_logs\csv_reports\" -ForegroundColor Yellow
}


function Show-AMPLatestReport {
    <#
    .SYNOPSIS
    Show today's validation report
    
    .EXAMPLE
    Show-AMPLatestReport
    #>
    
    $logDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_validation_logs"
    $today = Get-Date -Format "yyyy-MM-dd"
    $reportFile = (Join-Path $logDir "daily_reports") + "\validation_$today.json"
    
    if (Test-Path $reportFile) {
        $report = Get-Content $reportFile | ConvertFrom-Json
        
        Write-Host "`n=== AMP Validation Report - $today ===" -ForegroundColor Green
        Write-Host "Status: $($report.status)" -ForegroundColor $(
            switch ($report.status) {
                "PASS" { "Green" }
                "FAIL" { "Red" }
                default { "Yellow" }
            }
        )
        
        Write-Host "QuickBase Email Found: $($report.qb_email_found)"
        Write-Host "AMP Email Found: $($report.amp_email_found)"
        
        if ($report.comparison.differences) {
            Write-Host "`nDifferences:" -ForegroundColor Yellow
            foreach ($diff in $report.comparison.differences) {
                Write-Host "  - $diff"
            }
        } else {
            Write-Host "`n✓ No differences detected" -ForegroundColor Green
        }
        
        Write-Host "`nFull report: $reportFile"
    } else {
        Write-Host "✗ No report found for today" -ForegroundColor Yellow
        Write-Host "Run: Start-AMPValidation" -ForegroundColor Cyan
    }
}


function Set-AMPEmailConfig {
    <#
    .SYNOPSIS
    Configure email settings for automated reports
    
    .PARAMETER SmtpServer
    SMTP server (e.g., smtp.gmail.com)
    
    .PARAMETER SenderEmail
    Email address to send from
    
    .EXAMPLE
    Set-AMPEmailConfig -SmtpServer "smtp.gmail.com" -SenderEmail "your.email@gmail.com"
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$SmtpServer,
        
        [Parameter(Mandatory=$true)]
        [string]$SenderEmail
    )
    
    Write-Host "Setting email configuration..." -ForegroundColor Cyan
    Write-Host "SMTP Server: $SmtpServer"
    Write-Host "Sender: $SenderEmail"
    
    $scriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_orchestrator.py"
    
    python $scriptPath configure-email --smtp $SmtpServer --email $SenderEmail
}


# Display available commands
Write-Host @"

╔════════════════════════════════════════════════════════════════════════╗
║       AMP AutoFeed Validation Management Functions                    ║
╚════════════════════════════════════════════════════════════════════════╝

DAILY OPERATIONS:
  Start-AMPValidation              Run validation immediately
  Start-AMPValidation -SendEmail   Run and send email report
  Get-AMPValidationStatus          Show recent validation results
  Show-AMPLatestReport             Display today's report

ANALYSIS & DEBUGGING:
  Get-AMPAnalyzeEmails             Analyze what's in today's emails
  Get-AMPHistoricalReport          Generate trend analysis
  Get-AMPHistoricalReport -Days 30 Analyze last 30 days
  Get-AMPCSVReports                Generate CSV reports (4 files)
  Get-AMPCSVReports -Days 30       CSV reports for last 30 days

SYSTEM MANAGEMENT:
  Get-AMPScheduledTasks            Check scheduled task status
  Set-AMPEmailConfig               Configure email settings
  Open-AMPValidationLogs           Open logs folder

EXAMPLES:
  PS> Start-AMPValidation                    # Run now
  PS> Start-AMPValidation -SendEmail         # Run with email report
  PS> Get-AMPValidationStatus                # See results
  PS> Get-AMPHistoricalReport -Days 90       # Analyze 3 months
  PS> Get-AMPCSVReports -Days 30             # Generate CSV for last month
  PS> Get-AMPAnalyzeEmails                   # Debug today's emails
  PS> Open-AMPValidationLogs                 # View all logs

"@

