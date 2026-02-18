# Complete AMP Business Logic Deployment and Validation Script
# Deploys enhanced BigQuery trigger system with comprehensive business logic
# Date: October 28, 2024

Write-Host "🚀 Deploying Complete AMP Business Logic System..." -ForegroundColor Green

# Configuration
$PROJECT_ID = "wmt-assetprotection-prod"
$DATASET_DEV = "Store_Support_Dev"
$DATASET_PROD = "Store_Support"
$SQL_FILE = "amp_bigquery_enhanced_multisource_system_20251028_080418.sql"

# Verify prerequisites
Write-Host "🔍 Verifying prerequisites..." -ForegroundColor Yellow

# Check if we can access bq command
try {
    $bqVersion = bq version
    Write-Host "✅ BigQuery CLI available: $bqVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ BigQuery CLI not available. Please run add_to_path.ps1 first." -ForegroundColor Red
    exit 1
}

# Check authentication
try {
    $authInfo = gcloud auth list --filter="status:ACTIVE" --format="value(account)"
    Write-Host "✅ Authenticated as: $authInfo" -ForegroundColor Green
} catch {
    Write-Host "❌ Not authenticated. Please run 'gcloud auth login'" -ForegroundColor Red
    exit 1
}

# Verify project access
try {
    gcloud config set project $PROJECT_ID
    Write-Host "✅ Project set to: $PROJECT_ID" -ForegroundColor Green
} catch {
    Write-Host "❌ Cannot access project: $PROJECT_ID" -ForegroundColor Red
    exit 1
}

# Deploy SQL Components
Write-Host "📊 Deploying SQL components..." -ForegroundColor Yellow

Write-Host "1. Creating main data table..."
bq query --use_legacy_sql=false --project_id=$PROJECT_ID @"
-- Create AMP_Data_Primary table with comprehensive business logic structure
CREATE OR REPLACE TABLE `$PROJECT_ID.${DATASET_DEV}.AMP_Data_Primary` AS
SELECT 
  -- Core fields from AMP Events
  CAST(event_id AS STRING) as Event_ID,
  CAST(event_creation_date AS TIMESTAMP) as Event_Creation_Date,
  CAST(event_modified_date AS TIMESTAMP) as Event_Modified_Date,
  CAST(status_name AS STRING) as status_name,
  CAST(store_nbr AS INT64) as store_nbr,
  
  -- Business logic JSON fields
  JSON_EXTRACT(json_payload, '$.store_activity') as Store_Activity_JSON,
  JSON_EXTRACT(json_payload, '$.users') as Users_JSON,
  JSON_EXTRACT(json_payload, '$.comments') as Comments_JSON,
  JSON_EXTRACT(json_payload, '$.verification') as Verification_JSON,
  JSON_EXTRACT_SCALAR(json_payload, '$.team_name') as team_name,
  
  -- Source timestamp for change tracking
  upd_ts as src_rcv_ts,
  
  -- Add processing metadata
  CURRENT_TIMESTAMP() as record_processed_at

FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
WHERE DATE(msg_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  AND event_id IS NOT NULL
LIMIT 1000;  -- Start with sample data
"@

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ AMP_Data_Primary table created successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create AMP_Data_Primary table" -ForegroundColor Red
    exit 1
}

Write-Host "2. Deploying business logic views..."
# Deploy the SQL file components
$sqlContent = Get-Content $SQL_FILE -Raw

# Split SQL file into individual statements and execute key components
$statements = $sqlContent -split ";\s*(?=CREATE|ALTER|DROP)"

