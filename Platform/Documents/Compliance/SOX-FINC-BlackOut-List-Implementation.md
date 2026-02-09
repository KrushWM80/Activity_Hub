# SOX/FINC Compliance: Black Out List & Access Control Implementation
**Date:** January 14, 2026  
**Status:** Implementation Requirements & Architecture  
**Priority:** 🔴 CRITICAL - Pre-Login Enforcement Required

---

## EXECUTIVE SUMMARY

Activity Hub must implement a **Black Out List** mechanism that prevents restricted associates from accessing SOX/FINC-related data. This list must be checked **at or before login** to enforce access restrictions across all application layers.

---

## 1. BLACK OUT LIST REQUIREMENTS

### 1.1 What is the Black Out List?

**Definition:** A centralized registry of Walmart associates who are restricted from accessing financial/SOX data due to:
- Conflicts of interest
- Regulatory restrictions
- HR/Compliance hold orders
- Union/labor restrictions
- Segregation of duties violations
- Temporary compliance holds

### 1.2 Why Pre-Login Enforcement?

**Security Principle:** Deny-at-entry (prevent login if restricted) rather than deny-at-access (allow login but hide data)

**Benefits:**
- ✅ Cannot be bypassed by URL manipulation
- ✅ Cannot access via API if login denied
- ✅ Audit trail shows attempted unauthorized access
- ✅ Compliance-aligned with SOX segregation requirements
- ✅ Prevents accidental exposure during session

---

## 2. BLACK OUT LIST DATA STRUCTURE

### 2.1 Database Schema

```sql
-- Create blackout_list table
CREATE TABLE blackout_list (
    id SERIAL PRIMARY KEY,
    associate_id INTEGER NOT NULL,
    associate_email VARCHAR(255) NOT NULL,
    associate_name VARCHAR(255) NOT NULL,
    
    -- Restriction details
    restriction_type VARCHAR(50) NOT NULL,  -- 'sox_financial', 'conflict_of_interest', 'compliance_hold', 'union_restriction', etc.
    restriction_reason TEXT NOT NULL,
    restriction_categories JSONB NOT NULL,  -- ['kpi_financial', 'approval_workflows', 'budget_data', etc.]
    
    -- Validity period
    effective_date TIMESTAMP NOT NULL,
    expiration_date TIMESTAMP,  -- NULL = indefinite
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Enforcement
    enforced_at_login BOOLEAN DEFAULT TRUE,  -- Must check at login
    enforced_at_api BOOLEAN DEFAULT TRUE,    -- Must check at API access
    notify_user_on_restriction BOOLEAN DEFAULT FALSE,  -- Show warning message
    
    -- Audit trail
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_by VARCHAR(255),
    modified_at TIMESTAMP,
    reason_for_change TEXT,
    
    -- Indexes for performance
    UNIQUE(associate_id, effective_date),
    INDEX idx_active_blackouts (is_active, effective_date),
    INDEX idx_email_lookup (associate_email),
    INDEX idx_expiration (expiration_date)
);

-- Create blackout_categories table (for data granularity)
CREATE TABLE blackout_categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    data_types JSONB,  -- What data this category restricts
    
    -- Examples:
    -- 'kpi_financial': Financial KPI metrics
    -- 'approval_workflows': Approval processes for financial activities
    -- 'budget_data': Budget and spend data
    -- 'executive_dashboards': Executive-only reports
    -- 'audit_trail': Financial audit logs
    -- 'personnel_decisions': HR decisions based on performance
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create blackout_audit_log table (for compliance)
CREATE TABLE blackout_audit_log (
    id SERIAL PRIMARY KEY,
    associate_id INTEGER,
    associate_email VARCHAR(255),
    
    -- Access attempt
    event_type VARCHAR(50),  -- 'login_denied', 'api_call_denied', 'data_access_denied', 'restriction_added', 'restriction_removed'
    event_timestamp TIMESTAMP DEFAULT NOW(),
    
    -- Details
    blackout_reason VARCHAR(50),
    restricted_categories TEXT[],  -- Categories they tried to access
    
    -- Request details
    ip_address VARCHAR(45),
    user_agent TEXT,
    endpoint VARCHAR(500),  -- Which API endpoint if applicable
    
    -- Result
    action_taken VARCHAR(50),  -- 'denied', 'allowed_with_audit', 'escalated'
    escalation_details TEXT,
    
    -- Compliance
    reviewed_by VARCHAR(255),
    review_date TIMESTAMP,
    
    INDEX idx_denied_logins (event_type, event_timestamp),
    INDEX idx_associate_email (associate_email)
);
```

