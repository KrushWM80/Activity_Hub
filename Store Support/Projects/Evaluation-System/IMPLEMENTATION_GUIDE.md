# Evaluation System - Implementation Guide

## Overview

The Evaluation System is a standalone web application that generates performance evaluations from structured work data. This document outlines how to deploy it and prepare for future integration with Activity-Hub.

## Current Architecture

### Standalone Deployment

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│            Evaluation System (Standalone)               │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Frontend (Client)                              │   │
│  │  - React-free vanilla JS                        │   │
│  │  - HTML5 + CSS3 interface                       │   │
│  │  - 5-step wizard workflow                       │   │
│  │  - File upload + manual entry                   │   │
│  │  - Column mapping with tooltips                 │   │
│  │  - Live HTML editor                             │   │
│  └─────────────────────────────────────────────────┘   │
│                      ↓ REST API                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Backend (Node.js / Express)                    │   │
│  │  - File parsing (CSV, Excel)                    │   │
│  │  - Data transformation & mapping                │   │
│  │  - Evaluation engine                            │   │
│  │  - HTML template rendering                      │   │
│  │  - Score calculation algorithm                  │   │
│  └─────────────────────────────────────────────────┘   │
│                      ↓                                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Output Formats                                 │   │
│  │  - HTML (downloadable, editable)                │   │
│  │  - In-memory JSON (evaluation object)           │   │
│  │  - Database-ready (for Activity-Hub)            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Deployment Instructions

### Prerequisites

- Node.js 16+
- npm 7+
- Windows/Mac/Linux OS
- Browser: Chrome, Firefox, Safari, Edge

### Local Development

```bash
# 1. Navigate to project
cd C:\Users\krush\Documents\VSCode\Evaluation-System

# 2. Install dependencies
npm install

# 3. Start server
npm start

# 4. Open browser
# http://localhost:3001
```

### Production Deployment

#### Option 1: Docker (Recommended)

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY server ./server
COPY client ./client

EXPOSE 3001

CMD ["npm", "start"]
```

Build and run:
```bash
docker build -t evaluation-system .
docker run -p 3001:3001 evaluation-system
```

#### Option 2: Environment Variables

Create `.env` file:
```
PORT=3001
NODE_ENV=production
MAX_FILE_SIZE=52428800
EVALUATION_FIELDS_PATH=./server/config.js
TEMPLATE_PATH=./server/templateEngine.js
```

#### Option 3: Cloud Deployment

**AWS Elastic Beanstalk:**
```bash
eb init -p node.js-14 evaluation-system
eb create evaluation-system-env
eb deploy
```

**Heroku:**
```bash
heroku create your-evaluation-system
git push heroku main
```

**Azure App Service:**
```bash
az webapp up --name evaluation-system --resource-group your-group
```

## API Reference for Integration

### Core Endpoints

#### 1. Upload File
```
POST /api/upload
Content-Type: multipart/form-data

Request:
- file: <binary CSV or Excel>

Response:
{
  "success": true,
  "data": [
    {
      "Project": "Refresh Guide",
      "Status": "In Production",
      ...
    }
  ],
  "totalRows": 8,
  "availableColumns": ["Project", "Status", ...]
}
```

#### 2. Get Field Definitions
```
GET /api/fields

Response:
{
  "fields": {
    "project_name": {
      "label": "Project Name",
      "description": "Name of the project",
      "required": true,
      "type": "text",
      "category": "core"
    },
    ...
  },
  "periods": {...},
  "categories": ["core", "metrics", ...]
}
```

#### 3. Generate Evaluation
```
POST /api/evaluate
Content-Type: application/json

Request:
{
  "data": [
    {
      "Project": "Refresh Guide",
      "Status": "In Production",
      ...
    }
  ],
  "columnMappings": {
    "Project": "project_name",
    "Status": "project_status",
    ...
  },
  "userInfo": {
    "name": "John Doe",
    "title": "Senior Director",
    "period": "fy"
  }
}

