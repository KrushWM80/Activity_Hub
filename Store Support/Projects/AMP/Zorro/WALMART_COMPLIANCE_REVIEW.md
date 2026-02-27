# Walmart Compliance Review - Zorro GenAI Project
**Date**: January 21, 2026
**Status**: Phase 1 Production - Compliance Assessment
**Project**: Zorro - Enterprise AI Video Content Generation Platform

---

## Executive Summary

Zorro is a **PHASE 1 PRODUCTION SYSTEM** handling real Walmart Store communications. This review assesses compliance against Walmart's GenAI SSP (Service Security Platform) requirements and identifies gaps that must be addressed before enterprise-wide rollout.

### Compliance Status
| Category | Status | Notes |
|----------|--------|-------|
| **Data Privacy & PII** | ⚠️ NEEDS WORK | No formal PII de-identification process |
| **SSL/TLS Encryption** | ⚠️ PARTIAL | SSL verification disabled in dev, needs enforcement in prod |
| **Audit Logging** | ⚠️ CRITICAL | No SIEM integration or SOC forwarding |
| **SSO Integration** | ⚠️ CRITICAL | Currently using SSO token, needs RBAC/ABAC implementation |
| **Access Control** | ⚠️ PARTIAL | No formal RBAC/ABAC framework |
| **Data Retention** | ⚠️ MISSING | No retention policies documented |
| **Secrets Management** | 🔴 CRITICAL | OpenAI key exposed in .env file |
| **API Security** | ⚠️ PARTIAL | API keys not properly protected |

---

## Critical Issues (Must Fix Before Enterprise Deployment)

### 1. 🔴 **CRITICAL: Exposed Secrets in Repository**

**Finding**: OpenAI API key is exposed in `.env` file
**Location**: `.env` line 8
**Risk**: Private key can be used to impersonate the application
**Walmart Requirement**: Secrets must be managed via secure vaults (Azure Key Vault, Hashicorp Vault)

**Immediate Actions Required**:
```bash
# 1. Revoke the exposed OpenAI key immediately
# 2. Generate new API key
# 3. Remove .env from git history (dangerous operation - consult security team)
# 4. Never commit .env to version control
```

**Implementation**:
- ✅ `.gitignore` already excludes `.env` (correct)
- ❌ But the key was already committed to history
- Use `.env.example` (already in place) for documentation only

**Remediation**:
```bash
# Contact OpenAI to revoke exposed key
# Add to secret management system
# Remove from git history (git-filter-branch or BFG)
```

---

### 2. 🔴 **CRITICAL: SSL Verification Disabled**

**Finding**: `WALMART_SSL_VERIFY=false` in development and `.env.example`
**Location**: `.env`, `docker-compose.yml`, `src/providers/walmart_media_studio.py`
**Risk**: Vulnerable to man-in-the-middle (MITM) attacks on internal network

**Current Implementation** (walmart_media_studio.py, lines 28-40):
```python
SSL_VERIFY_ENABLED = os.getenv("WALMART_SSL_VERIFY", "false").lower() == "true"
CA_BUNDLE_PATH = os.getenv("WALMART_CA_BUNDLE", None)

if not SSL_VERIFY_ENABLED:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    warnings.warn("SSL verification is disabled...")
```

**Issues**:
- Default is `false` (insecure)
- Warnings are suppressed in production
- No CA bundle path validation

**Walmart Requirement**: TLS 1.2 or higher with certificate verification

**Remediation**:
```python
# FIX: Change default to require SSL
SSL_VERIFY_ENABLED = os.getenv("WALMART_SSL_VERIFY", "true").lower() == "true"

# FIX: Enforce CA bundle in production
if os.getenv("ENVIRONMENT") == "production":
    if not CA_BUNDLE_PATH or not Path(CA_BUNDLE_PATH).exists():
        raise ConfigurationError(
            "WALMART_CA_BUNDLE must be set and valid in production"
        )
    SSL_VERIFY = CA_BUNDLE_PATH
else:
    SSL_VERIFY = CA_BUNDLE_PATH if CA_BUNDLE_PATH else False

# Enforce minimum TLS version
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = (
    'TLS_AES_256_GCM_SHA384:'
    'TLS_CHACHA20_POLY1305_SHA256:'
    'TLS_AES_128_GCM_SHA256'
)
```

---

