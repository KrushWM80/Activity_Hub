"""
MP4 Audio Pipeline - Direct Text-to-MP4 Synthesis
==================================================

Generates MP4 audio files directly from text without WAV intermediates.
Uses Windows.Media neural voices (Jenny, David, Zira) and FFmpeg for MP4 encoding.

Date: March 10, 2026
Status: MP4-only output with neural voices (Jenny, David, Zira)
"""

import logging
import subprocess
import os
from pathlib import Path
from typing import Tuple, Optional
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Voice(Enum):
    """Available neural voices (Windows.Media)"""
    JENNY = "Jenny"
    DAVID = "David"
    ZIRA = "Zira"


class MP4Pipeline:
    """Direct text-to-MP4 synthesis pipeline using Windows.Media neural voices"""
    
    OUTPUT_DIR = Path(__file__).parent / "mp4_output"
    
    def __init__(self):
        """Initialize MP4 pipeline"""
        # Create output directory
        self.OUTPUT_DIR.mkdir(exist_ok=True)
        logger.info("🎬 MP4 Pipeline initialized (Windows.Media neural voices)")
        logger.info(f"   Available voices: Jenny (default), David, Zira")
    
    def synthesize(
        self,
        text: str,
        output_file: Optional[str] = None,
        voice: Voice = Voice.JENNY,
        pitch: float = 1.0,
        rate: float = 0.95
    ) -> Tuple[bool, Optional[str]]:
        """
        Synthesize text directly to MP4 using Windows.Media neural voices.
        
        Args:
            text: Text to synthesize
            output_file: Output MP4 path (auto-generated if None)
            voice: Voice to use (JENNY, DAVID, ZIRA - default: JENNY)
            pitch: Voice pitch (0.5-2.0, default: 1.0)
            rate: Speech rate (0.5-2.0, default: 0.95)
        
        Returns:
            (success: bool, output_path: str or None)
        """
        
        # Generate output path if not provided
        if output_file is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = str(self.OUTPUT_DIR / f"synthesis_{voice.value}_{timestamp}.mp4")
        
        # Ensure output directory exists
        output_dir = Path(output_file).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🎤 Synthesizing text ({len(text)} chars) to MP4...")
        logger.info(f"   Voice: {voice.value}")
        logger.info(f"   Output: {Path(output_file).name}")
        
        try:
            # Import and use Windows.Media synthesizer
            from windows_media_synthesizer import WindowsMediaSynthesizer
            
            synth = WindowsMediaSynthesizer()
            success = synth.synthesize_to_mp4(text, output_file, voice=voice.value, pitch=pitch, rate=rate)
            
            if not success:
                logger.error("❌ Synthesis failed")
                return (False, None)
            
            # Verify output file
            if not Path(output_file).exists():
                logger.error(f"❌ Output file not created: {output_file}")
                return (False, None)
            
            file_size = Path(output_file).stat().st_size
            logger.info(f"✅ MP4 synthesis successful")
            logger.info(f"   File: {Path(output_file).name}")
            logger.info(f"   Size: {file_size / 1024:.1f}KB")
            
            return (True, output_file)
            
        except Exception as e:
            logger.error(f"❌ Synthesis error: {e}")
            return (False, None)


def synthesize_activity_message_mp4(
    message_text: str,
    voice: Voice = Voice.JENNY,
    output_file: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Simple API for MP4 synthesis.
    
    Args:
        message_text: Activity message text
        voice: Voice to use (default: Jenny)
        output_file: Output MP4 path (auto-generated if None)
    
    Returns:
        (success: bool, output_path: str or None)
    """
    pipeline = MP4Pipeline()
    return pipeline.synthesize(message_text, output_file, voice)


# ========== TEST ==========
if __name__ == "__main__":
    print("\n" + "="*60)
    print("MP4 Pipeline Test - Direct Text-to-MP4 Synthesis")
    print("="*60 + "\n")
    
    # Test 1: Simple message
    print("[Test 1] Activity Hub message")
    success, output = synthesize_activity_message_mp4(
        "Welcome to Walmart Activity Hub. Daily messages are now available in high quality audio.",
        voice=Voice.JENNY
    )
    if success:
        print(f"✅ Test 1 passed: {output}\n")
    else:
        print("❌ Test 1 failed\n")
    
    # Test 2: Store update message
    print("[Test 2] Store update message")
    success, output = synthesize_activity_message_mp4(
        "Store 1234 location update. All activity messages are now available in MP4 format.",
        voice=Voice.DAVID
    )
    if success:
        print(f"✅ Test 2 passed: {output}\n")
    else:
        print("❌ Test 2 failed\n")
    
    print("="*60)
    print("Test complete")
    print("="*60)
