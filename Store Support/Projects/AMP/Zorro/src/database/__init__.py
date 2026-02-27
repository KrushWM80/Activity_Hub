"""
Database module for Zorro platform.

Provides PostgreSQL database connectivity and ORM models for:
- Design elements storage
- Video generation history
- User activity tracking
- Analytics and metrics
"""

from .connection import Database, get_db
from .models import DesignElementDB, VideoGenerationDB, UserActivityDB
from .migrations import run_migrations

__all__ = [
    "Database",
    "get_db",
    "DesignElementDB",
    "VideoGenerationDB",
    "UserActivityDB",
    "run_migrations",
]