### 3. 🔴 **CRITICAL: No Audit Logging to SOC SIEM**

**Finding**: Application logs are local only, not forwarded to Walmart SOC
**Current**: Logs written to `logs/` directory with structlog
**Missing**: SIEM integration, SOC forwarding, incident response capability

**Walmart Requirement**: All access and activity must be logged to SOC SIEM

**Current Logging Setup** (src/utils/logger.py):
- ✅ Uses structlog (JSON structured logging - good foundation)
- ✅ Logs to file with rotation
- ❌ No SIEM forwarding
- ❌ No centralized logging service

**Required Implementation**:
```python
# Add to logging configuration
import sys
from pythonjsonlogger import jsonlogger
import logging.handlers

# Configure syslog for SIEM forwarding
syslog_handler = logging.handlers.SysLogHandler(
    address=("walmart-siem.internal", 514),
    facility=logging.handlers.SysLogHandler.LOG_LOCAL0
)
syslog_handler.setFormatter(
    jsonlogger.JsonFormatter('%(timestamp)s %(level)s %(message)s')
)

# All audit events must be logged
audit_logger = logging.getLogger('zorro.audit')
audit_logger.addHandler(syslog_handler)

# Log all access events
def log_access_event(user_id: str, action: str, resource: str, status: str):
    audit_logger.info({
        'event_type': 'ACCESS',
        'user_id': user_id,
        'action': action,
        'resource': resource,
        'status': status,
        'timestamp': datetime.utcnow().isoformat()
    })

# Log all video generation
def log_generation_event(user_id: str, message_content: str, output_path: str):
    audit_logger.info({
        'event_type': 'GENERATION',
        'user_id': user_id,
        'message_length': len(message_content),
        'output_path': output_path,
        'timestamp': datetime.utcnow().isoformat()
    })
```

**Action Items**:
- [ ] Contact Walmart SOC to provision syslog endpoint
- [ ] Implement structured audit logging with event types
- [ ] Forward all access/generation events to SIEM
- [ ] Set up log retention policy (minimum 90 days)
- [ ] Document log schema for SOC team

---

### 4. 🔴 **CRITICAL: Missing Access Control & RBAC**

**Finding**: No role-based access control (RBAC) implementation
**Current**: SSO token-based access, but no facility-level or role differentiation
**Walmart Requirement**: RBAC/ABAC required for both admin and user access

**Current State**:
- ✅ Uses Walmart SSO (good)
- ❌ No role checking
- ❌ No facility-level isolation
- ❌ No permission validation

**Required Implementation**:
```python
# Create new file: src/security/access_control.py

from enum import Enum
from typing import List
from pydantic import BaseModel

class Role(Enum):
    """User roles for Zorro."""
    ADMIN = "admin"              # Full access, all facilities
    FACILITY_MANAGER = "facility_manager"  # Manage own facility
    CONTENT_CREATOR = "content_creator"    # Create videos
    VIEWER = "viewer"            # View only

class Permission(Enum):
    """Granular permissions."""
    CREATE_VIDEO = "create_video"
    APPROVE_VIDEO = "approve_video"
    MANAGE_DESIGNS = "manage_designs"
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_USERS = "manage_users"

class UserContext(BaseModel):
    """Authenticated user context from SSO."""
    user_id: str
    email: str
    name: str
    roles: List[Role]
    facilities: List[str]  # Facility codes user can access
    department: str

# Middleware for access control
def require_permission(permission: Permission):
    def decorator(func):
        async def wrapper(*args, user: UserContext = None, **kwargs):
            if not user:
                raise UnauthorizedError("User context not found")

            # Check if user has permission
            user_permissions = get_user_permissions(user.roles)
            if permission not in user_permissions:
                audit_logger.warning({
                    'event_type': 'PERMISSION_DENIED',
                    'user_id': user.user_id,
                    'permission': permission.value,
                    'timestamp': datetime.utcnow().isoformat()
                })
                raise ForbiddenError(f"Permission denied: {permission.value}")

            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator

# Usage in Streamlit app
@require_permission(Permission.CREATE_VIDEO)
def create_video(user: UserContext, message: str):
    # Only users with CREATE_VIDEO permission can proceed
    pass
```

