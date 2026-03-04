# TDA Insights Dashboard - API Reference

## Base URL

```
http://localhost:5000/api
```

## Authentication

None (local deployment). For production, implement OAuth2 or API keys.

## Rate Limiting

None (local deployment). For production, implement rate limiting.

## Response Format

All endpoints return JSON:

```json
{
  "success": true,
  "data": {},
  "timestamp": "2026-03-03T10:30:00.000000",
  "message": "Optional message"
}
```

---

## Health & Status Endpoints

### GET /api/health

Health check endpoint to verify backend is running.

**Request:**
```bash
curl http://localhost:5000/api/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-03T10:30:00.000000",
  "bigquery_connected": true
}
```

**Use Case:** Monitor dashboard availability

---

## Data Endpoints

### GET /api/data

Retrieve TDA initiative data with optional filtering.

**Parameters:**
| Parameter | Type | Required | Description |
|---|---|---|---|
| `phase` | string | No | Filter by phase (e.g., "Test", "Production"). Use "All" for all phases. |
| `health_status` | string | No | Filter by health status (e.g., "On Track", "At Risk", "Off Track") |
| `refresh` | bool | No | Force refresh from BigQuery, bypass cache |

**Request:**
```bash
# Get all data
curl http://localhost:5000/api/data

# Filter by phase
curl "http://localhost:5000/api/data?phase=Test"

# Filter by health status
curl "http://localhost:5000/api/data?health_status=On%20Track"

# Both filters
curl "http://localhost:5000/api/data?phase=Test&health_status=At%20Risk"

# Force refresh
curl "http://localhost:5000/api/data?refresh=true"
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 45,
  "phase": "Test",
  "health_status": "All",
  "data": [
    {
      "Initiative - Project Title": "Sidekick Enhancement",
      "Health Status": "On Track",
      "Phase": "Test",
      "# of Stores": 120,
      "Intake & Testing": "In Progress",
      "Dallas POC": "John Smith",
      "Deployment": "Scheduled"
    },
    ...
  ],
  "timestamp": "2026-03-03T10:30:00.000000"
}
```

**Status Codes:**
| Code | Meaning |
|---|---|
| 200 | Success |
| 400 | Invalid parameters |
| 500 | Server error (check BigQuery connection) |

**Use Case:** Get filtered initiative data

---

### GET /api/phases

Get list of all unique phases in the dataset.

**Request:**
```bash
curl http://localhost:5000/api/phases
```

**Response (200 OK):**
```json
{
  "success": true,
  "phases": [
    "Planning",
    "Test",
    "Pilot",
    "Production",
    "Rollback"
  ],
  "timestamp": "2026-03-03T10:30:00.000000"
}
```

**Use Case:** Populate filter dropdowns

---

### GET /api/health-statuses

Get list of all unique health statuses in the dataset.

**Request:**
```bash
curl http://localhost:5000/api/health-statuses
```

**Response (200 OK):**
```json
{
  "success": true,
  "health_statuses": [
    "On Track",
    "At Risk",
    "Off Track"
  ],
  "timestamp": "2026-03-03T10:30:00.000000"
}
```

**Use Case:** Populate health status filter dropdown

---

### GET /api/summary

Get summary statistics for current data view.

**Parameters:**
| Parameter | Type | Description |
|---|---|---|
| `phase` | string | (Optional) Filter by phase |
| `health_status` | string | (Optional) Filter by health status |

**Request:**
```bash
# Overall summary
curl http://localhost:5000/api/summary

# Summary for specific phase
curl "http://localhost:5000/api/summary?phase=Test"

# Summary for specific health status
curl "http://localhost:5000/api/summary?health_status=At%20Risk"

# Both filters
curl "http://localhost:5000/api/summary?phase=Test&health_status=On%20Track"
```

**Response (200 OK):**
```json
{
  "success": true,
  "summary": {
    "total_projects": 45,
    "total_stores": 3200,
    "by_health_status": {
      "On Track": 35,
      "At Risk": 8,
      "Off Track": 2
    },
    "by_phase": {
      "Test": 20,
      "Production": 25
    }
  },
  "timestamp": "2026-03-03T10:30:00.000000"
}
```

**Use Case:** Display summary cards on dashboard

---

### GET /api/export/csv

Export filtered data as CSV format.

