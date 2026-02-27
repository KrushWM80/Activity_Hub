"""
Walmart Media Studio Integration - Quick Setup

This script helps you set up and test the Walmart GenAI Media Studio integration.
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Print welcome banner."""
    print("=" * 70)
    print("  🎬 Zorro Video Generator - Walmart Media Studio Setup")
    print("=" * 70)
    print()

def check_env_file():
    """Check if .env file exists."""
    env_file = Path(".env")
    template_file = Path(".env.template")
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print()
        print("📝 Creating .env from template...")
        
        if template_file.exists():
            import shutil
            shutil.copy(template_file, env_file)
            print("✅ .env file created!")
            print()
            print("⚠️  IMPORTANT: Edit .env and add your WALMART_SSO_TOKEN")
            print()
            return False
        else:
            print("❌ Template file not found. Please create .env manually.")
            return False
    
    return True

def check_sso_token():
    """Check if SSO token is configured."""
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv("WALMART_SSO_TOKEN")
    
    if not token or token == "your_sso_token_here":
        print("❌ WALMART_SSO_TOKEN not configured!")
        print()
        print("📋 How to get your SSO token:")
        print("   1. Open https://mediagenai.walmart.com/")
        print("   2. Login with Walmart SSO")
        print("   3. Open browser DevTools (F12)")
        print("   4. Go to Network tab")
        print("   5. Make a request (generate something)")
        print("   6. Look for 'Authorization: Bearer ...' header")
        print("   7. Copy the token and add to .env file")
        print()
        print("   OR request API access from #help-genai-media-studio")
        print()
        return False
    
    print("✅ SSO token configured!")
    return True

def test_provider():
    """Test Media Studio provider."""
    print()
    print("🧪 Testing Walmart Media Studio provider...")
    print()
    
    try:
        from src.providers.walmart_media_studio import WalmartMediaStudioProvider
        
        provider = WalmartMediaStudioProvider()
        info = provider.get_provider_info()
        
        print("Provider Information:")
        print(f"  Name: {info['name']}")
        print(f"  Provider: {info['provider']}")
        print(f"  Models: {', '.join(info['models'])}")
        print(f"  Authenticated: {info['authenticated']}")
        print(f"  API Endpoint: {info['api_endpoint']}")
        print()
        
        if info['authenticated']:
            print("✅ Provider initialized successfully!")
            
            # Test availability
            print()
            print("🔍 Testing API availability...")
            available = provider.is_available()
            
            if available:
                print("✅ Media Studio API is accessible!")
                return True
            else:
                print("⚠️  Could not reach Media Studio API")
                print("   This might be normal if API endpoint is not finalized")
                print("   Contact #help-genai-media-studio for API documentation")
                return False
        else:
            print("⚠️  Provider initialized but not authenticated")
            print("   Add WALMART_SSO_TOKEN to .env file")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print()
        print("Make sure you're in the zorro directory and dependencies are installed:")
        print("   pip install -r requirements.txt")
        return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_next_steps(all_checks_passed: bool):
    """Show next steps."""
    print()
    print("=" * 70)
    
    if all_checks_passed:
        print("🎉 Setup Complete! Ready to generate videos!")
        print()
        print("Next Steps:")
        print("  1. Launch the GUI:")
        print("     python run_gui.py")
        print()
        print("  2. Try generating a video with a preset message")
        print()
        print("  3. Monitor generation in the GUI")
        print()
        print("Documentation:")
        print("  • WALMART_INTEGRATION.md - Full integration guide")
        print("  • QUICKSTART_GUI.md - GUI tutorial")
        print("  • docs/GUI_GUIDE.md - Complete manual")
    else:
        print("⚠️  Setup Incomplete")
        print()
        print("To finish setup:")
        print("  1. Get SSO token from https://mediagenai.walmart.com/")
        print("  2. Add to .env file: WALMART_SSO_TOKEN=your_token")
        print("  3. Run this script again: python setup_walmart.py")
        print()
        print("Need Help?")
        print("  • Slack: #help-genai-media-studio")
        print("  • Request API access from Next Gen Content DS team")
        print("  • See WALMART_INTEGRATION.md for details")
    
    print("=" * 70)

def main():
    """Main setup flow."""
    print_banner()
    
    # Check environment
    env_exists = check_env_file()
    
    if not env_exists:
        show_next_steps(False)
        return
    
    # Check SSO token
    token_configured = check_sso_token()
    
    # Test provider
    provider_works = test_provider()
    
    # Show next steps
    all_good = env_exists and token_configured and provider_works
    show_next_steps(all_good)

if __name__ == "__main__":
    main()
