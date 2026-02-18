# Walmart Refresh Touring Guide

A comprehensive web application for managing Walmart store refresh processes with role-based interfaces and multi-language support.

## 🎯 Quick Links
- **[Installation Guide](./INSTALLATION.md)** - Setup and prerequisites
- **[Quick Start Guide](./QUICK_START.md)** - Get running in 5 minutes
- **[MVP Tasks](./docs/MVP-TASKS.md)** - Current development priorities
- **[BigQuery Setup](./server/docs/BIGQUERY_SETUP.md)** - Store data integration
- **[API Documentation](./docs/api.md)** - REST API reference
- **[PRD 3.0](./docs/PRD.md)** - Product requirements

## 🌐 Local Development URLs

Once the development servers are running, access the application at:

- **http://localhost:3002/** - Main Business Owner Dashboard (Refresh Guide App)
  - Login page and authentication
  - Business Owner Dashboard with "View & Manage All Items"
  - Survey/Checklist functionality
  - User management interface

- **http://localhost:3000/** - Business Overview Reporting Dashboard (Code Puppy Pages)
  - business-overview-dashboard-v3-1-19-26.html
  - business-overview-comparison-dashboard.html
  - Various dashboard versions and reports

- **http://localhost:5000/** - Backend API Server
  - REST API endpoints (not user-facing)
  - Authentication and data management APIs

## Core Interfaces

1. **Business Owner Dashboard** - Create items, track progress, filter by store attributes
2. **Store Associate Mobile Interface** - Complete checklist items on mobile devices
3. **Admin Dashboard** - User management and item approval workflow
4. **Store Manager View** - Store-specific progress tracking

## Architecture

- **Backend**: Node.js + Express + PostgreSQL + BigQuery integration
- **Frontend**: React 18 + TypeScript + Material-UI v5
- **Authentication**: JWT-based with role-based access control (5 roles)
- **Internationalization**: i18next (English, Spanish)
- **Mobile**: Progressive Web App (PWA) optimized for mobile devices
- **Data Integration**: Daily BigQuery sync for store details and contacts

## 🔄 Disaster Recovery

If you lose your local copy and need to rebuild from GitHub:

### 1. Clone Repository
```bash
git clone https://gecgithub01.walmart.com/krush/refresh_guide.git
cd refresh_guide
```

### 2. Regenerate Data from BigQuery
The following large data files are **not stored in git** but can be regenerated:

```bash
# Extract V3 user engagement data
node extract-v3-user-data.js

# Generate dashboard with embedded BigQuery data
node code-puppy-pages/generate-embedded-data-bigquery-pr.js
```

### 3. Required Access
- BigQuery access to `athena-gateway-prod.store_refresh.store_refresh_data`
- BigQuery access to `wmt-assetprotection-prod.Store_Support_Dev.Store Cur Data`
- BigQuery credentials file (not in git - contact admin)

### 4. Generated Files
These files will be recreated from BigQuery:
- `data/EmbeddedData2/reviewAssignments.json` (320 MB)
- `data/business_overview_/reviewAssignments.json` (190 MB)
- `code-puppy-pages/business-overview-dashboard-v3-PR-1-19-26.html` (7.15 MB - also in git)

**Recovery Time**: ~5-10 minutes depending on BigQuery response time

**Note**: Dashboard HTML files are kept in git for deployment, but raw data files are excluded and regenerated from source.

## Project Structure

```
walmart-refresh-guide/
├── server/                 # Backend API
│   ├── src/
│   │   ├── controllers/    # API controllers
│   │   ├── models/         # Database models
│   │   ├── routes/         # API routes
│   │   ├── middleware/     # Authentication & validation
│   │   ├── utils/          # Helper functions
│   │   └── database/       # Database configuration
│   └── package.json
├── client/                 # Frontend React app
│   ├── src/
│   │   ├── components/     # Shared components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API services
│   │   ├── utils/          # Helper functions
│   │   └── styles/         # CSS/styling
│   └── package.json
├── database/               # Database scripts
│   ├── migrations/         # Database migrations
│   └── seeds/              # Sample data
└── docs/                   # Documentation
```

## ✨ Key Features

### 🌍 Multi-Language Support (NEW)
- English (en-US) and Spanish (es-MX) translations
- Language switcher in header
- Dynamic content translation for 366 checklist items
- Locale-based formatting