Response:
{
  "success": true,
  "evaluation": {
    "metadata": {...},
    "summary": "...",
    "competencies": "...",
    "projectPortfolio": "...",
    "statistics": {...}
  },
  "score": 85,
  "summary": {...}
}
```

#### 4. Generate HTML
```
POST /api/generate-html
Content-Type: application/json

Request:
{
  "evaluation": {...},
  "score": 85,
  "userInfo": {...}
}

Response:
{
  "success": true,
  "html": "<html>...</html>"
}
```

#### 5. Download HTML
```
POST /api/download-html
Content-Type: application/json

Request: (same as generate-html)

Response:
- Content-Type: text/html
- Content-Disposition: attachment
- File: evaluation_name_date.html
```

## Integration with Activity-Hub

### Phase 1: Current (Standalone)
✅ Complete - Web app generates evaluations independently

### Phase 2: Planned Integration

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              Activity-Hub Platform                      │
│              (Future Integration)                       │
│                                                         │
│  ┌────────────────────────────────────────────────┐    │
│  │  Activity-Hub UI                               │    │
│  │  - Embedded Evaluation Tab                     │    │
│  │  - Real-time project data sync                 │    │
│  │  - Evaluation history view                     │    │
│  └────────────────────────────────────────────────┘    │
│                    ↓                                    │
│  ┌────────────────────────────────────────────────┐    │
│  │  Evaluation Service (Embedded)                 │    │
│  │  - Use same evaluation engine                  │    │
│  │  - Pull projects from Activity-Hub DB          │    │
│  │  - Auto-map Activity-Hub fields                │    │
│  │  - Store evaluations in Activity-Hub           │    │
│  └────────────────────────────────────────────────┘    │
│                    ↓                                    │
│  ┌────────────────────────────────────────────────┐    │
│  │  Activity-Hub Database                         │    │
│  │  - Projects table (already exists)             │    │
│  │  - New: Evaluations table                      │    │
│  │  - New: Evaluation history                     │    │
│  └────────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Integration Steps (When Ready)

1. **Extract Evaluation Engine**
   ```
   - Move evaluationEngine.js to Activity-Hub
   - Repackage as npm module
   - Import in Activity-Hub service
   ```

2. **Map Activity-Hub Data**
   ```javascript
   // Instead of file upload, pull from Activity-Hub DB
   const projectsFromHub = await getProjectsFromActivityHub(userId);
   const mappedData = autoMapActivityHubFields(projectsFromHub);
   const evaluation = evaluationEngine.generateEvaluation(mappedData);
   ```

3. **Store Evaluations**
   ```javascript
   // Save to Activity-Hub database
   const evaluation = new Evaluation({
     userId,
     period,
     generatedDate,
     content: evaluation,
     score,
     metadata
   });
   await evaluation.save();
   ```

4. **UI Integration**
   ```
   - Add "Evaluations" tab to Activity-Hub
   - Show evaluation history timeline
   - Quarterly/Mid-Year/FY auto-prompts
   - One-click regeneration
   ```

### Database Schema for Integration

```sql
-- Activity-Hub Integration Tables

