Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime] > $null
[Windows.Foundation.Metadata.ApiInformation, Windows.Foundation.Metadata, ContentType = WindowsRuntime] > $null

try {
    $synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    Write-Host "=== Windows.Media AllVoices Collection ===" -ForegroundColor Cyan
    
    $voiceCount = 0
    foreach ($voice in $synth.AllVoices) {
        $voiceCount++
        Write-Host ("Voice {0}:" -f $voiceCount) -ForegroundColor Yellow
        Write-Host ("  DisplayName: {0}" -f $voice.DisplayName)
        Write-Host ("  Id: {0}" -f $voice.Id)
        Write-Host ("  Gender: {0}" -f $voice.Gender)
        Write-Host ("  Language: {0}" -f $voice.Language)
        Write-Host ""
    }
    
    Write-Host ("Total: {0} voices found" -f $voiceCount) -ForegroundColor Cyan
    
    # Now try to set Jenny explicitly
    Write-Host "`n=== Testing Jenny voice directly ===" -ForegroundColor Cyan
    
    $voicesToTry = @(
        "Microsoft Jenny",
        "Jenny",
        "Microsoft Jenny(Natural) - English (United States)",
        "Microsoft Jenny Natural",
        "Jenny Natural",
        "MSTTS_V110_enUS_JennyF"
    )
    
    foreach ($voiceName in $voicesToTry) {
        try {
            $synth.Voice = [Windows.Media.SpeechSynthesis.VoiceInformation]::GetDefault()
            # Try to find the voice
            $found = $false
            foreach ($voice in $synth.AllVoices) {
                if ($voice.DisplayName -eq $voiceName -or $voice.Id -eq $voiceName) {
                    $synth.Voice = $voice
                    Write-Host ("Successfully set voice: {0}" -f $voiceName) -ForegroundColor Green
                    Write-Host ("  Using: {0}" -f $voice.DisplayName) -ForegroundColor Green
                    $found = $true
                    break
                }
            }
            if (-not $found) {
                Write-Host ("Voice not found: {0}" -f $voiceName) -ForegroundColor Gray
            }
        } catch {
            Write-Host ("Error setting voice '{0}': {1}" -f $voiceName, $_) -ForegroundColor Red
        }
    }
    
} catch {
    Write-Host ("Error initializing SpeechSynthesizer: {0}" -f $_) -ForegroundColor Red
}
