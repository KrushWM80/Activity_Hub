# Google Cloud Run - Deployment Guide

## Overview

Google Cloud Run is a fully managed serverless platform for deploying containerized applications. Perfect for deploying backend APIs that integrate with Code Puppy Pages.

**Key Features**:
- **Automatic Scaling** - Scales to zero when not in use
- **Pay-per-Use** - Only charged when requests are running
- **Container-Based** - Automatically builds from source code
- **Fast Deployment** - 30-60 seconds for updates
- **HTTPS Built-in** - Automatic SSL certificates
- **Integration** - Works seamlessly with BigQuery, Cloud Storage, etc.

---

## 🚀 Quick Deploy

### Prerequisites

```bash
# Install Google Cloud SDK
# Windows: https://cloud.google.com/sdk/docs/install
# Mac: brew install google-cloud-sdk

# Authenticate
gcloud auth login

# Set project
gcloud config set project your-project-id
```

### Deploy from Source

```bash
# Navigate to your API directory
cd api/

# Deploy (builds container automatically)
gcloud run deploy your-api-name \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

# Note the service URL:
# https://your-api-name-xxxxx.us-central1.run.app
```

**That's it!** Cloud Run builds the container and deploys automatically.

---

## 📁 Project Structure

### Python/Flask API

```
api/
├── main.py              # Your Flask app
├── requirements.txt     # Python dependencies
└── .gcloudignore       # Files to exclude (optional)
```

**main.py**:
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/endpoint', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from Cloud Run'}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Cloud Run sets PORT environment variable
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
```

**requirements.txt**:
```
flask>=2.3.0
google-cloud-bigquery>=3.11.0
```

### Node.js/Express API

```
api/
├── server.js           # Your Express app
├── package.json        # Dependencies
└── .gcloudignore      # Files to exclude (optional)
```

**server.js**:
```javascript
const express = require('express');
const app = express();

