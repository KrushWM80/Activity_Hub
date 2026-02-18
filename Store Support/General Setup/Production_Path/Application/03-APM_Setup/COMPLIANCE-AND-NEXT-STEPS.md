# APM Compliance & Next Steps - Review Checklist
**Version:** 1.0  
**Date:** January 14, 2026  
**Purpose:** Compliance requirements and next development steps

---

## Part 1: Compliance Standards Overview (Review Before Starting)

### Quick Decision Tree - Does APM Need Compliance?

```
Question 1: Will APM handle financial data?
├─ YES → SOX Applies ✅
│  └─ Requires: Segregation of duties, audit trails, Black Out List
│
└─ NO → Continue

Question 2: Will APM have 50+ users?
├─ YES → SOC 2 Type II May Apply ✅
│  └─ Requires: Security controls documentation, audit logging
│
└─ NO → Continue

Question 3: Will APM use third-party AI (OpenAI, Google, etc.)?
├─ YES → DPA Required ✅
│  └─ Requires: Legal approval, encryption, data classification
│
└─ NO → Minimal compliance needed
```

### Key Control Checklist (Required if any above = YES)

```
☑ MUST HAVE (All projects):
  □ Authentication (SSO, strong passwords)
  □ Encryption in transit (TLS 1.2+, HTTPS)
  □ Access control (RBAC)
  □ Audit logging (who, what, when)
  □ Change management (code review)

☑ IF FINANCIAL DATA (SOX):
  □ Black Out List (pre-login access control)
  □ Segregation of duties (no self-approval)
  □ Immutable audit logs (7-10 year retention)
  □ Encrypted databases
  □ Financial data classification

☑ IF 50+ USERS (SOC 2):
  □ All above + complete documentation
  □ System Security Plan (SSP)
  □ Risk assessment
  □ Incident response plan
  □ Annual external audit

☑ IF USING 3RD-PARTY AI (DPA):
  □ Data Processing Agreement signed
  □ Encrypt data before sending to AI
  □ Data minimization (send only what's needed)
  □ Audit logging of all API calls
  □ Vendor SOC 2 Type II verified
```

---

## Part 2: Backend Development Next Steps

### Immediate Actions (This Sprint)

#### Step 1: Architecture & Authentication
```
Priority: 🔴 CRITICAL

Task 1.1: Review existing SSO integration
- Verify Walmart SSO is configured
- Test JWT token generation (8-hour expiration)
- Confirm token validation in all endpoints
- Document: SSO flow in README

Task 1.2: Implement MFA for admin roles (if not present)
- Enable TOTP or SMS-based MFA
- Enforce for admin/compliance access only
- Document recovery procedures

Task 1.3: Verify RBAC implementation
- Confirm 8 role types defined in database
- Test role-based access control
- Verify role-based data filtering
- Document: Role definitions & permissions
```

#### Step 2: Database & Data Protection
```
Priority: 🔴 CRITICAL

Task 2.1: Data Classification
- Identify all financial data fields (PII, financial, etc.)
- Mark financial fields with is_restricted = TRUE
- Document: Data classification mapping
- Create: Data dictionary

Task 2.2: Encryption at Rest
- Enable PostgreSQL pgcrypto (if on prod DB)
- Identify which fields need encryption:
  - All PII (emails, names, phone)
  - All financial data
  - Sensitive personal info
- Document: Encryption key management
- Test: Backup/recovery with encryption

Task 2.3: Encryption in Transit
- Verify all API endpoints use HTTPS/TLS 1.2+
- Remove any HTTP endpoints
- Configure HSTS headers
- Test: SSL Labs scan for A+ rating
```

#### Step 3: Audit Logging
```
Priority: 🔴 CRITICAL

Task 3.1: API Access Logging
- Log all API calls (user, endpoint, timestamp, outcome)
- Ensure PII is NOT logged in plaintext
- Create: Audit log schema (if not present)
- Test: Verify logging is working
- Document: Audit log retention policy

Task 3.2: Change Logging
- Log all database changes (INSERT, UPDATE, DELETE)
- Include: Before/after values, user, timestamp
- Implement: Append-only audit log table
- Test: Verify immutability constraints
- Document: Change logging procedures

Task 3.3: Alerting
- Set up real-time alerts for:
  - Failed authentication attempts
  - Unusual data access patterns
  - Restricted data access
  - Configuration changes
- Document: Alert response procedures
```

#### Step 4: Secrets Management
```
Priority: 🟠 HIGH

Task 4.1: Remove Hardcoded Secrets
- Scan code for API keys, passwords, tokens
- Remove from: Source code, .env files, config
- Store in: AWS Secrets Manager or equivalent
- Test: Application works with secrets manager
- Document: Secrets management procedures

Task 4.2: API Key Rotation
- Implement quarterly key rotation
- Automate if possible
- Document: Key rotation process
- Create: Runbook for manual rotation if needed
```

