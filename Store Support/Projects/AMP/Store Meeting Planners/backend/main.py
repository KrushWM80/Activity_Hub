"""Store Meeting Planner — FastAPI Backend"""
import json
import os
import subprocess
import uuid
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

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
    """Get the real logged-in Windows username.
    When running as SYSTEM (scheduled task), USERNAME is the machine account
    (e.g. weus42608431466$). Fall back to multiple detection methods."""
    username = os.getenv("USERNAME", "").lower()
    # Machine accounts end with '$' — not a real user
    # 'systemprofile' is the SYSTEM home dir, also not a real user
    _bad = lambda u: (not u or u.endswith("$") or u in ("systemprofile", "system", "unknown", ""))
    if _bad(username):
        # Try USERPROFILE (C:\Users\krush -> krush)
        profile = os.getenv("USERPROFILE", "")
        if profile:
            username = Path(profile).name.lower()
    if _bad(username):
        # Try extracting from the python executable path
        # e.g. C:\Users\krush\...\python.exe -> krush
        import sys
        exe = sys.executable or ""
        parts = Path(exe).parts
        for i, p in enumerate(parts):
            if p.lower() == "users" and i + 1 < len(parts):
                username = parts[i + 1].lower()
                break
    if _bad(username):
        # Try expanduser
        home = os.path.expanduser("~")
        if home:
            username = Path(home).name.lower()
    if _bad(username):
        # Try GCP credentials path
        creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
        if creds:
            cparts = Path(creds).parts
            for i, p in enumerate(cparts):
                if p.lower() == "users" and i + 1 < len(cparts):
                    username = cparts[i + 1].lower()
                    break
    return username if not _bad(username) else "unknown"


def get_user_email(username: str) -> str:
    if "@" in username:
        return username
    return f"{username}@homeoffice.wal-mart.com"


def is_admin(username: str) -> bool:
    uname = username.lower()
    email = get_user_email(uname)
    return uname in admin_config["admin_usernames"] or email in admin_config["admins"]


def send_outlook_email(to_email: str, subject: str, html_body: str) -> bool:
    """Send an email via Outlook COM (PowerShell subprocess). Returns True on success."""
    import subprocess
    # Escape single quotes in the HTML body for PowerShell
    escaped_body = html_body.replace("'", "''")
    escaped_subject = subject.replace("'", "''")
    escaped_to = to_email.replace("'", "''")
    ps_script = f"""
$Outlook = New-Object -ComObject Outlook.Application
$Mail = $Outlook.CreateItem(0)
$Mail.To = '{escaped_to}'
$Mail.Subject = '{escaped_subject}'
$Mail.HTMLBody = '{escaped_body}'
$Mail.Send()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($Mail) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($Outlook) | Out-Null
"""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(f"[Email] Sent to {to_email}: {subject}")
            return True
        else:
            print(f"[Email] Failed: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[Email] Error: {e}")
        return False


# =============================================
# APScheduler — AMP auto-sync
# =============================================

scheduler = None

