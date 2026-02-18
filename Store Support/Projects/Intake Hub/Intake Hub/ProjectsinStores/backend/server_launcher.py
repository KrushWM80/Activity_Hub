#!/usr/bin/env python3
"""
Server Launcher - Isolates Uvicorn from PowerShell signal handling
Uses subprocess to spawn the server process independently
"""

import subprocess
import sys
import os
import signal
import time
import threading
from pathlib import Path

# Get the backend directory
BACKEND_DIR = Path(__file__).parent.absolute()
os.chdir(BACKEND_DIR)

# Global process reference
server_process = None
shutdown_event = threading.Event()

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    global server_process
    print("\n[*] Received interrupt signal, shutting down server...")
    shutdown_event.set()
    
    if server_process and server_process.poll() is None:
        try:
            if sys.platform == "win32":
                try:
                    os.kill(server_process.pid, signal.CTRL_BREAK_EVENT)
                except:
                    server_process.terminate()
            else:
                os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
            
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
                server_process.wait()
        except Exception as e:
            print(f"[ERROR] Error stopping server: {e}")

def get_python_executable():
    """Get the correct Python executable for the virtual environment"""
    venv_path = BACKEND_DIR.parent / ".code-puppy-venv"
    
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    if python_exe.exists():
        return str(python_exe)
    
    # Fallback to system Python
    return sys.executable

def run_server():
    """Launch the Uvicorn server in an isolated subprocess"""
    global server_process
    
    python_exe = get_python_executable()
    
    print("[*] Server Launcher Starting")
    print(f"[*] Using Python: {python_exe}")
    print(f"[*] Working directory: {BACKEND_DIR}")
    print(f"[*] Starting Uvicorn server on http://0.0.0.0:8001")
    print("[*] Press Ctrl+C to stop the server")
    print("-" * 60)
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGBREAK'):
        signal.signal(signal.SIGBREAK, signal_handler)
    
    # Prepare the command
    cmd = [
        python_exe,
        "-m",
        "uvicorn",
        "main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8001",
        "--timeout-keep-alive",
        "300",
    ]
    
    # Create subprocess with proper signal isolation
    try:
        # On Windows, use CREATE_NEW_PROCESS_GROUP to isolate from parent terminal
        if sys.platform == "win32":
            server_process = subprocess.Popen(
                cmd,
                cwd=str(BACKEND_DIR),
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                env=os.environ.copy(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
            )
        else:
            # On Unix-like systems, use a new process group
            server_process = subprocess.Popen(
                cmd,
                cwd=str(BACKEND_DIR),
                preexec_fn=os.setsid,
                env=os.environ.copy(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
            )
        
        print(f"[OK] Server process started (PID: {server_process.pid})")
        
        # Stream output from the server
        try:
            while not shutdown_event.is_set():
                line = server_process.stdout.readline()
                if not line:
                    # Process finished
                    poll_result = server_process.poll()
                    if poll_result == 0:
                        print("\n[OK] Server shut down gracefully")
                    else:
                        print(f"\n[ERROR] Server exited with code {poll_result}")
                    return poll_result
                
                print(line.rstrip())
        
        except Exception as e:
            print(f"[ERROR] Error monitoring server: {e}")
            return 1
    
    except FileNotFoundError:
        print(f"[ERROR] Python executable not found: {python_exe}")
        return 1
    except Exception as e:
        print(f"[ERROR] Failed to start server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = run_server()
    sys.exit(exit_code)
