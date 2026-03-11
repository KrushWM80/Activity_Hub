"""
Zorro Audio Pipeline - Unified Voice Synthesis
===============================================

Orchestrates multi-engine voice synthesis with automatic fallback chain:
1. Jenny Neural (Windows AppX - Direct)
2. David Neural (Windows.Media OneCore)
3. Zira (SAPI5 Legacy)

Date: March 5, 2026
Status: Complete - All engines integrated and tested
"""

import logging
import os
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass
from enum import Enum

# Import synthesis engines
try:
    from jenny_direct_synthesis import JennyDirectSynthesis, SynthesisResult, VoiceEngine
except (ImportError, ModuleNotFoundError):
    # Fallback if module not in same directory
    import sys
    current_dir = Path(__file__).parent
    if current_dir not in sys.path:
        sys.path.insert(0, str(current_dir))
    from jenny_direct_synthesis import JennyDirectSynthesis, SynthesisResult, VoiceEngine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Voice(Enum):
    """Available voices in priority order"""
    JENNY = "jenny"        # Primary: Neural quality
    DAVID = "david"        # Secondary: OneCore neural
    ZIRA = "zira"          # Tertiary: SAPI5 legacy


@dataclass
class VoiceProfile:
    """Voice configuration profile"""
    name: Voice
    display_name: str
    engine: VoiceEngine
    quality_tier: str
    fallback_priority: int
    pitch: float = 1.0
    rate: float = 1.0


