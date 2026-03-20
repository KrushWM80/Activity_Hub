# Workflow Patterns & Multi-Step Approval Systems

## Overview

The Job Code Teaming Dashboard implements a **multi-step workflow** for managing requests:
- User Registration → Admin Approval
- Job Code Request → Admin Review → Export

This guide covers the patterns for building similar approval-based workflows.

---

## 🔄 Workflow Types

### Type 1: Registration Approval Workflow

```
User Registration Form
        ↓
Application Pending
        ↓
Admin Reviews in Dashboard
        ↓
┌─────────────┬──────────────┐
│             │              │
APPROVED      REJECTED    EMAIL SENT
│             │              │
✓ Account     ✗ Denied   User Notified
  Activated
```

**Key Points:**
- Users can't access system until approved
- Admin explicitly approves/rejects
- Email notifications keep user informed

---

### Type 2: Request Approval Workflow

```
User Submits Request
(Job Code + Team Assignment)
        ↓
Request Stored in Database
(status = "pending")
        ↓
Admin Dashboard Shows Pending Requests
        ↓
Admin Reviews Details
        ↓
┌─────────────┬──────────────┐
│             │              │
APPROVE       REJECT
│             │
Changes       Remains
Approved      Pending
```

**Key Points:**
- Request stored immediately (no loss of data)
- Admin can review before approving
- Can reject and let user resubmit

---

### Type 3: Export/Publication Workflow

```
Admin Reviews Approved Requests
        ↓
Admin Clicks "Export"
        ↓
System Generates Export File
(CSV, JSON, formatted for TMS)
        ↓
Admin Downloads File
        ↓
Admin Uploads to External System
(TMS, SharePoint, etc.)
        ↓
Changes Applied to External System
```

**Key Points:**
- Batch processing of multiple requests
- Standardized export format
- Human review before external changes

---

## 🛠️ Implementation Patterns

### Pattern 1: Status-Based State Machine

```python
class RequestStatus:
    """Allowed status transitions"""
    
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPORTED = "exported"
    
    @staticmethod
    def get_transitions(current_status):
        """What statuses can this transition to?"""
        
        transitions = {
            "pending": ["approved", "rejected"],
            "approved": ["exported", "rejected"],
            "rejected": ["pending"],  # Can resubmit
            "exported": []  # Terminal state
        }
        
        return transitions.get(current_status, [])
    
    @staticmethod
    def can_transition(from_status, to_status):
        """Check if transition is allowed"""
        allowed = RequestStatus.get_transitions(from_status)
        return to_status in allowed

def update_request_status(request_id, new_status, changed_by):
    """Update request status with validation"""
    
    requests = load_json("data/update_requests.json")
    request = requests[request_id]
    current_status = request["status"]
    
    # Validate transition
    if not RequestStatus.can_transition(current_status, new_status):
        raise ValueError(
            f"Cannot transition from {current_status} to {new_status}"
        )
    
    # Update request
    request["status"] = new_status
    request[f"{new_status}_by"] = changed_by
    request[f"{new_status}_at"] = datetime.now().isoformat()
    
    save_json("data/update_requests.json", requests)
    
    return request
```

**State Diagram:**

```
┌──────────────┐
│   Pending    │◄──────────┐
└──────┬───────┘           │
       │                   │
       │ Reject      Resubmit
       ▼                   │
┌──────────────┐           │
│  Rejected    ├───────────┘
└──────────────┘

       ┌──────────────┐
       │   Pending    │
       └──────┬───────┘
              │
              │ Approve
              ▼
       ┌──────────────┐
       │  Approved    │
       └──────┬───────┘
              │
              │ Export
              ▼
       ┌──────────────┐
       │  Exported    │
       └──────────────┘
```

### Pattern 2: Approval Queue System

