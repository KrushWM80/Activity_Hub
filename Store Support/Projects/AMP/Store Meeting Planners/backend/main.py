"""Store Meeting Planner — FastAPI Backend"""
import json
import os
import uuid
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import DatabaseService
from amp_ingestion import run_amp_sync
import traceback

# =============================================
# APP SETUP
# =============================================

PORT = int(os.getenv("PORT", "8090"))
HOST = os.getenv("HOST", "0.0.0.0")

app = FastAPI(title="Store Meeting Planner API")


@app.middleware("http")
async def catch_all_errors(request: Request, call_next):
    """Global safety net — log any unhandled exception instead of crashing."""
    try:
        return await call_next(request)
    except Exception as exc:
        print(f"[FATAL] Unhandled error on {request.method} {request.url}: {exc}")
        traceback.print_exc()
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"detail": str(exc)})


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db = DatabaseService()

# Uploads directory
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

# =============================================
# AUTH
# =============================================

def load_admin_access_list() -> dict:
    try:
        path = os.path.join(os.path.dirname(__file__), "admin-access.json")
        with open(path, "r") as f:
            data = json.load(f)
        return {
            "admins": [e.lower() for e in data.get("authorized_admins", [])],
            "admin_usernames": [u.lower() for u in data.get("admin_usernames", [])],
            "fallback_password": data.get("fallback_password", ""),
        }
    except Exception as e:
        print(f"[AUTH] Error loading admin access: {e}")
        return {"admins": [], "admin_usernames": [], "fallback_password": ""}

admin_config = load_admin_access_list()


def get_windows_username() -> str:
    username = os.getenv("USERNAME", "").lower()
    return username if username else "unknown"


def get_user_email(username: str) -> str:
    if "@" in username:
        return username
    return f"{username}@homeoffice.wal-mart.com"


def is_admin(username: str) -> bool:
    uname = username.lower()
    email = get_user_email(uname)
    return uname in admin_config["admin_usernames"] or email in admin_config["admins"]


# =============================================
# APScheduler — AMP auto-sync
# =============================================

scheduler = None

def start_scheduler():
    global scheduler
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        interval = int(os.getenv("AMP_SYNC_INTERVAL_MINUTES", "30"))
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            lambda: run_amp_sync(db),
            "interval",
            minutes=interval,
            id="amp_sync",
            replace_existing=True,
        )
        scheduler.start()
        print(f"[Scheduler] AMP sync running every {interval} minutes")
    except ImportError:
        print("[Scheduler] apscheduler not installed — AMP sync available via manual trigger only")
    except Exception as e:
        print(f"[Scheduler] Failed to start: {e}")


@app.on_event("startup")
async def startup():
    print("[Startup] Running initial AMP sync...")
    try:
        run_amp_sync(db)
    except Exception as e:
        print(f"[Startup] Initial AMP sync error: {e}")
    start_scheduler()


@app.on_event("shutdown")
async def shutdown():
    if scheduler:
        scheduler.shutdown(wait=False)


# =============================================
# FAVICON (prevent 404)
# =============================================

@app.get("/favicon.ico")
async def favicon():
    fav_path = Path(__file__).parent.parent / "frontend" / "favicon.ico"
    if fav_path.exists():
        return FileResponse(str(fav_path))
    # Return a minimal 1x1 transparent ico
    from fastapi.responses import Response
    return Response(content=b"", media_type="image/x-icon", status_code=204)


# =============================================
# API: Health
# =============================================

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "bigquery_connected": db.is_connected(),
        "timestamp": datetime.utcnow().isoformat(),
    }


# =============================================
# API: User / Auth
# =============================================

@app.get("/api/user")
async def get_current_user():
    username = get_windows_username()
    email = get_user_email(username)
    return {
        "username": username,
        "email": email,
        "is_admin": is_admin(username),
    }


# =============================================
# API: Calendar
# =============================================

@app.get("/api/calendar")
async def get_calendar(start_date: str = Query(...), end_date: str = Query(...)):
    events = db.get_calendar_events(start_date, end_date)
    slots = db.get_slot_availability(start_date, end_date)
    return {"events": events, "slots": slots}


@app.get("/api/protected-weeks")
async def get_protected_weeks(fy: int = Query(...)):
    weeks = db.get_protected_weeks(fy)
    return {"protected_weeks": weeks}


# =============================================
# API: Requests
# =============================================

