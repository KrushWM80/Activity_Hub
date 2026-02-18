#!/usr/bin/env python3
"""
Windows-compatible server runner for Projects in Stores Dashboard.
Handles asyncio event loop properly and isolates signal handling.
"""

import sys
import os

def main():
    """Run the server with proper Windows compatibility."""
    # CRITICAL: Set the event loop policy BEFORE importing uvicorn
    if sys.platform == "win32":
        import asyncio
        # Use WindowsSelectorEventLoopPolicy to avoid ProactorEventLoop signal issues
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Now import uvicorn (AFTER setting event loop policy)
    import uvicorn
    
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    print("[*] Starting Projects in Stores Dashboard API")
    print(f"[*] Working directory: {backend_dir}")
    print("[*] Server: http://localhost:8001")
    print("[*] Press Ctrl+C to stop")
    print("-" * 50)
    
    # Run uvicorn with Windows-safe settings
    # Key settings:
    # - reload=False: Avoids file watching issues
    # - workers=1: Single worker mode avoids multiprocessing
    # - loop="asyncio": Explicit asyncio loop 
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        workers=1,
        loop="asyncio",
        timeout_keep_alive=30,
        access_log=True,
        log_level="info",
    )

if __name__ == "__main__":
    main()