#### Step 5: Access Control - Segregation of Duties
```
Priority: 🟠 HIGH

Task 5.1: Segregation of Duties for Financial Data
- Prevent: No one can approve their own requests
- Implement: creator_id ≠ approver_id check
- Test: Verify workflow enforcement
- Document: SOD procedures

Task 5.2: Development vs Production Access
- Ensure: Dev team cannot access production databases
- Implement: Network segregation or IAM policies
- Test: Verify access controls
- Document: Access policies
```

---

### Sprint Planning (Weeks 1-4)

**Week 1: Assessment & Planning**
```
□ Review current backend code for security gaps
□ Identify missing compliance controls
□ Assess data encryption status
□ Create detailed implementation plan
□ Estimate effort & timeline
```

**Week 2: Authentication & SSO**
```
□ Verify SSO integration working
□ Implement MFA for admins
□ Test authentication flow
□ Document procedures
```

**Week 3: Data Protection & Encryption**
```
□ Classify all data fields
□ Implement encryption at rest
□ Verify encryption in transit (TLS 1.2+)
□ Test backup/recovery with encryption
```

**Week 4: Logging & Monitoring**
```
□ Implement audit logging
□ Configure alerting
□ Test logging procedures
□ Document retention policies
```

---

### Code Changes Required

#### File: app/core/dependencies.py
```python
# ADD: Pre-login blackout check (if SOX applies)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Existing JWT validation
    user = validate_token(token)
    
    # ADD THIS: Check if user is on blackout list
    # if is_user_blacklisted(user.id):
    #     raise HTTPException(status_code=403, detail="Access denied")
    
    return user
```

#### File: app/core/logging_config.py
```python
# VERIFY: Audit logging is enabled
# VERIFY: PII masking in logs (no plaintext emails/names)
# ADD: Real-time alerting for suspicious activity
# ADD: Immutable append-only log storage
```

#### File: app/db/models.py
```python
# ADD (if not present): data_classification field
class Activity(Base):
    __tablename__ = "activities"
    
    # Existing fields...
    
    # ADD: Financial data flag
    is_sox_restricted = Column(Boolean, default=False)
    is_confidential = Column(Boolean, default=False)
```

#### File: app/services/audit_service.py (NEW)
```python
# CREATE: Immutable audit logging service
# Methods:
# - log_api_call(user_id, endpoint, method, outcome)
# - log_data_change(user_id, table, action, before, after)
# - log_restricted_access(user_id, resource, result)
# Properties:
# - Append-only (no UPDATE/DELETE)
# - Encrypted at rest
# - Hash chain for integrity
```

---

### Testing Checklist

#### Security Testing
```
□ SQL injection prevention (parameterized queries)
□ XSS prevention (output encoding)
□ CSRF protection (token validation)
□ Authentication bypass attempts (fail securely)
□ Authorization bypass (RBAC enforcement)
□ Data exposure (encryption verified)
```

#### Compliance Testing
```
□ SOX: Segregation of duties enforced
□ SOX: Audit logs immutable
□ SOX: Financial data encrypted
□ SOX: Access control working
□ Audit: All API calls logged
□ Encryption: At rest & in transit
□ Data Classification: Accurate & enforced
```

---

### Documentation Requirements

**Create/Update:**
```
□ SECURITY.md - Security overview for developers
□ AUDIT-LOGGING.md - Audit trail documentation
□ DATA-CLASSIFICATION.md - Data types & sensitivity
□ API-ENDPOINTS.md - Authentication & authorization per endpoint
□ DEPLOYMENT.md - Security checklist for deployment
□ INCIDENT-RESPONSE.md - Procedures for security incidents
```

---

### Success Metrics (By End of Sprint)

```
✓ All API endpoints use TLS 1.2+ (100% compliance)
✓ All sensitive data encrypted at rest
✓ All user actions logged (100% coverage)
✓ MFA enforced for admin roles
✓ Secrets removed from code
✓ RBAC verified working
✓ No hardcoded credentials
✓ Documentation complete
```

---

## Part 3: Related Resources

### In Compliance Folder (General Setup/Compliance)
- `COMPLIANCE-STANDARDS-FRAMEWORK.md` - Detailed frameworks
- `AI-POLICY.md` - AI/ML usage guidelines
- `README.md` - Navigation guide

### For Complete Activity Hub Context
- See Activity Hub repository for detailed compliance analysis
- Refer to Security-Compliance-Review.md for gap analysis
- Reference SOX implementation guide for Black Out List details

---

## Approval & Sign-Off

```
□ Backend Lead: ________________________ Date: _____
□ Security Review: _____________________ Date: _____
□ Compliance Officer: __________________ Date: _____
```

---

**Next Review:** After first sprint completion  
**Status:** ✅ Ready for development

