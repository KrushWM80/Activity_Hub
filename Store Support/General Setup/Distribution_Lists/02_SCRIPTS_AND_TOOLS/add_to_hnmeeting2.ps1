# Add Members to HNMeeting2 Distribution List
# Adds emails from need_to_add list to the DL

$dlEmail = "HNMeeting2@email.wal-mart.com"
$emailFile = "need_to_add_to_hnmeeting2_20251216_112306.txt"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "  Adding Members to HNMeeting2 Distribution List" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# Load emails to add
$emailsToAdd = Get-Content $emailFile | Where-Object { $_ -match '@' }
Write-Host "`nEmails to add: $($emailsToAdd.Count)" -ForegroundColor Green

# Get the DL group object from AD
$searcher = New-Object System.DirectoryServices.DirectorySearcher
$searcher.Filter = "(&(objectClass=group)(mail=$dlEmail))"
$dlResult = $searcher.FindOne()

if (-not $dlResult) {
    Write-Host "`nX Distribution list not found in AD" -ForegroundColor Red
    Write-Host "The DL may be Exchange Online only. You'll need to use Exchange admin tools." -ForegroundColor Yellow
    exit 1
}

$dlEntry = $dlResult.GetDirectoryEntry()
Write-Host "✓ Found DL: $($dlEntry.Properties['cn'][0])" -ForegroundColor Green

Write-Host "`nAdding members..." -ForegroundColor Yellow
Write-Host "This may take a few minutes for 308 members...`n"

$added = 0
$failed = 0
$alreadyMember = 0
$notFound = 0

$total = $emailsToAdd.Count
$count = 0

foreach ($email in $emailsToAdd) {
    $count++
    
    if ($count % 25 -eq 0) {
        Write-Host "  Progress: $count / $total (Added: $added, Failed: $failed)" -ForegroundColor Cyan
    }
    
    # Find the user in AD
    $userSearcher = New-Object System.DirectoryServices.DirectorySearcher
    $userSearcher.Filter = "(mail=$email)"
    $userResult = $userSearcher.FindOne()
    
    if (-not $userResult) {
        $notFound++
        Write-Host "  X Not found in AD: $email" -ForegroundColor Red
        continue
    }
    
    $userDN = $userResult.Properties["distinguishedName"][0]
    
    # Check if already a member
    $currentMembers = $dlEntry.Properties["member"]
    if ($currentMembers -contains $userDN) {
        $alreadyMember++
        continue
    }
    
    # Add to group
    try {
        $dlEntry.Properties["member"].Add($userDN)
        $dlEntry.CommitChanges()
        $added++
    }
    catch {
        $failed++
        Write-Host "  X Failed to add: $email - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "  COMPLETE" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

Write-Host "`nResults:" -ForegroundColor White
Write-Host "  ✓ Successfully added:     $added" -ForegroundColor Green
Write-Host "  ⊙ Already members:        $alreadyMember" -ForegroundColor Yellow
Write-Host "  ⊗ Not found in AD:        $notFound" -ForegroundColor Red
Write-Host "  X Failed:                 $failed" -ForegroundColor Red
Write-Host "  ━ Total processed:        $total" -ForegroundColor Cyan

if ($added -gt 0) {
    Write-Host "`n✓ Successfully added $added members to HNMeeting2!" -ForegroundColor Green
    Write-Host "`nNote: Changes may take 5-15 minutes to replicate in Exchange." -ForegroundColor Yellow
}

if ($notFound -gt 0) {
    Write-Host "`nWarning: $notFound emails not found in Active Directory." -ForegroundColor Yellow
    Write-Host "These may be external emails or accounts not synced to AD." -ForegroundColor Yellow
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
