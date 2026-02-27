# Compliance Remediation Plan - Zorro GenAI Project
**Status**: Action Plan for SSP/Enterprise Deployment
**Timeline**: 4-6 weeks to full compliance
**Priority**: CRITICAL - Blocking production rollout

---

## Overview

This document outlines the specific, actionable steps needed to bring Zorro into compliance with Walmart's GenAI SSP requirements. All items are broken down into tasks that can be assigned to developers.

---

## Phase 1: CRITICAL ISSUES (Week 1)

### Task 1.1: Remove Exposed OpenAI Key
**Priority**: 🔴 CRITICAL
**Owner**: DevOps/Security Lead
**Time**: 2 hours

**Steps**:
1. **Revoke exposed key** (ASAP - within 1 hour)
   ```bash
   # Contact: OpenAI API settings
   # Action: Delete key "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"
   ```

2. **Generate new key** (immediately after revocation)
   ```bash
   # OpenAI Portal → API Keys → Create new key
   # Store in secure vault ONLY (not .env files)
   ```

3. **Remove from git history** (Use BFG or git-filter-branch)
   ```bash
   # DANGEROUS: Consult with team lead first
   # Only if .env.example matches (.env should never be in history)
   cd zorro

   # Option A: Using BFG (recommended)
   wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar
   java -jar bfg-1.14.0.jar --replace-text .env-replacements.txt zorro.git

   # Option B: Using git-filter-branch
   git filter-branch --tree-filter 'rm -f .env' -- --all
   ```

4. **Verify removal**
   ```bash
   git log -p -- .env | grep "OPENAI_API_KEY" || echo "Key removed"
   ```

5. **Update .env.example** (if needed)
   ```bash
   # Ensure .env.example has placeholder only
   cat .env.example | grep "OPENAI_API_KEY"
   # Output: OPENAI_API_KEY=your_openai_api_key_here
   ```

**Verification**:
- [ ] Key revoked in OpenAI portal
- [ ] New key generated
- [ ] Old key NOT in git history
- [ ] Team notified of key rotation

---

### Task 1.2: Implement Secret Management System
**Priority**: 🔴 CRITICAL
**Owner**: DevOps/Backend Engineer
**Time**: 4-6 hours

**Option A: Azure Key Vault (RECOMMENDED for Walmart)**

1. **Create Key Vault in Azure**
   ```bash
   # Prerequisites: Azure subscription, Azure CLI installed

   az keyvault create \
     --resource-group "zorro-prod" \
     --name "zorro-secrets-prod" \
     --location "eastus"
   ```

2. **Store secrets**
   ```bash
   # Store OpenAI key
   az keyvault secret set \
     --vault-name "zorro-secrets-prod" \
     --name "openai-api-key" \
     --value "sk-proj-NEWKEY123..."

   # Store other secrets
   az keyvault secret set \
     --vault-name "zorro-secrets-prod" \
     --name "anthropic-api-key" \
     --value "..."
   ```

3. **Python integration**
   ```python
   # src/utils/secrets.py
   from azure.identity import DefaultAzureCredential
   from azure.keyvault.secrets import SecretClient

   class SecretManager:
       def __init__(self):
           credential = DefaultAzureCredential()
           self.client = SecretClient(
               vault_url="https://zorro-secrets-prod.vault.azure.net/",
               credential=credential
           )

       def get_secret(self, name: str) -> str:
           """Fetch secret from Key Vault."""
           try:
               secret = self.client.get_secret(name)
               return secret.value
           except Exception as e:
               raise ConfigurationError(
                   f"Failed to retrieve secret '{name}': {str(e)}"
               )

   # Usage in app initialization
   secrets = SecretManager()
   OPENAI_API_KEY = secrets.get_secret("openai-api-key")
   ```

4. **Update docker-compose.yml**
   ```yaml
   # Remove local .env volume mount
   # Instead use Azure Managed Identity
   zorro-app:
     build: .
     environment:
       - AZURE_VAULT_URL=https://zorro-secrets-prod.vault.azure.net/
       - AZURE_TENANT_ID=${AZURE_TENANT_ID}
   ```

**Verification**:
- [ ] Key Vault created
- [ ] Secrets stored in vault
- [ ] Python code retrieves from vault
- [ ] .env file not needed in production
- [ ] Docker image works with vault integration

---

### Task 1.3: Enable SSL Verification (Production)
**Priority**: 🔴 CRITICAL
**Owner**: Backend Engineer
**Time**: 2-3 hours

**File**: `src/providers/walmart_media_studio.py`

