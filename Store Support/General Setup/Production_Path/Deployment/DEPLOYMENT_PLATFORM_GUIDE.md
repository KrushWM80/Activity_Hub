# Deployment Platform Decision Guide

**Last Updated:** December 3, 2025  
**Purpose:** Help you choose the right deployment platform for your project

---

## Quick Decision Tree

```
START: What type of project do you have?

├─ Single HTML page with client-side JavaScript only?
│  └─ ✅ USE: Code Puppy
│
├─ Python Flask/FastAPI application?
│  └─ ✅ USE: Posit Connect
│
├─ R Shiny application?
│  └─ ✅ USE: Posit Connect
│
├─ Node.js/Express + React/Angular/Vue?
│  ├─ Does it need a database?
│  │  ├─ Yes → ✅ USE: Walmart Cloud Platform (Docker)
│  │  └─ No → ✅ USE: Static Hosting + Serverless API
│  │
│  └─ Is it just for demo/POC?
│     └─ ✅ USE: Local deployment or Code Puppy (simplified version)
│
├─ Java Spring Boot application?
│  └─ ✅ USE: Walmart Cloud Platform (Kubernetes)
│
├─ .NET Core application?
│  └─ ✅ USE: Walmart Cloud Platform (IIS/Azure)
│
└─ Static website (HTML/CSS/JS only)?
   └─ ✅ USE: Static Hosting (S3, GitHub Pages, Azure Static Web Apps)
```

---

## Platform Comparison Matrix

| Platform | Best For | Language Support | Database Support | Complexity | Hosting Location |
|----------|----------|------------------|------------------|------------|-----------------|
| **Code Puppy** | Single HTML page demos | JavaScript (client-side) | BigQuery only | ⭐ Low | Walmart Internal |
| **Posit Connect** | Python/R data apps | Python, R | PostgreSQL, BigQuery, MySQL | ⭐⭐ Medium | Walmart Internal |
| **Walmart Cloud** | Full-stack apps | Any (Node, Python, Java, .NET) | Any database | ⭐⭐⭐ High | AWS/Azure (Walmart) |
| **Docker** | Containerized apps | Any | Any | ⭐⭐⭐ High | Any platform |
| **Static Hosting** | Frontend-only sites | HTML/CSS/JS | None (API only) | ⭐ Low | Various |
| **Serverless** | Event-driven apps | Node, Python, Java, .NET | Managed databases | ⭐⭐ Medium | AWS Lambda, Azure Functions |

---

## Platform Deep Dive

### 1. Code Puppy

**What It Is:**  
Walmart's platform for hosting **single HTML page** applications with BigQuery integration.

**✅ Use Code Puppy When:**
- You have a simple dashboard or visualization
- All logic can run client-side (JavaScript)
- You only need BigQuery for data
- No user authentication required (or LDAP only)
- Quick POC or demo needed

**❌ Don't Use Code Puppy When:**
- You have multiple files/pages
- You need a backend server
- You require databases beyond BigQuery
- You need complex authentication
- You have React/Angular/Vue that needs compilation

**Technology Stack:**
- **Frontend:** Pure HTML, CSS, JavaScript (vanilla or jQuery)
- **Backend:** None (direct BigQuery from browser)
- **Database:** BigQuery only

**Deployment Requirements:**
- Single `.html` file with embedded CSS and JavaScript
- BigQuery connection configured
- No build process

**Example Use Cases:**
- Executive dashboards pulling from BigQuery
- Data visualization tools (charts, graphs, tables)
- Simple form submissions to BigQuery
- Interactive reports

**Time to Deploy:** 1-2 hours

---

### 2. Posit Connect

**What It Is:**  
Enterprise platform for hosting **Python Flask/FastAPI** and **R Shiny** applications.

**✅ Use Posit Connect When:**
- You have a Python Flask/FastAPI application
- You have an R Shiny application
- You need scheduled reports/jobs
- You need Jupyter notebooks hosted
- Data science team needs to share work

**❌ Don't Use Posit Connect When:**
- You have Node.js/Express backend
- You have React/Angular/Vue frontend only
- You need WebSocket support
- You need complex microservices architecture

**Technology Stack:**
- **Frontend:** Jinja templates (Python) or Shiny UI (R)
- **Backend:** Flask, FastAPI (Python) or Shiny Server (R)
- **Database:** PostgreSQL, BigQuery, MySQL, Snowflake

**Deployment Requirements:**
- `app.py` (Flask entry point)
- `requirements.txt` (Python dependencies)
- `manifest.json` (Posit-specific configuration)
- Service account for GCP/BigQuery access
- All dependencies must be pip-installable

