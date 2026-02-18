# Enrich HNMeeting2 Members with Workday Data
param(
    [string]$MemberFile = "archive\hnmeeting2_members.txt",
    [string]$WorkdayFile = "",
    [string]$OutputFile = "HNMeeting2_Members_Enriched_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv"
)

Write-Host "`nEnriching HNMeeting2 Members`n" -ForegroundColor Cyan

# Load member emails
if (-not (Test-Path $MemberFile)) {
    Write-Host "Error: Member file not found: $MemberFile" -ForegroundColor Red
    exit 1
}

$memberEmails = Get-Content $MemberFile | Where-Object { $_ -match '@' }
Write-Host "Found $($memberEmails.Count) email addresses" -ForegroundColor Green

# Check for Workday data
$workdayData = $null
if ($WorkdayFile -and (Test-Path $WorkdayFile)) {
    $workdayData = Import-Csv $WorkdayFile
    Write-Host "Loaded $($workdayData.Count) Workday records" -ForegroundColor Green
}

# Build enriched data
$enrichedData = @()

foreach ($email in $memberEmails) {
    $email = $email.Trim()
    
    $enrichedData += [PSCustomObject]@{
        Email = $email
        Name = ""
        WIN = ""
        JobCode = ""
        JobTitle = ""
        Department = ""
    }
}

# Export
$enrichedData | Export-Csv -Path $OutputFile -NoTypeInformation -Encoding UTF8

Write-Host "`nExported to: $OutputFile" -ForegroundColor Green
Write-Host "Total: $($enrichedData.Count) members" -ForegroundColor Cyan
