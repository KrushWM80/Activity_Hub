# 🔌 API Datasources

## Overview

Activity Hub integrates with several external and internal APIs to provide real-time data access and services. This document covers all API integrations, authentication methods, and usage patterns.

---

## API Integrations Overview

| API | Type | Purpose | Authentication | Frequency |
|---|---|---|---|---|
| **Workday** | External | HR data, employee profiles, job codes | Service Account | Daily |
| **Active Directory** | Internal/Azure | User authentication, group membership | OAuth 2.0 | Real-time |
| **Microsoft Graph** | External | Teams, Outlook, Calendar, SharePoint | OAuth 2.0 Service Account | Real-time |
| **Sparky AI** | Internal | AI query processing, natural language | API Key | Real-time |
| **REST APIs** | Custom | Project data, custom integrations | Various | As needed |

---

## 1. 🏢 Workday HR System API

### Purpose
Provides employee HR data, job title mappings, organizational structure, and employee profiles.

### Used By
- `General Setup/Distribution_Lists/` - Job code lookups
- `Store Support/` - Employee information
- `Interface/Admin/` - User management

### Endpoints

```
Base URL: https://api.workday.com/v1/

GET  /employees/{employee_id}      - Get employee details
GET  /jobs/{job_code}              - Get job descriptions
GET  /departments/{dept_id}        - Get department info
GET  /locations/{location_id}      - Get facility locations
```

### Authentication
```
Method: Workday Service Account OAuth
Client ID: [Stored in Azure Key Vault]
Client Secret: [Stored in Azure Key Vault]
Scope: HR API, Organization Management
```

### Python Example
```python
import requests
from typing import Dict, Optional

class WorkdayAPI:
    def __init__(self, client_id: str, client_secret: str):
        self.base_url = "https://api.workday.com/v1"
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
    
    def get_token(self) -> str:
        """Get OAuth2 access token"""
        auth_url = "https://workday.auth.oauth.com/token"
        response = requests.post(auth_url, data={
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        })
        self.token = response.json()['access_token']
        return self.token
    
    def get_employee(self, employee_id: str) -> Dict:
        """Get employee details"""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(
            f"{self.base_url}/employees/{employee_id}",
            headers=headers
        )
        return response.json()
    
    def get_job_info(self, job_code: str) -> Dict:
        """Get job title and description"""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(
            f"{self.base_url}/jobs/{job_code}",
            headers=headers
        )
        return response.json()
```

### Response Example
```json
{
    "id": "e1001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@walmart.com",
    "job_code": "2000",
    "job_title": "Sales Associate",
    "department": "Merchandise",
    "location": "1497",
    "location_name": "Store 1497 - Rogers, AR",
    "hire_date": "2022-01-15",
    "status": "active"
}
```

### Error Handling
```python
try:
    employee = workday_api.get_employee('e1001')
except requests.exceptions.Timeout:
    print("Request timed out - retry with backoff")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Invalid credentials - refresh token")
    elif e.response.status_code == 404:
        print("Employee not found")
```

### Files Using This
- [workday_job_lookup.py](../../Distribution_Lists/02_SCRIPTS_AND_TOOLS/workday_job_lookup.py)

---

## 2. 🔐 Microsoft Active Directory API

### Purpose
Manages user authentication, group membership, and access control across Activity Hub.

### Used By
- `Interface/Admin/` - User and group management
- All modules - Authentication and authorization
- `General Setup/` - Access control setup

### Endpoints

```
Base URL: https://graph.microsoft.com/v1.0/

GET    /me                              - Current user info
GET    /me/memberOf                     - User's groups
GET    /groups/{id}/members             - Group members
GET    /directoryObjects/{id}           - Directory object details
POST   /groups/{id}/members/$ref        - Add member to group
DELETE /groups/{id}/members/{id}/$ref   - Remove member from group
```

### Authentication
```
Method: Azure AD OAuth 2.0
Tenant: wmt-assetprotection.onmicrosoft.com
Client ID: [Stored in Azure Key Vault]
Client Secret: [Stored in Azure Key Vault]
Scope: Directory.Read.All, Directory.ReadWrite.All
```

