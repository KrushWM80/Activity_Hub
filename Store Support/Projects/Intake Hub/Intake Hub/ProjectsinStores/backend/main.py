from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime, timedelta
import uvicorn
import os
import smtplib
import uuid
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from models import (
    Project, ProjectStatus, ProjectSource, FilterCriteria, 
    ProjectSummary, StoreCount
)
from database import DatabaseService
from ai_agent import AIAgent
from sqlite_cache import get_cache, SQLiteCache

# Simplified email reporting (no external packages required)
from email_service_simple import SimpleEmailReportService
from scheduler_manager import WindowsSchedulerManager

# Environment detection for Dev vs Production
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev").lower()
IS_DEV = ENVIRONMENT == "dev"

app = FastAPI(title="Projects in Stores Dashboard API")

# ===== SESSION MANAGEMENT FOR REMOTE USERS =====
# Simple in-memory session store: session_id -> {email, expires, is_admin}
# Declare EARLY so middleware can use it
_SESSIONS: Dict[str, dict] = {}
SESSION_TIMEOUT_MINUTES = 480  # 8 hours

# ==============================================
# IMPORTANT: FRONTEND SINGLE SOURCE OF TRUTH
# ==============================================
# ✅ MAIN DASHBOARD: frontend/index.html
#    - This is the ONLY dashboard being served at /
#    - All updates, features, and fixes go here
#    - simple.html is DEPRECATED and not used
# 
# When updating the frontend:
# 1. Edit frontend/index.html ONLY
# 2. All routes serve index.html (/, /admin.html, /reports.html, etc.)
# 3. No other versions of the dashboard exist
# 4. Clear your browser cache (Ctrl+Shift+R) after updates
# ==============================================

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================
# AUTOMATIC USER TRACKING MIDDLEWARE
# =============================================
# This middleware automatically tracks ANY authenticated user
# on ANY request, so everyone is tracked regardless of frontend code

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class AutomaticUserTrackingMiddleware(BaseHTTPMiddleware):
    """Middleware that automatically tracks authenticated users on every request"""
    
    async def dispatch(self, request: Request, call_next):
        # Try to get authenticated user
        current_user = None
        page = request.url.path
        
        try:
            # Method 1: Check session cookie first
            session_id = request.cookies.get('session_id')
            if session_id:
                from datetime import datetime, timedelta
                if session_id in _SESSIONS:
                    session = _SESSIONS[session_id]
                    if datetime.utcnow() < session['expires']:
                        current_user = session['email']
            
            # Method 2: Check Kerberos/Windows AD headers
            if not current_user:
                # Check for Kerberos headers
                kerberos_user = (
                    request.headers.get('X-Remote-User') or
                    request.headers.get('Remote-User') or
                    request.headers.get('HTTP_REMOTE_USER') or
                    request.headers.get('X-Authenticated-User')
                )
                
                if kerberos_user:
                    if '\\' in kerberos_user:
                        kerberos_user = kerberos_user.split('\\')[-1]
                    if '@' not in kerberos_user:
                        # Map to email format
                        username_map = {'krush': 'kendall.rush@walmart.com'}
                        kerberos_user_lower = kerberos_user.lower()
                        if kerberos_user_lower in username_map:
                            current_user = username_map[kerberos_user_lower]
                        else:
                            current_user = f"{kerberos_user_lower}@homeoffice.wal-mart.com"
                    else:
                        current_user = kerberos_user.lower()
            
            # Method 3: Fall back to Windows username
            if not current_user:
                windows_user = os.getenv('USERNAME', '').lower()
                if windows_user:
                    username_map = {'krush': 'kendall.rush@walmart.com'}
                    if windows_user in username_map:
                        current_user = username_map[windows_user]
                    else:
                        if '@' not in windows_user:
                            current_user = f"{windows_user}@homeoffice.wal-mart.com"
                        else:
                            current_user = windows_user
            
            # Track the user if we found one
            if current_user:
                # Determine page name from path
                if page in ['/', '/index.html']:
                    page = 'Main Dashboard'
                elif page == '/admin.html':
                    page = 'Admin Dashboard'
                elif '/api/' in page:
                    # API endpoint - extract meaningful name
                    parts = page.split('/')
                    page = f"API: {parts[-1]}" if len(parts) > 2 else page
                
                # Call tracking function asynchronously to not block request
                try:
                    from functools import partial
                    track_user_activity(current_user, page)
                except Exception as e:
                    # Silently fail - don't break the request if tracking fails
                    print(f"[TRACKING] Error tracking {current_user}: {e}")
        
        except Exception as e:
            # Silently continue if anything goes wrong
            print(f"[MIDDLEWARE] Error in tracking middleware: {e}")
        
        # Always call the next middleware/endpoint
        response = await call_next(request)
        return response

# Add the middleware to the app
app.add_middleware(AutomaticUserTrackingMiddleware)

# Initialize services
db_service = DatabaseService()
ai_agent = AIAgent()
email_service = SimpleEmailReportService(db_service)
scheduler_manager = WindowsSchedulerManager()
sqlite_cache = get_cache()

# Create report configs directory if it doesn't exist
import os
from pathlib import Path
configs_dir = Path(__file__).parent / "report_configs"
configs_dir.mkdir(exist_ok=True)

# =============================================
# AUTHENTICATION & ADMIN ACCESS CONTROL
# =============================================

import json

def load_admin_access_list():
    """Load authorized admin users from admin-access.json"""
    try:
        admin_access_path = os.path.join(os.path.dirname(__file__), "admin-access.json")
        with open(admin_access_path, 'r') as f:
            data = json.load(f)
            return {
                'admins': [email.lower() for email in data.get('authorized_admins', [])],
                'fallback_password': data.get('fallback_password', 'Admin2026')
            }
    except Exception as e:
        print(f"[AUTH] Error loading admin access list: {e}")
        return {'admins': [], 'fallback_password': 'Admin2026'}

admin_config = load_admin_access_list()

def create_session(user_email: str, is_admin: bool = False) -> str:
    """Create a new session and return session ID"""
    session_id = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(minutes=SESSION_TIMEOUT_MINUTES)
    _SESSIONS[session_id] = {
        'email': user_email,
        'is_admin': is_admin,
        'expires': expires,
        'created': datetime.utcnow()
    }
    return session_id

def get_session_user(session_id: str) -> Optional[str]:
    """Get user email from session, returns None if expired or invalid"""
    if session_id not in _SESSIONS:
        return None
    session = _SESSIONS[session_id]
    if datetime.utcnow() > session['expires']:
        # Session expired, clean it up
        del _SESSIONS[session_id]
        return None
    # Update last accessed time (extend expiry on each access)
    session['expires'] = datetime.utcnow() + timedelta(minutes=SESSION_TIMEOUT_MINUTES)
    return session['email']

def clear_session(session_id: str):
    """Clear/logout a session"""
    _SESSIONS.pop(session_id, None)

def cleanup_expired_sessions():
    """Remove expired sessions"""
    now = datetime.utcnow()
    expired = [sid for sid, sess in _SESSIONS.items() if now > sess['expires']]
    for sid in expired:
        del _SESSIONS[sid]

def get_current_authenticated_user(request: Request = None) -> Optional[str]:
    """Get current authenticated user from: session → Kerberos headers → Windows AD"""
    # 1. Try session first (for remote users with active session)
    if request:
        session_id = request.cookies.get('session_id')
        if session_id:
            user = get_session_user(session_id)
            if user:
                return user
        
        # 2. Try Kerberos/NTLM headers (for domain-joined machines)
        # Check various headers that IIS/reverse proxy might set
        kerberos_user = None
        
        # Check Authorization header for Negotiate/NTLM token
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Negotiate ') or auth_header.startswith('NTLM '):
            # User is authenticated via Kerberos/NTLM, extract username from other headers
            kerberos_user = extract_kerberos_username(request)
        
        # Also check common header aliases
        if not kerberos_user:
            kerberos_user = (
                request.headers.get('X-Remote-User') or
                request.headers.get('Remote-User') or
                request.headers.get('HTTP_REMOTE_USER') or
                request.headers.get('X-Authenticated-User')
            )
        
        if kerberos_user:
            return kerberos_user.lower()
    
    # 3. Fall back to Windows AD (for local users on same machine)
    return get_windows_username()

def get_windows_username():
    """Get current Windows username from environment and map to correct email"""
    try:
        username = os.getenv('USERNAME', '').lower()
        if username:
            # Map Windows usernames to their canonical Walmart email addresses
            # This ensures consistent user identity across the system
            username_map = {
                'krush': 'kendall.rush@walmart.com',
                # Add more mappings as needed: 'username': 'firstname.lastname@walmart.com'
            }
            
            # Check if there's a mapping for this user
            if username in username_map:
                return username_map[username]
            
            # Default: Convert to email format if it's just a username
            if '@' not in username:
                username = f"{username}@homeoffice.wal-mart.com"
            return username
    except:
        pass
    return None

def extract_kerberos_username(request: Request) -> Optional[str]:
    """Extract username from Kerberos/NTLM authentication headers
    
    When a user accesses from a domain-joined machine, the web server receives
    Kerberos authentication tokens. This function extracts the username.
    """
    try:
        # Try to extract from various possible header locations
        # Method 1: Direct remote user header (set by IIS/reverse proxy after Kerberos validation)
        user = (
            request.headers.get('X-Remote-User') or
            request.headers.get('Remote-User') or
            request.headers.get('HTTP_REMOTE_USER') or
            request.headers.get('X-Authenticated-User')
        )
        
        if user:
            # Clean up the username (remove domain prefix if present)
            if '\\' in user:
                # Format: DOMAIN\username → extract username
                user = user.split('\\')[-1]
            if '@' in user:
                # Already in email format or contains domain
                return user.lower()
            else:
                # Just a Windows username, map to Walmart email
                user_lower = user.lower()
                username_map = {
                    'krush': 'kendall.rush@walmart.com',
                    # Add more mappings as needed
                }
                if user_lower in username_map:
                    return username_map[user_lower]
                else:
                    # Default: convert to @homeoffice.wal-mart.com format
                    return f"{user_lower}@homeoffice.wal-mart.com"
    except:
        pass
    
    return None

def get_admin_email_variants(windows_user):
    """Get all possible email variants for a user to check admin access
    Handles both mapped and unmapped users"""
    variants = [windows_user]  # Original mapped email (in canonical format)
    
    # Check if this user is in the username map (reverse lookup)
    username_map = {
        'krush': 'kendall.rush@walmart.com',
        # Add more mappings as needed
    }
    
    # If this user was mapped from a Windows username, also include the homeoffice variant
    for windows_username, mapped_email in username_map.items():
        if mapped_email == windows_user:
            # Add the homeoffice email variant for backward compatibility
            variants.append(f"{windows_username}@homeoffice.wal-mart.com")
            break
    
    return variants

class AuthResponse(BaseModel):
    """Response model for authentication endpoints"""
    email: Optional[str] = None
    username: Optional[str] = None
    is_admin: bool = False
    auth_method: str = "none"  # 'windows_ad', 'fallback_password', 'none'
    message: str = ""

class LoginRequest(BaseModel):
    """Request model for manual login - username only (password ignored)"""
    username: str
    password: str = ""  # Optional, not used for authentication