**Action Items**:
- [ ] Define role hierarchy (Admin → Facility Manager → Creator → Viewer)
- [ ] Implement permission model in database
- [ ] Extract roles from Walmart SSO/AD attributes
- [ ] Add access control checks to all endpoints
- [ ] Implement facility-level data isolation

---

### 5. 🔴 **CRITICAL: No Data Retention Policy**

**Finding**: No documented data retention or deletion procedures
**Current**: Videos stored indefinitely in `output/videos/`
**Walmart Requirement**: GenAI outputs are transitory, should not be retained longer than 2 years unless legally required

**Required Implementation**:
```python
# src/services/data_retention_service.py

from datetime import datetime, timedelta
from pathlib import Path

class DataRetentionService:
    """Manages data lifecycle per Walmart compliance."""

    RETENTION_PERIODS = {
        'video': timedelta(days=730),           # 2 years
        'design_element': timedelta(days=2555), # 7 years (IP retention)
        'audit_log': timedelta(days=1095),      # 3 years (legal hold)
        'user_generated_prompt': timedelta(days=90)  # 90 days
    }

    def should_delete(self, file_path: Path, file_type: str) -> bool:
        """Check if file exceeds retention period."""
        created_time = datetime.fromtimestamp(file_path.stat().st_ctime)
        retention = self.RETENTION_PERIODS.get(file_type)

        if not retention:
            return False

        age = datetime.now() - created_time
        return age > retention

    def prune_expired_data(self, base_path: Path):
        """Delete expired files and log deletion."""
        for video_path in base_path.glob('output/videos/*.mp4'):
            if self.should_delete(video_path, 'video'):
                audit_logger.info({
                    'event_type': 'DATA_DELETION',
                    'file_path': str(video_path),
                    'reason': 'retention_expired',
                    'timestamp': datetime.utcnow().isoformat()
                })
                video_path.unlink()

    def document_retention(self):
        """Generate retention compliance report."""
        return {
            'policy': 'Walmart GenAI transitory data policy',
            'reviewed_date': datetime.now().isoformat(),
            'retention_periods': self.RETENTION_PERIODS,
            'legal_hold_enabled': True
        }
```

**Action Items**:
- [ ] Document retention periods per data type
- [ ] Implement scheduled deletion job (daily prune at 2 AM)
- [ ] Log all deletions for audit trail
- [ ] Get legal approval for retention periods
- [ ] Test deletion and recovery procedures

---

## High Priority Issues (Should Fix Before General Release)

### 6. ⚠️ **HIGH: PII De-identification Process Missing**

**Finding**: No mechanism to detect or strip PII from user inputs
**Risk**: User prompts might contain sensitive information (names, phone numbers, emails)
**Walmart Standard**: DG-01-ST-02 requires de-identification of all sensitive data

**Required Implementation**:
```python
# src/security/pii_detection.py

import re
from typing import Tuple

class PIIDetector:
    """Detect and mask PII in content."""

    PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b',
        'ssn': r'\b(?:\d{3}-){2}\d{4}\b',
        'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        'zipcode': r'\b\d{5}(?:-\d{4})?\b',
    }

    def detect_pii(self, text: str) -> dict:
        """Detect PII types in text."""
        findings = {}
        for pii_type, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                findings[pii_type] = len(matches)
        return findings

    def mask_pii(self, text: str) -> str:
        """Replace detected PII with masks."""
        for pii_type, pattern in self.PATTERNS.items():
            if pii_type == 'email':
                text = re.sub(pattern, '[EMAIL_MASKED]', text)
            elif pii_type == 'phone':
                text = re.sub(pattern, '[PHONE_MASKED]', text)
            elif pii_type in ['ssn', 'credit_card']:
                text = re.sub(pattern, '[REDACTED]', text)
        return text

    def validate_prompt(self, prompt: str) -> Tuple[bool, list]:
        """Validate prompt for PII before processing."""
        pii_found = self.detect_pii(prompt)

        if pii_found:
            audit_logger.warning({
                'event_type': 'PII_DETECTION',
                'pii_types': list(pii_found.keys()),
                'timestamp': datetime.utcnow().isoformat()
            })
            return False, list(pii_found.keys())

        return True, []

# Usage in video generation
detector = PIIDetector()
is_clean, pii_types = detector.validate_prompt(user_message)

if not is_clean:
    raise ValueError(f"Message contains PII: {', '.join(pii_types)}. "
                     "Please remove sensitive information.")
```