**Parameters:**
| Parameter | Type | Description |
|---|---|---|
| `phase` | string | (Optional) Filter by phase |
| `health_status` | string | (Optional) Filter by health status |

**Request:**
```bash
# Export all data
curl http://localhost:5000/api/export/csv > initiatives.csv

# Export filtered data
curl "http://localhost:5000/api/export/csv?phase=Test" > test_initiatives.csv
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "CSV export ready",
  "data": "\"Initiative - Project Title\",\"Health Status\",...\n\"Sidekick\"...\n"
}
```

**Use Case:** Download data for external analysis

---

## PowerPoint Generation Endpoints

### POST /api/ppt/generate

Generate a PowerPoint report with initiative data.

**Request Body:**
```json
{
  "phases": ["Test", "Production"],  // Optional: specific phases
  "force_regenerate": false          // Optional: force new generation
}
```

**Request:**
```bash
# Generate report for all phases
curl -X POST http://localhost:5000/api/ppt/generate \
  -H "Content-Type: application/json" \
  -d '{}'

# Generate report for specific phases
curl -X POST http://localhost:5000/api/ppt/generate \
  -H "Content-Type: application/json" \
  -d '{"phases": ["Test"]}'

# Force regenerate (bypass cache)
curl -X POST http://localhost:5000/api/ppt/generate \
  -H "Content-Type: application/json" \
  -d '{"force_regenerate": true}'
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Report generated successfully",
  "file_path": "reports/TDA_Report_20260303_103000.pptx",
  "file_name": "TDA_Report_20260303_103000.pptx",
  "timestamp": "2026-03-03T10:30:00.000000"
}
```

**Response (500 Error):**
```json
{
  "success": false,
  "message": "Error: No data available for report generation",
  "timestamp": "2026-03-03T10:30:00.000000"
}
```

**Use Case:** Generate executive-ready PowerPoint presentations

**Report Contents:**
- Title slide
- Summary slide
- Phase-based slides (one per phase)
- Statistics and color-coded status
- Professional Walmart branding

---

### GET /api/ppt/download/:filename

Download a previously generated PowerPoint report.

**Parameters:**
| Parameter | Type | Required | Description |
|---|---|---|---|
| `filename` | string | Yes | Name of PPT file to download |

**Request:**
```bash
curl -O http://localhost:5000/api/ppt/download/TDA_Report_20260303_103000.pptx
```

**Response (200 OK):**
Binary file (application/vnd.openxmlformats-officedocument.presentationml.presentation)

**Response (404 Not Found):**
```json
{
  "error": "File not found"
}
```

**Use Case:** Download generated reports

---

### GET /api/ppt/list

List all previously generated PowerPoint reports.

**Request:**
```bash
curl http://localhost:5000/api/ppt/list
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 3,
  "reports": [
    {
      "filename": "TDA_Report_20260303_103000.pptx",
      "size": 2048576,
      "created": "2026-03-03T10:30:00.000000",
      "modified": "2026-03-03T10:30:00.000000"
    },
    {
      "filename": "TDA_Report_20260302_150000.pptx",
      "size": 2045342,
      "created": "2026-03-02T15:00:00.000000",
      "modified": "2026-03-02T15:00:00.000000"
    }
  ],
  "timestamp": "2026-03-03T10:30:00.000000"
}
```

**Use Case:** Show list of available reports to download

---

### DELETE /api/ppt/delete/:filename

Delete a previously generated PowerPoint report.

**Parameters:**
| Parameter | Type | Required | Description |
|---|---|---|---|
| `filename` | string | Yes | Name of PPT file to delete |

**Request:**
```bash
curl -X DELETE http://localhost:5000/api/ppt/delete/TDA_Report_20260303_103000.pptx
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Report deleted: TDA_Report_20260303_103000.pptx",
  "timestamp": "2026-03-03T10:30:00.000000"
}
```

**Response (404 Not Found):**
```json
{
  "error": "File not found"
}
```

**Use Case:** Clean up old/unused reports

---

### GET /api/ppt/status

Get status of PPT generation service.

**Request:**
```bash
curl http://localhost:5000/api/ppt/status
```

**Response (200 OK):**
```json
{
  "success": true,
  "service": "TDA PPT Report Generator",
  "status": "operational",
  "output_directory": "c:\\...\\TDA Insights\\reports",
  "reports_directory_exists": true,
  "last_report_path": "c:\\...\\TDA_Report_20260303_103000.pptx",
  "last_report_time": "2026-03-03T10:30:00.000000",
  "timestamp": "2026-03-03T10:30:00.000000"
}
```