### 2.2 Blackout List Categories

```json
{
  "restriction_categories": {
    "kpi_financial": {
      "description": "Financial KPI metrics (revenue, margin, costs)",
      "data_tables": ["kpis"],
      "fields": ["current_value", "target_value", "trend_direction"],
      "dashboard_widgets": ["revenue_growth", "efficiency_metrics", "cost_analysis"]
    },
    "approval_workflows": {
      "description": "Approval processes for financial activities",
      "data_tables": ["activities", "approvals"],
      "operations": ["create_approval", "review_approval", "submit_approval"],
      "dashboard_widgets": ["pending_approvals", "approval_pipeline"]
    },
    "budget_data": {
      "description": "Budget and spend data",
      "data_tables": ["budgets", "spend_tracking"],
      "fields": ["budget_amount", "actual_spend", "variance"],
      "api_endpoints": ["/api/v1/budgets/*", "/api/v1/spend/*"]
    },
    "executive_dashboards": {
      "description": "Executive-only financial dashboards",
      "dashboard_ids": ["executive_dashboard", "board_reporting"],
      "role_required": ["c-level-executive", "vice-president"]
    },
    "audit_trail": {
      "description": "Financial audit logs and change history",
      "data_tables": ["audit_logs", "integration_logs"],
      "api_endpoints": ["/api/v1/audit/*"]
    },
    "personnel_decisions": {
      "description": "Performance data used for employment decisions",
      "data_fields": ["activity_completion_rate", "performance_score"],
      "use_case_restriction": "Cannot use for promotion/termination decisions"
    }
  }
}
```

---

## 3. PRE-LOGIN BLACKOUT CHECK IMPLEMENTATION

### 3.1 Authentication Flow with Blackout Check

```
┌──────────────────────────────────────────────────────────────┐
│                    USER LOGIN FLOW                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. User submits email + password                           │
│     ↓                                                        │
│  2. Validate credentials with Walmart SSO                   │
│     ↓                                                        │
│  3. ⭐ NEW: CHECK BLACKOUT LIST ⭐ (BEFORE JWT generation) │
│     ├─ Query blackout_list table                           │
│     ├─ Check if associate_email is active + not expired    │
│     ├─ If FOUND: DENY LOGIN                                │
│     │   ├─ Log attempt in blackout_audit_log               │
│     │   ├─ Send audit alert to compliance team             │
│     │   ├─ Return error: "Access denied due to compliance  │
│     │   │   restriction. Contact [compliance_contact]"     │
│     │   └─ Exit                                            │
│     │                                                        │
│     └─ If NOT FOUND: Continue                              │
│     ↓                                                        │
│  4. Generate JWT token (8-hour expiration)                 │
│     ↓                                                        │
│  5. Create Redis session                                    │
│     ├─ Store user_id                                       │
│     ├─ Store restricted_categories (if any)                │
│     └─ Store blackout_status (for middleware)              │
│     ↓                                                        │
│  6. Return token to client                                 │
│     ↓                                                        │
│  7. User can now access dashboard                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 Python Implementation (FastAPI)

```python
# app/core/blackout_check.py
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.models import User, BlackoutList, BlackoutAuditLog
import structlog

logger = structlog.get_logger(__name__)