```python
class ApprovalQueue:
    """Manage pending items for admin review"""
    
    def __init__(self, data_file):
        self.data_file = data_file
    
    def add_item(self, item_id, item_data):
        """Add item to queue"""
        data = load_json(self.data_file)
        data[item_id] = {
            **item_data,
            "status": "pending",
            "queued_at": datetime.now().isoformat()
        }
        save_json(self.data_file, data)
        return item_id
    
    def get_pending(self):
        """Get all pending items, oldest first"""
        data = load_json(self.data_file)
        pending = [
            item for item in data.values()
            if item["status"] == "pending"
        ]
        return sorted(pending, key=lambda x: x["queued_at"])
    
    def get_pending_count(self):
        """Count pending items"""
        return len(self.get_pending())
    
    def approve(self, item_id, approved_by, notes=""):
        """Approve an item"""
        data = load_json(self.data_file)
        
        if item_id not in data:
            raise ValueError(f"Item {item_id} not found")
        
        data[item_id]["status"] = "approved"
        data[item_id]["approved_by"] = approved_by
        data[item_id]["approved_at"] = datetime.now().isoformat()
        data[item_id]["approval_notes"] = notes
        
        save_json(self.data_file, data)
        return data[item_id]
    
    def reject(self, item_id, rejected_by, reason=""):
        """Reject an item"""
        data = load_json(self.data_file)
        
        if item_id not in data:
            raise ValueError(f"Item {item_id} not found")
        
        data[item_id]["status"] = "rejected"
        data[item_id]["rejected_by"] = rejected_by
        data[item_id]["rejected_at"] = datetime.now().isoformat()
        data[item_id]["rejection_reason"] = reason
        
        save_json(self.data_file, data)
        return data[item_id]
    
    def get_approval_metrics(self):
        """Get stats on approval queue"""
        data = load_json(self.data_file)
        
        total = len(data)
        pending = sum(1 for item in data.values() if item["status"] == "pending")
        approved = sum(1 for item in data.values() if item["status"] == "approved")
        rejected = sum(1 for item in data.values() if item["status"] == "rejected")
        
        return {
            "total": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": round((approved / total * 100) if total > 0 else 0, 1)
        }

# Usage
queue = ApprovalQueue("data/update_requests.json")

# API endpoint to get pending requests
@app.get("/api/pending-requests")
async def get_pending(session: dict):
    if session["role"] != "admin":
        raise HTTPException(status_code=403)
    
    pending = queue.get_pending()
    count = queue.get_pending_count()
    
    return {
        "total_pending": count,
        "requests": pending
    }

# API endpoint to approve
@app.post("/api/requests/{request_id}/approve")
async def approve(request_id: str, notes: str = "", session: dict = None):
    if session["role"] != "admin":
        raise HTTPException(status_code=403)
    
    request = queue.approve(request_id, session["username"], notes)
    
    return {
        "success": True,
        "request": request,
        "pending_count": queue.get_pending_count()
    }

# API endpoint to get metrics
@app.get("/api/approval-metrics")
async def get_metrics(session: dict):
    if session["role"] != "admin":
        raise HTTPException(status_code=403)
    
    metrics = queue.get_approval_metrics()
    return metrics
```

### Pattern 3: Role-Based Actions

```python
class WorkflowRoles:
    """Define what each role can do"""
    
    PERMISSIONS = {
        "admin": {
            "can_view_all": True,
            "can_approve": True,
            "can_reject": True,
            "can_export": True,
            "can_manage_users": True
        },
        "user": {
            "can_view_own": True,
            "can_submit_request": True,
            "can_view_all": False,
            "can_approve": False,
            "can_reject": False,
            "can_export": False
        },
        "manager": {
            "can_view_team": True,
            "can_approve": True,  # Limited
            "can_reject": True,   # Limited
            "can_export": False
        }
    }
    
    @staticmethod
    def has_permission(role, permission):
        """Check if role has permission"""
        return WorkflowRoles.PERMISSIONS.get(role, {}).get(permission, False)

def require_permission(permission):
    """Decorator to require specific permission"""
    def decorator(func):
        async def wrapper(session: dict, *args, **kwargs):
            role = session["role"]
            
            if not WorkflowRoles.has_permission(role, permission):
                raise HTTPException(
                    status_code=403,
                    detail=f"Permission '{permission}' denied for role '{role}'"
                )
            
            return await func(session, *args, **kwargs)
        return wrapper
    return decorator

# Usage
@app.post("/api/requests/{request_id}/approve")
@require_permission("can_approve")
async def approve_request(request_id: str, session: dict):
    # Only users with "can_approve" permission can reach here
    queue.approve(request_id, session["username"])
    return {"success": True}
```

### Pattern 4: Workflow Dashboard

