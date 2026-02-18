# Export Distribution List Members to CSV
# Run this script to export HNMeeting2 DL members without needing Exchange Online Management module

# Method 1: Using Active Directory (if DL is in AD)
Write-Host "`n================================================================================`n" -ForegroundColor Cyan
Write-Host "METHOD 1: Export via Active Directory" -ForegroundColor Yellow
Write-Host "================================================================================`n" -ForegroundColor Cyan

try {
    # Try to get the group from AD
    $group = Get-ADGroup -Filter "mail -eq 'HNMeeting2@email.wal-mart.com'" -Properties mail, member -ErrorAction Stop
    
    if ($group) {
        Write-Host "✓ Found group in AD: $($group.Name)" -ForegroundColor Green
        
        $members = @()
        foreach ($memberDN in $group.member) {
            try {
                $user = Get-ADUser -Identity $memberDN -Properties mail, displayName, title -ErrorAction SilentlyContinue
                if ($user.mail) {
                    $members += [PSCustomObject]@{
                        Email = $user.mail
                        Name = $user.displayName
                        Title = $user.title
                    }
                }
            } catch {
                # Skip if can't get user
            }
        }
        
        if ($members.Count -gt 0) {
            $outputFile = "hnmeeting2_members.csv"
            $members | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8
            Write-Host "✓ Exported $($members.Count) members to: $outputFile" -ForegroundColor Green
            Write-Host "`nNow run: python compare_emails_simple.py" -ForegroundColor Cyan
            exit 0
        } else {
            Write-Host "X No members found with email addresses" -ForegroundColor Red
        }
    } else {
        Write-Host "X Group not found in AD" -ForegroundColor Red
    }
}
catch {
    Write-Host "X AD method failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Method 2: Using LDAP query
Write-Host "`n================================================================================`n" -ForegroundColor Cyan
Write-Host "METHOD 2: Export via LDAP Query" -ForegroundColor Yellow
Write-Host "================================================================================`n" -ForegroundColor Cyan

try {
    $searcher = New-Object System.DirectoryServices.DirectorySearcher
    $searcher.Filter = "(&(objectClass=group)(mail=HNMeeting2@email.wal-mart.com))"
    $searcher.PropertiesToLoad.Add("member") | Out-Null
    
    $result = $searcher.FindOne()
    
    if ($result) {
        Write-Host "✓ Found group via LDAP" -ForegroundColor Green
        
        $members = @()
        $memberDNs = $result.Properties["member"]
        
        $i = 0
        foreach ($memberDN in $memberDNs) {
            $i++
            if ($i % 50 -eq 0) {
                Write-Host "  Processing member $i of $($memberDNs.Count)..."
            }
            
            $userSearcher = New-Object System.DirectoryServices.DirectorySearcher
            $userSearcher.Filter = "(distinguishedName=$memberDN)"
            $userSearcher.PropertiesToLoad.Add("mail") | Out-Null
            $userSearcher.PropertiesToLoad.Add("displayName") | Out-Null
            
            $userResult = $userSearcher.FindOne()
            if ($userResult -and $userResult.Properties["mail"]) {
                $members += [PSCustomObject]@{
                    Email = $userResult.Properties["mail"][0]
                    Name = $userResult.Properties["displayName"][0]
                }
            }
        }
        
        if ($members.Count -gt 0) {
            $outputFile = "hnmeeting2_members.csv"
            $members | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8
            Write-Host "✓ Exported $($members.Count) members to: $outputFile" -ForegroundColor Green
            Write-Host "`nNow run: python compare_emails_simple.py" -ForegroundColor Cyan
            exit 0
        } else {
            Write-Host "X No members with email found" -ForegroundColor Red
        }
    } else {
        Write-Host "X Group not found via LDAP" -ForegroundColor Red
    }
}
catch {
    Write-Host "X LDAP method failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Method 3: Manual instructions
Write-Host "`n================================================================================`n" -ForegroundColor Cyan
Write-Host "ALTERNATIVE: Manual Export from Outlook" -ForegroundColor Yellow
Write-Host "================================================================================`n" -ForegroundColor Cyan

Write-Host @"
Since automated methods aren't working, please export manually:

1. Open Outlook
2. In the search box, type: HNMeeting2@email.wal-mart.com
3. Right-click on the distribution list in results
4. Select "Properties" or "Advanced Find"
5. Go to "Members" tab
6. Options:
   
   Option A: Copy members
   - Select all members (Ctrl+A)
   - Copy (Ctrl+C)
   - Paste into Excel
   - Save as: hnmeeting2_members.csv
   
   Option B: Export feature
   - Look for "Export" or "Save" button
   - Save as CSV
   - Name it: hnmeeting2_members.csv

7. Place the CSV file in this folder:
   $PWD

8. Run: python compare_emails_simple.py

The CSV should have at least one column with email addresses.

"@ -ForegroundColor White

Write-Host "`n================================================================================`n" -ForegroundColor Cyan
Write-Host "Or try Outlook Web Access (OWA):" -ForegroundColor Yellow
Write-Host "  1. Go to: https://outlook.office365.com" -ForegroundColor White
Write-Host "  2. Search for: HNMeeting2@email.wal-mart.com" -ForegroundColor White
Write-Host "  3. Click the group → Members" -ForegroundColor White
Write-Host "  4. Copy the member list" -ForegroundColor White
Write-Host "`n================================================================================`n" -ForegroundColor Cyan