**Current Code** (Lines 27-40):
```python
SSL_VERIFY_ENABLED = os.getenv("WALMART_SSL_VERIFY", "false").lower() == "true"
CA_BUNDLE_PATH = os.getenv("WALMART_CA_BUNDLE", None)

if not SSL_VERIFY_ENABLED:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    warnings.warn("SSL verification is disabled...")
```

**Replacement Code**:
```python
import os
from pathlib import Path

class SSLConfiguration:
    """Manage SSL/TLS configuration."""

    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.ca_bundle = os.getenv("WALMART_CA_BUNDLE", None)
        self.ssl_verify = self._get_ssl_verify()

    def _get_ssl_verify(self):
        """Determine SSL verification setting."""
        if self.environment == "production":
            # Production MUST verify SSL
            if not self.ca_bundle:
                raise ConfigurationError(
                    "WALMART_CA_BUNDLE required in production. "
                    "Set to path of Walmart CA certificate."
                )
            if not Path(self.ca_bundle).exists():
                raise ConfigurationError(
                    f"CA bundle not found at: {self.ca_bundle}"
                )
            return self.ca_bundle

        elif self.environment == "staging":
            # Staging strongly recommended to verify
            if self.ca_bundle and Path(self.ca_bundle).exists():
                return self.ca_bundle
            # Warn but allow to proceed
            logger.warning(
                "SSL verification disabled in staging. "
                "This is only acceptable for development."
            )
            return False

        else:  # development
            # Dev can disable for internal network
            logger.info("SSL verification disabled in development mode")
            return False

    def get_requests_kwargs(self) -> dict:
        """Get kwargs for requests library."""
        return {
            'verify': self.ssl_verify,
            'timeout': 30
        }

# Global instance
ssl_config = SSLConfiguration()

# Usage in requests
response = requests.get(
    api_url,
    **ssl_config.get_requests_kwargs()
)
```

**Environment Setup**:
```bash
# .env.example
ENVIRONMENT=production
WALMART_CA_BUNDLE=/etc/ssl/certs/walmart-ca-bundle.crt

# docker-compose.yml
environment:
  - ENVIRONMENT=production
  - WALMART_CA_BUNDLE=/app/certs/walmart-ca-bundle.crt
volumes:
  - ./certs/walmart-ca-bundle.crt:/app/certs/walmart-ca-bundle.crt:ro
```

**Verification**:
- [ ] SSL verification required in production
- [ ] CA bundle validated on startup
- [ ] Clear error if bundle missing
- [ ] Test with valid certificate
- [ ] Test with invalid certificate (should fail)

---

### Task 1.4: Set Up SIEM Integration (Audit Logging)
**Priority**: 🔴 CRITICAL
**Owner**: DevOps/Security Engineer
**Time**: 6-8 hours

**Step 1: Prepare Walmart SOC**
```bash
# Contact: Walmart Security Operations Center (SOC)
# Email: soc@walmart.com
# Request: Syslog endpoint for Zorro application
# Provide:
#   - Application name: Zorro Video Generator
#   - Estimated log volume: 1000-5000 events/day
#   - Log format: JSON
#   - Required fields: timestamp, level, event_type, user_id, resource, status
```

**Step 2: Implement structured audit logging**