@app.get("/api/auth/user")
async def get_current_user(request: Request):
    """Check current user from session (if logged in) or Windows AD and return admin status"""
    # Check session first, fall back to Windows
    current_user = get_current_authenticated_user(request)
    
    if current_user:
        # Check admin access using all possible email variants
        email_variants = get_admin_email_variants(current_user)
        is_admin = any(variant in admin_config['admins'] for variant in email_variants)
        
        # Determine auth method
        session_id = request.cookies.get('session_id')
        auth_method = 'session' if session_id else 'windows_ad'
        
        return AuthResponse(
            email=current_user,
            username=current_user.split('@')[0],
            is_admin=is_admin,
            auth_method=auth_method,
            message=f'Authenticated via {auth_method}'
        )
    
    # Not on network or Windows auth failed
    return AuthResponse(
        is_admin=False,
        auth_method='none',
        message='Not authenticated - Windows AD failed, fallback login available'
    )

@app.post("/api/auth/login")
async def fallback_login(request: LoginRequest):
    """Fallback login for remote users by username only (NO PASSWORD REQUIRED)
    
    Allows any Walmart domain user to log in by providing just their username.
    This endpoint is only used when Kerberos/NTLM headers are not detected.
    No password validation - any domain username can authenticate.
    Returns session info for user tracking and sets session cookie.
    """
    username = request.username.lower().strip()
    
    if not username:
        raise HTTPException(status_code=400, detail="Username required")
    
    # Map username to canonical email format
    username_map = {
        'krush': 'kendall.rush@walmart.com',
        # Add more mappings as needed
    }
    
    if username in username_map:
        user_email = username_map[username]
    else:
        # Default: convert to @homeoffice.wal-mart.com format
        user_email = f"{username}@homeoffice.wal-mart.com"
    
    # Check if user is admin
    email_variants = [user_email]
    # Add walmart.com variant if not already
    if '@homeoffice.wal-mart.com' in user_email:
        email_variants.append(user_email.replace('@homeoffice.wal-mart.com', '@walmart.com'))
    
    is_admin = any(variant in admin_config.get('admins', []) for variant in email_variants)
    
    # Create session for this user
    session_id = create_session(user_email, is_admin)
    
    # Track user activity (login)
    track_user_activity(user_email, "Logged in (Fallback - No Password)")
    log_activity(
        action='User Login',
        user=user_email,
        details='User logged in via username-only authentication (Kerberos not detected)',
        category='auth'
    )
    
    # Create response with session cookie
    response_data = AuthResponse(
        email=user_email,
        username=username,
        is_admin=is_admin,
        auth_method='session',
        message=f'Logged in as {user_email}'
    )
    
    response = JSONResponse(content=response_data.dict())
    # Set HttpOnly cookie with session ID (httpOnly prevents JavaScript access for security)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,  # Set to True if using HTTPS in production
        samesite="lax",
        max_age=SESSION_TIMEOUT_MINUTES * 60,  # Seconds
        path="/"
    )
    
    return response

@app.post("/api/auth/logout")
async def logout(request: Request):
    """Logout the current user and clear session"""
    session_id = request.cookies.get('session_id')
    if session_id:
        # Get user email before clearing
        user_email = get_session_user(session_id)
        # Clear the session
        clear_session(session_id)
        
        if user_email:
            log_activity(
                action='User Logout',
                user=user_email,
                details='User logged out',
                category='auth'
            )
    
    # Create response and clear the cookie
    response = JSONResponse(content={'message': 'Logged out successfully'})
    response.delete_cookie('session_id', path='/')
    return response

# Startup and shutdown events for SQLite cache sync
@app.on_event("startup")
async def startup_event():
    """Initialize SQLite cache on startup"""
    print("[Startup] Initializing SQLite cache...")
    
    # Don't block startup on sync - let it happen in background
    # The cache will be empty initially but will sync asynchronously
    print("[Startup] Starting background cache sync...")
    
    # Start background sync (every 15 minutes) 
    # This includes initial sync on first run
    if db_service.client:
        import threading
        sync_thread = threading.Thread(
            target=_background_cache_init,
            daemon=True
        )
        sync_thread.start()
        print("[Startup] Background sync thread started, server ready for requests")


def _background_cache_init():
    """Background initialization of cache - doesn't block startup"""
    try:
        # Check if cache is valid
        if sqlite_cache.is_cache_valid(max_age_minutes=60):
            print(f"[Background] Cache is valid with {sqlite_cache.get_record_count()} records")
        else:
            print("[Background] Cache is empty or stale, syncing from BigQuery...")
            if db_service.client:
                sqlite_cache.sync_from_bigquery(
                    db_service.client,
                    db_service.project_id,
                    db_service.dataset,
                    db_service.table
                )
                print(f"[Background] Cache sync complete with {sqlite_cache.get_record_count()} records")
        
        # Start periodic background sync (every 15 minutes)
        if db_service.client:
            sqlite_cache.start_background_sync(
                db_service.client,
                db_service.project_id,
                db_service.dataset,
                db_service.table
            )
    except Exception as e:
        print(f"[Background] Error during cache initialization: {e}")
        # Don't fail startup if cache init fails

@app.on_event("shutdown")
async def shutdown_event():
    """Stop background sync on shutdown"""
    print("[Shutdown] Stopping background sync...")
    sqlite_cache.stop_background_sync()


# Middleware for automatic user tracking on API calls
@app.middleware("http")
async def track_user_middleware(request, call_next):
    """
    Automatically track authenticated users on every API request.
    This ensures all users are visible in active users list regardless of page.
    Only tracks API endpoints, not static files.
    Also checks for session cookies and Windows auth.
    """
    try:
        # Only track API requests
        if request.url.path.startswith("/api/"):
            # Skip auth endpoints and other non-tracking endpoints
            if not any(skip in request.url.path for skip in [
                "/api/auth/user",
                "/api/auth/login",
                "/api/auth/logout",
                "/api/health",
                "/api/admin/track-user"  # Skip explicit track-user to avoid double tracking
            ]):
                # Get authenticated user (checks session first, then Windows)
                current_user = get_current_authenticated_user(request)
                
                if current_user:
                    # Derive page name from endpoint
                    path = request.url.path
                    if "/reports/" in path:
                        page = "Email Reports"
                    elif "/admin/" in path:
                        page = "Admin Dashboard"
                    elif "/projects" in path:
                        page = "Projects Dashboard"
                    elif "/summary" in path:
                        page = "Summary"
                    else:
                        page = path.replace("/api/", "").split("/")[0].title() or "API"
                    
                    # Track user activity (updates last_seen and page)
                    track_user_activity(current_user, page)
    except Exception as e:
        # Log but don't fail the request if tracking fails
        print(f"[Tracking] Error in user tracking middleware: {e}")
    
    # Continue with the request
    response = await call_next(request)
    return response

# Pydantic models for API
class ProjectResponse(BaseModel):
    project_id: str
    project_source: str
    title: str
    division: str
    region: str
    market: str
    store: str
    phase: str
    tribe: str
    wm_week: str
    fy: str
    status: str
    store_count: int
    owner: Optional[str] = None
    partner: Optional[str] = None
    store_area: Optional[str] = None
    business_area: Optional[str] = None
    health: Optional[str] = None
    business_type: Optional[str] = None
    associate_impact: Optional[str] = None
    customer_impact: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    store_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

class ProjectSummaryResponse(BaseModel):
    total_active_projects: int
    total_stores: int
    intake_hub_projects: int
    intake_hub_stores: int
    realty_projects: int
    realty_stores: int
    by_division: dict
    by_phase: dict
    last_updated: str

class FilterOptionsResponse(BaseModel):
    tribes: List[str] = []
    stores: List[str] = []
    project_sources: List[str] = []
    markets: List[str] = []
    regions: List[str] = []
    divisions: List[str] = []
    phases: List[str] = []
    wm_weeks: List[str] = []
    fiscal_years: List[str] = []
    owners: List[str] = []
    store_areas: List[str] = []
    business_areas: List[str] = []
    health_statuses: List[str] = []
    business_types: List[str] = []
    associate_impacts: List[str] = []
    customer_impacts: List[str] = []


class AIQueryRequest(BaseModel):
    query: str
    context: Optional[dict] = None

class AIQueryResponse(BaseModel):
    answer: str
    data: Optional[dict] = None
    query: str

@app.get("/")
async def root(request: Request):
    """Serve main dashboard - with automatic authentication
    
    If user is authenticated (via session or Kerberos), serve dashboard.
    If user is not authenticated, redirect to login page for username entry.
    """
    # Check if user is authenticated
    current_user = get_current_authenticated_user(request)
    if current_user:
        # Auto-login: User detected via Kerberos or session
        # Create session if they came via Kerberos headers but don't have a session cookie yet
        session_id = request.cookies.get('session_id')
        if not session_id:
            # Extract admin status
            email_variants = [current_user]
            if '@homeoffice.wal-mart.com' in current_user:
                email_variants.append(current_user.replace('@homeoffice.wal-mart.com', '@walmart.com'))
            is_admin = any(variant in admin_config.get('admins', []) for variant in email_variants)
            
            # Create a new session for this auto-detected user
            session_id = create_session(current_user, is_admin)
            
            # Track this auto-login
            track_user_activity(current_user, "Auto-Login (Kerberos/Windows)")
            log_activity(
                action='Auto-Login',
                user=current_user,
                details='User automatically detected and logged in via Kerberos/Windows auth',
                category='auth'
            )
        else:
            # Just track normal access
            track_user_activity(current_user, "Main Dashboard")
        
        # Serve dashboard
        html_file = "index.html" if IS_DEV else "index.html.production"
        html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", html_file)
        if os.path.exists(html_path):
            response = FileResponse(html_path, media_type="text/html")
            # Ensure session cookie is set (if it was created above)
            if session_id:
                response.set_cookie(
                    key="session_id",
                    value=session_id,
                    httponly=True,
                    secure=False,
                    samesite="lax",
                    max_age=SESSION_TIMEOUT_MINUTES * 60,
                    path="/"
                )
            return response
        else:
            # Fallback to API info if HTML not found
            return {
                "message": "Projects in Stores Dashboard API",
                "version": "1.0.0",
                "endpoints": [
                    "/api/projects",
                    "/api/summary",
                    "/api/filters",
                    "/api/store-counts",
                    "/api/ai/query"
                ]
            }
    else:
        # Not authenticated - redirect to login page
        return RedirectResponse(url="/login.html", status_code=302)

@app.get("/index.html")
async def index_html(request: Request):
    """Serve dashboard via index.html - PRIMARY ENTRY POINT
    
    Users access this URL directly: http://weus.../8001/index.html
    Supports same auto-authentication as root endpoint.
    """
    # Check if user is authenticated
    current_user = get_current_authenticated_user(request)
    if current_user:
        # Auto-login: User detected via Kerberos or session
        # Create session if they came via Kerberos headers but don't have a session cookie yet
        session_id = request.cookies.get('session_id')
        if not session_id:
            # Extract admin status
            email_variants = [current_user]
            if '@homeoffice.wal-mart.com' in current_user:
                email_variants.append(current_user.replace('@homeoffice.wal-mart.com', '@walmart.com'))
            is_admin = any(variant in admin_config.get('admins', []) for variant in email_variants)
            
            # Create a new session for this auto-detected user
            session_id = create_session(current_user, is_admin)
            
            # Track this auto-login
            track_user_activity(current_user, "Auto-Login (Kerberos/Windows)")
            log_activity(
                action='Auto-Login',
                user=current_user,
                details='User automatically detected and logged in via Kerberos/Windows auth',
                category='auth'
            )
        else:
            # Just track normal access
            track_user_activity(current_user, "Dashboard Access")
        
        # Serve dashboard
        html_file = "index.html" if IS_DEV else "index.html.production"
        html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", html_file)
        if os.path.exists(html_path):
            response = FileResponse(html_path, media_type="text/html")
            # Ensure session cookie is set (if it was created above)
            if session_id:
                response.set_cookie(
                    key="session_id",
                    value=session_id,
                    httponly=True,
                    secure=False,
                    samesite="lax",
                    max_age=SESSION_TIMEOUT_MINUTES * 60,
                    path="/"
                )
            return response
        else:
            # Fallback to API info if HTML not found
            return {
                "message": "Projects in Stores Dashboard API",
                "version": "1.0.0",
                "endpoints": [
                    "/api/projects",
                    "/api/summary",
                    "/api/filters",
                    "/api/store-counts",
                    "/api/ai/query"
                ]
            }
    else:
        # Not authenticated - redirect to login page
        return RedirectResponse(url="/login.html", status_code=302)

