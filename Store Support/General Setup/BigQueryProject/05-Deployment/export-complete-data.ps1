# Export complete AMP data from BigQuery without limits

Write-Host "🔍 EXPORTING COMPLETE AMP DATASET FROM BIGQUERY..." -ForegroundColor Yellow
Write-Host ""

$query = @"
SELECT 
    week_number,
    actv_title_home_ofc_nm,
    division,
    store_nbr,
    preview_link,
    published,
    region,
    market,
    activity_type,
    store_area,
    create_ts,
    msg_start_dt,
    msg_end_dt,
    -- Get ALL fields to ensure complete data
    *
FROM ``wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep``
WHERE published = true
ORDER BY week_number DESC, actv_title_home_ofc_nm
"@

Write-Host "📊 Running BigQuery export (NO LIMITS)..." -ForegroundColor Green
Write-Host "Query: $query" -ForegroundColor Cyan
Write-Host ""

# Export to JSON
$outputFile = "bigquery-complete-export.json"

try {
    # Run BigQuery command to export complete dataset
    Write-Host "Executing: bq query --use_legacy_sql=false --format=json" -ForegroundColor Magenta
    
    $result = bq query --use_legacy_sql=false --format=json $query | Out-String
    
    # Save to file
    $result | Out-File -FilePath $outputFile -Encoding UTF8
    
    Write-Host "✅ SUCCESS: Complete dataset exported to $outputFile" -ForegroundColor Green
    
    # Count records
    $jsonData = Get-Content $outputFile | ConvertFrom-Json
    $totalRecords = $jsonData.Count
    $week39Records = ($jsonData | Where-Object { $_.week_number -eq 39 }).Count
    
    Write-Host ""
    Write-Host "📈 EXPORT SUMMARY:" -ForegroundColor Yellow
    Write-Host "   Total Records: $totalRecords" -ForegroundColor White
    Write-Host "   Week 39 Records: $week39Records" -ForegroundColor White
    Write-Host "   Output File: $outputFile" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 Next Steps:" -ForegroundColor Green
    Write-Host "   1. Refresh dashboard" -ForegroundColor White
    Write-Host "   2. Dashboard will auto-load complete dataset" -ForegroundColor White
    Write-Host "   3. Verify 75+ Week 39 activities display" -ForegroundColor White
    
} catch {
    Write-Host "❌ ERROR: Failed to export BigQuery data" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Manual Alternative:" -ForegroundColor Yellow
    Write-Host "   1. Open BigQuery Console" -ForegroundColor White
    Write-Host "   2. Run query manually" -ForegroundColor White
    Write-Host "   3. Export results as JSON" -ForegroundColor White
    Write-Host "   4. Save as $outputFile" -ForegroundColor White
}