Create `src/security/audit_logger.py`:
```python
import json
import logging
import logging.handlers
import socket
from datetime import datetime
from enum import Enum
from typing import Any, Dict

class EventType(Enum):
    """Audit event types for Walmart SOC."""
    # Access events
    ACCESS_GRANTED = "ACCESS_GRANTED"
    ACCESS_DENIED = "ACCESS_DENIED"
    PERMISSION_DENIED = "PERMISSION_DENIED"

    # Data events
    VIDEO_GENERATION = "VIDEO_GENERATION"
    DESIGN_CREATED = "DESIGN_CREATED"
    DESIGN_MODIFIED = "DESIGN_MODIFIED"
    DESIGN_DELETED = "DESIGN_DELETED"
    DESIGN_APPROVED = "DESIGN_APPROVED"

    # Admin events
    USER_CREATED = "USER_CREATED"
    USER_MODIFIED = "USER_MODIFIED"
    USER_DELETED = "USER_DELETED"
    CONFIG_CHANGED = "CONFIG_CHANGED"

    # Security events
    PII_DETECTED = "PII_DETECTED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    INVALID_SSL_CERT = "INVALID_SSL_CERT"
    AUTHENTICATION_FAILURE = "AUTHENTICATION_FAILURE"

    # Data lifecycle
    DATA_DELETED = "DATA_DELETED"
    DATA_EXPORTED = "DATA_EXPORTED"

class AuditLogger:
    """Structured audit logging to SIEM."""

    def __init__(self):
        self.logger = logging.getLogger('zorro.audit')
        self._configure_handlers()

    def _configure_handlers(self):
        """Set up syslog handler for SIEM forwarding."""

        # File handler (local backup)
        file_handler = logging.handlers.RotatingFileHandler(
            filename='logs/audit.log',
            maxBytes=100_000_000,  # 100 MB
            backupCount=10
        )
        file_handler.setFormatter(self._json_formatter())
        self.logger.addHandler(file_handler)

        # Syslog handler (SIEM forwarding)
        syslog_handler = logging.handlers.SysLogHandler(
            address=(os.getenv('SIEM_SYSLOG_HOST'), 514),
            facility=logging.handlers.SysLogHandler.LOG_LOCAL0
        )
        syslog_handler.setFormatter(self._json_formatter())
        self.logger.addHandler(syslog_handler)

        self.logger.setLevel(logging.INFO)

    def _json_formatter(self):
        """Create JSON formatter for structured logging."""
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'level': record.levelname,
                    'logger': record.name,
                    'message': record.getMessage()
                }

                # Add extra fields if present
                if hasattr(record, 'event_data'):
                    log_data.update(record.event_data)

                return json.dumps(log_data)

        return JSONFormatter()

    def log_event(
        self,
        event_type: EventType,
        user_id: str = None,
        resource: str = None,
        status: str = "SUCCESS",
        details: Dict[str, Any] = None
    ):
        """Log structured audit event."""

        event_data = {
            'event_type': event_type.value,
            'user_id': user_id or 'SYSTEM',
            'resource': resource,
            'status': status,
            'hostname': socket.gethostname(),
            'application': 'Zorro-VideoGenerator'
        }

        if details:
            event_data['details'] = details

        record = logging.LogRecord(
            name='zorro.audit',
            level=logging.INFO,
            pathname='',
            lineno=0,
            msg='audit_event',
            args=(),
            exc_info=None
        )
        record.event_data = event_data

        self.logger.handle(record)

# Global instance
audit_log = AuditLogger()

# Usage examples
audit_log.log_event(
    EventType.VIDEO_GENERATION,
    user_id="user@walmart.com",
    resource="/videos/abc123",
    details={'message_length': 150, 'duration': 10}
)

audit_log.log_event(
    EventType.PII_DETECTED,
    user_id="user@walmart.com",
    status="BLOCKED",
    details={'pii_types': ['email', 'phone']}
)
```

**Step 3: Update app.py to log all events**
```python
# In Streamlit app
from src.security.audit_logger import audit_log, EventType

# Log access
@st.cache_resource
def authenticate_user():
    user_id = st.session_state.get('user_id')
    audit_log.log_event(
        EventType.ACCESS_GRANTED,
        user_id=user_id,
        resource="/app/main"
    )

# Log video generation
def generate_video():
    audit_log.log_event(
        EventType.VIDEO_GENERATION,
        user_id=user_id,
        resource="/videos/generated",
        details={'message': message_content[:100]}
    )
```

**Step 4: Configure SIEM endpoint**
```bash
# .env.example
SIEM_SYSLOG_HOST=walmart-siem-collector.prod.walmart.com
SIEM_SYSLOG_PORT=514

# docker-compose.yml
environment:
  - SIEM_SYSLOG_HOST=walmart-siem-collector.prod.walmart.com
```

**Verification**:
- [ ] SOC endpoint provisioned
- [ ] Logs sent to syslog endpoint
- [ ] SOC can receive and parse JSON logs
- [ ] Alert rule configured in SIEM
- [ ] Test with sample events

---

## Phase 2: ACCESS CONTROL & RBAC (Week 2)

### Task 2.1: Implement Role-Based Access Control (RBAC)
**Priority**: 🔴 CRITICAL
**Owner**: Backend Engineer + Frontend Engineer
**Time**: 8-10 hours

