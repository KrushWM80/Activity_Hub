# Install RSAT and Extract Tableau Group
# Run this script as Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RSAT Installation & Group Extraction" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✓ Running as Administrator" -ForegroundColor Green
Write-Host ""

# Step 1: Check if RSAT AD Tools are installed
Write-Host "Step 1: Checking RSAT Active Directory Tools..." -ForegroundColor Yellow

try {
    $rsatAD = Get-WindowsCapability -Name "Rsat.ActiveDirectory.DS-LDS.Tools*" -Online
    
    if ($rsatAD.State -eq "Installed") {
        Write-Host "✓ RSAT Active Directory Tools already installed" -ForegroundColor Green
    } else {
        Write-Host "Installing RSAT Active Directory Tools..." -ForegroundColor Yellow
        Write-Host "This may take several minutes..." -ForegroundColor Gray
        
        Add-WindowsCapability -Online -Name "Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0"
        
        Write-Host "✓ RSAT Active Directory Tools installed successfully" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Error checking/installing RSAT: $_" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""

# Step 2: Import Active Directory Module
Write-Host "Step 2: Importing Active Directory Module..." -ForegroundColor Yellow

try {
    Import-Module ActiveDirectory -ErrorAction Stop
    Write-Host "✓ Active Directory module imported" -ForegroundColor Green
} catch {
    Write-Host "✗ Error importing AD module: $_" -ForegroundColor Red
    Write-Host "You may need to restart PowerShell after RSAT installation" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""

# Step 3: Extract Group Members
Write-Host "Step 3: Extracting tableau_home_office_all_type_a group members..." -ForegroundColor Yellow

$groupName = "tableau_home_office_all_type_a"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputFile = "${groupName}_${timestamp}.csv"

try {
    # Get AD group members
    Write-Host "Querying Active Directory..." -ForegroundColor Gray
    $members = Get-ADGroupMember -Identity $groupName -Recursive -ErrorAction Stop | 
        Where-Object {$_.objectClass -eq 'user'} |
        Sort-Object SamAccountName

    if ($members.Count -eq 0) {
        Write-Host "✗ No members found in $groupName" -ForegroundColor Red
        pause
        exit 1
    }

    Write-Host "✓ Found $($members.Count) members" -ForegroundColor Green
    Write-Host ""
    Write-Host "Retrieving detailed user information..." -ForegroundColor Yellow

    # Get detailed user information
    $userDetails = @()
    $counter = 0
    
    foreach ($member in $members) {
        $counter++
        Write-Progress -Activity "Processing users" -Status "$counter of $($members.Count)" -PercentComplete (($counter / $members.Count) * 100)
        
        try {
            $user = Get-ADUser -Identity $member.SamAccountName -Properties mail, displayName, title, department, employeeNumber, userPrincipalName
            
            $userDetails += [PSCustomObject]@{
                displayName = $user.displayName
                objectType = "user"
                mail = $user.mail
                userType = "Member"
                id = $user.ObjectGUID
                deviceId = ""
                userPrincipalName = $user.userPrincipalName
                isUser = $true
                isGroup = $false
                isGuest = $false
                title = $user.title
                department = $user.department
                employeeNumber = $user.employeeNumber
                samAccountName = $user.SamAccountName
            }
        } catch {
            Write-Host "Warning: Could not retrieve details for $($member.SamAccountName)" -ForegroundColor Yellow
        }
    }

    Write-Progress -Activity "Processing users" -Completed

    # Export to CSV
    $userDetails | Export-Csv -Path $outputFile -NoTypeInformation
    
    Write-Host ""
    Write-Host "✓ Successfully exported $($userDetails.Count) users" -ForegroundColor Green
    Write-Host "✓ File saved: $outputFile" -ForegroundColor Green
    
    # Display sample
    Write-Host ""
    Write-Host "Sample records (first 5):" -ForegroundColor Cyan
    $userDetails | Select-Object -First 5 | Format-Table displayName, mail, employeeNumber -AutoSize

} catch {
    Write-Host "✗ Error extracting group: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  - Group name might be incorrect" -ForegroundColor Gray
    Write-Host "  - You may not have permission to query this group" -ForegroundColor Gray
    Write-Host "  - You may need to be connected to VPN/corporate network" -ForegroundColor Gray
    pause
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update user_id_lookup.py to use: $outputFile" -ForegroundColor Gray
Write-Host "2. Run: python quick_lookup.py <email>" -ForegroundColor Gray
Write-Host ""

pause