**Use Case:** Monitor report generation service health

---

## Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "success": false,
  "error": "Invalid parameters",
  "timestamp": "2026-03-03T10:30:00.000000"
}
```

**500 Internal Server Error:**
```json
{
  "success": false,
  "error": "BigQuery connection failed",
  "timestamp": "2026-03-03T10:30:00.000000"
}
```

### Troubleshooting

| Error | Cause | Solution |
|---|---|---|
| "BigQuery connection failed" | Credentials not set | Run `gcloud auth application-default login` |
| "No data found" | Wrong table name | Verify `Output_TDA Report` table exists |
| "Port 5000 in use" | Another process using port | Kill process or use different PORT |
| "File not found" | Report doesn't exist | Check filename, run `/api/ppt/list` |

---

## Rate Limiting & Caching

### Caching Strategy
- **Data Cache:** 5 minutes TTL for BigQuery queries
- **PPT Cache:** 5 minutes for generated reports
- **Force Refresh:** Use `?refresh=true` to bypass cache

### Timeouts
- **BigQuery Query:** 30 seconds default
- **HTTP Request:** 60 seconds default
- **PPT Generation:** 60 seconds default

---

## Example Workflows

### 1. Load Dashboard Data

```bash
# 1. Get available phases
curl http://localhost:5000/api/phases

# 2. Get available health statuses
curl http://localhost:5000/api/health-statuses

# 3. Get all data (or filtered)
curl "http://localhost:5000/api/data?phase=Test"

# 4. Get summary statistics
curl "http://localhost:5000/api/summary?phase=Test"
```

### 2. Generate & Download Report

```bash
# 1. Generate new report
curl -X POST http://localhost:5000/api/ppt/generate \
  -H "Content-Type: application/json" \
  -d '{"phases": ["Test"]}'

# 2. Extract filename from response
FILENAME="TDA_Report_20260303_103000.pptx"

# 3. Download report
curl -O http://localhost:5000/api/ppt/download/$FILENAME
```

### 3. Export Data

```bash
# Export filtered data as CSV
curl "http://localhost:5000/api/export/csv?phase=Test&health_status=At%20Risk" > at_risk.csv

# Open in Excel
start at_risk.csv
```

### 4. Monitor Service

```bash
# Check health
curl http://localhost:5000/api/health

# Check PPT service
curl http://localhost:5000/api/ppt/status

# List available reports
curl http://localhost:5000/api/ppt/list
```

---

## Integration Examples

### Python

```python
import requests
import json

API_BASE = "http://localhost:5000/api"

# Get data
response = requests.get(f"{API_BASE}/data")
data = response.json()
print(f"Found {data['count']} initiatives")

# Generate report
response = requests.post(
    f"{API_BASE}/ppt/generate",
    json={"phases": ["Test"]}
)
if response.json()['success']:
    print("Report generated!")
```

### JavaScript

```javascript
const API_BASE = "http://localhost:5000/api";

// Get data
fetch(`${API_BASE}/data?phase=Test`)
  .then(r => r.json())
  .then(data => {
    console.log(`Found ${data.count} initiatives`);
    console.table(data.data);
  });

// Generate report
fetch(`${API_BASE}/ppt/generate`, {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({phases: ["Test"]})
})
.then(r => r.json())
.then(result => console.log(result));
```

### cURL

```bash
# Alias for easy API calls
alias tda='function() { curl -s "http://localhost:5000/api/$1" | jq . ; }; function'

# Use alias
tda health
tda data
tda "data?phase=Test"
```

---

## Performance Metrics

**Average Response Times:**
- `/api/data` - 200-500ms (BigQuery query)
- `/api/phases` - 50-100ms (cached)
- `/api/summary` - 100-300ms (calculated data)
- `/api/ppt/generate` - 2000-5000ms (generation)
- `/api/ppt/download` - 100-500ms (file download)

---

## Future API Enhancements

- [ ] Field-level filtering
- [ ] Custom date ranges
- [ ] Advanced search syntax
- [ ] Pagination/limit support
- [ ] GraphQL endpoint
- [ ] WebSocket real-time updates
- [ ] Batch operations
- [ ] API versioning

---

For more information, see [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)
