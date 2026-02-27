#!/usr/bin/env python
"""
Quick API connectivity test - Non-interactive
Run this to verify the API is accessible
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.providers.walmart_media_studio import WalmartMediaStudioProvider

def main():
    print("=" * 60)
    print("WALMART GENAI MEDIA STUDIO - QUICK TEST")
    print("=" * 60)
    
    # Initialize provider
    print("\n[*] Initializing provider...")
    provider = WalmartMediaStudioProvider()
    
    # Get info
    info = provider.get_provider_info()
    print(f"\n[+] API Endpoint: {info['api_endpoint']}")
    print(f"[+] OpenAPI Version: {info.get('api_version', 'unknown')}")
    
    # Test connectivity
    print("\n[*] Testing API connectivity...")
    if provider.is_available():
        print("[✓] API is AVAILABLE")
        print(f"    Video Models: {', '.join(info['supported_models']['video'])}")
        print(f"    Image Models: {', '.join(info['supported_models']['image'])}")
        print(f"    Duration: {info['supported_durations']}")
        print(f"    Aspect Ratios: {', '.join(info['supported_aspect_ratios'])}")
        return True
    else:
        print("[✗] API is NOT available")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
