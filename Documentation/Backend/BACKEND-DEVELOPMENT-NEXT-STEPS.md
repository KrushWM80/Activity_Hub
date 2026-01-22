# Activity Hub - Backend Development Next Steps
**Version:** 1.0  
**Date:** January 14, 2026  
**Purpose:** Focused backend development roadmap for Activity Hub

---

## Development Phases Overview

```
Phase 1 (Weeks 1-2): Compliance Setup & Architecture Review
├─ Architecture approval
├─ Budget authorization
├─ Team assignment
└─ Status: STARTING THIS WEEK

Phase 2 (Weeks 3-5): Black Out List Implementation
├─ Database schema
├─ Service layer
├─ Authentication integration
└─ Status: Next (blocked on Phase 1)

Phase 3 (Weeks 6-8): SOX Controls Hardening
├─ Segregation of duties
├─ Audit trails
├─ Financial data protection
└─ Status: Pending

Phase 4-6: MSO Integration, Encryption, Audit
└─ Status: Future
```

---

## Sprint 1: Compliance & Security Foundation (Weeks 1-2)

### Backend Tasks (This Sprint)

#### Task 1.1: Security Audit
**Owner:** Backend Lead  
**Effort:** 2 days  
**Acceptance Criteria:**
```
✓ SSO integration verified (Walmart SSO working)
✓ JWT token generation working (8-hour expiration)
✓ Token validation on all API endpoints
✓ RBAC enforced (role-based access control)
✓ No hardcoded credentials in code
✓ All secrets in AWS Secrets Manager
```

**Deliverables:**
- Security audit report
- List of gaps found
- Remediation plan

#### Task 1.2: Encryption Assessment
**Owner:** Database Lead  
**Effort:** 2 days  
**Acceptance Criteria:**
```
✓ All HTTPS/TLS 1.2+ on API endpoints
✓ Data classification documented (PII, financial, etc.)
✓ Encryption at rest strategy defined
✓ Encryption key management plan documented
```

**Deliverables:**
- Data classification matrix
- Encryption implementation plan
- Key management procedures

#### Task 1.3: Audit Logging Setup
**Owner:** Backend Lead  
**Effort:** 2 days  
**Acceptance Criteria:**
```
✓ API access logging configured
✓ Database change logging enabled
✓ No PII in logs
✓ Log retention policy documented
✓ Alerting configured for suspicious activity
```

**Deliverables:**
- Audit logging configuration
- Sample logs reviewed
- Alerting rules documented

---

## Sprint 2: Black Out List Implementation (Weeks 3-5)

### Database Schema (Week 3)

```sql
-- Create blackout_list table
CREATE TABLE blackout_list (
    id SERIAL PRIMARY KEY,
    associate_id VARCHAR(255) NOT NULL UNIQUE,
    associate_email VARCHAR(255) NOT NULL,
    restriction_type VARCHAR(50), -- 'sox_financial', 'confidential', etc
    restriction_categories JSONB, -- ['financial_kpis', 'approval_workflows']
    effective_date TIMESTAMP,
    expiration_date TIMESTAMP,
    enforced_at_login BOOLEAN DEFAULT TRUE,
    enforced_at_api BOOLEAN DEFAULT TRUE,
    created_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create audit log for blackout list
CREATE TABLE blackout_audit_log (
    id SERIAL PRIMARY KEY,
    associate_id VARCHAR(255),
    action VARCHAR(50), -- 'login_denied', 'access_blocked', 'added', 'removed'
    category VARCHAR(100),
    timestamp TIMESTAMP DEFAULT NOW(),
    ip_address VARCHAR(45),
    user_agent TEXT,
    reason TEXT
);
```

### Backend Service (Week 3-4)

