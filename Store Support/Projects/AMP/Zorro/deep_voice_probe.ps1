# Deep investigation of Windows speech voice discovery
# Test various methods to find Jenny neural voice

Write-Host "=== Method 1: WinRT AllVoices ===" -ForegroundColor Cyan
[Windows.Media.SpeechSynthesis.SpeechSynthesizer,Windows.Media.SpeechSynthesis,ContentType=WindowsRuntime] | Out-Null
$allVoices = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
Write-Host "Count: $($allVoices.Count)"
foreach ($v in $allVoices) {
    Write-Host "  $($v.DisplayName) | Gender=$($v.Gender) | Lang=$($v.Language)"
}

Write-Host ""
Write-Host "=== Method 2: Default Voice ===" -ForegroundColor Cyan
$synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
$dv = $synth.Voice
Write-Host "Default: $($dv.DisplayName) | $($dv.Id)"
$synth.Dispose()

Write-Host ""
Write-Host "=== Method 3: App Extension Catalog ===" -ForegroundColor Cyan
try {
    [Windows.ApplicationModel.AppExtensions.AppExtensionCatalog,Windows.ApplicationModel,ContentType=WindowsRuntime] | Out-Null
    $catalog = [Windows.ApplicationModel.AppExtensions.AppExtensionCatalog]::Open("com.microsoft.voice.model.1")
    
    # Need async pattern
    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    $asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { 
        $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' 
    })[0]
    
    $findOp = $catalog.FindAllAsync()
    $findTask = $asTask.MakeGenericMethod([System.Collections.Generic.IReadOnlyList[Windows.ApplicationModel.AppExtensions.AppExtension]]).Invoke($null, @($findOp))
    $findTask.Wait()
    $extensions = $findTask.Result
    
    Write-Host "Found $($extensions.Count) voice extensions:"
    foreach ($ext in $extensions) {
        Write-Host "  Name=$($ext.DisplayName) | AppInfo=$($ext.AppInfo.DisplayInfo.DisplayName) | Id=$($ext.Id)"
        
        # Get properties
        $propsOp = $ext.GetExtensionPropertiesAsync()
        $propsTask = $asTask.MakeGenericMethod([Windows.Foundation.Collections.IPropertySet]).Invoke($null, @($propsOp))
        $propsTask.Wait()
        $props = $propsTask.Result
        foreach ($key in $props.Keys) {
            Write-Host "    $key = $($props[$key])"
        }
    }
} catch {
    Write-Host "  App Extension method failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  $($_.Exception.InnerException)" -ForegroundColor DarkRed
}

Write-Host ""
Write-Host "=== Method 4: Check SpeechSynthesizer with SSML voice selection ===" -ForegroundColor Cyan
try {
    $synth2 = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    
    # Try SSML with Jenny voice name
    $ssml = @"
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
    <voice name='Microsoft Jenny(Natural) - English (United States)'>Hello, this is a test of the Jenny neural voice.</voice>
</speak>
"@
    
    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    $asTask2 = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { 
        $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' 
    })[0]
    
    $synthOp = $synth2.SynthesizeSsmlToStreamAsync($ssml)
    $synthTask = $asTask2.MakeGenericMethod([Windows.Media.SpeechSynthesis.SpeechSynthesisStream]).Invoke($null, @($synthOp))
    $synthTask.Wait([TimeSpan]::FromSeconds(30))
    
    if ($synthTask.IsCompleted) {
        $stream = $synthTask.Result
        Write-Host "  SSML synthesis succeeded! Stream size: $($stream.Size) bytes"
    }
    $synth2.Dispose()
} catch {
    Write-Host "  SSML test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Method 5: Try selecting voice by matching ===" -ForegroundColor Cyan
try {
    $synth3 = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    $voices = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
    foreach ($v in $voices) {
        Write-Host "  Available for selection: $($v.DisplayName) - Gender=$($v.Gender)"
    }
    
    # Try to find a Female voice
    $femaleVoice = $voices | Where-Object { $_.Gender -eq 'Female' } | Select-Object -First 1
    if ($femaleVoice) {
        $synth3.Voice = $femaleVoice
        Write-Host "  Selected female voice: $($synth3.Voice.DisplayName)"
    }
    $synth3.Dispose()
} catch {
    Write-Host "  Voice selection test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