**Example Use Cases:**
- Data science dashboards with ML models
- Interactive analytics applications
- Scheduled report generation
- Jupyter notebook sharing
- Python-based CRUD applications

**Time to Deploy:** 1-2 days (first time), 2-4 hours (subsequent)

---

### 3. Walmart Cloud Platform (Docker/Kubernetes)

**What It Is:**  
Walmart's internal cloud infrastructure (AWS/Azure) for hosting **production applications**.

**✅ Use Walmart Cloud When:**
- You have a production-ready application
- You need scalability (horizontal scaling)
- You require high availability (99.9%+ uptime)
- You need multiple environments (dev/staging/prod)
- You have complex backend logic
- You require databases (PostgreSQL, MongoDB, Redis, etc.)

**❌ Don't Use Walmart Cloud When:**
- Simple demo or POC
- No IT support available
- Project is temporary (<3 months)
- Very small user base (<10 users)

**Technology Stack:**
- **Any language/framework:** Node.js, Python, Java, .NET, Go, Ruby
- **Any database:** PostgreSQL, MySQL, MongoDB, Redis, Cassandra, BigQuery
- **Any architecture:** Monolith, microservices, serverless

**Deployment Requirements:**
- `Dockerfile` (container definition)
- `docker-compose.yml` (multi-container setup) or Kubernetes manifests
- CI/CD pipeline configuration
- Environment variables configuration
- Health check endpoints
- Logging and monitoring setup

**Example Use Cases:**
- Full-stack web applications
- REST APIs with database
- Microservices architectures
- Applications with >100 concurrent users
- Mission-critical business applications

**Time to Deploy:** 1-2 weeks (first time), 1-2 days (subsequent)

---

### 4. Static Hosting (S3, GitHub Pages, Azure Static Web Apps)

**What It Is:**  
Hosting for **frontend-only** applications (HTML/CSS/JS) without a backend.

**✅ Use Static Hosting When:**
- You have a React/Angular/Vue app with no backend
- All APIs are external (REST APIs, serverless functions)
- Content is mostly static or client-side rendered
- You need fast, cheap hosting

**❌ Don't Use Static Hosting When:**
- You need server-side rendering (SSR)
- You need authentication beyond OAuth
- You need database connections
- You need scheduled jobs

**Technology Stack:**
- **Frontend:** React, Angular, Vue, or plain HTML/CSS/JS
- **Backend:** External APIs only (AWS Lambda, Azure Functions, third-party APIs)
- **Database:** None (use APIs to access databases)

**Deployment Requirements:**
- Build command (e.g., `npm run build`)
- Output directory (`build/` or `dist/`)
- Optional: CDN configuration
- Optional: Custom domain setup

**Example Use Cases:**
- Marketing websites
- Documentation sites
- Single Page Applications (SPAs) with API backends
- Portfolio or blog sites

**Time to Deploy:** 30 minutes - 2 hours

---

### 5. Serverless (AWS Lambda, Azure Functions)

**What It Is:**  
**Event-driven** compute service that runs code without managing servers.

**✅ Use Serverless When:**
- You have event-driven workloads (API calls, file uploads, scheduled tasks)
- You need automatic scaling (0 to thousands)
- You want to minimize infrastructure management
- You have sporadic or unpredictable traffic

**❌ Don't Use Serverless When:**
- Long-running processes (>15 minutes)
- Need persistent WebSocket connections
- Require low-latency (<10ms) responses
- Need full control over server environment

**Technology Stack:**
- **Languages:** Node.js, Python, Java, .NET, Go
- **Triggers:** HTTP requests, S3 events, database changes, scheduled cron
- **Database:** DynamoDB, RDS, BigQuery (via API)

**Deployment Requirements:**
- Function code (single entry point)
- Dependencies package
- Trigger configuration
- IAM roles and permissions

**Example Use Cases:**
- REST APIs with light processing
- Image/file processing pipelines
- Scheduled data transformations
- Webhook handlers

**Time to Deploy:** 2-4 hours

---

### 6. Docker Containers (Generic)

**What It Is:**  
Packaged application with all dependencies that can run **anywhere**.

**✅ Use Docker When:**
- You need consistent environments (dev/staging/prod)
- You want easy local development
- You need to deploy to multiple platforms
- You want version control for infrastructure

**❌ Don't Use Docker When:**
- Simple static website
- Single HTML page
- No IT/DevOps support available
- Learning curve is too steep for team

**Technology Stack:**
- **Any language/framework**
- **Any database** (containerized or external)
- **Any architecture**

**Deployment Requirements:**
- `Dockerfile` (defines container image)
- Application code
- Environment variables
- Port configuration
- Health check endpoint

