# BigQuery Connection Test - PowerShell Version
# Test connection to wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep

Write-Host "🧪 BigQuery Connection Test - PowerShell Version" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Gray
Write-Host "📊 Target: wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep" -ForegroundColor Yellow
Write-Host ""

# Test 1: Check Google Cloud CLI
Write-Host "1. 🏠 Environment Check" -ForegroundColor Green

try {
    $gcloudVersion = gcloud --version 2>$null
    if ($gcloudVersion) {
        Write-Host "   ✅ Google Cloud CLI found" -ForegroundColor Green
        Write-Host "   📋 Version: $($gcloudVersion[0])" -ForegroundColor Gray
        
        # Check authentication
        $activeAccount = gcloud auth list --filter="status:ACTIVE" --format="value(account)" 2>$null
        if ($activeAccount) {
            Write-Host "   ✅ Authenticated as: $activeAccount" -ForegroundColor Green
        } else {
            Write-Host "   ❌ Not authenticated with gcloud" -ForegroundColor Red
            Write-Host "   💡 Run: gcloud auth login" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ❌ Google Cloud CLI not found" -ForegroundColor Red
        Write-Host "   💡 Install from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Error checking Google Cloud CLI: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Generate test commands
Write-Host ""
Write-Host "2. 🌐 Test Commands" -ForegroundColor Green

$projectId = "wmt-assetprotection-prod"
$dataset = "Store_Support_Dev"
$table = "AMP_Data_Prep"

# Basic connection test
$basicQuery = @"
{
  "query": "SELECT COUNT(*) as total_rows FROM \`$projectId.$dataset.$table\` LIMIT 1",
  "useLegacySql": false
}
"@

Write-Host "   📋 Basic Connection Test:" -ForegroundColor Gray
Write-Host "   " + ("-" * 50) -ForegroundColor Gray
Write-Host "   # Method 1: Using gcloud" -ForegroundColor Cyan
Write-Host "   bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM \`$projectId.$dataset.$table\`'" -ForegroundColor White
Write-Host ""
Write-Host "   # Method 2: Using curl with REST API" -ForegroundColor Cyan
$curlCommand = @"
curl -H "Authorization: Bearer `$(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  --data '$($basicQuery -replace '"', '\"')' \
  "https://bigquery.googleapis.com/bigquery/v2/projects/$projectId/queries"
"@
Write-Host "   $curlCommand" -ForegroundColor White

# Test 3: Sample queries
Write-Host ""
Write-Host "3. 📝 Sample Test Queries" -ForegroundColor Green

$queries = @(
    @{
        Name = "Table Statistics"
        Query = @"
SELECT 
  COUNT(*) as total_rows,
  COUNT(DISTINCT actv_title_home_ofc_nm) as unique_activities,
  MIN(create_ts) as earliest_date,
  MAX(create_ts) as latest_date
FROM \`$projectId.$dataset.$table\`
"@
    },
    @{
        Name = "Recent Activities"
        Query = @"
SELECT 
  actv_title_home_ofc_nm as activity_title,
  location,
  division,
  activity_type,
  status,
  create_ts
FROM \`$projectId.$dataset.$table\`
WHERE create_ts >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
ORDER BY create_ts DESC
LIMIT 10
"@
    },
    @{
        Name = "Dashboard Data Sample"
        Query = @"
SELECT 
  EXTRACT(WEEK FROM create_ts) as week_number,
  actv_title_home_ofc_nm as activity_title,
  location,
  COUNT(*) as total_count,
  division,
  activity_type,
  status
FROM \`$projectId.$dataset.$table\`
WHERE published = true
  AND create_ts >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
GROUP BY week_number, activity_title, location, division, activity_type, status
ORDER BY week_number DESC, activity_title
LIMIT 20
"@
    }
)

foreach ($query in $queries) {
    Write-Host "   📊 $($query.Name):" -ForegroundColor Yellow
    Write-Host "   " + ("-" * 40) -ForegroundColor Gray
    Write-Host "   bq query --use_legacy_sql=false """ -ForegroundColor Cyan -NoNewline
    Write-Host $query.Query -ForegroundColor White -NoNewline
    Write-Host """" -ForegroundColor Cyan
    Write-Host ""
}

# Test 4: Save test files
Write-Host "4. 💾 Generating Test Files" -ForegroundColor Green

# Save basic test script
$testScript = @"
#!/bin/bash
# BigQuery Connection Test Script
# Generated: $(Get-Date)

echo "🧪 Testing BigQuery Connection..."
echo "📊 Target: $projectId.$dataset.$table"

# Test 1: Basic connection
echo "1. Testing basic connection..."
bq query --use_legacy_sql=false 'SELECT COUNT(*) as total_rows FROM \`$projectId.$dataset.$table\` LIMIT 1'

# Test 2: Sample data
echo "2. Getting sample data..."
bq query --use_legacy_sql=false 'SELECT * FROM \`$projectId.$dataset.$table\` LIMIT 5'

echo "✅ Test complete!"
"@

$testScript | Out-File -FilePath "bigquery-test.sh" -Encoding UTF8
Write-Host "   ✅ Created: bigquery-test.sh" -ForegroundColor Green

# Save SQL queries
$sqlQueries = @"
-- BigQuery Test Queries for AMP Dashboard
-- Generated: $(Get-Date)
-- Target: $projectId.$dataset.$table

"@ + ($queries | ForEach-Object { "-- $($_.Name)`n$($_.Query);`n`n" }) -join ""

$sqlQueries | Out-File -FilePath "bigquery-test-queries.sql" -Encoding UTF8
Write-Host "   ✅ Created: bigquery-test-queries.sql" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host ("=" * 60) -ForegroundColor Gray
Write-Host "🏁 Test Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Ensure you're authenticated: gcloud auth login" -ForegroundColor White
Write-Host "2. Test basic connection: bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM \`$projectId.$dataset.$table\`'" -ForegroundColor White
Write-Host "3. Run test script: bash bigquery-test.sh" -ForegroundColor White
Write-Host "4. Check dashboard connection in browser console" -ForegroundColor White
Write-Host ""
Write-Host "Files created:" -ForegroundColor Yellow
Write-Host "- bigquery-test.sh (bash test script)" -ForegroundColor Gray
Write-Host "- bigquery-test-queries.sql (sample queries)" -ForegroundColor Gray

# Optional: Run basic test if gcloud is available
Write-Host ""
$runTest = Read-Host "Run basic connection test now? (y/N)"
if ($runTest -eq 'y' -or $runTest -eq 'Y') {
    Write-Host ""
    Write-Host "🚀 Running basic connection test..." -ForegroundColor Cyan
    
    try {
        $result = bq query --use_legacy_sql=false "SELECT COUNT(*) as total_rows FROM \`$projectId.$dataset.$table\` LIMIT 1" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Connection successful!" -ForegroundColor Green
            Write-Host "📊 Result: $result" -ForegroundColor Gray
        } else {
            Write-Host "❌ Connection failed!" -ForegroundColor Red
            Write-Host "Error: $result" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Test error: $($_.Exception.Message)" -ForegroundColor Red
    }
}