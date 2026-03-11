#!/usr/bin/env python3
"""
Neural Voice to MP4 Synthesizer
Uses edge-tts (Microsoft Edge Neural TTS) for Jenny/Guy/Aria neural voices,
with SAPI5 fallback for David/Zira when offline.
Outputs MP4 via FFmpeg.
"""

import subprocess
import asyncio
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# edge-tts voice mapping
EDGE_VOICES = {
    "Jenny": "en-US-JennyNeural",
    "Guy": "en-US-GuyNeural",
    "Aria": "en-US-AriaNeural",
    "David": "en-US-AndrewNeural",  # No David neural; Andrew is closest male
    "Zira": "en-US-JennyNeural",    # No Zira neural; Jenny is default female
}

# SAPI5 fallback voices (offline, non-neural)
SAPI5_VOICES = {
    "David": "Microsoft David Desktop",
    "Zira": "Microsoft Zira Desktop",
}


class WindowsMediaSynthesizer:
    """Synthesizes speech using edge-tts neural voices with SAPI5 fallback"""
    
    def __init__(self):
        self.ffmpeg_path = Path("C:\\ffmpeg\\bin\\ffmpeg.exe")
        if not self.ffmpeg_path.exists():
            raise FileNotFoundError(f"FFmpeg not found at {self.ffmpeg_path}")
        logger.info("WindowsMediaSynthesizer initialized (edge-tts + SAPI5 fallback)")
    
    def synthesize_to_mp4(self, text: str, output_file: str, voice: str = "Jenny", pitch: float = 1.0, rate: float = 0.95) -> bool:
        """Synthesize text to MP4. Uses edge-tts neural voices, falls back to SAPI5 if offline."""
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Temp MP3 for edge-tts or WAV for SAPI5
        temp_audio = output_path.parent / f"temp_{output_path.stem}"
        
        try:
            logger.info(f"Synthesizing with voice: {voice}")
            logger.info(f"Text length: {len(text)} characters")
            
            # Try edge-tts (neural) first
            edge_voice = EDGE_VOICES.get(voice, "en-US-JennyNeural")
            temp_mp3 = temp_audio.with_suffix(".mp3")
            success = self._synthesize_with_edge_tts(text, str(temp_mp3), edge_voice, rate)
            
            if success and temp_mp3.exists() and temp_mp3.stat().st_size > 0:
                input_file = temp_mp3
                logger.info(f"Neural audio created: {temp_mp3.stat().st_size:,} bytes")
            else:
                # Fallback to SAPI5
                logger.warning(f"edge-tts failed, falling back to SAPI5 for {voice}")
                temp_wav = temp_audio.with_suffix(".wav")
                sapi_voice = SAPI5_VOICES.get(voice, "Microsoft David Desktop")
                success = self._synthesize_with_sapi5(text, str(temp_wav), sapi_voice, rate)
                if not success or not temp_wav.exists():
                    logger.error("Both edge-tts and SAPI5 synthesis failed")
                    return False
                input_file = temp_wav
                logger.info(f"SAPI5 audio created: {temp_wav.stat().st_size:,} bytes")
            
            # Encode to MP4 with FFmpeg
            logger.info("Encoding MP4 with FFmpeg...")
            ffmpeg_cmd = [
                str(self.ffmpeg_path),
                "-i", str(input_file),
                "-c:a", "aac",
                "-b:a", "256k",
                "-y",
                str(output_path)
            ]
            
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"FFmpeg failed: {result.stderr}")
                return False
            
            logger.info(f"MP4 encoded: {output_path.stat().st_size:,} bytes")
            logger.info(f"Complete: {output_path.name}")
            return True
        
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return False
        
        finally:
            for ext in [".mp3", ".wav"]:
                f = temp_audio.with_suffix(ext)
                if f.exists():
                    f.unlink(missing_ok=True)
    
    def _synthesize_with_edge_tts(self, text: str, output_mp3: str, voice: str, rate: float) -> bool:
        """Synthesize using edge-tts (Microsoft Edge Neural TTS service)."""
        try:
            import edge_tts
        except ImportError:
            logger.warning("edge-tts not installed")
            return False
        
        rate_pct = int((rate - 1.0) * 100)
        rate_str = f"{rate_pct:+d}%" if rate_pct != 0 else "+0%"
        
        async def _do_synth():
            communicate = edge_tts.Communicate(text, voice, rate=rate_str)
            await communicate.save(output_mp3)
        
        try:
            asyncio.run(_do_synth())
            return True
        except Exception as e:
            logger.warning(f"edge-tts synthesis failed: {e}")
            return False
    
    def _synthesize_with_sapi5(self, text: str, output_wav: str, voice_name: str, rate: float) -> bool:
        """Fallback: synthesize using SAPI5 (System.Speech) — David/Zira only, non-neural."""
        escaped_text = text.replace("'", "''").replace('"', '""')
        sapi_rate = max(-10, min(10, int((rate - 1.0) * 10)))
        
        ps_script = f'''
[void][System.Reflection.Assembly]::LoadWithPartialName("System.Speech")
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SetOutputToWaveFile('{output_wav}')
try {{ $synth.SelectVoice("{voice_name}") }} catch {{ }}
$synth.Rate = {sapi_rate}
$synth.Speak("{escaped_text}")
$synth.Dispose()
Write-Host "OK"
'''
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                capture_output=True, text=True, timeout=120
            )
            return result.returncode == 0 and "OK" in result.stdout
        except Exception as e:
            logger.error(f"SAPI5 error: {e}")
            return False


if __name__ == "__main__":
    synth = WindowsMediaSynthesizer()
    
    test_text = "Hello, this is Jenny from Walmart Activity Hub. This is a neural voice test."
    output = "test_jenny.mp4"
    
    success = synth.synthesize_to_mp4(test_text, output, voice="Jenny", rate=0.95)
    
    if success:
        print(f"Successfully created: {output}")
    else:
        print("Synthesis failed")
        sys.exit(1)