```python
@app.get("/api/dashboard/summary")
async def get_workflow_summary(session: dict):
    """Dashboard showing all workflow metrics"""
    
    requests = load_json("data/update_requests.json")
    users = load_json("data/users.json")
    
    summary = {
        "workflow_stats": {
            "total_requests": len(requests),
            "pending": sum(1 for r in requests.values() if r["status"] == "pending"),
            "approved": sum(1 for r in requests.values() if r["status"] == "approved"),
            "rejected": sum(1 for r in requests.values() if r["status"] == "rejected")
        },
        "user_stats": {
            "total_users": len(users),
            "admins": sum(1 for u in users.values() if u["role"] == "admin"),
            "regular_users": sum(1 for u in users.values() if u["role"] == "user")
        },
        "approval_queue": {
            "pending_count": sum(1 for r in requests.values() if r["status"] == "pending"),
            "oldest_pending": min(
                (r["submitted_at"] for r in requests.values() if r["status"] == "pending"),
                default=None
            )
        },
        "admin_activity": {
            "approvals_today": sum(
                1 for r in requests.values()
                if r.get("status") == "approved" and
                   r.get("approved_at", "").startswith(datetime.now().strftime("%Y-%m-%d"))
            )
        }
    }
    
    # Only show admin activity to admins
    if session["role"] != "admin":
        del summary["admin_activity"]
    
    return summary
```

---

## 📊 Workflow Visualization

### Request Lifecycle

```
Day 1:
  10:30 AM - User Submits Request
            ✓ Stored in "pending" queue
            ✓ Admin notified (email)
  
  11:00 AM - Admin Reviews Request
            ✓ Checks job code validity
            ✓ Verifies team name
  
  11:15 AM - Admin Clicks "Approve"
            ✓ Status changed to "approved"
            ✓ User notified (email)

Day 2:
  09:00 AM - Admin Exports Approved Requests
            ✓ Generates JSON/CSV
            ✓ File downloaded
  
  09:30 AM - Admin Uploads to TMS
            ✓ External system updated
            ✓ Status changed to "exported"
```

### Parallel Workflows

Multiple requests can be in different stages:

```
Request #1: Job Code 1234
  Status: pending (waiting for admin)

Request #2: Job Code 5678
  Status: approved (ready for export)

Request #3: Job Code 9012
  Status: exported (already sent to TMS)
```

---

## 🔐 Audit Trail

```python
class AuditLog:
    """Track all workflow changes"""
    
    def __init__(self, log_file):
        self.log_file = log_file
    
    def log_action(self, action_type, item_id, changed_by, details):
        """Record an action"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action_type,
            "item_id": item_id,
            "changed_by": changed_by,
            "details": details
        }
        
        logs = load_json(self.log_file)
        
        # Keep as list
        if not isinstance(logs, list):
            logs = []
        
        logs.append(log_entry)
        save_json(self.log_file, logs)
    
    def get_item_history(self, item_id):
        """Get all actions for an item"""
        logs = load_json(self.log_file)
        
        if not isinstance(logs, list):
            return []
        
        return [log for log in logs if log["item_id"] == item_id]
    
    def get_user_actions(self, username):
        """Get all actions by a user"""
        logs = load_json(self.log_file)
        
        if not isinstance(logs, list):
            return []
        
        return [log for log in logs if log["changed_by"] == username]

# Usage
audit = AuditLog("data/audit_log.json")

# Log when request is created
audit.log_action(
    action_type="request_created",
    item_id="req_20250121_103000",
    changed_by="john_smith",
    details={"job_code": "1234", "team": "Team A"}
)

# Log when request is approved
audit.log_action(
    action_type="request_approved",
    item_id="req_20250121_103000",
    changed_by="admin",
    details={"approval_notes": "Verified with team lead"}
)

# API endpoint to view history
@app.get("/api/requests/{request_id}/history")
async def get_request_history(request_id: str):
    return audit.get_item_history(request_id)
```

---

## 🎓 Key Learnings

✅ **Status machines** - Simple state transitions prevent invalid states  
✅ **Queues** - Manage pending items systematically  
✅ **Permissions** - Role-based access control at every step  
✅ **Notifications** - Keep users informed of status changes  
✅ **Audit trails** - Track who did what and when  
✅ **Parallel workflows** - Multiple requests at different stages  
✅ **Export step** - Batch processing before external changes  

---

## 📚 Related Documentation

- See: [USER_AUTHENTICATION.md](./USER_AUTHENTICATION.md) - Role definitions
- See: [EMAIL_NOTIFICATIONS.md](./EMAIL_NOTIFICATIONS.md) - Status change emails
- See: [DATA_PERSISTENCE.md](./DATA_PERSISTENCE.md) - Request data storage
- Source: `C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\dashboard`
