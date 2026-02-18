# AMP Video Creation Script
# Automates video creation using FFmpeg and PowerShell

param(
    [string]$InputScript = "scripts\amp_video_script.json",
    [string]$OutputVideo = "output\amp_video_30sec.mp4",
    [string]$VoiceFile = "audio\voiceover.wav"
)

Write-Host "🎬 AMP Video Creation Tool" -ForegroundColor Cyan
Write-Host "=" * 40 -ForegroundColor Cyan

# Check if FFmpeg is available
function Test-FFmpeg {
    try {
        $null = ffmpeg -version 2>$null
        return $true
    } catch {
        return $false
    }
}

# Install FFmpeg if not available
function Install-FFmpeg {
    Write-Host "📥 Installing FFmpeg..." -ForegroundColor Yellow
    
    try {
        # Download FFmpeg
        $downloadUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        $zipPath = "ffmpeg.zip"
        
        Write-Host "⬇️ Downloading FFmpeg..." -ForegroundColor Gray
        Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath
        
        # Extract FFmpeg
        Write-Host "📁 Extracting FFmpeg..." -ForegroundColor Gray
        Expand-Archive -Path $zipPath -DestinationPath "." -Force
        
        # Add to PATH for this session
        $ffmpegPath = Get-ChildItem -Path "." -Name "ffmpeg-*" -Directory | Select-Object -First 1
        $env:PATH += ";$PWD\$ffmpegPath\bin"
        
        Write-Host "✅ FFmpeg installed successfully!" -ForegroundColor Green
        Remove-Item $zipPath -Force
        
        return $true
    } catch {
        Write-Host "❌ Failed to install FFmpeg" -ForegroundColor Red
        Write-Host "Please download manually from: https://ffmpeg.org/download.html" -ForegroundColor Yellow
        return $false
    }
}

