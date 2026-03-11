# Projects in Stores - Project Structure

**Last Updated**: March 10, 2026  
**Project Status**: ✅ ACTIVE

---

## 📋 Quick Navigation

### 🎯 **Starting Points**

- **First time here?** → Read [QUICK_START_USERS.md](QUICK_START_USERS.md)
- **Need to understand cache?** → Go to [docs/CACHE/](docs/CACHE/)
- **Building/deploying?** → See [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)
- **Admin operations?** → Check [docs/Admin_Guide.md](docs/Admin_Guide.md)

---

## 📁 Folder Structure

### **Root Level** (What You Need to Know)
Files in the main folder are directional - start here to understand the project.

| File | Purpose |
|------|---------|
| [QUICK_START_USERS.md](QUICK_START_USERS.md) | 5-minute user guide |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick lookup reference |
| [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md) | System overview & what was built |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | This file - navigation guide |

### **docs/** (Detailed Documentation)
Organized by topic for deeper understanding.

| Folder | Contents |
|--------|----------|
| **docs/CACHE/** | Cache sync & validation system [→ View](docs/CACHE/) |
| **docs/** | Admin guides, caching options, etc. |

### **frontend/** (User Interface)
Static HTML dashboard and admin portal.

```
frontend/
├── admin.html          # Admin dashboard
│   └── Features: Login tracking, user activity, data sync status
└── index.html         # User interface
```

### **backend/** (Server & Data)
FastAPI server with SQLite cache and BigQuery sync.

```
backend/
├── main.py                    # FastAPI application
├── sqlite_cache.py            # ⭐ Cache validation & sync logic
├── monitor_cache_health.py    # Health check tool
├── projects_cache.db          # SQLite cache database
└── requirements.txt           # Python dependencies
```

---

## 🔄 Cache System (Most Important!)

**Location**: [docs/CACHE/](docs/CACHE/)

Three levels of documentation:
1. **[01_SMART_PARAMETERS.md](docs/CACHE/01_SMART_PARAMETERS.md)** - When to expect alerts
2. **[02_IMPLEMENTATION_GUIDE.md](docs/CACHE/02_IMPLEMENTATION_GUIDE.md)** - How it works
3. **[03_KNOWLEDGE_BASE.md](docs/CACHE/03_KNOWLEDGE_BASE.md)** - Complete reference

**Quick Fact**: Cache system validates data before updating using smart parameters:
- ✅ ±50k variance is normal (no email)
- ✅ 0 records retried 2x (gives sync time)
- ✅ Bad data never overwrites old cache

---

## 🚀 Key Features

### ✅ **Backend Server** (port 8001)
- FastAPI REST API
- SQLite cache (queries in milliseconds)
- BigQuery sync (every 15 minutes)
- **Start with**: `python main.py`

### ✅ **Admin Dashboard**
- Login tracking (see every unique user)
- User activity monitoring
- Cache health status
- **Access at**: `http://localhost:8001/admin.html`

### ✅ **User Dashboard**
- Project search & filtering
- Real-time data from cache
- Status indicators
- **Access at**: `http://localhost:8001/`

### ✅ **Smart Cache Validation**
- Automatically retries failed syncs
- Prevents bad data from corrupting cache
- Sends intelligent email alerts
- Dashboard never goes down
- **Details**: [docs/CACHE/](docs/CACHE/)

---

## 🔧 Common Tasks

### Check Cache Health
```powershell
cd backend
python monitor_cache_health.py
```

Shows: Record count, sync history, health status, recommendations.

### Restart Backend Server
```powershell
cd backend
python main.py
```

### Run for 24/7 (Production)
```powershell
# Windows batch file with auto-restart
.\start_server_24_7.bat

# Or create task scheduler job (requires admin)
# See: docs/Admin_Guide.md
```

### Check Sync Details
```powershell
cd backend

# Monitor live sync
python monitor_cache_health.py

# View debug logs
# Edit sqlite_cache.py to adjust logging
```

---

## 📊 Data Flow

```
BigQuery (1.4M records)
         ↓ [Every 15 min]
[Validation] ← Smart parameters check:
         ├─ ✓ Variance within ±50k?
         ├─ ✓ 0 records (retry)?
         └─ ✓ Sync > 60 seconds?
         ↓
SQLite Cache [Rollback if invalid]
         ↓
Dashboard ← Always serves good data
```

---

## 🔐 Security & Operations

### Admin Access
- **Username**: `krush`
- **Password**: `Admin2026` (change in production)
- **Location**: `http://localhost:8001/admin.html`

### Data Protection
- ✅ Cache locked behind transaction (rollback on failure)
- ✅ Email alerts for real issues only (not false positives)
- ✅ Last good data served during problems
- ✅ Complete audit trail in `sync_error_log` table

### Monitoring
- **Health check**: `python monitor_cache_health.py`
- **Email alerts**: kendall.rush@walmart.com (configured in `sqlite_cache.py`)
- **Log file**: Check outputs in console

---

## 📖 Documentation Map

**For Users**:
1. Start → [QUICK_START_USERS.md](QUICK_START_USERS.md)
2. Reference → [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
3. Questions → Check file below

**For Admins**:
1. Setup → [docs/Admin_Guide.md](docs/Admin_Guide.md)
2. Cache → [docs/CACHE/README.md](docs/CACHE/README.md)
3. 24/7 → [docs/Admin_Guide.md](docs/Admin_Guide.md#24-7-operation)

**For Developers**:
1. Overview → [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)
2. Cache Details → [docs/CACHE/02_IMPLEMENTATION_GUIDE.md](docs/CACHE/02_IMPLEMENTATION_GUIDE.md)
3. Complete Ref → [docs/CACHE/03_KNOWLEDGE_BASE.md](docs/CACHE/03_KNOWLEDGE_BASE.md)

---

## 🆘 Common Questions

**"Website not loading?"**
→ Check if server is running: `netstat -ano | Select-String ":8001"`  
→ Start server: `cd backend && python main.py`

**"Seeing old data?"**
→ Cache might be mid-sync. Check: `python monitor_cache_health.py`  
→ Data refreshes every 15 minutes automatically.

**"Got an email about cache failure?"**
→ Check [docs/CACHE/01_SMART_PARAMETERS.md](docs/CACHE/01_SMART_PARAMETERS.md#expected-behavior)  
→ Not always a problem. Could be normal retry during sync.

**"Want to adjust cache settings?"**
→ See [docs/CACHE/02_IMPLEMENTATION_GUIDE.md](docs/CACHE/02_IMPLEMENTATION_GUIDE.md#configuration)

---

## 📋 File Checklist

Main level files should be minimal & directional:
- ✅ [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Navigation
- ✅ [QUICK_START_USERS.md](QUICK_START_USERS.md) - Getting started
- ✅ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick lookup
- ✅ [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md) - Overview
- ✓ Archived old drafts in `_archived/`

Detailed docs in `docs/`:
- ✅ [docs/CACHE/README.md](docs/CACHE/README.md) - Cache navigation
- ✅ [docs/CACHE/01_SMART_PARAMETERS.md](docs/CACHE/01_SMART_PARAMETERS.md) - For everyone
- ✅ [docs/CACHE/02_IMPLEMENTATION_GUIDE.md](docs/CACHE/02_IMPLEMENTATION_GUIDE.md) - For developers
- ✅ [docs/CACHE/03_KNOWLEDGE_BASE.md](docs/CACHE/03_KNOWLEDGE_BASE.md) - Complete reference
- ✅ [docs/Admin_Guide.md](docs/Admin_Guide.md) - Admin operations

---

## 🎯 Next Steps

1. **User?** → [QUICK_START_USERS.md](QUICK_START_USERS.md)
2. **Admin?** → [docs/Admin_Guide.md](docs/Admin_Guide.md)
3. **Developer?** → [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)
4. **Cache questions?** → [docs/CACHE/README.md](docs/CACHE/README.md)
