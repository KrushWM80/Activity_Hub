# Fix Jenny Neural Voice Registry Entry
# This script recreates the OneCore registry entry with correct structure
# matching the official Tokens.xml specification

$ErrorActionPreference = "Stop"

$tokenBase = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
$tokenName = "MSTTS_V110_enUS_JennyNeural"
$tokenPath = "$tokenBase\$tokenName"
$attrPath  = "$tokenPath\Attributes"

$installDir = "C:\Program Files\WindowsApps\MicrosoftWindows.Voice.en-US.Jenny.2_1.0.2.0_x64__cw5n1h2txyewy"
$displayName = "Microsoft Jenny(Natural) - English (United States)"
$clsid = "{a12bdfa1-c3a1-48ea-8e3f-27945e16cf7e}"

Write-Host "=== Fixing Jenny Neural Voice Registry ===" -ForegroundColor Cyan

# Step 1: Remove old broken entry
if (Test-Path $tokenPath) {
    Write-Host "Removing broken registry entry..." -ForegroundColor Yellow
    Remove-Item -Path $tokenPath -Recurse -Force
    Write-Host "  Old entry removed." -ForegroundColor Green
}

# Step 2: Create token key with correct values
Write-Host "Creating new registry entry..." -ForegroundColor Yellow
New-Item -Path $tokenPath -Force | Out-Null

# (Default) value
Set-ItemProperty -Path $tokenPath -Name "(Default)" -Value $displayName
# 409 = English (US) locale ID
Set-ItemProperty -Path $tokenPath -Name "409" -Value $displayName
# CLSID - Neural TTS engine
Set-ItemProperty -Path $tokenPath -Name "CLSID" -Value $clsid
# LangDataPath - points to the main TTS data file
Set-ItemProperty -Path $tokenPath -Name "LangDataPath" -Value "$installDir\MSTTSLocEnUS.dat"
# VoicePath - points to the 1033 locale directory
Set-ItemProperty -Path $tokenPath -Name "VoicePath" -Value "$installDir\1033"

Write-Host "  Token key created." -ForegroundColor Green

# Step 3: Create Attributes subkey
Write-Host "Creating Attributes subkey..." -ForegroundColor Yellow
New-Item -Path $attrPath -Force | Out-Null

Set-ItemProperty -Path $attrPath -Name "Age" -Value "Adult"
Set-ItemProperty -Path $attrPath -Name "AudioFormats" -Value "18"
Set-ItemProperty -Path $attrPath -Name "Gender" -Value "Female"
Set-ItemProperty -Path $attrPath -Name "Language" -Value "409"
Set-ItemProperty -Path $attrPath -Name "Name" -Value "Microsoft Jenny(Natural) - English (United States)"
Set-ItemProperty -Path $attrPath -Name "Vendor" -Value "Microsoft"
Set-ItemProperty -Path $attrPath -Name "Version" -Value "11.0"
Set-ItemProperty -Path $attrPath -Name "VoiceType" -Value "Neural"
Set-ItemProperty -Path $attrPath -Name "LicenseVersion" -Value "1"

Write-Host "  Attributes subkey created." -ForegroundColor Green

# Step 4: Verify
Write-Host ""
Write-Host "=== Verification ===" -ForegroundColor Cyan
Write-Host "Registry entry:" -ForegroundColor Yellow
reg query "HKLM\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens\$tokenName" /s

Write-Host ""
Write-Host "=== Testing WinRT Voice Enumeration ===" -ForegroundColor Cyan
try {
    [Windows.Media.SpeechSynthesis.SpeechSynthesizer,Windows.Media.SpeechSynthesis,ContentType=WindowsRuntime] | Out-Null
    $allVoices = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
    Write-Host "WinRT voices found: $($allVoices.Count)" -ForegroundColor Green
    foreach ($voice in $allVoices) {
        $marker = ""
        if ($voice.DisplayName -like "*Jenny*") { $marker = " <<<< JENNY FOUND!" }
        Write-Host "  DisplayName='$($voice.DisplayName)' | Id='$($voice.Id)' | Gender=$($voice.Gender)$marker"
    }
} catch {
    Write-Host "  WinRT test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