### 📊 BigQuery Integration (NEW)
- Daily automated sync from `wmt-assetprotection-prod`
- Store details: Format (SC/NHM/DIV 1), Division, Region, Market
- Store contacts: Manager and coach information
- Business Owner filtering by store attributes
- Email alerts on sync failures

### Business Owner Interface
- Create/manage refresh items across all stores
- Filter by Format, Division, Region, Market, Store
- Attach resource URLs to items
- Assign items to store coaches (Coach 1-4)
- Track completion status (Pending/Completed/N/A)
- View aggregated progress metrics

### Store Associate Interface
- Mobile-optimized checklist interface
- Store-specific items based on login email
- Expandable item descriptions
- Inline editing with auto-save
- Progress tracking by area (Backroom, Front End, etc.)
- Resources dropdown for each item

### Admin Interface
- User management (create, edit, deactivate)
- Item approval workflow
- Role assignment (Store Associate, Store Manager, Business Owner, Admin, Super Admin)

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ (includes npm)
- PostgreSQL 12+
- BigQuery service account (optional, for store data sync)

### Quick Setup

1. **Install dependencies:**
   ```bash
   # Install all packages (client + server)
   cd client
   npm install --legacy-peer-deps
   
   cd ../server
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   # Copy example files
   cp server/.env.example server/.env
   cp client/.env.example client/.env
   
   # Edit server/.env with your database credentials
   # Add BigQuery credentials (optional)
   ```

3. **Set up database:**
   ```bash
   # Create database
   createdb walmart_refresh_guide
   
   # Run migrations
   cd server
   npm run migrate
   ```

4. **Start development servers:**
   ```bash
   # Terminal 1 - Start backend (port 5000)
   cd server
   npm start
   
   # Terminal 2 - Start frontend (port 3000)
   cd client
   npm start
   ```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Health check: http://localhost:5000/health

### BigQuery Setup (Optional)
For store data integration, see [BigQuery Setup Guide](./server/docs/BIGQUERY_SETUP.md)

## 📂 Project Structure

```
refresh-guide/
├── client/                          # React frontend
│   ├── public/
│   │   └── checklist-data.json     # 366 refresh items
│   ├── src/
│   │   ├── components/
│   │   │   ├── Common/             # Shared components
│   │   │   ├── Dashboard/          # Dashboard widgets
│   │   │   ├── Forms/              # Form components
│   │   │   ├── LanguageSwitcher/   # Language selection (NEW)
│   │   │   └── Layout/             # Layout wrapper
│   │   ├── locales/                # Translation files (NEW)
│   │   │   ├── en-US.json
│   │   │   └── es-MX.json
│   │   ├── pages/
│   │   │   ├── Admin/              # Admin interface
│   │   │   ├── BusinessOwner/      # Business Owner dashboard
│   │   │   └── StoreAssociate/     # Store interface
│   │   ├── services/               # API clients
│   │   ├── i18n.ts                 # i18next config (NEW)
│   │   └── App.tsx
│   └── package.json
├── server/                          # Node.js backend
│   ├── config/
│   │   └── bigquery-config.js      # BigQuery config (NEW)
│   ├── data/                        # Generated data files
│   │   ├── store-details.json      # From BigQuery (NEW)
│   │   └── store-contacts.json     # From BigQuery (NEW)
│   ├── docs/
│   │   └── BIGQUERY_SETUP.md       # Setup guide (NEW)
│   ├── routes/
│   │   ├── auth.js                 # Authentication
│   │   ├── bigquery.js             # BigQuery API (NEW)
│   │   ├── checklistData.js        # Checklist items
│   │   └── ...
│   ├── scripts/
│   │   ├── sync-bigquery.js        # Manual sync (NEW)
│   │   └── sync-scheduler.js       # Scheduled sync (NEW)
│   ├── src/
│   │   ├── database/               # PostgreSQL models
│   │   ├── middleware/             # Auth & validation
│   │   ├── models/                 # Sequelize models
│   │   └── index.js                # Server entry
│   └── utils/
│       ├── bigquery-client.js      # BigQuery client (NEW)
│       └── email-alert.js          # Email notifications (NEW)
├── docs/                            # Documentation
│   ├── api.md                       # API reference
│   ├── LANGUAGE_TRANSLATION.md      # Translation guide
│   ├── MVP-QUICK-REFERENCE.md       # MVP summary
│   ├── MVP-TASKS.md                 # Development tasks
│   └── PRD.md                       # Product requirements
└── README.md                        # This file
```

