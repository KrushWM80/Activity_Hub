#!/usr/bin/env python3
"""Test server with a simple /api/projects endpoint without response_model validation."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
import uvicorn
from sqlite_cache import get_cache

app = FastAPI()
sqlite_cache = get_cache()

@app.get("/api/projects")
async def get_projects(limit: int = 10):
    """Raw projects endpoint without response_model validation."""
    print(f"[ENDPOINT] /api/projects called with limit={limit}")
    projects = sqlite_cache.get_projects(limit=limit)
    print(f"[ENDPOINT] Got {len(projects)} projects, returning as JSON...")
    return projects

@app.get("/api/projects-raw")
async def get_projects_raw(limit: int = 10):
    """Raw projects endpoint without response_model validation."""
    print(f"[ENDPOINT] Raw projects requested with limit={limit}")
    projects = sqlite_cache.get_projects(limit=limit)
    print(f"[ENDPOINT] Got {len(projects)} projects, converting to JSON...")
    return projects

@app.get("/api/summary")
async def get_summary():
    """Summary endpoint."""
    cached_summary = sqlite_cache.get_summary()
    return cached_summary

if __name__ == "__main__":
    print("[TEST SERVER] Starting...")
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8001,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n[TEST SERVER] Terminated")
    except Exception as e:
        print(f"[TEST SERVER] Error: {e}")
        import traceback
        traceback.print_exc()
