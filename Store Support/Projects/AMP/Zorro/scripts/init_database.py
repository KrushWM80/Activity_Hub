#!/usr/bin/env python
"""
Initialize Zorro database.

Creates tables, runs migrations, and imports existing JSON data.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import get_db, run_migrations
from src.database.migrations import backup_json_file, create_indexes
from src.utils import get_logger

logger = get_logger(__name__)


def main():
    """Initialize database."""
    print("=" * 60)
    print("Zorro Database Initialization")
    print("=" * 60)
    print()
    
    # Get database instance
    try:
        db = get_db()
        print(f"✓ Connected to database: {db.db_type}")
        print(f"  URL: {db.database_url.split('@')[-1] if '@' in db.database_url else 'SQLite'}")
        print()
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print()
        print("Make sure DATABASE_URL is set in .env file:")
        print("  DATABASE_URL=postgresql://user:password@localhost:5432/zorro")
        return 1
    
    # Backup JSON file
    print("Step 1: Backing up JSON data...")
    try:
        backup_json_file()
        print("✓ JSON backup created")
    except Exception as e:
        print(f"✗ Backup failed: {e}")
    print()
    
    # Run migrations
    print("Step 2: Running migrations...")
    try:
        run_migrations(db)
        print("✓ Migrations complete")
        print("  - Tables created")
        print("  - JSON data imported")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        logger.error("migration_failed", error=str(e))
        return 1
    print()
    
    # Create indexes
    print("Step 3: Creating performance indexes...")
    try:
        create_indexes(db)
        print("✓ Indexes created")
    except Exception as e:
        print(f"⚠ Index creation failed: {e}")
        print("  (Non-critical, continuing...)")
    print()
    
    # Verify setup
    print("Step 4: Verifying setup...")
    try:
        from src.database.models import DesignElementDB
        with db.session() as session:
            count = session.query(DesignElementDB).count()
            print(f"✓ Database operational")
            print(f"  Design elements: {count}")
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return 1
    print()
    
    print("=" * 60)
    print("✓ Database initialization complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Start Celery worker: celery -A src.workers.celery_app worker --loglevel=info")
    print("  2. Start Streamlit app: streamlit run app.py")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
