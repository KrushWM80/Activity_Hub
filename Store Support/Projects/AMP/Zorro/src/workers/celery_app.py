"""Celery application configuration for async video generation."""

import os
from celery import Celery

# Initialize Celery app
celery_app = Celery(
    "zorro",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
    include=["src.workers.tasks"]
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Result backend settings
    result_expires=3600,  # Results expire after 1 hour
    result_persistent=True,
    
    # Task execution settings
    task_acks_late=True,  # Acknowledge after task completes
    task_reject_on_worker_lost=True,
    task_track_started=True,
    
    # Worker settings
    worker_prefetch_multiplier=1,  # One task at a time (videos are heavy)
    worker_max_tasks_per_child=10,  # Restart worker after 10 tasks (memory cleanup)
    
    # Retry settings
    task_default_retry_delay=60,  # Retry after 1 minute
    task_max_retries=3,
    
    # Time limits
    task_soft_time_limit=600,  # 10 minutes soft limit
    task_time_limit=900,  # 15 minutes hard limit
)

# Task routes
celery_app.conf.task_routes = {
    "src.workers.tasks.generate_video_async": {"queue": "videos"},
    "src.workers.tasks.batch_generate_videos": {"queue": "batch"},
}

if __name__ == "__main__":
    celery_app.start()