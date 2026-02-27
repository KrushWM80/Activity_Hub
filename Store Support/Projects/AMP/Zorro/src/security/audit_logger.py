"""SIEM audit logging for compliance."""

import json
import logging
import logging.handlers
import os
import socket
from datetime import datetime
from typing import Any, Dict, Optional
from functools import wraps

from ..utils import get_logger

logger = get_logger(__name__)


class AuditLogger:
    """
    Structured audit logging to Walmart SIEM.
    
    Logs security-relevant events in JSON format to syslog for SIEM ingestion.
    
    Example:
        >>> audit = AuditLogger()
        >>> audit.log_event(
        ...     event_type="video.created",
        ...     user_id="jdoe",
        ...     resource_id="vid_123",
        ...     action="create"
        ... )
    """
    
    def __init__(
        self,
        siem_host: Optional[str] = None,
        siem_port: Optional[int] = None,
        enable_siem: bool = None
    ):
        """
        Initialize audit logger.
        
        Args:
            siem_host: SIEM collector hostname
            siem_port: SIEM collector port
            enable_siem: Enable SIEM logging (auto-detect if None)
        """
        self.environment = os.getenv("ZORRO_ENV", "development")
        
        # SIEM configuration
        self.siem_host = siem_host or os.getenv(
            "SIEM_SYSLOG_HOST",
            "walmart-siem-collector.prod.walmart.com"
        )
        self.siem_port = siem_port or int(os.getenv("SIEM_SYSLOG_PORT", "514"))
        
        # Enable SIEM in production by default
        if enable_siem is None:
            self.enable_siem = self.environment == "production"
        else:
            self.enable_siem = enable_siem
        
        # Set up syslog handler if enabled
        self.syslog_handler: Optional[logging.Handler] = None
        
        if self.enable_siem:
            try:
                self.syslog_handler = logging.handlers.SysLogHandler(
                    address=(self.siem_host, self.siem_port),
                    socktype=socket.SOCK_DGRAM
                )
                
                # JSON formatter for SIEM
                formatter = logging.Formatter(
                    '{"timestamp":"%(asctime)s","level":"%(levelname)s","message":%(message)s}'
                )
                self.syslog_handler.setFormatter(formatter)
                
                logger.info(
                    "siem_logging_enabled",
                    host=self.siem_host,
                    port=self.siem_port
                )
            except Exception as e:
                logger.error(
                    "siem_initialization_failed",
                    error=str(e),
                    host=self.siem_host,
                    port=self.siem_port
                )
                self.syslog_handler = None
        else:
            logger.info(
                "siem_logging_disabled",
                environment=self.environment
            )
    
    def log_event(
        self,
        event_type: str,
        user_id: str,
        action: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        facility_id: Optional[str] = None,
        status: str = "success",
        details: Optional[Dict[str, Any]] = None,
        severity: str = "info"
    ):
        """
        Log security audit event.
        
        Args:
            event_type: Event type (e.g., "video.created", "user.login")
            user_id: User who performed action
            action: Action performed (create, read, update, delete, etc.)
            resource_type: Type of resource (video, design, user, etc.)
            resource_id: Specific resource identifier
            facility_id: Facility context
            status: Status (success, failure, error)
            details: Additional event details
            severity: Log severity (info, warning, error, critical)
        """
        # Build structured audit event
        audit_event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "environment": self.environment,
            "application": "zorro",
            "event_type": event_type,
            "user_id": user_id,
            "action": action,
            "status": status,
            "severity": severity,
        }
        
        # Add optional fields
        if resource_type:
            audit_event["resource_type"] = resource_type
        if resource_id:
            audit_event["resource_id"] = resource_id
        if facility_id:
            audit_event["facility_id"] = facility_id
        if details:
            audit_event["details"] = details
        
        # Log to application logger
        log_level = getattr(logging, severity.upper(), logging.INFO)
        logger.log(
            log_level,
            "audit_event",
            **audit_event
        )
        
        # Send to SIEM if enabled
        if self.syslog_handler:
            try:
                # Create logger for SIEM
                siem_logger = logging.getLogger("siem")
                siem_logger.setLevel(logging.INFO)
                siem_logger.addHandler(self.syslog_handler)
                
                # Log to SIEM in JSON format
                siem_logger.log(
                    log_level,
                    json.dumps(audit_event)
                )
            except Exception as e:
                logger.error(
                    "siem_logging_failed",
                    error=str(e),
                    event_type=event_type
                )
    
    def log_access(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        granted: bool,
        reason: Optional[str] = None
    ):
        """
        Log access control decision.
        
        Args:
            user_id: User requesting access
            resource_type: Type of resource
            resource_id: Resource identifier
            action: Action attempted
            granted: Whether access was granted
            reason: Reason for denial (if applicable)
        """
        self.log_event(
            event_type="access.control",
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            status="granted" if granted else "denied",
            details={"reason": reason} if reason else None,
            severity="warning" if not granted else "info"
        )
    
    def log_authentication(
        self,
        user_id: str,
        auth_method: str,
        success: bool,
        ip_address: Optional[str] = None,
        failure_reason: Optional[str] = None
    ):
        """
        Log authentication attempt.
        
        Args:
            user_id: User attempting authentication
            auth_method: Authentication method (sso, password, mfa, etc.)
            success: Whether authentication succeeded
            ip_address: Source IP address
            failure_reason: Reason for failure (if applicable)
        """
        self.log_event(
            event_type="user.authentication",
            user_id=user_id,
            action="authenticate",
            status="success" if success else "failure",
            details={
                "auth_method": auth_method,
                "ip_address": ip_address,
                "failure_reason": failure_reason
            },
            severity="warning" if not success else "info"
        )
    
    def log_data_access(
        self,
        user_id: str,
        data_type: str,
        operation: str,
        record_count: int,
        filters: Optional[Dict[str, Any]] = None
    ):
        """
        Log data access for compliance.
        
        Args:
            user_id: User accessing data
            data_type: Type of data accessed
            operation: Operation (query, export, delete, etc.)
            record_count: Number of records accessed
            filters: Query filters applied
        """
        self.log_event(
            event_type="data.access",
            user_id=user_id,
            action=operation,
            resource_type=data_type,
            details={
                "record_count": record_count,
                "filters": filters
            }
        )