## 🔑 Environment Variables

### Server (`.env`)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/walmart_refresh_guide

# JWT
JWT_SECRET=your-secret-key

# BigQuery (Optional)
BIGQUERY_PROJECT_ID=wmt-assetprotection-prod
BIGQUERY_CREDENTIALS_PATH=./config/bigquery-key.json
SYNC_SCHEDULE_CRON=0 8 * * *
ALERT_EMAIL=your-email@walmart.com
SMTP_HOST=smtp.walmart.com
SMTP_PORT=587
```

### Client (`.env`)
```env
REACT_APP_API_URL=http://localhost:5000
```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user

### Checklist Data
- `GET /api/checklist-data` - Get all checklist items
- `POST /api/checklist-data` - Create new item (Business Owner)
- `PUT /api/checklist-data/:id` - Update item
- `DELETE /api/checklist-data/:id` - Delete item (Admin)

### BigQuery (NEW)
- `GET /api/bigquery/sync/status` - Check last sync status
- `POST /api/bigquery/sync/trigger` - Manual sync (Admin)
- `GET /api/bigquery/store-details` - Get store data with filters
- `GET /api/bigquery/store-details/:storeNumber` - Get single store
- `GET /api/bigquery/store-contacts/:storeNumber` - Get store contacts
- `GET /api/bigquery/filters/options` - Get filter dropdown options

### Dashboard
- `GET /api/dashboard/stats` - Get completion statistics
- `GET /api/dashboard/progress` - Get progress by area

Detailed API documentation: [`/docs/api.md`](./docs/api.md)

## Deployment

Instructions for production deployment are available in `/docs/deployment.md`.

## Contributing

1. Follow the established project structure
2. Use TypeScript for type safety
3. Follow mobile-first responsive design principles
4. Write tests for new features
5. Update documentation as needed

---

## 📋 Recent Updates (November 20, 2025)

### ✅ Phase 15: BigQuery Integration (COMPLETE)
- **Automated daily sync** from BigQuery at 2 AM CT
- **Store data integration**: Format, Division, Region, Market
- **Store contacts**: Manager and coach information
- **Email alerts** for sync failures
- **REST API** for filtered store data access
- **Infrastructure**: Configuration, client, scheduler, routes

### ✅ Phase 10-11: Language Translation (COMPLETE)
- **Multi-language support**: English (en-US) and Spanish (es-MX)
- **Dynamic content translation** for 366 checklist items
- **Language switcher** component in header
- **Translation infrastructure**: i18next, getTranslatedText() helper
- **Status**: 4 items translated, 362 remaining (MVP task)

### 📋 MVP Tasks In Progress
See [`docs/MVP-TASKS.md`](./docs/MVP-TASKS.md) for detailed requirements:
1. Create Item Button (8-12h)
2. AMP AD Group Integration (20-30h)
3. Business Area Access Control (10-15h)
4. Spanish Translation Complete (15-20h)
5. Store Management Contacts (2-4h)
6. Admin Approval Workflow (8-12h)
7. Business Owner Filtering (20-25h) - **Depends on BigQuery**
8. Voice-to-Text Notes (12-16h)
9. WCAG 2.1 AA Compliance (25-30h)

**Total MVP Effort:** 120-164 hours | **Target:** December 2025

### 🎯 MVP Strategy Document

We've created a comprehensive strategy for rapid value delivery while managing enterprise compliance requirements.

📄 **Key Document:** [`MVP_STRATEGY.md`](./MVP_STRATEGY.md)

### What's Inside:

**The Challenge:**
- Full Walmart compliance requires 20+ weeks
- Multiple blockers with 2-week+ lead times (SSO registration, API access)
- We have a working app today that could help stores now

**The Solution - Three-Tier Hybrid Approach:**

1. **Tier 1: Pilot (Weeks 1-2)**
   - Deploy to 5 stores using current tech stack
   - Add Phase 0 improvements (already complete)
   - Fast Azure deployment (App Service + PostgreSQL)
   - Prove value, gather feedback
   - **Investment:** $8K | **Return:** Validates concept

2. **Tier 2: Limited Production (Weeks 3-6)**
   - Scale to 20 stores
   - Hybrid authentication (JWT + SSO in parallel)
   - Basic compliance (monitoring, accessibility, branding)
   - Azure Database for PostgreSQL (no provisioning wait)
   - **Investment:** $24K | **ROI:** 50% Year 1

3. **Tier 3: Enterprise Scale (Weeks 7-20)**
   - Scale to 4,700 stores
   - Full compliance (mandatory SSO, Living Design, AKS)
   - All enterprise integrations (Store Directory, Retail Link, FMS)
   - **Investment:** $86K | **ROI:** 3,200% Year 1 ($2.82M savings)

### Smart Workarounds for Blockers:

| Blocker | Traditional Approach | Our Solution |
|---------|---------------------|--------------|
| SSO registration (2 weeks) | Wait for approval | Hybrid auth: JWT + SSO in parallel |
| Cloud SQL provisioning (2 weeks) | Wait for provisioning | Azure PostgreSQL (instant) |
| Living Design migration (complex) | Block UI work | Walmart colors + accessibility first, migrate incrementally |
| Store Directory API access | Wait for approval | Manual validation, request in parallel |

### Quick Win Features (Implement First):

1. **Bulk Operations** - Complete entire department at once (reduces time by 66%)
2. **Smart Defaults** - Auto-populate common responses (N/A for unavailable departments)
3. **Progressive Disclosure** - Show 5-10 items at a time (reduces cognitive load)
4. **Image Compression** - Reduce 5MB → 500KB (fixes slow WiFi issues)
5. **Offline Queue** - Visual sync status (works in backroom/freezer WiFi dead zones)

### Business Case:
- **Current:** 70-item checklist takes 30 minutes per store manually
- **With MVP:** Same checklist takes 10 minutes with smart features
- **At Scale:** 4,700 stores × 2 hours saved/month = **$2.82M annual savings**
- **Cost:** $6,600/year infrastructure = **42,800% ROI**

### Recommended Next Steps:

**This Week:**
- [ ] Review `MVP_STRATEGY.md` together
- [ ] Decide: Proceed with Tier 1 pilot?
- [ ] If yes: Identify 5 pilot stores
- [ ] Spin up Azure resources (1 day)
- [ ] Deploy pilot (2 days)

**Week 2:**
- [ ] Implement Quick Win features (bulk actions, image compression)
- [ ] Onboard pilot stores with training
- [ ] Monitor usage and gather feedback
- [ ] Iterate on critical issues

**Weeks 3-6:**
- [ ] Submit SSO registration (runs in parallel)
- [ ] Scale to 20 stores with hybrid auth
- [ ] Add basic compliance (monitoring, accessibility)

### Decision Point:

**Option A: Start Tier 1 Pilot Now**
- Pros: Immediate value, fast feedback, proves ROI
- Cons: Pilot exemption needed from IT Security

**Option B: Wait for Full Compliance First**
- Pros: No exemptions needed
- Cons: 20+ week delay, no user feedback, risk building wrong solution

**Recommendation:** Option A (pilot approach is industry best practice)

---

## 📚 Documentation Suite

For collaboration and stakeholder communication, we have several key documents:

- **[`EXECUTIVE_SUMMARY.md`](./EXECUTIVE_SUMMARY.md)** - Professional presentation for stakeholders (formatted like tour-it)
- **[`MVP_STRATEGY.md`](./MVP_STRATEGY.md)** - Rapid delivery strategy with 3-tier hybrid approach ⭐ **READ THIS FIRST**
- **[`IMPLEMENTATION_ROADMAP.md`](./IMPLEMENTATION_ROADMAP.md)** - Detailed 20-week technical plan
- **[`WALMART_COMPLIANCE_MIGRATION.md`](./WALMART_COMPLIANCE_MIGRATION.md)** - Enterprise compliance requirements
- **[`WALMART_STANDARDS_REFERENCE.md`](./WALMART_STANDARDS_REFERENCE.md)** - Official Walmart standards (from Wibey AI)
- **[`PHASE_0_SUMMARY.md`](./PHASE_0_SUMMARY.md)** - Foundation improvements (COMPLETE ✅)

## 🛠️ Technology Stack

### Frontend
- React 18.2.0 with TypeScript 4.9.5
- Material-UI (MUI) v5
- i18next for internationalization
- React Router v6 for routing
- Axios for API calls

### Backend
- Node.js with Express.js
- PostgreSQL with Sequelize ORM
- JWT authentication
- Google BigQuery Node.js client
- node-cron for scheduled tasks
- nodemailer for email alerts

### DevOps
- Git for version control
- npm for package management
- Development/Production environments
- Daily BigQuery sync automation

## 📊 Data Flow

```
BigQuery (wmt-assetprotection-prod)
  └─> Daily Sync (2 AM CT)
       └─> Store Details + Contacts
            └─> JSON Files (server/data/)
                 └─> REST API Endpoints
                      └─> Business Owner Filters
                           └─> Store-Specific Items
