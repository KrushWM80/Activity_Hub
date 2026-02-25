# 🗄️ Database Datasources

## Overview

Activity Hub uses relational databases for storing application data, project information, user preferences, and operational metadata. These databases provide structured, persistent storage with ACID compliance.

---

## Database Systems Used

| Database | Purpose | Used By | Backup | Encryption |
|---|---|---|---|---|
| **PostgreSQL** | Primary application database | All modules | Daily | SSL/TLS + at-rest |
| **Redis** | Caching, session storage | Backend services | Real-time replica | In-transit only |

---

## 1. 🐘 PostgreSQL Database

### Purpose
Central relational database for Activity Hub storing projects, users, configurations, and operational data.

### Connection Details

```
Host: db.assetprotection-prod.walmart.com
Port: 5432
Database: activity_hub_prod
User: app_user (read-only)
        app_admin (admin operations)
SSL: Required (TLS 1.2+)
```

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role_id UUID REFERENCES roles(role_id),
    ad_group_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

#### Projects Table
```sql
CREATE TABLE projects (
    project_id UUID PRIMARY KEY,
    project_title VARCHAR(255) NOT NULL,
    project_description TEXT,
    status VARCHAR(50) NOT NULL, -- Active, Pending, Completed, On Hold
    owner_id UUID REFERENCES users(user_id),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12, 2),
    priority VARCHAR(20), -- High, Medium, Low
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Store Assignments Table
```sql
CREATE TABLE project_store_assignments (
    assignment_id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(project_id),
    store_number INTEGER NOT NULL,
    store_name VARCHAR(255),
    region VARCHAR(100),
    market VARCHAR(100),
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_date DATE
);
```

#### Activities/Events Table
```sql
CREATE TABLE project_activities (
    activity_id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(project_id),
    activity_type VARCHAR(100), -- Update, Completion, Risk, Delay
    description TEXT,
    created_by UUID REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attachments JSONB
);
```

#### User Preferences Table
```sql
CREATE TABLE user_preferences (
    preference_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    widget_layout JSONB,
    theme VARCHAR(50), -- light, dark, system
    notifications_enabled BOOLEAN DEFAULT TRUE,
    preferred_view VARCHAR(50), -- list, grid, kanban
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Audit Log Table
```sql
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    action VARCHAR(255),
    table_name VARCHAR(255),
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Python Connection Examples

#### Using psycopg2 (Low-level)
```python
import psycopg2
from psycopg2.extras import RealDictCursor

class PostgreSQLConnection:
    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(connection_string)
    
    def query_projects(self, owner_email: str) -> list:
        """Get projects for a user"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT p.* FROM projects p
                JOIN users u ON p.owner_id = u.user_id
                WHERE u.email = %s
                ORDER BY p.created_at DESC
            """, (owner_email,))
            return cur.fetchall()
    
    def insert_project(self, title: str, owner_id: str, budget: float) -> str:
        """Create new project"""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO projects (project_id, project_title, owner_id, budget, status)
                VALUES (gen_random_uuid(), %s, %s, %s, 'Pending')
                RETURNING project_id
            """, (title, owner_id, budget))
            self.conn.commit()
            return cur.fetchone()[0]
```

#### Using SQLAlchemy (ORM)
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    
    project_id = Column(String, primary_key=True)
    project_title = Column(String)
    status = Column(String)
    owner_id = Column(String, ForeignKey("users.user_id"))
    budget = Column(Float)

# Connection
engine = create_engine(
    "postgresql://user:password@host:5432/activity_hub_prod",
    echo=False,
    sslmode="require"
)

# Query
with Session(engine) as session:
    projects = session.query(Project).filter(
        Project.status == "Active"
    ).all()
```

### Indexing Strategy

```sql
-- Performance indexes
CREATE INDEX idx_projects_owner_id ON projects(owner_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_project_activities_project_id ON project_activities(project_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_project_store_assignments_store_number 
    ON project_store_assignments(store_number);

-- For time-series queries
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
```

### Backup & Recovery

```
Backup Schedule: Daily at 2:00 AM CT
Retention: 30 days
Recovery Time Objective (RTO): 4 hours
Recovery Point Objective (RPO): 1 hour
Backup Location: Azure Blob Storage (replicated across regions)
```

---

## 2. 🚀 Redis Cache

### Purpose
High-performance caching layer for frequently accessed data, session management, and real-time features.

### Connection Details
```
Host: cache.assetprotection-prod.walmart.com
Port: 6379
SSL: Required (TLS)
Auth: Redis ACL with username/password
Database: 0 (primary), 1-15 available for different uses
```

### Cache Strategy

#### Session Cache
```python
import redis
import json
from datetime import timedelta

class SessionCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='cache.assetprotection-prod.walmart.com',
            port=6379,
            decode_responses=True,
            ssl=True
        )
    
    def store_session(self, user_id: str, session_data: dict):
        """Store user session"""
        key = f"session:{user_id}"
        self.redis_client.setex(
            key,
            timedelta(hours=8),
            json.dumps(session_data)
        )
    
    def get_session(self, user_id: str) -> dict:
        """Retrieve session"""
        key = f"session:{user_id}"
        data = self.redis_client.get(key)
        return json.loads(data) if data else None
```

#### Data Cache
```python
class DataCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='cache.assetprotection-prod.walmart.com',
            port=6379,
            decode_responses=True
    )
    
    def cache_projects(self, user_id: str, projects: list):
        """Cache user's projects"""
        key = f"projects:{user_id}"
        self.redis_client.setex(
            key,
            timedelta(hours=1),
            json.dumps(projects)
        )
    
    def get_cached_projects(self, user_id: str) -> list:
        """Get cached projects"""
        key = f"projects:{user_id}"
        data = self.redis_client.get(key)
        return json.loads(data) if data else None
    
    def invalidate_cache(self, user_id: str):
        """Clear user's project cache"""
        key = f"projects:{user_id}"
        self.redis_client.delete(key)
