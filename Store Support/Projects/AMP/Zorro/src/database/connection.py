"""Database connection management."""

import os
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool, QueuePool

from ..utils import get_logger

logger = get_logger(__name__)


class Database:
    """
    Database connection manager with connection pooling.
    
    Supports both PostgreSQL and SQLite (development fallback).
    
    Example:
        >>> db = Database()
        >>> with db.session() as session:
        ...     results = session.query(DesignElementDB).all()
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database connection.
        
        Args:
            database_url: Database URL (uses DATABASE_URL env var if None)
        """
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "sqlite:///data/zorro.db"  # Fallback to SQLite
        )
        
        # Parse database type
        self.db_type = self._get_db_type()
        
        # Create engine with appropriate pool settings
        self.engine = self._create_engine()
        
        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        logger.info(
            "database_initialized",
            db_type=self.db_type,
            pool_size=self.engine.pool.size() if hasattr(self.engine.pool, 'size') else 'N/A'
        )
    
    def _get_db_type(self) -> str:
        """Get database type from URL."""
        if self.database_url.startswith("postgresql"):
            return "postgresql"
        elif self.database_url.startswith("sqlite"):
            return "sqlite"
        else:
            return "unknown"
    
    def _create_engine(self) -> Engine:
        """Create SQLAlchemy engine with optimized settings."""
        engine_kwargs = {
            "echo": os.getenv("SQL_ECHO", "false").lower() == "true",
        }
        
        if self.db_type == "postgresql":
            # Production PostgreSQL settings
            pool_size = int(os.getenv("DATABASE_POOL_SIZE", "10"))
            max_overflow = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))
            
            engine_kwargs.update({
                "poolclass": QueuePool,
                "pool_size": pool_size,
                "max_overflow": max_overflow,
                "pool_pre_ping": True,  # Verify connections before use
                "pool_recycle": 3600,  # Recycle connections after 1 hour
            })
            
            logger.info(
                "postgresql_pool_configured",
                pool_size=pool_size,
                max_overflow=max_overflow
            )
        else:
            # SQLite development settings
            engine_kwargs.update({
                "poolclass": NullPool,  # SQLite doesn't benefit from pooling
                "connect_args": {"check_same_thread": False}
            })
            
            logger.warning(
                "sqlite_fallback",
                message="Using SQLite for development. Use PostgreSQL for production."
            )
        
        engine = create_engine(self.database_url, **engine_kwargs)
        
        # Add query logging for PostgreSQL in debug mode
        if self.db_type == "postgresql" and engine_kwargs.get("echo"):
            @event.listens_for(engine, "before_cursor_execute")
            def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
                logger.debug("sql_query", statement=statement[:200], params=str(params)[:100])
        
        return engine
    
    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """
        Provide a transactional scope for database operations.
        
        Yields:
            Session: SQLAlchemy session
            
        Example:
            >>> with db.session() as session:
            ...     element = session.query(DesignElementDB).first()
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error("database_transaction_failed", error=str(e))
            raise
        finally:
            session.close()
    
    def close(self):
        """Close all database connections."""
        self.engine.dispose()
        logger.info("database_connections_closed")


# Global database instance
_db: Optional[Database] = None


def get_db() -> Database:
    """
    Get global database instance (singleton pattern).
    
    Returns:
        Database: Global database instance
        
    Example:
        >>> db = get_db()
        >>> with db.session() as session:
        ...     ...
    """
    global _db
    if _db is None:
        _db = Database()
    return _db