@app.get("/api/requests")
async def get_all_requests(
    status: Optional[str] = None,
    source: Optional[str] = None,
    meeting_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """Admin-only: get all meeting requests."""
    username = get_windows_username()
    if not is_admin(username):
        raise HTTPException(status_code=403, detail="Admin access required")
    rows = db.get_all_requests(status=status, source=source,
                                meeting_type=meeting_type,
                                start_date=start_date, end_date=end_date)
    return {"requests": rows}


@app.get("/api/requests/mine")
async def get_my_requests():
    """Current user's requests."""
    username = get_windows_username()
    email = get_user_email(username)
    rows = db.get_user_requests(email)
    return {"requests": rows}


@app.post("/api/requests")
async def submit_request(
    Title: str = Form(...),
    Start_Date: str = Form(...),
    End_Date: str = Form(...),
    Meeting_Duration: int = Form(...),
    Meeting_Type: str = Form(...),
    Impacted_Shift: int = Form(...),
    Store_Selection: str = Form(...),
    Meeting_Reoccurrence: str = Form("None"),
    AMP_Activity: bool = Form(False),
    AMP_Activity_URL: str = Form(""),
    store_file: Optional[UploadFile] = File(None),
):
    """Submit a new meeting request from the intake form."""
    username = get_windows_username()
    email = get_user_email(username)
    name = username  # Windows username as display name

    data = {
        "Title": Title,
        "Start_Date": Start_Date,
        "End_Date": End_Date,
        "Meeting_Duration": Meeting_Duration,
        "Meeting_Type": Meeting_Type,
        "Impacted_Shift": Impacted_Shift,
        "Store_Selection": Store_Selection,
        "Meeting_Reoccurrence": Meeting_Reoccurrence,
        "AMP_Activity": AMP_Activity,
        "AMP_Activity_URL": AMP_Activity_URL,
    }

    # Handle custom store list file upload
    if store_file and Store_Selection == "Custom List":
        if store_file.size > MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large (max 10 MB)")
        # Validate file extension
        allowed_ext = {".csv", ".xlsx", ".xls", ".txt"}
        ext = Path(store_file.filename).suffix.lower()
        if ext not in allowed_ext:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
        file_id = str(uuid.uuid4())[:8]
        safe_name = f"{file_id}_{Path(store_file.filename).name}"
        file_path = UPLOAD_DIR / safe_name
        with open(file_path, "wb") as f:
            content = await store_file.read()
            f.write(content)
        data["Store_Selection"] = f"Custom List: {safe_name}"

    result = db.submit_request(data, email, name)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@app.put("/api/requests/{request_id}")
async def update_request(request_id: str, body: dict):
    """Admin: update a request (status, comment, start_time, meeting_link)."""
    username = get_windows_username()
    if not is_admin(username):
        raise HTTPException(status_code=403, detail="Admin access required")
    email = get_user_email(username)
    try:
        result = db.update_request(request_id, body, email)
        return result
    except Exception as e:
        print(f"[ERROR] update_request failed: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/requests/{request_id}/complete")
async def complete_request(request_id: str, body: dict):
    """User completes missing fields on a Pending request."""
    username = get_windows_username()
    email = get_user_email(username)
    result = db.complete_pending_request(request_id, body, email)
    return result


# =============================================
# API: Store Data
# =============================================

@app.get("/api/store-data")
async def get_store_data():
    stores = db.get_store_data()
    return {"stores": stores}


# =============================================
# API: AMP Sync (Manual trigger)
# =============================================

@app.post("/api/amp-sync")
async def trigger_amp_sync():
    """Admin-only: manually trigger AMP sync."""
    username = get_windows_username()
    if not is_admin(username):
        raise HTTPException(status_code=403, detail="Admin access required")
    stats = run_amp_sync(db)
    return {"message": "AMP sync complete", "stats": stats}


# =============================================
# API: Meeting Tracker Report
# =============================================

@app.get("/api/reports/meeting-tracker")
async def meeting_tracker_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """Admin: get Calls to Stores report data."""
    username = get_windows_username()
    if not is_admin(username):
        raise HTTPException(status_code=403, detail="Admin access required")
    rows = db.get_meeting_tracker_report(start_date, end_date)
    return {"report": rows}


# =============================================
# API: Compliance Scan
# =============================================

@app.get("/api/reports/compliance-scan")
async def compliance_scan():
    """Admin: scan AMP events for meetings missing from Meeting Planner."""
    username = get_windows_username()
    if not is_admin(username):
        raise HTTPException(status_code=403, detail="Admin access required")
    results = db.scan_compliance_gaps()
    return results


# =============================================
# STATIC FILES & FRONTEND
# =============================================

frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(str(frontend_path / "index.html"))


# =============================================
# RUN
# =============================================

if __name__ == "__main__":
    print(f"[Server] Starting Store Meeting Planner on {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
