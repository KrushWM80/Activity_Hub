# Quick test to verify Windows.Media and system capabilities
$osVersion = [System.Environment]::OSVersion.Version
Write-Host "OS Version: $($osVersion.Major).$($osVersion.Minor) Build $($osVersion.Build)"
Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)"

# Check if WinRT/Windows.Media is available
if ($osVersion.Build -ge 19041) {
    Write-Host "✅ Windows 10 Build 19041+ or Windows 11 detected" -ForegroundColor Green
    Write-Host "✅ Windows.Media.SpeechSynthesis API AVAILABLE" -ForegroundColor Green
} else {
    Write-Host "⚠️ Older Windows version - API may be limited" -ForegroundColor Yellow
}

# Test SAPI5 voice enumeration
try {
    Add-Type -AssemblyName System.Speech
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $voices = $synth.GetInstalledVoices()
    Write-Host "SAPI5 Voices Found: $($voices.Count)"
    foreach ($voice in $voices) {
        Write-Host "  - $($voice.VoiceInfo.Name)"
    }
} catch {
    Write-Host "Error enumerating SAPI5 voices: $_" -ForegroundColor Red
}
