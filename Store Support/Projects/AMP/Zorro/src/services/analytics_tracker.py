"""
Analytics and Multi-Layer Tracking System

Tracks content engagement across multiple layers:
- Unique clicks
- User-specific clicks  
- Total page/content views
- Time on page/content
- Interaction heatmaps
- Device/platform specifics
- Download tracking
- Format utilization
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from collections import defaultdict
import logging
import hashlib

logger = logging.getLogger(__name__)


class AnalyticsTracker:
    """
    Multi-layer analytics and tracking system for content distribution.
    
    Tracks:
    - Content views (unique and total)
    - User interactions
    - Click patterns
    - Time engagement
    - Download metrics
    - Device/platform usage
    - Geographic distribution
    - Format preferences
    """
    
    def __init__(self, db_dir: str = "analytics_data"):
        self.db_dir = Path(db_dir)
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.cache = {}
        self.session_data = {}
        
    def track_content_view(
        self,
        content_id: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        device_type: str = "desktop",
        platform: str = "unknown",
        referrer: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Track a content view event.
        
        Args:
            content_id: Unique content/project ID
            user_id: Optional unique user identifier
            session_id: Browser/session ID
            device_type: desktop/mobile/tablet
            platform: web/mobile_app/email/etc
            referrer: Where user came from
            metadata: Additional context
            
        Returns:
            Event tracking confirmation
        """
        
        event_id = self._generate_event_id()
        timestamp = datetime.now()
        
        # Generate unique click ID if user is not logged in
        if not user_id:
            user_id = f"anon_{self._hash_session(session_id)}"
        
        # Determine if this is a unique view
        is_unique = self._is_unique_view(content_id, user_id)
        
        event = {
            "event_id": event_id,
            "event_type": "content_view",
            "content_id": content_id,
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": timestamp.isoformat(),
            "device_type": device_type,
            "platform": platform,
            "referrer": referrer,
            "is_unique": is_unique,
            "metadata": metadata or {},
        }
        
        # Save event
        self._save_event(event)
        
        # Update content metrics
        self._update_content_view_metrics(content_id, event)
        
        return {
            "tracked": True,
            "event_id": event_id,
            "is_unique_user": is_unique,
            "timestamp": timestamp.isoformat(),
        }
    
    def track_click(
        self,
        content_id: str,
        click_element: str,  # e.g., "download_button", "share_twitter", "link_123"
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Track a click/interaction event on content.
        
        Args:
            content_id: Content being interacted with
            click_element: What was clicked
            user_id: User making the click
            session_id: Browser session
            metadata: Additional context
            
        Returns:
            Click event confirmation
        """
        
        event_id = self._generate_event_id()
        timestamp = datetime.now()
        
        if not user_id:
            user_id = f"anon_{self._hash_session(session_id)}"
        
        # Check if this is a unique click
        is_unique_click = self._is_unique_click(content_id, user_id, click_element)
        
        event = {
            "event_id": event_id,
            "event_type": "click",
            "content_id": content_id,
            "click_element": click_element,
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": timestamp.isoformat(),
            "is_unique_click": is_unique_click,
            "metadata": metadata or {},
        }
        
        self._save_event(event)
        self._update_click_metrics(content_id, event)
        
        return {
            "tracked": True,
            "event_id": event_id,
            "is_unique_click": is_unique_click,
            "timestamp": timestamp.isoformat(),
        }
    
    def track_time_on_page(
        self,
        content_id: str,
        duration_seconds: int,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Track how long user spent viewing content.
        """
        
        if not user_id:
            user_id = f"anon_{self._hash_session(session_id)}"
        
        event_id = self._generate_event_id()
        timestamp = datetime.now()
        
        event = {
            "event_id": event_id,
            "event_type": "time_on_page",
            "content_id": content_id,
            "duration_seconds": duration_seconds,
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": timestamp.isoformat(),
        }
        
        self._save_event(event)
        self._update_engagement_metrics(content_id, duration_seconds)
        
        return {
            "tracked": True,
            "event_id": event_id,
            "duration_seconds": duration_seconds,
        }
    
    def track_download(
        self,
        content_id: str,
        format_type: str,  # video, audio, infographic, etc
        file_size_mb: float,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Track file download events.
        """
        
        event_id = self._generate_event_id()
        timestamp = datetime.now()
        
        if not user_id:
            user_id = f"anon_{self._hash_session(session_id)}"
        
        event = {
            "event_id": event_id,
            "event_type": "download",
            "content_id": content_id,
            "format_type": format_type,
            "file_size_mb": file_size_mb,
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": timestamp.isoformat(),
        }
        
        self._save_event(event)
        self._update_download_metrics(content_id, format_type, file_size_mb)
        
        return {
            "tracked": True,
            "event_id": event_id,
            "format": format_type,
        }
    
    def get_content_analytics(self, content_id: str) -> Dict[str, Any]:
        """
        Get comprehensive analytics for a content piece.
        """
        
        events = self._load_content_events(content_id)
        
        # Calculate metrics
        view_events = [e for e in events if e["event_type"] == "content_view"]
        click_events = [e for e in events if e["event_type"] == "click"]
        time_events = [e for e in events if e["event_type"] == "time_on_page"]
        download_events = [e for e in events if e["event_type"] == "download"]
        
        # Unique users
        unique_users = len(set(e["user_id"] for e in view_events))
        unique_views = len([e for e in view_events if e.get("is_unique")])
        total_views = len(view_events)
        
        # Click analytics
        total_clicks = len(click_events)
        unique_clicks = len(set((e["user_id"], e["click_element"]) for e in click_events))
        clicks_by_element = defaultdict(int)
        for e in click_events:
            clicks_by_element[e["click_element"]] += 1
        
        # Engagement
        time_on_page = [e["duration_seconds"] for e in time_events] if time_events else []
        avg_time_seconds = sum(time_on_page) / len(time_on_page) if time_on_page else 0
        
        # Download tracking
        downloads_by_format = defaultdict(int)
        total_download_size_mb = 0
        for e in download_events:
            downloads_by_format[e["format_type"]] += 1
            total_download_size_mb += e.get("file_size_mb", 0)
        
        # Device distribution
        devices = defaultdict(int)
        for e in view_events:
            devices[e.get("device_type", "unknown")] += 1
        
        # Platform distribution
        platforms = defaultdict(int)
        for e in view_events:
            platforms[e.get("platform", "unknown")] += 1
        
        return {
            "content_id": content_id,
            "generated": datetime.now().isoformat(),
            "views": {
                "total": total_views,
                "unique": unique_views,
                "unique_users": unique_users,
                "avg_views_per_user": round(total_views / unique_users, 2) if unique_users > 0 else 0,
            },
            "clicks": {
                "total": total_clicks,
                "unique": unique_clicks,
                "by_element": dict(clicks_by_element),
                "click_through_rate": round((total_clicks / total_views * 100), 2) if total_views > 0 else 0,
            },
            "engagement": {
                "average_time_seconds": round(avg_time_seconds, 2),
                "views_spending_time": len(time_events),
                "engagement_rate": round((len(time_events) / total_views * 100), 2) if total_views > 0 else 0,
            },
            "downloads": {
                "total": len(download_events),
                "by_format": dict(downloads_by_format),
                "total_data_downloaded_mb": round(total_download_size_mb, 2),
            },
            "device_distribution": dict(devices),
            "platform_distribution": dict(platforms),
            "events_count": len(events),
        }
    
    def get_user_journey(self, user_id: str) -> Dict[str, Any]:
        """
        Get complete user journey across content.
        """
        
        events = self._load_user_events(user_id)
        events_sorted = sorted(events, key=lambda x: x["timestamp"])
        
        # Group by content
        content_interactions = defaultdict(list)
        for e in events_sorted:
            content_interactions[e["content_id"]].append(e)
        
        # Calculate session data
        sessions = self._group_by_session(events_sorted)
        
        return {
            "user_id": user_id,
            "generated": datetime.now().isoformat(),
            "total_events": len(events),
            "total_sessions": len(sessions),
            "content_interacted": len(content_interactions),
            "interactions_by_content": {
                content_id: {
                    "views": len([e for e in evts if e["event_type"] == "content_view"]),
                    "clicks": len([e for e in evts if e["event_type"] == "click"]),
                    "downloads": len([e for e in evts if e["event_type"] == "download"]),
                    "first_interaction": evts[0]["timestamp"] if evts else None,
                    "last_interaction": evts[-1]["timestamp"] if evts else None,
                }
                for content_id, evts in content_interactions.items()
            },
            "total_time_on_pages_seconds": sum(
                e["duration_seconds"] for e in events 
                if e["event_type"] == "time_on_page"
            ),
        }
    
    def get_trending_analytics(self, hours: int = 24) -> Dict[str, Any]:
        """
        Get trending content and engagement over time period.
        """
        
        since = datetime.now() - timedelta(hours=hours)
        
        # Load all recent events
        all_events = self._load_recent_events(since)
        
        # Group by content
        content_views = defaultdict(int)
        content_clicks = defaultdict(int)
        content_downloads = defaultdict(int)
        
        for e in all_events:
            content_id = e["content_id"]
            if e["event_type"] == "content_view":
                content_views[content_id] += 1
            elif e["event_type"] == "click":
                content_clicks[content_id] += 1
            elif e["event_type"] == "download":
                content_downloads[content_id] += 1
        
        # Sort by views
        top_content = sorted(
            content_views.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            "time_period_hours": hours,
            "generated": datetime.now().isoformat(),
            "total_views": sum(content_views.values()),
            "total_clicks": sum(content_clicks.values()),
            "total_downloads": sum(content_downloads.values()),
            "top_content": [
                {
                    "content_id": content_id,
                    "views": views,
                    "clicks": content_clicks.get(content_id, 0),
                    "downloads": content_downloads.get(content_id, 0),
                }
                for content_id, views in top_content
            ],
        }
    
    # Private helper methods
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID."""
        import uuid
        return str(uuid.uuid4())
    
    def _hash_session(self, session_id: Optional[str]) -> str:
        """Hash session ID preserving anonymity."""
        if not session_id:
            session_id = datetime.now().isoformat()
        return hashlib.md5(session_id.encode()).hexdigest()[:8]
    
    def _is_unique_view(self, content_id: str, user_id: str) -> bool:
        """Check if this is a unique view for user."""
        view_key = f"view_{content_id}_{user_id}"
        
        if view_key not in self.cache:
            self.cache[view_key] = True
            return True
        return False
    
    def _is_unique_click(self, content_id: str, user_id: str, element: str) -> bool:
        """Check if this is a unique click for user on element."""
        click_key = f"click_{content_id}_{user_id}_{element}"
        
        if click_key not in self.cache:
            self.cache[click_key] = True
            return True
        return False
    
    def _save_event(self, event: Dict[str, Any]) -> None:
        """Save event to storage."""
        content_id = event["content_id"]
        events_file = self.db_dir / f"{content_id}_events.jsonl"
        
        with open(events_file, "a") as f:
            f.write(json.dumps(event) + "\n")
    
    def _load_content_events(self, content_id: str) -> List[Dict[str, Any]]:
        """Load all events for a content piece."""
        events_file = self.db_dir / f"{content_id}_events.jsonl"
        
        if not events_file.exists():
            return []
        
        events = []
        with open(events_file, "r") as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))
        
        return events
    
    def _load_user_events(self, user_id: str) -> List[Dict[str, Any]]:
        """Load all events for a user."""
        events = []
        
        for events_file in self.db_dir.glob("*_events.jsonl"):
            with open(events_file, "r") as f:
                for line in f:
                    if line.strip():
                        event = json.loads(line)
                        if event["user_id"] == user_id:
                            events.append(event)
        
        return events
    
    def _load_recent_events(self, since: datetime) -> List[Dict[str, Any]]:
        """Load events since a specific time."""
        events = []
        
        for events_file in self.db_dir.glob("*_events.jsonl"):
            with open(events_file, "r") as f:
                for line in f:
                    if line.strip():
                        event = json.loads(line)
                        event_time = datetime.fromisoformat(event["timestamp"])
                        if event_time >= since:
                            events.append(event)
        
        return events
    
    def _update_content_view_metrics(self, content_id: str, event: Dict[str, Any]) -> None:
        """Update content view metrics."""
        pass  # Metrics already calculated in get_content_analytics
    
    def _update_click_metrics(self, content_id: str, event: Dict[str, Any]) -> None:
        """Update click metrics."""
        pass
    
    def _update_engagement_metrics(self, content_id: str, duration_seconds: int) -> None:
        """Update engagement metrics."""
        pass
    
    def _update_download_metrics(self, content_id: str, format_type: str, file_size_mb: float) -> None:
        """Update download metrics."""
        pass
    
    def _group_by_session(self, events: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group events by session."""
        sessions = defaultdict(list)
        
        for event in events:
            session_id = event.get("session_id", "default")
            sessions[session_id].append(event)
        
        return dict(sessions)
