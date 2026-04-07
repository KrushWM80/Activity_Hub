#!/usr/bin/env python3
"""Direct server runner without run_server.py intermediary."""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run
try:
    print("[DIRECT] Importing FastAPI app...")
    from main import app
    print("[DIRECT] Importing uvicorn...")
    import uvicorn
    
    print("[DIRECT] Starting server on port 8001...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        reload=False,
        workers=1,
        log_level="info",
        access_log=True
    )
except KeyboardInterrupt:
    print("\n[DIRECT] Server interrupted")
except Exception as e:
    print(f"[DIRECT] ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