class BlackoutListService:
    """Service for managing SOX/FINC blackout list checks"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def is_user_blacklisted(self, email: str) -> tuple[bool, dict]:
        """
        Check if user is on blackout list (pre-login check)
        
        Returns:
            (is_blacklisted: bool, blackout_details: dict)
        """
        # Query active blackout records for this email
        blackout = self.db.query(BlackoutList).filter(
            BlackoutList.associate_email == email.lower(),
            BlackoutList.is_active == True,
            BlackoutList.effective_date <= datetime.utcnow(),
            # Check expiration (NULL means indefinite)
            (BlackoutList.expiration_date > datetime.utcnow()) | 
            (BlackoutList.expiration_date == None)
        ).first()
        
        if blackout:
            # Log this access attempt
            self._log_denied_access(
                email=email,
                reason=blackout.restriction_reason,
                categories=blackout.restriction_categories,
                event_type="login_denied"
            )
            
            return True, {
                "restriction_reason": blackout.restriction_reason,
                "restriction_type": blackout.restriction_type,
                "categories": blackout.restriction_categories,
                "effective_date": blackout.effective_date.isoformat(),
                "expiration_date": blackout.expiration_date.isoformat() if blackout.expiration_date else None,
                "notify_user": blackout.notify_user_on_restriction
            }
        
        return False, {}
    
    def _log_denied_access(self, email: str, reason: str, categories: list, event_type: str):
        """Log blackout list denial for audit trail"""
        audit_log = BlackoutAuditLog(
            associate_email=email,
            event_type=event_type,
            event_timestamp=datetime.utcnow(),
            blackout_reason=reason,
            restricted_categories=categories,
            action_taken="denied"
        )
        self.db.add(audit_log)
        self.db.commit()
        
        # Alert compliance team
        logger.info(
            "blackout_list_denial",
            email=email,
            reason=reason,
            event_type=event_type,
            categories=categories
        )
    
    def get_user_restricted_categories(self, user_id: int) -> list:
        """
        Get restricted categories for logged-in user
        (Some users may have partial restrictions - check on every API call)
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        
        blackout = self.db.query(BlackoutList).filter(
            BlackoutList.associate_email == user.email.lower(),
            BlackoutList.is_active == True,
            BlackoutList.enforced_at_api == True
        ).first()
        
        if blackout:
            return blackout.restriction_categories
        
        return []

# app/api/auth.py
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.blackout_check import BlackoutListService
from app.db.session import get_db
from app.db.models import User

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
async def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """
    Login endpoint with SOX/FINC blackout list enforcement
    """
    
    # Step 1: Validate email/password with Walmart SSO
    user = authenticate_with_sso(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # ⭐ STEP 2: CHECK BLACKOUT LIST (PRE-TOKEN GENERATION)
    blackout_service = BlackoutListService(db)
    is_blacklisted, blackout_details = blackout_service.is_user_blacklisted(email)
    
    if is_blacklisted:
        logger.warning(
            "login_denied_blackout",
            email=email,
            reason=blackout_details.get("restriction_reason")
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied due to compliance restriction. "
                   f"Reason: {blackout_details.get('restriction_reason')}. "
                   f"Contact compliance@walmart.com for assistance."
        )
    
    # Step 3: Generate JWT token
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    # Step 4: Create Redis session
    restricted_categories = blackout_service.get_user_restricted_categories(user.id)
    
    redis_session = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "restricted_categories": restricted_categories,
        "login_time": datetime.utcnow().isoformat(),
        "blackout_status": "checked"
    }
    
    # Store in Redis with 8-hour TTL
    redis_client.setex(
        f"session:{user.id}",
        settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        json.dumps(redis_session)
    )
    
    logger.info(
        "user_login_successful",
        email=email,
        has_restrictions=len(restricted_categories) > 0
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "restricted_categories": restricted_categories
    }

def authenticate_with_sso(email: str, password: str) -> User:
    """Validate credentials with Walmart SSO (external service)"""
    # Call Walmart SSO validation endpoint
    # Return user if valid, None if invalid
    pass

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=8)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
```

---

## 4. API-LEVEL ACCESS CONTROL (Per-Request Enforcement)

### 4.1 Middleware for Data Access Validation

```python
# app/middleware/blackout_check_middleware.py
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
import json

class BlackoutCheckMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce blackout restrictions on every API call
    Prevents accessing restricted data even if login check bypassed
    """
    
    # Protected endpoints that require blackout check
    PROTECTED_ENDPOINTS = {
        "/api/v1/kpis": ["kpi_financial", "executive_dashboards"],
        "/api/v1/kpis/financial": ["kpi_financial"],
        "/api/v1/analytics/executive": ["executive_dashboards"],
        "/api/v1/analytics/board-report": ["executive_dashboards"],
        "/api/v1/activities/approval": ["approval_workflows"],
        "/api/v1/budgets": ["budget_data"],
        "/api/v1/audit": ["audit_trail"],
    }
    
    async def dispatch(self, request: Request, call_next):
        # Check if this is a protected endpoint
        path = request.url.path
        restricted_categories = []
        
        for protected_path, categories in self.PROTECTED_ENDPOINTS.items():
            if path.startswith(protected_path):
                restricted_categories = categories
                break
        
        if not restricted_categories:
            # Not a protected endpoint, proceed normally
            return await call_next(request)
        
        # Get user from session/token
        user_id = request.headers.get("X-User-ID")
        user_session = redis_client.get(f"session:{user_id}")
        
        if not user_session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired"
            )
        
        session_data = json.loads(user_session)
        user_restricted = session_data.get("restricted_categories", [])
        
        # Check if user has restriction that applies to this endpoint
        for category in restricted_categories:
            if category in user_restricted:
                logger.warning(
                    "api_access_denied_blackout",
                    user_id=user_id,
                    endpoint=path,
                    restricted_category=category
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied to {path}. "
                           f"You have a compliance restriction on: {category}"
                )
        
        # User is allowed, proceed
        response = await call_next(request)
        return response
```

### 4.2 Endpoint-Level Decorators

```python
# app/dependencies/blackout_decorators.py
from functools import wraps
from fastapi import Depends, HTTPException, status
from app.core.dependencies import get_current_user

def require_sox_access(required_categories: list = None):
    """
    Decorator to enforce SOX/FINC access requirements
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            # Check if user is on blackout list
            blackout_service = BlackoutListService(kwargs.get('db'))
            is_blacklisted, details = blackout_service.is_user_blacklisted(current_user.email)
            
            if is_blacklisted:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied: {details['restriction_reason']}"
                )
            
            # If specific categories required, check those too
            if required_categories:
                user_restricted = blackout_service.get_user_restricted_categories(current_user.id)
                for category in required_categories:
                    if category in user_restricted:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Access denied to SOX data category: {category}"
                        )
            
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage in endpoints:
@router.get("/api/v1/kpis/financial")
@require_sox_access(required_categories=["kpi_financial"])
async def get_financial_kpis(current_user: User = Depends(get_current_user)):
    """Get financial KPIs - SOX/FINC restricted"""
    # Only accessible if user passes blackout check
    pass
```

---

## 5. DATA LAYER AWARENESS & CONDITIONAL RENDERING

### 5.1 Data Filtering at Query Level

```python
# app/db/models.py - Add to KPI model
class KPI(Base):
    __tablename__ = "kpis"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    # ... other fields ...
    
    # NEW: Access control fields
    is_sox_restricted = Column(Boolean, default=False)  # Marks SOX/FINC data
    restricted_categories = Column(JSON)  # Which categories restrict this
    requires_segregation_of_duties = Column(Boolean, default=False)

