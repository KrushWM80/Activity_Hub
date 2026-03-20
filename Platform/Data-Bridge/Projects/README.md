# Projects Backend - Data Bridge Integration

**Component**: Platform/Data-Bridge/Projects  
**Purpose**: Backend API and storage for Projects Data-Bridge (Admin sync control)  
**Port**: 8002 (Projects Data-Bridge Admin API)  
**Status**: Phase 1 Implementation ✅

---

## Architecture

### Three-Layer Design

```
┌─────────────────────────────────────────┐
│     Admin Dashboard (Admin/admin-dashboard.html) │
│        HTTP Requests to port 8002        │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│       Projects Backend API (Express)      │
│   - REST endpoints                        │
│   - Request validation                    │
│   - Response formatting                   │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┴────────────┐
    ▼                         ▼
┌──────────────────┐    ┌──────────────────┐
│ Projects Storage │    │ Validation &     │
│                  │    │ Transformation   │
│ - Native         │    │                  │
│   projects       │    │ Sync Service     │
│ - Relationships  │    │ - Intake Hub     │
│ - Cache          │    │   bridging       │
└──────────────────┘    └──────────────────┘
```

### Data Model

#### Native Projects
```json
{
  "project_id": "string (required)",
  "project_source": "Manual_Upload",
  "title": "string",
  "owner": "string",
  "status": "Active|Pending|Complete|Archived|Cancelled",
  "phase": "POC/POT|Test|Mkt Scale|Roll/Deploy|Complete|Pending|Planning",
  "health": "Green|Yellow|Red|Unknown",
  "created_date": "ISO8601",
  "last_updated": "ISO8601",
  "...": "All fields from projects-schema.json"
}
```

#### Bridged Projects (Intake Hub)
```json
{
  "project_id": "string",
  "project_source": "Intake_Hub",
  "intake_card": "string",
  "synced_at": "ISO8601",
  "data_source_id": "string",
  "...": "Transformed from Intake Hub columns"
}
```

#### Relationships
```
followers.json:
{
  "project_id_1": ["user_id_1", "user_id_2"],
  "project_id_2": ["user_id_3"]
}

partner_groups.json:
{
  "project_id_1": [
    {
      "group_name": "Fashion Team",
      "followers": ["user_1", "user_2"],
      "added_date": "ISO8601"
    }
  ]
}
```

---

## File Structure

```
Platform/Data-Bridge/Projects/
├── server.js                    # Main Express server (port 8002)
├── projects-storage.js          # File-based JSON storage layer
├── projects-validator.js        # Schema-based validation (uses Admin schema)
├── projects-sync.js             # Intake Hub data bridge and sync service
├── projects-api.js              # REST API endpoints
├── storage/
│   ├── projects/
│   │   ├── native/
│   │   │   ├── projects.json           # Native projects array
│   │   │   └── metadata.json           # Native project metadata
│   │   └── bridged/
│   │       ├── intake-hub-cache.json   # Cached bridged projects
│   │       └── last-sync.json          # Sync metadata
│   └── relationships/
│       ├── followers.json              # User follows relationships
│       └── partner_groups.json         # Partner group relationships
├── package.json                 # Node dependencies
└── README.md                    # This file
```

---

## Setup & Installation

### Prerequisites
- Node.js 14+ 
- npm or yarn

### Installation

```bash
cd Platform/Data-Bridge/Projects

# Install dependencies
npm install

# Verify dependencies are installed
npm list --depth=0
```

### Environment Variables