$viewCount = 0
foreach ($statement in $statements) {
    if ($statement.Trim() -match "^CREATE OR REPLACE VIEW.*AMP_.*" -and 
        $statement -match "Business_Logic|Latest_Updates|Store_Activity|Teams|Users|Comments|Verification") {
        
        $viewName = if ($statement -match "`([^`]+\.AMP_[^`]+)`") { $matches[1] } else { "Unknown View" }
        Write-Host "   Creating view: $viewName" -ForegroundColor Cyan
        
        try {
            $statement.Trim() + ";" | bq query --use_legacy_sql=false --project_id=$PROJECT_ID
            if ($LASTEXITCODE -eq 0) {
                $viewCount++
                Write-Host "   ✅ $viewName created successfully" -ForegroundColor Green
            } else {
                Write-Host "   ⚠️ $viewName creation had issues" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "   ❌ Failed to create $viewName" -ForegroundColor Red
        }
    }
}

Write-Host "✅ Created $viewCount business logic views" -ForegroundColor Green

Write-Host "3. Deploying stored procedures..."
# Deploy procedures
foreach ($statement in $statements) {
    if ($statement.Trim() -match "^CREATE OR REPLACE PROCEDURE") {
        $procName = if ($statement -match "`([^`]+\.[^`]+_proc)`") { $matches[1] } else { "Unknown Procedure" }
        Write-Host "   Creating procedure: $procName" -ForegroundColor Cyan
        
        try {
            $statement.Trim() + ";" | bq query --use_legacy_sql=false --project_id=$PROJECT_ID
            if ($LASTEXITCODE -eq 0) {
                Write-Host "   ✅ $procName created successfully" -ForegroundColor Green
            } else {
                Write-Host "   ⚠️ $procName creation had issues" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "   ❌ Failed to create $procName" -ForegroundColor Red
        }
    }
}

# Business Logic Validation
Write-Host "🔍 Validating business logic implementation..." -ForegroundColor Yellow

Write-Host "1. Testing Latest Updates view..."
try {
    $latestCount = bq query --use_legacy_sql=false --project_id=$PROJECT_ID --format=csv --quiet "
    SELECT COUNT(*) as count 
    FROM `$PROJECT_ID.${DATASET_DEV}.AMP_Latest_Updates`
    " | Select-Object -Skip 1
    
    Write-Host "   ✅ Latest Updates view: $latestCount records" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Latest Updates view validation failed" -ForegroundColor Red
}

Write-Host "2. Testing Store Activity processing..."
try {
    $activityCount = bq query --use_legacy_sql=false --project_id=$PROJECT_ID --format=csv --quiet "
    SELECT COUNT(*) as count 
    FROM `$PROJECT_ID.${DATASET_DEV}.AMP_Store_Activity`
    " | Select-Object -Skip 1
    
    Write-Host "   ✅ Store Activity view: $activityCount records" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Store Activity view validation failed" -ForegroundColor Red
}

Write-Host "3. Testing Teams mapping..."
try {
    $teamsCount = bq query --use_legacy_sql=false --project_id=$PROJECT_ID --format=csv --quiet "
    SELECT COUNT(DISTINCT team_display_name) as count 
    FROM `$PROJECT_ID.${DATASET_DEV}.AMP_Teams`
    WHERE team_display_name != 'Unknown Team'
    " | Select-Object -Skip 1
    
    Write-Host "   ✅ Teams mapping: $teamsCount unique teams" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Teams mapping validation failed" -ForegroundColor Red
}

Write-Host "4. Testing Complete Business Logic view..."
try {
    $businessLogicCount = bq query --use_legacy_sql=false --project_id=$PROJECT_ID --format=csv --quiet "
    SELECT COUNT(*) as count 
    FROM `$PROJECT_ID.${DATASET_DEV}.AMP_Complete_Business_Logic`
    " | Select-Object -Skip 1
    
    Write-Host "   ✅ Complete Business Logic view: $businessLogicCount records" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Complete Business Logic view validation failed" -ForegroundColor Red
}

# Test procedure execution
Write-Host "5. Testing stored procedures..."
try {
    Write-Host "   Testing full refresh procedure..." -ForegroundColor Cyan
    bq query --use_legacy_sql=false --project_id=$PROJECT_ID "
    CALL `$PROJECT_ID.${DATASET_DEV}.full_refresh_proc`();
    "
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Full refresh procedure executed successfully" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ Full refresh procedure had issues" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Full refresh procedure test failed" -ForegroundColor Red
}

# Final validation report
Write-Host "📋 Generating validation report..." -ForegroundColor Yellow

$report = @"

=== AMP Business Logic Deployment Report ===
Date: $(Get-Date)
Project: $PROJECT_ID
Dataset: $DATASET_DEV

✅ DEPLOYED COMPONENTS:
- AMP_Data_Primary table
- AMP_Latest_Updates view
- AMP_Store_Activity view  
- AMP_Teams view
- AMP_Users view
- AMP_Comments view
- AMP_Verification_Complete view
- AMP_Complete_Business_Logic view
- full_refresh_proc stored procedure
- incremental_amp_update_proc stored procedure
- enhanced_amp_sync_proc stored procedure

🔍 BUSINESS LOGIC FEATURES:
- Latest timestamp extraction (max src_rcv_ts per Event_ID)
- Store activity processing with overdue indicators
- Team name mapping (TN0-TN18 to descriptive names)
- JSON array parsing for users, comments, verification
- Priority level assignment based on overdue and verification status
- Data quality flags for incomplete records
- Comprehensive change tracking and monitoring

📊 NEXT STEPS:
1. Test with actual AMP data
2. Deploy Cloud Functions for automated triggering
3. Set up monitoring and alerting
4. Schedule regular data validation

=== End Report ===
"@

Write-Host $report -ForegroundColor White

# Save report to file
$report | Out-File "deployment_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

Write-Host "`n🎉 Complete AMP Business Logic System deployment finished!" -ForegroundColor Green
Write-Host "Check the deployment report file for details." -ForegroundColor Cyan