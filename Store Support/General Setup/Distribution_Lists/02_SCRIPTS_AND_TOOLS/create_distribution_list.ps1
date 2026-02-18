<#
.SYNOPSIS
    Create a Microsoft 365 Distribution List from an email list file
    
.DESCRIPTION
    Reads emails from a text file and creates a Distribution List in M365,
    then adds all members to it.
    
.EXAMPLE
    .\create_distribution_list.ps1 -EmailListFile "email_list_20251215_153336.txt" -GroupName "OPS_Support_Market" -DisplayName "OPS Support Market Team"
    
.NOTES
    Requires: Exchange Online PowerShell module
    Install: Install-Module -Name ExchangeOnlineManagement -Force
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$EmailListFile,
    
    [Parameter(Mandatory=$true)]
    [string]$GroupName,
    
    [Parameter(Mandatory=$false)]
    [string]$DisplayName = $GroupName,
    
    [Parameter(Mandatory=$false)]
    [string]$Description = "Automated distribution list created from AD group"
)

function Main {
    Write-Host "`n" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "Microsoft 365 Distribution List Creator" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "`n"
    
    # Check if file exists
    if (-not (Test-Path $EmailListFile)) {
        Write-Host "[X] Error: Email list file not found: $EmailListFile" -ForegroundColor Red
        exit 1
    }
    
    # Read emails
    $emails = @(Get-Content $EmailListFile | Where-Object { $_.Trim() -ne '' })
    Write-Host "[+] Loaded $($emails.Count) email addresses from $EmailListFile" -ForegroundColor Green
    
    # Check connection
    try {
        $connectionTest = Get-ExoMailbox -ResultSize 1 -ErrorAction Stop
        Write-Host "[+] Connected to Exchange Online" -ForegroundColor Green
    }
    catch {
        Write-Host "[X] Not connected to Exchange Online. Run: Connect-ExchangeOnline" -ForegroundColor Red
        exit 1
    }
    
    # Check if group already exists
    $existing = $null
    try {
        $existing = Get-DistributionGroup -Identity $GroupName -ErrorAction SilentlyContinue
    }
    catch { }
    
    if ($existing) {
        Write-Host "[?] Distribution group '$GroupName' already exists" -ForegroundColor Yellow
        Write-Host "    Do you want to update it with new members? (Y/N)"
        $response = Read-Host
        if ($response -ne 'Y') {
            Write-Host "[*] Cancelled" -ForegroundColor Yellow
            exit 0
        }
    }
    else {
        # Create new group
        Write-Host "[*] Creating distribution list: $GroupName" -ForegroundColor Cyan
        try {
            New-DistributionGroup `
                -Name $GroupName `
                -DisplayName $DisplayName `
                -Type Distribution `
                -ErrorAction Stop
            Write-Host "[+] Distribution list created successfully" -ForegroundColor Green
        }
        catch {
            Write-Host "[X] Error creating distribution list: $_" -ForegroundColor Red
            exit 1
        }
    }
    
    # Add members
    Write-Host "`n[*] Adding members to $GroupName..." -ForegroundColor Cyan
    $successCount = 0
    $failCount = 0
    $skippedCount = 0
    
    foreach ($i = 0; $i -lt $emails.Count; $i++) {
        $email = $emails[$i].Trim()
        
        if ($i % 100 -eq 0) {
            Write-Host "    Progress: $i/$($emails.Count)" -ForegroundColor Gray
        }
        
        if ($email -eq '') {
            $skippedCount++
            continue
        }
        
        try {
            Add-DistributionGroupMember -Identity $GroupName -Member $email -ErrorAction Stop -WarningAction SilentlyContinue
            $successCount++
        }
        catch {
            if ($_ -match "already a member") {
                $skippedCount++
            }
            else {
                Write-Host "    [!] Failed to add $email : $_" -ForegroundColor Yellow
                $failCount++
            }
        }
    }
    
    # Summary
    Write-Host "`n" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "COMPLETION SUMMARY" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "`n"
    Write-Host "Distribution List: $DisplayName" -ForegroundColor Green
    Write-Host "  Address: $GroupName@walmart.com" -ForegroundColor Green
    Write-Host "`n"
    Write-Host "Members Added: $successCount" -ForegroundColor Green
    Write-Host "Already Members: $skippedCount" -ForegroundColor Yellow
    Write-Host "Failed: $failCount" -ForegroundColor $(if ($failCount -eq 0) { 'Green' } else { 'Red' })
    Write-Host "Total Processed: $($emails.Count)" -ForegroundColor Cyan
    Write-Host "`n"
}

Main