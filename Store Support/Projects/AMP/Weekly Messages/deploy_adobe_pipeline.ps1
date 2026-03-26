# Adobe Analytics to BigQuery Loader - Deployment Script
# Path: Store Support\Projects\AMP\Weekly Messages\deploy_adobe_pipeline.ps1
#
# Purpose: Bootstrap environment, install dependencies, run loader with validation
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File deploy_adobe_pipeline.ps1

param(
    [switch]$SkipValidation = $false,
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"
$WarningPreference = "Continue"

# ============================================================================
# SETUP
# ============================================================================

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Project = Split-Path -Leaf $ScriptDir
$LogDir = Join-Path $ScriptDir "logs"
$VenvPath = Join-Path $ScriptDir "venv"
$ScriptName = "adobe_to_bigquery_loader.py"
$ConfigName = "adobe_config.yaml"

Write-Host "`n" + ("=" * 80) -ForegroundColor Cyan
Write-Host " Adobe Analytics to BigQuery Loader - DEPLOYMENT" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host " Start Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray

# ============================================================================
# PHASE 0: SETUP BIGQUERY TABLES (if not exists)
# ============================================================================

Write-Host "`n[PHASE 0] Checking BigQuery tables..." -ForegroundColor Cyan

try {
    Write-Host "  Running setup_bigquery_tables.py..." -ForegroundColor Gray
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Skipping BigQuery table creation" -ForegroundColor Cyan
    }
    else {
        Push-Location $ScriptDir
        python setup_bigquery_tables.py
        $ExitCode = $LASTEXITCODE
        Pop-Location
        
        if ($ExitCode -ne 0) {
            throw "BigQuery setup failed with exit code: $ExitCode"
        }
    }
    
    Write-Host "  ✓ BigQuery tables ready" -ForegroundColor Green
}
catch {
    Write-Host "  ERROR: $_" -ForegroundColor Red
    exit 1
}

# ============================================================================
# PHASE 1: PYTHON ENVIRONMENT SETUP
# ============================================================================

Write-Host "`n[PHASE 1] Setting up Python environment..." -ForegroundColor Yellow

try {
    # Check if venv exists
    if (-not (Test-Path $VenvPath)) {
        Write-Host "  Creating virtual environment..." -ForegroundColor Gray
        python -m venv $VenvPath
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create Python virtual environment"
        }
    }
    
    # Activate venv
    $ActivateScript = Join-Path $VenvPath "Scripts" "Activate.ps1"
    & $ActivateScript
    
    # Install dependencies
    Write-Host "  Installing Python dependencies..." -ForegroundColor Gray
    $Dependencies = @(
        "pandas",
        "openpyxl",
        "google-cloud-bigquery",
        "pyyaml",
        "python-dateutil"
    )
    
    foreach ($dep in $Dependencies) {
        Write-Host "    - $dep" -ForegroundColor Gray
        pip install $dep -q
        if ($LASTEXITCODE -ne 0) {
            Write-Host "    ERROR installing $dep" -ForegroundColor Red
            throw "Failed to install $dep"
        }
    }
    
    Write-Host "  ✓ Python environment ready" -ForegroundColor Green
}
catch {
    Write-Host "  ERROR: $_" -ForegroundColor Red
    exit 1
}

# ============================================================================
# PHASE 2: GCP AUTHENTICATION CHECK
# ============================================================================

Write-Host "`n[PHASE 2] Checking GCP authentication..." -ForegroundColor Yellow

try {
    # Check gcloud auth
    Write-Host "  Checking gcloud authentication..." -ForegroundColor Gray
    gcloud auth list 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "gcloud not found or not authenticated"
    }
    
    # Check application-default credentials
    Write-Host "  Checking application-default credentials..." -ForegroundColor Gray
    $CredsPath = "$env:APPDATA\gcloud\application_default_credentials.json"
    if (-not (Test-Path $CredsPath)) {
        throw "Application-default credentials not found. Run: gcloud auth application-default login"
    }
    
    Write-Host "  ✓ GCP authentication verified" -ForegroundColor Green
}
catch {
    Write-Host "  ERROR: $_" -ForegroundColor Red
    Write-Host "`n  SETUP REQUIRED:" -ForegroundColor Yellow
    Write-Host "    1. Run: gcloud auth application-default login" -ForegroundColor Yellow
    Write-Host "    2. Follow the browser login flow" -ForegroundColor Yellow
    Write-Host "    3. Return and run this script again" -ForegroundColor Yellow
    exit 1
}