### JavaScript Example
```javascript
const { Client } = require('@microsoft/microsoft-graph-client');

class ActiveDirectoryManager {
    constructor(token) {
        this.client = Client.init({
            authProvider: (done) => {
                done(null, token);
            }
        });
    }
    
    async getCurrentUser() {
        return await this.client.api('/me').get();
    }
    
    async getUserGroups(userId) {
        return await this.client.api(`/users/${userId}/memberOf`).get();
    }
    
    async getGroupMembers(groupId) {
        return await this.client.api(`/groups/${groupId}/members`).get();
    }
    
    async addUserToGroup(groupId, userId) {
        const body = {
            "@odata.id": `https://graph.microsoft.com/v1.0/users/${userId}`
        };
        return await this.client.api(`/groups/${groupId}/members/$ref`)
            .post(body);
    }
}
```

### Response Example
```json
{
    "id": "4c3e1234-1234-1234-1234-123456789012",
    "displayName": "Store Support Admins",
    "description": "Users with admin access to Store Support modules"
}
```

### AD Groups Used by Activity Hub
```
Group Name                           Purpose
------------------------------------------------------
activity-hub-admins                  System administrators
activity-hub-managers                Department managers
activity-hub-project-leads           Project management
activity-hub-store-support           Store support team
activity-hub-intake-hub              Intake hub users
store-refresh-team                   Store refresh guide users
```

### Files Using This
- [access-groups.json](../../Admin/access-groups.json)
- [role-configuration.json](../../Admin/role-configuration.json)

---

## 3. 📧 Microsoft Graph API

### Purpose
Integrates Microsoft 365 services: Teams, Outlook, Calendar, SharePoint, OneDrive.

### Used By
- `Interface/Notifications/` - Teams notifications
- `Interface/Settings/` - Outlook calendar sync
- `Store Support/` - SharePoint document access

### Endpoints

```
Teams:
GET  /me/joinedTeams                   - User's teams
GET  /teams/{id}/channels              - Team channels
POST /teams/{id}/channels/{id}/messages - Send message

Calendar:
GET  /me/calendar/events               - User's events
POST /me/events                        - Create event
GET  /me/events?$filter=start eq '2026-02-25' - Day's events

Email:
GET  /me/messages                      - User's emails
POST /me/sendMail                      - Send email
GET  /me/mailFolders                   - Email folders

SharePoint:
GET  /sites/{id}/lists                 - Site lists
GET  /drives/{id}/items                - Drive files
POST /sites/{id}/lists/{id}/items      - Create list item
```

### Authentication
```
Method: Azure AD OAuth 2.0 (Service Account)
Scope: Team.ReadWrite.All, Calendars.ReadWrite, Mail.Send
Token Refresh: Automatic (every 60 minutes)
```

### Python Example
```python
import msal
from msgraph.core import GraphClient

class MicrosoftGraphManager:
    def __init__(self, client_id: str, client_secret: str, tenant_id: str):
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        self.client_id = client_id
        self.client_secret = client_secret
        self.graph_client = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Microsoft Graph"""
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        token = app.acquire_token_for_client(
            scopes=["https://graph.microsoft.com/.default"]
        )
        self.graph_client = GraphClient(
            credential=token['access_token']
        )
    
    def send_teams_message(self, team_id: str, channel_id: str, message: str):
        """Send message to Teams channel"""
        body = {
            "body": {"content": message}
        }
        endpoint = f"/teams/{team_id}/channels/{channel_id}/messages"
        return self.graph_client.post(endpoint, data=body)
    
    def create_calendar_event(self, subject: str, start: str, end: str):
        """Create calendar event"""
        event = {
            "subject": subject,
            "start": {"dateTime": start, "timeZone": "Central Time"},
            "end": {"dateTime": end, "timeZone": "Central Time"}
        }
        return self.graph_client.post("/me/events", data=event)
```

### Usage Examples

**Send Teams Notification**:
```python
manager.send_teams_message(
    team_id="a1b2c3d4",
    channel_id="x9y8z7w6",
    message="Project status updated: On track for Q1 release"
)
```

**Create Calendar Event**:
```python
manager.create_calendar_event(
    subject="Project Kickoff Meeting",
    start="2026-03-01T10:00:00",
    end="2026-03-01T11:00:00"
)
```

---

## 4. 🤖 Sparky AI API

### Purpose
Provides AI-powered query processing, natural language understanding, and intelligent recommendations.

### Used By
- `Platform/Sparky AI/` - AI assistant
- `Interface/Projects/` - AI features
- Various dashboards - Smart recommendations

### Endpoints

```
POST /api/v1/assistant/query           - Process natural language query
POST /api/v1/assistant/chat             - Multi-turn conversation
GET  /api/v1/assistant/capabilities     - Available AI features
POST /api/v1/assistant/feedback         - Feedback on responses
```

### Authentication
```
Method: API Key (Bearer Token)
Header: Authorization: Bearer {API_KEY}
Key Location: Environment variable SPARKY_API_KEY
Rate Limit: 1000 requests/minute
```

### Request Format
```json
{
    "query": "What are the top performing stores in the Southwest region?",
    "context": {
        "user_role": "manager",
        "store_filters": ["region:Southwest"],
        "time_range": "last_30_days"
    },
    "include_reasoning": true,
    "response_format": "json"
}
```

### Response Format
```json
{
    "status": "success",
    "response": {
        "summary": "Top 5 stores in Southwest region by sales...",
        "data": [
            {"store_id": "1497", "sales": "$2.1M", "growth": "12.5%"},
            {"store_id": "1502", "sales": "$1.9M", "growth": "8.2%"}
        ],
        "confidence_score": 0.95,
        "reasoning": "Based on sales data from last 30 days..."
    },
    "alternatives": [
        {"query": "Top performing stores by..."}
    ]
}
```

### Python Client
```python
import requests
import json

class SparkyAIClient:
    def __init__(self, api_key: str):
        self.base_url = "https://sparky-api.walmart.com/api/v1"
        self.api_key = api_key
    
    def query(self, query: str, context: dict = None) -> dict:
        """Submit query to Sparky AI"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'query': query,
            'context': context or {}
        }
        response = requests.post(
            f"{self.base_url}/assistant/query",
            headers=headers,
            json=payload
        )
        return response.json()
