@{
    'test' = 'script'
}

# Check all statuses
$response = Invoke-WebRequest -Uri 'http://localhost:8001/api/projects?status=Active&limit=10000' -UseBasicParsing -ErrorAction Stop
$data = $response.Content | ConvertFrom-Json

$titles_active = @()
foreach ($item in $data) {
    if ($item.title) {
        $titles_active += $item.title
    }
}
$unique_active = $titles_active | Sort-Object -Unique

Write-Host "Status: ACTIVE"
Write-Host "  Total records: $(($data | Measure-Object).Count)"
Write-Host "  Unique titles: $($unique_active.Count)"
Write-Host "  Titles:"
$unique_active | ForEach-Object { Write-Host "    - $_" }
Write-Host ""

# Try with no status filter (raw from API)
Write-Host "Checking if we can see all statuses from filters endpoint..."
$filters = Invoke-WebRequest -Uri 'http://localhost:8001/api/filters' -UseBasicParsing -ErrorAction Stop
$filter_data = $filters.Content | ConvertFrom-Json
if ($filter_data.health_statuses) {
    Write-Host "Available statuses from filters:"
    $filter_data.health_statuses | ForEach-Object { Write-Host "  - $_" }
}
