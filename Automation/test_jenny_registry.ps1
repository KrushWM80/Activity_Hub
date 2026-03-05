Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime] > $null

Write-Host "=== Windows.Media Voice Enumeration ===" -ForegroundColor Cyan
$synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer

Write-Host ("Default voice: {0}" -f $synth.Voice.DisplayName)
Write-Host ("AllVoices count: {0}" -f $synth.AllVoices.Count)
Write-Host ""

Write-Host "=== All Available Voices ===" -ForegroundColor Cyan
$voiceCount = 0
foreach ($voice in $synth.AllVoices) {
    $voiceCount++
    Write-Host ("  {0}. {1}" -f $voiceCount, $voice.DisplayName)
}

if ($voiceCount -eq 0) {
    Write-Host "  (No voices found in AllVoices collection)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Checking Speech Server Registry ===" -ForegroundColor Cyan
$regPath = "HKLM:\SOFTWARE\Microsoft\Speech Server\v11.0\Voices\Tokens"
if (Test-Path $regPath) {
    $tokens = Get-ChildItem $regPath -ErrorAction SilentlyContinue
    Write-Host ("Registry tokens found: {0}" -f @($tokens).Count)
    $tokens | ForEach-Object {
        Write-Host ("  - {0}" -f $_.PSChildName)
    }
} else {
    Write-Host "  Registry path does not exist"
}

Write-Host ""
Write-Host "=== Checking OneCore Tokens ===" -ForegroundColor Cyan
$oneCorePath = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
if (Test-Path $oneCorePath) {
    $tokens = Get-ChildItem $oneCorePath -ErrorAction SilentlyContinue
    Write-Host ("OneCore tokens found: {0}" -f @($tokens).Count)
    $tokens | ForEach-Object {
        Write-Host ("  - {0}" -f $_.PSChildName)
    }
} else {
    Write-Host "  OneCore registry path does not exist"
}
