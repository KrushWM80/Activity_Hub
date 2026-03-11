#!/usr/bin/env python3
"""
Direct MP4 synthesis from text using Jenny voice
Generates MP4 files without intermediate WAV files
"""

import os
import sys
import tempfile
import subprocess
import logging
from pathlib import Path
from enum import Enum

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add Zorro Audio path
audio_dir = Path("Store Support/Projects/AMP/Zorro/Audio").resolve()
sys.path.insert(0, str(audio_dir))

from audio_pipeline import synthesize_activity_message, Voice

class MP4Synthesis:
    """Direct text-to-MP4 synthesis using Jenny voice"""
    
    def __init__(self):
        self.ffmpeg_path = "C:\\ffmpeg\\bin\\ffmpeg.exe"
        self.verify_ffmpeg()
    
    def verify_ffmpeg(self):
        """Verify FFmpeg is installed and accessible"""
        if not Path(self.ffmpeg_path).exists():
            raise FileNotFoundError(f"FFmpeg not found at {self.ffmpeg_path}")
        
        result = subprocess.run([self.ffmpeg_path, '-version'], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            raise RuntimeError("FFmpeg verification failed")
        
        logger.info("✓ FFmpeg verified")
    
    def text_to_mp4(self, text, output_path=None, voice=Voice.JENNY):
        """
        Synthesize text directly to MP4 file
        
        Args:
            text: Message text to synthesize
            output_path: Output MP4 file path (auto-generated if None)
            voice: Voice to use (default: JENNY)
        
        Returns:
            (success: bool, output_file: str)
        """
        
        logger.info(f"🎤 Audio MP4 synthesis started")
        logger.info(f"   Text length: {len(text)} characters")
        logger.info(f"   Voice: {voice.name}")
        
        # Create output directory if not specified
        if output_path is None:
            output_dir = Path("Store Support/Projects/AMP/Zorro/Audio/mp4_output").resolve()
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"jenny_{Path(tempfile.mktemp()).name}_audio.mp4"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Synthesize audio (generates WAV in temp)
        logger.info("   [1/2] Generating audio...")
        try:
            success, wav_file = synthesize_activity_message(
                message_text=text,
                voice=voice
            )
            
            if not success or not wav_file:
                logger.error("✗ Audio synthesis failed")
                return False, None
            
            wav_path = Path(wav_file)
            if not wav_path.exists():
                logger.error(f"✗ WAV file not created: {wav_file}")
                return False, None
            
            wav_size = wav_path.stat().st_size
            logger.info(f"   ✓ Audio generated ({wav_size:,} bytes)")
            
        except Exception as e:
            logger.error(f"✗ Synthesis error: {e}")
            return False, None
        
        # Step 2: Convert WAV to MP4 using FFmpeg
        logger.info("   [2/2] Encoding to MP4...")
        try:
            # Simple FFmpeg command: WAV → MP4 (audio-only)
            cmd = [
                self.ffmpeg_path,
                '-i', str(wav_path),
                '-c:a', 'aac',           # AAC codec
                '-b:a', '256k',          # 256kbps bitrate
                '-vn',                   # No video
                '-loglevel', 'error',    # Suppress FFmpeg output
                '-y',                    # Overwrite
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                logger.error(f"✗ FFmpeg encoding failed: {result.stderr}")
                return False, None
            
            # Verify output
            if not output_path.exists():
                logger.error("✗ MP4 file not created")
                return False, None
            
            mp4_size = output_path.stat().st_size
            logger.info(f"   ✓ MP4 encoded ({mp4_size:,} bytes)\n")
            
            # Cleanup WAV
            try:
                wav_path.unlink()
            except:
                pass
            
            logger.info(f"✅ Synthesis complete: {output_path.name}")
            return True, str(output_path)
            
        except subprocess.TimeoutExpired:
            logger.error("✗ Encoding timed out")
            return False, None
        except Exception as e:
            logger.error(f"✗ Encoding error: {e}")
            return False, None


def synthesize_activity_message_mp4(message_text, voice=Voice.JENNY, output_dir=None):
    """
    Convenience function: Synthesize activity message directly to MP4
    
    Args:
        message_text: Text to synthesize
        voice: Voice to use
        output_dir: Output directory (uses default if None)
    
    Returns:
        (success: bool, mp4_file_path: str)
    """
    
    synthesizer = MP4Synthesis()
    
    if output_dir:
        output_path = Path(output_dir) / f"message_{Path(tempfile.mktemp()).name}.mp4"
    else:
        output_path = None
    
    return synthesizer.text_to_mp4(message_text, output_path, voice)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("DIRECT TEXT-TO-MP4 SYNTHESIS TEST")
    print("="*70 + "\n")
    
    # Test messages
    test_messages = [
        "Welcome to Walmart Activity Hub. This is a test message with Jenny voice.",
        "Store 1234 location update. Daily operations summary.",
    ]
    
    for i, msg in enumerate(test_messages, 1):
        print(f"[Test {i}] Synthesizing: {msg[:60]}...\n")
        
        success, mp4_file = synthesize_activity_message_mp4(msg)
        
        if success:
            file_size = os.path.getsize(mp4_file)
            print(f"✓ SUCCESS: {Path(mp4_file).name}")
            print(f"  Size: {file_size:,} bytes\n")
        else:
            print(f"✗ FAILED\n")
    
    print("="*70)
    print("✓ Direct MP4 synthesis is ready for integration")
    print("="*70 + "\n")
