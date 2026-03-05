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
$synth.SelectVoice($VoiceName)

# Set volume
$synth.Volume = 100

# Create file and audio stream
$stream = New-Object System.IO.FileStream($OutputFile, [System.IO.FileMode]::Create)

# Set output to file
$synth.SetOutputToAudioStream($stream, [System.Speech.AudioFormat.SpeechAudioFormatInfo]::new([System.Speech.AudioFormat.EncodingFormat]::Pcm, 16000, 16, 1, 32000, 2, $null))

# Synthesize text
$synth.Speak($Text)

# Clean up
$synth.SetOutputToNull()
$stream.Close()
$stream.Dispose()

Write-Host "Synthesis successful: $OutputFile"