```bash
# Can be set via .env file or command line

# Server port (default: 8001)
PORT=8001

# Storage directory (default: ./storage)
STORAGE_DIR=./storage

# Auto-sync interval in milliseconds (default: 3600000 = 1 hour)
# Set to 0 to disable auto-sync
SYNC_INTERVAL_MS=3600000

# BigQuery/Intake Hub credentials (when real sync implemented)
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

---

## Running the Server

### Development Mode
```bash
node server.js
```

### With Environment Variables
```bash
PORT=8001 STORAGE_DIR=./storage node server.js
```

### Using npm script (if added to package.json)
```bash
npm start
```

### Health Check
```bash
curl http://localhost:8001/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "Projects Backend",
  "port": 8001,
  "storage": {
    "native_projects": 0,
    "bridged_projects": 0,
    "total_followers": 0,
    "last_sync": { ... }
  }
}
```

---

## API Endpoints

### Base URL
```
http://localhost:8001
```

### Projects Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | List all projects (with filters, pagination) |
| GET | `/api/projects/{id}` | Get project details |
| POST | `/api/projects` | Create new native project |
| PUT | `/api/projects/{id}` | Update native project |
| DELETE | `/api/projects/{id}` | Delete native project |

### Follower Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/projects/{id}/follow` | User follows project |
| DELETE | `/api/projects/{id}/follow` | User unfollows project |
| GET | `/api/projects/{id}/followers` | Get project followers & groups |

### Metrics Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/{id}/metrics` | Get project metrics from Project_Metric_Lift |

### Template Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/templates/{type}` | Get template definition |
| POST | `/api/templates/{type}/render` | Render template with project data |

### Sync Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sync/status` | Get sync status and stats |
| POST | `/api/sync/trigger` | Manually trigger sync |

---

## Example API Usage

### List Projects
```bash
curl "http://localhost:8001/api/projects?status=Active&limit=10&offset=0"
```

### Get Project Details
```bash
curl "http://localhost:8001/api/projects/PROJECT-123"
```

### Create Native Project
```bash
curl -X POST http://localhost:8001/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "NATIVE-001",
    "title": "Fashion Digital Touring",
    "owner": "Amanda Falkowski",
    "status": "Active",
    "phase": "Test"
  }'
```

### Follow a Project
```bash
curl -X POST http://localhost:8001/api/projects/PROJECT-123/follow \
  -H "Content-Type: application/json" \
  -d '{ "user_id": "user@walmart.com" }'
```

### Get Sync Status
```bash
curl "http://localhost:8001/api/sync/status"
```

---

## Data Bridge Integration

### How Intake Hub Data Flows

1. **Trigger Sync** → `/api/sync/trigger` called (manually or scheduled)
2. **Query Intake Hub** → Fetch from `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
3. **Map Columns** → Use `intake-hub-mapping.json` to align columns
4. **Transform** → Apply transformation functions (normalize status, dates, etc)
5. **Validate** → Check against `projects-schema.json`
6. **Cache** → Store in `storage/projects/bridged/intake-hub-cache.json`
7. **Track** → Record sync stats in `storage/projects/bridged/last-sync.json`
8. **Serve** → Frontend queries both native + bridged via `/api/projects`

### Sync Modes

**Scheduled Sync** (Default)
- Runs every `SYNC_INTERVAL_MS` (default 1 hour)
- Only syncs new/updated data (incremental)
- Non-blocking, runs in background

**On-Demand Sync**
- Frontend calls `/api/sync/trigger`
- Can be full or incremental based on query param
- Blocks until complete

**Transformation Functions**
- `resolve_project_id` - Use PROJECT_ID → Intake_Card → Facility-based fallback
- `normalize_status` - Map IH status values to canonical
- `normalize_phase` - Map IH phase values to canonical
- `normalize_market_3digit` - Pad market to 3 digits
- `parse_date` - Parse date from various formats

---

## Validation

### Schema Validation
Uses `Interface/Admin/Data-Bridge/Schemas/projects-schema.json` as source of truth

### Validation Rules
- **Required Fields**: Must be present, cannot be null/empty
- **Field Types**: string, integer, float, boolean, date, datetime, array, object
- **Constraints**: Enums, min/max length, min/max values, regex patterns
- **Transformations**: Applied to field values before storage

### Example Validation Error
```json
{
  "success": false,
  "errors": [
    "Missing required field: project_id",
    "title must be at least 1 characters",
    "status must be one of: Active, Archived, Pending, Cancelled, Complete"
  ]
}
```

---

## Storage Management

### Directory Structure
```
storage/
├── projects/
│   ├── native/          # User-created projects
│   └── bridged/         # Synced bridged projects
└── relationships/       # Followers and partner groups
```

### File Organization
- **Native projects** isolated from bridged for clear data provenance
- **Relationships** stored separately for flexible querying
- **Metadata** tracks creation dates, sync info, and audit trail
- **JSON format** for easy inspection and backup

### Migration from localStorage
When Phase 3 frontend refactoring begins:
- Frontend currently uses localStorage
- New frontend will use HTTP to call this backend API
- Old localStorage data can be imported via `/api/projects` POST endpoint

---

## Dependencies

See `package.json` for complete list. Key dependencies:

| Package | Purpose |
|---------|---------|
| `express` | Web framework |
| `cors` | Cross-origin support |
| `dotenv` | Environment variable loading |
| (Future) `@google-cloud/bigquery` | BigQuery client for real Intake Hub queries |

---

## Troubleshooting

### Port Already in Use
```bash
# Check what's using port 8001
netstat -ano | findstr ":8001"

