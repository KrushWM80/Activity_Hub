"""
Activity Hub Logic Rules Engine - Scheduler Service
Port: 5011
Purpose: Monitor for trigger events and execute Logic Rules (notifications, tasks, next steps)

This is the central orchestration service that:
1. Periodically checks for trigger conditions (new projects, status changes, etc.)
2. Evaluates matched Logic Rules from BigQuery
3. Executes all components of matched rules (notification + task + next-step)
4. Logs execution results for audit trail
"""

import os
import json
import logging
from datetime import datetime, timedelta
import uuid
from typing import List, Dict, Optional
import asyncio
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from google.cloud import bigquery
from google.oauth2 import service_account

# ============================================================
# CONFIGURATION
# ============================================================

HOST = "0.0.0.0"
PORT = 5011
DEBUG = True
SCHEDULER_INSTANCE_ID = str(uuid.uuid4())[:8]  # Unique ID for this instance
TRIGGER_CHECK_INTERVAL = 300  # Check for triggers every 5 minutes (in seconds)

# Cache Configuration
METRICS_CACHE = {
    "data": None,
    "timestamp": None,
    "ttl": 60  # Cache for 60 seconds
}

NOTIFICATIONS_CACHE = {
    "data": None,
    "timestamp": None,
    "ttl": 30  # Cache notifications for 30 seconds
}

# BigQuery Configuration
PROJECT_ID = "wmt-assetprotection-prod"
DATASET_ID = "Store_Support_Dev"
BQ_TABLES = {
    "logic_requests": "logic_requests",
    "notification_rules": "notification_logic_rules",
    "scheduler_log": "scheduler_execution_log",
    "deliveries": "notification_deliveries",
    "projects": "projects",  # Point to actual projects table when ready
}

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# BIGQUERY CLIENT SETUP
# ============================================================

def get_bigquery_client():
    """
    Initialize BigQuery client using GOOGLE_APPLICATION_CREDENTIALS
    Falls back to application default credentials (gcloud auth)
    """
    try:
        # Try using GOOGLE_APPLICATION_CREDENTIALS environment variable
        credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path and os.path.exists(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            client = bigquery.Client(project=PROJECT_ID, credentials=credentials)
            logger.info(f"BigQuery client initialized with service account: {credentials_path}")
        else:
            # Use application default credentials (gcloud auth)
            client = bigquery.Client(project=PROJECT_ID)
            logger.info("BigQuery client initialized with application default credentials")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize BigQuery client: {e}")
        raise

bq_client: Optional[bigquery.Client] = None

# ============================================================
# SCHEDULER MODULES
# ============================================================

class TriggerDetector:
    """Detects trigger events (new projects, status changes, etc.)"""
    
    def __init__(self, bq_client: bigquery.Client):
        self.bq_client = bq_client
        self.last_check_time = datetime.utcnow() - timedelta(minutes=5)
    
    async def detect_new_projects(self) -> List[Dict]:
        """
        Detect new projects created since last check
        Returns list of project records that match trigger conditions
        """
        try:
            query = f"""
            SELECT 
                project_id,
                project_name,
                owner_email,
                status,
                created_at,
                updated_at
            FROM `{PROJECT_ID}.{DATASET_ID}.projects`
            WHERE created_at > @last_check_time
            ORDER BY created_at DESC
            LIMIT 100
            """
            
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("last_check_time", "TIMESTAMP", self.last_check_time),
                ]
            )
            
            results = self.bq_client.query(query, job_config=job_config).result()
            projects = [dict(row) for row in results]
            
            logger.info(f"Detected {len(projects)} new projects since {self.last_check_time}")
            self.last_check_time = datetime.utcnow()
            
            return projects
        except Exception as e:
            logger.error(f"Error detecting new projects: {e}")
            return []