@app.get("/login.html")
async def login_page(request: Request):
    """Serve login page - username-only form for non-domain users
    
    If user is already authenticated (Kerberos detected), redirect to dashboard.
    Otherwise, serve username-only login form.
    """
    # Check if user is already authenticated
    current_user = get_current_authenticated_user(request)
    if current_user:
        # User already authenticated, redirect to dashboard
        return RedirectResponse(url="/", status_code=302)
    
    # Not authenticated yet - serve login form
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "login.html")
    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="Login page not found")

@app.get("/reports.html")
async def reports_page(request: Request):
    """Serve reports management interface - track user"""
    # Track user access to reports page
    current_user = get_current_authenticated_user(request)
    if current_user:
        track_user_activity(current_user, "Email Reports")
    
    # Serve the reports management interface
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "reports.html")
    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="Reports page not found")

@app.get("/admin.html")
async def admin_page(request: Request):
    """Serve the admin dashboard directly via /admin.html - track user"""
    # Track user access to admin dashboard
    current_user = get_current_authenticated_user(request)
    if current_user:
        track_user_activity(current_user, "Admin Dashboard")
    
    admin_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "admin.html")
    if os.path.exists(admin_path):
        return FileResponse(admin_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="Admin dashboard not found")

@app.get("/spark-logo.png")
async def spark_logo():
    """Serve the Spark logo image"""
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "spark-logo.png")
    if os.path.exists(logo_path):
        return FileResponse(logo_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Logo not found")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected" if db_service.is_connected() else "disconnected"
    }

@app.get("/api/cache/status")
async def cache_status():
    """Get SQLite cache status"""
    last_sync = sqlite_cache.get_last_sync_time()
    return {
        "cache_valid": sqlite_cache.is_cache_valid(),
        "record_count": sqlite_cache.get_record_count(),
        "last_sync": last_sync.isoformat() if last_sync else None,
        "sync_interval_minutes": sqlite_cache.sync_interval // 60,
        "cache_file": sqlite_cache.db_path
    }

@app.post("/api/cache/sync")
async def force_cache_sync():
    """Force an immediate sync from BigQuery to SQLite cache"""
    if not db_service.client:
        raise HTTPException(status_code=503, detail="BigQuery client not available")
    
    success = sqlite_cache.force_sync(
        db_service.client,
        db_service.project_id,
        db_service.dataset,
        db_service.table
    )
    
    if success:
        return {
            "status": "success",
            "record_count": sqlite_cache.get_record_count(),
            "last_sync": sqlite_cache.get_last_sync_time().isoformat()
        }
    else:
        raise HTTPException(status_code=500, detail="Sync failed")

@app.get("/api/project-titles")
async def get_project_titles():
    """Get all unique project titles with store counts for Quick Preview"""
    try:
        titles = sqlite_cache.get_unique_project_titles()
        return titles
    except Exception as e:
        print(f"[API] Error getting project titles from cache: {e}")
        # Fallback to BigQuery if cache fails
        try:
            query = """
                SELECT 
                    CASE
                        WHEN Project_Title IS NOT NULL AND Project_Title != '' THEN Project_Title
                        WHEN Title IS NOT NULL AND Title != '' THEN Title
                        WHEN Project_Type IS NOT NULL AND Project_Type != 'None' AND Project_Type != '' 
                             AND Initiative_Type IS NOT NULL AND Initiative_Type != '' 
                            THEN CONCAT(Project_Type, ' - ', Initiative_Type)
                        WHEN Initiative_Type IS NOT NULL AND Initiative_Type != '' THEN Initiative_Type
                        ELSE NULL
                    END as title,
                    MIN(COALESCE(CAST(Intake_Card AS STRING), CONCAT('R-', CAST(Facility AS STRING)))) as project_id,
                    COUNT(DISTINCT Facility) as store_count,
                    MIN(Project_Source) as project_source
                FROM `{}.{}.{}`
                WHERE Status = 'Active'
                GROUP BY 1
                HAVING title IS NOT NULL AND title != ''
                ORDER BY title
            """.format(db_service.project_id, db_service.dataset, db_service.table)
            result = db_service.client.query(query).result()
            return [
                {
                    'title': row.title,
                    'project_id': row.project_id,
                    'store_count': row.store_count,
                    'project_source': row.project_source
                }
                for row in result
            ]
        except Exception as bq_error:
            print(f"[API] BigQuery fallback also failed: {bq_error}")
            raise HTTPException(status_code=500, detail="Failed to get project titles")