# Create text-to-speech audio
function Create-TextToSpeech {
    param([string]$Text, [string]$OutputFile)
    
    Write-Host "🗣️ Creating text-to-speech audio..." -ForegroundColor Yellow
    
    try {
        # Use Windows built-in SAPI for text-to-speech
        $voice = New-Object -ComObject SAPI.SpVoice
        $file = New-Object -ComObject SAPI.SpFileStream
        
        # Configure audio output
        $file.Open($OutputFile, 3)
        $voice.AudioOutputStream = $file
        
        # Set voice properties
        $voice.Rate = 0    # Normal speed
        $voice.Volume = 100 # Full volume
        
        # Speak the text
        $voice.Speak($Text, 0)
        $file.Close()
        
        Write-Host "✅ Audio file created: $OutputFile" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Failed to create audio: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Create video slides
function Create-VideoSlides {
    Write-Host "🎨 Creating video slides..." -ForegroundColor Yellow
    
    # Create slides directory
    $slidesDir = "assets\slides"
    New-Item -ItemType Directory -Force -Path $slidesDir | Out-Null
    
    # Slide templates (using HTML/CSS for easy creation)
    $slideTemplates = @{
        "opening" = @"
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: linear-gradient(45deg, #004c91, #0066cc); color: white; font-family: Arial; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .container { text-align: center; }
        h1 { font-size: 48px; margin-bottom: 20px; }
        .subtitle { font-size: 24px; opacity: 0.9; }
        .logo { width: 100px; height: 100px; background: #ffc220; border-radius: 50%; margin: 20px auto; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo"></div>
        <h1>AMP Update</h1>
        <div class="subtitle">Week 41 - Store Safety & Security</div>
    </div>
</body>
</html>
"@
        "content" = @"
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: linear-gradient(45deg, #f8f9fa, #ffffff); color: #333; font-family: Arial; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .container { text-align: left; max-width: 800px; }
        h2 { color: #004c91; font-size: 36px; margin-bottom: 30px; }
        .action-item { background: #ffc220; padding: 15px; margin: 10px 0; border-radius: 8px; font-size: 20px; }
        .priority { background: #dc3545; color: white; padding: 10px 20px; border-radius: 20px; display: inline-block; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Key Actions This Week</h2>
        <div class="action-item">✓ Review safety checklist with team</div>
        <div class="action-item">✓ Implement new security protocols</div>
        <div class="priority">Priority: HIGH</div>
    </div>
</body>
</html>
"@
        "closing" = @"
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: linear-gradient(45deg, #004c91, #0066cc); color: white; font-family: Arial; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .container { text-align: center; }
        h2 { font-size: 42px; margin-bottom: 30px; }
        .cta { background: #ffc220; color: #333; padding: 20px 40px; border-radius: 10px; font-size: 24px; display: inline-block; }
        .logo { width: 80px; height: 80px; background: #ffc220; border-radius: 50%; margin: 20px auto; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo"></div>
        <h2>View Full Details</h2>
        <div class="cta">Check Your AMP Dashboard</div>
    </div>
</body>
</html>
"@
    }
    
    # Save slide templates
    foreach ($slide in $slideTemplates.GetEnumerator()) {
        $slideFile = "$slidesDir\$($slide.Key).html"
        $slide.Value | Out-File -FilePath $slideFile -Encoding UTF8
        Write-Host "✅ Created slide: $slideFile" -ForegroundColor Green
    }
    
    return $true
}

# Convert HTML slides to images
function Convert-SlidesToImages {
    Write-Host "🖼️ Converting slides to images..." -ForegroundColor Yellow
    
    # Note: This requires a browser automation tool or screenshot utility
    # For now, we'll create a manual instruction
    
    Write-Host "📋 Manual Step Required:" -ForegroundColor Yellow
    Write-Host "1. Open each HTML file in assets\slides\" -ForegroundColor Gray
    Write-Host "2. Take screenshots (1920x1080 recommended)" -ForegroundColor Gray
    Write-Host "3. Save as PNG files in assets\images\" -ForegroundColor Gray
    Write-Host "4. Name them: slide1.png, slide2.png, slide3.png" -ForegroundColor Gray
    
    return $true
}

# Create final video
function Create-FinalVideo {
    param([string]$AudioFile, [string]$OutputFile)
    
    Write-Host "🎬 Creating final video..." -ForegroundColor Yellow
    
    try {
        # FFmpeg command to create video from images and audio
        $ffmpegCmd = @"
ffmpeg -y -loop 1 -i "assets\images\slide1.png" -loop 1 -i "assets\images\slide2.png" -loop 1 -i "assets\images\slide3.png" -i "$AudioFile" -filter_complex "[0:v]scale=1920:1080,setpts=PTS-STARTPTS[v0];[1:v]scale=1920:1080,setpts=PTS-STARTPTS+5/TB[v1];[2:v]scale=1920:1080,setpts=PTS-STARTPTS+20/TB[v2];[v0][v1][v2]concat=n=3:v=1:a=0[outv]" -map "[outv]" -map 3:a -c:v libx264 -c:a aac -t 30 "$OutputFile"
"@
        
        Write-Host "📱 Running FFmpeg command..." -ForegroundColor Gray
        Invoke-Expression $ffmpegCmd
        
        Write-Host "✅ Video created successfully: $OutputFile" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Failed to create video: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main execution
function Main {
    # Check dependencies
    if (-not (Test-FFmpeg)) {
        $install = Read-Host "FFmpeg not found. Install automatically? (y/n)"
        if ($install -eq "y" -or $install -eq "Y") {
            if (-not (Install-FFmpeg)) {
                exit 1
            }
        } else {
            Write-Host "❌ FFmpeg required for video creation" -ForegroundColor Red
            exit 1
        }
    }
    
    # Create directory structure
    @("scripts", "assets\slides", "assets\images", "audio", "output") | ForEach-Object {
        New-Item -ItemType Directory -Force -Path $_ | Out-Null
    }
    
    # Generate video script
    Write-Host "📝 Running video script generator..." -ForegroundColor Yellow
    python amp_video_generator.py
    
    # Create audio
    $voiceScript = "Important update: Store Safety and Security Update Week 41. Key actions this week: Review safety checklist with team, Implement new security protocols. Priority level: High. Deadline: End of Week 41. Check your AMP dashboard for complete details."
    
    $audioFile = "audio\voiceover.wav"
    if (Create-TextToSpeech -Text $voiceScript -OutputFile $audioFile) {
        Write-Host "✅ Audio created successfully" -ForegroundColor Green
    }
    
    # Create visual elements
    if (Create-VideoSlides) {
        Write-Host "✅ Slides created successfully" -ForegroundColor Green
    }
    
    Convert-SlidesToImages
    
    Write-Host ""
    Write-Host "🎉 AMP Video Creation Setup Complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Final Steps:" -ForegroundColor Cyan
    Write-Host "1. Take screenshots of HTML slides in assets\slides\" -ForegroundColor Yellow
    Write-Host "2. Save images as PNG in assets\images\" -ForegroundColor Yellow
    Write-Host "3. Run: Create-FinalVideo to combine everything" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🎬 Your 30-second AMP video will be saved to: $OutputVideo" -ForegroundColor Cyan
}

# Run main function
Main