**Example Use Cases:**
- Any application that needs portability
- Microservices architectures
- Applications with complex dependencies
- Multi-environment deployments

**Time to Deploy:** 1-3 days (first time), 2-4 hours (subsequent)

---

## Decision Factors

### 1. Project Complexity

**Simple (Single Page):**
- ✅ Code Puppy
- ✅ Static Hosting

**Medium (Backend + Frontend):**
- ✅ Posit Connect (Python)
- ✅ Serverless + Static Hosting
- ✅ Docker

**Complex (Microservices, High Scale):**
- ✅ Walmart Cloud (Kubernetes)
- ✅ Docker with orchestration

### 2. Team Skills

**HTML/CSS/JavaScript only:**
- ✅ Code Puppy
- ✅ Static Hosting

**Python/R data science:**
- ✅ Posit Connect

**Full-stack developers (any language):**
- ✅ Walmart Cloud
- ✅ Docker
- ✅ Serverless

**No DevOps experience:**
- ✅ Code Puppy
- ✅ Posit Connect
- ❌ Avoid: Docker, Kubernetes

### 3. Timeline

**Need it today/tomorrow:**
- ✅ Code Puppy (hours)
- ✅ Static Hosting (hours)

**Need it this week:**
- ✅ Posit Connect (1-2 days)
- ✅ Serverless (2-4 days)

**Need it this month:**
- ✅ Walmart Cloud (1-2 weeks)
- ✅ Docker/Kubernetes (1-2 weeks)

### 4. Budget

**$0 (Free):**
- ✅ Code Puppy (Walmart internal)
- ✅ Static Hosting (many free options)

**Low (<$100/month):**
- ✅ Serverless (pay per use)
- ✅ Static Hosting + CDN

**Medium ($100-$1000/month):**
- ✅ Posit Connect (Walmart internal)
- ✅ Docker on small VMs

**High (>$1000/month):**
- ✅ Walmart Cloud (enterprise)
- ✅ Kubernetes clusters

### 5. Data Requirements

**Only BigQuery:**
- ✅ Code Puppy

**PostgreSQL/MySQL:**
- ✅ Posit Connect
- ✅ Walmart Cloud
- ✅ Docker

**Multiple databases:**
- ✅ Walmart Cloud
- ✅ Docker

**No database (API only):**
- ✅ Static Hosting
- ✅ Serverless

### 6. User Load

**<10 users:**
- ✅ Code Puppy
- ✅ Posit Connect
- ✅ Static Hosting

**10-100 users:**
- ✅ Posit Connect
- ✅ Serverless
- ✅ Docker (single instance)

**100-1000 users:**
- ✅ Walmart Cloud
- ✅ Docker (multiple instances)

**1000+ users:**
- ✅ Walmart Cloud (auto-scaling)
- ✅ Kubernetes

---

## Common Scenarios

### Scenario 1: Executive Dashboard (BigQuery Data)

**Requirements:**
- Display charts and tables from BigQuery
- Used by 5-10 executives
- Simple filtering
- No user authentication needed

**Recommended Platform:** Code Puppy  
**Why:** Single HTML page, direct BigQuery access, simple to deploy  
**Alternative:** Posit Connect (if Python/R preferred)

---

### Scenario 2: Data Science Application (ML Model)

**Requirements:**
- Python Flask backend with ML model
- Interactive UI for predictions
- Scheduled retraining jobs
- 20-50 users

**Recommended Platform:** Posit Connect  
**Why:** Native Python support, scheduled jobs, built for data science  
**Alternative:** Walmart Cloud (if need more scaling)

---

### Scenario 3: Full-Stack CRUD Application

**Requirements:**
- React frontend
- Node.js Express backend
- PostgreSQL database
- User authentication
- 100-500 users

**Recommended Platform:** Walmart Cloud (Docker)  
**Why:** Supports full stack, database support, scales well  
**Alternative:** Split into Static Hosting (frontend) + Serverless (backend)

---

### Scenario 4: Marketing Website

**Requirements:**
- React/Next.js frontend
- No backend needed
- Fast loading
- Global audience

**Recommended Platform:** Static Hosting (S3 + CloudFront)  
**Why:** Fast CDN delivery, cheap, scales automatically  
**Alternative:** Next.js on Vercel/Netlify

---

### Scenario 5: REST API Only (No UI)

**Requirements:**
- Node.js/Python API
- MongoDB database
- Event-driven processing
- Variable load (0-1000 req/min)

**Recommended Platform:** Serverless (AWS Lambda)  
**Why:** Auto-scales, pay per use, handles variable load  
**Alternative:** Docker container on Walmart Cloud

