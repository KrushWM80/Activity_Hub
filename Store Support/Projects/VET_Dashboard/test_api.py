#!/usr/bin/env python3
"""
Quick API test script to verify V.E.T. Dashboard backend is running
"""

import urllib.request
import urllib.error
import json
import sys

def test_backend():
    """Test if backend is running and API endpoints are responding"""
    
    base_url = "http://127.0.0.1:5001"
    
    print("=" * 80)
    print("V.E.T. DASHBOARD BACKEND TEST")
    print("=" * 80)
    print()
    
    endpoints = {
        "/api/summary": "Get dashboard summary stats",
        "/api/health": "Health check endpoint",
        "/api/data": "Get full data payload",
    }
    
    for endpoint, description in endpoints.items():
        url = base_url + endpoint
        print(f"Testing {endpoint}...")
        print(f"  Description: {description}")
        print(f"  URL: {url}")
        
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                print(f"  ✅ SUCCESS - Response status: {response.status}")
                
                # Show key fields from summary endpoint
                if endpoint == "/api/summary":
                    print(f"     Projects: {data.get('total_projects', 'N/A')}")
                    print(f"     Stores: {data.get('total_stores', 'N/A')}")
                    print(f"     On Track: {data.get('on_track', 'N/A')}")
                    print(f"     At Risk: {data.get('at_risk', 'N/A')}")
                    print(f"     Off Track: {data.get('off_track', 'N/A')}")
                
        except urllib.error.URLError as e:
            print(f"  ❌ FAILED - Cannot connect: {e}")
            print(f"     Make sure the backend is running:")
            print(f"     $ cd 'Store Support/Projects/VET_Dashboard'")
            print(f"     $ python backend.py")
            return False
        except json.JSONDecodeError:
            print(f"  ⚠️  WARNING - Got response but could not parse JSON")
        except Exception as e:
            print(f"  ❌ ERROR - {e}")
            return False
        
        print()
    
    print("=" * 80)
    print("✅ ALL TESTS PASSED - Backend is running correctly!")
    print("=" * 80)
    print()
    print("You can now run the email reporter:")
    print("  $ python send_vet_report.py")
    print()
    
    return True

if __name__ == "__main__":
    success = test_backend()
    sys.exit(0 if success else 1)
