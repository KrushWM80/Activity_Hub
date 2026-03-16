[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer
Write-Host "Available Voices:"
$tts.GetInstalledVoices() | ForEach-Object { 
    Write-Host "  - $($_.VoiceInfo.Name)"
}