# app/services/kpi_service.py
class KPIService:
    def get_kpis_for_user(self, user_id: int, db: Session) -> List[KPI]:
        """
        Get KPIs filtered by user's access level
        Remove SOX-restricted KPIs if user is blacklisted
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        # Get user's restricted categories
        blackout_service = BlackoutListService(db)
        user_restricted = blackout_service.get_user_restricted_categories(user_id)
        
        # Build query - exclude restricted KPIs
        query = db.query(KPI)
        
        if "kpi_financial" in user_restricted:
            query = query.filter(KPI.is_sox_restricted == False)
        
        if "budget_data" in user_restricted:
            query = query.filter(
                ~KPI.restricted_categories.contains("budget_data")
            )
        
        return query.all()
```

### 5.2 Frontend Awareness

```typescript
// Frontend: React Component - Conditional rendering based on restrictions
import { useAuth } from '@/hooks/useAuth';

export const FinancialDashboard = () => {
  const { user, restrictedCategories } = useAuth();
  
  const canViewFinancials = !restrictedCategories.includes('kpi_financial');
  const canViewBudgets = !restrictedCategories.includes('budget_data');
  const canViewApprovals = !restrictedCategories.includes('approval_workflows');
  
  if (!canViewFinancials) {
    return (
      <ErrorMessage 
        title="Access Restricted"
        message="You do not have permission to view financial data."
        contact="compliance@walmart.com"
      />
    );
  }
  
  return (
    <div>
      {canViewFinancials && <FinancialKPICard />}
      {canViewBudgets && <BudgetChart />}
      {canViewApprovals && <ApprovalWorkflow />}
    </div>
  );
};
```

---

## 6. BLACKOUT LIST MANAGEMENT INTERFACE

### 6.1 Admin Portal for Compliance Team

```python
# app/api/admin/blackout_management.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(prefix="/api/v1/admin/blackout", tags=["admin-blackout"])

@router.post("/associate")
async def add_to_blackout_list(
    associate_email: str,
    restriction_type: str,
    restriction_reason: str,
    categories: List[str],
    expiration_date: Optional[datetime] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Add associate to blackout list
    Only accessible to compliance admins
    """
    # Verify user has admin rights
    if current_user.role not in ["admin", "compliance_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only compliance admins can modify blackout list"
        )
    
    # Create blackout entry
    blackout = BlackoutList(
        associate_email=associate_email.lower(),
        restriction_type=restriction_type,
        restriction_reason=restriction_reason,
        restriction_categories=categories,
        effective_date=datetime.utcnow(),
        expiration_date=expiration_date,
        is_active=True,
        enforced_at_login=True,
        enforced_at_api=True,
        created_by=current_user.email
    )
    
    db.add(blackout)
    db.commit()
    
    logger.info(
        "blackout_list_entry_added",
        email=associate_email,
        restriction_type=restriction_type,
        created_by=current_user.email,
        categories=categories
    )
    
    return {"status": "added", "email": associate_email}

