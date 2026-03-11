Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer

Write-Host "SAPI5 Voices Available:" -ForegroundColor Cyan
$voices = $synth.GetInstalledVoices()
$voices | ForEach-Object {
    Write-Host "  - Name: '$($_.VoiceInfo.Name)'" -ForegroundColor Yellow
}

Write-Host "`nRegistry Check for Jenny:" -ForegroundColor Cyan
reg query "HKLM\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens" 2>$null | findstr /i "MSTTS"

Write-Host "`nAttempting to select each voice and verify:" -ForegroundColor Cyan
@("Microsoft Jenny", "Microsoft David Desktop", "Microsoft Zira Desktop", "MSTTS_V110_enUS_JennyNeural") | ForEach-Object {
    try {
        $synth.SelectVoice($_)
        $current = $synth.Voice.Name
        Write-Host "  ✓ Selected: '$_' -> Actual: '$current'" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Failed: '$_'" -ForegroundColor Red
    }
}
