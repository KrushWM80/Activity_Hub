#!/usr/bin/env python3
"""Test API with different limits."""

import subprocess
import time
import requests
import os

os.chdir(r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend")

print("[TEST] Starting server...")
pythonExe = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
proc = subprocess.Popen([pythonExe, "direct_server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

time.sleep(3)

tests = [
    ("?limit=10", 10),
    ("?limit=100", 100),
    ("?limit=1000", 1000),
    ("?module=Realty&limit=100", "Realty (first 100)"),
    ("?module=Operations&limit=100", "Operations (first 100)"),
]

for endpoint, desc in tests:
    try:
        response = requests.get(f"http://localhost:8001/api/projects{endpoint}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"[TEST] {desc}: Got {len(data)} projects")
            if data:
                print(f"       First project: {data[0].get('project_id', 'N/A')}")
        else:
            print(f"[TEST] {desc}: Status {response.status_code}")
    except Exception as e:
        print(f"[TEST] {desc}: Error - {e}")

print("[TEST] Terminating server...")
proc.terminate()
proc.wait(timeout=5)
print("[TEST] Done")
