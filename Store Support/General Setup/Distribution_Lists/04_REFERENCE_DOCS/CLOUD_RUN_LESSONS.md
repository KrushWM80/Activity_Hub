# Cloud Run Deployment - Lessons Learned

**Based on**: Distribution List Lookup 404 Fix (December 2025)

---

## Key Learnings

### 1. Missing API Endpoints Require Redeployment

**Problem**: Adding new API endpoints (like `/api/distribution-lists`) to an existing Cloud Run service requires redeployment. The endpoint won't be available until the service is redeployed.

**Solution**: Always redeploy after adding/modifying endpoints:
```powershell
.\REDEPLOY.ps1
```

### 2. Deployment Time Expectations

- **First deployment**: 3-5 minutes (builds Docker image)
- **Subsequent deployments**: 30-60 seconds
- **Downtime**: ~30 seconds maximum (rolling update)

### 3. API Endpoint Best Practices

**Always include query parameters**:
- `search` or `q` - Search term
- `limit` - Max results (default 100, max 200)
- `offset` - Pagination offset
- `store`, `department` - Filtering options

**Always return metadata**:
```json
{
  "data": [...],
  "count": 50,
  "limit": 100,
  "offset": 0,
  "timestamp": "2025-12-17T10:30:00Z"
}
```

### 4. Health Check Endpoints Are Critical

Always include:
- `/health` - Simple health check
- `/status` - Detailed status with dependency checks (BigQuery, etc.)

**Example**:
```python
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/status')
def status_check():
    return jsonify({
        'status': 'operational',
        'bigquery': 'connected',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 200
```

### 5. Testing Deployment

**Always test these after deployment**:
```bash
# 1. Health check
curl https://your-api.run.app/health

# 2. Status check
curl https://your-api.run.app/status

# 3. Main endpoint with minimal data
curl 'https://your-api.run.app/api/your-endpoint?limit=1'
```

### 6. Browser Cache Issues

**Problem**: After redeployment, browsers may cache old 404 errors

**Solution**: Always hard refresh:
- **Windows**: Ctrl + Shift + R
- **Mac**: Cmd + Shift + R
- **Or**: Open DevTools (F12) and right-click refresh → "Empty Cache and Hard Reload"

### 7. Troubleshooting Steps

When API returns 404:
1. Check Cloud Run deployment status
2. View Cloud Run logs: `gcloud run services logs read your-api --limit 50`
3. Test endpoint directly with curl
4. Check browser console (F12) for network errors
5. Verify API URL in frontend matches deployed service URL
6. Hard refresh browser

### 8. Rollback Strategy

Always keep previous revisions available:
```bash
# List revisions
gcloud run revisions list --service your-api

# Rollback if needed
gcloud run deploy your-api \
  --revision=<previous-revision-id> \
  --no-traffic-100 \
  --region us-central1
```

### 9. Deployment Scripts Are Essential

Create quick redeploy scripts for efficiency:

**REDEPLOY.ps1** (Windows):
```powershell
gcloud run deploy your-api `
  --source . `
  --region us-central1 `
  --allow-unauthenticated
```

**REDEPLOY.sh** (Linux/Mac):
```bash
gcloud run deploy your-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### 10. Documentation Should Include

- **API endpoint specifications** with parameters and examples
- **Redeployment procedures** (scripts and manual commands)
- **Testing commands** for verification
- **Troubleshooting steps** for common issues (especially 404)
- **Rollback procedures** for emergencies

---

## Common Pitfalls

### ❌ Don't:
- Forget to redeploy after changing endpoints
- Skip health check endpoints
- Ignore browser cache when testing
- Deploy without testing first
- Leave API URLs hardcoded in frontend

### ✅ Do:
- Always redeploy after API changes
- Include `/health` and `/status` endpoints
- Test with curl before browser testing
- Hard refresh browser after deployment
- Use environment variables for API URLs
- Create redeployment scripts
- Monitor Cloud Run logs

---

## Quick Reference Commands

```bash
# Deploy/Redeploy
gcloud run deploy your-api --source . --region us-central1 --allow-unauthenticated

# View logs
gcloud run services logs read your-api --limit 50
gcloud run services logs tail your-api

# List revisions
gcloud run revisions list --service your-api

# Check service status
gcloud run services describe your-api --region us-central1

# Test endpoints
curl https://your-api.run.app/health
curl https://your-api.run.app/status
curl 'https://your-api.run.app/api/endpoint?limit=1'
```

---

## Template Files Created

Based on this experience, create these standard files for all Cloud Run projects:

1. **REDEPLOY.ps1** - Windows redeployment script
2. **REDEPLOY.sh** - Linux/Mac redeployment script
3. **FIX_[ISSUE].md** - Document fixes for common issues
4. **API_SPECIFICATION.md** - Document all endpoints with examples
5. **TROUBLESHOOTING.md** - Common issues and solutions

---

**Last Updated**: December 17, 2025  
**Source**: Distribution List Lookup 404 Fix Experience
