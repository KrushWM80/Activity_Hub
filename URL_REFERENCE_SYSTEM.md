# Activity Hub - Complete URL Reference System
**Last Updated:** May 1, 2026  
**Machine:** WEUS42608431466 | IP: 10.97.114.181

---

## 📋 Master URL Reference

### TDA Insights - Port 5000

| Environment | URL | Use Case | Type |
|-------------|-----|----------|------|
| **Local (Development)** | `http://localhost:5000/tda-initiatives-insights` | Dev/Testing | Frontend |
| **IP (Internal Network)** | `http://10.97.114.181:5000/tda-initiatives-insights` | Team access via IP | Frontend |
| **Hostname (Production)** | `http://weus42608431466:5000/tda-initiatives-insights` | Standard production | Frontend |
| **Backend API** | `http://localhost:5000/api/*` | Data endpoints | Backend |
| **Backend Health** | `http://localhost:5000/health` | Service status check | Backend |

**Backend Server**: Flask (`backend_simple.py`)  
**Routes**: `/`, `/dashboard.html`, `/tda-initiatives-insights`  
**Active Route**: `/tda-initiatives-insights` (primary)

---

### VET Dashboard - Port 5001

| Environment | URL | Use Case | Type |
|-------------|-----|----------|------|
| **Local (Development)** | `http://localhost:5001/Dallas_Team_Report` | Dev/Testing | Frontend |
| **IP (Internal Network)** | `http://10.97.114.181:5001/Dallas_Team_Report` | Team access via IP | Frontend |
| **Hostname (Production)** | `http://weus42608431466:5001/Dallas_Team_Report` | Standard production | Frontend |
| **Backend API** | `http://localhost:5001/api/*` | Data endpoints | Backend |
| **Backend Health** | `http://localhost:5001/health` | Service status check | Backend |

**Backend Server**: Flask (`backend.py`)  
**Primary Route**: `/Dallas_Team_Report`  
**Redirect**: Root `/` redirects to `/Dallas_Team_Report`

---

### Projects in Stores - Port 8001

| Environment | URL | Use Case | Type |
|-------------|-----|----------|------|
| **Development** | `http://localhost:8002/` | Local dev | Frontend |
| **IP (Internal Network)** | `http://10.97.114.181:8001/` | Team access via IP | Frontend |
| **FQDN (Production)** | `http://weus42608431466.homeoffice.wal-mart.com:8001/` | Standard production | Frontend |
| **Backend API** | `http://weus42608431466.homeoffice.wal-mart.com:8001/api/*` | Data endpoints | Backend |
| **Cache Status** | `http://weus42608431466.homeoffice.wal-mart.com:8001/api/cache/usage` | Cache diagnostic | Backend |

**Backend Server**: FastAPI/Uvicorn (`main.py`)  
**Primary Route**: `/index.html` (or root `/`)  
**Note**: Uses fully qualified domain name (FQDN) with `.homeoffice.wal-mart.com` suffix for production

---

### Job Codes Teaming Dashboard - Port 8080

| Environment | URL | Use Case | Type |
|-------------|-----|----------|------|
| **Local (Development)** | `http://localhost:8080/Aligned#` | Dev/Testing | Frontend |
| **IP (Internal Network)** | `http://10.97.114.181:8080/Aligned#` | Team access via IP | Frontend |
| **Hostname (Production)** | `http://weus42608431466:8080/Aligned#` | Standard production | Frontend |
| **Admin Panel** | `http://weus42608431466:8080/Aligned#admin` | Admin access | Frontend |
| **Admin with ID** | `http://weus42608431466:8080/Aligned#admin/{request_id}` | Review request | Frontend |
| **Backend API** | `http://localhost:8080/api/*` | Data endpoints | Backend |

**Backend Server**: FastAPI (`main.py`)  
**Primary Route**: `/Aligned#` (SPA hash routing)  
**Admin Route**: `/Aligned#admin` and `/Aligned#admin/{id}`

---

### AMP Store Dashboard (Store Updates) - Port 8081

