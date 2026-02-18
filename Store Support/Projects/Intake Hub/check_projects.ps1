@{
    'test' = 'script'
}

$response = Invoke-WebRequest -Uri 'http://localhost:8001/api/projects' -UseBasicParsing -ErrorAction Stop
$data = $response.Content | ConvertFrom-Json

Write-Host "Total items in response: $(($data | Measure-Object).Count)"
Write-Host ""

# Extract all titles
$titles = @()
foreach ($item in $data) {
    if ($item.title) {
        $titles += $item.title
    }
}

# Get unique titles  
$unique = $titles | Sort-Object -Unique

Write-Host "Unique titles: $($unique.Count)"
Write-Host ""
Write-Host "All  unique titles:"
$unique | ForEach-Object { Write-Host "  - $_" }
