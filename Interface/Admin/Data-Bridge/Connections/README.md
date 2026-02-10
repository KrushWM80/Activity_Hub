# Data Bridge Connections

This folder stores saved connection configurations for external data sources.

## Connection Types

### BigQuery Connections
Configuration for Google BigQuery data sources.

```json
{
  "id": "conn_bq_123",
  "name": "Intake Hub Production",
  "type": "bigquery",
  "config": {
    "projectId": "your-gcp-project",
    "dataset": "your_dataset",
    "table": "your_table"
  },
  "createdAt": "2025-01-15T...",
  "lastUsed": "2025-01-16T..."
}
```

### API Connections
Configuration for REST API data sources.

```json
{
  "id": "conn_api_456",
  "name": "External Projects API",
  "type": "api",
  "config": {
    "endpoint": "https://api.example.com/projects",
    "method": "GET",
    "authType": "bearer",
    "syncEnabled": true,
    "syncDirection": "bidirectional",
    "syncFrequency": "daily"
  },
  "createdAt": "2025-01-15T...",
  "lastUsed": "2025-01-16T..."
}
```

## Storage

Connections are stored in the browser's localStorage under the key `activity_hub_connections`. In a production environment, sensitive credentials should be:

1. Stored server-side or in secure vaults
2. Never exposed in client-side code
3. Encrypted at rest

## Sync Configuration

For API connections with sync enabled:

| Property | Description |
|----------|-------------|
| `syncEnabled` | Whether automatic sync is active |
| `syncDirection` | `pull`, `push`, or `bidirectional` |
| `syncFrequency` | `realtime`, `hourly`, `daily`, `weekly`, or `manual` |
| `conflictResolution` | `source_wins`, `activity_hub_wins`, or `manual` |
| `lastSync` | Timestamp of last successful sync |

## Security Notes

- Service account keys for BigQuery should never be stored in this folder
- API tokens and passwords are stored in localStorage (demo only)
- Production implementations should use OAuth flows and secure token storage