class RuleEvaluator:
    """Evaluates which Logic Rules match detected triggers"""
    
    def __init__(self, bq_client: bigquery.Client):
        self.bq_client = bq_client
    
    async def find_matching_rules(self, trigger_type: str, trigger_source_record_id: str) -> List[Dict]:
        """
        Find all active Logic Rules that match a trigger type
        """
        try:
            query = f"""
            SELECT 
                lr.request_id,
                lr.name,
                lr.trigger_type,
                nr.rule_id,
                nr.category,
                nr.trigger_event,
                nr.title_template,
                nr.message_template,
                nr.recipient_rule,
                nr.channels,
                nr.schedule,
                nr.is_active
            FROM `{PROJECT_ID}.{DATASET_ID}.notification_logic_rules` nr
            INNER JOIN `{PROJECT_ID}.{DATASET_ID}.logic_requests` lr
                ON nr.logic_request_id = lr.request_id
            WHERE lr.status = 'approved'
              AND lr.is_active = TRUE
              AND nr.is_active = TRUE
              AND lr.trigger_type = @trigger_type
            """
            
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("trigger_type", "STRING", trigger_type),
                ]
            )
            
            results = self.bq_client.query(query, job_config=job_config).result()
            rules = [dict(row) for row in results]
            
            logger.info(f"Found {len(rules)} matching rules for trigger_type: {trigger_type}")
            return rules
        except Exception as e:
            logger.error(f"Error finding matching rules: {e}")
            return []

