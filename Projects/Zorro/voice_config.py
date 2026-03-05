"""
Voice Configuration Module - Profiles and fallback logic for audio synthesis
Supports both Windows.Media (modern) and SAPI5 (legacy) voice systems
"""

# Complete voice profile library with all attributes
VOICE_PROFILES = {
    # ========== WINDOWS.MEDIA API VOICES (Modern, High Quality) ==========
    
    "jenny": {
        "engine": "windows_media",
        "display_name": "Microsoft Jenny",
        "full_name": "Microsoft Jenny - English (United States)",
        "gender": "Female",
        "age_group": "Adult",
        "locale": "en-US",
        "style": "Neutral",
        "quality_tier": "High",
        "bitrate": "128k",
        "sample_rate": 16000,
        "speech_rate": 1.0,  # 1.0 = normal, 0.5 = half speed, 2.0 = double speed
        "pitch_adjustment": 1.2,  # 1.0 = normal, 1.2 = slightly higher
        "volume": 100,
        "prosody_style": None,  # Can be: cheerful, sad, serious, etc.
        "voice_id": "Microsoft-Jenny",
        "description": "Professional female voice, clear and natural"
    },
    
    "aria": {
        "engine": "windows_media",
        "display_name": "Microsoft Aria",
        "full_name": "Microsoft Aria - English (United States)",
        "gender": "Female",
        "age_group": "Young Adult",
        "locale": "en-US",
        "style": "Neutral",
        "quality_tier": "High",
        "bitrate": "128k",
        "sample_rate": 16000,
        "speech_rate": 1.0,
        "pitch_adjustment": 1.0,
        "volume": 100,
        "prosody_style": None,
        "voice_id": "Microsoft-Aria",
        "description": "Youthful female voice, energetic and engaging"
    },
    
    "guy": {
        "engine": "windows_media",
        "display_name": "Microsoft Guy",
        "full_name": "Microsoft Guy - English (United States)",
        "gender": "Male",
        "age_group": "Adult",
        "locale": "en-US",
        "style": "Neutral",
        "quality_tier": "High",
        "bitrate": "128k",
        "sample_rate": 16000,
        "speech_rate": 0.95,  # Slightly slower than default
        "pitch_adjustment": 0.95,  # Slightly lower pitch
        "volume": 100,
        "prosody_style": None,
        "voice_id": "Microsoft-Guy",
        "description": "Professional male voice, clear and authoritative"
    },
    
    "mark": {
        "engine": "windows_media",
        "display_name": "Microsoft Mark",
        "full_name": "Microsoft Mark - English (United States)",
        "gender": "Male",
        "age_group": "Older Adult",
        "locale": "en-US",
        "style": "Neutral",
        "quality_tier": "High",
        "bitrate": "128k",
        "sample_rate": 16000,
        "speech_rate": 0.90,  # Slower for clarity
        "pitch_adjustment": 0.90,  # Lower pitch
        "volume": 100,
        "prosody_style": None,
        "voice_id": "Microsoft-Mark",
        "description": "Mature male voice, authoritative and measured"
    },
    
    # ========== SAPI5 LEGACY VOICES (Fallback only) ==========
    
    "david": {
        "engine": "sapi5",
        "display_name": "Microsoft David Desktop",
        "full_name": "Microsoft David Desktop",
        "gender": "Male",
        "age_group": "Adult",
        "locale": "en-US",
        "style": "Neutral",
        "quality_tier": "Medium",
        "bitrate": "64k",  # SAPI5 is lower bitrate
        "sample_rate": 8000,  # SAPI5 lower sample rate
        "speech_rate": -2,  # SAPI5 rate parameter (-10 to +10)
        "pitch_adjustment": None,  # SAPI5 doesn't support pitch separately
        "volume": 100,
        "prosody_style": None,
        "voice_id": "SAPI5-David",
        "description": "SAPI5 legacy voice - fallback option"
    },
    
    "zira": {
        "engine": "sapi5",
        "display_name": "Microsoft Zira Desktop",
        "full_name": "Microsoft Zira Desktop",
        "gender": "Female",
        "age_group": "Adult",
        "locale": "en-US",
        "style": "Neutral",
        "quality_tier": "Medium",
        "bitrate": "64k",
        "sample_rate": 8000,
        "speech_rate": -2,  # SAPI5 rate parameter
        "pitch_adjustment": None,
        "volume": 100,
        "prosody_style": None,
        "voice_id": "SAPI5-Zira",
        "description": "SAPI5 legacy voice - fallback option"
    },
}

# Primary selection order: tries each voice in order until one succeeds
FALLBACK_CHAIN = [
    "jenny",    # First choice - modern, natural, female
    "aria",     # Second - modern, youthful female
    "guy",      # Third - modern, professional male
    "mark",     # Fourth - modern, mature male
    "david",    # Fallback - SAPI5, legacy but reliable
    "zira",     # Last resort - SAPI5 female
]

