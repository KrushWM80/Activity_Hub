#!/usr/bin/env python3
"""Start server and test /api/projects endpoint immediately."""

import subprocess
import time
import requests
import sys
import os

os.chdir(r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend")

# Start server in background
print("[TEST] Starting server in background...")
pythonExe = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
proc = subprocess.Popen([pythonExe, "direct_server.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# Give it a bit of time to start
time.sleep(3)

# Try to hit the API
print("[TEST] Testing /api/projects endpoint...")
try:
    response = requests.get("http://localhost:8001/api/projects?limit=10", timeout=10)
    print(f"[TEST] Status: {response.status_code}")
    print(f"[TEST] Response length: {len(response.text)}")
    if response.status_code == 200:
        data = response.json()
        print(f"[TEST] SUCCESS! Got {len(data)} projects")
        if data:
            print(f"[TEST] First project: {data[0]['project_id']}")
    else:
        print(f"[TEST] ERROR! Status {response.status_code}")
        print(f"[TEST] Response: {response.text[:500]}")
except Exception as e:
    print(f"[TEST] Connection failed: {e}")

# Kill the server process
print("[TEST] Terminating server...")
proc.terminate()
proc.wait(timeout=5)
print("[TEST] Done")
