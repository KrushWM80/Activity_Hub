#!/usr/bin/env python3
"""Minimal test server to verify uvicorn works."""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/test")
def test_route():
    return {"status": "ok"}

if __name__ == "__main__":
    print("[TEST] Starting minimal test server...")
    try:
        uvicorn.run(
            app=app,
            host="0.0.0.0",
            port=8002,
            reload=False,
            workers=1,
            log_level="info",
        )
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    print("[TEST] Server exited")