**Database Schema** (PostgreSQL):
```sql
-- Create tables for RBAC
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE role_permissions (
    role_id INT REFERENCES roles(id),
    permission_id INT REFERENCES permissions(id),
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    walmart_employee_id VARCHAR(20) UNIQUE,
    name VARCHAR(255),
    role_id INT REFERENCES roles(id),
    facilities TEXT[], -- Array of facility codes
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE audit_access (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    action VARCHAR(100),
    resource VARCHAR(255),
    status VARCHAR(20), -- ALLOWED, DENIED
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Insert roles
INSERT INTO roles (name, description) VALUES
('ADMIN', 'Full access to all facilities and features'),
('FACILITY_MANAGER', 'Manage their assigned facility'),
('CONTENT_CREATOR', 'Create videos, manage designs'),
('VIEWER', 'View-only access to library');

-- Insert permissions
INSERT INTO permissions (name, description) VALUES
('CREATE_VIDEO', 'Generate new videos'),
('APPROVE_VIDEO', 'Approve generated videos'),
('MANAGE_DESIGNS', 'Create and edit design templates'),
('VIEW_ANALYTICS', 'View usage analytics'),
('MANAGE_USERS', 'Manage user roles and access'),
('MANAGE_FACILITIES', 'Configure facility settings'),
('DELETE_VIDEO', 'Delete videos from library');

-- Assign permissions to roles
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r, permissions p
WHERE r.name = 'ADMIN'; -- Admin gets all permissions

INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r, permissions p
WHERE r.name = 'CONTENT_CREATOR'
AND p.name IN ('CREATE_VIDEO', 'MANAGE_DESIGNS', 'VIEW_ANALYTICS');

INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r, permissions p
WHERE r.name = 'FACILITY_MANAGER'
AND p.name IN ('CREATE_VIDEO', 'MANAGE_DESIGNS', 'VIEW_ANALYTICS', 'APPROVE_VIDEO');

INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r, permissions p
WHERE r.name = 'VIEWER'
AND p.name = 'VIEW_ANALYTICS';
```

**Python Implementation**:

Create `src/security/rbac.py`:
```python
from enum import Enum
from typing import List
from pydantic import BaseModel

class Role(str, Enum):
    ADMIN = "ADMIN"
    FACILITY_MANAGER = "FACILITY_MANAGER"
    CONTENT_CREATOR = "CONTENT_CREATOR"
    VIEWER = "VIEWER"

class Permission(str, Enum):
    CREATE_VIDEO = "CREATE_VIDEO"
    APPROVE_VIDEO = "APPROVE_VIDEO"
    MANAGE_DESIGNS = "MANAGE_DESIGNS"
    VIEW_ANALYTICS = "VIEW_ANALYTICS"
    MANAGE_USERS = "MANAGE_USERS"
    MANAGE_FACILITIES = "MANAGE_FACILITIES"
    DELETE_VIDEO = "DELETE_VIDEO"

class UserContext(BaseModel):
    """Authenticated user from SSO."""
    user_id: str
    email: str
    name: str
    role: Role
    facilities: List[str]  # Facility codes

class RBACManager:
    """Manage role-based access control."""

    # Permission map
    ROLE_PERMISSIONS = {
        Role.ADMIN: [p.value for p in Permission],
        Role.FACILITY_MANAGER: [
            Permission.CREATE_VIDEO,
            Permission.MANAGE_DESIGNS,
            Permission.VIEW_ANALYTICS,
            Permission.APPROVE_VIDEO
        ],
        Role.CONTENT_CREATOR: [
            Permission.CREATE_VIDEO,
            Permission.MANAGE_DESIGNS,
            Permission.VIEW_ANALYTICS
        ],
        Role.VIEWER: [Permission.VIEW_ANALYTICS]
    }

    def has_permission(
        self,
        user: UserContext,
        permission: Permission
    ) -> bool:
        """Check if user has permission."""
        perms = self.ROLE_PERMISSIONS.get(user.role, [])
        return permission.value in perms

    def can_access_facility(
        self,
        user: UserContext,
        facility_code: str
    ) -> bool:
        """Check if user can access facility."""
        if user.role == Role.ADMIN:
            return True
        return facility_code in user.facilities

    def require_permission(self, permission: Permission):
        """Decorator to check permission."""
        def decorator(func):
            def wrapper(user: UserContext, *args, **kwargs):
                if not self.has_permission(user, permission):
                    audit_log.log_event(
                        EventType.PERMISSION_DENIED,
                        user_id=user.user_id,
                        status="DENIED",
                        details={'permission': permission.value}
                    )
                    raise PermissionError(
                        f"User lacks permission: {permission.value}"
                    )
                return func(user, *args, **kwargs)
            return wrapper
        return decorator

rbac = RBACManager()
```

**Streamlit Integration**:
```python
# In app.py

from src.security.rbac import rbac, Permission

@rbac.require_permission(Permission.CREATE_VIDEO)
def create_video_page(user: UserContext):
    st.title("Create Video")
    # Video creation UI

@rbac.require_permission(Permission.MANAGE_DESIGNS)
def design_studio_page(user: UserContext):
    st.title("Design Studio")
    # Design management UI

# In sidebar
if rbac.has_permission(user, Permission.CREATE_VIDEO):
    if st.sidebar.button("Create Video"):
        st.session_state.page = "create_video"

if rbac.has_permission(user, Permission.MANAGE_DESIGNS):
    if st.sidebar.button("Design Studio"):
        st.session_state.page = "design_studio"

if rbac.has_permission(user, Permission.MANAGE_USERS):
    if st.sidebar.button("Admin Panel"):
        st.session_state.page = "admin"
```

