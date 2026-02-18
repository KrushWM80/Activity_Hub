# Extract members from two distribution lists for comparison
# U.S. Comm - All MMs vs OPS_SUP_MARKET_TEAM

$distributionLists = @(
    'U.S. Comm - All MMs',
    'OPS_SUP_MARKET_TEAM'
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

Write-Host ("="*80) -ForegroundColor Cyan
Write-Host "EXTRACTING MEMBERS FROM TWO DISTRIBUTION LISTS" -ForegroundColor Cyan
Write-Host ("="*80) -ForegroundColor Cyan

$allResults = @()

foreach ($dlName in $distributionLists) {
    Write-Host "`nExtracting: $dlName" -ForegroundColor Yellow
    
    # Try multiple email formats
    $emailFormats = @(
        $dlName,
        "$dlName@email.wal-mart.com",
        "$dlName@walmart.com"
    )
    
    $extracted = $false
    foreach ($email in $emailFormats) {
        try {
            $members = Get-DistributionGroupMember -Identity $email -ResultSize Unlimited -ErrorAction Stop
            
            Write-Host "  Found: $($members.Count) members" -ForegroundColor Green
            
            foreach ($member in $members) {
                $allResults += [PSCustomObject]@{
                    DistributionList = $dlName
                    Email = $member.PrimarySmtpAddress
                    DisplayName = $member.DisplayName
                    Name = $member.Name
                    RecipientType = $member.RecipientType
                }
            }
            
            $extracted = $true
            break
        }
        catch {
            # Try next format
            continue
        }
    }
    
    if (-not $extracted) {
        Write-Host "  ERROR: Could not extract members" -ForegroundColor Red
        Write-Host "  Please export manually or check the exact DL name" -ForegroundColor Yellow
    }
}

if ($allResults.Count -gt 0) {
    # Export combined results
    $outputFile = "Two_DL_Comparison_Raw_$timestamp.csv"
    $allResults | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8
    
    Write-Host "`n$([char]0x2713) Data exported to: $outputFile" -ForegroundColor Green
    
    # Show summary
    Write-Host "`n$("="*80)" -ForegroundColor Cyan
    Write-Host "EXTRACTION SUMMARY" -ForegroundColor Cyan
    Write-Host ("="*80) -ForegroundColor Cyan
    
    $grouped = $allResults | Group-Object DistributionList
    foreach ($group in $grouped) {
        Write-Host "  $($group.Name): $($group.Count) members" -ForegroundColor White
    }
}
else {
    Write-Host "`nNo data extracted. Manual export needed." -ForegroundColor Red
    Write-Host "`nTo manually export:" -ForegroundColor Yellow
    Write-Host "1. Open Outlook or OWA" -ForegroundColor White
    Write-Host "2. Search for each distribution list" -ForegroundColor White
    Write-Host "3. Export members to CSV" -ForegroundColor White
    Write-Host "4. Save as:" -ForegroundColor White
    Write-Host "   - US_Comm_All_MMs.csv" -ForegroundColor Cyan
    Write-Host "   - OPS_SUP_MARKET_TEAM.csv" -ForegroundColor Cyan
    Write-Host "5. Run the Python comparison script" -ForegroundColor White
}

Write-Host "`n$("="*80)" -ForegroundColor Cyan
