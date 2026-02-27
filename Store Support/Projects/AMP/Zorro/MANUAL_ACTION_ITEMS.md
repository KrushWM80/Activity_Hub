# Zorro - Manual Action Items Required

**Last Updated**: January 21, 2026  
**Status**: Production Pilot Active - Scaling Preparation

These items require your direct action and cannot be automated. Complete them in order to scale beyond pilot phase.

---

## 🔴 CRITICAL - Required for Phase 2 (February 2026)

### 1. Install Updated Dependencies

New dependencies added for database and async processing:

```powershell
cd "c:\Users\hrisaac\OneDrive - Walmart Inc\Documents\VSCode\Projects\zorro"
pip install -r requirements.txt
```

**New packages**:
- `sqlalchemy>=2.0.0` - Database ORM
- `psycopg2-binary>=2.9.9` - PostgreSQL driver
- `celery[redis]>=5.3.0` - Async task queue
- `redis>=5.0.0` - Message broker

### 2. Set Up PostgreSQL Database **[BLOCKING SCALE]**

The JSON file storage must be replaced with a proper database for production scale.

**Option A: Local Development (Docker) - FASTEST**
```powershell
# Start PostgreSQL container
docker run -d `
  --name zorro-postgres `
  -e POSTGRES_USER=zorro `
  -e POSTGRES_PASSWORD=zorro_dev_password `
  -e POSTGRES_DB=zorro `
  -p 5432:5432 `
  postgres:15-alpine

# Verify it's running
docker ps | Select-String zorro-postgres

# Update .env
@"
DATABASE_URL=postgresql://zorro:zorro_dev_password@localhost:5432/zorro
SQL_ECHO=false
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
"@ | Out-File -Append .env

# Run migrations
python -c "from src.database import get_db, run_migrations; run_migrations(get_db())"
```

**Option B: Walmart Enterprise PostgreSQL (Request via ServiceNow)**
1. Go to https://servicenow.walmart.com
2. Request: "PostgreSQL Database for Zorro Video Platform"
3. Details:
   - **Purpose**: Production video generation platform
   - **Size**: 50GB initial, 200GB growth
   - **Users**: 10-50 concurrent
   - **Backup**: Daily with 30-day retention
4. Wait for provisioning (typically 3-5 business days)
5. Update `.env` with provided connection string

**Option C: Azure Database for PostgreSQL**
1. Contact Walmart Cloud Services
2. Request Azure PostgreSQL Flexible Server
3. Tier: General Purpose (2-4 vCores, 8-16GB RAM)
4. Update `.env` with connection string

### 3. Set Up Redis and Celery **[BLOCKING SCALE]**

Required for async video generation (prevents UI blocking).

**Step 1: Install Redis**
```powershell
# Option A: Docker (RECOMMENDED)
docker run -d `
  --name zorro-redis `
  -p 6379:6379 `
  redis:7-alpine

# Option B: Windows WSL + Ubuntu
# wsl --install
# wsl -d Ubuntu
# sudo apt update && sudo apt install redis-server
# sudo service redis-server start
```

**Step 2: Configure Celery**
```powershell
# Add to .env
@"
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
"@ | Out-File -Append .env
```

**Step 3: Start Celery Worker**
```powershell
# Terminal 1: Start Celery worker
celery -A src.workers.celery_app worker --loglevel=info --pool=solo -Q videos,batch

# Terminal 2: Start Celery beat (scheduler - optional)
celery -A src.workers.celery_app beat --loglevel=info

# Terminal 3: Start Streamlit app
streamlit run app.py
```

**For Production**: Use Celery as a Windows Service or systemd service

### 4. Enable SSL Verification (Production Security) **[SECURITY]**

Before deploying to production, SSL verification MUST be enabled:

```powershell
# Update .env
@"
WALMART_SSL_VERIFY=true
"@ | Out-File -Append .env

# If using custom CA bundle (corporate certificates)
# WALMART_CA_BUNDLE=C:\path\to\walmart-ca-bundle.crt
```

**To obtain CA bundle**:
1. Contact Walmart InfoSec team
2. Request: "Internal CA Certificate Bundle for API Access"
3. Save to secure location
4. Update `WALMART_CA_BUNDLE` path in `.env`

### 5. Obtain/Refresh Walmart SSO Token **[ALREADY CONFIGURED]**

Authentication token for Walmart Media Studio API:

**Current Status**: ✅ Token configured (check `.env` for `WALMART_SSO_TOKEN`)

**If expired or missing**:
1. Go to https://retina-ds-genai-backend.prod.k8s.walmart.net
2. Log in with Walmart credentials
3. Open browser DevTools (F12)
4. Go to Network tab
5. Make any API request
6. Copy the `Authorization` header value
7. Update `.env`:
   ```
   WALMART_SSO_TOKEN=your-token-here
   ```

**Note**: Token expires periodically. Contact #help-genai-media-studio for service account setup.

### 6. Install FFmpeg **[FEATURE COMPLETION]**

Required for video thumbnail extraction and watermarking:

**Status**: ✅ AI Watermark feature implemented, FFmpeg installation pending

**Option A: Manual Download (IF IT SUPPORT DELAYED)**
1. Go to https://www.gyan.dev/ffmpeg/builds/
2. Download "ffmpeg-release-essentials.zip"
3. Extract to `C:\ffmpeg`
4. Add `C:\ffmpeg\bin` to System PATH
5. Verify: `ffmpeg -version`

**Option B: Request IT Installation (RECOMMENDED)**
1. Open ServiceNow ticket
2. Request: "FFmpeg Installation for Video Processing"
3. Business justification: "Required for Zorro video platform thumbnail generation"
4. Wait for approval and installation

**Option C: Chocolatey (If Available)**
```powershell
choco install ffmpeg
```

---

## 🟡 HIGH PRIORITY - Improves Quality & Readiness

### 7. Configure GitHub Repository Secrets (CI/CD)

1. Go to https://mediagenai.walmart.com/
2. Log in with your Walmart credentials
3. Open browser DevTools (F12)
4. Go to Network tab
5. Find any API request
6. Copy the `Authorization` header value
7. Add to `.env`:
   ```
   WALMART_SSO_TOKEN=your-token-here
   ```

**Note:** Token expires. Contact #help-genai-media-studio for service account setup.

### 4. Enable SSL Verification (Production)

Before deploying to production:

```powershell
# Option A: Use system certificates
$env:WALMART_SSL_VERIFY = "true"