app.get('/api/endpoint', (req, res) => {
    res.json({ message: 'Hello from Cloud Run' });
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

---

## 🔄 Redeployment Scripts

### PowerShell (Windows)

**REDEPLOY.ps1**:
```powershell
# REDEPLOY.ps1 - Quick redeploy to Cloud Run

Write-Host "Deploying to Cloud Run..." -ForegroundColor Cyan

cd api

gcloud run deploy your-api-name `
  --source . `
  --region us-central1 `
  --allow-unauthenticated

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nDeployment successful!" -ForegroundColor Green
    Write-Host "API URL: https://your-api-name-xxxxx.us-central1.run.app" -ForegroundColor Yellow
    Write-Host "Test: curl https://your-api-name-xxxxx.us-central1.run.app/health" -ForegroundColor Cyan
} else {
    Write-Host "`nDeployment failed!" -ForegroundColor Red
    exit 1
}
```

**Usage**:
```powershell
.\REDEPLOY.ps1
```

### Bash (Linux/Mac)

**REDEPLOY.sh**:
```bash
#!/bin/bash
# REDEPLOY.sh - Quick redeploy to Cloud Run

echo "Deploying to Cloud Run..."

cd api

gcloud run deploy your-api-name \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

if [ $? -eq 0 ]; then
    echo ""
    echo "Deployment successful!"
    echo "API URL: https://your-api-name-xxxxx.us-central1.run.app"
    echo "Test: curl https://your-api-name-xxxxx.us-central1.run.app/health"
else
    echo ""
    echo "Deployment failed!"
    exit 1
fi
```

**Usage**:
```bash
chmod +x REDEPLOY.sh
./REDEPLOY.sh
```

---

## 🧪 Testing Deployment

### Test Endpoints

```bash
# Health check
curl https://your-api-name-xxxxx.us-central1.run.app/health

# Status check (if implemented)
curl https://your-api-name-xxxxx.us-central1.run.app/status

# Main API endpoint
curl 'https://your-api-name-xxxxx.us-central1.run.app/api/endpoint?limit=5'
```

### Local Testing Before Deploy

```bash
# Python/Flask
cd api
python main.py
# Test: http://localhost:8080

# Node.js/Express
cd api
npm install
node server.js
# Test: http://localhost:8080
```

---

## 📊 Monitoring & Logs

### View Logs

```bash
# Recent logs
gcloud run services logs read your-api-name --limit 50

# Follow logs in real-time
gcloud run services logs tail your-api-name

# Filter by severity
gcloud run services logs read your-api-name --filter="severity>=ERROR"
```

### Service Status

```bash
# Describe service
gcloud run services describe your-api-name --region us-central1

# List all services
gcloud run services list

# List revisions
gcloud run revisions list --service your-api-name
```

---

## 🔐 Authentication & Permissions

### Allow Unauthenticated Access

For APIs consumed by Code Puppy (internal only):
```bash
gcloud run deploy your-api-name \
  --allow-unauthenticated
```

### Require Authentication

For restricted APIs:
```bash
gcloud run deploy your-api-name \
  --no-allow-unauthenticated
```

### BigQuery Access

Grant Cloud Run service account BigQuery access:
```bash
# Get service account email
gcloud run services describe your-api-name --region us-central1 --format="value(spec.template.spec.serviceAccountName)"

# Grant BigQuery access
gcloud projects add-iam-policy-binding your-project-id \
  --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
  --role="roles/bigquery.dataViewer"
```

---

## 🔄 Rollback & Revisions

### List Revisions

```bash
gcloud run revisions list --service your-api-name
```

### Rollback to Previous Revision

```bash
# Route 100% traffic to specific revision
gcloud run services update-traffic your-api-name \
  --to-revisions=REVISION_NAME=100 \
  --region us-central1
```

### Delete Old Revisions

```bash
gcloud run revisions delete REVISION_NAME --region us-central1
```

---

## ⚙️ Configuration Options

### Environment Variables

```bash
gcloud run deploy your-api-name \
  --set-env-vars="DATABASE_URL=xxx,API_KEY=yyy"
```

### Memory & CPU

```bash
gcloud run deploy your-api-name \
  --memory=512Mi \
  --cpu=1
```

### Timeout & Concurrency

```bash
gcloud run deploy your-api-name \
  --timeout=300 \
  --concurrency=80
```

### Max Instances (Cost Control)

```bash
gcloud run deploy your-api-name \
  --max-instances=10
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "404 Not Found" on API Endpoint**
- Redeploy the service: `.\REDEPLOY.ps1`
- Check endpoint exists in code
- Test with curl directly
- Hard refresh browser (Ctrl+Shift+R)

**2. "Permission Denied" Error**
- Run: `gcloud auth login`
- Set project: `gcloud config set project your-project-id`
- Check IAM permissions

**3. "Build Failed" Error**
- Check `requirements.txt` or `package.json` syntax
- Review build logs: `gcloud builds log BUILD_ID`
- Test locally first

**4. "Container Failed to Start"**
- Check logs: `gcloud run services logs read your-api-name --limit 50`
- Verify PORT environment variable is used
- Ensure app binds to `0.0.0.0` not `localhost`

**5. "Service Takes Too Long to Respond"**
- Increase timeout: `--timeout=300`
- Check for cold start delays
- Optimize code/queries

### Debug Tips

```bash
# View recent logs
gcloud run services logs read your-api-name --limit 50

# Check service configuration
gcloud run services describe your-api-name --region us-central1

# Test locally with same container
gcloud run services proxy your-api-name --region us-central1
```

---

## 💰 Cost Optimization

### Pricing Model

- **CPU**: Only charged when processing requests
- **Memory**: Same as CPU
- **Requests**: First 2 million/month free
- **Compute Time**: First 180,000 vCPU-seconds free

### Cost Reduction Tips

1. **Scale to Zero**: Scales down when not in use (automatic)
2. **Set Max Instances**: `--max-instances=10` to limit costs
3. **Reduce Memory**: Use `--memory=256Mi` if possible
4. **Optimize Cold Starts**: Keep container small
5. **Cache Results**: Reduce BigQuery queries

---

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Test locally
- [ ] Add `/health` endpoint
- [ ] Add `/status` endpoint
- [ ] Include error handling
- [ ] Set PORT environment variable
- [ ] Bind to `0.0.0.0` not `localhost`

### Deployment
- [ ] Run `gcloud run deploy`
- [ ] Note service URL
- [ ] Test `/health` endpoint
- [ ] Test main API endpoints
- [ ] Check logs for errors

### Post-Deployment
- [ ] Update frontend API URL
- [ ] Hard refresh browser
- [ ] Monitor logs
- [ ] Test with real data
- [ ] Set up monitoring alerts (optional)

---

## 🎯 Best Practices

### API Design

1. **Always include health checks**:
   - `/health` - Simple status
   - `/status` - Detailed with dependencies

2. **Use query parameters**:
   - `limit` - Max results (default 100)
   - `offset` - Pagination
   - `search` or `q` - Search term

3. **Return metadata**:
   ```json
   {
     "data": [...],
     "count": 50,
     "limit": 100,
     "offset": 0,
     "timestamp": "2025-12-17T10:30:00Z"
   }
   ```

4. **Implement proper error handling**:
   ```python
   try:
       # Logic
   except Exception as e:
       return jsonify({'error': str(e)}), 500
   ```

### Security

- Use environment variables for secrets
- Don't commit API keys to Git
- Use service accounts for GCP resources
- Limit permissions (principle of least privilege)
- Validate all input

### Performance

- Cache frequently accessed data
- Use pagination for large datasets
- Optimize BigQuery queries
- Set appropriate memory/CPU limits
- Monitor cold start times

---

## 📚 Resources

- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **gcloud CLI Reference**: https://cloud.google.com/sdk/gcloud/reference/run
- **Pricing Calculator**: https://cloud.google.com/products/calculator

---

**Last Updated**: December 17, 2025  
**Version**: 1.0
