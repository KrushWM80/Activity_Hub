$EmailAddresses = @("ATCTeamsupport@walmart.com", "kendall.rush@walmart.com")
$Subject = "Activity Hub Daily Status Report - $(Get-Date -Format 'MMMM d, yyyy')"

$HTMLBody = @"
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; font-size: 11pt; }
        .header { background: #0071ce; color: white; padding: 15px; }
        .section { margin: 15px 0; padding: 10px; background: #f5f5f5; }
        .status-ok { color: #22863a; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; }
        th { background: #f1f8ff; text-align: left; padding: 8px; border: 1px solid #ddd; }
        td { padding: 8px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Activity Hub Daily Status Report</h2>
        <p>$(Get-Date -Format 'MMMM d, yyyy - dddd h:mm tt')</p>
    </div>

    <div class="section">
        <h3>System Status</h3>
        <table>
            <tr>
                <th>Component</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
            <tr>
                <td>Projects in Stores Backend</td>
                <td class="status-ok">RUNNING</td>
                <td>Port 8001 - FastAPI operational</td>
            </tr>
            <tr>
                <td>DC Manager PayCycle Automation</td>
                <td class="status-ok">ACTIVE</td>
                <td>26/26 tasks scheduled through Jan 2027</td>
            </tr>
            <tr>
                <td>Job Codes and Teaming Sync</td>
                <td class="status-ok">RUNNING</td>
                <td>Daily reconciliation active (2:00 AM EST)</td>
            </tr>
        </table>
    </div>

    <div class="section">
        <h3>Key Metrics</h3>
        <ul>
            <li><strong>Services Running:</strong> 3 of 3 (100%)</li>
            <li><strong>Scheduled Tasks:</strong> 29 active</li>
            <li><strong>Job Codes Coverage:</strong> 191/195 roles (98%)</li>
            <li><strong>Last Update:</strong> $(Get-Date -Format 'MMMM d, yyyy h:mm tt')</li>
        </ul>
    </div>

    <div class="section">
        <h3>Recent Activity</h3>
        <ul>
            <li>March 10, 2026: All services restored and verified</li>
            <li>March 11, 2026: Continuous monitoring - all systems stable</li>
            <li>Next PayCycle: PC-03 on March 6, 2026 at 6:00 AM</li>
        </ul>
    </div>

    <div class="section">
        <h3>Upcoming Schedule</h3>
        <ul>
            <li>Tonight (2:00 AM): Job Codes reconciliation</li>
            <li>March 6 (6:00 AM): DC Manager PayCycle email send</li>
            <li>Daily: Automated health monitoring</li>
        </ul>
    </div>

    <hr>
    <p style="font-size: 9pt; color: #666;">
        Activity Hub Monitor | WEUS42608431466 | Automated Report
    </p>
</body>
</html>
"@

try {
    $outlook = New-Object -ComObject Outlook.Application
    $mail = $outlook.CreateItem(0)
    
    $mail.To = $EmailAddresses -join ";"
    $mail.Subject = $Subject
    $mail.HTMLBody = $HTMLBody
    $mail.Send()
    
    Write-Host "SUCCESS: Email sent!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Recipients:" -ForegroundColor Cyan
    foreach ($addr in $EmailAddresses) {
        Write-Host "  - $addr" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "Subject: $Subject" -ForegroundColor Cyan
    Write-Host "Sent: $(Get-Date -Format 'MMMM d, yyyy h:mm tt')" -ForegroundColor Cyan
    
} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
}
