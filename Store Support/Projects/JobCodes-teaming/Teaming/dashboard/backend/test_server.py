"""
Minimal test server to debug worker data endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
import os
import sys

app = FastAPI(title="Test Server")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEAMING_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

print(f"BASE_DIR: {BASE_DIR}")
print(f"TEAMING_DIR: {TEAMING_DIR}")

@app.get("/Worker_Names_Stores_Missing_JobCodes_Optimized.json")
async def get_worker_data_optimized():
    try:
        print("[ENDPOINT] Called /Worker_Names_Stores_Missing_JobCodes_Optimized.json")
        json_file = os.path.join(TEAMING_DIR, "Worker_Names_Stores_Missing_JobCodes_Optimized.json")
        print(f"[DEBUG] File path: {json_file}")
        print(f"[DEBUG] File exists: {os.path.exists(json_file)}")
        
        if not os.path.exists(json_file):
            print(f"[ERROR] File not found")
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"[SUCCESS] Loaded {len(data)} records")
            return data
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Exception: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/Worker_Names_Stores_Missing_JobCodes.json")
async def get_worker_data():
    try:
        print("[ENDPOINT] Called /Worker_Names_Stores_Missing_JobCodes.json")
        json_file = os.path.join(TEAMING_DIR, "Worker_Names_Stores_Missing_JobCodes.json")
        print(f"[DEBUG] File path: {json_file}")
        print(f"[DEBUG] File exists: {os.path.exists(json_file)}")
        
        if not os.path.exists(json_file):
            print(f"[ERROR] File not found")
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"[SUCCESS] Loaded {len(data)} records")
            return data
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Exception: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("Starting minimal test server on port 8082...")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8082)