**Verification**:
- [ ] Database tables created
- [ ] Permissions assigned to roles
- [ ] RBAC middleware working
- [ ] Streamlit UI shows/hides menu items
- [ ] Permission denied returns 403

---

### Task 2.2: Integrate Walmart SSO with RBAC
**Priority**: 🔴 CRITICAL
**Owner**: Backend Engineer
**Time**: 4-6 hours

**Extract roles from SSO:**

```python
# src/security/sso_integration.py

import requests
from typing import Optional

class WalmartSSO:
    """Integrate with Walmart SSO for authentication and roles."""

    def __init__(self):
        self.sso_endpoint = os.getenv('WALMART_SSO_ENDPOINT')
        self.token = os.getenv('WALMART_SSO_TOKEN')

    def get_user_context(self, sso_token: str) -> UserContext:
        """Get user info and roles from Walmart SSO."""

        headers = {
            'Authorization': f'Bearer {sso_token}',
            'Content-Type': 'application/json'
        }

        # Call SSO API to get user info
        response = requests.get(
            f"{self.sso_endpoint}/v1/users/me",
            headers=headers,
            **ssl_config.get_requests_kwargs()
        )

        if response.status_code != 200:
            audit_log.log_event(
                EventType.AUTHENTICATION_FAILURE,
                status="FAILED"
            )
            raise AuthenticationError("SSO token invalid")

        user_data = response.json()

        # Extract roles and facilities from SSO attributes
        roles = user_data.get('groups', [])
        user_role = self._map_groups_to_role(roles)
        facilities = self._extract_facilities(user_data)

        return UserContext(
            user_id=user_data['employee_id'],
            email=user_data['email'],
            name=user_data['display_name'],
            role=user_role,
            facilities=facilities
        )

    def _map_groups_to_role(self, groups: list) -> Role:
        """Map SSO groups to application roles."""
        # Walmart AD groups convention
        group_mappings = {
            'zorro-admins': Role.ADMIN,
            'zorro-facility-managers': Role.FACILITY_MANAGER,
            'zorro-creators': Role.CONTENT_CREATOR,
        }

        for group, role in group_mappings.items():
            if group in groups:
                return role

        # Default to VIEWER
        return Role.VIEWER

    def _extract_facilities(self, user_data: dict) -> list:
        """Extract facility codes from user attributes."""
        # Walmart stores facility code in 'facility_code' attribute
        facility_code = user_data.get('facility_code')
        if facility_code:
            return [facility_code]

        # Admins have access to all facilities
        if 'zorro-admins' in user_data.get('groups', []):
            return ['*']  # Wildcard for all

        return []

# Streamlit session state
@st.cache_resource
def get_sso():
    return WalmartSSO()

# Authentication middleware
def authenticate():
    """Authenticate user and set session."""
    sso = get_sso()

    # Get token from URL or session
    token = st.query_params.get('token') or st.session_state.get('sso_token')

    if not token:
        st.error("SSO token required. Please log in through Walmart portal.")
        st.stop()

    try:
        user = sso.get_user_context(token)
        st.session_state.user = user
        st.session_state.sso_token = token

        audit_log.log_event(
            EventType.ACCESS_GRANTED,
            user_id=user.user_id,
            resource="/app/main"
        )
        return user

    except AuthenticationError as e:
        st.error(f"Authentication failed: {str(e)}")
        st.stop()

# In main app
def main():
    user = authenticate()

    st.title(f"Welcome, {user.name}!")
    st.write(f"Role: {user.role.value}")

    # Rest of app
```

**Verification**:
- [ ] SSO token validated
- [ ] User roles extracted from AD groups
- [ ] Facilities assigned correctly
- [ ] Access control enforced
- [ ] Audit logs show authentication

---

### Task 2.3: Add MFA (Multi-Factor Authentication)
**Priority**: ⚠️ MEDIUM (can be deferred to week 3)
**Owner**: Backend Engineer
**Time**: 3-4 hours

**Streamlit MFA Integration**:

```python
# src/security/mfa.py

class MFAManager:
    """Manage multi-factor authentication."""

    def __init__(self):
        # Walmart uses Duo Security
        self.duo_ikey = os.getenv('DUO_IKEY')
        self.duo_skey = os.getenv('DUO_SKEY')
        self.duo_host = os.getenv('DUO_HOST')

    def verify_mfa(self, user_id: str) -> bool:
        """Verify MFA through Duo."""
        # Implementation depends on Duo API
        # For Streamlit, typically handled at proxy level
        pass
```