```

## 🔒 Authentication & Authorization

### Roles
1. **Store Associate** - View/edit assigned store items
2. **Store Manager** - View store progress, manage team
3. **Business Owner** - Create items, view all stores, filter by attributes
4. **Admin** - User management, approve items
5. **Super Admin** - Full system access

### Security Features
- JWT-based authentication
- Password hashing with bcryptjs
- Role-based access control (RBAC)
- Rate limiting (100 requests/15 minutes)
- Helmet.js security headers
- CORS configuration

## 🌍 Internationalization

Currently supported languages:
- 🇺🇸 **English (en-US)** - Default
- 🇲🇽 **Spanish (es-MX)** - 4 of 366 items translated

**Phase 2:** Mandarin Chinese (zh-CN)

Translation files: `client/src/locales/*.json`

## 📖 Documentation Suite

### Getting Started
- **[README.md](./README.md)** - This file (overview and quick start)
- **[INSTALLATION.md](./INSTALLATION.md)** - Detailed installation guide
- **[QUICK_START.md](./QUICK_START.md)** - 5-minute setup guide

### Development
- **[docs/MVP-TASKS.md](./docs/MVP-TASKS.md)** - Current development priorities
- **[docs/MVP-QUICK-REFERENCE.md](./docs/MVP-QUICK-REFERENCE.md)** - MVP summary
- **[docs/api.md](./docs/api.md)** - REST API documentation
- **[server/docs/BIGQUERY_SETUP.md](./server/docs/BIGQUERY_SETUP.md)** - BigQuery integration guide
- **[docs/LANGUAGE_TRANSLATION.md](./docs/LANGUAGE_TRANSLATION.md)** - Translation workflow

### Product & Strategy
- **[docs/PRD.md](./docs/PRD.md)** - Product Requirements Document v3.0
- **[MVP_STRATEGY.md](./MVP_STRATEGY.md)** - Rapid delivery strategy
- **[IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md)** - 20-week technical plan
- **[WALMART_COMPLIANCE_MIGRATION.md](./WALMART_COMPLIANCE_MIGRATION.md)** - Enterprise compliance

## 🧪 Testing

```bash
# Run backend tests (when available)
cd server
npm test

# Run frontend tests (when available)
cd client
npm test
```

See [`TESTING_GUIDE.md`](./TESTING_GUIDE.md) for detailed testing procedures.

## 🚀 Deployment

Production deployment instructions: [`docs/deployment.md`](./docs/deployment.md)

**Recommended Stack:**
- Azure App Service (backend)
- Azure Static Web Apps (frontend)
- Azure Database for PostgreSQL
- Azure Key Vault (credentials)

## 🤝 Contributing

1. Follow the established project structure
2. Use TypeScript for type safety
3. Follow mobile-first responsive design principles
4. Write tests for new features
5. Update documentation as needed
6. Follow Walmart coding standards

## 📝 License

Internal Walmart project - Not for public distribution

## 👥 Team & Contacts

**Business Owner:** Kendall Rush (kendall.rush@walmart.com)  
**Product Owner:** Kendall Rush  
**Development Team:** TBD  
**Support:** #refresh-touring-guide-support (Slack)

---

**Last Updated:** November 20, 2025  
**Version:** 3.0 (BigQuery Integration Complete)  
**Next Milestone:** MVP Feature Development (December 2025)