"""
Windows Media Synthesis Engine - Wrapper for Windows.Media.SpeechSynthesis API
Uses PowerShell to access WinRT APIs directly
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple
import logging

# Get logger
logger = logging.getLogger(__name__)

# Path to PowerShell script
SCRIPT_DIR = Path(__file__).parent / "scripts"
SYNTHESIZE_SCRIPT = SCRIPT_DIR / "synthesize_windows_media.ps1"


class WindowsMediaEngine:
    """Synthesize audio using Windows.Media.SpeechSynthesis API"""
    
    def __init__(self, voice: str = "Jenny"):
        """
        Initialize Windows.Media synthesis engine
        
        Args:
            voice: Voice name (Jenny, Aria, Guy, Mark)
        """
        self.voice = voice
        self.engine_name = "Windows.Media"
        self.available_voices = []
        self._detect_available_voices()
    
    def _detect_available_voices(self) -> None:
        """Detect which Windows.Media voices are available on system"""
        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy", "Bypass",
                    "-Command",
                    """
                    Add-Type -AssemblyName System.Runtime.WindowsRuntime
                    [Windows.Foundation.Metadata.ApiInformation, Windows.Foundation.Metadata, ContentType = WindowsRuntime] | Out-Null
                    $voices = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
                    $voices | ForEach-Object { Write-Host $_.DisplayName }
                    """
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.available_voices = [
                    v.strip() for v in result.stdout.split('\n')
                    if v.strip() and not v.startswith('Add-Type')
                ]
                logger.info(f"Detected {len(self.available_voices)} Windows.Media voices")
            else:
                logger.warning("Could not enumerate Windows.Media voices")
                self.available_voices = []
        except Exception as e:
            logger.error(f"Error detecting voices: {e}")
            self.available_voices = []
    
    def synthesize(
        self,
        text: str,
        output_file: str,
        voice: Optional[str] = None,
        rate: float = 1.0,
        pitch: float = 1.0
    ) -> Tuple[bool, str]:
        """
        Synthesize text to audio file using Windows.Media API
        
        Args:
            text: Text to synthesize
            output_file: Path to output WAV file
            voice: Voice name (overrides default)
            rate: Speech rate (0.5 to 2.0)
            pitch: Pitch adjustment (0.5 to 2.0)
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        
        if not text or text.strip() == "":
            return False, "Text cannot be empty"
        
        if not output_file:
            return False, "Output file path required"
        
        # Use provided voice or default
        target_voice = voice or self.voice
        
        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if PowerShell script exists
        if not SYNTHESIZE_SCRIPT.exists():
            # Try alternate location
            alt_script = Path(__file__).parent / "scripts" / "synthesize_windows_media.ps1"
            if not alt_script.exists():
                return False, f"PowerShell script not found at {SYNTHESIZE_SCRIPT}"
        
        # Prepare PowerShell command
        ps_command = f"""
        & '{SYNTHESIZE_SCRIPT}' -VoiceName '{target_voice}' -InputText @'
{text}
'@ -OutputFile '{output_file}' -Rate {rate} -Pitch {pitch}
        """
        
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=180  # 3 minute timeout for long text
            )
            
            # Check if file was created
            if output_path.exists() and output_path.stat().st_size > 1000:
                file_size_mb = output_path.stat().st_size / (1024 * 1024)
                msg = f"✅ Audio synthesized: {output_file} ({file_size_mb:.2f} MB)"
                logger.info(msg)
                return True, msg
            else:
                error_msg = result.stderr if result.stderr else "File not created or too small"
                logger.error(f"Synthesis failed: {error_msg}")
                return False, f"Synthesis failed: {error_msg}"
        
        except subprocess.TimeoutExpired:
            return False, "Synthesis timed out (>3 minutes)"
        except Exception as e:
            return False, f"Synthesis error: {str(e)}"
    
    def test_voice(self, voice: str) -> Tuple[bool, str]:
        """
        Test if a voice is available without generating full audio
        
        Args:
            voice: Voice name to test
        
        Returns:
            Tuple of (available: bool, message: str)
        """
        if not self.available_voices:
            return False, "Voice detection failed on system"
        
        normalized_voice = voice.strip().lower()
        matched = [
            v for v in self.available_voices
            if normalized_voice in v.lower()
        ]
        
        if matched:
            return True, f"Voice found: {matched[0]}"
        else:
            return False, (
                f"Voice '{voice}' not found. Available: "
                f"{', '.join(self.available_voices[:3])}..."
            )
    
    def list_available_voices(self) -> list:
        """Return list of available Windows.Media voices"""
        return self.available_voices
    
    def is_available(self) -> bool:
        """Check if Windows.Media API is available and functional"""
        return len(self.available_voices) > 0


class WindowsMediaEngineError(Exception):
    """Custom exception for Windows.Media engine errors"""
    pass
