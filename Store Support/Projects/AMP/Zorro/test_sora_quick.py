"""
Quick test to verify OpenAI Sora 2 API access.

This script checks:
1. API key is loaded
2. Can connect to OpenAI API
3. Has access to Sora models

Usage: python test_sora_quick.py
"""

import os
import sys
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def test_api_key():
    """Test that API key is loaded."""
    print("=" * 60)
    print("OpenAI Sora 2 - Quick API Test")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n❌ ERROR: OPENAI_API_KEY not found in .env file")
        return False
    
    print(f"\n✅ API Key loaded: {api_key[:20]}...")
    return True


def test_connection():
    """Test connection to OpenAI API."""
    print("\n📡 Testing OpenAI API connection...")
    
    try:
        import requests
        
        api_key = os.getenv("OPENAI_API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Test with models endpoint (doesn't use credits)
        response = requests.get(
            "https://api.openai.com/v1/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Successfully connected to OpenAI API")
            
            # Check if Sora models are available
            models = response.json()
            model_ids = [m['id'] for m in models.get('data', [])]
            
            sora_models = [m for m in model_ids if 'sora' in m.lower()]
            if sora_models:
                print(f"✅ Sora models available: {', '.join(sora_models)}")
            else:
                print("⚠️  Sora models not found in model list")
                print("   This may mean:")
                print("   1. Your API key doesn't have Sora access yet")
                print("   2. Sora API uses different endpoint structure")
                print("   3. Need to apply for Sora beta access")
            
            return True
            
        elif response.status_code == 401:
            print("❌ Authentication failed - Invalid API key")
            return False
            
        elif response.status_code == 403:
            print("❌ Access forbidden - API key may not have proper permissions")
            return False
            
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            print(f"   Message: {response.text[:200]}")
            return False
            
    except ImportError:
        print("❌ 'requests' library not installed")
        print("   Run: pip install requests")
        return False
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False


def test_sora_provider():
    """Test the Sora provider implementation."""
    print("\n🎬 Testing Sora provider implementation...")
    
    try:
        from src.providers.sora_provider import SoraVideoProvider
        
        provider = SoraVideoProvider(model="sora-2")
        print("✅ Sora provider initialized successfully")
        
        info = provider.get_provider_info()
        print(f"\n📋 Provider Info:")
        print(f"   Name: {info['name']}")
        print(f"   Model: {info['model']}")
        print(f"   Endpoint: {info['api_endpoint']}")
        print(f"   Authenticated: {info['authenticated']}")
        
        # Test availability
        if provider.is_available():
            print("\n✅ Sora API is available and ready to use!")
            print("\n🎉 SUCCESS! You can now generate videos with Sora 2")
            print("\nNext steps:")
            print("1. Run full test: python test_sora_integration.py")
            print("2. Or use the GUI: python app.py")
            return True
        else:
            print("\n⚠️  Sora API not fully available")
            print("\nPossible reasons:")
            print("1. Sora 2 API may not be publicly available yet")
            print("2. Your API key may need Sora access enabled")
            print("3. May need to apply at: https://openai.com/sora")
            print("\nYour integration code is ready - just needs API access!")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Ensure src/providers/sora_provider.py exists")
        return False
        
    except Exception as e:
        print(f"❌ Provider error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n")
    
    # Test 1: API Key
    if not test_api_key():
        return
    
    # Test 2: Connection
    test_connection()
    
    # Test 3: Provider
    test_sora_provider()
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