| Environment | URL | Use Case | Type |
|-------------|-----|----------|------|
| **Local (Development)** | `http://localhost:8081/` | Dev/Testing | Frontend |
| **IP (Internal Network)** | `http://10.97.114.181:8081/` | Team access via IP | Frontend |
| **Hostname (Production)** | `http://weus42608431466:8081/StoreActivityandCommunications` | Standard production | Frontend |
| **Backend API** | `http://localhost:8081/api/amp-data` | Data endpoints | Backend |
| **Health Check** | `http://localhost:8081/health` | Service status | Backend |

**Backend Server**: Flask (`amp_backend_server.py`)  
**Primary Route**: `/StoreActivityandCommunications`  
**Fallback**: Root `/` shows API documentation if `index.html` not found

---

### Activity Hub - Port 8088

| Environment | URL | Use Case | Type |
|-------------|-----|----------|------|
| **Local (Development)** | `http://localhost:8088/activity-hub/` | Dev/Testing | Frontend |
| **IP (Internal Network)** | `http://10.97.114.181:8088/activity-hub/` | Team access via IP | Frontend |
| **Hostname (Production)** | `http://weus42608431466:8088/activity-hub/for-you` | Standard production | Frontend |
| **Landing Page** | `http://weus42608431466:8088/activity-hub/for-you` | Main entry point | Frontend |
| **Backend API** | `http://localhost:8088/api/*` | Data endpoints | Backend |

**Frontend**: React SPA (`activity-hub/`)  
**Primary Route**: `/for-you` (landing page)

---

### Store Meeting Planner - Port 8090

| Environment | URL | Use Case | Type |
|-------------|-----|----------|------|
| **Local (Development)** | `http://localhost:8090/StoreMeetingPlanner` | Dev/Testing | Frontend |
| **IP (Internal Network)** | `http://10.97.114.181:8090/StoreMeetingPlanner` | Team access via IP | Frontend |
| **Hostname (Production)** | `http://weus42608431466:8090/StoreMeetingPlanner` | Standard production | Frontend |
| **Backend API** | `http://localhost:8090/api/*` | Data endpoints | Backend |

**Backend Server**: FastAPI (`main.py`)  
**Primary Route**: `/StoreMeetingPlanner`

---

### Zorro Audio Message Hub - Port 8888

| Environment | URL | Use Case | Type |
|-------------|-----|----------|------|
| **Local (Development)** | `http://localhost:8888/Zorro/AudioMessageHub` | Dev/Testing | Frontend |
| **IP (Internal Network)** | `http://10.97.114.181:8888/Zorro/AudioMessageHub` | Team access via IP | Frontend |
| **Hostname (Production)** | `http://weus42608431466:8888/Zorro/AudioMessageHub` | Standard production | Frontend |
| **Audio Download** | `http://weus42608431466:8888/Zorro/AudioMessageHub/audio/{filename}` | Get audio file | Backend |
| **Metadata** | `http://weus42608431466:8888/Zorro/AudioMessageHub/metadata/{json}` | Get metadata | Backend |
| **Test Audio** | `http://weus42608431466:8888/api/test-audio` | Test endpoint | Backend |

**Backend Server**: HTTP Server (`audio_server.py`)  
**Primary Route**: `/Zorro/AudioMessageHub` (strips prefix for routing)

---

## 🔄 Environment Definitions

### Local (Development)
- **Access**: `localhost` or `127.0.0.1`
- **Use**: Development, testing, debugging
- **Access From**: Your machine only
- **Backend Testing**: Use these URLs directly
- **Frontend Development**: HTML/JS debugging

### IP (Internal Network)  
- **Access**: `10.97.114.181` (DHCP, changes on reboot)
- **Use**: Team testing from other machines
- **Access From**: Anyone on Walmart Eagle WiFi network
- **Stability**: Not recommended for production (DHCP changes)
- **Use Case**: Quick internal testing

### Hostname (Production/Standard)
- **Access**: `weus42608431466` or `weus42608431466.homeoffice.wal-mart.com`
- **Use**: Standard production access
- **Access From**: Team members, automated scripts, browsers
- **Stability**: Stable via AD DNS
- **Recommendation**: Use this for all production URLs

