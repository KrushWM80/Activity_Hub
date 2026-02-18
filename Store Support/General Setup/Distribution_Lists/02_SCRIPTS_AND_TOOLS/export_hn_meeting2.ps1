# Export Distribution List Members - Simple Version
# Exports HNMeeting2 DL members without Exchange module

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "  Distribution List Member Export" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

$dlEmail = "HNMeeting2@email.wal-mart.com"
$outputFile = "hnmeeting2_members.csv"

Write-Host "`nSearching for: $dlEmail`n"

# Try LDAP query
Write-Host "Trying LDAP query..." -ForegroundColor Yellow

$searcher = New-Object System.DirectoryServices.DirectorySearcher
$searcher.Filter = "(&(objectClass=group)(mail=$dlEmail))"
$searcher.PropertiesToLoad.Add("member") | Out-Null
$searcher.PropertiesToLoad.Add("cn") | Out-Null

$result = $searcher.FindOne()

if ($result) {
    $groupName = $result.Properties["cn"][0]
    Write-Host "✓ Found group: $groupName" -ForegroundColor Green
    
    $memberDNs = $result.Properties["member"]
    Write-Host "  Total members: $($memberDNs.Count)" -ForegroundColor Green
    Write-Host "`nExtracting email addresses...`n"
    
    $members = @()
    $count = 0
    
    foreach ($memberDN in $memberDNs) {
        $count++
        if ($count % 100 -eq 0) {
            Write-Host "  Processed $count of $($memberDNs.Count)..."
        }
        
        $userSearcher = New-Object System.DirectoryServices.DirectorySearcher
        $userSearcher.Filter = "(distinguishedName=$memberDN)"
        $userSearcher.PropertiesToLoad.Add("mail") | Out-Null
        $userSearcher.PropertiesToLoad.Add("displayName") | Out-Null
        $userSearcher.PropertiesToLoad.Add("title") | Out-Null
        
        $userResult = $userSearcher.FindOne()
        
        if ($userResult) {
            $email = if ($userResult.Properties["mail"].Count -gt 0) { $userResult.Properties["mail"][0] } else { "" }
            $name = if ($userResult.Properties["displayName"].Count -gt 0) { $userResult.Properties["displayName"][0] } else { "" }
            $title = if ($userResult.Properties["title"].Count -gt 0) { $userResult.Properties["title"][0] } else { "" }
            
            if ($email) {
                $members += [PSCustomObject]@{
                    Email = $email
                    Name = $name
                    Title = $title
                }
            }
        }
    }
    
    if ($members.Count -gt 0) {
        $members | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8
        Write-Host "`n✓ SUCCESS!" -ForegroundColor Green
        Write-Host "  Exported $($members.Count) members to: $outputFile" -ForegroundColor Green
        Write-Host "`nNext step: Run comparison" -ForegroundColor Cyan
        Write-Host "  python compare_emails_simple.py`n" -ForegroundColor White
    } else {
        Write-Host "`nX No members with email addresses found" -ForegroundColor Red
    }
    
} else {
    Write-Host "X Group not found: $dlEmail" -ForegroundColor Red
    Write-Host "`nPossible reasons:" -ForegroundColor Yellow
    Write-Host "  - DL doesn't exist in Active Directory"
    Write-Host "  - DL is in Exchange Online only (not synced to AD)"
    Write-Host "  - Different email address"
    Write-Host "  - No permission to query"
    
    Write-Host "`n==========================================================" -ForegroundColor Cyan
    Write-Host "  Alternative: Manual Export from Outlook" -ForegroundColor Yellow
    Write-Host "==========================================================" -ForegroundColor Cyan
    
    Write-Host "
1. Open Outlook
2. Search for: $dlEmail
3. Right-click the group -> Properties
4. Members tab -> Export or copy member list
5. Save as: $outputFile in this folder
6. Run: python compare_emails_simple.py

Or use Outlook Web:
  https://outlook.office365.com
  Search -> Group -> Members -> Copy list
"
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
