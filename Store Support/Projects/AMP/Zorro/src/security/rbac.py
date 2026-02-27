"""Role-Based Access Control (RBAC) system."""

import os
from enum import Enum
from typing import List, Optional, Set
from dataclasses import dataclass
from functools import wraps

import streamlit as st

from ..utils import get_logger

logger = get_logger(__name__)


class Role(str, Enum):
    """User roles in Zorro platform."""
    
    ADMIN = "admin"  # Full system access
    FACILITY_MANAGER = "facility_manager"  # Manage facility content
    CREATOR = "creator"  # Create and edit videos
    VIEWER = "viewer"  # View only
    
    def __str__(self) -> str:
        return self.value


class Permission(str, Enum):
    """System permissions."""
    
    # Video operations
    VIDEO_CREATE = "video:create"
    VIDEO_EDIT = "video:edit"
    VIDEO_DELETE = "video:delete"
    VIDEO_VIEW = "video:view"
    
    # Design elements
    DESIGN_CREATE = "design:create"
    DESIGN_EDIT = "design:edit"
    DESIGN_DELETE = "design:delete"
    DESIGN_APPROVE = "design:approve"
    DESIGN_VIEW = "design:view"
    
    # System administration
    SYSTEM_CONFIG = "system:config"
    USER_MANAGE = "user:manage"
    AUDIT_VIEW = "audit:view"
    
    def __str__(self) -> str:
        return self.value


# Role to permissions mapping
ROLE_PERMISSIONS: dict[Role, Set[Permission]] = {
    Role.ADMIN: {
        # All permissions
        Permission.VIDEO_CREATE,
        Permission.VIDEO_EDIT,
        Permission.VIDEO_DELETE,
        Permission.VIDEO_VIEW,
        Permission.DESIGN_CREATE,
        Permission.DESIGN_EDIT,
        Permission.DESIGN_DELETE,
        Permission.DESIGN_APPROVE,
        Permission.DESIGN_VIEW,
        Permission.SYSTEM_CONFIG,
        Permission.USER_MANAGE,
        Permission.AUDIT_VIEW,
    },
    Role.FACILITY_MANAGER: {
        Permission.VIDEO_CREATE,
        Permission.VIDEO_EDIT,
        Permission.VIDEO_DELETE,
        Permission.VIDEO_VIEW,
        Permission.DESIGN_CREATE,
        Permission.DESIGN_EDIT,
        Permission.DESIGN_APPROVE,  # Can approve for facility
        Permission.DESIGN_VIEW,
        Permission.AUDIT_VIEW,  # Can view facility audits
    },
    Role.CREATOR: {
        Permission.VIDEO_CREATE,
        Permission.VIDEO_EDIT,
        Permission.VIDEO_VIEW,
        Permission.DESIGN_CREATE,
        Permission.DESIGN_EDIT,
        Permission.DESIGN_VIEW,
    },
    Role.VIEWER: {
        Permission.VIDEO_VIEW,
        Permission.DESIGN_VIEW,
    },
}


@dataclass
class UserContext:
    """Current user context."""
    
    user_id: str
    username: str
    email: str
    role: Role
    facility_id: Optional[str] = None
    is_authenticated: bool = True
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission."""
        return permission in ROLE_PERMISSIONS.get(self.role, set())
    
    def has_any_permission(self, permissions: List[Permission]) -> bool:
        """Check if user has any of the specified permissions."""
        return any(self.has_permission(p) for p in permissions)
    
    def has_all_permissions(self, permissions: List[Permission]) -> bool:
        """Check if user has all of the specified permissions."""
        return all(self.has_permission(p) for p in permissions)


class RBACManager:
    """
    Manage role-based access control.
    
    Example:
        >>> rbac = RBACManager()
        >>> user = rbac.get_current_user()
        >>> if rbac.check_permission(user, Permission.VIDEO_CREATE):
        ...     # Allow video creation
    """
    
    @staticmethod
    def get_current_user() -> Optional[UserContext]:
        """
        Get current user from session state.
        
        Returns:
            UserContext or None if not authenticated
        """
        # Check if user is in Streamlit session
        if "user" in st.session_state:
            return st.session_state.user
        
        # Development mode: Create mock user
        if os.getenv("ZORRO_ENV") == "development":
            mock_role = os.getenv("MOCK_USER_ROLE", Role.CREATOR.value)
            return UserContext(
                user_id="dev_user",
                username="Developer",
                email="developer@walmart.com",
                role=Role(mock_role),
                facility_id="0001"
            )
        
        return None
    
    @staticmethod
    def check_permission(user: UserContext, permission: Permission) -> bool:
        """
        Check if user has permission.
        
        Args:
            user: User context
            permission: Required permission
            
        Returns:
            bool: True if user has permission
        """
        has_perm = user.has_permission(permission)
        
        logger.debug(
            "permission_check",
            user_id=user.user_id,
            permission=str(permission),
            granted=has_perm
        )
        
        return has_perm
    
    @staticmethod
    def require_permission(permission: Permission, error_message: str = None):
        """
        Decorator to require permission for a function.
        
        Args:
            permission: Required permission
            error_message: Custom error message
            
        Example:
            @require_permission(Permission.VIDEO_CREATE)
            def create_video():
                ...
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                user = RBACManager.get_current_user()
                
                if not user:
                    st.error("Authentication required. Please log in.")
                    st.stop()
                
                if not user.has_permission(permission):
                    msg = error_message or f"Permission denied: {permission.value}"
                    logger.warning(
                        "permission_denied",
                        user_id=user.user_id,
                        permission=str(permission)
                    )
                    st.error(msg)
                    st.stop()
                
                return func(*args, **kwargs)
            
            return wrapper
        return decorator


# Convenience functions
def get_current_user() -> Optional[UserContext]:
    """Get current authenticated user."""
    return RBACManager.get_current_user()


def require_permission(permission: Permission, error_message: str = None):
    """Decorator to require permission."""
    return RBACManager.require_permission(permission, error_message)


def check_permission(permission: Permission) -> bool:
    """
    Check if current user has permission.
    
    Returns:
        bool: True if user has permission
    """
    user = get_current_user()
    if not user:
        return False
    return RBACManager.check_permission(user, permission)
