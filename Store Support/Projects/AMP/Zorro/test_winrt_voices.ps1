[Windows.Media.SpeechSynthesis.SpeechSynthesizer,Windows.Media.SpeechSynthesis,ContentType=WindowsRuntime] | Out-Null
$voices = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
Write-Host "Total WinRT voices: $($voices.Count)"
foreach ($v in $voices) {
    $marker = ""
    if ($v.DisplayName -like "*Jenny*") { $marker = " <<<< JENNY!" }
    Write-Host "  $($v.DisplayName) | $($v.Gender) | $($v.Language) | $($v.Id)$marker"
}