class RuleExecutor:
    """Executes Logic Rules (notifications, tasks, next steps)"""
    
    def __init__(self, bq_client: bigquery.Client):
        self.bq_client = bq_client
    
    async def execute_notification_rule(
        self, 
        rule: Dict, 
        trigger_data: Dict,
        trigger_timestamp: datetime
    ) -> Dict:
        """
        Execute a notification rule
        Renders templates, looks up recipients, logs execution
        """
        execution_id = str(uuid.uuid4())
        
        try:
            # Step 1: Render templates with trigger data
            title = self._render_template(rule['title_template'], trigger_data)
            message = self._render_template(rule['message_template'], trigger_data)
            
            # Step 2: Determine recipients based on recipient_rule
            recipient_emails = await self._resolve_recipients(rule['recipient_rule'], trigger_data)
            
            if not recipient_emails:
                logger.warning(f"No recipients resolved for rule {rule['rule_id']}")
                return {
                    "execution_id": execution_id,
                    "status": "failed",
                    "error": "No recipients resolved"
                }
            
            # Step 3: Log execution start
            execution_log = {
                "execution_id": execution_id,
                "trigger_timestamp": trigger_timestamp,
                "trigger_type": rule.get('trigger_event', 'new_project'),
                "trigger_source_table": "projects",
                "trigger_source_record_id": trigger_data.get('project_id', 'unknown'),
                "logic_request_id": rule['request_id'],
                "notification_rule_id": rule['rule_id'],
                "status": "in_progress",
                "executed_at": datetime.utcnow(),
                "recipient_emails": recipient_emails,
                "channels_attempted": rule['channels'],
                "scheduler_instance_id": SCHEDULER_INSTANCE_ID,
                "attempt_number": 1
            }
            
            # Step 4: Deliver notifications via channels
            delivery_status = {}
            for channel in rule['channels']:
                try:
                    if channel == "email":
                        success = await self._deliver_email(
                            title, message, recipient_emails, trigger_data
                        )
                        delivery_status[channel] = "sent" if success else "failed"
                    elif channel == "in_app":
                        success = await self._deliver_in_app(
                            title, message, recipient_emails, trigger_data, rule
                        )
                        delivery_status[channel] = "created" if success else "failed"
                    elif channel == "teams":
                        # Phase 2: Teams integration
                        delivery_status[channel] = "not_implemented"
                    elif channel == "slack":
                        # Phase 2: Slack integration
                        delivery_status[channel] = "not_implemented"
                except Exception as e:
                    logger.error(f"Error delivering via {channel}: {e}")
                    delivery_status[channel] = "failed"
            
            # Step 5: Update execution log
            execution_log['delivery_status'] = delivery_status
            execution_log['completed_at'] = datetime.utcnow()
            execution_log['status'] = "success" if any(
                v == "sent" or v == "created" for v in delivery_status.values()
            ) else "partial_success"
            
            await self._log_execution(execution_log)
            
            logger.info(f"Successfully executed rule {rule['rule_id']}: {execution_log['status']}")
            return execution_log
            
        except Exception as e:
            logger.error(f"Error executing notification rule {rule['rule_id']}: {e}")
            execution_log = {
                "execution_id": execution_id,
                "status": "failed",
                "error_message": str(e),
                "logic_request_id": rule.get('request_id'),
                "notification_rule_id": rule.get('rule_id')
            }
            await self._log_execution(execution_log)
            return execution_log
    
    def _render_template(self, template: str, context: Dict) -> str:
        """Simple string template rendering: {key} replaced with context[key]"""
        try:
            return template.format(**context)
        except KeyError as e:
            logger.warning(f"Missing template variable: {e}, using original template")
            return template
    
    async def _resolve_recipients(self, recipient_rule: str, trigger_data: Dict) -> List[str]:
        """
        Resolve recipient emails based on recipient_rule
        Rule format: {"type": "owner"} or {"type": "users", "emails": [...]}
        """
        try:
            rule = json.loads(recipient_rule) if isinstance(recipient_rule, str) else recipient_rule
            
            if rule.get('type') == 'owner':
                # Get owner from trigger data (project owner)
                return [trigger_data.get('owner_email')] if trigger_data.get('owner_email') else []
            elif rule.get('type') == 'users':
                return rule.get('emails', [])
            elif rule.get('type') == 'manager':
                # Phase 2: Look up manager from organizational data
                return []
            else:
                logger.warning(f"Unknown recipient rule type: {rule.get('type')}")
                return []
        except Exception as e:
            logger.error(f"Error resolving recipients: {e}")
            return []
    
    async def _deliver_email(self, title: str, message: str, recipients: List[str], trigger_data: Dict) -> bool:
        """
        Deliver notification via email
        Phase 1: Placeholder, will integrate with Walmart SMTP
        """
        logger.info(f"[EMAIL] Sending '{title}' to {recipients}")
        # TODO: Integrate with Walmart SMTP
        # For now, just log the intent
        return True
    
    async def _deliver_in_app(self, title: str, message: str, recipients: List[str], trigger_data: Dict, rule: Dict) -> bool:
        """
        Deliver notification via in-app notification bell/inbox
        Creates entries in notification_deliveries table
        """
        try:
            delivery_records = []
            action_link = trigger_data.get('sif_form_link', '')  # Placeholder for SIF link
            
            for recipient in recipients:
                delivery_record = {
                    "delivery_id": str(uuid.uuid4()),
                    "recipient_email": recipient,
                    "title": title,
                    "message": message,
                    "action_link": action_link,
                    "channel": "in_app",
                    "sent_at": datetime.utcnow(),
                    "is_read": False,
                    "is_archived": False
                }
                delivery_records.append(delivery_record)
            
            # Insert into BQ
            table_id = f"{PROJECT_ID}.{DATASET_ID}.notification_deliveries"
            errors = self.bq_client.insert_rows_json(table_id, delivery_records)
            
            if errors:
                logger.error(f"BigQuery insert errors: {errors}")
                return False
            
            logger.info(f"[IN-APP] Created {len(delivery_records)} in-app notifications")
            return True
        except Exception as e:
            logger.error(f"Error delivering in-app notifications: {e}")
            return False
    
    async def _log_execution(self, execution_log: Dict) -> bool:
        """Log execution to scheduler_execution_log table"""
        try:
            table_id = f"{PROJECT_ID}.{DATASET_ID}.scheduler_execution_log"
            
            # Convert datetime objects to ISO format strings for JSON
            log_copy = execution_log.copy()
            for key in ['trigger_timestamp', 'executed_at', 'completed_at']:
                if key in log_copy and isinstance(log_copy[key], datetime):
                    log_copy[key] = log_copy[key].isoformat()
            
            errors = self.bq_client.insert_rows_json(table_id, [log_copy])
            
            if errors:
                logger.error(f"Failed to log execution: {errors}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error logging execution: {e}")
            return False

