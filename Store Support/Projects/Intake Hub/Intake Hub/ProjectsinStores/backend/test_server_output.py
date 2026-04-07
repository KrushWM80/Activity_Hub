#!/usr/bin/env python3
"""Start server and capture output to see what's happening."""

import subprocess
import time
import os

os.chdir(r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend")

print("[TEST] Starting server in background...")
pythonExe = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
proc = subprocess.Popen(
    [pythonExe, "direct_server.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

print("[TEST] Reading server output for 5 seconds...")
start = time.time()
while time.time() - start < 5:
    line = proc.stdout.readline()
    if line:
        print(f"[SERVER] {line.rstrip()}")
    else:
        print("[SERVER] No more output")
        break

print("[TEST] Terminating server...")
proc.terminate()
try:
    proc.wait(timeout=2)
except subprocess.TimeoutExpired:
    proc.kill()
    
print("[TEST] Done")
