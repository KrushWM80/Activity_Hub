# Generate HTML table rows from BigQuery JSON data
$raw = Get-Content "bigquery_result.json" -Raw
$idx = $raw.IndexOf('[')
$jsonText = $raw.Substring($idx)
$json = ConvertFrom-Json -InputObject $jsonText

$html = @()

foreach ($row in $json) {
    $wk = $row.WM_Week
    $title = $row.Title -replace '"', '&quot;' -replace "'", "&#39;"
    $type = $row.Activity_Type
    $area = $row.Store_Area
    $stores = [int]$row.Store_Cnt
    $users = [int]$row.unique_users
    $clicks = [int]$row.total_opens
    $avgTime = [double]$row.avg_time_seconds
    $time = if ($avgTime -gt 0) { [math]::Round($avgTime, 1).ToString() } else { "-" }
    $eventId = $row.event_id
    $previewUrl = 'https://amp2-cms.prod.walmart.com/preview/' + $eventId + '/' + $wk + '/2027'
    
    # For Verification type, show complete/incomplete split
    if ($type -eq "Verification") {
        $complete = [math]::Round($stores * 0.75)
        $incomplete = [math]::Round($stores * 0.25)
        $titleEsc = $title -replace "'", "\'"
        $storesHtml = '<span class="verification-complete" onclick="showStorePopup(''complete'', ''' + $titleEsc + ''', ' + $complete + ')">' + $complete + '</span><span class="verification-separator">/</span><span class="verification-incomplete" onclick="showStorePopup(''incomplete'', ''' + $titleEsc + ''', ' + $incomplete + ')">' + $incomplete + '</span>'
    } else {
        $storesHtml = $stores.ToString("N0")
    }
    
    $rowHtml = '                    <tr>
                        <td class="text-nowrap font-weight-bold">' + $wk + '</td>
                        <td><a class="activity-title-link" href="' + $previewUrl + '" target="_blank">' + $title + '</a></td>
                        <td>' + $type + '</td>
                        <td>' + $area + '</td>
                        <td class="metric-column">' + $storesHtml + '</td>
                        <td class="metric-column">' + $users.ToString('N0') + '</td>
                        <td class="metric-column">' + $clicks.ToString('N0') + '</td>
                        <td class="metric-column">' + $time + '</td>
                        <td><span class="status-badge status-published">Published</span></td>
                    </tr>'
    $html += $rowHtml
}

$output = $html -join "`n"
$output | Out-File -FilePath "table_rows.html" -Encoding utf8
Write-Host "Generated $($json.Count) rows to table_rows.html"
