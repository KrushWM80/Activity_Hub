# Test permissions and add 308 members to HNMeeting2 Distribution List
# Created: December 17, 2025

Write-Host "=" * 80
Write-Host "HNMeeting2 Member Addition Script"
Write-Host "=" * 80
Write-Host ""

# Configuration
$groupEmail = "HNMeeting2@email.wal-mart.com"
$groupDN = "CN=HNMeeting2,OU=Collab,OU=ManualManaged,OU=Groups,OU=IDM,DC=homeoffice,DC=Wal-Mart,DC=com"
$emailListFile = "need_to_add_to_hnmeeting2_20251216_112306.txt"
$logFile = "add_members_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

# Initialize counters
$totalToAdd = 0
$successCount = 0
$failCount = 0
$notFoundCount = 0

# Step 1: Test group access
Write-Host "Step 1: Testing access to HNMeeting2 group..."
try {
    $group = [ADSI]"LDAP://$groupDN"
    Write-Host "✓ Successfully connected to group: $($group.cn)" -ForegroundColor Green
    Write-Host "  Email: $($group.mail)"
    Write-Host "  Managed By: $($group.managedBy)"
    Write-Host ""
} catch {
    Write-Host "✗ FAILED: Cannot access group" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please contact IT or Exchange administrator." -ForegroundColor Yellow
    exit 1
}

# Step 2: Test write permissions
Write-Host "Step 2: Testing write permissions..."
try {
    # Try to modify a harmless property (description) to test write access
    $originalDescription = $group.description
    $group.Put("description", $originalDescription)
    $group.SetInfo()
    Write-Host "✓ We have WRITE permissions to the group!" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "✗ FAILED: No write permissions" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "You need one of the following:" -ForegroundColor Yellow
    Write-Host "  1. Be the group owner (Jenny DeShields - jdeshi1)" -ForegroundColor Yellow
    Write-Host "  2. Have Exchange Administrator role" -ForegroundColor Yellow
    Write-Host "  3. Have delegated permissions to manage this group" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Contact IT Help Desk or email the group owner to request member additions." -ForegroundColor Yellow
    exit 1
}

# Step 3: Read email list
Write-Host "Step 3: Reading email list from $emailListFile..."
if (!(Test-Path $emailListFile)) {
    Write-Host "✗ FAILED: File not found: $emailListFile" -ForegroundColor Red
    exit 1
}

$content = Get-Content $emailListFile
$emails = $content | Where-Object { $_ -match '@' -and $_ -notmatch '^Emails to add' -and $_ -notmatch '^====' }
$totalToAdd = $emails.Count
Write-Host "✓ Found $totalToAdd emails to add" -ForegroundColor Green
Write-Host ""

# Step 4: Add members
Write-Host "Step 4: Adding members to HNMeeting2..."
Write-Host "This may take several minutes..."
Write-Host ""

$startTime = Get-Date

foreach ($email in $emails) {
    $email = $email.Trim()
    if ([string]::IsNullOrWhiteSpace($email)) { continue }
    
    try {
        # Search for user in AD
        $userSearcher = New-Object System.DirectoryServices.DirectorySearcher
        $userSearcher.Filter = "(&(objectClass=user)(mail=$email))"
        $userSearcher.PropertiesToLoad.Add("distinguishedName") | Out-Null
        $userSearcher.PropertiesToLoad.Add("cn") | Out-Null
        $userResult = $userSearcher.FindOne()
        
        if (!$userResult) {
            Write-Host "  ⚠ NOT FOUND in AD: $email" -ForegroundColor Yellow
            $notFoundCount++
            Add-Content $logFile "NOT_FOUND: $email"
            continue
        }
        
        $userDN = $userResult.Properties['distinguishedname'][0]
        $userName = $userResult.Properties['cn'][0]
        
        # Check if already a member
        $isMember = $false
        foreach ($member in $group.member) {
            if ($member -eq $userDN) {
                $isMember = $true
                break
            }
        }
        
        if ($isMember) {
            Write-Host "  ⚠ ALREADY MEMBER: $email ($userName)" -ForegroundColor Yellow
            Add-Content $logFile "ALREADY_MEMBER: $email"
            continue
        }
        
        # Add user to group
        $group.Add("LDAP://$userDN")
        $group.SetInfo()
        
        Write-Host "  ✓ ADDED: $email ($userName)" -ForegroundColor Green
        $successCount++
        Add-Content $logFile "SUCCESS: $email ($userName)"
        
        # Brief pause to avoid overwhelming AD
        Start-Sleep -Milliseconds 100
        
    } catch {
        Write-Host "  ✗ FAILED: $email - $($_.Exception.Message)" -ForegroundColor Red
        $failCount++
        Add-Content $logFile "FAILED: $email - $($_.Exception.Message)"
    }
    
    # Progress update every 50 emails
    $processed = $successCount + $failCount + $notFoundCount
    if ($processed % 50 -eq 0) {
        Write-Host ""
        Write-Host "  Progress: $processed / $totalToAdd processed..." -ForegroundColor Cyan
        Write-Host ""
    }
}

$endTime = Get-Date
$duration = $endTime - $startTime

# Step 5: Summary
Write-Host ""
Write-Host "=" * 80
Write-Host "SUMMARY"
Write-Host "=" * 80
Write-Host "Total emails to add:    $totalToAdd"
Write-Host "✓ Successfully added:   $successCount" -ForegroundColor Green
Write-Host "✗ Failed:               $failCount" -ForegroundColor Red
Write-Host "⚠ Not found in AD:      $notFoundCount" -ForegroundColor Yellow
Write-Host "⚠ Already members:      $(($totalToAdd - $successCount - $failCount - $notFoundCount))" -ForegroundColor Yellow
Write-Host ""
Write-Host "Time taken: $($duration.TotalSeconds) seconds"
Write-Host "Log file: $logFile"
Write-Host "=" * 80

if ($successCount -gt 0) {
    Write-Host ""
    Write-Host "✓ HNMeeting2 distribution list updated successfully!" -ForegroundColor Green
    Write-Host "  New member count: $(1246 + $successCount)" -ForegroundColor Green
}
