param([switch]$Force)

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "ERROR: Run PowerShell as Administrator" -ForegroundColor Red
    exit 1
}

Write-Host " " 
Write-Host "JENNY VOICE REGISTRATION SCRIPT" -ForegroundColor Cyan
Write-Host " "

$registryBasePath = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens\"
$jennyTokenName = "MSTTS_V110_enUS_JennyNeural"
$jennyRegistryPath = "$registryBasePath$jennyTokenName"
$jennyAppXPath = "C:\Program Files\WindowsApps\MicrosoftWindows.Voice.en-US.Jenny.2_1.0.2.0_x64__cw5n1h2txyewy"

Write-Host "[1/4] Verifying Jenny AppX package..." -ForegroundColor Yellow
if (Test-Path $jennyAppXPath) {
    Write-Host "OK: Jenny AppX found" -ForegroundColor Green
} else {
    Write-Host "ERROR: Jenny AppX NOT found" -ForegroundColor Red
    exit 1
}

if (Test-Path "$jennyAppXPath\MSTTSLocEnUS.dat") {
    Write-Host "OK: Jenny voice data found" -ForegroundColor Green
} else {
    Write-Host "ERROR: Jenny voice data NOT found" -ForegroundColor Red
    exit 1
}

Write-Host " "
Write-Host "[2/4] Checking registration status..." -ForegroundColor Yellow
if (Test-Path $jennyRegistryPath) {
    Write-Host "OK: Jenny already registered" -ForegroundColor Green
    if (-not $Force) {
        Write-Host "No action needed." -ForegroundColor Green
        exit 0
    }
    Write-Host "Force flag set - re-registering..." -ForegroundColor Yellow
    Remove-Item -Path $jennyRegistryPath -Force -ErrorAction SilentlyContinue
} else {
    Write-Host "OK: Ready to register Jenny" -ForegroundColor Green
}

Write-Host " "
Write-Host "[3/4] Creating registry entries..." -ForegroundColor Yellow
try {
    if (-not (Test-Path $jennyRegistryPath)) {
        New-Item -Path $jennyRegistryPath -Force | Out-Null
    }
    
    Set-ItemProperty -Path $jennyRegistryPath -Name "DisplayName" -Value "Microsoft Jenny Neural Voice" -ErrorAction Stop
    Set-ItemProperty -Path $jennyRegistryPath -Name "Gender" -Value "Female" -ErrorAction Stop
    Set-ItemProperty -Path $jennyRegistryPath -Name "Age" -Value "Adult" -ErrorAction Stop
    Set-ItemProperty -Path $jennyRegistryPath -Name "Language" -Value "409" -ErrorAction Stop
    Set-ItemProperty -Path $jennyRegistryPath -Name "LangDataPath" -Value $jennyAppXPath -ErrorAction Stop
    Set-ItemProperty -Path $jennyRegistryPath -Name "VoicePath" -Value "$jennyAppXPath\MSTTSLocEnUS.dat" -ErrorAction Stop
    Set-ItemProperty -Path $jennyRegistryPath -Name "Vendor" -Value "Microsoft" -ErrorAction Stop
    Set-ItemProperty -Path $jennyRegistryPath -Name "Version" -Value "11.0" -ErrorAction Stop
    Set-ItemProperty -Path $jennyRegistryPath -Name "CLSID" -Value "{D41D8369-020A-44DC-A82E-CE7657597D11}" -ErrorAction Stop
    Set-ItemProperty -Path $jennyRegistryPath -Name "RunOnce" -Value "" -ErrorAction Stop
    
    Write-Host "OK: Registry entries created" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to create registry entries: $_" -ForegroundColor Red
    exit 1
}

Write-Host " "
Write-Host "[4/4] Verifying registration..." -ForegroundColor Yellow
try {
    $test = Get-Item -Path $jennyRegistryPath -ErrorAction Stop
    Write-Host "OK: Jenny registered successfully" -ForegroundColor Green
    Write-Host " "
    Write-Host "Registered as: $jennyTokenName" -ForegroundColor Cyan
} catch {
    Write-Host "ERROR: Verification failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host " "
Write-Host "REGISTRATION COMPLETE" -ForegroundColor Green
Write-Host " "
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Restart Windows (required for registry reload)" -ForegroundColor Gray
Write-Host "  2. Update audio_pipeline.py to use Voice.JENNY" -ForegroundColor Gray
Write-Host "  3. Test voice synthesis" -ForegroundColor Gray
Write-Host " "

exit 0