# ============================================================
# FASTAPI APPLICATION
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan: initialize on startup, cleanup on shutdown"""
    global bq_client
    
    # Startup
    logger.info(f"Starting Scheduler Service (instance: {SCHEDULER_INSTANCE_ID})")
    bq_client = get_bigquery_client()
    
    # TODO: Call service registration endpoint
    # await register_with_activity_hub()
    
    # Start background scheduler task
    scheduler_task = asyncio.create_task(run_scheduler_loop())
    
    yield
    
    # Shutdown
    logger.info("Shutting down Scheduler Service")
    scheduler_task.cancel()
    try:
        await scheduler_task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="Activity Hub Logic Rules Engine - Scheduler",
    description="Central scheduler that monitors triggers and executes Logic Rules",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for admin dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# SCHEDULER LOOP (Background Task)
# ============================================================

async def run_scheduler_loop():
    """
    Main scheduler loop that runs every TRIGGER_CHECK_INTERVAL seconds
    Detects triggers, finds matching rules, executes them
    """
    trigger_detector = TriggerDetector(bq_client)
    rule_evaluator = RuleEvaluator(bq_client)
    rule_executor = RuleExecutor(bq_client)
    
    logger.info(f"Scheduler loop started (interval: {TRIGGER_CHECK_INTERVAL}s)")
    
    while True:
        try:
            logger.debug("Checking for triggers...")
            
            # Step 1: Detect new projects
            new_projects = await trigger_detector.detect_new_projects()
            
            if new_projects:
                logger.info(f"Processing {len(new_projects)} triggered events")
                
                for project in new_projects:
                    try:
                        # Step 2: Find matching rules
                        matching_rules = await rule_evaluator.find_matching_rules(
                            trigger_type="new_project",
                            trigger_source_record_id=project.get('project_id', 'unknown')
                        )
                        
                        # Step 3: Execute each matching rule
                        for rule in matching_rules:
                            await rule_executor.execute_notification_rule(
                                rule=rule,
                                trigger_data=project,
                                trigger_timestamp=project.get('created_at', datetime.utcnow())
                            )
                    except Exception as e:
                        logger.error(f"Error processing project {project.get('project_id')}: {e}")
            
            # Wait for next check interval
            await asyncio.sleep(TRIGGER_CHECK_INTERVAL)
            
        except asyncio.CancelledError:
            logger.info("Scheduler loop cancelled")
            break
        except Exception as e:
            logger.error(f"Error in scheduler loop: {e}")
            await asyncio.sleep(TRIGGER_CHECK_INTERVAL)

# ============================================================
# REST API ENDPOINTS
# ============================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "Logic Rules Engine - Scheduler",
        "version": "1.0.0",
        "instance_id": SCHEDULER_INSTANCE_ID,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/scheduler/status", tags=["Admin"])
async def get_scheduler_status():
    """Get current scheduler status and metrics"""
    try:
        # Query recent execution logs
        query = f"""
        SELECT 
            COUNT(*) as total_executions,
            COUNTIF(status = 'success') as successful,
            COUNTIF(status = 'failed') as failed,
            MAX(executed_at) as last_execution
        FROM `{PROJECT_ID}.{DATASET_ID}.scheduler_execution_log`
        WHERE executed_at > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
        """
        
        results = bq_client.query(query).result()
        row = next(results)
        
        return {
            "status": "running",
            "instance_id": SCHEDULER_INSTANCE_ID,
            "check_interval_seconds": TRIGGER_CHECK_INTERVAL,
            "last_24_hours": {
                "total_executions": int(row.total_executions),
                "successful": int(row.successful),
                "failed": int(row.failed),
                "last_execution": row.last_execution.isoformat() if row.last_execution else None
            }
        }
    except Exception as e:
        logger.error(f"Error getting scheduler status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/logic-requests", tags=["Logic Rules"])
async def list_logic_requests(status: str = "approved", limit: int = 50):
    """List active Logic Requests"""
    try:
        query = f"""
        SELECT 
            request_id,
            name,
            description,
            trigger_type,
            status,
            is_active,
            created_at,
            approved_at
        FROM `{PROJECT_ID}.{DATASET_ID}.logic_requests`
        WHERE status = @status
        ORDER BY created_at DESC
        LIMIT @limit
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("status", "STRING", status),
                bigquery.ScalarQueryParameter("limit", "INT64", limit),
            ]
        )
        
        results = bq_client.query(query, job_config=job_config).result()
        requests = [dict(row) for row in results]
        
        return {"count": len(requests), "requests": requests}
    except Exception as e:
        logger.error(f"Error listing logic requests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/logic-requests", tags=["Logic Rules"])
