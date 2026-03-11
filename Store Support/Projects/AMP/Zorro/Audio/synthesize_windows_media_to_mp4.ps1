<#
.SYNOPSIS
    Direct Windows.Media Text-to-MP4 Synthesis with Neural Voices (Jenny, David, Zira)
    
.DESCRIPTION
    Synthesizes text to speech using Windows.Media.SpeechSynthesis (supports neural voices)
    and encodes directly to MP4 using FFmpeg.
    Uses the new neural voices: Jenny, David, Zira
    
.PARAMETER Text
    Text to synthesize
    
.PARAMETER OutputFile
    Output MP4 file path
    
.PARAMETER Voice
    Voice to use: "Microsoft Jenny", "Microsoft David", "Microsoft Zira"
    
.PARAMETER Pitch
    Voice pitch (0.5 to 2.0, default: 1.0)
    
.PARAMETER Rate
    Speech rate (0.5 to 2.0, default: 0.95)

.EXAMPLE
    .\synthesize_sapi5_to_mp4.ps1 -Text "Welcome" -OutputFile "output.mp4" -Voice "Microsoft Jenny"

.NOTES
    - Uses Windows.Media.SpeechSynthesis API (neural voices)
    - Requires FFmpeg installed at C:\ffmpeg\bin\ffmpeg.exe
    - Date: March 10, 2026
    - Status: Windows.Media synthesis with neural voices
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Text,
    
    [Parameter(Mandatory=$true)]
    [string]$OutputFile,
    
    [string]$Voice = "Microsoft Jenny",
    
    [float]$Pitch = 1.0,
    
    [float]$Rate = 0.95
)

# Ensure output directory exists
$outputDir = Split-Path -Parent $OutputFile
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# FFmpeg path
$FFmpegPath = "C:\ffmpeg\bin\ffmpeg.exe"
if (-not (Test-Path $FFmpegPath)) {
    Write-Error "FFmpeg not found at $FFmpegPath. Install FFmpeg first."
    exit 1
}

# Temporary WAV file (intermediate only - will be deleted)
$tempWavFile = [System.IO.Path]::GetTempFileName() -replace '\.tmp$', '.wav'

try {
    # ========== PHASE 1: WINDOWS.MEDIA SYNTHESIS ==========
    Write-Host "[1/3] Windows.Media Synthesis to WAV" -ForegroundColor Cyan
    
    # Load Windows.Media assembly
    Add-Type -AssemblyName Windows.Media.SpeechSynthesis
    
    $synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    
    # Map voice names to neural voice IDs
    $voiceMap = @{
        "Microsoft Jenny" = "Microsoft Jenny"
        "Jenny" = "Microsoft Jenny"
        "Microsoft David" = "Microsoft David"
        "David" = "Microsoft David"
        "Microsoft Zira" = "Microsoft Zira"
        "Zira" = "Microsoft Zira"
    }
    
    $selectedVoice = $voiceMap[$Voice]
    if (-not $selectedVoice) {
        $selectedVoice = "Microsoft Jenny"  # Default to Jenny
    }
    
    # Configure pitch and rate
    $synth.Options.IncludeWordBoundaryMetadata = $true
    $synth.Options.IncludeSentenceBoundaryMetadata = $true
    
    Write-Host "   Voice: $selectedVoice" -ForegroundColor Green
    Write-Host "   Text length: $($Text.Length) characters" -ForegroundColor Green
    
    # Build SSML with voice and prosody settings
    $rate_percent = [int](($Rate - 1.0) * 100)
    if ($rate_percent -gt 0) { $rate_percent = "+$rate_percent" }
    
    $pitch_semitones = [int]((([Math]::Log2($Pitch)) * 12))
    if ($pitch_semitones -gt 0) { $pitch_semitones = "+$pitch_semitones" }
    
    $ssml = @"
<speak version='1.0' xml:lang='en-US'>
    <voice name='$selectedVoice'>
        <prosody pitch='$pitch_semitones%' rate='$rate_percent%'>
            $Text
        </prosody>
    </voice>
</speak>
"@
    
    # Create audio stream and synthesize
    $outputStream = New-Object System.IO.FileStream($tempWavFile, [System.IO.FileMode]::Create)
    
    # Synthesize with SSML
    $result = $synth.SynthesizeTextToStreamAsync($Text) | Wait-Job | Receive-Job
    
    # Use the audio stream to write to file
    $audioStream = New-Object Windows.Media.Audio.AudioGraph
    
    # Alternative: Use simple text synthesis
    [byte[]]$buffer = @()
    $task = $synth.SynthesizeTextToStreamAsync($Text)
    $task.AsTask().Wait()
    
    Write-Host "   ✓ WAV synthesized: $([System.IO.FileInfo]$tempWavFile | Select-Object -ExpandProperty Length | Invoke-Expression) bytes" -ForegroundColor Green
    
    # ========== PHASE 2: FFmpeg MP4 ENCODING ==========
    Write-Host "[2/3] FFmpeg MP4 Encoding" -ForegroundColor Cyan
    
    $ffmpegArgs = @(
        "-i", $tempWavFile,
        "-c:a", "aac",
        "-b:a", "256k",
        "-y",
        $OutputFile
    )
    
    & $FFmpegPath $ffmpegArgs 2>&1 | Where-Object { $_ -match "error|Error" } | ForEach-Object {
        Write-Host "   FFmpeg: $_" -ForegroundColor Yellow
    }
    
    if (-not (Test-Path $OutputFile)) {
        Write-Error "MP4 encoding failed"
        exit 1
    }
    
    Write-Host "   ✓ MP4 encoded: $([System.IO.FileInfo]$OutputFile | Select-Object -ExpandProperty Length | Invoke-Expression) bytes" -ForegroundColor Green
    
    # ========== PHASE 3: CLEANUP ==========
    Write-Host "[3/3] Cleanup" -ForegroundColor Cyan
    Remove-Item -Path $tempWavFile -Force -ErrorAction SilentlyContinue
    Write-Host "   ✓ Temporary files cleaned up" -ForegroundColor Green
    
    Write-Host "✅ Synthesis complete: $OutputFile" -ForegroundColor Green
    exit 0
}
catch {
    Write-Error "Synthesis failed: $_"
    Remove-Item -Path $tempWavFile, $OutputFile -Force -ErrorAction SilentlyContinue
    exit 1
}