# ============================================================================
# PHASE 3: RUN LOADER SCRIPT
# ============================================================================

Write-Host "`n[PHASE 3] Running Adobe Analytics loader..." -ForegroundColor Yellow

try {
    $LoaderPath = Join-Path $ScriptDir $ScriptName
    
    if (-not (Test-Path $LoaderPath)) {
        throw "Loader script not found: $LoaderPath"
    }
    
    Write-Host "  Executing: python $ScriptName" -ForegroundColor Gray
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Skipping actual execution" -ForegroundColor Cyan
    }
    else {
        # Run loader with explicit credentials
        $env:GOOGLE_APPLICATION_CREDENTIALS = $CredsPath
        
        # Change to script directory and run
        Push-Location $ScriptDir
        python $ScriptName
        $ExitCode = $LASTEXITCODE
        Pop-Location
        
        if ($ExitCode -ne 0) {
            throw "Loader script failed with exit code: $ExitCode"
        }
    }
    
    Write-Host "  ✓ Loader execution completed" -ForegroundColor Green
}
catch {
    Write-Host "  ERROR: $_" -ForegroundColor Red
    exit 1
}

# ============================================================================
# PHASE 4: VALIDATION (Optional)
# ============================================================================

if (-not $SkipValidation) {
    Write-Host "`n[PHASE 4] Validating BigQuery load..." -ForegroundColor Yellow
    
    try {
        Write-Host "  Querying row counts..." -ForegroundColor Gray
        
        $ProjectId = "wmt-assetprotection-prod"
        
        # Query 1: Weekly Messages Devices
        $Query1 = @"
SELECT COUNT(*) as device_count 
FROM \`$ProjectId.Weekly_Message_FY27.bq_weekly_messages_devices\` 
WHERE DATE(extracted_date) = CURRENT_DATE()
"@
        
        # Query 2: Weekly Messages Metrics
        $Query2 = @"
SELECT COUNT(*) as metrics_count 
FROM \`$ProjectId.Weekly_Message_FY27.bq_weekly_messages_metrics\` 
WHERE DATE(extracted_date) = CURRENT_DATE()
"@
        
        # Query 3: Playbook Hub
        $Query3 = @"
SELECT COUNT(*) as playbook_count 
FROM \`$ProjectId.Playbook_Hub_Data.bq_playbook_hub_metrics\` 
WHERE DATE(extracted_date) = CURRENT_DATE()
"@
        
        if (-not $DryRun) {
            $Result1 = python -c "
from google.cloud import bigquery
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'$CredsPath'
client = bigquery.Client(project='$ProjectId')
result = client.query('$Query1').result()
for row in result:
    print(row.device_count)
"
            
            $Result2 = python -c "
from google.cloud import bigquery
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'$CredsPath'
client = bigquery.Client(project='$ProjectId')
result = client.query('$Query2').result()
for row in result:
    print(row.metrics_count)
"
            
            $Result3 = python -c "
from google.cloud import bigquery
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'$CredsPath'
client = bigquery.Client(project='$ProjectId')
result = client.query('$Query3').result()
for row in result:
    print(row.playbook_count)
"
            
            Write-Host "    Weekly Messages Devices: $Result1 rows" -ForegroundColor Cyan
            Write-Host "    Weekly Messages Metrics: $Result2 rows" -ForegroundColor Cyan
            Write-Host "    Playbook Hub: $Result3 rows" -ForegroundColor Cyan
        }
        else {
            Write-Host "    [DRY RUN] Skipping BigQuery validation" -ForegroundColor Cyan
        }
        
        Write-Host "  ✓ Validation completed" -ForegroundColor Green
    }
    catch {
        Write-Host "  WARNING: Validation failed: $_" -ForegroundColor Yellow
        # Don't fail deployment on validation errors
    }
}

# ============================================================================
# CLEANUP & SUMMARY
# ============================================================================

Write-Host "`n[PHASE 5] Cleanup..." -ForegroundColor Yellow

try {
    # Deactivate venv (optional)
    deactivate 2>&1 | Out-Null
    
    Write-Host "  ✓ Cleanup completed" -ForegroundColor Green
}
catch {
    # Deactivate may not always work, that's OK
}

Write-Host "`n" + ("=" * 80) -ForegroundColor Cyan
Write-Host " Adobe Analytics to BigQuery Loader - SUCCESS" -ForegroundColor Green
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host " End Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host " Log File: $(Join-Path $LogDir 'adobe_loader.log')" -ForegroundColor Gray
Write-Host ""

exit 0