async def create_logic_request(request_data: dict):
    """Create a new Logic Request (composite: notification + task + next-step)"""
    try:
        # Generate request ID and timestamps
        request_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat() + "Z"  # Convert to ISO string for JSON serialization
        
        # Insert into logic_requests table
        logic_request_row = {
            "request_id": request_id,
            "name": request_data.get("name"),
            "description": request_data.get("description"),
            "created_by_admin": request_data.get("created_by", "system"),
            "created_at": created_at,
            "updated_at": created_at,
            "trigger_type": request_data.get("trigger_type"),
            "custom_trigger_text": request_data.get("custom_trigger_text"),
            "trigger_condition": request_data.get("trigger_condition"),
            "trigger_table": request_data.get("trigger_table"),
            "has_notification_component": request_data.get("has_notification_component", False),
            "has_task_component": request_data.get("has_task_component", False),
            "has_nextstep_component": request_data.get("has_nextstep_component", False),
            "status": "pending_approval",
            "approval_status": "pending",
            "is_active": False,
            "execution_count": 0
        }
        
        # Insert parent Logic Request into BigQuery
        table = bq_client.get_table(f"{PROJECT_ID}.{DATASET_ID}.logic_requests")
        errors = bq_client.insert_rows_json(table, [logic_request_row])
        
        if errors:
            logger.error(f"BigQuery insert errors for logic_requests: {errors}")
            raise HTTPException(status_code=500, detail=f"Failed to insert Logic Request: {errors}")
        
        # If notification component, insert notification rule
        if request_data.get("has_notification_component") and request_data.get("notification_rule"):
            rule_id = str(uuid.uuid4())
            notification_rule = request_data.get("notification_rule")
            
            # Map form field names to BigQuery column names
            notification_row = {
                "rule_id": rule_id,
                "logic_request_id": request_id,
                "created_at": created_at,
                "updated_at": created_at,
                "category": notification_rule.get("category", "PROJECT_LIFECYCLE"),
                "trigger_event": notification_rule.get("trigger_event", request_data.get("trigger_type", "custom")),
                "title_template": notification_rule.get("title_template") or notification_rule.get("title", ""),
                "message_template": notification_rule.get("message_template") or notification_rule.get("message", ""),
                "recipient_rule": notification_rule.get("recipient_rule") or notification_rule.get("recipients", "owner"),
                "channels": notification_rule.get("channels", ["in_app"]),
                "schedule": notification_rule.get("schedule", "immediate"),
                "is_active": True,
                "status": "active",
                "execution_count": 0
            }
            
            notification_table = bq_client.get_table(f"{PROJECT_ID}.{DATASET_ID}.notification_logic_rules")
            notification_errors = bq_client.insert_rows_json(notification_table, [notification_row])
            
            if notification_errors:
                logger.error(f"BigQuery insert errors for notification_logic_rules: {notification_errors}")
                raise HTTPException(status_code=500, detail=f"Failed to insert notification rule: {notification_errors}")
        
        logger.info(f"Created Logic Request {request_id} with trigger type: {request_data.get('trigger_type')}")
        
        response_data = {
            "status": "success",
            "request_id": request_id,
            "name": request_data.get("name"),
            "trigger_type": request_data.get("trigger_type"),
            "approval_status": "pending",
            "created_at": created_at,
            "message": f"Logic Request created and pending approval. Request ID: {request_id}"
        }
        
        # Include custom trigger info if provided
        if request_data.get("trigger_type") == "custom" and request_data.get("custom_trigger_text"):
            response_data["custom_trigger_text"] = request_data.get("custom_trigger_text")
            response_data["note"] = "Custom triggers require backend implementation. Approval confirms requirement; backend developer will implement detection SQL."
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating Logic Request: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating Logic Request: {str(e)}")