# Groups for easy access
MODERN_VOICES = ["jenny", "aria", "guy", "mark"]
LEGACY_VOICES = ["david", "zira"]
FEMALE_VOICES = ["jenny", "aria", "zira"]
MALE_VOICES = ["guy", "mark", "david"]

# Default configuration
DEFAULT_VOICE = "jenny"
DEFAULT_ENGINE = "windows_media"


def get_voice_profile(voice_name: str) -> dict:
    """
    Retrieve complete voice profile by name
    
    Args:
        voice_name: Voice identifier (e.g., 'jenny', 'david')
    
    Returns:
        Dictionary with all voice attributes, or None if not found
    """
    return VOICE_PROFILES.get(voice_name.lower())


def get_voices_by_gender(gender: str) -> list:
    """Get all available voices for a specific gender"""
    return [
        name for name, profile in VOICE_PROFILES.items()
        if profile["gender"].lower() == gender.lower()
    ]


def get_voices_by_engine(engine: str) -> list:
    """Get all voices for a specific synthesis engine"""
    return [
        name for name, profile in VOICE_PROFILES.items()
        if profile["engine"].lower() == engine.lower()
    ]


def is_voice_available(voice_name: str) -> bool:
    """Check if a voice is defined in profiles"""
    return voice_name.lower() in VOICE_PROFILES


def get_next_fallback(current_voice: str) -> str:
    """
    Get next voice in fallback chain after current voice
    
    Args:
        current_voice: Current voice that failed
    
    Returns:
        Next voice to try, or None if no more fallbacks
    """
    try:
        current_index = FALLBACK_CHAIN.index(current_voice.lower())
        if current_index + 1 < len(FALLBACK_CHAIN):
            return FALLBACK_CHAIN[current_index + 1]
    except ValueError:
        pass
    return None


def validate_voice_config(voice_name: str) -> tuple[bool, str]:
    """
    Validate voice configuration and report issues
    
    Returns:
        Tuple of (is_valid, message)
    """
    if not voice_name:
        return False, "Voice name cannot be empty"
    
    profile = get_voice_profile(voice_name)
    if not profile:
        available = ", ".join(VOICE_PROFILES.keys())
        return False, f"Voice '{voice_name}' not found. Available: {available}"
    
    # Validate required fields
    required_fields = ["engine", "display_name", "gender", "quality_tier"]
    missing = [f for f in required_fields if not profile.get(f)]
    if missing:
        return False, f"Voice profile missing fields: {missing}"
    
    return True, f"Voice '{voice_name}' ({profile['display_name']}) is valid"


def get_voice_summary(voice_name: str) -> str:
    """Get human-readable summary of a voice"""
    profile = get_voice_profile(voice_name)
    if not profile:
        return f"Unknown voice: {voice_name}"
    
    return (
        f"{profile['display_name']} | "
        f"{profile['gender']} {profile['age_group']} | "
        f"{profile['engine'].upper()} | "
        f"Quality: {profile['quality_tier']}"
    )


# Quality presets for common use cases
QUALITY_PRESETS = {
    "broadcast": {
        "voices": ["jenny", "aria", "guy", "mark"],
        "bitrate": "128k",
        "sample_rate": 16000,
        "description": "Professional broadcast quality"
    },
    "podcast": {
        "voices": ["jenny", "aria", "guy", "mark"],
        "bitrate": "128k",
        "sample_rate": 16000,
        "description": "Podcast-grade audio"
    },
    "web": {
        "voices": ["jenny", "david"],
        "bitrate": "96k",
        "sample_rate": 16000,
        "description": "Web streaming quality"
    },
    "accessibility": {
        "voices": ["david", "zira"],
        "bitrate": "64k",
        "sample_rate": 16000,
        "description": "Accessibility/screenreader quality"
    },
}


if __name__ == "__main__":
    # Test voice configuration
    print("=" * 70)
    print("VOICE CONFIGURATION TEST")
    print("=" * 70)
    print()
    
    print("Available Voices:")
    for voice_name in VOICE_PROFILES:
        is_valid, msg = validate_voice_config(voice_name)
        status = "✅" if is_valid else "❌"
        print(f"  {status} {get_voice_summary(voice_name)}")
    
    print()
    print(f"Fallback Chain: {' → '.join(FALLBACK_CHAIN)}")
    print()
    print("Voice Groups:")
    print(f"  Modern: {', '.join(MODERN_VOICES)}")
    print(f"  Legacy: {', '.join(LEGACY_VOICES)}")
    print(f"  Female: {', '.join(FEMALE_VOICES)}")
    print(f"  Male: {', '.join(MALE_VOICES)}")
    print()
    print("=" * 70)