**Note**: MFA is typically handled at the authentication proxy level (reverse proxy/WAF), not within the application. Contact Walmart IT to enable this at infrastructure level.

---

## Phase 3: DATA PROTECTION (Week 2-3)

### Task 3.1: Implement PII Detection & Masking
**Priority**: 🔴 CRITICAL
**Owner**: Backend Engineer
**Time**: 4-5 hours

**File**: `src/security/pii_detection.py`

```python
import re
from typing import Tuple, Dict, List
from src.security.audit_logger import audit_log, EventType

class PIIDetector:
    """Detect and mask PII in user content."""

    # Regex patterns for common PII
    PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone_us': r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b',
        'ssn': r'\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4}\b',
        'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        'bank_account': r'\b\d{8,17}\b',
        'zipcode_us': r'\b\d{5}(?:-\d{4})?\b',
        'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        'walmart_employee_id': r'\b[a-zA-Z]\d{7}\b',  # e.g., m1234567
    }

    def detect_pii(self, text: str) -> Dict[str, int]:
        """Detect PII types and count occurrences."""
        findings = {}

        for pii_type, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Handle nested tuples from regex groups
                count = len(matches) if isinstance(matches[0], str) else len(matches)
                findings[pii_type] = count

        return findings

    def mask_pii(self, text: str) -> str:
        """Replace PII with generic masks."""
        masked = text

        # Email
        masked = re.sub(
            self.PATTERNS['email'],
            '[EMAIL_MASKED]',
            masked,
            flags=re.IGNORECASE
        )

        # Phone
        masked = re.sub(
            self.PATTERNS['phone_us'],
            '[PHONE_MASKED]',
            masked
        )

        # SSN
        masked = re.sub(
            self.PATTERNS['ssn'],
            '[SSN_MASKED]',
            masked
        )

        # Credit card
        masked = re.sub(
            self.PATTERNS['credit_card'],
            '[CC_MASKED]',
            masked
        )

        # Employee ID
        masked = re.sub(
            self.PATTERNS['walmart_employee_id'],
            '[EMPLOYEE_ID_MASKED]',
            masked
        )

        return masked

    def validate_user_input(self, prompt: str, user_id: str) -> Tuple[bool, List[str], str]:
        """
        Validate user prompt for PII.

        Returns:
            (is_clean, pii_types_found, masked_prompt)
        """
        pii_found = self.detect_pii(prompt)

        if pii_found:
            # Log PII detection
            audit_log.log_event(
                EventType.PII_DETECTED,
                user_id=user_id,
                status="BLOCKED",
                details={
                    'pii_types': list(pii_found.keys()),
                    'counts': pii_found,
                    'message_length': len(prompt)
                }
            )

            return False, list(pii_found.keys()), None

        return True, [], prompt

    def get_safe_prompt(self, prompt: str) -> str:
        """Get masked version of prompt for logging."""
        return self.mask_pii(prompt)[:200]  # First 200 chars masked

# Global instance
pii_detector = PIIDetector()

# Unit tests
def test_pii_detection():
    detector = PIIDetector()

    # Test email
    assert 'email' in detector.detect_pii("Contact john@walmart.com")

    # Test phone
    assert 'phone_us' in detector.detect_pii("Call 555-123-4567")

    # Test SSN
    assert 'ssn' in detector.detect_pii("SSN: 123-45-6789")

    # Test Walmart employee ID
    assert 'walmart_employee_id' in detector.detect_pii("Employee m1234567")

    # Test masking
    masked = detector.mask_pii("Email john@walmart.com and phone 555-123-4567")
    assert "[EMAIL_MASKED]" in masked
    assert "[PHONE_MASKED]" in masked

    print("✅ All PII detection tests passed")
```

**Integration with Video Generation**:

```python
# In src/core/message_processor.py

class MessageProcessor:
    def __init__(self):
        self.pii_detector = pii_detector

    def process(self, message: str, user_id: str) -> ProcessedMessage:
        """Process message with PII validation."""

        # Check for PII
        is_clean, pii_types, _ = self.pii_detector.validate_user_input(
            message,
            user_id
        )

        if not is_clean:
            raise ValueError(
                f"Your message contains sensitive information ({', '.join(pii_types)}). "
                "Please remove the following:\n"
                "- Email addresses\n"
                "- Phone numbers\n"
                "- Social security numbers\n"
                "- Credit card numbers\n"
                "- Employee IDs"
            )

        # Continue with processing
        return ProcessedMessage(content=message)

# In app.py (Streamlit)
def generate_video_page():
    st.title("Generate Video")

    message = st.text_area("Activity Message")

    if st.button("Generate"):
        try:
            processor = MessageProcessor()
            processed = processor.process(message, user.user_id)

            # Continue with generation
            result = pipeline.generate(processed.content)
            st.success("Video generated!")

        except ValueError as e:
            st.error(str(e))  # PII error message
        except Exception as e:
            st.error("Generation failed. Please try again.")
            audit_log.log_event(
                EventType.VIDEO_GENERATION,
                user_id=user.user_id,
                status="FAILED",
                details={'error': str(e)[:100]}
            )
```

