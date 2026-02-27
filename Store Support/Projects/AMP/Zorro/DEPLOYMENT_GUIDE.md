# Zorro Platform - Deployment Guide
## From Pilot to Production Scale

**Last Updated**: January 21, 2026  
**Target**: Phase 2 Deployment (February 2026)  
**Goal**: Scale from 5 → 100 videos/week

---

## Overview

This guide walks through deploying Zorro from development/pilot mode to production scale, capable of handling 50-100+ videos per week with multiple concurrent users.

### Architecture Evolution

**Phase 1 (Current - Pilot)**:
- SQLite/JSON file storage
- Synchronous video generation
- 1-5 videos/week, 2 users
- Single instance

**Phase 2 (Target - February 2026)**:
- PostgreSQL database
- Async video generation (Celery + Redis)
- 50-100 videos/week, 5-10 users
- Load balanced instances

---

## Prerequisites

### Required Access
- [ ] Walmart GitHub Enterprise account
- [ ] Azure/Cloud Services access (if cloud deployment)
- [ ] ServiceNow access (for IT requests)
- [ ] #help-genai-media-studio Slack channel

### Required Skills
- Basic Python knowledge
- Docker familiarity
- Database administration basics
- Command line proficiency

### Estimated Timeline
- **Quick Start (Local)**: 2 hours
- **Development Environment**: 1 day
- **Production Deployment**: 3-5 days

---

## Part 1: Local Development Setup (2 hours)

Perfect for testing before production deployment.

### Step 1: Install Dependencies (15 min)

```powershell
# Navigate to project
cd "c:\Users\hrisaac\OneDrive - Walmart Inc\Documents\VSCode\Projects\zorro"

# Update to latest dependencies
pip install -r requirements.txt

# Verify installation
python -c "import sqlalchemy, celery, redis; print('✓ All packages installed')"
```

### Step 2: Start Infrastructure Services (10 min)

```powershell
# Start PostgreSQL
docker run -d `
  --name zorro-postgres `
  --restart unless-stopped `
  -e POSTGRES_USER=zorro `
  -e POSTGRES_PASSWORD=zorro_dev_password `
  -e POSTGRES_DB=zorro `
  -p 5432:5432 `
  postgres:15-alpine

# Start Redis
docker run -d `
  --name zorro-redis `
  --restart unless-stopped `
  -p 6379:6379 `
  redis:7-alpine

# Verify services
docker ps
```

### Step 3: Configure Environment (10 min)

Create or update `.env`:

```dotenv
# Environment
ZORRO_ENV=development

# Database
DATABASE_URL=postgresql://zorro:zorro_dev_password@localhost:5432/zorro
SQL_ECHO=false
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Celery/Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Walmart Media Studio
WALMART_SSO_TOKEN=your_token_here
WALMART_MEDIA_STUDIO_API=https://retina-ds-genai-backend.prod.k8s.walmart.net
WALMART_SSL_VERIFY=false

# AI Watermark (Legal Requirement)
AI_WATERMARK_ENABLED=true
AI_WATERMARK_TEXT=AI Generated
AI_WATERMARK_POSITION=bottom_right

# OpenAI (Optional - for prompt enhancement)
OPENAI_API_KEY=your_key_here

# Logging
LOG_LEVEL=INFO
```

### Step 4: Initialize Database (5 min)

```powershell
# Run database initialization
python scripts/init_database.py

# Expected output:
# ✓ Connected to database: postgresql
# ✓ JSON backup created
# ✓ Migrations complete
# ✓ Indexes created
# ✓ Database operational
```

### Step 5: Start Services (5 min)

Open 3 terminal windows:

**Terminal 1: Celery Worker**
```powershell
celery -A src.workers.celery_app worker `
  --loglevel=info `
  --pool=solo `
  -Q videos,batch `
  --concurrency=2