@router.delete("/associate/{associate_email}")
async def remove_from_blackout_list(
    associate_email: str,
    reason_for_removal: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Remove associate from blackout list
    """
    blackout = db.query(BlackoutList).filter(
        BlackoutList.associate_email == associate_email.lower()
    ).first()
    
    if not blackout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associate not found on blackout list"
        )
    
    blackout.is_active = False
    blackout.modified_by = current_user.email
    blackout.modified_at = datetime.utcnow()
    blackout.reason_for_change = reason_for_removal
    
    db.commit()
    
    logger.info(
        "blackout_list_entry_removed",
        email=associate_email,
        reason=reason_for_removal,
        modified_by=current_user.email
    )
    
    return {"status": "removed", "email": associate_email}

@router.get("/active-restrictions")
async def get_active_restrictions(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Get list of all active blackout restrictions
    """
    active_blackouts = db.query(BlackoutList).filter(
        BlackoutList.is_active == True,
        BlackoutList.effective_date <= datetime.utcnow(),
        (BlackoutList.expiration_date > datetime.utcnow()) | 
        (BlackoutList.expiration_date == None)
    ).all()
    
    return {
        "total": len(active_blackouts),
        "restrictions": [
            {
                "email": b.associate_email,
                "restriction_type": b.restriction_type,
                "categories": b.restriction_categories,
                "effective_date": b.effective_date,
                "expiration_date": b.expiration_date,
                "created_by": b.created_by
            }
            for b in active_blackouts
        ]
    }
```

---

## 7. AUDIT & COMPLIANCE REPORTING

### 7.1 Blackout Access Denial Report

```python
# app/services/compliance_reporting.py
class ComplianceReportingService:
    
    def generate_blackout_denial_report(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """
        Generate report of blackout list denials for compliance review
        """
        denied_logins = db.query(BlackoutAuditLog).filter(
            BlackoutAuditLog.event_type == "login_denied",
            BlackoutAuditLog.event_timestamp >= start_date,
            BlackoutAuditLog.event_timestamp <= end_date
        ).all()
        
        denied_api_access = db.query(BlackoutAuditLog).filter(
            BlackoutAuditLog.event_type == "api_call_denied",
            BlackoutAuditLog.event_timestamp >= start_date,
            BlackoutAuditLog.event_timestamp <= end_date
        ).all()
        
        return {
            "report_period": f"{start_date} to {end_date}",
            "denied_login_attempts": {
                "total": len(denied_logins),
                "by_reason": self._group_by_reason(denied_logins),
                "details": [
                    {
                        "email": log.associate_email,
                        "time": log.event_timestamp,
                        "reason": log.blackout_reason,
                        "ip_address": log.ip_address
                    }
                    for log in denied_logins
                ]
            },
            "denied_api_access": {
                "total": len(denied_api_access),
                "by_category": self._group_by_category(denied_api_access),
                "details": [
                    {
                        "email": log.associate_email,
                        "endpoint": log.endpoint,
                        "time": log.event_timestamp,
                        "category": log.restricted_categories
                    }
                    for log in denied_api_access
                ]
            },
            "compliance_status": "✅ ENFORCED" if (denied_logins or denied_api_access) else "⚠️ NO DENIALS RECORDED"
        }
    
    def _group_by_reason(self, logs: List) -> dict:
        """Group denial reasons"""
        grouped = {}
        for log in logs:
            reason = log.blackout_reason
            grouped[reason] = grouped.get(reason, 0) + 1
        return grouped
    
    def _group_by_category(self, logs: List) -> dict:
        """Group by restricted category"""
        grouped = {}
        for log in logs:
            for category in log.restricted_categories:
                grouped[category] = grouped.get(category, 0) + 1
        return grouped
```

---

## 8. IMPLEMENTATION ROADMAP

### Phase 1: Database & Core Logic (Week 1-2)
- [ ] Create blackout_list tables
- [ ] Implement BlackoutListService
- [ ] Add pre-login check to /auth/login endpoint
- [ ] Add middleware for API-level enforcement

### Phase 2: Data Layer Awareness (Week 3)
- [ ] Mark SOX-restricted KPIs
- [ ] Update KPIService to filter by user restrictions
- [ ] Add restricted_categories to all protected tables

### Phase 3: Frontend Updates (Week 4)
- [ ] Update React components to check restricted categories
- [ ] Add restricted data warnings
- [ ] Conditional rendering based on access level

### Phase 4: Admin Interface & Reporting (Week 5)
- [ ] Build admin blackout management panel
- [ ] Implement compliance reporting
- [ ] Create audit log dashboard

### Phase 5: Testing & Validation (Week 6)
- [ ] SOX auditor approval
- [ ] Security review
- [ ] Compliance validation

---

## 9. COMPLIANCE BENEFITS

| Benefit | How Blackout List Delivers |
|---------|----------------------------|
| **Segregation of Duties** | ✅ Prevents users with conflicts from accessing financial data |
| **Access Control Enforcement** | ✅ Pre-login check prevents bypass |
| **Audit Trail** | ✅ Complete log of all denial attempts |
| **Regulatory Compliance** | ✅ Demonstrates SOX control implementation |
| **Risk Mitigation** | ✅ Prevents accidental data exposure to restricted users |
| **Compliance Reporting** | ✅ Ready-to-audit reports for auditors |

---

**Next Steps:**
1. Architect review of blackout implementation
2. Database schema deployment
3. Integration into authentication flow
4. Compliance team validation

