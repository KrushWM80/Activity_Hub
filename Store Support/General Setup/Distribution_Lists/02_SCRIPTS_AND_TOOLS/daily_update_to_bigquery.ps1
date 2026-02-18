# Complete Daily Update Script
# Extracts all DLs from AD, uploads to BigQuery automatically
# Schedule this to run daily at 5:00 AM

$ErrorActionPreference = "Stop"
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$logPath = Join-Path $scriptPath "logs"
$logFile = Join-Path $logPath "daily_update_$(Get-Date -Format 'yyyyMMdd').log"

# Create logs directory
if (!(Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath | Out-Null
}

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage
    Add-Content -Path $logFile -Value $logMessage
}

Write-Log "=========================================="
Write-Log "Starting Daily DL Update Process"
Write-Log "=========================================="

# Step 1: Extract all distribution lists from Active Directory
Write-Log "Step 1: Extracting distribution lists from Active Directory..."
try {
    $pythonExe = "C:/Users/krush/AppData/Local/Programs/Python/Python314/python.exe"
    $extractScript = Join-Path $scriptPath "extract_all_dls_optimized.py"
    
    $extractOutput = & $pythonExe $extractScript 2>&1
    Write-Log $extractOutput
    Write-Log "✓ DL extraction completed successfully"
} catch {
    Write-Log "ERROR: DL extraction failed - $($_.Exception.Message)"
    exit 1
}

# Step 2: Find the latest CSV file
Write-Log "Step 2: Locating extracted CSV file..."
$csvPattern = Join-Path $scriptPath "all_distribution_lists_*.csv"
$latestCsv = Get-ChildItem $csvPattern -ErrorAction SilentlyContinue | 
             Sort-Object LastWriteTime -Descending | 
             Select-Object -First 1

if (!$latestCsv) {
    Write-Log "ERROR: No CSV file found after extraction"
    exit 1
}

Write-Log "✓ Found CSV: $($latestCsv.Name) ($([math]::Round($latestCsv.Length / 1MB, 2)) MB)"

# Copy to standard name for upload
$standardCsv = Join-Path $scriptPath "all_distribution_lists.csv"
Copy-Item $latestCsv.FullName $standardCsv -Force
Write-Log "✓ Copied to standard name: all_distribution_lists.csv"

# Step 3: Upload to BigQuery
Write-Log "Step 3: Uploading to BigQuery..."
try {
    $uploadScript = Join-Path $scriptPath "upload_to_bigquery_simple.ps1"
    
    & $uploadScript -ProjectId "wmt-assetprotection-prod" `
                    -Dataset "Store_Support_Dev" `
                    -Table "dl_catalog"
    
    Write-Log "✓ BigQuery upload completed successfully"
} catch {
    Write-Log "ERROR: BigQuery upload failed - $($_.Exception.Message)"
    exit 1
}

# Step 4: Cleanup old files (keep last 7 days)
Write-Log "Step 4: Cleaning up old files..."
try {
    $cutoffDate = (Get-Date).AddDays(-7)
    $oldFiles = Get-ChildItem (Join-Path $scriptPath "all_distribution_lists_*.csv") | 
                Where-Object { $_.LastWriteTime -lt $cutoffDate }
    
    foreach ($file in $oldFiles) {
        Remove-Item $file.FullName -Force
        Write-Log "  Deleted old file: $($file.Name)"
    }
    
    if ($oldFiles.Count -eq 0) {
        Write-Log "  No old files to delete"
    } else {
        Write-Log "✓ Cleaned up $($oldFiles.Count) old file(s)"
    }
} catch {
    Write-Log "WARNING: Cleanup failed - $($_.Exception.Message)"
    # Don't exit on cleanup failure
}

Write-Log "=========================================="
Write-Log "Daily Update Process Completed Successfully"
Write-Log "=========================================="
Write-Log ""

exit 0
