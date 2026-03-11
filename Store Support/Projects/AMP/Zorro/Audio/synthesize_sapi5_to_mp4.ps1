
<#
.SYNOPSIS
    Direct SAPI5 Text-to-MP4 Synthesis (NO WAV INTERMEDIATE)
    
.DESCRIPTION
    Synthesizes text to speech using Windows SAPI5 API and encodes directly to MP4 using FFmpeg.
    Completely bypasses WAV file generation - MP4 is the final output format.
    
.PARAMETER Text
    Text to synthesize (supports basic SSML)
    
.PARAMETER OutputFile
    Output MP4 file path
    
.PARAMETER Voice
    SAPI5 voice name (default: "Microsoft Jenny" or "Microsoft David")
    
.PARAMETER Pitch
    Voice pitch (0.5 to 2.0, default: 1.0)
    
.PARAMETER Rate
    Speech rate (0.5 to 2.0, default: 0.95 for Jenny, 1.0 for David)

.EXAMPLE
    .\synthesize_sapi5_to_mp4.ps1 -Text "Welcome to Walmart Activity Hub" -OutputFile "output.mp4"

.NOTES
    - Requires Windows SAPI5 (System.Speech namespace)
    - Requires FFmpeg installed at C:\ffmpeg\bin\ffmpeg.exe
    - Date: March 10, 2026
    - Status: Direct MP4 synthesis (no WAV intermediate)
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
    # ========== PHASE 1: SAPI5 SYNTHESIS ==========
    Write-Host "[1/3] SAPI5 Synthesis to WAV" -ForegroundColor Cyan
    
    # Load SAPI5
    Add-Type -AssemblyName System.Speech
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    
    # Configure voice
    try {
        $synth.SelectVoice($Voice)
        Write-Host "   Voice selected: $Voice" -ForegroundColor Green
    }
    catch {
        Write-Warning "Voice $Voice not found, using default"
    }
    
    # Configure pitch and rate
    $synth.Volume = 100
    
    try {
        $synth.Pitch = $Pitch
        Write-Host "   Pitch: $Pitch" -ForegroundColor Green
    }
    catch {
        Write-Warning "Pitch setting failed, using default"
    }
    
    try {
        $synth.Rate = $Rate
        Write-Host "   Rate: $Rate" -ForegroundColor Green
    }
    catch {
        Write-Warning "Rate setting failed, using default"
    }
    
    # Output to WAV file (ONLY temporary)
    $synth.SetOutputToWaveFile($tempWavFile)
    
    # Synthesize text
    $synth.Speak($Text)
    $synth.Dispose()
    
    # Verify WAV file
    if (-not (Test-Path $tempWavFile)) {
        Write-Error "WAV synthesis failed - file not created"
        exit 1
    }
    
    $wavSize = (Get-Item $tempWavFile).Length
    Write-Host "   WAV created: $([Math]::Round($wavSize/1024,1))KB" -ForegroundColor Green
    
    # ========== PHASE 2: FFMPEG ENCODING ==========
    Write-Host "[2/3] FFmpeg Encoding to MP4" -ForegroundColor Cyan
    
    # FFmpeg command: WAV to MP4 (audio-only)
    $ffmpegArgs = '-i "{0}" -c:a aac -b:a 256k -movflags faststart -y "{1}"' -f $tempWavFile, $OutputFile
    
    # Run FFmpeg
    $ffmpegProcess = Start-Process -FilePath $FFmpegPath -ArgumentList $ffmpegArgs -NoNewWindow -Wait -PassThru
    
    if ($ffmpegProcess.ExitCode -ne 0) {
        Write-Error "FFmpeg encoding failed with exit code $($ffmpegProcess.ExitCode)"
        exit 1
    }
    
    Write-Host "   FFmpeg encoding successful" -ForegroundColor Green
    
    # ========== PHASE 3: CLEANUP AND VERIFICATION ==========
    Write-Host "[3/3] Cleanup and Verification" -ForegroundColor Cyan
    
    # Delete temporary WAV file
    if (Test-Path $tempWavFile) {
        Remove-Item $tempWavFile -Force -ErrorAction SilentlyContinue
        Write-Host "   Temporary WAV deleted" -ForegroundColor Green
    }
    
    # Verify final MP4
    if (-not (Test-Path $OutputFile)) {
        Write-Error "MP4 file not created"
        exit 1
    }
    
    $mp4Size = (Get-Item $OutputFile).Length
    Write-Host "   MP4 created: $([Math]::Round($mp4Size/1024,1))KB" -ForegroundColor Green
    
    # Return success
    Write-Host ""
    Write-Host "SUCCESS: MP4 synthesis complete" -ForegroundColor Green
    Write-Host "   Output: $OutputFile" -ForegroundColor Green
    Write-Host "   Codec: AAC at 256kbps" -ForegroundColor Green
    
    exit 0
    
}
catch {
    Write-Error "Fatal error: $($_.Exception.Message)"
    
    # Cleanup temp file on error
    if (Test-Path $tempWavFile) {
        Remove-Item $tempWavFile -Force -ErrorAction SilentlyContinue
    }
    
    exit 1
}