@app.get("/api/projects", response_model=List[ProjectResponse])
async def get_projects(
    tribe: Optional[str] = None,
    division: Optional[str] = None,
    region: Optional[str] = None,
    market: Optional[str] = None,
    phase: Optional[str] = None,
    project_source: Optional[str] = None,
    wm_week: Optional[str] = None,
    fy: Optional[str] = None,
    title: Optional[str] = None,
    store: Optional[str] = None,
    owner: Optional[str] = None,
    partner: Optional[str] = None,
    business_area: Optional[str] = None,
    store_area: Optional[str] = None,
    business_type: Optional[str] = None,
    health: Optional[str] = None,
    associate_impact: Optional[str] = None,
    customer_impact: Optional[str] = None,
    status: str = "Active",
    include_location: bool = False,
    limit: Optional[int] = 50000
):
    """Get filtered list of projects. Uses SQLite cache for fast response. Set include_location=true to fetch store lat/long data (slower). Use limit to cap results (default: 50000 to capture all unique projects across sources)."""
    try:
        # Try SQLite cache first (fast - milliseconds)
        if sqlite_cache.is_cache_valid() and not include_location:
            try:
                print("[API] Using SQLite cache for /api/projects")
                cache_filters = {
                    'division': division,
                    'region': region,
                    'market': market,
                    'store': store,
                    'phase': phase,
                    'fy': fy,
                    'wm_week': wm_week,
                    'project_source': project_source,
                    'owner': owner,
                    'business_area': business_area,
                    'store_area': store_area,
                    'business_type': business_type,
                    'health': health,
                    'associate_impact': associate_impact,
                    'customer_impact': customer_impact
                }
                
                # If partner filter applied, get intake_cards from partner cache
                partner_intake_cards = None
                if partner:
                    print(f"[API] Getting projects for partner(s): {partner}")
                    partner_list = [p.strip() for p in partner.split(',')] if isinstance(partner, str) else [partner]
                    partner_intake_cards = sqlite_cache.get_project_ids_by_partners(partner_list)
                    print(f"[API] Found {len(partner_intake_cards)} projects with partner(s)")
                    
                    if not partner_intake_cards:
                        # No projects found for this partner
                        return []
                
                # Remove None values
                cache_filters = {k: v for k, v in cache_filters.items() if v is not None}
                
                cached_projects = sqlite_cache.get_projects(
                    filters=cache_filters,
                    limit=limit,
                    title_search=title
                )
                
                # Filter by partner intake cards if partner filter was applied
                if partner_intake_cards:
                    partner_set = set(partner_intake_cards)
                    cached_projects = [
                        p for p in cached_projects 
                        if p.get('intake_card') in partner_set
                    ]
                
                return [
                    ProjectResponse(
                        project_id=p['project_id'],
                        project_source=p['project_source'] or 'Unknown',
                        title=p['title'] or '',
                        division=p['division'] or '',
                        region=p['region'] or '',
                        market=p['market'] or '',
                        store=p['store'] or '',
                        phase=p['phase'] or '',
                        tribe='',  # Not in cache
                        wm_week=p['wm_week'] or '',
                        fy=p['fy'] or '',
                        status=p['status'] or 'Active',
                        store_count=p['store_count'] or 1,
                        owner=p.get('owner'),
                        partner=partner if partner else (p.get('partner') or ''),  # Use filter or cached
                        store_area=p.get('store_area'),
                        business_area=p.get('business_area'),
                        health=p.get('health'),
                        business_type=p.get('business_type'),
                        associate_impact=p.get('associate_impact'),
                        customer_impact=p.get('customer_impact'),
                        description=None,
                        latitude=None,
                        longitude=None,
                        store_address=None,
                        city=None,
                        state=None,
                        zip_code=None
                    )
                    for p in cached_projects
                ]
            except Exception as cache_error:
                print(f"[API] SQLite cache error: {cache_error}, falling back to BigQuery")
        
        # Fall back to BigQuery (slower)
        print("[API] Using BigQuery for /api/projects (cache miss or include_location=true)")
        filters = FilterCriteria()
        filters.status = ProjectStatus(status)
        
        if tribe:
            filters.tribe = [tribe]
        if division:
            filters.division = [division]
        if region:
            filters.region = [region]
        if market:
            filters.market = [market]
        if phase:
            filters.phase = [phase]
        if project_source:
            filters.project_source = [project_source]
        if wm_week:
            filters.wm_week = [wm_week]
        if fy:
            filters.fy = [fy]
        if store:
            filters.store = [store]
        if partner:
            filters.partners = [partner]
        
        projects = await db_service.get_projects(filters, include_location=include_location, limit=limit, title_search=title)
        
        return [
            ProjectResponse(
                project_id=p.project_id,
                project_source=p.project_source.value,
                title=p.title,
                division=p.division,
                region=p.region,
                market=p.market,
                store=p.store,
                phase=p.phase,
                tribe=p.tribe,
                wm_week=p.wm_week,
                fy=p.fy,
                status=p.status.value,
                store_count=p.store_count,
                owner=p.owner,
                partner=p.partner,
                store_area=p.store_area,
                business_area=p.business_area,
                health=p.health,
                business_type=p.business_type,
                associate_impact=p.associate_impact,
                customer_impact=p.customer_impact,
                description=p.description,
                latitude=p.latitude,
                longitude=p.longitude,
                store_address=p.store_address,
                city=p.city,
                state=p.state,
                zip_code=p.zip_code
            )
            for p in projects
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/summary", response_model=ProjectSummaryResponse)
async def get_summary(
    tribe: Optional[str] = None,
    division: Optional[str] = None,
    region: Optional[str] = None,
    status: str = "Active"
):
    """Get dashboard summary statistics. Uses SQLite cache for fast response."""
    try:
        # Use cache if valid and no specific filters
        if sqlite_cache.is_cache_valid() and not tribe and not division and not region:
            print("[API] Using SQLite cache for /api/summary")
            cached_summary = sqlite_cache.get_summary()
            return ProjectSummaryResponse(
                total_active_projects=cached_summary['total_active_projects'],
                total_stores=cached_summary['total_stores'],
                intake_hub_projects=cached_summary['intake_hub_projects'],
                intake_hub_stores=cached_summary['intake_hub_stores'],
                realty_projects=cached_summary['realty_projects'],
                realty_stores=cached_summary['realty_stores'],
                by_division={},  # Not cached
                by_phase={},  # Not cached
                last_updated=cached_summary['last_updated'] or datetime.now().isoformat()
            )
        
        # Fall back to BigQuery
        print("[API] Using BigQuery for /api/summary")
        filters = FilterCriteria()
        filters.status = ProjectStatus(status)
        if tribe:
            filters.tribe = [tribe]
        if division:
            filters.division = [division]
        if region:
            filters.region = [region]
            
        summary = await db_service.get_summary(filters)
        
        return ProjectSummaryResponse(
            total_active_projects=summary.total_active_projects,
            total_stores=summary.total_stores,
            intake_hub_projects=summary.intake_hub_projects,
            intake_hub_stores=summary.intake_hub_stores,
            realty_projects=summary.realty_projects,
            realty_stores=summary.realty_stores,
            by_division=summary.by_division,
            by_phase=summary.by_phase,
            last_updated=summary.last_updated.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/filters-debug")
async def get_filter_options_debug():
    """Debug endpoint - returns hardcoded dict with all 16 fields"""
    return {
        "tribes": ["test"],
        "stores": ["test"],
        "project_sources": ["test"],
        "markets": ["test"],
        "regions": ["test"],
        "divisions": ["test"],
        "phases": ["test"],
        "wm_weeks": ["test"],
        "fiscal_years": ["test"],
        "owners": ["test"],
        "store_areas": ["test"],
        "business_areas": ["test"],
        "health_statuses": ["test"],
        "business_types": ["test"],
        "associate_impacts": ["test"],
        "customer_impacts": ["test"]
    }


@app.get("/api/filters")
def get_filter_options():
    """Get all available filter options - ALWAYS use cache if it has data"""
    import threading
    
    try:
        # SIMPLIFIED LOGIC: Check cache first, use it if it has any data
        record_count = sqlite_cache.get_record_count()
        
        # If cache has data, use it (don't rely on timestamp validity check)
        if record_count > 0:
            filters = sqlite_cache.get_filter_options()
        else:
            # Only fall back to database if cache is completely empty
            filters = db_service.get_filter_options()
        
        # Load partners asynchronously with timeout to avoid blocking
        partners_list = []
        def fetch_partners():
            nonlocal partners_list
            try:
                partner_client = db_service.client
                if partner_client:
                    # Simplified query without ORDER BY for performance
                    partner_query = """
                        SELECT DISTINCT Partner as partner_name
                        FROM `wmt-assetprotection-prod.Store_Support.IH_Branch_Data`
                        WHERE Partner IS NOT NULL
                        LIMIT 1000
                    """
                    query_job = partner_client.query(partner_query)
                    # Set timeout to 5 seconds
                    results = query_job.result(timeout=5)
                    partners_list = sorted(list(set([str(row.partner_name).strip() for row in results if row.partner_name])))
            except Exception as e:
                print(f"[API] Warning: Could not fetch partners - {e}", flush=True)
                import traceback
                traceback.print_exc()
                partners_list = []
        
        # Run partner fetch in a thread with timeout
        partner_thread = threading.Thread(target=fetch_partners, daemon=True)
        partner_thread.start()
        partner_thread.join(timeout=3)  # Only wait 3 seconds max
        
        filters['partners'] = partners_list
        return filters
    except Exception as e:
        print(f"[API] ERROR in /api/filters: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/debug/cache-state")
def debug_cache_state():
    """Debug endpoint to check cache state"""
    return {
        "record_count": sqlite_cache.get_record_count(),
        "cache_valid": sqlite_cache.is_cache_valid(),
        "last_sync": str(sqlite_cache.get_last_sync_time())
    }

@app.post("/api/debug/clear-filter-cache")
def clear_filter_cache():
    """Clear the in-memory filter cache in DatabaseService"""
    from database import DatabaseService
    DatabaseService._filters_cache = None
    DatabaseService._filters_cache_timestamp = None
    return {"status": "Filter cache cleared"}

@app.get("/api/store-counts")
async def get_store_counts(
    group_by: str = Query("division", pattern="^(division|region|market|phase)$")
):
    """Get store counts grouped by specified dimension"""
    try:
        counts = await db_service.get_store_counts(group_by)
        return {"counts": counts, "group_by": group_by}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/preview/projects")
async def get_project_preview(
    division: Optional[str] = None,
    region: Optional[str] = None,
    market: Optional[str] = None,
    store: Optional[str] = None,
    phase: Optional[str] = None,
    source: Optional[str] = None
):
    """Get preview of top 5 project titles based on current filters"""
    try:
        projects = db_service.get_all_projects()
        
        # Apply filters
        if source:
            projects = [p for p in projects if p.get('project_source') == source]
        if division:
            projects = [p for p in projects if p.get('division') == division]
        if region:
            projects = [p for p in projects if p.get('region') == region]
        if market:
            projects = [p for p in projects if str(p.get('market', '')) == market]
        if store:
            projects = [p for p in projects if p.get('store') == store]
        if phase:
            projects = [p for p in projects if p.get('phase') == phase]
        
        # Get unique titles and return top 5
        unique_titles = sorted(list(set([p.get('title', '') for p in projects if p.get('title')])))[:5]
        
        return {
            "preview_titles": unique_titles,
            "total_matching": len(set([p.get('title', '') for p in projects])),
            "total_projects_in_filter": len(projects)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/query", response_model=AIQueryResponse)
async def ai_query(request: AIQueryRequest):
    """Query the AI agent about project data"""
    try:
        response = await ai_agent.process_query(
            query=request.query,
            context=request.context
        )
        return AIQueryResponse(
            answer=response["answer"],
            data=response.get("data"),
            query=request.query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class FeedbackRequest(BaseModel):
    category: str
    rating: int
    comments: str
    timestamp: str
    user_context: Optional[dict] = None

def analyze_feedback_and_email_admin(feedback: FeedbackRequest):
    """
    STEP 2: Copilot AI performs discovery, creates pending fix, and sends analysis to Kendall.
    This happens AFTER the raw feedback is sent to ATCteamsupport.
    
    Flow:
    1. User submits feedback → ATCteamsupport@walmart.com receives raw feedback
    2. Copilot AI performs DISCOVERY to find root cause
    3. Creates pending fix with specific resolution
    4. Sends analysis email to kendall.rush@walmart.com
    5. Kendall can approve/deny via Admin Dashboard at /admin
    """
    try:
        # STEP 1: Perform discovery to find root cause and resolution
        print(f"\n{'='*80}")
        print(f"PERFORMING DISCOVERY ON FEEDBACK...")
        print(f"{'='*80}")
        
        discovery_result = perform_discovery(feedback)
        
        print(f"Title: {discovery_result['title']}")
        print(f"Root Cause: {discovery_result['root_cause'][:100]}...")
        print(f"Resolution: {discovery_result['resolution'][:100]}...")
        
        # STEP 2: Create pending fix in the queue
        pending_fix = create_pending_fix(feedback, discovery_result)
        fix_id = pending_fix["id"]
        
        print(f"\n[OK] Created pending fix: FIX-{fix_id}")
        
        # STEP 3: Build email with discovery results
        analysis_report = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<h2 style="color: #0071ce;">🔍 Copilot AI Feedback Analysis - FIX-{fix_id}</h2>

<div style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; border-radius: 4px; margin-bottom: 20px;">
    <strong>📬 Raw feedback sent to:</strong> ATCteamsupport@walmart.com<br>
    <strong>📊 Pending fix created:</strong> FIX-{fix_id}<br>
    <strong>🔧 Approve/Deny at:</strong> <a href="http://localhost:8001/admin">Admin Dashboard</a>
</div>

<div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
    <h3>📝 Feedback Summary</h3>
    <table style="width: 100%; border-collapse: collapse;">
        <tr><td style="padding: 8px;"><strong>Category:</strong></td><td>{feedback.category}</td></tr>
        <tr><td style="padding: 8px;"><strong>Rating:</strong></td><td>{'⭐' * feedback.rating} ({feedback.rating}/5)</td></tr>
        <tr><td style="padding: 8px;"><strong>Timestamp:</strong></td><td>{feedback.timestamp}</td></tr>
        <tr><td style="padding: 8px;"><strong>Priority:</strong></td><td>{'🔴 HIGH' if feedback.rating <= 2 else '🟡 MEDIUM' if feedback.rating <= 3 else '🟢 LOW'}</td></tr>
    </table>
</div>

<h3>💬 User Comments</h3>
<div style="background: #e7f3ff; padding: 15px; border-left: 4px solid #0071ce; border-radius: 4px; margin-bottom: 20px;">
    <p>{feedback.comments}</p>
</div>

<h3>🔍 Root Cause Analysis</h3>
<div style="background: #f8d7da; padding: 15px; border-left: 4px solid #dc3545; border-radius: 4px; margin-bottom: 20px;">
    <p><strong>{discovery_result['title']}</strong></p>
    <p>{discovery_result['root_cause']}</p>
</div>

<h3>💡 Proposed Resolution</h3>
<div style="background: #d1ecf1; padding: 15px; border-left: 4px solid #17a2b8; border-radius: 4px; margin-bottom: 20px;">
    <p>{discovery_result['resolution']}</p>
    {f'''<div style="margin-top: 10px; background: #1e1e1e; color: #d4d4d4; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px;">
        <strong style="color: #569cd6;">File:</strong> {discovery_result['code_changes']['file']}<br>
        <span style="color: #f14c4c;">- {discovery_result['code_changes']['old_code']}</span><br>
        <span style="color: #4ec9b0;">+ {discovery_result['code_changes']['new_code']}</span>
    </div>''' if discovery_result.get('code_changes') else ''}
</div>

<hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">

<h3>🚀 Action Required</h3>
<div style="background: #d4edda; padding: 15px; border-left: 4px solid #28a745; border-radius: 4px;">
    <p><strong>To approve or deny this fix:</strong></p>
    <p style="margin-top: 10px;">
        👉 Go to <a href="http://localhost:8001/admin" style="color: #0071ce; font-weight: bold;">Admin Dashboard</a><br>
        👉 Login with your admin credentials<br>
        👉 Find FIX-{fix_id} and click Approve, Deny, or Hold
    </p>
    <p style="margin-top: 15px; font-style: italic; color: #666;">
        When approved, the fix will be automatically implemented.
    </p>
</div>

<p style="margin-top: 20px; font-size: 12px; color: #666;">
This is an automated analysis from Copilot AI. Discovery was performed to identify the specific root cause and resolution.
</p>
</body>
</html>
"""
        
        # Send analysis email to Kendall
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"📊 [FIX-{fix_id}] {discovery_result['title']} ({feedback.rating}/5)"
        msg['From'] = 'ATCteamsupport@walmart.com'
        msg['To'] = 'kendall.rush@walmart.com'
        
        html_part = MIMEText(analysis_report, 'html')
        msg.attach(html_part)
        
        print(f"\n{'='*80}")
        print(f"STEP 3: SENDING ANALYSIS TO KENDALL")
        print(f"To: kendall.rush@walmart.com")
        print(f"Subject: {msg['Subject']}")
        print(f"{'='*80}\n")
        
        try:
            with smtplib.SMTP('smtp-gw1.homeoffice.wal-mart.com', 25, timeout=5) as server:
                server.sendmail(msg['From'], ['kendall.rush@walmart.com'], msg.as_string())
                print("[OK] Analysis email sent to kendall.rush@walmart.com!")
        except Exception as e:
            print(f"⚠️ Could not send analysis email (outside Walmart network): {e}")
            print(f"\n--- DISCOVERY RESULTS (to console) ---")
            print(f"Fix ID: FIX-{fix_id}")
            print(f"Title: {discovery_result['title']}")
            print(f"Root Cause: {discovery_result['root_cause']}")
            print(f"Resolution: {discovery_result['resolution']}")
            print(f"--- END DISCOVERY ---\n")
            print(f"💡 Approve this fix at: http://localhost:8001/admin")
    
    except Exception as e:
        print(f"⚠️ Error analyzing feedback: {e}")

@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit user feedback"""
    try:
        # Log feedback to console (always works)
        print("=" * 80)
        print("NEW FEEDBACK RECEIVED")
        print("=" * 80)
        print(f"Category: {feedback.category}")
        print(f"Rating: {feedback.rating}/5")
        print(f"Comments: {feedback.comments[:200]}")  # Truncate for console
        print(f"Timestamp: {feedback.timestamp}")
        if feedback.user_context:
            print(f"User Context: {feedback.user_context}")
        print("=" * 80)
        
        # Analyze feedback and send report to admin
        analyze_feedback_and_email_admin(feedback)
        
        # WEBHOOK: Real-time notification via webhook (Option C)
        # This will be called immediately when feedback is submitted
        try:
            import json
            import urllib.request
            
            webhook_url = os.getenv("FEEDBACK_WEBHOOK_URL")
            if webhook_url:
                webhook_payload = {
                    "timestamp": feedback.timestamp,
                    "category": feedback.category,
                    "rating": feedback.rating,
                    "comments": feedback.comments,
                    "user_context": feedback.user_context or {},
                    "alert_level": "HIGH" if feedback.rating <= 2 else "MEDIUM" if feedback.rating <= 3 else "LOW",
                    "event_type": "FEEDBACK_SUBMITTED"
                }
                
                req = urllib.request.Request(
                    webhook_url,
                    data=json.dumps(webhook_payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                try:
                    with urllib.request.urlopen(req, timeout=5) as response:
                        print(f"[OK] Webhook notification sent successfully! Status: {response.status}")
                except Exception as e:
                    print(f"⚠️ Webhook notification failed (non-blocking): {e}")
            else:
                print("ℹ️ FEEDBACK_WEBHOOK_URL not set. To enable real-time notifications, set this environment variable.")
                print("   Example: FEEDBACK_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN")
        
        except Exception as e:
            print(f"⚠️ Error sending webhook notification: {e}")
        
        # Try to send email notification (but don't fail if it doesn't work)
        email_sent = False
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Create email content
            email_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #0071ce;">New Feedback Received</h2>
                <table style="border-collapse: collapse; width: 100%; max-width: 600px;">
                    <tr>
                        <td style="padding: 10px; background: #f0f0f0; font-weight: bold; width: 150px;">Category:</td>
                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{feedback.category}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; background: #f0f0f0; font-weight: bold;">Rating:</td>
                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{feedback.rating}/5 {'⭐' * feedback.rating}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; background: #f0f0f0; font-weight: bold;">Timestamp:</td>
                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{feedback.timestamp}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; background: #f0f0f0; font-weight: bold; vertical-align: top;">Comments:</td>
                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{feedback.comments}</td>
                    </tr>
                </table>
                <br>
                <p style="color: #666; font-size: 12px;">Sent from Projects in Stores Dashboard</p>
            </body>
            </html>
            """
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"[User Feedback] {feedback.category} - Rating {feedback.rating}/5"
            msg['From'] = 'noreply-dashboard@walmart.com'
            msg['To'] = 'ATCteamsupport@walmart.com'  # STEP 1: Raw feedback goes to ATC team
            
            html_part = MIMEText(email_body, 'html')
            msg.attach(html_part)
            
            # Send email using Walmart's internal SMTP gateway
            print(f"\nSTEP 1: SENDING RAW FEEDBACK TO ATC TEAM")
            print(f"To: ATCteamsupport@walmart.com")
            print(f"Subject: {msg['Subject']}")
            
            # Walmart SMTP Configuration (no auth required for internal)
            with smtplib.SMTP('smtp-gw1.homeoffice.wal-mart.com', 25, timeout=5) as server:
                server.sendmail(msg['From'], ['ATCteamsupport@walmart.com'], msg.as_string())
                print("[OK] Raw feedback sent to ATCteamsupport@walmart.com!")
                email_sent = True
            
        except Exception as email_error:
            print(f"⚠️ Email sending failed (feedback still recorded): {email_error}")
            print("Troubleshooting: Ensure you're on Walmart VPN or network")
            print(f"Recipient: ATCteamsupport@walmart.com")
            # Continue - feedback is still logged to console
        
        # Always return success since feedback was logged
        return {
            "status": "success", 
            "message": "Feedback received. Thank you!",
            "email_sent": email_sent
        }
    except Exception as e:
        print(f"[ERROR] Error processing feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ADMIN ENDPOINTS - Fix Management System
# ============================================================================

import json
import uuid
from collections import defaultdict

PENDING_FIXES_FILE = os.path.join(os.path.dirname(__file__), "pending_fixes.json")
ACTIVITY_LOG_FILE = os.path.join(os.path.dirname(__file__), "activity_log.json")
ACTIVE_USERS_FILE = os.path.join(os.path.dirname(__file__), "active_users.json")

def load_activity_log():
    """Load activity log from JSON file"""
    try:
        if os.path.exists(ACTIVITY_LOG_FILE):
            with open(ACTIVITY_LOG_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading activity log: {e}")
    return {"activities": []}

def save_activity_log(data):
    """Save activity log to JSON file"""
    try:
        # Keep only last 500 activities
        if len(data.get("activities", [])) > 500:
            data["activities"] = data["activities"][-500:]
        with open(ACTIVITY_LOG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving activity log: {e}")
        return False

def log_activity(action: str, user: str = "Anonymous", details: str = "", category: str = "general"):
    """Log an activity to the activity log"""
    data = load_activity_log()
    activity = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "user": user,
        "details": details,
        "category": category
    }
    data["activities"].append(activity)
    save_activity_log(data)
    return activity

def load_active_users():
    """Load active users from JSON file"""
    try:
        if os.path.exists(ACTIVE_USERS_FILE):
            with open(ACTIVE_USERS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading active users: {e}")
    return {"users": {}}

def save_active_users(data):
    """Save active users to JSON file"""
    try:
        with open(ACTIVE_USERS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving active users: {e}")
        return False

def track_user_activity(user_id: str, page: str = "dashboard"):
    """Track user activity - update last seen time"""
    data = load_active_users()
    now = datetime.now()
    data["users"][user_id] = {
        "last_seen": now.strftime("%Y-%m-%d %H:%M:%S"),
        "page": page,
        "timestamp": now.timestamp()
    }
    # Clean up users not seen in last 30 minutes
    cutoff = now.timestamp() - (30 * 60)
    data["users"] = {k: v for k, v in data["users"].items() if v.get("timestamp", 0) > cutoff}
    save_active_users(data)
    return data["users"]

def load_pending_fixes():
    """Load pending fixes from JSON file"""
    try:
        if os.path.exists(PENDING_FIXES_FILE):
            with open(PENDING_FIXES_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading pending fixes: {e}")
    return {"fixes": [], "history": []}

def save_pending_fixes(data):
    """Save pending fixes to JSON file"""
    try:
        with open(PENDING_FIXES_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving pending fixes: {e}")
        return False

@app.get("/admin")
async def admin_dashboard():
    """Serve the admin dashboard"""
    admin_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "admin.html")
    if os.path.exists(admin_path):
        return FileResponse(admin_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="Admin dashboard not found")

@app.get("/api/admin/fixes")
async def get_pending_fixes():
    """Get all pending fixes and history"""
    return load_pending_fixes()

# Activity Log and User Tracking Endpoints
class ActivityLogRequest(BaseModel):
    action: str
    user: str = "Anonymous"
    details: str = ""
    category: str = "general"

class TrackUserRequest(BaseModel):
    user_id: str
    page: str = "dashboard"

@app.get("/api/admin/activity-log")
async def get_activity_log(limit: int = 100):
    """Get recent activity log entries"""
    data = load_activity_log()
    activities = data.get("activities", [])
    # Return most recent first
    return {"activities": list(reversed(activities[-limit:]))}

@app.post("/api/admin/activity-log")
async def add_activity(request: ActivityLogRequest):
    """Add a new activity log entry"""
    activity = log_activity(
        action=request.action,
        user=request.user,
        details=request.details,
        category=request.category
    )
    return {"success": True, "activity": activity}

@app.get("/api/admin/active-users")
async def get_active_users():
    """Get list of currently active users"""
    data = load_active_users()
    users = data.get("users", {})
    # Clean up old entries (not seen in 30 min)
    now = datetime.now().timestamp()
    cutoff = now - (30 * 60)
    active_users = {k: v for k, v in users.items() if v.get("timestamp", 0) > cutoff}
    return {"users": active_users, "count": len(active_users)}

@app.post("/api/admin/track-user")
async def track_user(request: TrackUserRequest):
    """Track user activity (heartbeat)"""
    users = track_user_activity(request.user_id, request.page)
    return {"success": True, "active_users": len(users)}

@app.delete("/api/admin/activity-log")
async def clear_activity_log():
    """Clear all activity log entries"""
    save_activity_log({"activities": []})
    return {"success": True, "message": "Activity log cleared"}

class AdminActionRequest(BaseModel):
    admin_user: str

@app.post("/api/admin/fixes/{fix_id}/approve")
async def approve_fix(fix_id: str, action: AdminActionRequest):
    """Approve and implement a fix"""
    data = load_pending_fixes()
    
    # Log the activity
    log_activity("Fix Approved", action.admin_user, f"Approved fix {fix_id}", "admin")
    
    # Find the fix
    fix = next((f for f in data["fixes"] if f["id"] == fix_id), None)
    if not fix:
        return {"success": False, "error": "Fix not found"}
    
    implementation_result = {"success": True, "message": ""}
    
    # If there are code changes, apply them
    if fix.get("code_changes"):
        try:
            changes = fix["code_changes"]
            file_path = changes.get("file")
            old_code = changes.get("old_code")
            new_code = changes.get("new_code")
            
            if file_path and old_code and new_code:
                # Resolve file path
                if not os.path.isabs(file_path):
                    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), file_path)
                
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if old_code in content:
                        new_content = content.replace(old_code, new_code, 1)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        implementation_result["message"] = f"Code updated in {changes.get('file')}"
                        print(f"[ADMIN] Code fix applied to {file_path} by {action.admin_user}")
                    else:
                        implementation_result["message"] = "Code pattern not found - manual review needed"
                else:
                    implementation_result["message"] = f"File not found: {file_path}"
        except Exception as e:
            implementation_result["success"] = False
            implementation_result["error"] = str(e)
            print(f"[ADMIN ERROR] Failed to apply fix: {e}")
    
    # Move fix to history
    fix["status"] = "approved"
    fix["actioned_by"] = action.admin_user
    fix["actioned_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fix["implementation_result"] = implementation_result
    
    data["fixes"] = [f for f in data["fixes"] if f["id"] != fix_id]
    data["history"].append(fix)
    
    save_pending_fixes(data)
    
    return {"success": True, "message": "Fix approved and implemented", "result": implementation_result}

@app.post("/api/admin/fixes/{fix_id}/deny")
async def deny_fix(fix_id: str, action: AdminActionRequest):
    """Deny a fix"""
    data = load_pending_fixes()
    
    # Log the activity
    log_activity("Fix Denied", action.admin_user, f"Denied fix {fix_id}", "admin")
    
    fix = next((f for f in data["fixes"] if f["id"] == fix_id), None)
    if not fix:
        return {"success": False, "error": "Fix not found"}
    
    fix["status"] = "denied"
    fix["actioned_by"] = action.admin_user
    fix["actioned_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data["fixes"] = [f for f in data["fixes"] if f["id"] != fix_id]
    data["history"].append(fix)
    
    save_pending_fixes(data)
    
    return {"success": True, "message": "Fix denied"}

@app.post("/api/admin/fixes/{fix_id}/hold")
async def hold_fix(fix_id: str, action: AdminActionRequest):
    """Place a fix on hold (keep in pending but mark as held)"""
    data = load_pending_fixes()
    
    # Log the activity
    log_activity("Fix On Hold", action.admin_user, f"Placed fix {fix_id} on hold", "admin")
    
    for fix in data["fixes"]:
        if fix["id"] == fix_id:
            fix["on_hold"] = True
            fix["hold_by"] = action.admin_user
            fix["hold_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    
    save_pending_fixes(data)
    
    return {"success": True, "message": "Fix placed on hold"}

def create_pending_fix(feedback: FeedbackRequest, discovery_result: dict):
    """Create a new pending fix from feedback analysis with discovery"""
    fix_id = str(uuid.uuid4())[:8]
    
    fix = {
        "id": fix_id,
        "title": discovery_result.get("title", f"Feedback: {feedback.category}"),
        "feedback_category": feedback.category,
        "feedback_rating": feedback.rating,
        "feedback_comments": feedback.comments,
        "timestamp": feedback.timestamp,
        "priority": "high" if feedback.rating <= 2 else "medium" if feedback.rating <= 3 else "low",
        "root_cause": discovery_result.get("root_cause", "Analysis pending"),
        "resolution": discovery_result.get("resolution", "Manual review required"),
        "code_changes": discovery_result.get("code_changes"),
        "user_context": feedback.user_context,
        "investigation_notes": discovery_result.get("investigation_notes", []),
        "files_analyzed": discovery_result.get("files_analyzed", []),
        "requires_ai_review": discovery_result.get("requires_ai_review", False)
    }
    
    data = load_pending_fixes()
    data["fixes"].append(fix)
    save_pending_fixes(data)
    
    return fix


# =============================================================================
# AI-POWERED CODE FIX GENERATOR
# =============================================================================

class AICodeAnalyzer:
    """
    Intelligent code analyzer that reads the actual codebase and generates
    specific, reviewable code fixes based on user feedback.
    """
    
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(__file__))
        self.frontend_path = os.path.join(self.base_path, "frontend", "index.html")
        self.ai_agent_path = os.path.join(self.base_path, "backend", "ai_agent.py")
        self.main_path = os.path.join(self.base_path, "backend", "main.py")
    
    def read_file_section(self, file_path: str, search_pattern: str, context_lines: int = 10) -> tuple:
        """Read a section of code around a pattern match"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                if search_pattern.lower() in line.lower():
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    return (''.join(lines[start:end]), i + 1, start + 1, end)
            return (None, 0, 0, 0)
        except Exception as e:
            return (None, 0, 0, 0)
    
    def find_function(self, file_path: str, function_name: str) -> str:
        """Extract a complete function from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find function start
            import re
            pattern = rf'(def {function_name}\([^)]*\):.*?)(?=\ndef |\nclass |\Z)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return match.group(1)
            return None
        except:
            return None
    
    def analyze_filter_issue(self, feedback_text: str, context: dict) -> dict:
        """Analyze filter-related issues and generate fixes"""
        result = {"code_changes": None, "analysis": ""}
        
        # Extract filter names mentioned
        filter_keywords = {
            'division': 'division_filter',
            'region': 'region_filter', 
            'market': 'market_filter',
            'phase': 'phase_filter',
            'source': 'source_filter',
            'wm week': 'wm_week_filter',
            'week': 'wm_week_filter'
        }
        
        mentioned_filters = []
        for keyword, filter_name in filter_keywords.items():
            if keyword in feedback_text.lower():
                mentioned_filters.append((keyword, filter_name))
        
        result["analysis"] = f"Filters mentioned: {mentioned_filters}"
        
        # Check if this filter is handled in AI agent
        if mentioned_filters:
            keyword, filter_name = mentioned_filters[0]
            code_section, line_num, _, _ = self.read_file_section(
                self.ai_agent_path, filter_name, context_lines=5
            )
            
            if code_section:
                result["analysis"] += f"\nFound {filter_name} handling at line {line_num}"
            else:
                result["analysis"] += f"\nWARNING: {filter_name} may not be implemented"
        
        return result
    
    def analyze_search_issue(self, feedback_text: str, context: dict) -> dict:
        """Analyze search-related issues"""
        result = {"code_changes": None, "analysis": ""}
        
        # Extract what they were searching for
        search_terms = []
        if "You:" in feedback_text:
            # Extract user queries from chat
            import re
            queries = re.findall(r'You:\s*([^\n]+)', feedback_text)
            search_terms = queries
        
        result["analysis"] = f"User searched for: {search_terms}"
        
        # Check if 0 results were mentioned
        if any(x in feedback_text.lower() for x in ['0 result', 'no result', '0 project']):
            result["analysis"] += "\n⚠️ Zero results issue detected"
            
            # Check current filters at time of feedback
            current_filters = context.get("current_filters", {})
            active = {k: v for k, v in current_filters.items() if v}
            if active:
                result["analysis"] += f"\nActive filters at time: {active}"
        
        return result
    
    def generate_ai_agent_fix(self, issue_type: str, details: dict) -> dict:
        """Generate a fix for the AI agent based on issue type"""
        
        if issue_type == "missing_filter_handling":
            filter_name = details.get("filter_name", "unknown")
            filter_value = details.get("filter_value", "Unknown")
            
            # Read current filter handling section
            code_section, _, _, _ = self.read_file_section(
                self.ai_agent_path, "division_filter", context_lines=20
            )
            
            if code_section and filter_name not in code_section:
                return {
                    "file": "backend/ai_agent.py",
                    "description": f"Add {filter_name} handling to AI agent",
                    "old_code": "# Add filter handling here",
                    "new_code": f"# Handle {filter_name}\nif '{filter_value.lower()}' in query_lower:\n    data_payload['{filter_name}'] = '{filter_value}'"
                }
        
        return None

# Global analyzer instance
code_analyzer = AICodeAnalyzer()


def perform_discovery(feedback: FeedbackRequest) -> dict:
    """
    Perform AI-powered discovery on the feedback to find root cause and specific resolution.
    This analyzes the feedback context, investigates the codebase, and proposes specific fixes.
    """
    import re
    import os
    
    comments_lower = feedback.comments.lower()
    context = feedback.user_context or {}
    
    discovery_result = {
        "title": "",
        "root_cause": "",
        "resolution": "",
        "code_changes": None,
        "investigation_notes": [],
        "files_analyzed": [],
        "requires_ai_review": False
    }
    
    # =========================================================================
    # PHASE 1: Extract key information from feedback
    # =========================================================================
    
    # Extract any chat conversation from comments
    chat_context = ""
    if "You:" in feedback.comments or "Sparky:" in feedback.comments:
        chat_context = feedback.comments
    
    # Get filter state at time of feedback
    current_filters = context.get("current_filters", {})
    active_filters = {k: v for k, v in current_filters.items() if v and (isinstance(v, str) or len(v) > 0)}
    
    # =========================================================================
    # PHASE 2: Intelligent pattern analysis with code investigation
    # =========================================================================
    
    base_path = os.path.dirname(os.path.dirname(__file__))
    frontend_path = os.path.join(base_path, "frontend", "index.html")
    ai_agent_path = os.path.join(base_path, "backend", "ai_agent.py")
    
    # Pattern: Filter/Search conflict (like the Division issue)
    if any(phrase in comments_lower for phrase in [
        "showed 0", "shows 0", "0 result", "no result",
        "didn't remove", "didn't clear", "still there",
        "then i", "reworded", "second", "next"
    ]) and any(word in comments_lower for word in ["filter", "search", "division", "region", "market"]):
        
        discovery_result["title"] = "Filter State Conflict"
        discovery_result["investigation_notes"].append("User experienced filter conflict between consecutive queries")
        
        # Analyze the chat to understand the flow
        if chat_context:
            discovery_result["investigation_notes"].append(f"Chat context provided - analyzing query flow")
            
            # Check if there's a pattern of search → filter conflict
            if "division" in comments_lower.lower():
                discovery_result["root_cause"] = """When user asks about a division (e.g., "East division"), Sparky may:
1. First interpret "division" as a search keyword (adds to search box)
2. Then on next query, recognize "East" as a Division filter value
3. But the search box still contains "division" from previous query
4. Combined filter (Search="division" + Division="EAST") returns 0 results

The frontend applies filters additively without clearing previous state."""
                
                discovery_result["resolution"] = """Clear the search text box automatically when Sparky applies a dropdown filter (Division, Region, Market, Phase, WM Week), unless a new search term is explicitly being set. This prevents stale search terms from conflicting with new filter selections."""
                
                # Check if fix already exists in code
                try:
                    with open(frontend_path, 'r', encoding='utf-8') as f:
                        frontend_code = f.read()
                    
                    if "hasDropdownFilter" in frontend_code:
                        discovery_result["investigation_notes"].append("✅ Fix already applied - hasDropdownFilter check exists")
                        discovery_result["resolution"] = "Fix was already implemented. If issue persists, browser may need hard refresh (Ctrl+Shift+R) to clear cache."
                    else:
                        discovery_result["files_analyzed"].append("frontend/index.html")
                        discovery_result["code_changes"] = {
                            "file": "frontend/index.html",
                            "description": "Add logic to clear search box when applying dropdown filters",
                            "old_code": """                // Apply suggested project search filter
                if (data.data && data.data.suggested_filter) {
                    document.getElementById('filter-title').value = data.data.suggested_filter;
                }""",
                            "new_code": """                // Check if any dropdown filters are being applied (not just search)
                const hasDropdownFilter = data.data && (
                    data.data.division_filter || 
                    data.data.region_filter || 
                    data.data.market_filter || 
                    data.data.phase_filter || 
                    data.data.wm_week_filter
                );
                
                // If applying dropdown filters and NO new search term, clear the search box first
                // This prevents old search terms from conflicting with new dropdown filters
                if (hasDropdownFilter && !(data.data && data.data.suggested_filter)) {
                    document.getElementById('filter-title').value = '';
                }
                
                // Apply suggested project search filter
                if (data.data && data.data.suggested_filter) {
                    document.getElementById('filter-title').value = data.data.suggested_filter;
                }"""
                        }
                except Exception as e:
                    discovery_result["investigation_notes"].append(f"Could not read frontend file: {e}")
        else:
            discovery_result["root_cause"] = "Filter state conflict detected but specific cause unclear without chat context."
            discovery_result["resolution"] = "Review filter application logic in frontend. Ensure filters are cleared appropriately between queries."
            discovery_result["requires_ai_review"] = True
    
    # Pattern: Source filter not working (Realty, Operations, etc. returning 0 results)
    elif any(source in comments_lower for source in ["realty", "operations", "store support"]) and \
         any(phrase in comments_lower for phrase in ["0 result", "no result", "shows 0", "showed 0", "doesn't work", "not working"]):
        
        # Extract which source was mentioned
        source_mentioned = None
        if "realty" in comments_lower:
            source_mentioned = "Realty"
        elif "operations" in comments_lower:
            source_mentioned = "Operations"
        elif "store support" in comments_lower:
            source_mentioned = "Store Support"
        
        discovery_result["title"] = f"Source Filter Issue ({source_mentioned})"
        discovery_result["investigation_notes"].append(f"User searching for {source_mentioned} projects returned 0 results")
        
        # Check if source_filter is handled in frontend
        try:
            with open(frontend_path, 'r', encoding='utf-8') as f:
                frontend_code = f.read()
            
            if "source_filter" in frontend_code:
                discovery_result["investigation_notes"].append("✅ Frontend already handles source_filter")
                discovery_result["root_cause"] = f"Source filter for '{source_mentioned}' is implemented but may have data issues."
                discovery_result["resolution"] = f"Verify BigQuery has projects with project_source = '{source_mentioned}'. Check case sensitivity."
            else:
                discovery_result["root_cause"] = f"Frontend does NOT handle source_filter from AI agent response."
                discovery_result["resolution"] = f"Add source_filter handling to frontend JavaScript."
                discovery_result["files_analyzed"].append("frontend/index.html")
                
                # Generate the actual fix
                discovery_result["code_changes"] = {
                    "file": "frontend/index.html",
                    "description": f"Add source_filter handling so '{source_mentioned}' queries work",
                    "old_code": """                const hasDropdownFilter = data.data && (
                    data.data.division_filter || 
                    data.data.region_filter || 
                    data.data.market_filter || 
                    data.data.phase_filter || 
                    data.data.wm_week_filter
                );""",
                    "new_code": """                const hasDropdownFilter = data.data && (
                    data.data.division_filter || 
                    data.data.region_filter || 
                    data.data.market_filter || 
                    data.data.phase_filter || 
                    data.data.wm_week_filter ||
                    data.data.source_filter
                );
                
                // Apply source filter
                if (data.data && data.data.source_filter) {
                    document.getElementById('filter-source').value = data.data.source_filter;
                }"""
                }
        except Exception as e:
            discovery_result["investigation_notes"].append(f"Could not read frontend: {e}")
            discovery_result["requires_ai_review"] = True
        
        discovery_result["files_analyzed"].append("backend/ai_agent.py")
        discovery_result["files_analyzed"].append("frontend/index.html")
    
    # Pattern: Owner search not working
    elif any(phrase in comments_lower for phrase in ["owned by", "owner", "who owns"]) and \
         any(phrase in comments_lower for phrase in ["not found", "no projects", "doesn't work", "can't find", "0 result", "no result"]):
        
        discovery_result["title"] = "Owner Search Issue"
        discovery_result["investigation_notes"].append("User having trouble searching by project owner")
        
        # Extract owner name if mentioned
        owner_match = re.search(r'(?:owned by|owner[:\s]+)([A-Za-z]+(?:\s+[A-Za-z]+)?)', feedback.comments, re.IGNORECASE)
        owner_name = owner_match.group(1).strip() if owner_match else "unknown"
        
        discovery_result["root_cause"] = f"""Owner search for '{owner_name}' returned 0 results. The AI agent may not be:
1. Recognizing "owned by" or "owner" as owner search intent
2. Applying the owner filter correctly to the dataset
3. Handling partial name matches (first name only, last name only)"""
        
        discovery_result["files_analyzed"].append("backend/ai_agent.py")
        
        # Check if owner search exists in AI agent
        try:
            with open(ai_agent_path, 'r', encoding='utf-8') as f:
                ai_code = f.read()
            
            if "owned by" in ai_code.lower() or "owner" in ai_code.lower():
                discovery_result["investigation_notes"].append("✅ Owner search pattern exists in AI agent")
                discovery_result["resolution"] = f"Owner search is implemented. Verify '{owner_name}' exists in Owner field. Check for name format mismatches."
            else:
                discovery_result["investigation_notes"].append("⚠️ Owner search pattern NOT found in AI agent")
                discovery_result["resolution"] = "Add owner search handling to AI agent."
                
                # Generate fix to add owner search
                discovery_result["code_changes"] = {
                    "file": "backend/ai_agent.py",
                    "description": "Add owner search capability to AI agent",
                    "old_code": "# Owner search will be added here",
                    "new_code": f"""# Handle owner search
        if any(phrase in query_lower for phrase in ['owned by', 'owner is', 'belongs to']):
            import re
            owner_match = re.search(r'(?:owned by|owner is|belongs to)\\s+([A-Za-z]+(?:\\s+[A-Za-z]+)?)', query_lower)
            if owner_match:
                owner_name = owner_match.group(1).strip()
                matching = [p for p in all_projects if owner_name.lower() in p.get('owner', '').lower()]
                if matching:
                    return {{"response": f"Found {{len(matching)}} projects owned by {{owner_name}}", "data": {{"projects": matching[:20], "owner_search": owner_name}}}}"""
                }
        except Exception as e:
            discovery_result["investigation_notes"].append(f"Could not analyze AI agent: {e}")
            discovery_result["requires_ai_review"] = True
    
    # Pattern: AI response quality issues
    elif any(phrase in comments_lower for phrase in ["repeated", "duplicate", "spam", "too many", "same thing", "keeps saying"]):
        discovery_result["title"] = "AI Response Quality Issue"
        discovery_result["investigation_notes"].append("User reports duplicate or excessive content in AI responses")
        
        discovery_result["root_cause"] = "AI response contains duplicate or excessive content. This typically happens when:\n1. Data is not deduplicated before display\n2. Multiple response formats are being combined\n3. Loop logic is adding items multiple times"
        
        discovery_result["files_analyzed"].append("backend/ai_agent.py")
        
        # Check for deduplication in AI agent
        try:
            with open(ai_agent_path, 'r', encoding='utf-8') as f:
                ai_code = f.read()
            
            if "set(" in ai_code or "deduplicate" in ai_code.lower() or "unique" in ai_code.lower():
                discovery_result["investigation_notes"].append("✅ Deduplication logic exists")
                discovery_result["resolution"] = "Deduplication exists but may not cover all cases. Review specific response type mentioned in feedback."
            else:
                discovery_result["investigation_notes"].append("⚠️ No deduplication found")
                discovery_result["resolution"] = "Add deduplication to response formatting"
                
                discovery_result["code_changes"] = {
                    "file": "backend/ai_agent.py",
                    "description": "Add deduplication to prevent repeated content",
                    "old_code": "# Deduplication will be added here",
                    "new_code": """# Deduplicate results before returning
        seen = set()
        unique_results = []
        for item in results:
            key = item.get('project_id') or str(item)
            if key not in seen:
                seen.add(key)
                unique_results.append(item)
        results = unique_results"""
                }
        except Exception as e:
            discovery_result["investigation_notes"].append(f"Could not analyze: {e}")
            discovery_result["requires_ai_review"] = True
    
    # Pattern: Performance issues
    elif any(phrase in comments_lower for phrase in ["slow", "takes long", "loading", "wait", "timeout", "freeze", "hanging"]):
        discovery_result["title"] = "Performance Issue"
        discovery_result["investigation_notes"].append("User experiencing slow application performance")
        
        discovery_result["root_cause"] = """Application experiencing slow performance. Common causes:
1. Loading all projects on page load (can be 100k+ records)
2. No result caching - every query hits BigQuery
3. Large DOM updates when displaying many results
4. No loading indicators making it feel slower"""
        
        discovery_result["files_analyzed"].append("frontend/index.html")
        discovery_result["files_analyzed"].append("backend/database.py")
        
        # Check for loading indicator
        try:
            with open(frontend_path, 'r', encoding='utf-8') as f:
                frontend_code = f.read()
            
            has_loading = "loading" in frontend_code.lower() or "spinner" in frontend_code.lower()
            
            if not has_loading:
                discovery_result["investigation_notes"].append("⚠️ No loading indicator found")
                discovery_result["resolution"] = "Add loading spinner to improve perceived performance"
                
                discovery_result["code_changes"] = {
                    "file": "frontend/index.html",
                    "description": "Add loading indicator for better UX during queries",
                    "old_code": """        async function sendMessage() {
            const input = document.getElementById('sparkyInput');
            const message = input.value.trim();
            if (!message) return;""",
                    "new_code": """        async function sendMessage() {
            const input = document.getElementById('sparkyInput');
            const message = input.value.trim();
            if (!message) return;
            
            // Show loading indicator
            const chatMessages = document.getElementById('chatMessages');
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message assistant loading';
            loadingDiv.innerHTML = '<span class="loading-dots">Thinking<span>.</span><span>.</span><span>.</span></span>';
            chatMessages.appendChild(loadingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;"""
                }
            else:
                discovery_result["investigation_notes"].append("✅ Loading indicator exists")
                discovery_result["resolution"] = "Loading indicator exists. Consider adding server-side caching or pagination for large result sets."
        except Exception as e:
            discovery_result["investigation_notes"].append(f"Could not analyze frontend: {e}")
            discovery_result["requires_ai_review"] = True
    
    # Pattern: UI/Visual issues
    elif any(phrase in comments_lower for phrase in ["display", "show", "see", "visual", "layout", "button", "click"]):
        discovery_result["title"] = "UI/Visual Issue"
        discovery_result["root_cause"] = "User interface element not behaving as expected. Need to identify specific element and expected vs actual behavior."
        discovery_result["resolution"] = "Identify specific UI element from feedback. Review CSS styling and JavaScript event handlers. Test across browsers."
        discovery_result["files_analyzed"].append("frontend/index.html")
        discovery_result["requires_ai_review"] = True
    
    # Pattern: Data accuracy
    elif any(phrase in comments_lower for phrase in ["wrong", "incorrect", "inaccurate", "doesn't match", "should be"]):
        discovery_result["title"] = "Data Accuracy Issue"
        discovery_result["root_cause"] = "Data displayed doesn't match user expectations. Could be data transformation error, stale data, or misunderstanding of data source."
        discovery_result["resolution"] = "Verify data pipeline: BigQuery → API → Frontend. Check for any transformations. Compare with source of truth in Intake Hub."
        discovery_result["files_analyzed"].append("backend/database.py")
    
    # Default: Requires detailed AI review
    else:
        discovery_result["title"] = f"Feedback Analysis: {feedback.category}"
        discovery_result["root_cause"] = f"Issue reported in '{feedback.category}' category requires detailed analysis."
        discovery_result["resolution"] = "This feedback requires manual AI review to determine specific root cause and resolution."
        discovery_result["requires_ai_review"] = True
        discovery_result["investigation_notes"].append("No specific pattern matched - flagged for detailed review")
    
    # =========================================================================
    # PHASE 3: Add context for AI review
    # =========================================================================
    
    if discovery_result["requires_ai_review"]:
        discovery_result["investigation_notes"].append(f"Active filters at time of feedback: {active_filters}")
        discovery_result["investigation_notes"].append(f"Projects displayed: {context.get('projects_displayed', 'unknown')}")
    
    return discovery_result


# ============================================================================
# EMAIL REPORTING ENDPOINTS (SIMPLIFIED VERSION)
# ============================================================================
# Uses Windows Task Scheduler instead of APScheduler (no package installation needed)
# Sends HTML emails using built-in smtplib (no reportlab needed)

@app.get("/api/reports/options")
async def get_report_options():
    """Get available options for report configuration"""
    return {
        "content_types": [
            "All Projects",
            "New Projects (Last 7 Days)",
            "Completed Projects",
            "Overdue Projects",
            "Projects by Status",
            "Projects by Partner",
            "Projects by Store Area",
            "Projects by Priority",
            "Project Trends",
            "Completion Rates",
            "Performance Metrics",
            "Summary Dashboard",
            "Detailed Project List"
        ],
        "frequencies": [
            "Daily",
            "Weekly", 
            "Every Monday",
            "Every Tuesday",
            "Every Wednesday",
            "Every Thursday",
            "Every Friday",
            "Bi-Weekly",
            "Monthly"
        ],
        "days_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "timeframes": ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last Quarter", "Last Year", "All Time"],
        "available_columns": [
            "intake_card_number",
            "title_with_link", 
            "partner",
            "store_id",
            "store_name",
            "project_title",
            "status",
            "priority",
            "due_date",
            "assigned_to",
            "completion_date",
            "days_overdue",
            "store_area",
            "business_organization",
            "owner",
            "phase",
            "health",
            "archived",
            "projected_completion_date",
            "director",
            "sr_director",
            "vp",
            "division",
            "region",
            "market"
        ]
    }


@app.get("/api/reports/configs")
async def get_report_configs(request: Request, user_id: str = None):
    """Get report configurations - only return reports for authenticated user (or all if admin)"""
    import json
    
    # Get the currently authenticated user (checks session first, then Windows AD) - ALWAYS use this, ignore user_id parameter
    current_user = get_current_authenticated_user(request)
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated. Please log in via Windows AD.")
    
    # Check if user is admin
    email_variants = get_admin_email_variants(current_user)
    is_admin = any(variant in admin_config.get('admins', []) for variant in email_variants)
    
    configs = []
    configs_dir = Path(__file__).parent / "report_configs"
    
    # Load all config files
    if configs_dir.exists():
        for config_file in configs_dir.glob("*.json"):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    # Return config if:
                    # 1. User is admin (can see all reports), OR
                    # 2. Report belongs to the authenticated user
                    if is_admin or config.get('user_id') == current_user:
                        configs.append(config)
            except:
                pass
    
    # Log access for audit trail
    log_activity(
        action='Accessed Email Reports',
        user=current_user,
        details=f'Retrieved {len(configs)} report configurations',
        category='email_reports'
    )
    
    return {"configs": configs}


@app.post("/api/reports/configs")
async def create_report_config(request: Request):
    """Create new report configuration with Windows Task Scheduler
    
    Automatically assigns report to authenticated user - user_id parameter is ignored.
    Only authenticated users can create reports for themselves.
    """
    import json
    import uuid
    
    try:
        # Get authenticated user (checks session first, then Windows) - ALWAYS use this, never trust request data
        current_user = get_current_authenticated_user(request)
        
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated. Please log in via Windows AD.")
        
        # Parse request body
        body = await request.json()
        
        # Generate config ID
        config_id = str(uuid.uuid4())
        
        # Add metadata AND FORCE user_id to authenticated user
        # This prevents any user from creating reports for other users
        body['config_id'] = config_id
        body['user_id'] = current_user  # FORCE to authenticated user
        body['created_at'] = datetime.now().isoformat()
        body['last_sent'] = None
        
        # Save config to file
        configs_dir = Path(__file__).parent / "report_configs"
        configs_dir.mkdir(exist_ok=True)
        config_file = configs_dir / f"{config_id}.json"
        
        with open(config_file, 'w') as f:
            json.dump(body, f, indent=2)
        
        # Log the action
        log_activity(
            action='Created Email Report',
            user=current_user,
            details=f'Report: {body.get("report_name", "Unnamed")} (ID: {config_id})',
            category='email_reports'
        )
        
        # Create Windows scheduled task if active
        if body.get('is_active', False):
            scheduler_manager.create_scheduled_task(body)
        
        return {
            "success": True,
            "message": "Report configuration created successfully",
            "config_id": config_id,
            "config": body
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating report: {str(e)}")


@app.get("/api/reports/configs/{config_id}")
async def get_report_config(config_id: str):
    """Get a single report configuration"""
    import json
    
    try:
        configs_dir = Path(__file__).parent / "report_configs"
        config_file = configs_dir / f"{config_id}.json"
        
        if not config_file.exists():
            raise HTTPException(status_code=404, detail="Configuration not found")
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        return config
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading report: {str(e)}")


@app.put("/api/reports/configs/{config_id}")
async def update_report_config(config_id: str, http_request: Request):
    """Update report configuration - only owner or admin can update
    
    Preserves the original user_id - reports cannot be transferred between users.
    """
    import json
    
    try:
        # Get authenticated user (checks session first, then Windows)
        current_user = get_current_authenticated_user(http_request)
        
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated. Please log in via Windows AD.")
        
        # Parse request body
        request = await http_request.json()
        
        # Check admin status
        email_variants = get_admin_email_variants(current_user)
        is_admin = any(variant in admin_config.get('admins', []) for variant in email_variants)
        
        configs_dir = Path(__file__).parent / "report_configs"
        config_file = configs_dir / f"{config_id}.json"
        
        if not config_file.exists():
            raise HTTPException(status_code=404, detail="Configuration not found")
        
        # Load existing config to verify ownership
        with open(config_file, 'r') as f:
            existing_config = json.load(f)
        
        # Check authorization: must be owner or admin
        owner = existing_config.get('user_id')
        if owner != current_user and not is_admin:
            raise HTTPException(
                status_code=403, 
                detail="You can only update your own reports. Contact admin if you need help."
            )
        
        # Update config - PRESERVE user_id, never allow changing ownership
        request['config_id'] = config_id
        request['user_id'] = owner  # FORCE preservation of original owner
        request['updated_at'] = datetime.now().isoformat()
        request['created_at'] = existing_config.get('created_at')  # Keep original creation date
        
        with open(config_file, 'w') as f:
            json.dump(request, f, indent=2)
        
        # Log the action
        log_activity(
            action='Updated Email Report',
            user=current_user,
            details=f'Report: {request.get("report_name", "Unnamed")} (ID: {config_id})',
            category='email_reports'
        )
        
        # Update Windows scheduled task
        if request.get('is_active', False):
            scheduler_manager.update_scheduled_task(request)
        else:
            scheduler_manager.disable_task(config_id)
        
        return {
            "success": True,
            "message": "Report configuration updated successfully",
            "config": request
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating report: {str(e)}")


@app.delete("/api/reports/configs/{config_id}")
async def delete_report_config(config_id: str, request: Request):
    """Delete report configuration - only owner or admin can delete"""
    import json
    
    try:
        # Get authenticated user (checks session first, then Windows)
        current_user = get_current_authenticated_user(request)
        
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated. Please log in via Windows AD.")
        
        # Check admin status
        email_variants = get_admin_email_variants(current_user)
        is_admin = any(variant in admin_config.get('admins', []) for variant in email_variants)
        
        configs_dir = Path(__file__).parent / "report_configs"
        config_file = configs_dir / f"{config_id}.json"
        
        if not config_file.exists():
            raise HTTPException(status_code=404, detail="Configuration not found")
        
        # Load config to verify ownership
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Check authorization: must be owner or admin
        owner = config.get('user_id')
        if owner != current_user and not is_admin:
            raise HTTPException(
                status_code=403, 
                detail="You can only delete your own reports. Contact admin if you need help."
            )
        
        # Log the action
        log_activity(
            action='Deleted Email Report',
            user=current_user,
            details=f'Report: {config.get("report_name", "Unnamed")} (ID: {config_id})',
            category='email_reports'
        )
        
        # Delete Windows scheduled task
        scheduler_manager.delete_scheduled_task(config_id)
        
        # Delete config file
        config_file.unlink()
        
        return {
            "success": True,
            "message": "Report configuration deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting report: {str(e)}")


@app.post("/api/reports/generate")
async def generate_report(request: dict):
    """Generate and send report immediately
    
    Parameters:
        config_id: ID of the report configuration
        override_email: (optional) Override recipient for testing
        current_user_email: (optional) Email of logged-in user - if provided, report sends to them instead
    """
    import json
    
    try:
        config_id = request.get('config_id')
        override_email = request.get('override_email')
        current_user_email = request.get('current_user_email')
        
        # Load config
        configs_dir = Path(__file__).parent / "report_configs"
        config_file = configs_dir / f"{config_id}.json"
        
        if not config_file.exists():
            raise HTTPException(status_code=404, detail="Configuration not found")
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Generate and send report with user email
        result = await email_service.generate_and_send_report(
            config, 
            current_user_email=current_user_email,
            override_email=override_email
        )
        
        # Log execution (for test emails and manual triggers)
        def log_execution(config_id_val, success, recipients, error_msg=None, report_name_val=None):
            """Log report execution locally"""
            log_file = Path(__file__).parent / "report_execution_log.json"
            log_entry = {
                "config_id": config_id_val,
                "report_name": report_name_val or config_id_val,
                "timestamp": datetime.now().isoformat(),
                "status": "success" if success else "failed",
                "recipients": ', '.join(recipients) if recipients else "",
                "error_message": error_msg
            }
            
            try:
                logs = []
                if log_file.exists():
                    with open(log_file, 'r') as f:
                        logs = json.load(f)
                logs.append(log_entry)
                logs = logs[-1000:]  # Keep last 1000
                with open(log_file, 'w') as f:
                    json.dump(logs, f, indent=2)
            except Exception as e:
                print(f"⚠️ Error logging: {e}")
        
        log_execution(
            config_id,
            result['success'],
            result.get('sent_to', []),
            error_msg=None if result['success'] else result.get('message'),
            report_name_val=config.get('report_name', 'Unknown Report')
        )
        
        if result['success']:
            # Update last_sent timestamp
            config['last_sent'] = result['timestamp']
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@app.post("/api/reports/toggle/{config_id}")
async def toggle_report(config_id: str, is_active: bool):
    """Enable or disable a report schedule"""
    import json
    
    try:
        configs_dir = Path(__file__).parent / "report_configs"
        config_file = configs_dir / f"{config_id}.json"
        
        if not config_file.exists():
            raise HTTPException(status_code=404, detail="Configuration not found")
        
        # Update config
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        config['is_active'] = is_active
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Enable/disable Windows scheduled task
        if is_active:
            scheduler_manager.enable_task(config_id)
        else:
            scheduler_manager.disable_task(config_id)
        
        return {
            "success": True,
            "message": f"Report {'enabled' if is_active else 'disabled'} successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error toggling report: {str(e)}")


@app.get("/api/reports/logs")
async def get_report_logs(config_id: Optional[str] = None, limit: int = 50):
    """Get execution logs for reports"""
    import json
    
    try:
        # Read logs directly from file without needing scheduler
        log_file = Path(__file__).parent / "report_execution_log.json"
        
        if not log_file.exists():
            return []
        
        with open(log_file, 'r') as f:
            logs = json.load(f)
        
        # Filter by config_id if provided
        if config_id:
            logs = [log for log in logs if log.get("config_id") == config_id]
        
        # Return most recent logs
        return sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]
        
    except Exception as e:
        print(f"⚠️ Error retrieving logs: {e}")
        return []


@app.delete("/api/reports/configs/{config_id}")
async def delete_report_config(config_id: str):
    """Delete a report configuration"""
    import json
    
    try:
        configs_dir = Path(__file__).parent / "report_configs"
        config_file = configs_dir / f"{config_id}.json"
        
        if not config_file.exists():
            raise HTTPException(status_code=404, detail="Configuration not found")
        
        # Delete the config file
        config_file.unlink()
        
        # Delete the scheduled task if it exists
        try:
            scheduler_manager.delete_task(config_id)
        except:
            pass  # Task may not exist, that's ok
        
        return {
            "success": True,
            "message": "Report deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting report: {str(e)}")


# Mount static files (images, logos, etc.) from frontend directory
frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir)), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)

