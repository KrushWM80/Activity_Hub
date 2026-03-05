# Enable Jenny Voice in SAPI5 through OneCore Bridge
# Requires: Admin elevation, reg file backup

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Jenny Voice OneCore → SAPI5 Bridge" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check admin elevation
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "❌ ERROR: This script requires Administrator privileges" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Admin privileges confirmed" -ForegroundColor Green
Write-Host ""

# Path definitions
$oneCorePath = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
$sapi5BasePath = "HKLM:\SOFTWARE\Microsoft\Speech\Voices\Tokens"
$backupDir = "$env:USERPROFILE\Documents\VSCode\Activity-Hub\Registry-Backups"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupFile = "$backupDir\Jenny-Registry-Backup-$timestamp.reg"

# Create backup directory
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
    Write-Host "📁 Created backup directory: $backupDir" -ForegroundColor Yellow
}

Write-Host "Step 1: Searching for Jenny voice in OneCore registry..." -ForegroundColor Cyan
Write-Host ""

# Find Jenny voice in OneCore
$jennyKey = $null
if (Test-Path $oneCorePath) {
    Get-ChildItem -Path $oneCorePath | ForEach-Object {
        if ($_.Name -match "Jenny") {
            $jennyKey = $_.PSChildName
        }
    }
}

if (-not $jennyKey) {
    Write-Host "❌ Jenny voice not found in OneCore registry:" -ForegroundColor Red
    Write-Host "   Path: $oneCorePath" -ForegroundColor Red
    Write-Host "" -ForegroundColor Red
    Write-Host "Checked for keys matching 'Jenny'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Found Jenny voice: $jennyKey" -ForegroundColor Green
Write-Host ""

Write-Host "Step 2: Backing up OneCore registry key..." -ForegroundColor Cyan
# Backup the OneCore key
$oneCoreFull = "$oneCorePath\$jennyKey"
cmd /c "reg export `"$oneCoreFull`" `"$backupFile`" /y" | Out-Null

if (Test-Path $backupFile) {
    $backupSize = (Get-Item $backupFile).Length
    Write-Host "✅ Registry backup saved:" -ForegroundColor Green
    Write-Host "   Path: $backupFile" -ForegroundColor Green
    Write-Host "   Size: $($backupSize) bytes" -ForegroundColor Green
}
Write-Host ""

Write-Host "Step 3: Reading registry key data..." -ForegroundColor Cyan
# Get all registry values
$regItem = Get-Item -Path $oneCoreFull
$regValues = @{}
$regItem.GetValueNames() | ForEach-Object {
    $value = $regItem.GetValue($_)
    $regValues[$_] = $value
}

Write-Host "✅ Registry values read: $($regValues.Count) properties" -ForegroundColor Green
Write-Host ""

Write-Host "Step 4: Creating SAPI5 registry entry..." -ForegroundColor Cyan

# Create new SAPI5-compatible key name
$sapi5Key = "TTS_MS_EN-US_Jenny_SAPI5"
$sapi5FullPath = "$sapi5BasePath\$sapi5Key"

# Ensure parent path exists
if (-not (Test-Path $sapi5BasePath)) {
    New-Item -Path $sapi5BasePath -Force | Out-Null
    Write-Host "📁 Created SAPI5 tokens registry path" -ForegroundColor Yellow
}

# Create the key
if (-not (Test-Path $sapi5FullPath)) {
    New-Item -Path $sapi5FullPath -Force | Out-Null
    Write-Host "✅ Created SAPI5 registry key: $sapi5Key" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 5: Updating registry values for SAPI5..." -ForegroundColor Cyan

# Copy and modify registry values
$regValues.Keys | ForEach-Object {
    $valueName = $_
    $value = $regValues[$valueName]
    
    # Update path references from OneCore to SAPI5
    if ($value -is [string]) {
        # Replace OneCore paths with SAPI5 paths in string values
        $newValue = $value -replace [regex]::Escape('Speech_OneCore'), 'Speech'
        $newValue = $newValue -replace [regex]::Escape($jennyKey), $sapi5Key
    } else {
        $newValue = $value
    }
    
    # Set the registry value
    Set-ItemProperty -Path $sapi5FullPath -Name $valueName -Value $newValue -Force
    Write-Host "  • $valueName" -ForegroundColor Gray
}

Write-Host "✅ Registry values imported and updated" -ForegroundColor Green
Write-Host ""

Write-Host "Step 6: Verifying SAPI5 entry..." -ForegroundColor Cyan

# Verify the SAPI5 key was created
$verifyItem = Get-Item -Path $sapi5FullPath -ErrorAction SilentlyContinue
if ($verifyItem) {
    $verifyCount = $verifyItem.GetValueNames().Count
    Write-Host "✅ Verified SAPI5 registry entry created" -ForegroundColor Green
    Write-Host "   Key: $sapi5Key" -ForegroundColor Green
    Write-Host "   Values: $verifyCount properties" -ForegroundColor Green
} else {
    Write-Host "❌ Verification failed - SAPI5 key not found" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Jenny Voice Bridge Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Close this PowerShell window" -ForegroundColor White
Write-Host "2. Open a NEW PowerShell window" -ForegroundColor White
Write-Host "3. Run: cd C:\Users\krush\Documents\VSCode\Activity-Hub" -ForegroundColor White
Write-Host "4. Run: .\check_sapi5_voices.ps1" -ForegroundColor White
Write-Host "5. Verify: Jenny should now appear in available voices" -ForegroundColor White
Write-Host ""
Write-Host "Registry backup location:" -ForegroundColor Yellow
Write-Host "   $backupFile" -ForegroundColor Yellow
Write-Host ""