# Kill existing process or change PORT
PORT=8002 node server.js
```

### Storage Directory Permissions
```bash
# Ensure storage directory is readable/writable
chmod -R 755 storage/
```

### Schema Not Found
```
Error: Failed to load projects schema
```
- Verify `Interface/Admin/Data-Bridge/Schemas/projects-schema.json` exists
- Check relative path in `projects-validator.js`

### Sync Failing
- Check BigQuery credentials are configured (when real sync implemented)
- Verify Intake Hub table exists and is accessible
- Check sync logs in console output

---

## Testing

### Unit Tests (TODO - Phase 2)
```bash
npm test
```

### Manual Testing via curl
See "Example API Usage" section above

### Integration Test
```bash
# 1. Check health
curl http://localhost:8001/health

# 2. Create sample project
curl -X POST http://localhost:8001/api/projects \
  -H "Content-Type: application/json" \
  -d '{"project_id":"TEST-1","title":"Test","owner":"Admin","status":"Active"}'

# 3. List projects
curl http://localhost:8001/api/projects

# 4. Verify storage created
ls -la storage/
```

---

## Development Roadmap

### Phase 1 ✅ (Current)
- ✅ Storage layer (native + bridged + relationships)
- ✅ Validator using schema
- ✅ Sync service structure
- ✅ API endpoints
- ✅ Basic server setup

### Phase 2 (Admin UI)
- Real BigQuery integration for Intake Hub
- Sync monitoring dashboard
- Admin configuration UI

### Phase 3 (Frontend)
- Update Interface/Projects to use this API
- Remove localStorage dependency
- Add frontend error handling

### Phase 4 (Features)
- Metrics integration from Project_Metric_Lift
- Template rendering and export
- Workflow integration for ownership changes

---

## References

- **Projects Schema**: `Interface/Admin/Data-Bridge/Schemas/projects-schema.json`
- **Intake Hub Mapping**: `Interface/Admin/Data-Bridge/Mappings/Projects/intake-hub-mapping.json`
- **Frontend Interface**: `Interface/Projects/`
- **Activity Hub Demo**: `Interface/For You - Landing Page/activity-hub-demo.html`

---

## Support & Next Steps

**For Questions**:
- Review plan in `/memories/session/plan.md`
- Check schema definitions in Admin/Data-Bridge
- Examine example payloads in this README

**Next Phase**:
- Implement real BigQuery integration
- Build Admin UI for Projects configuration
- Test with real Intake Hub data
- Deploy to staging environment

---

**Last Updated**: March 20, 2026  
**Implemented By**: Phase 1 Implementation  
**Status**: Ready for Phase 2 Admin Integration