```python
# app/services/blackout_service.py
from sqlalchemy.orm import Session
from app.db.models import BlackoutList

class BlackoutListService:
    
    @staticmethod
    def is_user_blacklisted(db: Session, user_id: str, category: str = None) -> bool:
        """
        Check if user is on blackout list
        Returns: True if blacklisted, False otherwise
        """
        blackout = db.query(BlackoutList).filter(
            BlackoutList.associate_id == user_id,
            BlackoutList.enforced_at_login == True,
            BlackoutList.effective_date <= datetime.now(),
            BlackoutList.expiration_date > datetime.now()
        ).first()
        
        if not blackout:
            return False
        
        if category and category in blackout.restriction_categories:
            return True
        
        return blackout is not None
    
    @staticmethod
    def log_blackout_attempt(db: Session, user_id: str, action: str):
        """Log access attempt to audit trail"""
        log_entry = BlackoutAuditLog(
            associate_id=user_id,
            action=action,
            timestamp=datetime.now()
        )
        db.add(log_entry)
        db.commit()
```

### Authentication Integration (Week 4)

```python
# app/core/dependencies.py - UPDATED
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current user with Black Out List check"""
    
    # 1. Validate JWT token
    user = validate_token(token)
    
    # 2. Check if user is on blackout list (PRE-LOGIN)
    if BlackoutListService.is_user_blacklisted(db, user.id):
        BlackoutListService.log_blackout_attempt(db, user.id, "login_denied")
        raise HTTPException(
            status_code=403,
            detail="Access denied - user restrictions"
        )
    
    # 3. Load user from database
    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user
```

### Testing (Week 5)

```
□ Unit Tests:
  - Test blackout check returns correct value
  - Test with multiple categories
  - Test expiration logic
  
□ Integration Tests:
  - Test login denied for blackout user
  - Test audit log entry created
  - Test non-blackout users can login
  
□ Performance Tests:
  - Blackout check < 100ms
  - No N+1 queries
  - Database indexed properly
```

---

## Sprint 3: SOX Controls (Weeks 6-8)

### Segregation of Duties

```python
# In approval workflow service
def approve_activity(db: Session, activity_id: int, approver_id: str):
    """Approve activity with segregation of duties check"""
    
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    # Check: Cannot approve own activity
    if activity.created_by == approver_id:
        raise HTTPException(
            status_code=403,
            detail="Cannot approve own activities (SOX compliance)"
        )
    
    # Check: If financial data, must be different role
    if activity.is_sox_restricted:
        creator_role = db.query(User).filter(User.id == activity.created_by).first().role
        approver_role = db.query(User).filter(User.id == approver_id).first().role
        
        if creator_role == approver_role:
            raise HTTPException(
                status_code=403,
                detail="Cannot approve financial activities within same role"
            )
    
    # Proceed with approval
    activity.approved_by = approver_id
    activity.approved_at = datetime.now()
    db.commit()
```

### Immutable Audit Logs

```python
# app/db/models.py - NEW TABLE
class AuditLogImmutable(Base):
    __tablename__ = "audit_log_immutable"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    user_id = Column(String(255))
    action = Column(String(100))
    table_name = Column(String(100))
    record_id = Column(Integer)
    data_before = Column(JSON)
    data_after = Column(JSON)
    hash_value = Column(String(256))  # SHA-256 of entry
    previous_hash = Column(String(256))  # For hash chain
    
    # Constraints to make append-only
    __table_args__ = (
        # No UPDATE/DELETE allowed (database level)
    )
```

---

## Sprint 4: MSO Integration (Weeks 9-11)

### API Integration with Encryption

```python
# app/services/mso_service.py
from cryptography.fernet import Fernet
import openai

class MSO_Service:
    
    @staticmethod
    def call_azure_openai_with_encryption(
        prompt: str,
        data: str,
        is_sensitive: bool = False
    ) -> str:
        """Call Azure OpenAI with encryption for sensitive data"""
        
        # 1. Classify data
        if is_sensitive:
            # 2. Encrypt before transmission
            cipher = Fernet(get_encryption_key())
            encrypted_data = cipher.encrypt(data.encode())
            transmission_data = encrypted_data.decode()
        else:
            transmission_data = data
        
        # 3. Log the call
        AuditService.log_mso_call(
            action="openai_api_call",
            user_id=current_user.id,
            data_encrypted=is_sensitive
        )
        
        # 4. Call MSO
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"{prompt}\n\n{transmission_data}"}]
        )
        
        return response.choices[0].message.content
```

---

## Sprint 5: Encryption & Hardening (Weeks 12-14)

### Database Encryption at Rest

