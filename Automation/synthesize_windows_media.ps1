# Windows.Media.SpeechSynthesis PowerShell Wrapper
# Synthesizes audio using modern Windows.Media API
# Parameters: VoiceName, InputText, OutputFile, Rate (0.5-2.0), Pitch (0.5-2.0)

param(
    [Parameter(Mandatory=$true)]
    [string]$VoiceName,
    
    [Parameter(Mandatory=$true)]
    [string]$InputText,
    
    [Parameter(Mandatory=$true)]
    [string]$OutputFile,
    
    [Parameter(Mandatory=$false)]
    [double]$Rate = 1.0,
    
    [Parameter(Mandatory=$false)]
    [double]$Pitch = 1.0
)

# ========== SETUP ==========
$ErrorActionPreference = "Stop"

# Ensure output directory exists
$OutputDir = Split-Path -Parent $OutputFile
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

# ========== WINDOWS.MEDIA API INITIALIZATION ==========

try {
    # Load required assemblies for WinRT
    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    
    # Load Windows.Foundation metadata for WinRT types
    [Windows.Foundation.Metadata.ApiInformation, Windows.Foundation.Metadata, ContentType = WindowsRuntime] | Out-Null
    
    # Load the actual speech synthesis type
    [Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime] | Out-Null
    
    Write-Verbose "Windows.Media assemblies loaded successfully"
} catch {
    Write-Error "Failed to load Windows.Media assemblies: $_"
    exit 1
}

# ========== VOICE SELECTION ==========

try {
    # Get all available voices
    $AllVoices = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
    
    if (-not $AllVoices) {
        Write-Error "No voices available in Windows.Media"
        exit 1
    }
    
    Write-Verbose "Found $($AllVoices.Count) total voices"
    
    # Normalize voice name
    $NormalizedVoiceName = $VoiceName.Trim().ToLower()
    
    # Find matching voice
    $SelectedVoice = $null
    foreach ($voice in $AllVoices) {
        if ($voice.DisplayName.ToLower() -like "*$NormalizedVoiceName*") {
            $SelectedVoice = $voice
            break
        }
    }
    
    if (-not $SelectedVoice) {
        Write-Error "Voice not found: '$VoiceName'"
        Write-Host "Available voices:"
        $AllVoices | ForEach-Object { Write-Host "  - $($_.DisplayName)" }
        exit 1
    }
    
    Write-Verbose "Selected voice: $($SelectedVoice.DisplayName)"
} catch {
    Write-Error "Voice selection error: $_"
    exit 1
}

# ========== SYNTHESIZER CREATION ==========

try {
    # Create speaking rate
    # Rate: 0.5 = half speed, 1.0 = normal, 2.0 = double speed
    $RateParam = [Windows.Media.SpeechSynthesis.ProsodyPitch]::new()
    
    # Create SSML string with prosody parameters
    $PitchPercent = [math]::Round(($Pitch - 1.0) * 100)
    $RatePercent = [math]::Round(($Rate - 1.0) * 100)
    
    $SSML = @"
<speak version="1.0" xml:lang="en-US">
    <voice name="$($SelectedVoice.DisplayName)">
        <prosody pitch="$PitchPercent%" rate="$RatePercent%">
            $InputText
        </prosody>
    </voice>
</speak>
"@
    
    Write-Verbose "SSML generated with pitch=$PitchPercent%, rate=$RatePercent%"
    
    # Create synthesizer
    $Synthesizer = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    $Synthesizer.Voice = $SelectedVoice
    
    Write-Verbose "Synthesizer created and voice set"
} catch {
    Write-Error "Synthesizer creation error: $_"
    exit 1
}

# ========== AUDIO OUTPUT SETUP ==========

try {
    # Create output stream for WAV file
    $OutputStream = [Windows.Storage.StorageFile]::GetFileFromPathAsync($OutputFile).GetAwaiter().GetResult()
    
    # If file exists, delete it
    if ($OutputStream) {
        $OutputStream.DeleteAsync().GetAwaiter().GetResult()
    }
    
    # Create new file
    $OutputFolder = [Windows.Storage.StorageFolder]::GetFolderFromPathAsync($OutputDir).GetAwaiter().GetResult()
    $FileName = Split-Path -Leaf $OutputFile
    $OutputStream = $OutputFolder.CreateFileAsync($FileName, [Windows.Storage.CreationCollisionOption]::ReplaceExisting).GetAwaiter().GetResult()
    
    Write-Verbose "Output stream created: $OutputFile"
} catch {
    Write-Error "Output stream creation error: $_"
    exit 1
}

# ========== SYNTHESIS ==========

try {
    # Create memory stream for audio
    $MemoryStream = New-Object System.IO.MemoryStream
    
    # Create random access stream for output
    $RandomAccessStream = [Windows.Storage.Streams.RandomAccessStream]::CreateFromStream($MemoryStream)
    
    # Synthesize speech to SSML
    Write-Host "Synthesizing speech..."
    $Task = $Synthesizer.SynthesizeSsmlToStreamAsync($SSML, $RandomAccessStream)
    $Task.GetAwaiter().GetResult() | Out-Null
    
    Write-Verbose "Speech synthesis completed"
    
    # Flush and close stream
    $RandomAccessStream.Dispose()
    
    # Write to output file
    $OutputStream = $OutputStream.OpenAsync([Windows.Storage.FileAccessMode]::ReadWrite).GetAwaiter().GetResult()
    $DataWriter = New-Object Windows.Storage.Streams.DataWriter $OutputStream
    $DataWriter.WriteBytes($MemoryStream.ToArray())
    $DataWriter.StoreAsync().GetAwaiter().GetResult() | Out-Null
    $DataWriter.DetachStream()
    $OutputStream.Dispose()
    $MemoryStream.Dispose()
    
    Write-Verbose "Audio written to file"
} catch {
    Write-Error "Synthesis error: $_"
    exit 1
}

# ========== VERIFICATION ==========

try {
    # Wait for file write
    Start-Sleep -Milliseconds 500
    
    # Verify file was created
    if (-not (Test-Path $OutputFile)) {
        Write-Error "Output file was not created"
        exit 1
    }
    
    $FileInfo = Get-Item $OutputFile
    $FileSizeMB = $FileInfo.Length / 1024 / 1024
    
    # Check file is not empty (WAV files are at least ~1KB)
    if ($FileInfo.Length -lt 1000) {
        Write-Error "Output file is too small ($($FileInfo.Length) bytes) - file might be corrupt"
        exit 1
    }
    
    Write-Host "✅ SUCCESS! Audio synthesized with '$($SelectedVoice.DisplayName)'"
    Write-Host "   File: $OutputFile"
    Write-Host "   Size: $([math]::Round($FileSizeMB, 2)) MB"
    Write-Host "   Rate: $([math]::Round($Rate, 2))x | Pitch: $([math]::Round($Pitch, 2))x"
    
    exit 0
} catch {
    Write-Error "Verification error: $_"
    exit 1
}
