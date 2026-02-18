# Extract members from four distribution lists
# Run this in PowerShell with Exchange Online module loaded

$distributionLists = @(
    'HN-MerchTeam@email.wal-mart.com',
    'HN-SupplyChainteam@email.wal-mart.com',
    'HN-SupportTeam@email.wal-mart.com',
    'HN-TomWardTeam@email.wal-mart.com'
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputFile = "Four_DL_Members_$timestamp.csv"

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*79) -ForegroundColor Cyan
Write-Host "EXTRACTING MEMBERS FROM FOUR DISTRIBUTION LISTS" -ForegroundColor Cyan
Write-Host ("="*80) -ForegroundColor Cyan

$allMembers = @()

foreach ($dl in $distributionLists) {
    Write-Host "`nExtracting: $dl" -ForegroundColor Yellow
    
    try {
        $members = Get-DistributionGroupMember -Identity $dl -ResultSize Unlimited -ErrorAction Stop
        
        Write-Host "  Found: $($members.Count) members" -ForegroundColor Green
        
        foreach ($member in $members) {
            $allMembers += [PSCustomObject]@{
                Email = $member.PrimarySmtpAddress
                Name = $member.Name
                DisplayName = $member.DisplayName
                RecipientType = $member.RecipientType
                Source_DL = $dl
            }
        }
    }
    catch {
        Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n$("="*80)" -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host ("="*80) -ForegroundColor Cyan
Write-Host "Total members extracted: $($allMembers.Count)" -ForegroundColor Green

# Group by source
$groupedByDL = $allMembers | Group-Object Source_DL
Write-Host "`nBreakdown by Distribution List:" -ForegroundColor Yellow
foreach ($group in $groupedByDL) {
    Write-Host "  $($group.Name): $($group.Count) members" -ForegroundColor White
}

# Export to CSV
$allMembers | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8

Write-Host "`n$([char]0x2713) Data exported to: $outputFile" -ForegroundColor Green
Write-Host ("="*80) -ForegroundColor Cyan

# Display sample
Write-Host "`nSample records (first 10):" -ForegroundColor Yellow
$allMembers | Select-Object Email, Name, Source_DL -First 10 | Format-Table -AutoSize
