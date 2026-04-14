# Impact Platform Frontend - Deployment Guide

## Location
**Network URL**: `http://weus42608431466:8088/activity-hub/projects`

## Files
- `index.html` - Main dashboard page
- `app.js` - API client and event handlers

## Deployment Steps

### 1. Connect to Network Server
```powershell
# Access the web server on weus42608431466
# Typically hosted in C:\inetpub\wwwroot or similar web root
```

### 2. Copy Files to Web Server
Copy both files to the web root at:
- `\\weus42608431466\wwwroot\activity-hub\projects\`
- OR the equivalent path for your web server deployment

### 3. Verify Backend Connectivity
The frontend expects the backend FastAPI service at:
```
http://weus42608431466:8002/api/impact
```

## Configuration Notes

### API Endpoint
In `app.js` (Line 2), the API is configured as:
```javascript
const API_BASE = "http://weus42608431466:8002/api/impact";
```

### Supported API Endpoints
- `GET /projects` - Fetch all projects with optional filters
- `GET /metrics` - Fetch dashboard metrics
- `POST /projects` - Create new project
- `POST /generate-ppt` - Generate PPT report

## Features

✅ **Dashboard Metrics**
- Active Projects count
- Unique Owners count
- Projects Updated This Week count
- Percent Updated percentage

✅ **Project Filtering**
- By Business Area
- By Health Status (Green/Yellow/Red)
- By Project Status (Active/Inactive)

✅ **Project Management**
- View all projects in table format
- Add new project via modal form
- Edit functionality (coming soon)
- Generate PPT report

✅ **Responsive Design**
- Bootstrap 5 framework
- Mobile-friendly layouts
- Walmart branding colors
- Smooth animations and transitions

## Testing Access

Once deployed, verify access at:
```
http://weus42608431466:8088/activity-hub/projects
```

## Troubleshooting

### Projects Not Loading
1. Check backend service is running on port 8002
2. Verify CORS is enabled on backend
3. Check browser console for errors (F12)
4. Verify BigQuery credentials are accessible on backend

### API Errors
- **CORS Error**: Backend CORS configuration needs to allow requests from the web server
- **Connection Refused**: Verify backend service is running
- **Empty Projects List**: Check if test data exists in BigQuery

## Backend Status
- **Service**: FastAPI (Python)
- **Port**: 8002
- **Status**: Running on http://weus42608431466:8002
- **Database**: BigQuery (`wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`)
