Write-Host "===== VOICE DIAGNOSTIC REPORT =====" -ForegroundColor Cyan
Write-Host ""

# --- 1) SAPI5 voices (System.Speech) ---
Write-Host "--- SAPI5 Voices (System.Speech) ---" -ForegroundColor Yellow
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.GetInstalledVoices() | ForEach-Object {
    $v = $_.VoiceInfo
    Write-Host "  Name='$($v.Name)' | Culture=$($v.Culture) | Gender=$($v.Gender) | Age=$($v.Age)"
}
$synth.Dispose()

# --- 2) OneCore registry voices ---
Write-Host ""
Write-Host "--- OneCore Registry Voices (Speech_OneCore) ---" -ForegroundColor Yellow
$tokenPath = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
if (Test-Path $tokenPath) {
    Get-ChildItem $tokenPath | ForEach-Object {
        $name = (Get-ItemProperty $_.PSPath -ErrorAction SilentlyContinue).'(default)'
        $langDataPath = Join-Path $_.PSPath "Attributes"
        $gender = (Get-ItemProperty $langDataPath -ErrorAction SilentlyContinue).Gender
        $lang = (Get-ItemProperty $langDataPath -ErrorAction SilentlyContinue).Language
        Write-Host "  Token=$($_.PSChildName) | Name=$name | Gender=$gender | Lang=$lang"
    }
} else {
    Write-Host "  (No OneCore voices found)"
}

# --- 3) Windows.Media.SpeechSynthesis (WinRT/UWP) ---
Write-Host ""
Write-Host "--- Windows.Media.SpeechSynthesis (WinRT) ---" -ForegroundColor Yellow
try {
    [Windows.Media.SpeechSynthesis.SpeechSynthesizer,Windows.Media.SpeechSynthesis,ContentType=WindowsRuntime] | Out-Null
    $allVoices = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
    Write-Host "  Found $($allVoices.Count) WinRT voices:"
    foreach ($voice in $allVoices) {
        Write-Host "  DisplayName='$($voice.DisplayName)' | Id='$($voice.Id)' | Gender=$($voice.Gender) | Lang=$($voice.Language)"
    }
} catch {
    Write-Host "  WinRT approach failed: $($_.Exception.Message)" -ForegroundColor Red
}

# --- 4) COM SAPI default + all ---
Write-Host ""
Write-Host "--- COM SAPI.SpVoice ---" -ForegroundColor Yellow
try {
    $spVoice = New-Object -ComObject SAPI.SpVoice
    Write-Host "  Default: $($spVoice.Voice.GetDescription())"
    $allComVoices = $spVoice.GetVoices()
    for ($i = 0; $i -lt $allComVoices.Count; $i++) {
        $v = $allComVoices.Item($i)
        Write-Host "  [$i] $($v.GetDescription()) | ID=$($v.Id)"
    }
} catch {
    Write-Host "  COM SAPI failed: $($_.Exception.Message)" -ForegroundColor Red
}

# --- 5) COM SAPI OneCore category ---
Write-Host ""
Write-Host "--- COM SAPI OneCore Category ---" -ForegroundColor Yellow
try {
    $cat = New-Object -ComObject SAPI.SpObjectTokenCategory
    $cat.SetId("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices")
    $oneVoices = $cat.EnumerateTokens()
    Write-Host "  OneCore voice count: $($oneVoices.Count)"
    for ($i = 0; $i -lt $oneVoices.Count; $i++) {
        $v = $oneVoices.Item($i)
        Write-Host "  [$i] $($v.GetDescription()) | ID=$($v.Id)"
    }
} catch {
    Write-Host "  OneCore COM failed: $($_.Exception.Message)" -ForegroundColor Red
}

# --- 6) Registry dump of OneCore token names ---
Write-Host ""
Write-Host "--- OneCore Token Registry Keys ---" -ForegroundColor Yellow
$regPath = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
if (Test-Path $regPath) {
    Get-ChildItem $regPath | ForEach-Object {
        Write-Host "  $($_.PSChildName)"
    }
}

Write-Host ""
Write-Host "===== END DIAGNOSTIC =====" -ForegroundColor Cyan
