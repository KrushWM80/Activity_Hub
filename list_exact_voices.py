"""Check exact voice names of newly installed voices."""

import subprocess

ps_script = r"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voices = $tts.GetInstalledVoices()

Write-Host "All installed voices:"
foreach ($v in $voices) {
    Write-Host "  '$($v.VoiceInfo.Name)'"
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
    capture_output=True,
    text=True,
    timeout=10
)

print(result.stdout)