---

### Scenario 6: Legacy Application Migration

**Requirements:**
- Java Spring Boot application
- Oracle database
- Needs to run on Walmart infrastructure
- Mission-critical

**Recommended Platform:** Walmart Cloud (Kubernetes)  
**Why:** Enterprise support, high availability, any technology  
**Alternative:** VM-based deployment if containerization too complex

---

## Migration Paths

### From Local Development → Production

**If you have Node.js + React:**
```
Local (ports 3000/5000)
    ↓
Docker container
    ↓
Walmart Cloud (dev environment)
    ↓
Walmart Cloud (production)
```

**If you have Python Flask:**
```
Local (port 5000)
    ↓
Create Posit manifest.json
    ↓
Posit Connect (dev)
    ↓
Posit Connect (production)
```

**If you have single HTML file:**
```
Local file
    ↓
Test BigQuery connection
    ↓
Code Puppy (immediate)
```

---

## Deployment Checklist by Platform

### Code Puppy
- [ ] Single HTML file created
- [ ] All CSS embedded in `<style>` tags
- [ ] All JavaScript embedded in `<script>` tags
- [ ] BigQuery queries tested
- [ ] No external dependencies
- [ ] Walmart branding applied

### Posit Connect
- [ ] `app.py` Flask application created
- [ ] `requirements.txt` with all dependencies
- [ ] `manifest.json` configured
- [ ] GCP service account created
- [ ] `.env` file with credentials
- [ ] Health check endpoint working
- [ ] Tested locally

### Walmart Cloud (Docker)
- [ ] `Dockerfile` created
- [ ] Application tested in container locally
- [ ] `docker-compose.yml` for multi-container setup
- [ ] Environment variables documented
- [ ] Health check endpoint implemented
- [ ] Logging configured
- [ ] CI/CD pipeline setup
- [ ] Security scan passed

### Static Hosting
- [ ] Build process tested (`npm run build`)
- [ ] Output directory identified
- [ ] Environment variables for APIs configured
- [ ] Custom domain DNS configured (if needed)
- [ ] CDN caching rules set
- [ ] HTTPS certificate configured

### Serverless
- [ ] Function code written with single entry point
- [ ] Dependencies packaged
- [ ] IAM roles configured
- [ ] Triggers configured (HTTP, cron, events)
- [ ] Environment variables set
- [ ] Timeout and memory limits configured
- [ ] Error handling and logging implemented

---

## Getting Help

### Code Puppy
- **Documentation:** [Internal Link]
- **Support:** [Team/Slack Channel]

### Posit Connect
- **Documentation:** https://docs.posit.co/connect/
- **Walmart Support:** [Team/Slack Channel]

### Walmart Cloud Platform
- **Documentation:** [Internal Link]
- **Support Ticket:** [ServiceNow Link]
- **Slack:** [Channel Name]

### Docker/Kubernetes
- **Docker Docs:** https://docs.docker.com/
- **Kubernetes Docs:** https://kubernetes.io/docs/
- **Walmart DevOps:** [Team/Slack Channel]

---

## Cost Comparison

| Platform | Setup Cost | Monthly Cost | Scaling Cost | Total (1st year) |
|----------|-----------|--------------|--------------|------------------|
| Code Puppy | $0 | $0 | $0 | $0 |
| Posit Connect | $0 | $0 (internal) | $0 | $0 |
| Static Hosting | $0 | $5-50 | $5-100 | $60-1800 |
| Serverless | $0 | $10-100 | $100-1000 | $1200-12000 |
| Docker (small) | $100 | $50-200 | $200-500 | $2400-6100 |
| Walmart Cloud | $500 | $500-5000 | $5000-50000 | $60000-600000 |

*Note: Walmart internal platforms (Code Puppy, Posit) are free for Walmart employees*

---

## Final Recommendations by Project Type

| Project Type | Best Platform | Second Choice | Avoid |
|--------------|---------------|---------------|-------|
| Single page dashboard | Code Puppy | Static Hosting | Walmart Cloud |
| Python data app | Posit Connect | Docker | Code Puppy |
| React + Node.js app | Walmart Cloud | Serverless + Static | Code Puppy |
| REST API only | Serverless | Docker | Code Puppy |
| Marketing website | Static Hosting | Serverless | Posit Connect |
| Legacy app migration | Walmart Cloud | Docker | Code Puppy |
| Microservices | Kubernetes (Walmart Cloud) | Docker Swarm | Posit Connect |
| Scheduled jobs | Posit Connect | Serverless (cron) | Static Hosting |

---

**Created by:** Kendall Rush  
**Last Updated:** December 3, 2025  
**Version:** 1.0