**Action Items**:
- [ ] Implement PII detection using regex and NLP
- [ ] Add validation to message processor
- [ ] Log all PII detection events
- [ ] Display user-friendly error messages
- [ ] Test with common PII examples

---

### 7. ⚠️ **HIGH: Third-Party Data Handling Not Documented**

**Finding**: External APIs used without documented data handling agreements
**Services Used**:
- OpenAI API (LLM)
- Google Veo (Walmart Media Studio)
- Anthropic API (optional)
- Stability AI (optional)
- RunwayML (optional)

**Walmart Requirement**: Third-party vendors must adhere to Walmart data policies

**Required Documentation**:
Create `THIRD_PARTY_DATA_HANDLING.md`:
```markdown
# Third-Party Data Handling Policy

## OpenAI API
- **Service**: GPT-4 Turbo Prompt Enhancement
- **Data Shared**: Activity message text (max 500 chars)
- **Data NOT Shared**: User IDs, customer data, PII
- **Retention**: Per OpenAI privacy policy (not used for training)
- **DPA Status**: Walmart has DPA with OpenAI
- **Approval**: Required before using in production

## Walmart Media Studio (Google Veo)
- **Service**: Video generation
- **Data Shared**: Prompts (de-identified)
- **Data NOT Shared**: Raw user prompts, PII
- **Retention**: Internal Walmart network only
- **Security**: Internal SSL-verified endpoint
- **Approval**: Part of Walmart infrastructure

## Post-Contract Data Handling
- All data must be deleted within 30 days of contract termination
- No residual access to user data
- Annual certifications from vendors

## Compliance Checklist
- [ ] Vendor DPA reviewed by Legal
- [ ] Data classification documented
- [ ] Retention terms agreed upon
- [ ] Annual compliance certification
```

