Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime] > $null

try {
    Write-Host "=== Windows.Media Voice Enumeration ===" -ForegroundColor Cyan
    $synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    
    Write-Host "Default voice: $($synth.Voice.DisplayName)"
    Write-Host "AllVoices count: $($synth.AllVoices.Count)"
    Write-Host ""
    
    # Try to enumerate and find Jenny
    $foundJenny = $false
    $voiceNames = @(
        "Microsoft Jenny(Natural) - English (United States)",
        "TTS_MS_en-US_JennyNeural_11.0",
        "Jenny"
    )
    
    foreach ($name in $voiceNames) {
        foreach ($voice in $synth.AllVoices) {
            if ($voice.DisplayName -eq $name -or $voice.Id -eq $name) {
                Write-Host "FOUND JENNY! DisplayName: $($voice.DisplayName), Id: $($voice.Id)" -ForegroundColor Green
                $foundJenny = $true
            }
        }
    }
    
    if (-not $foundJenny) {
        Write-Host "Jenny not found in AllVoices collection" -ForegroundColor Yellow
        Write-Host "Available voices:" -ForegroundColor Yellow
        $synth.AllVoices | ForEach-Object {
            Write-Host "  - $($_.DisplayName)"
        }
    }
    
    # Try to set each voice and check if it works
    Write-Host "`n=== Testing Direct Voice Synthesis ===" -ForegroundColor Cyan
    
    $testVoices = @(
        "Microsoft Jenny(Natural) - English (United States)",
        "Microsoft Mark - English (United States)",
        "Microsoft Zira - English (United States)"
    )
    
    foreach ($voiceName in $testVoices) {
        try {
            # Create a new SpeechSynthesizer for each test
            $synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
            
            # Try to find and set the voice by DisplayName
            $found = $false
            foreach ($voice in $synth.AllVoices) {
                if ($voice.DisplayName -like "*$voiceName*" -or $voiceName -like "*$($voice.DisplayName)*") {
                    $synth.Voice = $voice
                    Write-Host "✓ Set to: $($voice.DisplayName)" -ForegroundColor Green
                    $found = $true
                    break
                }
            }
            
            if (-not $found) {
                Write-Host "✗ Voice not found: $voiceName" -ForegroundColor Red
            }
        } catch {
            Write-Host "✗ Error with $voiceName : $_" -ForegroundColor Red
        }
    }
    
} catch {
    Write-Host ("Error: {0}" -f $_.Exception.Message) -ForegroundColor Red
}
