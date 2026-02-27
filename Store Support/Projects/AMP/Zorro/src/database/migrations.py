"""Database migrations for Zorro platform."""

import json
from pathlib import Path
from typing import List

from sqlalchemy import text

from ..utils import get_logger
from .connection import Database
from .models import Base, DesignElementDB

logger = get_logger(__name__)


def run_migrations(db: Database):
    """
    Run all database migrations.
    
    Creates tables and performs any necessary schema updates.
    
    Args:
        db: Database instance
    """
    logger.info("running_migrations")
    
    # Create all tables
    Base.metadata.create_all(bind=db.engine)
    logger.info("tables_created")
    
    # Run data migrations
    migrate_json_to_db(db)
    
    logger.info("migrations_complete")


def migrate_json_to_db(db: Database):
    """
    Migrate design elements from JSON file to database.
    
    Reads data/design_library.json and imports into database.
    One-time migration for existing data.
    
    Args:
        db: Database instance
    """
    json_file = Path("data/design_library.json")
    
    if not json_file.exists():
        logger.info("no_json_file_to_migrate")
        return
    
    logger.info("migrating_json_to_database", file=str(json_file))
    
    # Read JSON data
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    elements = data.get("elements", [])
    
    if not elements:
        logger.info("no_elements_to_migrate")
        return
    
    # Import elements
    with db.session() as session:
        migrated_count = 0
        skipped_count = 0
        
        for element_data in elements:
            element_id = element_data.get("id")
            
            # Check if already exists
            existing = session.query(DesignElementDB).filter_by(id=element_id).first()
            if existing:
                logger.debug("element_already_exists", id=element_id)
                skipped_count += 1
                continue
            
            # Create new element
            element = DesignElementDB(
                id=element_id,
                name=element_data.get("name"),
                type=element_data.get("type"),
                description=element_data.get("description"),
                prompt=element_data.get("prompt"),
                category=element_data.get("category"),
                tags=element_data.get("tags", []),
                created_by=element_data.get("created_by", "system"),
                facility_id=element_data.get("facility_id"),
                status=element_data.get("status", "approved"),
                approved_by=element_data.get("approved_by"),
                metadata=element_data.get("metadata", {}),
                usage_count=element_data.get("usage_count", 0),
                visibility=element_data.get("visibility", "company"),
            )
            
            session.add(element)
            migrated_count += 1
            logger.debug("element_migrated", id=element_id, name=element.name)
        
        session.commit()
        
        logger.info(
            "json_migration_complete",
            migrated=migrated_count,
            skipped=skipped_count,
            total=len(elements)
        )


def create_indexes(db: Database):
    """
    Create additional database indexes for performance.
    
    Args:
        db: Database instance
    """
    logger.info("creating_indexes")
    
    # Only for PostgreSQL
    if db.db_type != "postgresql":
        logger.info("skipping_indexes_for_sqlite")
        return
    
    indexes = [
        # Design elements
        "CREATE INDEX IF NOT EXISTS idx_design_created_at ON design_elements(created_at DESC)",
        "CREATE INDEX IF NOT EXISTS idx_design_status_facility ON design_elements(status, facility_id)",
        
        # Video generations
        "CREATE INDEX IF NOT EXISTS idx_video_created_at ON video_generations(created_at DESC)",
        "CREATE INDEX IF NOT EXISTS idx_video_user ON video_generations(created_by, created_at DESC)",
        "CREATE INDEX IF NOT EXISTS idx_video_status ON video_generations(status, created_at DESC)",
        
        # User activities
        "CREATE INDEX IF NOT EXISTS idx_activity_user_time ON user_activities(user_id, timestamp DESC)",
        "CREATE INDEX IF NOT EXISTS idx_activity_action_time ON user_activities(action, timestamp DESC)",
    ]
    
    with db.engine.connect() as conn:
        for index_sql in indexes:
            try:
                conn.execute(text(index_sql))
                conn.commit()
                logger.debug("index_created", sql=index_sql[:80])
            except Exception as e:
                logger.warning("index_creation_failed", sql=index_sql[:80], error=str(e))
    
    logger.info("indexes_created")


def backup_json_file():
    """
    Backup the JSON file before migration.
    
    Creates a timestamped backup in data/backups/
    """
    from datetime import datetime
    
    json_file = Path("data/design_library.json")
    
    if not json_file.exists():
        return
    
    backup_dir = Path("data/backups")
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"design_library_{timestamp}.json"
    
    import shutil
    shutil.copy2(json_file, backup_file)
    
    logger.info("json_backed_up", backup_file=str(backup_file))