```

### Cache Key Patterns

```
Pattern: service:entity:identifier:version

Examples:
- session:user:abc-123
- projects:user:xyz-789
- stores:region:central
- teams:manager:john.doe
- filter_options:module:intake-hub
- bigquery:table:polaris_schedule:v1
```

### TTL Strategy

| Cache Type | TTL | Invalidation |
|---|---|---|
| Session | 8 hours | On logout, token refresh |
| User Data | 15 minutes | On update |
| Projects List | 1 hour | On project change |
| Store Data | 24 hours | Daily refresh |
| Filter Options | 6 hours | On data update |
| Search Results | 5 minutes | Sliding window |

---

## 3. Connection Strings & Configuration

### Development Environment
```
postgresql://dev_user:dev_password@localhost:5432/activity_hub_dev
redis://localhost:6379/0
```

### Staging Environment
```
postgresql://stage_user:PASSWORD@staging-db.walmart.com:5432/activity_hub_stage
redis://staging-cache.walmart.com:6379/0
```

### Production Environment
```
postgresql://app_user:PASSWORD@db.assetprotection-prod.walmart.com:5432/activity_hub_prod
redis://cache.assetprotection-prod.walmart.com:6379/0
```

**Note**: All passwords stored in Azure Key Vault. Retrieved at runtime.

### Environment Configuration
```python
import os
from urllib.parse import quote_plus

# Read from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Build connection string
CONNECTION_STRING = f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:5432/{DB_NAME}?sslmode=require"

# Redis connection
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

REDIS_URL = f"redis://:{quote_plus(REDIS_PASSWORD)}@{REDIS_HOST}:{REDIS_PORT}/0?ssl=True"
```

---

## 🔒 Security

### Access Control
```sql
-- Read-only user (application)
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- Admin user (migrations, schema changes)
CREATE USER app_admin WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE activity_hub_prod TO app_admin;

-- Analytics user (reporting)
CREATE USER analytics_user WITH PASSWORD 'secure_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_user;
```

### Encryption

**In Transit**:
- SSL/TLS 1.2+ required for all connections
- Certificate pinning in production clients

**At Rest**:
- Database: Transparent Data Encryption (TDE)
- Redis: Encryption at rest enabled
- Backups: AES-256 encryption

---

## 🚨 Monitoring & Alerts

### Key Metrics
```python
# Monitor connection pool
- Active connections
- Idle connections
- Connection timeouts

# Monitor performance
- Query response time (p50, p95, p99)
- Slow query log (> 1 second)
- Lock waits

# Monitor cache
- Hit rate (target: > 80%)
- Memory usage
- Eviction rate
```

### Alert Thresholds
```
- Connection pool > 90% utilized: Alert
- Query response p95 > 500ms: Alert
- Redis memory > 80% of max: Warning
- Cache hit rate < 70%: Investigation
```

---

## ❌ Common Issues & Solutions

### Issue 1: Connection Pool Exhausted
```
Error: "too many connections"
Cause: Connections not being returned to pool
Solution:
1. Check for unclosed connections in code
2. Increase pool size if needed
3. Add connection timeout monitoring
```

### Issue 2: Slow Queries
```
Error: Query taking > 5 seconds
Cause: Missing indexes or inefficient query
Solution:
1. Check EXPLAIN ANALYZE output
2. Add indexes on frequently filtered columns
3. Rewrite query for better performance
```

### Issue 3: Cache Invalidation Issues
```
Problem: Stale data being served
Cause: Cache not being invalidated on updates
Solution:
1. Implement proper invalidation logic
2. Add event-based cache clearing
3. Monitor cache hit rates
```

---

## 🛠️ Common Queries

### Find Active Projects
```sql
SELECT p.project_id, p.project_title, COUNT(psa.assignment_id) as store_count
FROM projects p
LEFT JOIN project_store_assignments psa ON p.project_id = psa.project_id
WHERE p.status = 'Active'
GROUP BY p.project_id, p.project_title
ORDER BY store_count DESC;
```

### User Activity Report
```sql
SELECT u.email, COUNT(al.log_id) as action_count, MAX(al.timestamp) as last_action
FROM users u
LEFT JOIN audit_logs al ON u.user_id = al.user_id
WHERE al.timestamp >= NOW() - INTERVAL '30 days'
GROUP BY u.user_id, u.email
ORDER BY action_count DESC;
```

### Cache Performance
```
redis-cli --stat
redis-cli INFO cache_stats
redis-cli --bigkeys
```

---

## 📊 Performance Benchmarks

| Operation | Benchmark | P95 | P99 |
|---|---|---|---|
| SELECT single record | < 5ms | 10ms | 20ms |
| SELECT 1000 records | < 50ms | 100ms | 200ms |
| INSERT/UPDATE | < 10ms | 20ms | 50ms |
| Cache HIT | < 1ms | 2ms | 5ms |
| Cache MISS | 50-200ms | 500ms | 1000ms |

---

## 📞 Support & Maintenance

- **Database Admin**: DBA team email
- **Connection Issues**: Check firewall rules, SSL certificates
- **Performance**: Review slow query logs, run ANALYZE
- **Backup/Recovery**: Contact DBA for restore requests

