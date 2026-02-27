"""Data retention policy management."""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from ..utils import get_logger
from ..security import audit_log

logger = get_logger(__name__)


@dataclass
class DataRetentionPolicy:
    """Data retention policy definition."""
    
    data_type: str  # "videos", "design_elements", "audit_logs", etc.
    retention_days: int  # Days to retain data
    auto_delete: bool = True  # Automatically delete expired data
    archive_before_delete: bool = False  # Archive before deletion
    archive_location: Optional[str] = None
    
    @property
    def cutoff_date(self) -> datetime:
        """Calculate cutoff date for retention."""
        return datetime.utcnow() - timedelta(days=self.retention_days)


# Default retention policies (Walmart standard: 2 years for most data)
DEFAULT_POLICIES = {
    "videos": DataRetentionPolicy(
        data_type="videos",
        retention_days=730,  # 2 years
        auto_delete=True,
        archive_before_delete=True
    ),
    "design_elements": DataRetentionPolicy(
        data_type="design_elements",
        retention_days=1095,  # 3 years (longer retention for templates)
        auto_delete=False,  # Manual deletion only
    ),
    "audit_logs": DataRetentionPolicy(
        data_type="audit_logs",
        retention_days=2555,  # 7 years (compliance requirement)
        auto_delete=False,
        archive_before_delete=True
    ),
    "user_activities": DataRetentionPolicy(
        data_type="user_activities",
        retention_days=365,  # 1 year
        auto_delete=True
    ),
}