def send_daily_compliance_email():
    """Run compliance scan and email results to admins (called by scheduler at 6am)."""
    try:
        results = db.scan_compliance_gaps()
        flagged = results.get("flagged", [])
        total = results.get("total_scanned", 0)
        scan_start = results.get("scan_start", "")
        scan_end = results.get("scan_end", "")

        # Build HTML email
        rows_html = ""
        for f in flagged:
            conf_color = "#dc3545" if f["confidence"] == "HIGH" else "#ffc107"
            amp_link = f'<a href="https://amp2-cms.prod.walmart.com/message/{f["event_id"]}/10/2027">View</a>' if f.get("event_id") else ""
            rows_html += f"""<tr>
                <td style="color:{conf_color};font-weight:bold">{f['confidence']}</td>
                <td>{f['title']}</td>
                <td>{f['message_type']}</td>
                <td>{f['start_date']} - {f['end_date']}</td>
                <td>{f.get('author','')}</td>
                <td>{f.get('stores','—')}</td>
                <td>{amp_link}</td>
            </tr>"""

        if flagged:
            body_html = f"""<html><body style="font-family:Arial,sans-serif;">
            <div style="background:#0071ce;color:#fff;padding:15px;border-radius:5px;">
                <h2>Store Meeting Planner — Daily Compliance Scan</h2>
                <p>{datetime.now().strftime('%B %d, %Y %I:%M %p')}</p>
            </div>
            <div style="margin:15px 0;padding:10px;background:#fff3cd;border-radius:5px;">
                <strong>{len(flagged)} compliance gaps found</strong> out of {total} AMP events scanned
                (Range: {scan_start} to {scan_end})
            </div>
            <table style="width:100%;border-collapse:collapse;font-size:0.9em;">
                <thead><tr style="background:#f1f8ff;">
                    <th style="padding:8px;border:1px solid #ddd;text-align:left">Confidence</th>
                    <th style="padding:8px;border:1px solid #ddd;text-align:left">Title</th>
                    <th style="padding:8px;border:1px solid #ddd;text-align:left">Type</th>
                    <th style="padding:8px;border:1px solid #ddd;text-align:left">Dates</th>
                    <th style="padding:8px;border:1px solid #ddd;text-align:left">Author</th>
                    <th style="padding:8px;border:1px solid #ddd;text-align:left">Stores</th>
                    <th style="padding:8px;border:1px solid #ddd;text-align:left">AMP</th>
                </tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
            <p style="margin-top:15px;font-size:0.85em;color:#666">
                <a href="http://weus42608431466:8090/StoreMeetingPlanner">Open Store Meeting Planner</a>
            </p>
            </body></html>"""
        else:
            body_html = f"""<html><body style="font-family:Arial,sans-serif;">
            <div style="background:#0071ce;color:#fff;padding:15px;border-radius:5px;">
                <h2>Store Meeting Planner — Daily Compliance Scan</h2>
                <p>{datetime.now().strftime('%B %d, %Y %I:%M %p')}</p>
            </div>
            <div style="margin:15px 0;padding:10px;background:#d4edda;border-radius:5px;">
                <strong>✅ No compliance gaps found</strong> — {total} AMP events scanned ({scan_start} to {scan_end})
            </div>
            </body></html>"""

        subject = f"Meeting Planner Compliance: {len(flagged)} gap{'s' if len(flagged) != 1 else ''} — {datetime.now().strftime('%m/%d/%Y')}"

        # Send to all admins
        admin_emails = admin_config.get("authorized_admins", [])
        for admin_email in admin_emails:
            success = send_outlook_email(admin_email, subject, body_html)
            db.log_notification(
                notification_type="Daily Compliance Scan",
                recipient=admin_email,
                subject=subject,
                details=f"{len(flagged)} gaps out of {total} scanned",
                sent_by="system@automated",
            )
        print(f"[Compliance Email] Sent to {len(admin_emails)} admins: {len(flagged)} gaps found")
    except Exception as e:
        print(f"[Compliance Email] Error: {e}")
        traceback.print_exc()


def start_scheduler():
    global scheduler
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        interval = int(os.getenv("AMP_SYNC_INTERVAL_MINUTES", "30"))
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            lambda: run_amp_sync(db),
            "interval",
            minutes=interval,
            id="amp_sync",
            replace_existing=True,
        )
        # Daily compliance scan email at 6:00 AM
        scheduler.add_job(
            send_daily_compliance_email,
            CronTrigger(hour=6, minute=0),
            id="daily_compliance_email",
            replace_existing=True,
        )
        scheduler.start()
        print(f"[Scheduler] AMP sync every {interval}m, compliance email daily at 6:00 AM")
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
    fav_path = Path(__file__).parent.parent / "frontend" / "Spark_Blank.png"
    if fav_path.exists():
        return FileResponse(str(fav_path), media_type="image/png", headers={"Cache-Control": "public, max-age=86400"})
    from fastapi.responses import Response
    return Response(content=b"", media_type="image/png", status_code=204)


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

def get_request_user(request: Request) -> str:
    """Get the logged-in user from the mp_user cookie.
    Returns the username or empty string if not logged in."""
    return (request.cookies.get("mp_user") or "").strip().lower()


@app.get("/api/user")
async def get_current_user(request: Request):
    username = get_request_user(request)
    if not username:
        return {"username": "", "email": "", "is_admin": False, "logged_in": False}
    email = get_user_email(username)
    return {
        "username": username,
        "email": email,
        "is_admin": is_admin(username),
        "logged_in": True,
    }


@app.post("/api/login")
async def login(body: dict):
    """Log in as a user. Sets a cookie with the username."""
    username = (body.get("username") or "").strip().lower()
    if not username or len(username) < 2 or len(username) > 30:
        raise HTTPException(status_code=400, detail="Please enter a valid Windows username (e.g., jsmith)")
    # Sanitize — only allow alphanumeric and common username chars
    import re as _re
    if not _re.match(r'^[a-z0-9._-]+$', username):
        raise HTTPException(status_code=400, detail="Username can only contain letters, numbers, dots, dashes, and underscores")
    email = get_user_email(username)
    response = JSONResponse(content={
        "username": username,
        "email": email,
        "is_admin": is_admin(username),
        "logged_in": True,
    })
    response.set_cookie(
        key="mp_user",
        value=username,
        httponly=False,  # Needs to be readable by JS for display
        max_age=60 * 60 * 24 * 90,  # 90 days
        samesite="lax",
        path="/",
    )
    return response


@app.post("/api/logout")
async def logout():
    """Clear the user cookie."""
    response = JSONResponse(content={"logged_out": True})
    response.delete_cookie("mp_user", path="/")
    return response


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
    request: Request,
    status: Optional[str] = None,
    source: Optional[str] = None,
    meeting_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """Admin-only: get all meeting requests."""
    username = get_request_user(request)
    if not username or not is_admin(username):
        raise HTTPException(status_code=403, detail="Admin access required")
    rows = db.get_all_requests(status=status, source=source,
                                meeting_type=meeting_type,
                                start_date=start_date, end_date=end_date)
    return {"requests": rows}


