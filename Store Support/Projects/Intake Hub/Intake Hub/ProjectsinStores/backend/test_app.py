#!/usr/bin/env python
"""Minimal test to debug app startup issues"""

print("[1] Importing modules...")
from fastapi import FastAPI
from datetime import datetime
import sys

print("[2] Creating FastAPI app...")
app = FastAPI(title="Test API")

print("[3] Defining routes...")

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

print("[4] Running test with TestClient...")
try:
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    print("[5] Making GET /health request...")
    response = client.get("/health")
    print(f"[6] Response status: {response.status_code}")
    print(f"[7] Response body: {response.json()}")
    print("[OK] Test passed!")
    
except Exception as e:
    print(f"[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