**Verification**:
- [ ] Test with real PII patterns
- [ ] Unit tests passing
- [ ] Error message user-friendly
- [ ] Audit log records PII detection
- [ ] Masked prompts in logs

---

### Task 3.2: Implement Data Retention Policy
**Priority**: 🔴 CRITICAL
**Owner**: Backend Engineer + DevOps
**Time**: 4-5 hours

**File**: `src/services/data_retention_service.py`

```python
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict
from src.security.audit_logger import audit_log, EventType

class DataRetentionPolicy:
    """Walmart GenAI data retention compliance."""

    # Per Walmart Records and Information Management Policy
    RETENTION_PERIODS = {
        'generated_video': timedelta(days=730),           # 2 years (transitory AI output)
        'design_template': timedelta(days=2555),          # 7 years (IP/corporate asset)
        'audit_log': timedelta(days=1095),                # 3 years (legal hold)
        'user_prompt': timedelta(days=90),                # 90 days (transitory)
        'deleted_video_backup': timedelta(days=30),       # 30 days (recovery window)
    }

    def __init__(self, base_path: str = './'):
        self.base_path = Path(base_path)

    def get_retention_period(self, data_type: str) -> timedelta:
        """Get retention period for data type."""
        return self.RETENTION_PERIODS.get(
            data_type,
            timedelta(days=365)  # Default 1 year
        )

    def should_delete(self, file_path: Path, data_type: str) -> bool:
        """Check if file should be deleted based on age."""
        if not file_path.exists():
            return False

        created_time = datetime.fromtimestamp(file_path.stat().st_ctime)
        age = datetime.now() - created_time
        retention = self.get_retention_period(data_type)

        return age > retention

    def delete_file(self, file_path: Path, data_type: str):
        """Delete file and log the action."""
        if not file_path.exists():
            return

        # Secure deletion: overwrite before delete
        file_size = file_path.stat().st_size
        with open(file_path, 'wb') as f:
            f.write(os.urandom(file_size))  # Overwrite with random data

        file_path.unlink()

        # Log deletion
        audit_log.log_event(
            EventType.DATA_DELETED,
            user_id='SYSTEM',
            resource=str(file_path),
            status='DELETED',
            details={
                'data_type': data_type,
                'file_size': file_size,
                'retention_policy': self.get_retention_period(data_type).days
            }
        )

    def cleanup_expired_videos(self):
        """Remove videos older than retention period."""
        videos_dir = self.base_path / 'output' / 'videos'

        if not videos_dir.exists():
            return

        deleted_count = 0
        for video_file in videos_dir.glob('*.mp4'):
            if self.should_delete(video_file, 'generated_video'):
                self.delete_file(video_file, 'generated_video')
                deleted_count += 1

        if deleted_count > 0:
            audit_log.log_event(
                EventType.DATA_DELETED,
                user_id='SYSTEM',
                resource=str(videos_dir),
                status='CLEANUP_COMPLETED',
                details={'videos_deleted': deleted_count}
            )

    def cleanup_old_logs(self):
        """Remove audit logs older than retention period."""
        logs_file = self.base_path / 'logs' / 'audit.log'

        if self.should_delete(logs_file, 'audit_log'):
            # Archive before deletion
            archive_path = logs_file.with_suffix('.log.archived')
            logs_file.rename(archive_path)

    def generate_retention_report(self) -> Dict:
        """Generate compliance report on retention."""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'policy_version': '1.0',
            'retention_periods': {
                k: v.days for k, v in self.RETENTION_PERIODS.items()
            },
            'legal_hold_enabled': True,
            'last_cleanup': datetime.utcnow().isoformat()
        }

# Scheduled job (using APScheduler)
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

retention_service = DataRetentionService()

def schedule_cleanup():
    """Schedule daily cleanup job at 2 AM."""
    # Run cleanup every day at 2:00 AM
    scheduler.add_job(
        retention_service.cleanup_expired_videos,
        'cron',
        hour=2,
        minute=0,
        id='cleanup_videos'
    )

    # Run cleanup every Monday at 3:00 AM
    scheduler.add_job(
        retention_service.cleanup_old_logs,
        'cron',
        day_of_week='mon',
        hour=3,
        minute=0,
        id='cleanup_logs'
    )

    scheduler.start()
```

**Environment Configuration**:

