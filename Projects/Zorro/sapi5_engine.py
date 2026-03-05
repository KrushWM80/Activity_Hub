"""
SAPI5 Synthesis Engine - Wrapper for System.Speech.Synthesis (legacy)
Provides fallback support for David and Zira voices
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class SAPI5Engine:
    """Synthesize audio using Windows SAPI5 (System.Speech.Synthesis)"""
    
    def __init__(self):
        """Initialize SAPI5 synthesis engine"""
        self.engine_name = "SAPI5"
        self.available_voices = []
        self._detect_available_voices()
    
    def _detect_available_voices(self) -> None:
        """Detect which SAPI5 voices are available on system"""
        try:
            ps_script = """
            Add-Type -AssemblyName System.Speech
            $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $voices = $synth.GetInstalledVoices()
            $voices | ForEach-Object { Write-Host $_.VoiceInfo.Name }
            """
            
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.available_voices = [
                    v.strip() for v in result.stdout.split('\n')
                    if v.strip() and 'Microsoft' in v
                ]
                logger.info(f"Detected {len(self.available_voices)} SAPI5 voices: {self.available_voices}")
            else:
                logger.warning("Could not enumerate SAPI5 voices")
                self.available_voices = []
        except Exception as e:
            logger.error(f"Error detecting SAPI5 voices: {e}")
            self.available_voices = []
    
    def synthesize(
        self,
        text: str,
        output_file: str,
        voice: str = "Microsoft David Desktop",
        rate: int = -2
    ) -> Tuple[bool, str]:
        """
        Synthesize text to audio file using SAPI5
        
        Args:
            text: Text to synthesize
            output_file: Path to output WAV file
            voice: Voice name (David Desktop, Zira Desktop, etc.)
            rate: Speech rate (-10 to +10, -2 is normal)
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        
        if not text or text.strip() == "":
            return False, "Text cannot be empty"
        
        if not output_file:
            return False, "Output file path required"
        
        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Escape special characters in text
        escaped_text = text.replace('"', '""').replace("'", "''")
        
        # Map voice names to SAPI5 format
        voice_name = self._map_voice_name(voice)
        
        # PowerShell script for SAPI5 synthesis
        ps_script = f"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null

$text = @'
{escaped_text}
'@

$outputFile = "{output_file}"
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synthesizer.Rate = {rate}
$synthesizer.Volume = 100

# Find and select voice
$voices = $synthesizer.GetInstalledVoices()
$selectedVoice = $null
foreach ($v in $voices) {{
    if ($v.VoiceInfo.Name -like '*{voice_name}*') {{
        $selectedVoice = $v
        break
    }}
}}

if ($selectedVoice) {{
    $synthesizer.SelectVoice($selectedVoice.VoiceInfo.Name)
}} else {{
    Write-Host "Voice not found: {voice_name}"
    exit 1
}}

try {{
    $synthesizer.SetOutputToWaveFile($outputFile)
    $synthesizer.Speak($text)
    $synthesizer.SetOutputToNull()
    $synthesizer.Dispose()
    
    Start-Sleep -Milliseconds 500
    
    if (Test-Path $outputFile) {{
        $size = (Get-Item $outputFile).Length / 1024 / 1024
        Write-Host "Success: $outputFile ($([Math]::Round($size, 2)) MB)"
        exit 0
    }} else {{
        Write-Host "File not created"
        exit 1
    }}
}} catch {{
    Write-Host "Error: $_"
    exit 1
}}
"""
        
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=180  # 3 minute timeout
            )
            
            # Check if file was created
            if output_path.exists() and output_path.stat().st_size > 1000:
                file_size_mb = output_path.stat().st_size / (1024 * 1024)
                msg = f"✅ SAPI5 audio synthesized: {output_file} ({file_size_mb:.2f} MB)"
                logger.info(msg)
                return True, msg
            else:
                error_msg = result.stdout if result.stdout else result.stderr
                logger.error(f"SAPI5 synthesis failed: {error_msg}")
                return False, f"SAPI5 synthesis failed: {error_msg}"
        
        except subprocess.TimeoutExpired:
            return False, "SAPI5 synthesis timed out (>3 minutes)"
        except Exception as e:
            return False, f"SAPI5 synthesis error: {str(e)}"
    
    def _map_voice_name(self, voice: str) -> str:
        """
        Map voice identifier to SAPI5 voice name
        
        Args:
            voice: Voice name (david, zira, etc.)
        
        Returns:
            SAPI5 voice display name
        """
        voice_lower = voice.lower()
        
        if "david" in voice_lower:
            return "David"
        elif "zira" in voice_lower:
            return "Zira"
        
        return voice
    
    def test_voice(self, voice: str) -> Tuple[bool, str]:
        """
        Test if a voice is available
        
        Args:
            voice: Voice name to test
        
        Returns:
            Tuple of (available: bool, message: str)
        """
        if not self.available_voices:
            return False, "SAPI5 voice detection failed"
        
        voice_lower = voice.lower()
        matched = [
            v for v in self.available_voices
            if voice_lower in v.lower()
        ]
        
        if matched:
            return True, f"SAPI5 voice found: {matched[0]}"
        else:
            return False, (
                f"SAPI5 voice '{voice}' not found. Available: "
                f"{', '.join(self.available_voices)}"
            )
    
    def list_available_voices(self) -> list:
        """Return list of available SAPI5 voices"""
        return self.available_voices
    
    def is_available(self) -> bool:
        """Check if SAPI5 is available and functional"""
        return len(self.available_voices) > 0