```

**Terminal 2: Celery Beat (Optional - Scheduled Tasks)**
```powershell
celery -A src.workers.celery_app beat --loglevel=info
```

**Terminal 3: Streamlit App**
```powershell
streamlit run app.py
```

### Step 6: Verify Setup (5 min)

1. Open http://localhost:8501
2. Navigate to Design Studio
3. Create a test design element
4. Generate a video
5. Check Celery terminal for async processing logs

---

## Part 2: Production Deployment (3-5 days)

### Day 1: Infrastructure Provisioning

#### 1. Request PostgreSQL Database

**Via ServiceNow**:
1. Go to https://servicenow.walmart.com
2. Create new request: "Database Provisioning"
3. Details:
   - **Application**: Zorro Video Generation Platform
   - **Database Type**: PostgreSQL 15+
   - **Environment**: Production
   - **Size**: 50GB initial, 200GB max
   - **Backup**: Daily, 30-day retention
   - **Expected Load**: 50-100 transactions/day
   - **Business Justification**: Scale video content generation from 5 to 100+ videos/week

**Wait Time**: Typically 3-5 business days

#### 2. Request Redis Cache

**Via ServiceNow**:
1. Create request: "Redis Cache Provisioning"
2. Details:
   - **Purpose**: Message broker for async task queue
   - **Size**: 2GB RAM
   - **High Availability**: Yes (master-replica)
   - **Persistence**: RDB snapshots

**Alternative**: Use Azure Cache for Redis

#### 3. SSL Certificates

**Contact InfoSec**:
- Email: infosec@walmart.com
- Subject: "SSL Certificate Bundle for Internal API Access"
- Details: Need internal CA bundle for retina-ds-genai-backend.prod.k8s.walmart.net

### Day 2-3: Application Configuration

#### 1. Update Production .env

```dotenv
# Environment
ZORRO_ENV=production

# Database (from ServiceNow provisioning)
DATABASE_URL=postgresql://zorro_prod:SECURE_PASSWORD@prod-db.walmart.net:5432/zorro_prod
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40
SQL_ECHO=false

# Redis (from ServiceNow or Azure)
CELERY_BROKER_URL=redis://prod-redis.walmart.net:6379/0
CELERY_RESULT_BACKEND=redis://prod-redis.walmart.net:6379/0

# Walmart Media Studio
WALMART_SSO_TOKEN=<service_account_token>
WALMART_SSL_VERIFY=true
WALMART_CA_BUNDLE=/etc/ssl/certs/walmart-ca-bundle.crt

# Security
SECRET_KEY=<generate_secure_key>
ALLOWED_HOSTS=zorro.walmart.net

# Performance
MAX_CONCURRENT_GENERATIONS=5
CELERY_WORKER_CONCURRENCY=4

# Monitoring
SENTRY_DSN=<your_sentry_dsn>
LOG_LEVEL=WARNING
```

#### 2. Set Up Monitoring

**Recommended Tools**:
- **Application Monitoring**: Sentry or Walmart's APM
- **Infrastructure**: Prometheus + Grafana
- **Logging**: ELK Stack or Splunk

#### 3. Configure Secrets Management

**Azure Key Vault** (Recommended):
```powershell
# Store secrets in Key Vault
az keyvault secret set --vault-name zorro-vault --name database-url --value "postgresql://..."
az keyvault secret set --vault-name zorro-vault --name sso-token --value "..."

# Update app to read from Key Vault
# See: docs/azure-keyvault-integration.md
```

### Day 4: Deployment

#### Option A: Azure App Service (Easiest)

```powershell
# Create App Service
az webapp create `
  --resource-group zorro-prod `
  --plan zorro-plan `
  --name zorro-app `
  --runtime "PYTHON|3.11"

# Deploy code
az webapp up `
  --name zorro-app `
  --resource-group zorro-prod `
  --runtime "PYTHON|3.11"

# Configure app settings (environment variables)
az webapp config appsettings set `
  --name zorro-app `
  --resource-group zorro-prod `
  --settings @appsettings.json
```

#### Option B: Docker + Kubernetes

```powershell
# Build Docker image
docker build -t zorro:latest .

# Push to container registry
docker tag zorro:latest walmart.azurecr.io/zorro:latest
docker push walmart.azurecr.io/zorro:latest

# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

#### Start Celery Workers (Production)

