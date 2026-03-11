Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
Write-Host "Available SAPI5 Voices:" -ForegroundColor Cyan
$voices = $synth.GetInstalledVoices()
$voices | ForEach-Object {
    Write-Host "Name: $($_.VoiceInfo.Name)" -ForegroundColor Yellow
    Write-Host "Culture: $($_.VoiceInfo.Culture)" -ForegroundColor Gray
    Write-Host "Gender: $($_.VoiceInfo.Gender)" -ForegroundColor Gray
    Write-Host "---"
}
Write-Host "Total voices installed: $($voices.Count)" -ForegroundColor Green