# Global audit logger instance
_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    """Get global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


def audit_log(
    event_type: str,
    action: str,
    user_id: Optional[str] = None,
    **kwargs
):
    """
    Convenience function for audit logging.
    
    Example:
        >>> audit_log("video.created", "create", user_id="jdoe", resource_id="vid_123")
    """
    # Get user from context if not provided
    if user_id is None:
        try:
            from .rbac import get_current_user
            user = get_current_user()
            user_id = user.user_id if user else "anonymous"
        except Exception:
            user_id = "system"
    
    audit_logger = get_audit_logger()
    audit_logger.log_event(
        event_type=event_type,
        user_id=user_id,
        action=action,
        **kwargs
    )


def log_event(event_type: str, **kwargs):
    """Alias for audit_log."""
    return audit_log(event_type, action=event_type.split(".")[-1], **kwargs)


def audit_decorator(event_type: str, resource_type: Optional[str] = None):
    """
    Decorator to automatically log function calls.
    
    Example:
        @audit_decorator("video.create", resource_type="video")
        def create_video(video_id):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get user context
            try:
                from .rbac import get_current_user
                user = get_current_user()
                user_id = user.user_id if user else "anonymous"
            except Exception:
                user_id = "system"
            
            # Execute function
            try:
                result = func(*args, **kwargs)
                
                # Log success
                audit_log(
                    event_type=event_type,
                    action=func.__name__,
                    user_id=user_id,
                    resource_type=resource_type,
                    status="success"
                )
                
                return result
            
            except Exception as e:
                # Log failure
                audit_log(
                    event_type=event_type,
                    action=func.__name__,
                    user_id=user_id,
                    resource_type=resource_type,
                    status="error",
                    details={"error": str(e)},
                    severity="error"
                )
                raise
        
        return wrapper
    return decorator