# Option B: Use custom CA bundle (if needed)
$env:WALMART_SSL_VERIFY = "true"
$env:WALMART_CA_BUNDLE = "C:\path\to\walmart-ca-bundle.crt"
```

Add to `.env`:
```
WALMART_SSL_VERIFY=true
# WALMART_CA_BUNDLE=/path/to/walmart-ca-bundle.crt
```

### 5. Install FFmpeg

Required for video thumbnail extraction:

**Option A: Manual Download**
1. Go to https://www.gyan.dev/ffmpeg/builds/
2. Download "ffmpeg-release-essentials.zip"
3. Extract to `C:\ffmpeg`
4. Add `C:\ffmpeg\bin` to PATH

**Option B: Request IT Installation**
1. Open ServiceNow ticket
2. Request FFmpeg installation
3. Wait for approval and installation

### 6. Configure GitHub Repository Secrets

For CI/CD pipeline to work:

1. Go to your GitHub repository settings
2. Navigate to Secrets and Variables > Actions
3. Add these secrets:
   - `WALMART_SSO_TOKEN` - Your SSO token for testing
   - `DATABASE_URL` - Test database connection string

### 7. Set Up Celery for Async Processing (Phase 2)

Video generation blocks for 5+ minutes. For production:

```powershell
# Install Redis (Docker)
docker run -d --name zorro-redis -p 6379:6379 redis:7-alpine

# Install Celery
pip install celery[redis]

# Add to .env
echo "CELERY_BROKER_URL=redis://localhost:6379/0" >> .env
echo "CELERY_RESULT_BACKEND=redis://localhost:6379/0" >> .env
```

**Implementation required:** Create `src/workers/celery_app.py` and refactor pipeline.

---

## 🟡 RECOMMENDED - Improves Quality

### 8. Run Linting and Fix Issues

```powershell
pip install ruff black isort
black src/ tests/ --check
isort src/ tests/ --check
ruff check src/ tests/
```

Fix any issues reported.

### 9. Add Type Hints and Run mypy

```powershell
pip install mypy
mypy src/ --ignore-missing-imports
```

### 10. Increase Test Coverage

Current coverage is low. Add tests for:
- `src/services/design_studio_service.py`
- `src/services/character_prompt_builder.py`
- `src/providers/walmart_media_studio.py`

```powershell
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html to see coverage report
```

---

## 📋 Checklist

| Item | Priority | Status | Owner |
|------|----------|--------|-------|
| Install pydantic-settings | Critical | ✅ Done | Automated |
| PostgreSQL setup | Critical | ⬜ Pending | You |
| SSO token | Critical | ⬜ Pending | You |
| SSL verification | Critical | ⬜ Pending | You |
| FFmpeg installation | High | ⬜ Pending | You |
| GitHub secrets | High | ⬜ Pending | You |
| Celery setup | Medium | ⬜ Pending | Phase 2 |
| Linting fixes | Medium | ✅ Done | Automated |
| Type hints | Low | ⬜ Pending | You |
| Test coverage | Medium | ✅ Partial (65/77 pass) | Automated |

---

## ✅ What Has Been Done (Automated)

1. ✅ **Structured logging with correlation IDs** - `src/utils/logger.py`
2. ✅ **Circuit breaker for API resilience** - `src/providers/walmart_media_studio.py`
3. ✅ **Centralized settings module** - `src/utils/settings.py`
4. ✅ **CI/CD pipeline** - `.github/workflows/ci.yml`
5. ✅ **Dockerfile** - Multi-stage production build
6. ✅ **docker-compose.yml** - Local development setup
7. ✅ **Input validation** - `src/services/design_studio_service.py`
8. ✅ **SSL configuration** - Now configurable via environment variables
9. ✅ **Updated requirements.txt** - Added pydantic-settings
10. ✅ **Installed pydantic-settings** - Package verified working
11. ✅ **Installed linting tools** - ruff, black, isort, mypy, bandit
12. ✅ **Fixed import ordering** - isort applied to 30+ files
13. ✅ **Security scan passed** - No medium/high severity issues
14. ✅ **Unit tests running** - 65/77 tests passing
15. ✅ **Package installed in editable mode** - For development

---

## 🚀 Quick Start After Completing Actions

```powershell
# 1. Install new dependencies
pip install -r requirements.txt

# 2. Verify settings work
python -c "from src.utils.settings import settings; print(settings.model_dump())"

# 3. Run tests
pytest tests/unit/ -v

# 4. Start application
streamlit run app.py
```

---

*Last Updated: December 5, 2024*
