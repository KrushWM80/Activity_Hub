"""
Audio Pipeline - Unified abstraction layer for audio synthesis
Supports both Windows.Media (modern) and SAPI5 (legacy) engines with smart fallback
"""

import logging
from pathlib import Path
from typing import Optional, Tuple

from voice_config import (
    VOICE_PROFILES,
    FALLBACK_CHAIN,
    get_voice_profile,
    get_next_fallback,
    DEFAULT_VOICE
)
from windows_media_engine import WindowsMediaEngine
from sapi5_engine import SAPI5Engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AudioPipeline:
    """
    Unified audio synthesis pipeline supporting multiple engines and voices
    Automatically falls back to alternative voices/engines on failure
    """
    
    def __init__(
        self,
        voice: str = DEFAULT_VOICE,
        fallback_enabled: bool = True,
        fallback_chain: Optional[list] = None
    ):
        """
        Initialize audio synthesis pipeline
        
        Args:
            voice: Primary voice to use (jenny, aria, guy, mark, david, zira)
            fallback_enabled: Automatically try fallback chain if primary fails
            fallback_chain: Custom fallback chain (uses default if None)
        """
        self.primary_voice = voice.lower()
        self.fallback_enabled = fallback_enabled
        self.fallback_chain = fallback_chain or FALLBACK_CHAIN
        self.current_voice = None
        self.current_engine = None
        
        # Initialize engines
        self.windows_media_engine = None
        self.sapi5_engine = None
        
        self._initialize_engines()
        
        # Validate primary voice
        self._validate_voice(self.primary_voice)
    
    def _initialize_engines(self) -> None:
        """Initialize available synthesis engines"""
        try:
            self.windows_media_engine = WindowsMediaEngine()
            if self.windows_media_engine.is_available():
                logger.info("✅ Windows.Media engine initialized")
            else:
                logger.warning("⚠️  Windows.Media engine available but no voices detected")
        except Exception as e:
            logger.warning(f"Windows.Media engine init failed: {e}")
        
        try:
            self.sapi5_engine = SAPI5Engine()
            if self.sapi5_engine.is_available():
                logger.info("✅ SAPI5 engine initialized (fallback)")
            else:
                logger.warning("⚠️  SAPI5 engine failed")
        except Exception as e:
            logger.warning(f"SAPI5 engine init failed: {e}")
    
    def _validate_voice(self, voice: str) -> Tuple[bool, str]:
        """
        Validate that voice exists in profiles
        
        Returns:
            Tuple of (is_valid, message)
        """
        profile = get_voice_profile(voice)
        if not profile:
            available = ", ".join(self.fallback_chain)
            msg = f"Voice '{voice}' not found. Available: {available}"
            logger.warning(msg)
            return False, msg
        return True, f"Voice '{voice}' validated"
    
    def _get_engine_for_voice(self, voice: str) -> Optional[object]:
        """Get the appropriate engine for a voice"""
        profile = get_voice_profile(voice)
        if not profile:
            return None
        
        engine_type = profile.get("engine", "").lower()
        
        if engine_type == "windows_media":
            return self.windows_media_engine
        elif engine_type == "sapi5":
            return self.sapi5_engine
        
        return None
    
    def synthesize(
        self,
        text: str,
        output_file: str,
        voice: Optional[str] = None,
        fallback: bool = True
    ) -> Tuple[bool, str, str]:
        """
        Synthesize text to audio file with automatic fallback
        
        Args:
            text: Text to synthesize
            output_file: Path to output WAV file
            voice: Voice to use (overrides primary)
            fallback: Enable fallback chain on failure
        
        Returns:
            Tuple of (success: bool, message: str, voice_used: str)
        """
        
        # Use provided voice or primary
        target_voice = (voice or self.primary_voice).lower()
        voices_tried = []
        
        # Ensure output directory
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Try primary voice
        success, message = self._try_voice(target_voice, text, output_file)
        voices_tried.append(target_voice)
        
        if success:
            self.current_voice = target_voice
            logger.info(f"✅ Synthesized with '{target_voice}'")
            return True, message, target_voice
        
        # Try fallback chain if enabled
        if not fallback or not self.fallback_enabled:
            return False, f"Synthesis failed with {target_voice}: {message}", target_voice
        
        logger.info(f"⚠️  Fallback initiated: {message}")
        
        # Find starting point in fallback chain
        try:
            start_index = self.fallback_chain.index(target_voice) + 1
        except ValueError:
            start_index = 0
        
        # Try each voice in fallback chain
        for fallback_voice in self.fallback_chain[start_index:]:
            if fallback_voice in voices_tried:
                continue
            
            voices_tried.append(fallback_voice)
            success, message = self._try_voice(fallback_voice, text, output_file)
            
            if success:
                self.current_voice = fallback_voice
                fallback_msg = f"✅ Fallback success with '{fallback_voice}'"
                logger.info(fallback_msg)
                return True, message, fallback_voice
            else:
                logger.warning(f"  ❌ {fallback_voice} failed: {message}")
        
        # All voices failed
        fail_msg = f"All voices failed. Tried: {', '.join(voices_tried)}"
        logger.error(fail_msg)
        return False, fail_msg, None
    
    def _try_voice(self, voice: str, text: str, output_file: str) -> Tuple[bool, str]:
        """
        Attempt synthesis with a specific voice
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        voice = voice.lower()
        profile = get_voice_profile(voice)
        
        if not profile:
            return False, f"Voice '{voice}' not in profiles"
        
        engine = self._get_engine_for_voice(voice)
        if not engine:
            return False, f"No engine for voice '{voice}'"
        
        if not engine.is_available():
            return False, f"Engine for '{voice}' not available"
        
        # Call appropriate engine
        if profile["engine"] == "windows_media":
            success, message = engine.synthesize(
                text=text,
                output_file=output_file,
                voice=voice,
                rate=profile.get("speech_rate", 1.0),
                pitch=profile.get("pitch_adjustment", 1.0)
            )
        elif profile["engine"] == "sapi5":
            success, message = engine.synthesize(
                text=text,
                output_file=output_file,
                voice=voice,
                rate=profile.get("speech_rate", -2)
            )
        else:
            return False, f"Unknown engine: {profile['engine']}"
        
        return success, message
    
    def get_available_voices(self) -> dict:
        """
        Get all available voices grouped by engine
        
        Returns:
            Dict with engine names as keys, voice lists as values
        """
        voices = {
            "windows_media": [],
            "sapi5": [],
            "unavailable": []
        }
        
        for voice_name, profile in VOICE_PROFILES.items():
            engine_type = profile.get("engine", "").lower()
            
            # Check if engine is available
            if engine_type == "windows_media":
                if self.windows_media_engine and self.windows_media_engine.is_available():
                    voices["windows_media"].append(voice_name)
                else:
                    voices["unavailable"].append(voice_name)
            elif engine_type == "sapi5":
                if self.sapi5_engine and self.sapi5_engine.is_available():
                    voices["sapi5"].append(voice_name)
                else:
                    voices["unavailable"].append(voice_name)
        
        return voices
    
    def get_voice_info(self, voice: str) -> Optional[dict]:
        """Get detailed information about a specific voice"""
        profile = get_voice_profile(voice)
        if not profile:
            return None
        
        # Add availability status
        engine = self._get_engine_for_voice(voice)
        is_available = engine.is_available() if engine else False
        
        return {
            **profile,
            "is_available": is_available,
            "display_name": profile.get("display_name"),
            "engine_status": "ready" if is_available else "unavailable"
        }
    
    def validate_setup(self) -> dict:
        """Validate entire synthesis pipeline setup"""
        status = {
            "primary_voice": self.primary_voice,
            "primary_voice_valid": get_voice_profile(self.primary_voice) is not None,
            "windows_media_available": (
                self.windows_media_engine is not None and 
                self.windows_media_engine.is_available()
            ),
            "sapi5_available": (
                self.sapi5_engine is not None and 
                self.sapi5_engine.is_available()
            ),
            "fallback_chain": self.fallback_chain,
            "issues": []
        }
        
        # Check for issues
        if not status["primary_voice_valid"]:
            status["issues"].append(f"Primary voice '{self.primary_voice}' not found")
        
        if not status["windows_media_available"] and not status["sapi5_available"]:
            status["issues"].append("No synthesis engines available!")
        
        if not status["windows_media_available"]:
            status["issues"].append("Windows.Media API unavailable (will use SAPI5)")
        
        status["healthy"] = len(status["issues"]) == 0
        
        return status


# Quick test
if __name__ == "__main__":
    print("=" * 70)
    print("AUDIO PIPELINE TEST")
    print("=" * 70)
    print()
    
    pipeline = AudioPipeline(voice="jenny", fallback_enabled=True)
    
    # Validate setup
    setup = pipeline.validate_setup()
    print("Pipeline Status:")
    print(f"  Primary voice: {setup['primary_voice']}")
    print(f"  primry voice valid: {setup['primary_voice_valid']}")
    print(f"  Windows.Media available: {setup['windows_media_available']}")
    print(f"  SAPI5 available: {setup['sapi5_available']}")
    print(f"  Healthy: {setup['healthy']}")
    
    if setup["issues"]:
        print("\nIssues:")
        for issue in setup["issues"]:
            print(f"  ⚠️  {issue}")
    
    # List available voices
    print("\nAvailable Voices:")
    available = pipeline.get_available_voices()
    for engine, voices in available.items():
        if voices:
            print(f"  {engine}: {', '.join(voices)}")
    
    print("\n" + "=" * 70)
