# Get HNMeeting2 Distribution List Members with Employee Details
# Exports: email, name, WIN, job code, title/role

Write-Host "`nExtracting HNMeeting2 Members with Employee Details...`n" -ForegroundColor Cyan

# Configuration
$groupEmail = "HNMeeting2@email.wal-mart.com"
$outputFile = "HNMeeting2_Members_with_Details_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv"

# Step 1: Get distribution list members
Write-Host "Step 1: Getting distribution list members..." -ForegroundColor Yellow

try {
    # Try Exchange Online first
    Import-Module ExchangeOnlineManagement -ErrorAction SilentlyContinue
    
    if (Get-Command Get-DistributionGroupMember -ErrorAction SilentlyContinue) {
        Write-Host "Using Exchange Online..." -ForegroundColor Green
        $members = Get-DistributionGroupMember -Identity $groupEmail -ResultSize Unlimited
        
        $memberData = $members | ForEach-Object {
            [PSCustomObject]@{
                Email = $_.PrimarySmtpAddress
                Name = $_.DisplayName
                RecipientType = $_.RecipientType
            }
        }
    }
    else {
        # Fallback to Active Directory
        Write-Host "Using Active Directory..." -ForegroundColor Green
        Import-Module ActiveDirectory -ErrorAction Stop
        
        $group = Get-ADGroup -Filter "mail -eq '$groupEmail'" -Properties member
        
        $memberData = $group.member | ForEach-Object {
            $user = Get-ADUser $_ -Properties mail, displayName
            [PSCustomObject]@{
                Email = $user.mail
                Name = $user.displayName
                RecipientType = "User"
            }
        } | Where-Object { $_.Email -ne $null }
    }
    
    Write-Host "Found $($memberData.Count) members" -ForegroundColor Green
    
} catch {
    Write-Host "Error getting distribution list members: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "`nFalling back to CSV export method..." -ForegroundColor Yellow
    Write-Host "Please export HNMeeting2 members to CSV manually from Outlook or Exchange Admin Center" -ForegroundColor Yellow
    exit 1
}

# Step 2: Enrich with employee data from Active Directory
Write-Host "`nStep 2: Enriching with employee data from Active Directory..." -ForegroundColor Yellow

$enrichedData = @()

foreach ($member in $memberData) {
    Write-Host "Processing: $($member.Email)" -ForegroundColor Gray
    
    try {
        # Get user from Active Directory
        $adUser = Get-ADUser -Filter "mail -eq '$($member.Email)'" -Properties `
            mail, displayName, employeeID, employeeNumber, title, department, company, manager
        
        if ($adUser) {
            $enrichedData += [PSCustomObject]@{
                Email = $member.Email
                Name = $member.Name
                WIN = $adUser.employeeID
                EmployeeNumber = $adUser.employeeNumber
                JobTitle = $adUser.title
                Department = $adUser.department
                Company = $adUser.company
                Manager = if ($adUser.manager) { 
                    (Get-ADUser $adUser.manager -Properties displayName).displayName 
                } else { "" }
                RecipientType = $member.RecipientType
            }
        }
        else {
            # User not found in AD, just add email
            $enrichedData += [PSCustomObject]@{
                Email = $member.Email
                Name = $member.Name
                WIN = "N/A"
                EmployeeNumber = "N/A"
                JobTitle = "N/A"
                Department = "N/A"
                Company = "N/A"
                Manager = "N/A"
                RecipientType = $member.RecipientType
            }
        }
    }
    catch {
        Write-Host "  Warning: Could not get details for $($member.Email)" -ForegroundColor Yellow
        $enrichedData += [PSCustomObject]@{
            Email = $member.Email
            Name = $member.Name
            WIN = "Error"
            EmployeeNumber = "Error"
            JobTitle = "Error"
            Department = "Error"
            Company = "Error"
            Manager = "Error"
            RecipientType = $member.RecipientType
        }
    }
}

# Step 3: Export to CSV
Write-Host "`nStep 3: Exporting to CSV..." -ForegroundColor Yellow

$enrichedData | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8

Write-Host "`nSUCCESS!" -ForegroundColor Green
Write-Host "Exported $($enrichedData.Count) members with details to:" -ForegroundColor Green
Write-Host "  $outputFile" -ForegroundColor Cyan
Write-Host "`nColumns included:" -ForegroundColor Yellow
Write-Host "  - Email" -ForegroundColor Gray
Write-Host "  - Name" -ForegroundColor Gray
Write-Host "  - WIN (Employee ID)" -ForegroundColor Gray
Write-Host "  - Employee Number" -ForegroundColor Gray
Write-Host "  - Job Title" -ForegroundColor Gray
Write-Host "  - Department" -ForegroundColor Gray
Write-Host "  - Company" -ForegroundColor Gray
Write-Host "  - Manager" -ForegroundColor Gray
Write-Host "  - Recipient Type" -ForegroundColor Gray

# Display summary statistics
Write-Host "`nSummary:" -ForegroundColor Yellow
$enrichedData | Group-Object Department | Sort-Object Count -Descending | Select-Object -First 10 | ForEach-Object {
    Write-Host "  $($_.Name): $($_.Count) members" -ForegroundColor Gray
}