@app.get("/api/requests/mine")
async def get_my_requests(request: Request):
    """Current user's requests."""
    username = get_request_user(request)
    if not username:
        raise HTTPException(status_code=401, detail="Not logged in")
    email = get_user_email(username)
    rows = db.get_user_requests(email)
    return {"requests": rows}


@app.post("/api/requests")
async def submit_request(
    request: Request,
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
    username = get_request_user(request)
    if not username:
        raise HTTPException(status_code=401, detail="Not logged in")
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
async def update_request(request_id: str, body: dict, request: Request):
    """Admin: update a request (status, comment, start_time, meeting_link)."""
    username = get_request_user(request)
    if not username or not is_admin(username):
        raise HTTPException(status_code=403, detail="Admin access required")
    email = get_user_email(username)
    try:
        result = db.update_request(request_id, body, email)

        # Send email notification to submitter on comment or status change
        comment = body.get("comment", "").strip()
        new_status = body.get("status", "")
        if comment or new_status:
            try:
                request_info = db.get_request_by_id(request_id)
                submitter_email = request_info.get("Email", "")
                title = request_info.get("Title", "Unknown")
                if submitter_email:
                    parts = []
                    if new_status:
                        parts.append(f"<p>Status changed to: <strong>{new_status}</strong></p>")
                    if comment:
                        parts.append(f"<p>Admin comment: <em>{comment}</em></p>")
                    html_body = f"""<html><body>
                        <div style='font-family:Arial,sans-serif;'>
                        <h3 style='color:#0071ce'>Store Meeting Planner — Update</h3>
                        <p>Your request <strong>"{title}"</strong> has been updated:</p>
                        {''.join(parts)}
                        <p style='color:#666;font-size:0.9em'>— {email}</p>
                        <hr style='border:none;border-top:1px solid #ddd'>
                        <p style='font-size:0.8em;color:#999'>
                            <a href='http://weus42608431466:8090/StoreMeetingPlanner'>View in Store Meeting Planner</a>
                        </p>
                        </div></body></html>"""
                    subject = f"Meeting Planner: {title} — {'Comment' if comment else 'Status Update'}"
                    send_outlook_email(submitter_email, subject, html_body)
                    db.log_notification(
                        notification_type="Admin Comment" if comment else "Status Update",
                        recipient=submitter_email,
                        subject=subject,
                        details=comment or f"Status: {new_status}",
                        request_id=request_id,
                        sent_by=email,
                    )
            except Exception as notify_err:
                print(f"[Notify] Email/log error (non-blocking): {notify_err}")

        return result
    except Exception as e:
        print(f"[ERROR] update_request failed: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/requests/{request_id}/complete")
async def complete_request(request_id: str, body: dict, request: Request):
    """User completes missing fields on a Pending request."""
    username = get_request_user(request)
    if not username:
        raise HTTPException(status_code=401, detail="Not logged in")
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
async def trigger_amp_sync(request: Request):
    """Admin-only: manually trigger AMP sync."""
    username = get_request_user(request)
    if not username or not is_admin(username):
        raise HTTPException(status_code=403, detail="Admin access required")
    stats = run_amp_sync(db)
    return {"message": "AMP sync complete", "stats": stats}


# =============================================
# API: Meeting Tracker Report
# =============================================

@app.get("/api/reports/meeting-tracker")
async def meeting_tracker_report(
    request: Request,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """Admin: get Calls to Stores report data."""
    username = get_request_user(request)
    if not username or not is_admin(username):
        raise HTTPException(status_code=403, detail="Admin access required")
    rows = db.get_meeting_tracker_report(start_date, end_date)
    return {"report": rows, "generated_at": datetime.utcnow().isoformat()}


# =============================================
# API: Compliance Scan
# =============================================

@app.get("/api/reports/compliance-scan")
async def compliance_scan(
    request: Request,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """Admin: scan AMP events for meetings missing from Meeting Planner.
    Default: current WM week through future events."""
    username = get_request_user(request)
    if not username or not is_admin(username):
        raise HTTPException(status_code=403, detail="Admin access required")
    results = db.scan_compliance_gaps(scan_start=start_date, scan_end=end_date)
    return results


# =============================================
# STATIC FILES & FRONTEND
# =============================================

frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/StoreMeetingPlanner/static", StaticFiles(directory=str(frontend_path)), name="static")

    @app.get("/StoreMeetingPlanner")
    @app.get("/StoreMeetingPlanner/")
    async def serve_frontend():
        return FileResponse(str(frontend_path / "index.html"))

    @app.get("/")
    async def root_redirect():
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/StoreMeetingPlanner")


# =============================================
# RUN
# =============================================

if __name__ == "__main__":
    print(f"[Server] Starting Store Meeting Planner on {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