```yaml
# config/config.yaml
data_retention:
  enabled: true
  check_interval_hours: 24  # Check daily
  cleanup_time: "02:00"     # 2 AM UTC
  secure_deletion: true     # Overwrite before delete
  policy:
    generated_videos: 730    # days
    design_templates: 2555   # days
    audit_logs: 1095         # days
    user_prompts: 90         # days
```

**Docker Integration**:

```dockerfile
# Dockerfile - add APScheduler
RUN pip install apscheduler
```

**Verification**:
- [ ] Cleanup job runs daily
- [ ] Videos deleted after 730 days
- [ ] Audit logs preserved
- [ ] Deletion logged
- [ ] Recovery tested

---

## Phase 4: REMAINING COMPLIANCE (Week 3-4)

### Task 4.1: Third-Party Data Handling Documentation
**Priority**: ⚠️ HIGH
**Owner**: Product Manager + Legal
**Time**: 2-3 hours

**Create**: `THIRD_PARTY_DATA_HANDLING.md`

(See template in main compliance review document)

**Verification**:
- [ ] All vendors listed
- [ ] Data flow documented
- [ ] DPA status verified
- [ ] Legal review completed

---

### Task 4.2: Rate Limiting Implementation
**Priority**: ⚠️ MEDIUM
**Owner**: Backend Engineer
**Time**: 2-3 hours

```python
# src/middleware/rate_limit.py

from datetime import datetime, timedelta
from collections import defaultdict
import streamlit as st

class RateLimiter:
    """Rate limit user API requests."""

    def __init__(self, calls_per_minute: int = 10):
        self.calls_per_minute = calls_per_minute
        self.user_calls = defaultdict(list)

    def is_rate_limited(self, user_id: str) -> bool:
        """Check if user exceeded rate limit."""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)

        # Remove old calls
        self.user_calls[user_id] = [
            call_time for call_time in self.user_calls[user_id]
            if call_time > minute_ago
        ]

        # Check limit
        if len(self.user_calls[user_id]) >= self.calls_per_minute:
            audit_log.log_event(
                EventType.RATE_LIMIT_EXCEEDED,
                user_id=user_id,
                status="BLOCKED",
                details={'calls_in_minute': len(self.user_calls[user_id])}
            )
            return True

        # Record this call
        self.user_calls[user_id].append(now)
        return False

# In app.py
rate_limiter = RateLimiter(calls_per_minute=10)

def generate_video_page(user):
    if rate_limiter.is_rate_limited(user.user_id):
        st.error("Rate limit exceeded. Maximum 10 generations per minute.")
        return

    # Proceed with generation
```

---

## Success Metrics

### Week 1 (Critical Path)
- [ ] Exposed keys removed
- [ ] Secret management implemented
- [ ] SSL verification enabled
- [ ] SIEM integration active
- [ ] **Status**: All critical issues resolved

### Week 2
- [ ] RBAC fully implemented
- [ ] SSO integration complete
- [ ] PII detection working
- [ ] Audit logging comprehensive
- [ ] **Status**: Ready for internal testing

### Week 3
- [ ] Data retention policy active
- [ ] Third-party data handling documented
- [ ] Rate limiting deployed
- [ ] All tests passing
- [ ] **Status**: Ready for security review

### Week 4
- [ ] Internal security audit passed
- [ ] SSP (Service Security Platform) review initiated
- [ ] Documentation complete
- [ ] **Status**: Ready for production deployment

---

## Deployment Checklist

### Pre-Production
- [ ] All code changes reviewed
- [ ] Security tests passing (100%)
- [ ] SIEM integration tested
- [ ] Audit logs flowing
- [ ] RBAC tested end-to-end
- [ ] PII detection tested
- [ ] Rate limiting validated
- [ ] Data retention job running

### Production Deployment
- [ ] Environment variables set correctly
- [ ] SSL certificates installed
- [ ] SIEM endpoint accessible
- [ ] Database migrations completed
- [ ] Redis cache running
- [ ] Backup systems operational
- [ ] Monitoring dashboards created
- [ ] Incident response procedures documented

### Post-Deployment
- [ ] Monitor audit logs for anomalies
- [ ] Verify SIEM receiving events
- [ ] Track compliance metrics
- [ ] Schedule first review (30 days)

---

## Key Contacts

- **Walmart SOC**: soc@walmart.com
- **Walmart CISO**: ciso@walmart.com
- **SSP Portal**: [http://wmlink.wal-mart.com/ssp](http://wmlink.wal-mart.com/ssp)
- **Security Team**: Your internal security team

---

**Document Created**: January 21, 2026
**Next Update**: After Phase 1 completion
**Status**: Ready for implementation