```
□ PostgreSQL pgcrypto Extension
  - Enable: CREATE EXTENSION pgcrypto;
  - Encrypt: PII fields (email, name, phone)
  - Encrypt: Financial data fields
  - Key management: AWS Secrets Manager

□ Test Encryption
  - Verify: Encrypted data in database
  - Verify: Decryption works
  - Performance: < 5% overhead
  - Backups: Encryption includes backups
  - Recovery: Disaster recovery tested
```

### TLS & HTTPS Enforcement

```
□ Certificate: AWS Certificate Manager
□ Protocol: TLS 1.2+ only
□ Headers: HSTS enabled
□ Ciphers: Strong cipher suites only
□ Testing: SSL Labs A+ rating
```

### MFA Implementation

```python
# For admin roles
@router.post("/auth/mfa-setup")
def setup_mfa(user_id: str, db: Session = Depends(get_db)):
    """Generate TOTP secret for MFA"""
    
    if not is_admin(user_id):
        raise HTTPException(status_code=403)
    
    secret = pyotp.random_base32()
    # Store secret in database (encrypted)
    # Return QR code to user
    
    return {"qr_code": generate_qr_code(secret)}

@router.post("/auth/login-mfa")
def login_with_mfa(username: str, password: str, mfa_code: str):
    """Login with MFA verification"""
    
    user = verify_credentials(username, password)
    
    if not verify_mfa_code(user.id, mfa_code):
        raise HTTPException(status_code=401, detail="Invalid MFA code")
    
    return {"token": generate_jwt_token(user)}
```

---

## Development Checklist - Priority Order

### Week 1-2 (Immediate)
```
□ Verify SSO working
□ Confirm JWT expiration (8 hours)
□ Test HTTPS/TLS 1.2+
□ Document security audit findings
□ Review existing audit logging
```

### Week 3-5 (Black Out List)
```
□ Database schema: blackout_list tables
□ Service layer: BlackoutListService
□ Authentication: Pre-login check
□ Testing: Unit + integration tests
□ Deployment: Dev environment
```

### Week 6-8 (SOX)
```
□ Segregation of duties enforcement
□ Immutable audit log tables
□ Financial data marking
□ Approval workflow updates
□ SOD testing
```

### Week 9-11 (MSO)
```
□ Azure OpenAI integration
□ Encryption before API call
□ Audit logging for MSO calls
□ Error handling & failover
□ Testing
```

### Week 12-14 (Encryption)
```
□ Database encryption at rest
□ TLS 1.2+ enforcement
□ MFA for admins
□ Secrets management
□ Final testing & deployment
```

---

## Code Files to Modify/Create

```
CREATE:
- app/services/blackout_service.py
- app/services/audit_service.py
- app/services/mso_service.py
- app/middleware/security_middleware.py
- tests/test_blackout_service.py
- tests/test_audit_logging.py

MODIFY:
- app/core/dependencies.py (add blackout check)
- app/db/models.py (add blackout tables, data classification)
- app/api/v1/endpoints/*.py (add audit logging)
- app/core/config.py (security settings)
- app/main.py (middleware registration)

DOCUMENTATION:
- SECURITY.md (new)
- AUDIT-LOGGING.md (new)
- DATA-CLASSIFICATION.md (new)
- DEPLOYMENT-CHECKLIST.md (update)
```

---

## Success Metrics

```
By End of Phase 1 (Week 2):
✓ Security audit complete
✓ Gaps identified and documented
✓ Remediation plan created
✓ Team ready for Phase 2

By End of Phase 2 (Week 5):
✓ Black Out List deployed
✓ 100% audit logging rate
✓ < 100ms per blackout check
✓ All tests passing

By End of Phase 3 (Week 8):
✓ SOX controls enforced
✓ Segregation of duties working
✓ Immutable audit logs in place

By End of Phase 4 (Week 11):
✓ MSO integration live
✓ Encryption before transmission
✓ All MSO calls audited

By End of Phase 5 (Week 14):
✓ All data encrypted at rest
✓ TLS 1.2+ enforced
✓ MFA working for admins
✓ Production ready
```

---

**Owner:** Backend Development Team  
**Status:** Ready for Phase 1  
**Next Review:** End of Week 2

