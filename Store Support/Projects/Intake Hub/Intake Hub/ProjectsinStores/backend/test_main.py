#!/usr/bin/env python
"""Test if main app can be imported and tested"""

print("[1] Importing main app...")
try:
    from main import app
    print("[OK] main.app imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import main.app: {e}")
    import traceback
    traceback.print_exc()
    import sys
    sys.exit(1)

print("[2] Testing with TestClient...")
try:
    from fastapi.testclient import TestClient
    client = TestClient(app)
    print("[OK] TestClient created")
    
    print("[3] Testing /api/health...")
    response = client.get("/api/health")
    print(f"[OK] Status: {response.status_code}")
    print(f"[OK] Body: {response.json()}")
    
except Exception as e:
    print(f"[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()
    import sys
    sys.exit(1)

print("[SUCCESS] All tests passed!")