```

### Files Using This
- [ai_agent.py](../../Projects/Intake%20Hub/ProjectsinStores/backend/ai_agent.py)
- [Platform/Sparky AI/INTEGRATION_GUIDE.md](../../../Platform/Sparky%20AI/INTEGRATION_GUIDE.md)

---

## 5. 📱 REST API Integrations

### Generic REST API Connection

Activity Hub supports connecting to custom REST APIs for data import and sync.

### Configuration
```javascript
{
    "api_name": "My Custom API",
    "endpoint": "https://api.example.com/projects",
    "method": "GET",
    "authentication": {
        "type": "bearer", // "none", "api_key", "bearer", "basic"
        "token": "your-token-here"
    },
    "sync": {
        "enabled": true,
        "frequency": "daily", // "hourly", "daily", "weekly"
        "direction": "pull" // "pull", "push", "bidirectional"
    }
}
```

### Usage in Projects
See: [Upload Projects/Interface](../../../Interface/Projects/Upload%20Projects/)

---

## 🔄 API Sync Schedule

| API | Frequency | Time | Purpose | Fallback |
|---|---|---|---|---|
| Workday | Daily | 2:00 AM | HR data refresh | Last known data (24h) |
| Active Directory | Real-time | On-demand | Auth & access | Local cache (5 min TTL) |
| MS Graph | Real-time | Event-based | Notifications, Calendar | Queued until restored |
| Sparky AI | Real-time | On-demand | Queries | Error message + suggestions |

---

## ❌ Common API Issues & Solutions

### Issue 1: Authentication Failures (401/403)
```
Cause: Token expired or invalid credentials
Solution:
1. Check credentials in Azure Key Vault
2. Verify token refresh is working
3. Ensure scopes are correct for the endpoint
```

### Issue 2: Rate Limiting (429)
```
Cause: Too many requests
Solution:
1. Implement exponential backoff retry
2. Use batch endpoints if available
3. Query API limits: /api/v1/limits
```

### Issue 3: Timeout Errors (504)
```
Cause: API slow or down
Solution:
1. Check API status page
2. Increase timeout from 30s to 60s
3. Use caching for non-real-time data
```

### Issue 4: Invalid Response Data (422)
```
Cause: Schema mismatch
Solution:
1. Validate response with JSON schema
2. Log full response for debugging
3. Check API version and documentation
```

---

## 🛠️ API Best Practices

### 1. Always Implement Retry Logic
```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session
```

### 2. Use Caching for Non-Real-Time Data
```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=128)
def get_employee_cached(emp_id: str, cache_key: str):
    """Cache employee data for 5 minutes"""
    return workday_api.get_employee(emp_id)
```

### 3. Log All API Calls
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"API Call: {method} {endpoint}")
logger.info(f"Response: {status_code}, {response_time}ms")
```

### 4. Validate Responses
```python
from jsonschema import validate

def validate_employee_response(data):
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "email": {"type": "string"},
            "status": {"type": "string"}
        },
        "required": ["id", "email"]
    }
    validate(instance=data, schema=schema)
```

---

## 📞 Support & Documentation

- **Workday**: https://www.workday.com/en-us/solutions/api
- **AD/Graph**: https://docs.microsoft.com/en-us/graph/
- **Sparky AI**: See [INTEGRATION_GUIDE.md](../../../Platform/Sparky%20AI/INTEGRATION_GUIDE.md)
- **Status**: Check individual service status pages

