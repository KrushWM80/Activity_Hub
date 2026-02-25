"""Check all available SAPI5 voices on the system."""

import subprocess

ps_script = r"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null

$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voices = $synthesizer.GetInstalledVoices()

Write-Host "=========================================="
Write-Host "ALL AVAILABLE SAPI5 VOICES"
Write-Host "=========================================="
Write-Host ""
Write-Host "Total: $($voices.Count) voices found"
Write-Host ""

foreach ($voice in $voices) {
    $info = $voice.VoiceInfo
    Write-Host "Name: $($info.Name)"
    Write-Host "Gender: $($info.Gender), Culture: $($info.Culture)"
    Write-Host ""
}

Write-Host "=========================================="
Write-Host "VOICE AVAILABILITY CHECK"
Write-Host "=========================================="

$voiceNames = @("Aria", "Jenny", "Guy", "David Desktop", "Hazel Desktop", "Zira Desktop")

foreach ($searchName in $voiceNames) {
    $found = 0
    foreach ($voice in $voices) {
        if ($voice.VoiceInfo.Name -like "*$searchName*") {
            Write-Host "FOUND: $($voice.VoiceInfo.Name)"
            $found = 1
        }
    }
    if ($found -eq 0) {
        Write-Host "NOT FOUND: *$searchName*"
    }
}
"""

ps_file = "check_voices.ps1"
with open(ps_file, 'w', encoding='utf-8') as f:
    f.write(ps_script)

try:
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    print(result.stdout)
        
finally:
    import os
    try:
        os.remove(ps_file)
    except:
        pass
