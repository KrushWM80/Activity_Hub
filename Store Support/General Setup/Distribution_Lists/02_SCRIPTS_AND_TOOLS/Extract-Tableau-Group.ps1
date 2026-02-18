# Extract tableau_home_office_all_type_a AD Group Members
# This script extracts members from the Tableau AD group for comparison

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Tableau AD Group Member Extractor" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$groupName = "tableau_home_office_all_type_a"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputFile = "${groupName}_${timestamp}.csv"

Write-Host "Extracting members from: $groupName" -ForegroundColor Yellow
Write-Host ""

try {
    # Get AD group members
    $members = Get-ADGroupMember -Identity $groupName -Recursive | 
        Where-Object {$_.objectClass -eq 'user'} |
        Sort-Object SamAccountName

    if ($members.Count -eq 0) {
        Write-Host "No members found in $groupName" -ForegroundColor Red
        exit 1
    }

    Write-Host "Found $($members.Count) members" -ForegroundColor Green
    Write-Host "Retrieving user details..." -ForegroundColor Yellow

    # Get detailed user information
    $userDetails = @()
    $counter = 0
    
    foreach ($member in $members) {
        $counter++
        Write-Progress -Activity "Processing users" -Status "$counter of $($members.Count)" -PercentComplete (($counter / $members.Count) * 100)
        
        try {
            $user = Get-ADUser -Identity $member.SamAccountName -Properties mail, displayName, title, department, employeeNumber
            
            $userDetails += [PSCustomObject]@{
                group = $groupName
                username = $user.SamAccountName
                email = $user.mail
                display_name = $user.displayName
                title = $user.title
                department = $user.department
                employee_number = $user.employeeNumber
            }
        }
        catch {
            Write-Host "Warning: Could not retrieve details for $($member.SamAccountName)" -ForegroundColor Yellow
        }
    }

    Write-Progress -Activity "Processing users" -Completed

    # Export to CSV
    $userDetails | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "EXTRACTION COMPLETE" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Total members extracted: $($userDetails.Count)" -ForegroundColor Cyan
    Write-Host "Output file: $outputFile" -ForegroundColor Cyan
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "ERROR: $_" -ForegroundColor Red
    Write-Host ""
    exit 1
}