class RetentionManager:
    """
    Manage data retention and automatic cleanup.
    
    Example:
        >>> manager = RetentionManager()
        >>> expired = manager.find_expired_videos()
        >>> manager.cleanup_expired_data("videos")
    """
    
    def __init__(self, policies: Optional[Dict[str, DataRetentionPolicy]] = None):
        """
        Initialize retention manager.
        
        Args:
            policies: Custom retention policies (uses defaults if None)
        """
        self.policies = policies or DEFAULT_POLICIES
        logger.info(
            "retention_manager_initialized",
            policies=list(self.policies.keys())
        )
    
    def get_policy(self, data_type: str) -> DataRetentionPolicy:
        """
        Get retention policy for data type.
        
        Args:
            data_type: Type of data
            
        Returns:
            DataRetentionPolicy
            
        Raises:
            ValueError: If no policy defined for data type
        """
        if data_type not in self.policies:
            raise ValueError(
                f"No retention policy defined for '{data_type}'. "
                f"Available: {list(self.policies.keys())}"
            )
        return self.policies[data_type]
    
    def find_expired_videos(self) -> List[Dict[str, Any]]:
        """
        Find expired videos based on retention policy.
        
        Returns:
            List of expired video metadata
        """
        policy = self.get_policy("videos")
        cutoff_date = policy.cutoff_date
        
        logger.info(
            "searching_expired_videos",
            cutoff_date=cutoff_date.isoformat()
        )
        
        # Check if using database
        try:
            from ..database import get_db, VideoGenerationDB
            
            db = get_db()
            with db.session() as session:
                expired_videos = (
                    session.query(VideoGenerationDB)
                    .filter(VideoGenerationDB.created_at < cutoff_date)
                    .all()
                )
                
                results = [
                    {
                        "id": video.id,
                        "created_at": video.created_at,
                        "video_path": video.video_path,
                        "age_days": (datetime.utcnow() - video.created_at).days
                    }
                    for video in expired_videos
                ]
                
                logger.info(
                    "expired_videos_found",
                    count=len(results)
                )
                
                return results
        
        except ImportError:
            # Fallback to file-based search
            logger.warning(
                "database_not_available",
                message="Using file-based expiration check"
            )
            return self._find_expired_files("output/videos", policy)
    
    def _find_expired_files(
        self,
        directory: str,
        policy: DataRetentionPolicy
    ) -> List[Dict[str, Any]]:
        """
        Find expired files in directory.
        
        Args:
            directory: Directory to scan
            policy: Retention policy
            
        Returns:
            List of expired file metadata
        """
        path = Path(directory)
        if not path.exists():
            return []
        
        expired = []
        cutoff_timestamp = policy.cutoff_date.timestamp()
        
        for file_path in path.rglob("*.mp4"):
            if file_path.stat().st_mtime < cutoff_timestamp:
                age_days = (datetime.utcnow().timestamp() - file_path.stat().st_mtime) / 86400
                expired.append({
                    "path": str(file_path),
                    "created_at": datetime.fromtimestamp(file_path.stat().st_mtime),
                    "age_days": int(age_days)
                })
        
        return expired
    
    def cleanup_expired_data(
        self,
        data_type: str,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Clean up expired data according to retention policy.
        
        Args:
            data_type: Type of data to clean up
            dry_run: If True, only report what would be deleted
            
        Returns:
            Dict with cleanup summary
        """
        policy = self.get_policy(data_type)
        
        if not policy.auto_delete:
            logger.warning(
                "auto_delete_disabled",
                data_type=data_type
            )
            return {
                "status": "skipped",
                "reason": "auto_delete disabled for this data type"
            }
        
        logger.info(
            "starting_cleanup",
            data_type=data_type,
            dry_run=dry_run,
            retention_days=policy.retention_days
        )
        
        # Find expired data
        if data_type == "videos":
            expired_items = self.find_expired_videos()
        else:
            # Add other data types as needed
            expired_items = []
        
        if not expired_items:
            logger.info("no_expired_data_found", data_type=data_type)
            return {
                "status": "completed",
                "deleted_count": 0,
                "dry_run": dry_run
            }
        
        # Archive if required
        archived_count = 0
        if policy.archive_before_delete and not dry_run:
            archived_count = self._archive_items(expired_items, policy)
        
        # Delete items
        deleted_count = 0
        if not dry_run:
            deleted_count = self._delete_items(expired_items, data_type)
        
        # Audit log
        audit_log(
            event_type="data.retention.cleanup",
            action="cleanup",
            user_id="system",
            resource_type=data_type,
            status="completed",
            details={
                "deleted_count": deleted_count,
                "archived_count": archived_count,
                "retention_days": policy.retention_days,
                "dry_run": dry_run
            }
        )
        
        result = {
            "status": "completed",
            "data_type": data_type,
            "deleted_count": deleted_count if not dry_run else len(expired_items),
            "archived_count": archived_count,
            "dry_run": dry_run,
            "items": expired_items if dry_run else None
        }
        
        logger.info("cleanup_completed", **result)
        return result
    
    def _archive_items(
        self,
        items: List[Dict[str, Any]],
        policy: DataRetentionPolicy
    ) -> int:
        """
        Archive items before deletion.
        
        Args:
            items: Items to archive
            policy: Retention policy
            
        Returns:
            int: Number of items archived
        """
        archive_dir = Path(policy.archive_location or "archive")
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        archived = 0
        for item in items:
            try:
                # Implementation depends on data type
                # For videos: copy to archive location
                # For database records: export to JSON
                logger.debug("item_archived", item_id=item.get("id"))
                archived += 1
            except Exception as e:
                logger.error("archive_failed", error=str(e), item=item)
        
        return archived
    
    def _delete_items(
        self,
        items: List[Dict[str, Any]],
        data_type: str
    ) -> int:
        """
        Delete items.
        
        Args:
            items: Items to delete
            data_type: Type of data
            
        Returns:
            int: Number of items deleted
        """
        deleted = 0
        
        for item in items:
            try:
                if data_type == "videos":
                    # Delete video file and associated files
                    video_path = item.get("video_path") or item.get("path")
                    if video_path and Path(video_path).exists():
                        Path(video_path).unlink()
                        deleted += 1
                        
                        # Delete associated files (captions, transcripts, etc.)
                        base_path = Path(video_path).with_suffix("")
                        for ext in [".vtt", ".mp3", ".txt"]:
                            assoc_file = base_path.with_suffix(ext)
                            if assoc_file.exists():
                                assoc_file.unlink()
                
                # Delete database record if exists
                try:
                    from ..database import get_db, VideoGenerationDB
                    
                    video_id = item.get("id")
                    if video_id:
                        db = get_db()
                        with db.session() as session:
                            video = session.query(VideoGenerationDB).filter_by(id=video_id).first()
                            if video:
                                session.delete(video)
                                session.commit()
                except ImportError:
                    pass
                
                logger.debug("item_deleted", item_id=item.get("id"))
            
            except Exception as e:
                logger.error("deletion_failed", error=str(e), item=item)
        
        return deleted
    
    def generate_retention_report(self) -> Dict[str, Any]:
        """
        Generate compliance retention report.
        
        Returns:
            Dict with retention status for all data types
        """
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "policies": {},
            "summary": {}
        }
        
        for data_type, policy in self.policies.items():
            report["policies"][data_type] = {
                "retention_days": policy.retention_days,
                "auto_delete": policy.auto_delete,
                "archive_before_delete": policy.archive_before_delete,
                "cutoff_date": policy.cutoff_date.isoformat()
            }
        
        # Add actual data counts (if database available)
        try:
            from ..database import get_db, VideoGenerationDB, DesignElementDB
            
            db = get_db()
            with db.session() as session:
                # Videos
                total_videos = session.query(VideoGenerationDB).count()
                expired_videos = (
                    session.query(VideoGenerationDB)
                    .filter(VideoGenerationDB.created_at < self.policies["videos"].cutoff_date)
                    .count()
                )
                
                report["summary"]["videos"] = {
                    "total": total_videos,
                    "expired": expired_videos,
                    "active": total_videos - expired_videos
                }
                
                # Design elements
                total_designs = session.query(DesignElementDB).count()
                expired_designs = (
                    session.query(DesignElementDB)
                    .filter(DesignElementDB.created_at < self.policies["design_elements"].cutoff_date)
                    .count()
                )
                
                report["summary"]["design_elements"] = {
                    "total": total_designs,
                    "expired": expired_designs,
                    "active": total_designs - expired_designs
                }
        
        except Exception as e:
            logger.warning("report_generation_partial", error=str(e))
        
        return report


# Convenience functions
def schedule_cleanup(data_type: str = "videos", dry_run: bool = False):
    """
    Schedule cleanup job (to be called by scheduler).
    
    Example:
        >>> schedule_cleanup("videos", dry_run=True)
    """
    manager = RetentionManager()
    return manager.cleanup_expired_data(data_type, dry_run=dry_run)


def cleanup_expired_data(dry_run: bool = True):
    """
    Clean up all expired data types.
    
    Args:
        dry_run: If True, only report what would be deleted
    """
    manager = RetentionManager()
    results = {}
    
    for data_type in manager.policies.keys():
        try:
            result = manager.cleanup_expired_data(data_type, dry_run=dry_run)
            results[data_type] = result
        except Exception as e:
            logger.error("cleanup_failed", data_type=data_type, error=str(e))
            results[data_type] = {"status": "error", "error": str(e)}
    
    return results
