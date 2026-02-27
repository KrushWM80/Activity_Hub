"""Security module for Zorro platform.

Provides:
- Secret management (Azure Key Vault)
- SSL/TLS configuration
- Role-Based Access Control (RBAC)
- PII detection and masking
- SIEM audit logging
"""

from .secrets import SecretManager, get_secret
from .ssl_config import SSLConfiguration, ssl_config
from .rbac import Role, Permission, RBACManager, require_permission, get_current_user
from .pii_detector import PIIDetector, detect_pii, mask_pii
from .audit_logger import AuditLogger, audit_log, log_event

__all__ = [
    "SecretManager",
    "get_secret",
    "SSLConfiguration",
    "ssl_config",
    "Role",
    "Permission",
    "RBACManager",
    "require_permission",
    "get_current_user",
    "PIIDetector",
    "detect_pii",
    "mask_pii",
    "AuditLogger",
    "audit_log",
    "log_event",
]