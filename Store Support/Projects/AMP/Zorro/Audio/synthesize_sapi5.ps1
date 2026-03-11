param(
    [string]$Text,
    [string]$OutputFile,
    [string]$VoiceName = "Microsoft David Desktop"
)

# Add System.Speech assembly
Add-Type -AssemblyName System.Speech

# Create synthesizer
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer

# Select voice
try {
    $synth.SelectVoice($VoiceName)
} catch {
    Write-Error "Voice not found: $VoiceName"
    exit 1
}

# Set volume
$synth.Volume = 100
$synth.Rate = 0  # Normal speed

# Output directly to WAV file (proper WAV format with headers)
$synth.SetOutputToWaveFile($OutputFile)

# Synthesize text
$synth.Speak($Text)

# Clean up
$synth.SetOutputToNull()

# Verify file creation
if (Test-Path $OutputFile) {
    $fileSize = (Get-Item $OutputFile).Length
    Write-Host "Synthesis successful"
    Write-Host "  File: $OutputFile"
    Write-Host "  Size: $fileSize bytes"
    exit 0
} else {
    Write-Error "Failed to create WAV file"
    exit 1
}
