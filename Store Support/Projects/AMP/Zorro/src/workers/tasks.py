"""Celery tasks for async video generation."""

import traceback
from typing import Dict, List, Any

from celery import Task
from celery.utils.log import get_task_logger

from .celery_app import celery_app
from ..core.pipeline import VideoGenerationPipeline
from ..models.video_models import VideoPrompt
from ..database import get_db, VideoGenerationDB

logger = get_task_logger(__name__)


class VideoGenerationTask(Task):
    """Base task class with common error handling."""
    
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3, "countdown": 60}
    retry_backoff = True
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure."""
        logger.error(
            f"Task {task_id} failed: {exc}",
            exc_info=True
        )
        
        # Update database status
        video_id = kwargs.get("video_id") or (args[0] if args else None)
        if video_id:
            try:
                db = get_db()
                with db.session() as session:
                    video = session.query(VideoGenerationDB).filter_by(id=video_id).first()
                    if video:
                        video.status = "failed"
                        video.error_message = str(exc)
                        video.retry_count = self.request.retries
                        session.commit()
            except Exception as e:
                logger.error(f"Failed to update video status: {e}")


@celery_app.task(base=VideoGenerationTask, bind=True, name="src.workers.tasks.generate_video_async")
def generate_video_async(self, video_id: str, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate video asynchronously.
    
    Args:
        video_id: Unique video identifier
        prompt_data: Video prompt data dictionary
        
    Returns:
        Dict with video generation results
        
    Example:
        >>> from src.workers.tasks import generate_video_async
        >>> result = generate_video_async.delay(
        ...     video_id="vid_123",
        ...     prompt_data={"enhanced_prompt": "...", ...}
        ... )
        >>> result.get()  # Wait for completion
    """
    logger.info(f"Starting async video generation: {video_id}")
    
    try:
        # Update status to generating
        db = get_db()
        with db.session() as session:
            video = session.query(VideoGenerationDB).filter_by(id=video_id).first()
            if video:
                video.status = "generating"
                from datetime import datetime
                video.started_at = datetime.utcnow()
                session.commit()
        
        # Initialize pipeline
        pipeline = VideoGenerationPipeline()
        
        # Reconstruct VideoPrompt from data
        prompt = VideoPrompt(**prompt_data)
        
        # Generate video
        result = pipeline.generate_from_prompt(prompt)
        
        # Update database with results
        with db.session() as session:
            video = session.query(VideoGenerationDB).filter_by(id=video_id).first()
            if video:
                video.status = "completed"
                video.video_path = str(result.path)
                video.thumbnail_path = str(result.thumbnail) if result.thumbnail else None
                video.captions_path = str(result.accessibility.captions_path) if result.accessibility else None
                video.audio_desc_path = str(result.accessibility.audio_description_path) if result.accessibility else None
                video.transcript_path = str(result.accessibility.transcript_path) if result.accessibility else None
                video.file_size_bytes = result.metadata.get("file_size_bytes")
                video.resolution = result.metadata.get("resolution")
                video.fps = result.metadata.get("fps")
                from datetime import datetime
                video.completed_at = datetime.utcnow()
                session.commit()
        
        logger.info(f"Video generation completed: {video_id}")
        
        return {
            "status": "success",
            "video_id": video_id,
            "video_path": str(result.path),
            "duration": result.duration,
        }
        
    except Exception as e:
        logger.error(f"Video generation failed: {video_id} - {e}")
        logger.error(traceback.format_exc())
        
        # Update retry count
        try:
            db = get_db()
            with db.session() as session:
                video = session.query(VideoGenerationDB).filter_by(id=video_id).first()
                if video:
                    video.retry_count = self.request.retries + 1
                    session.commit()
        except Exception:
            pass
        
        raise


@celery_app.task(name="src.workers.tasks.batch_generate_videos")
def batch_generate_videos(video_requests: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate multiple videos in batch.
    
    Args:
        video_requests: List of video generation requests
        
    Returns:
        Dict with batch generation summary
        
    Example:
        >>> requests = [
        ...     {"video_id": "vid_1", "prompt_data": {...}},
        ...     {"video_id": "vid_2", "prompt_data": {...}},
        ... ]
        >>> result = batch_generate_videos.delay(requests)
    """
    logger.info(f"Starting batch generation: {len(video_requests)} videos")
    
    results = {
        "total": len(video_requests),
        "succeeded": 0,
        "failed": 0,
        "task_ids": []
    }
    
    # Queue individual video generation tasks
    for request in video_requests:
        try:
            task = generate_video_async.delay(
                video_id=request["video_id"],
                prompt_data=request["prompt_data"]
            )
            results["task_ids"].append(task.id)
            logger.info(f"Queued video: {request['video_id']} - Task: {task.id}")
        except Exception as e:
            logger.error(f"Failed to queue video: {request['video_id']} - {e}")
            results["failed"] += 1
    
    results["succeeded"] = len(results["task_ids"])
    
    logger.info(
        f"Batch queued: {results['succeeded']} succeeded, {results['failed']} failed"
    )
    
    return results