@app.get("/api/v1/execution-log", tags=["Audit"])
async def get_execution_log(limit: int = 100):
    """Get recent execution log entries"""
    try:
        query = f"""
        SELECT 
            execution_id,
            trigger_timestamp,
            trigger_type,
            trigger_source_record_id,
            status,
            executed_at,
            delivery_status,
            error_message
        FROM `{PROJECT_ID}.{DATASET_ID}.scheduler_execution_log`
        ORDER BY executed_at DESC
        LIMIT @limit
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("limit", "INT64", limit),
            ]
        )
        
        results = bq_client.query(query, job_config=job_config).result()
        logs = [dict(row) for row in results]
        
        return {"count": len(logs), "logs": logs}
    except Exception as e:
        logger.error(f"Error getting execution log: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/logic-metrics", tags=["Dashboard"])
async def get_logic_metrics():
    """Get dashboard metrics for Logic Rules Engine (with caching)"""
    try:
        # Check cache first
        current_time = time.time()
        if METRICS_CACHE["data"] is not None and METRICS_CACHE["timestamp"] is not None:
            cache_age = current_time - METRICS_CACHE["timestamp"]
            if cache_age < METRICS_CACHE["ttl"]:
                logger.info(f"Returning cached metrics (age: {cache_age:.1f}s)")
                return METRICS_CACHE["data"]
        
        # Cache miss or expired - query BigQuery
        logger.info("Cache miss - querying BigQuery for metrics")
        
        # Metric 1: Active Rules (notification_logic_rules with is_active=true)
        active_rules_query = f"""
        SELECT COUNT(*) as count
        FROM `{PROJECT_ID}.{DATASET_ID}.notification_logic_rules`
        WHERE is_active = TRUE
        """
        
        # Metric 2: Notifications Today
        notifications_today_query = f"""
        SELECT COUNT(*) as count
        FROM `{PROJECT_ID}.{DATASET_ID}.notification_deliveries`
        WHERE DATE(sent_at) = CURRENT_DATE('UTC')
        """
        
        # Metric 3: Pending Approvals
        pending_approvals_query = f"""
        SELECT COUNT(*) as count
        FROM `{PROJECT_ID}.{DATASET_ID}.logic_requests`
        WHERE status = 'pending_approval'
        """
        
        # Metric 4: Total Logic Requests (all time)
        total_requests_query = f"""
        SELECT COUNT(*) as count
        FROM `{PROJECT_ID}.{DATASET_ID}.logic_requests`
        """
        
        # Execute all queries
        active_rules_result = list(bq_client.query(active_rules_query).result())
        notifications_today_result = list(bq_client.query(notifications_today_query).result())
        pending_approvals_result = list(bq_client.query(pending_approvals_query).result())
        total_requests_result = list(bq_client.query(total_requests_query).result())
        
        # Build response
        response_data = {
            "activeRules": active_rules_result[0].count if active_rules_result else 0,
            "notificationsToday": notifications_today_result[0].count if notifications_today_result else 0,
            "pendingApprovals": pending_approvals_result[0].count if pending_approvals_result else 0,
            "totalLogicRequests": total_requests_result[0].count if total_requests_result else 0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "cached": False
        }
        
        # Update cache
        METRICS_CACHE["data"] = response_data
        METRICS_CACHE["timestamp"] = current_time
        logger.info("Metrics cached for 60 seconds")
        
        return response_data
    except Exception as e:
        logger.error(f"Error getting logic metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/notifications/today", tags=["Notifications"])
async def get_notifications_today():
    """Get notifications sent today (with caching) - for display on For You, My Work, etc"""
    try:
        # Check cache first
        current_time = time.time()
        if NOTIFICATIONS_CACHE["data"] is not None and NOTIFICATIONS_CACHE["timestamp"] is not None:
            cache_age = current_time - NOTIFICATIONS_CACHE["timestamp"]
            if cache_age < NOTIFICATIONS_CACHE["ttl"]:
                logger.info(f"Returning cached notifications (age: {cache_age:.1f}s)")
                return NOTIFICATIONS_CACHE["data"]
        
        # Cache miss or expired - query BigQuery
        logger.info("Cache miss - querying BigQuery for notifications")
        
        query = f"""
        SELECT 
            notification_id,
            user_id,
            title,
            message,
            category,
            channels,
            sent_at,
            read_at,
            status
        FROM `{PROJECT_ID}.{DATASET_ID}.notification_deliveries`
        WHERE DATE(sent_at) = CURRENT_DATE('UTC')
        ORDER BY sent_at DESC
        LIMIT 50
        """
        
        results = bq_client.query(query).result()
        notifications = [dict(row) for row in results]
        
        response_data = {
            "count": len(notifications),
            "notifications": notifications,
            "cached": False
        }
        
        # Update cache
        NOTIFICATIONS_CACHE["data"] = response_data
        NOTIFICATIONS_CACHE["timestamp"] = current_time
        logger.info(f"Notifications cached for 30 seconds ({len(notifications)} items)")
        
        return response_data
    except Exception as e:
        logger.error(f"Error getting notifications: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    logger.info(f"Starting Activity Hub Logic Rules Engine - Scheduler Service")
    logger.info(f"Service Instance ID: {SCHEDULER_INSTANCE_ID}")
    logger.info(f"Port: {PORT}")
    logger.info(f"BigQuery Project: {PROJECT_ID}, Dataset: {DATASET_ID}")
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info" if not DEBUG else "debug"
    )