**Action Items**:
- [ ] Create data handling documentation for each vendor
- [ ] Get Legal approval for OpenAI/other external services
- [ ] Document data flow diagrams (where data goes, what's shared)
- [ ] Establish data deletion procedures with vendors
- [ ] Schedule annual vendor compliance reviews

---

## Medium Priority Issues (Recommended Before Scaling)

### 8. ⚠️ **MEDIUM: MFA Not Enforced**

**Finding**: Streamlit app lacks multi-factor authentication (MFA)
**Current**: SSO token provides single factor
**Walmart Requirement**: MFA required for all access

**Recommended Implementation**:
```python
# Configure Streamlit with MFA
# Option 1: Use Streamlit Cloud authentication (built-in MFA)
# Option 2: Integrate with Duo Security (Walmart-approved)

# src/security/mfa.py
import duo_client

class MFAManager:
    def __init__(self):
        self.admin_api = duo_client.Admin(
            ikey=os.getenv('DUO_IKEY'),
            skey=os.getenv('DUO_SKEY'),
            host=os.getenv('DUO_HOST')
        )

    def trigger_mfa(self, user_id: str) -> bool:
        """Trigger MFA challenge via Duo."""
        return self.admin_api.send_sms(
            user_id=user_id,
            message="Authenticate in Zorro"
        )
```

**Action Items**:
- [ ] Contact IT to enable Duo MFA integration
- [ ] Test MFA flow with Streamlit
- [ ] Document MFA setup for admins
- [ ] Monitor MFA adoption metrics

---

### 9. ⚠️ **MEDIUM: No API Rate Limiting**

**Finding**: Video generation API has no rate limits
**Risk**: Malicious users could abuse API, DoS attacks
**Walmart Requirement**: Rate limiting recommended for all APIs

**Implementation**:
```python
# Add to app.py using streamlit-limited
from streamlit_limited import limited

@limited(calls=10, period=60)  # 10 calls per minute
def generate_video_endpoint(message: str):
    # Video generation logic
    pass
```

**Action Items**:
- [ ] Implement rate limiting (10 calls/minute per user)
- [ ] Track usage by facility
- [ ] Alert on suspicious usage patterns

---

### 10. ⚠️ **MEDIUM: Incomplete Error Handling**

**Finding**: Some error messages may leak system information
**Risk**: Information disclosure vulnerability
**Recommendation**: Sanitize all error messages

**Implementation**:
```python
# src/utils/error_handler.py
def safe_error_response(error: Exception) -> str:
    """Return sanitized error message."""
    # Never expose stack traces to users
    if os.getenv('ENVIRONMENT') == 'production':
        return "An error occurred. Please contact support."
    else:
        return str(error)
```

---

## Low Priority Improvements

### 11. 📋 **LOW: Encryption at Rest Missing**

**Finding**: Generated videos stored unencrypted on disk
**Recommendation**: Encrypt video storage

**Optional Implementation**:
```python
from cryptography.fernet import Fernet

cipher = Fernet(os.getenv('ENCRYPTION_KEY'))
video_data = Path('video.mp4').read_bytes()
encrypted = cipher.encrypt(video_data)
Path('video.mp4.enc').write_bytes(encrypted)
```

---

### 12. 📋 **LOW: API Documentation Compliance**

**Finding**: No OpenAPI/Swagger documentation
**Recommendation**: Add API documentation for third-party integrations

---

---

## Compliance Checklist

### Before Production Deployment
- [ ] **CRITICAL**: Remove exposed OpenAI key from git history
- [ ] **CRITICAL**: Generate new OpenAI API key
- [ ] **CRITICAL**: Implement secret management (Azure Key Vault)
- [ ] **CRITICAL**: Enable SSL verification in production
- [ ] **CRITICAL**: Implement audit logging to SOC SIEM
- [ ] **CRITICAL**: Implement RBAC/ABAC access control
- [ ] **CRITICAL**: Document and implement data retention policy
- [ ] **HIGH**: Implement PII detection and masking
- [ ] **HIGH**: Document third-party data handling (DPA verification)
- [ ] **MEDIUM**: Implement MFA for Streamlit admin access
- [ ] **MEDIUM**: Add API rate limiting

### Before Enterprise-Wide Rollout
- [ ] Security review by Walmart CISO office
- [ ] SSP (Service Security Platform) approval
- [ ] Legal review of third-party data sharing
- [ ] SOC SIEM integration validated
- [ ] Load testing (capacity planning)
- [ ] Disaster recovery / business continuity testing

### Ongoing Compliance
- [ ] Monthly SIEM log reviews
- [ ] Quarterly vendor compliance reviews
- [ ] Annual security assessment
- [ ] Data retention audit (quarterly)

---

## Recommended Next Steps

### Immediate (This Week)
1. **Revoke exposed OpenAI key**
   - Contact OpenAI support
   - Generate new API key
   - Update in secure vault

2. **Implement SSL enforcement**
   - Change `SSL_VERIFY` default to `true`
   - Document CA bundle setup
   - Test in staging

3. **Set up SIEM forwarding**
   - Contact Walmart SOC team
   - Provision syslog endpoint
   - Test log forwarding

### Week 2-3
4. **Implement RBAC framework**
   - Design role hierarchy
   - Create permission model
   - Update Streamlit middleware

5. **Add audit logging**
   - Log all access events
   - Log all video generations
   - Verify SIEM receipt

### Week 4-6
6. **PII detection & masking**
   - Implement detection logic
   - Add message validation
   - Test with sample data

7. **Data retention automation**
   - Schedule cleanup job
   - Document retention policy
   - Create compliance report

### Month 2
8. **Security review**
   - Internal security audit
   - External penetration testing (optional)
   - SSP approval process

---

## SSP Portal Reference

**For questions about Walmart compliance requirements, visit**:
- **SSP Portal**: [http://wmlink.wal-mart.com/ssp](http://wmlink.wal-mart.com/ssp)
- **GenAI Guidelines**: [Walmart GenAI Getting Started](https://confluence.walmart.com/pages/viewpage.action?spaceKey=GA&title=Getting+Started+with+Generative+AI)
- **De-Identification Standard**: [DG-01-ST-02](https://one.walmart.com/content/uswire/en_us/work1/global-governance/digital-citizenship/data-policies/data_governance/dg-standards/dg-01-st-02.html)
- **Data Governance**: [Records and Information Management](https://one.walmart.com/content/uswire/en_us/work1/global-governance/digital-citizenship/manage-records/overview.html)

---

## Contact & Support

- **Security Questions**: Contact Walmart CISO office
- **Compliance Help**: SSP Portal support team
- **SOC Integration**: SOC team (soc@walmart.com)
- **Data Governance**: DG team

---

**Report Generated**: January 21, 2026
**Next Review**: February 21, 2026
**Status**: Ready for remediation planning