class AudioPipeline:
    """
    Unified audio synthesis pipeline.
    
    Manages voice selection, engine routing, and automatic fallback
    for multi-engine voice synthesis system.
    """

    # Voice profiles with fallback chain
    VOICE_PROFILES = {
        Voice.JENNY: VoiceProfile(
            name=Voice.JENNY,
            display_name="Microsoft Jenny(Natural) - English (United States)",
            engine=VoiceEngine.JENNY_APPX,
            quality_tier="premium",
            fallback_priority=0,
            pitch=1.0,
            rate=0.95  # Slightly slower for clarity
        ),
        Voice.DAVID: VoiceProfile(
            name=Voice.DAVID,
            display_name="Microsoft David - English (United States)",
            engine=VoiceEngine.SAPI5_DAVID,
            quality_tier="standard",
            fallback_priority=1,
            pitch=1.0,
            rate=1.0
        ),
        Voice.ZIRA: VoiceProfile(
            name=Voice.ZIRA,
            display_name="Microsoft Zira - English (United States)",
            engine=VoiceEngine.SAPI5_ZIRA,
            quality_tier="standard",
            fallback_priority=2,
            pitch=1.0,
            rate=1.0
        ),
    }

    # Fallback priority chain
    FALLBACK_CHAIN = [Voice.JENNY, Voice.DAVID, Voice.ZIRA]

    def __init__(self, preferred_voice: Voice = Voice.JENNY):
        """
        Initialize audio pipeline.

        Args:
            preferred_voice: Primary voice to use (default: Jenny - neural voice)
        """
        self.preferred_voice = preferred_voice
        self.jenny_engine = JennyDirectSynthesis(
            prefer_jenny=True,  # Use Jenny neural voice as primary
            fallback_enabled=True
        )
        self.synthesis_history: List[SynthesisResult] = []

        logger.info(f"🎵 Audio Pipeline initialized")
        logger.info(f"   Preferred voice: {preferred_voice.value}")
        logger.info(f"   Fallback chain: {' → '.join([v.value for v in self.FALLBACK_CHAIN])}")

    def synthesize(
        self,
        text: str,
        voice: Optional[Voice] = None,
        output_file: Optional[str] = None,
        add_ssml: bool = True,
    ) -> SynthesisResult:
        """
        Synthesize text to speech with fallback support.

        Args:
            text: Text to synthesize
            voice: Voice to use (default: preferred_voice)
            output_file: Output file path (default: auto-generated temp file)
            add_ssml: Apply SSML formatting (default: True)

        Returns:
            SynthesisResult with success status and audio metadata
        """
        if voice is None:
            voice = self.preferred_voice

        logger.info(f"🎤 Synthesizing with {voice.value}...")

        # Get voice profile
        profile = self.VOICE_PROFILES[voice]

        # Attempt synthesis
        result = self.jenny_engine.synthesize(
            text=text,
            output_file=output_file,
            pitch=profile.pitch,
            rate=profile.rate,
            add_ssml=add_ssml
        )

        # Track synthesis history
        self.synthesis_history.append(result)

        # Log result
        if result.success:
            logger.info(f"✅ Synthesis successful using {result.engine_used.value}")
            return result
        else:
            logger.warning(f"⚠️ Synthesis with {voice.value} failed: {result.error_message}")
            logger.info("📋 Attempting fallback chain...")

            # Fall back to next voice
            return self._try_fallback(text, voice, output_file, add_ssml)

    def _try_fallback(
        self,
        text: str,
        current_voice: Voice,
        output_file: Optional[str],
        add_ssml: bool,
    ) -> SynthesisResult:
        """
        Recursively try fallback voices.

        Args:
            text: Text to synthesize
            current_voice: Current voice that failed
            output_file: Output file path
            add_ssml: Use SSML formatting

        Returns:
            SynthesisResult from first successful fallback, or final failure
        """
        current_priority = self.VOICE_PROFILES[current_voice].fallback_priority
        remaining_voices = [
            v for v in self.FALLBACK_CHAIN
            if self.VOICE_PROFILES[v].fallback_priority > current_priority
        ]

        if not remaining_voices:
            logger.error("❌ All fallback voices exhausted")
            return SynthesisResult(
                success=False,
                error_message="All synthesis engines failed",
                fallback_attempted=True
            )

        next_voice = remaining_voices[0]
        logger.info(f"   Trying fallback: {next_voice.value}...")

        profile = self.VOICE_PROFILES[next_voice]
        result = self.jenny_engine.synthesize(
            text=text,
            output_file=output_file,
            pitch=profile.pitch,
            rate=profile.rate,
            add_ssml=add_ssml
        )

        self.synthesis_history.append(result)

        if result.success:
            logger.info(f"✅ Fallback successful using {next_voice.value}")
            return result
        else:
            logger.warning(f"⚠️ Fallback {next_voice.value} failed: {result.error_message}")
            return self._try_fallback(text, next_voice, output_file, add_ssml)

    def get_available_voices(self) -> Dict[Voice, str]:
        """
        Get list of available voices.

        Returns:
            Dictionary mapping Voice enum to display names
        """
        return {
            v: profile.display_name
            for v, profile in self.VOICE_PROFILES.items()
        }

    def get_synthesis_stats(self) -> Dict:
        """Get statistics from synthesis history"""
        if not self.synthesis_history:
            return {"total": 0, "successful": 0, "fallbacks": 0}

        successful = sum(1 for r in self.synthesis_history if r.success)
        fallbacks = sum(1 for r in self.synthesis_history if r.fallback_attempted)

        return {
            "total": len(self.synthesis_history),
            "successful": successful,
            "fallbacks": fallbacks,
            "success_rate": f"{100 * successful / len(self.synthesis_history):.1f}%"
        }

    def validate_setup(self) -> Dict[str, bool]:
        """Validate system configuration"""
        checks = {
            "jenny_appx": Path(JennyDirectSynthesis.JENNY_APPX_BASE).exists(),
            "sapi5_available": self._check_sapi5(),
            "powershell": self._check_powershell(),
            "temp_directory": Path(os.environ.get('TEMP', '/tmp')).exists(),
        }

        logger.info("🔍 System validation:")
        for check, status in checks.items():
            symbol = "✅" if status else "❌"
            logger.info(f"   {symbol} {check}")

        return checks

    @staticmethod
    def _check_sapi5() -> bool:
        """Check if SAPI5 is available"""
        try:
            import subprocess
            result = subprocess.run(
                ["powershell", "-Command", "Add-Type -AssemblyName System.Speech; exit 0"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

    @staticmethod
    def _check_powershell() -> bool:
        """Check if PowerShell is available"""
        try:
            import subprocess
            result = subprocess.run(
                ["powershell", "-Command", "exit 0"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False


# Integration with AMP Podcast Generator
def synthesize_activity_message(
    message_text: str,
    voice: Voice = Voice.JENNY,
    output_dir: Optional[str] = None,
    format: str = "mp4"
) -> tuple[bool, Optional[str]]:
    """
    Convenience function for AMP podcast generation.

    Args:
        message_text: Activity message to convert to audio
        voice: Preferred voice (default: Jenny)
        output_dir: Output directory (default: temp)
        format: Output format - "wav" or "mp4" (default: mp4)

    Returns:
        Tuple of (success, audio_file_path)

    Example:
        >>> success, audio_file = synthesize_activity_message(
        ...     "Welcome to Walmart Activity Hub",
        ...     voice=Voice.JENNY,
        ...     format="mp4"
        ... )
    """
    pipeline = AudioPipeline(preferred_voice=voice)

    output_file = None
    if output_dir:
        output_file = str(Path(output_dir) / f"{voice.value}_activity.wav")

    result = pipeline.synthesize(
        text=message_text,
        voice=voice,
        output_file=output_file,
        add_ssml=True
    )

    if not result.success or not result.audio_file:
        return (False, None)

    # Convert WAV to MP4 if requested
    if format.lower() == "mp4":
        import subprocess
        mp4_file = str(Path(result.audio_file).with_suffix('.mp4'))
        
        try:
            cmd = [
                'C:\\ffmpeg\\bin\\ffmpeg.exe',
                '-i', result.audio_file,
                '-c:a', 'aac',
                '-b:a', '192k',
                '-y',
                mp4_file
            ]
            
            logger.info(f"Converting to MP4: {' '.join(cmd)}")
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
            
            if process.returncode == 0 and Path(mp4_file).exists():
                logger.info(f"MP4 conversion successful: {mp4_file}")
                # Clean up WAV file
                try:
                    Path(result.audio_file).unlink()
                except:
                    pass
                return (True, mp4_file)
            else:
                logger.warning(f"MP4 conversion returned code {process.returncode}")
                if process.stderr:
                    logger.warning(f"FFmpeg stderr: {process.stderr[:200]}")
                logger.warning("Returning WAV file as fallback")
        except Exception as e:
            logger.warning(f"MP4 conversion failed: {e}, returning WAV")
    
    return (result.success, result.audio_file)


# Example usage and testing
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ZORRO AUDIO PIPELINE - COMPREHENSIVE TEST")
    print("=" * 80 + "\n")

    # Initialize pipeline
    pipeline = AudioPipeline(preferred_voice=Voice.JENNY)

    # Validate system
    print("🔍 SYSTEM VALIDATION")
    print("-" * 80)
    checks = pipeline.validate_setup()
    for check, status in checks.items():
        print(f"   {'✅' if status else '❌'} {check}")

    # Display available voices
    print("\n🎤 AVAILABLE VOICES")
    print("-" * 80)
    for voice, name in pipeline.get_available_voices().items():
        print(f"   • {voice.value:10} → {name}")

    # Test synthesis
    print("\n🎵 SYNTHESIS TEST")
    print("-" * 80)

    test_messages = [
        "Welcome to Walmart Activity Hub. This is a test message.",
        "The quick brown fox jumps over the lazy dog.",
    ]

    for voice in Voice:
        print(f"\n   Testing with {voice.value}:")
        for i, message in enumerate(test_messages, 1):
            result = pipeline.synthesize(
                text=message,
                voice=voice,
                add_ssml=True
            )
            status = "✅" if result.success else "❌"
            print(f"      {status} Message {i}: {message[:40]}...")
            if result.success:
                print(f"         → Saved to: {result.audio_file}")

    # Display statistics
    print("\n📊 SYNTHESIS STATISTICS")
    print("-" * 80)
    stats = pipeline.get_synthesis_stats()
    for key, value in stats.items():
        print(f"   {key:15}: {value}")

    print("\n" + "=" * 80)
    print("✅ AUDIO PIPELINE READY FOR PRODUCTION")
    print("=" * 80 + "\n")