CREATE TABLE evaluations (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  evaluation_period VARCHAR(20), -- quarterly, midyear, fy, custom
  generated_date TIMESTAMP,
  evaluation_content JSONB, -- Full evaluation object
  performance_score INTEGER,
  metadata JSONB,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE evaluation_history (
  id UUID PRIMARY KEY,
  evaluation_id UUID REFERENCES evaluations(id),
  version INTEGER,
  changes JSONB,
  changed_by UUID,
  changed_at TIMESTAMP
);

CREATE TABLE evaluation_projects (
  id UUID PRIMARY KEY,
  evaluation_id UUID REFERENCES evaluations(id),
  project_id UUID REFERENCES projects(id),
  project_snapshot JSONB, -- Capture project state at eval time
  metrics_at_eval_time JSONB,
  created_at TIMESTAMP
);
```

### Activity-Hub API Modifications (Future)

```javascript
// New endpoints in Activity-Hub

// Get evaluation by ID
GET /api/users/{userId}/evaluations/{evaluationId}

// List evaluations for user
GET /api/users/{userId}/evaluations

// Generate new evaluation
POST /api/users/{userId}/evaluations
{
  "period": "fy",
  "projects": [...] // Optional: override project list
}

// Update evaluation
PATCH /api/users/{userId}/evaluations/{evaluationId}
{
  "evaluation_content": {...}
}

// Download evaluation
GET /api/users/{userId}/evaluations/{evaluationId}/download
// Returns: HTML file

// Compare evaluations
GET /api/users/{userId}/evaluations/compare?eval1={id1}&eval2={id2}
// Returns: Side-by-side comparison
```

## Maintenance & Updates

### Regular Tasks

- **Weekly**: Monitor error logs
- **Monthly**: Update dependencies (`npm update`)
- **Quarterly**: Review and optimize evaluation algorithm
- **Annually**: Update field definitions based on company competency changes

### Updating System Fields

Edit `server/config.js`:

```javascript
export const evaluationFields = {
  // Add new fields here
  new_field: {
    label: "New Field",
    description: "...",
    required: false,
    type: "text",
    category: "custom",
    info: "..."
  }
};
```

### Updating Evaluation Algorithm

Edit `server/evaluationEngine.js`:

```javascript
// Modify scoring weights
generateEvaluation(projects, summary) {
  // Adjust metrics here
  return {
    ...
  };
}

calculateScore(projects, summary) {
  // Adjust scoring logic here
  let score = 50; // Base
  // ... modify calculations
}
```

## Monitoring & Logs

### Enable Debug Logging

```bash
# Development mode with detailed logs
NODE_DEBUG=express npm start

# Or set environment
DEBUG=* npm start
```

### Log Locations

- **Application Logs**: Console output
- **Error Logs**: Captured in error responses
- **File Upload Logs**: Temporary files cleaned up after processing

### Performance Metrics

Monitor these metrics:

```
- File upload times
- Evaluation generation time (target: <2 seconds)
- HTML generation time
- API response times
- Error rates
```

## Security Considerations

### Current Implementation

- ✅ File size limits (50MB)
- ✅ CORS enabled for local development
- ✅ Input validation on column mapping
- ✅ No data persistence by default

### For Production/Integration

- [ ] Implement authentication (JWT/OAuth)
- [ ] Add rate limiting on API endpoints
- [ ] Implement data encryption at rest
- [ ] Add audit logging for evaluations
- [ ] Implement role-based access control
- [ ] Validate all user inputs server-side
- [ ] Use HTTPS/TLS for all communications
- [ ] Implement session management

### Data Privacy

- No evaluation data is stored by default (standalone mode)
- Files are processed in-memory and discarded
- Integration with Activity-Hub will require data governance policies

## Troubleshooting Guide

### Server Issues

**Server won't start**
```bash
# Check port availability
netstat -ano | findstr :3001

# Check Node.js installation
node --version
npm --version

# Clear npm cache
npm cache clean --force
npm install
```

**High memory usage**
- Set file size limits lower
- Implement pagination for large datasets
- Clear temporary files regularly

### API Issues

**CORS errors**
- Ensure CORS is enabled in production
- Set appropriate CORS headers
- Check client origin

**Slow performance**
- Monitor file sizes being uploaded
- Check server resources
- Consider caching evaluation results

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Jan 2026 | Initial release - Standalone evaluation system |
| 1.1.0 | (Planned) | Add evaluation history/comparison |
| 2.0.0 | (Planned) | Activity-Hub integration |
| 2.1.0 | (Planned) | Advanced analytics/reporting |
| 3.0.0 | (Planned) | Team calibration features |

## Support & Escalation

### Common Issues

- See QUICK_START.md for user-facing troubleshooting
- See README.md for technical documentation
- Check inline code comments for implementation details

### Getting Help

1. Review this document
2. Check error messages in browser console
3. Run with DEBUG=* for verbose logging
4. Check server logs for API errors

---

## Next Steps

1. ✅ Deploy standalone evaluation system
2. ⏳ Gather user feedback on field definitions
3. ⏳ Plan Activity-Hub integration
4. ⏳ Design evaluation comparison features
5. ⏳ Implement team calibration views

---

**Document Version:** 1.0.0  
**Last Updated:** January 2026  
**Status:** Ready for Deployment
