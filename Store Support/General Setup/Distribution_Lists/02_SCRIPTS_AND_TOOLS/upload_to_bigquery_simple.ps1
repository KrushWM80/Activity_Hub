# Daily DL Update to BigQuery (using gcloud CLI)
# Run this after extract_all_dls_optimized.py completes

param(
    [string]$ProjectId = "wmt-assetprotection-prod",
    [string]$Dataset = "Store_Support_Dev",
    [string]$Table = "dl_catalog"
)

$ErrorActionPreference = "Stop"
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$logPath = Join-Path $scriptPath "logs"
$logFile = Join-Path $logPath "bigquery_upload_$(Get-Date -Format 'yyyyMMdd').log"

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
Write-Log "Starting BigQuery Upload"
Write-Log "=========================================="

# Find latest CSV file
$csvPattern = Join-Path $scriptPath "all_distribution_lists_*.csv"
$latestCsv = Get-ChildItem $csvPattern -ErrorAction SilentlyContinue | 
             Sort-Object LastWriteTime -Descending | 
             Select-Object -First 1

if (!$latestCsv) {
    Write-Log "ERROR: No CSV file found matching: $csvPattern"
    exit 1
}

Write-Log "Found CSV file: $($latestCsv.Name)"
Write-Log "File size: $([math]::Round($latestCsv.Length / 1MB, 2)) MB"

# Copy to standard name
$standardCsv = Join-Path $scriptPath "all_distribution_lists.csv"
Copy-Item $latestCsv.FullName $standardCsv -Force
Write-Log "Copied to: all_distribution_lists.csv"

# Check if gcloud is installed
try {
    $gcloudVersion = & gcloud --version 2>&1
    Write-Log "gcloud CLI detected"
} catch {
    Write-Log "ERROR: gcloud CLI not found"
    Write-Log "Please install from: https://cloud.google.com/sdk/docs/install"
    Write-Log ""
    Write-Log "Alternative: Upload manually via BigQuery Console"
    Write-Log "  1. Go to BigQuery Console"
    Write-Log "  2. Select dataset: $Dataset"
    Write-Log "  3. Click 'Create Table' -> Upload"
    Write-Log "  4. Select file: $standardCsv"
    exit 1
}

# Upload to BigQuery
Write-Log "Uploading to BigQuery..."
Write-Log "Project: $ProjectId"
Write-Log "Dataset: $Dataset"
Write-Log "Table: $Table"

$tableRef = "$Dataset.$Table"

try {
    # Upload with bq command
    $bqOutput = & bq load `
        --project_id=$ProjectId `
        --replace `
        --skip_leading_rows=1 `
        --source_format=CSV `
        --autodetect `
        $tableRef `
        $standardCsv 2>&1
    
    Write-Log "BigQuery output:"
    $bqOutput | ForEach-Object { Write-Log "  $_" }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Log "SUCCESS: Data uploaded to BigQuery"
        
        # Get table info
        $tableInfo = & bq show --format=json $ProjectId`:$tableRef 2>&1 | ConvertFrom-Json
        $numRows = $tableInfo.numRows
        $numBytes = [math]::Round($tableInfo.numBytes / 1MB, 2)
        
        Write-Log "Table statistics:"
        Write-Log "  Rows: $($numRows)"
        Write-Log "  Size: $numBytes MB"
        Write-Log "  Last modified: $($tableInfo.lastModifiedTime)"
    } else {
        Write-Log "ERROR: Upload failed with exit code $LASTEXITCODE"
        exit 1
    }
    
} catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    exit 1
}

Write-Log "=========================================="
Write-Log "BigQuery Upload Completed Successfully"
Write-Log "=========================================="