**Option A: Systemd Service** (Linux):
```bash
# Create /etc/systemd/system/zorro-worker.service
[Unit]
Description=Zorro Celery Worker
After=network.target

[Service]
Type=forking
User=zorro
WorkingDirectory=/opt/zorro
Environment="PATH=/opt/zorro/venv/bin"
ExecStart=/opt/zorro/venv/bin/celery -A src.workers.celery_app worker \\
  --loglevel=warning \\
  --concurrency=4 \\
  -Q videos,batch \\
  --pidfile=/var/run/celery/worker.pid \\
  --logfile=/var/log/celery/worker.log

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable zorro-worker
sudo systemctl start zorro-worker
```

**Option B: Windows Service**:
Use NSSM (Non-Sucking Service Manager) to run Celery as Windows Service

### Day 5: Testing & Validation

#### Load Testing

```python
# scripts/load_test.py
import concurrent.futures
from src.workers.tasks import generate_video_async

def test_load():
    video_requests = [
        {"video_id": f"load_test_{i}", "prompt_data": {...}}
        for i in range(100)
    ]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(generate_video_async.delay, req["video_id"], req["prompt_data"])
            for req in video_requests
        ]
        
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    print(f"Completed: {len(results)}/100")

if __name__ == "__main__":
    test_load()
```

#### Monitoring Setup

```python
# Check system health
from src.database import get_db
from src.workers.celery_app import celery_app

# Database health
db = get_db()
with db.session() as session:
    print(f"✓ Database: {session.execute('SELECT 1').scalar()}")

# Celery health
inspect = celery_app.control.inspect()
print(f"✓ Active workers: {len(inspect.active())}")
print(f"✓ Registered tasks: {inspect.registered()}")
```

---

## Part 3: Scaling Strategy

### Phase 2 (February 2026): 50-100 videos/week

**Infrastructure**:
- 2 Celery workers (4 processes each)
- PostgreSQL (4 vCPU, 16GB RAM)
- Redis (2GB)
- Web app (2 instances, load balanced)

**Cost Estimate**: $500-800/month

### Phase 3 (Q2 2026): 100-150 videos/week

**Infrastructure**:
- 4 Celery workers
- PostgreSQL (8 vCPU, 32GB RAM)
- Redis (4GB, clustered)
- Web app (3 instances)

**Cost Estimate**: $1,200-1,500/month

### Production (Q3 2026): 150-200+ videos/week

**Infrastructure**:
- 8+ Celery workers (auto-scaling)
- PostgreSQL (16 vCPU, 64GB RAM)
- Redis Cluster (16GB)
- Web app (5+ instances, auto-scaling)
- CDN for video delivery

**Cost Estimate**: $2,500-3,500/month

---

## Troubleshooting

### Database Connection Issues

```powershell
# Test connection
python -c "from src.database import get_db; print(get_db().db_type)"

# Check PostgreSQL
docker exec -it zorro-postgres psql -U zorro -d zorro -c "\dt"
```

### Celery Not Processing

```powershell
# Check Celery status
celery -A src.workers.celery_app inspect active
celery -A src.workers.celery_app inspect stats

# Check Redis
redis-cli ping
redis-cli info stats
```

### Performance Issues

```sql
-- Check slow queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - pg_stat_activity.query_start > interval '5 seconds';

-- Check table sizes
SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename::regclass)) AS size
FROM pg_tables
WHERE schemaname = 'public';
```

---

## Security Checklist

- [ ] SSL verification enabled (`WALMART_SSL_VERIFY=true`)
- [ ] Secrets in Key Vault (not .env files)
- [ ] Database credentials rotated regularly
- [ ] SSO service account configured
- [ ] Network security groups configured
- [ ] Logging enabled and monitored
- [ ] Backup and recovery tested
- [ ] Security scan completed (Snyk, Bandit)

---

## Support

- **Technical Issues**: #help-genai-media-studio (Slack)
- **Infrastructure**: ServiceNow
- **Security**: infosec@walmart.com
- **Database**: database-team@walmart.com

---

**Ready to Deploy?** Follow the steps above, and Zorro will be production-ready in 3-5 days!
