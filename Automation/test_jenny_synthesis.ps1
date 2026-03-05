Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime] > $null

try {
    Write-Host "=== Creating SpeechSynthesizer ===" -ForegroundColor Cyan
    $synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    
    Write-Host "Default Voice: $($synth.Voice.DisplayName)" -ForegroundColor Green
    Write-Host "Total voices in AllVoices: $($synth.AllVoices.Count)"
    
    # List all voices with FullName (might be different from DisplayName)
    Write-Host "`n=== Attempting direct AllVoices enumeration ===" -ForegroundColor Cyan
    $voiceList = @()
    $synth.AllVoices | ForEach-Object {
        $voiceList += $_
        Write-Host ("Voice: {0}" -f $_.DisplayName)
    }
    Write-Host ("Total enumerated: {0}" -f $voiceList.Count)
    
    # Try to access voice properties through reflection
    Write-Host "`n=== Checking SpeechSynthesizer type info ===" -ForegroundColor Cyan
    $synthType = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]
    $props = $synthType.GetProperties([System.Reflection.BindingFlags]::Public) | Select-Object -ExpandProperty Name
    Write-Host "Public properties: $(($props -join ', '))"
    
    # Check if there's a method to get voices by name
    $methods = $synthType.GetMethods([System.Reflection.BindingFlags]::Public) | Select-Object -ExpandProperty Name
    Write-Host "Methods with 'Voice' in name: $(($methods | Where-Object { $_ -like '*Voice*' } | Select-Object -Unique) -join ', ')"
    
} catch {
    Write-Host ("Error: {0}" -f $_.Exception.Message) -ForegroundColor Red
    Write-Host ("Full error: {0}" -f $_)
}
