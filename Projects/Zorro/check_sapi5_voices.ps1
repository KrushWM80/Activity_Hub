Add-Type -AssemblyName System.Speech
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer

Write-Host "SAPI5 Voices Available:" -ForegroundColor Cyan
Write-Host "========================"

$voices = $tts.GetInstalledVoices()
foreach ($voice in $voices) {
    $name = $voice.VoiceInfo.Name
    Write-Host "  • $name"
}

Write-Host ""
Write-Host "Total: $($voices.Count) voices" -ForegroundColor Green

# Check for Jenny specifically
$jennyFound = $false
foreach ($voice in $voices) {
    if ($voice.VoiceInfo.Name -like "*Jenny*") {
        $jennyFound = $true
    }
}

Write-Host ""
if ($jennyFound) {
    Write-Host "✅ JENNY IS AVAILABLE IN SAPI5" -ForegroundColor Green
} else {
    Write-Host "❌ JENNY IS NOT AVAILABLE IN SAPI5" -ForegroundColor Red
}