---

## 📌 Quick Reference - What URLs to Use

### If You're...
- **Developing locally**: Use `localhost:PORT/route`
- **Testing from another machine**: Use `http://weus42608431466:PORT/route`
- **In automated scripts/emails**: Use `http://weus42608431466:PORT/route`
- **For Projects in Stores only**: Use `http://weus42608431466.homeoffice.wal-mart.com:8001`
- **Sharing with team**: Use hostname URLs (not localhost or IP)

---

## 🔐 URL Resolution Map

| What User Enters | Resolves To | Via | Reliability |
|------------------|-------------|-----|-------------|
| `localhost` | 127.0.0.1 | Localhost | Only on this machine |
| `10.97.114.181` | DHCP IP | Network | Changes on reboot ⚠️ |
| `weus42608431466` | 10.97.114.181 | AD DNS (Corp) | Stable on corp network ✅ |
| `weus42608431466.homeoffice.wal-mart.com` | 10.97.114.181 | AD DNS (FQDN) | Stable, standard format ✅ |

---

## 🛠️ Backend vs Frontend

### Backend Endpoints (Testing/Debugging)
- TDA Insights: `http://localhost:5000/api/initiatives`, `http://localhost:5000/api/data`
- VET Dashboard: `http://localhost:5001/api/filter_data`, `http://localhost:5001/api/rankings`
- AMP Dashboard: `http://localhost:8081/api/amp-data`, `http://localhost:8081/api/amp-metrics`
- Zorro: `http://localhost:8888/api/test-audio`, `http://localhost:8888/api/generate-audio`

### Frontend Entry Points (User Facing)
- TDA Insights: `http://weus42608431466:5000/tda-initiatives-insights` ✅
- VET Dashboard: `http://weus42608431466:5001/Dallas_Team_Report` ✅
- Projects in Stores: `http://weus42608431466.homeoffice.wal-mart.com:8001/` ✅
- Job Codes: `http://weus42608431466:8080/Aligned#` ✅
- AMP Dashboard: `http://weus42608431466:8081/StoreActivityandCommunications` ✅
- Activity Hub: `http://weus42608431466:8088/activity-hub/for-you` ✅
- Meeting Planner: `http://weus42608431466:8090/StoreMeetingPlanner` ✅
- Zorro: `http://weus42608431466:8888/Zorro/AudioMessageHub` ✅

---

## 🔗 URL Pattern by Service Type

### Pattern 1: Simple Root Route
```
Ports: 8001 (Projects)
Format: http://weus42608431466:PORT/
```

### Pattern 2: Named Route (No Hash)
```
Ports: 5000 (TDA), 5001 (VET), 8081 (AMP), 8090 (Meeting), 8888 (Zorro)
Format: http://weus42608431466:PORT/NamedRoute
Examples:
  - /tda-initiatives-insights
  - /Dallas_Team_Report
  - /StoreActivityandCommunications
  - /StoreMeetingPlanner
  - /Zorro/AudioMessageHub
```

### Pattern 3: Hash-Based SPA
```
Ports: 8080 (Job Codes)
Format: http://weus42608431466:PORT/route#hash
Examples:
  - /Aligned#
  - /Aligned#admin
  - /Aligned#admin/request_id
```

### Pattern 4: FQDN Required
```
Ports: 8001 (Projects - Dev exception)
Format: http://weus42608431466.homeoffice.wal-mart.com:PORT/
Reason: API uses window.location.origin for CORS/API calls
```

---

## ✅ Verification Checklist

Before deploying or sharing URLs:

- [ ] Is this URL for development (localhost) or production (hostname)?
- [ ] Does the route match what's defined in the backend?
- [ ] Have I tested this URL locally first?
- [ ] Is this URL being shared with team or used in automation?
- [ ] For Projects in Stores: Am I using FQDN (.homeoffice.wal-mart.com)?
- [ ] Does the backend support CORS for this frontend URL?